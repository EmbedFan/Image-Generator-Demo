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
"""Square Renderer (REQ-0007) — filled or stroked rectangle; no corner radius."""

from __future__ import annotations

import math
import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFilter

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import ColorValue, ColorNone, LengthValue, PointValue, ShadowValue
from imagegen.rendering.primitives.line_renderer import _resolve_color

if TYPE_CHECKING:
    from imagegen.ast_nodes import SquareNode
    from imagegen.error_reporter import ErrorReporter


def _apply_skew(img: Image.Image, skew_x: float, skew_y: float) -> Image.Image:
    tan_x = math.tan(math.radians(skew_x))
    tan_y = math.tan(math.radians(skew_y))
    w, h = img.size
    extra_w = math.ceil(abs(tan_x) * h)
    extra_h = math.ceil(abs(tan_y) * w)
    cx = -extra_w if tan_x >= 0 else 0
    fy = -extra_h if tan_y >= 0 else 0
    data = (1, tan_x, cx, tan_y, 1, fy)
    return img.transform((w + extra_w, h + extra_h), Image.AFFINE, data, Image.BICUBIC)


class SquareRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: SquareNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params
        color = params.get("color")
        fill = params.get("fill")
        pos = params.get("pos")
        width_val = params.get("width")
        height_val = params.get("height")
        line_width = self._px(canvas, params["line-width"]) if isinstance(params.get("line-width"), LengthValue) else canvas.info.get("aa_scale", 1)

        x = self._px(canvas, pos.x) if isinstance(pos, PointValue) else 0
        y = self._px(canvas, pos.y) if isinstance(pos, PointValue) else 0
        w = self._px(canvas, width_val) if isinstance(width_val, LengthValue) else self._s(canvas, 100)
        h = self._px(canvas, height_val) if isinstance(height_val, LengthValue) else self._s(canvas, 100)

        if w <= 0 or h <= 0:
            self._reporter.runtime_error(
                node.source_file, node.line,
                f"square: width and height must be > 0 after evaluation, got width={w}, height={h}"
            )

        stroke_color = _resolve_color(color, "RGBA") if isinstance(color, ColorValue) else None
        fill_color: tuple | None = None
        if fill is not None and not isinstance(fill, ColorNone):
            fill_color = _resolve_color(fill, "RGBA") if isinstance(fill, ColorValue) else None
        shadow = params.get("shadow")
        has_shadow = isinstance(shadow, ShadowValue) and shadow.color.a > 0.0

        scale_val = params.get("scale")
        scale = float(scale_val.number) if isinstance(scale_val, LengthValue) else 1.0
        skew_x_val = params.get("skew-x")
        skew_x = float(skew_x_val.number) if isinstance(skew_x_val, LengthValue) else 0.0
        skew_y_val = params.get("skew-y")
        skew_y = float(skew_y_val.number) if isinstance(skew_y_val, LengthValue) else 0.0
        rotate_val = params.get("rotate")
        rotate = float(rotate_val.number) if isinstance(rotate_val, LengthValue) else 0.0

        if scale == 1.0 and skew_x == 0.0 and skew_y == 0.0 and rotate == 0.0 and not has_shadow:
            # Fast path: no transforms — draw directly at canvas coordinates (REQ-0007).
            temp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            ImageDraw.Draw(temp).rectangle(
                [x, y, x + w - 1, y + h - 1],
                fill=fill_color, outline=stroke_color, width=line_width,
            )
            canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), temp).convert(canvas.mode))
        else:
            # Transform/shadow path: isolated surface → optional shadow → scale → skew → rotate → composite.
            surf, rect_x, rect_y = self._build_surface(w, h, line_width, fill_color, stroke_color, shadow, canvas)
            rect_cx = rect_x + w // 2
            rect_cy = rect_y + h // 2

            if scale != 1.0 and scale > 0:
                surf = surf.resize(
                    (max(1, int(surf.width * scale)), max(1, int(surf.height * scale))), Image.LANCZOS
                )
                rect_cx = int(rect_cx * scale)
                rect_cy = int(rect_cy * scale)
            if skew_x != 0.0 or skew_y != 0.0:
                surf = _apply_skew(surf, skew_x, skew_y)
            if rotate != 0.0:
                pre_w, pre_h = surf.width, surf.height
                surf = surf.rotate(-rotate, expand=True, resample=Image.BICUBIC)
                rect_cx += (surf.width - pre_w) // 2
                rect_cy += (surf.height - pre_h) // 2

            # Composite anchored on the rectangle center rather than the shadow surface center.
            elem_cx = x + w // 2
            elem_cy = y + h // 2
            px = elem_cx - rect_cx
            py = elem_cy - rect_cy
            canvas_rgba = canvas.convert("RGBA")
            canvas_rgba.paste(surf, (px, py), surf)
            canvas.paste(canvas_rgba.convert(canvas.mode))

    def _build_surface(
        self,
        w: int,
        h: int,
        line_width: int,
        fill_color: tuple | None,
        stroke_color: tuple | None,
        shadow: object,
        canvas: Image.Image,
    ) -> tuple[Image.Image, int, int]:
        if not isinstance(shadow, ShadowValue) or shadow.color.a <= 0.0:
            surf = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ImageDraw.Draw(surf).rectangle(
                [0, 0, w - 1, h - 1],
                fill=fill_color, outline=stroke_color, width=line_width,
            )
            return surf, 0, 0

        dx = self._px(canvas, shadow.dx)
        dy = self._px(canvas, shadow.dy)
        blur = max(0, self._px(canvas, shadow.blur))
        margin = blur * 3
        left_pad = margin + max(0, -dx)
        top_pad = margin + max(0, -dy)
        right_pad = margin + max(0, dx)
        bottom_pad = margin + max(0, dy)

        surf = Image.new("RGBA", (w + left_pad + right_pad, h + top_pad + bottom_pad), (0, 0, 0, 0))
        rect_x = left_pad
        rect_y = top_pad

        shadow_layer = Image.new("RGBA", surf.size, (0, 0, 0, 0))
        shadow_color = _resolve_color(shadow.color, "RGBA")
        ImageDraw.Draw(shadow_layer).rectangle(
            [rect_x + dx, rect_y + dy, rect_x + dx + w - 1, rect_y + dy + h - 1],
            fill=shadow_color,
        )
        if blur > 0:
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=blur))
        surf = Image.alpha_composite(surf, shadow_layer)

        ImageDraw.Draw(surf).rectangle(
            [rect_x, rect_y, rect_x + w - 1, rect_y + h - 1],
            fill=fill_color, outline=stroke_color, width=line_width,
        )
        return surf, rect_x, rect_y
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
