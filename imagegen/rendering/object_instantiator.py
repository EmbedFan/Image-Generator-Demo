# =============================================================================
# DSL-demo-v1.x
# This version is a public demo version: DSL-demo-v1.x
#
# Created by Attila Gallai using AI aided software development process
# Copyright Attila Gallai (C) 1995 - 2026
#
# -----------------------------------------------------------------------------
# Minimal MIT License
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following condition:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# =============================================================================
"""Object Instantiator (REQ-0014, REQ-0014.1-REQ-0014.4).

Steps per instantiation:
  1. Lookup template in symbol_table.objects.
  2. Deep-copy template attributes; apply instance param overrides.
  3. Apply clip-bounds and/or clip-shape.
     When both are present the effective clip region is their intersection (REQ-0014.2).
  4. Execute template body drawing commands via the dispatcher.

Note: clip-shape=polygon is a validation error caught by SemanticValidator - not
handled here. Only 'circle' and 'square' are valid clip shapes.
"""

from __future__ import annotations

import copy
import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFilter

from imagegen.ast_nodes import (
    ExprFactor,
    FuncCall,
    IdentValue,
    LengthValue,
    NamedDrawCmd,
    ObjectInst,
    PointList,
    ShadowValue,
)

if TYPE_CHECKING:
    from imagegen.error_reporter import ErrorReporter
    from imagegen.rendering.primitive_dispatcher import PrimitiveDispatcher
    from imagegen.symbol_table import SymbolTable


def _unwrap_length(val: object) -> LengthValue | None:
    """Accept LengthValue or ExprFactor(LengthValue) produced by in_func_body parsing."""
    if isinstance(val, LengthValue):
        return val
    if isinstance(val, ExprFactor) and isinstance(val.value, LengthValue):
        return val.value
    return None


def _unwrap_ident_name(val: object) -> str | None:
    """Accept IdentValue or ExprFactor(str) for enum-like object-inst params."""
    if isinstance(val, IdentValue):
        return val.name
    if isinstance(val, ExprFactor) and isinstance(val.value, str):
        return val.value
    return None


class ObjectInstantiator:
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    def instantiate(
        self,
        canvas: Image.Image,
        node: ObjectInst,
        symbol_table: SymbolTable,
        dispatcher: PrimitiveDispatcher,
        base_dir: pathlib.Path,
        frame_index: int,
    ) -> None:
        """Lookup, merge params, apply clip, execute body."""
        template = symbol_table.lookup_object(node.name)
        if template is None:
            self._reporter.validation_error(
                node.source_file, node.line,
                f"undefined object template '{node.name}'"
            )

        merged = self._merge_params(template, node.params)
        aa_scale = canvas.info.get("aa_scale", 1)

        native_w_attr = next((a.value for a in template.attributes if a.key == "width"), None)
        native_h_attr = next((a.value for a in template.attributes if a.key == "height"), None)
        native_w_px = native_w_attr.number if isinstance(native_w_attr, LengthValue) else canvas.width / aa_scale
        native_h_px = native_h_attr.number if isinstance(native_h_attr, LengthValue) else canvas.height / aa_scale

        resize_mode = _unwrap_ident_name(node.params.get("resize-mode")) or "default"
        w_lv = _unwrap_length(node.params.get("width"))
        h_lv = _unwrap_length(node.params.get("height"))
        has_explicit_w = w_lv is not None
        has_explicit_h = h_lv is not None
        scale_lv = _unwrap_length(node.params.get("scale"))

        layout_w_px = w_lv.number if has_explicit_w else native_w_px
        layout_h_px = h_lv.number if has_explicit_h else native_h_px

        if resize_mode == "layout":
            render_w_px = layout_w_px
            render_h_px = layout_h_px
            geometric_scale = scale_lv.number if scale_lv is not None else 1.0
            final_w_px = render_w_px * geometric_scale
            final_h_px = render_h_px * geometric_scale
        else:
            render_w_px = native_w_px
            render_h_px = native_h_px
            if scale_lv is not None and not (has_explicit_w or has_explicit_h):
                geometric_scale = scale_lv.number
                final_w_px = native_w_px * geometric_scale
                final_h_px = native_h_px * geometric_scale
            elif has_explicit_w or has_explicit_h:
                final_w_px = layout_w_px
                final_h_px = layout_h_px
            else:
                final_w_px = native_w_px
                final_h_px = native_h_px

        render_w = max(1, int(round(render_w_px * aa_scale)))
        render_h = max(1, int(round(render_h_px * aa_scale)))
        final_w = max(1, int(round(final_w_px * aa_scale)))
        final_h = max(1, int(round(final_h_px * aa_scale)))

        obj_canvas = Image.new("RGBA", (render_w, render_h), (0, 0, 0, 0))
        obj_canvas.info["aa_scale"] = aa_scale

        body_attrs = copy.deepcopy(merged)
        if resize_mode == "layout":
            body_attrs["width"] = copy.deepcopy(w_lv) if has_explicit_w else copy.deepcopy(native_w_attr)
            body_attrs["height"] = copy.deepcopy(h_lv) if has_explicit_h else copy.deepcopy(native_h_attr)
            if body_attrs["width"] is None:
                body_attrs["width"] = LengthValue(number=render_w_px, unit="px")
            if body_attrs["height"] is None:
                body_attrs["height"] = LengthValue(number=render_h_px, unit="px")
        else:
            if native_w_attr is not None:
                body_attrs["width"] = copy.deepcopy(native_w_attr)
            if native_h_attr is not None:
                body_attrs["height"] = copy.deepcopy(native_h_attr)

        resolved_body = [
            self._resolve_object_attrs(cmd, body_attrs)
            for cmd in template.body
        ]

        dispatcher.dispatch_all(obj_canvas, resolved_body, symbol_table, base_dir, frame_index)
        obj_canvas = self._apply_clip(obj_canvas, body_attrs, aa_scale)

        if obj_canvas.size != (final_w, final_h):
            obj_canvas = obj_canvas.resize((final_w, final_h), Image.LANCZOS)

        shadow_pad_x = 0
        shadow_pad_y = 0
        obj_canvas, shadow_pad_x, shadow_pad_y = self._apply_object_shadow(obj_canvas, merged, aa_scale)

        rotate_lv = _unwrap_length(node.params.get("rotate"))
        if rotate_lv is not None and rotate_lv.number != 0:
            pre_w, pre_h = obj_canvas.width, obj_canvas.height
            obj_canvas = obj_canvas.rotate(-rotate_lv.number, expand=True, resample=Image.BICUBIC)
            rotation_offset_x = (obj_canvas.width - pre_w) // 2
            rotation_offset_y = (obj_canvas.height - pre_h) // 2
        else:
            rotation_offset_x = 0
            rotation_offset_y = 0

        pos_val = node.params.get("pos")
        px = int(round(pos_val.x.number * aa_scale)) if hasattr(pos_val, "x") else 0
        py = int(round(pos_val.y.number * aa_scale)) if hasattr(pos_val, "y") else 0

        px -= shadow_pad_x
        py -= shadow_pad_y
        px -= rotation_offset_x
        py -= rotation_offset_y

        alpha = obj_canvas.split()[3]
        canvas.paste(obj_canvas.convert(canvas.mode), (px, py), alpha)

    @staticmethod
    def _merge_params(template, overrides: dict) -> dict:
        """Deep-copy template attributes into a flat dict; apply instance overrides."""
        merged: dict = {}
        for attr in template.attributes:
            merged[attr.key] = copy.deepcopy(attr.value)
        merged.update(overrides)
        return merged

    def _resolve_object_attrs(self, cmd: object, merged: dict) -> object:
        """Substitute IdentValue references to object attributes inside body commands."""
        if isinstance(cmd, NamedDrawCmd):
            resolved_inner = self._resolve_object_attrs(cmd.cmd, merged)
            if resolved_inner is cmd.cmd:
                return cmd
            return NamedDrawCmd(
                binding_name=cmd.binding_name,
                cmd=resolved_inner,
                source_file=cmd.source_file,
                line=cmd.line,
            )

        if isinstance(cmd, FuncCall):
            resolved_args = tuple(self._resolve_object_attr_value(arg, merged) for arg in cmd.args)
            if resolved_args == cmd.args:
                return cmd
            return FuncCall(
                name=cmd.name,
                args=resolved_args,
                source_file=cmd.source_file,
                line=cmd.line,
            )

        if isinstance(cmd, ObjectInst):
            resolved_params = {
                key: self._resolve_object_attr_value(value, merged)
                for key, value in cmd.params.items()
            }
            if resolved_params == cmd.params:
                return cmd
            return ObjectInst(
                name=cmd.name,
                params=resolved_params,
                source_file=cmd.source_file,
                line=cmd.line,
            )

        params = getattr(cmd, "params", None)
        if not isinstance(params, dict):
            return cmd

        resolved_params = {
            key: self._resolve_object_attr_value(value, merged)
            for key, value in params.items()
        }
        if resolved_params == params:
            return cmd
        return type(cmd)(params=resolved_params, source_file=cmd.source_file, line=cmd.line)

    def _resolve_object_attr_value(self, value: object, merged: dict) -> object:
        """Replace IdentValue(name=<attr>) with the merged object attribute value."""
        if isinstance(value, IdentValue) and value.name in merged:
            return copy.deepcopy(merged[value.name])
        return value

    def _apply_object_shadow(
        self,
        obj_canvas: Image.Image,
        attrs: dict,
        aa_scale: int,
    ) -> tuple[Image.Image, int, int]:
        """Apply a shadow around the fully rendered object without clipping it."""
        shadow = attrs.get("shadow")
        if not isinstance(shadow, ShadowValue) or shadow.color.a <= 0.0:
            return obj_canvas, 0, 0

        dx = int(round(shadow.dx.number * aa_scale))
        dy = int(round(shadow.dy.number * aa_scale))
        blur = max(0, int(round(shadow.blur.number * aa_scale)))
        margin = blur * 3
        left_pad = margin + max(0, -dx)
        top_pad = margin + max(0, -dy)
        right_pad = margin + max(0, dx)
        bottom_pad = margin + max(0, dy)

        w, h = obj_canvas.size
        out = Image.new("RGBA", (w + left_pad + right_pad, h + top_pad + bottom_pad), (0, 0, 0, 0))

        alpha = obj_canvas.convert("RGBA").split()[3]
        shadow_mask = Image.new("L", out.size, 0)
        shadow_mask.paste(alpha, (left_pad + dx, top_pad + dy))
        if blur > 0:
            shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(radius=blur))

        shadow_rgba = Image.new(
            "RGBA",
            out.size,
            (
                shadow.color.r,
                shadow.color.g,
                shadow.color.b,
                int(round(shadow.color.a * 255)),
            ),
        )
        shadow_rgba.putalpha(shadow_mask)
        out = Image.alpha_composite(out, shadow_rgba)
        out.paste(obj_canvas.convert("RGBA"), (left_pad, top_pad), obj_canvas.convert("RGBA"))
        return out, left_pad, top_pad

    def _apply_clip(self, obj_canvas: Image.Image, attrs: dict, aa_scale: int = 1) -> Image.Image:
        """Apply clip-bounds and/or clip-shape.

        When both are present, the effective region is their intersection (REQ-0014.2).
        clip-shape=polygon is a validation error caught before reaching here.
        """
        w, h = obj_canvas.size

        bounds_mask = None
        shape_mask = None

        clip_bounds = attrs.get("clip-bounds")
        if isinstance(clip_bounds, PointList) and len(clip_bounds.points) == 2:
            p1, p2 = clip_bounds.points
            x1 = int(min(p1.x.number, p2.x.number) * aa_scale)
            y1 = int(min(p1.y.number, p2.y.number) * aa_scale)
            x2 = int(max(p1.x.number, p2.x.number) * aa_scale)
            y2 = int(max(p1.y.number, p2.y.number) * aa_scale)
            bounds_mask = Image.new("L", (w, h), 0)
            ImageDraw.Draw(bounds_mask).rectangle([x1, y1, x2, y2], fill=255)

        clip_shape = attrs.get("clip-shape")
        if isinstance(clip_shape, IdentValue):
            shape_mask = Image.new("L", (w, h), 0)
            draw = ImageDraw.Draw(shape_mask)
            if clip_shape.name == "circle":
                r = min(w, h) // 2
                cx, cy = w // 2, h // 2
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
            elif clip_shape.name == "square":
                side = min(w, h)
                ox = (w - side) // 2
                oy = (h - side) // 2
                draw.rectangle([ox, oy, ox + side, oy + side], fill=255)

        if bounds_mask is not None and shape_mask is not None:
            from PIL import ImageChops
            mask = ImageChops.multiply(bounds_mask, shape_mask)
        elif bounds_mask is not None:
            mask = bounds_mask
        elif shape_mask is not None:
            mask = shape_mask
        else:
            return obj_canvas

        rgba = obj_canvas.convert("RGBA")
        rgba.putalpha(mask)
        return rgba.convert(obj_canvas.mode) if obj_canvas.mode != "RGBA" else rgba
# =============================================================================
# DSL-demo-v1.x
# This version is a public demo version: DSL-demo-v1.x
#
# Created by Attila Gallai using AI aided software development process
# Copyright Attila Gallai (C) 1995 - 2026
#
# -----------------------------------------------------------------------------
# Minimal MIT License
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, subject to the following condition:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# =============================================================================
