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
"""Font / Text Renderer (REQ-0012).

Font resolution chain:
  1. Named font (truetype via ImageFont.truetype)
  2. System generic family: serif / sans-serif / monospace
  3. Final fallback: ImageFont.load_default()

Multi-line text: split on \\n; repeat ImageDraw.text() at font_size × 1.2 spacing.
"""

from __future__ import annotations

import math
import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import ColorValue, LengthValue, PointValue, StringValue, IdentValue
from imagegen.rendering.primitives.line_renderer import _resolve_color
from imagegen.font_discovery import find_font_file

if TYPE_CHECKING:
    from imagegen.ast_nodes import FontNode
    from imagegen.error_reporter import ErrorReporter

# Generic CSS family names → ordered list of real family names to try
_GENERIC_FONTS: dict[str, list[str]] = {
    "sans-serif":  ["Arial", "Helvetica", "DejaVu Sans", "FreeSans"],
    "serif":       ["Times New Roman", "Georgia", "DejaVu Serif", "FreeSerif"],
    "monospace":   ["Courier New", "Consolas", "DejaVu Sans Mono", "FreeMono"],
}


def _style_label(style: str, weight: str) -> str:
    """Map (style, weight) DSL values to a font_discovery style label."""
    bold = weight == "bold"
    italic = style == "italic"
    if bold and italic:
        return "bold-italic"
    if bold:
        return "bold"
    if italic:
        return "italic"
    return "normal"


def _family_chain(font_family: str) -> list[str]:
    """Expand a comma-separated DSL font-family string into individual names.

    Generic CSS families (sans-serif, serif, monospace) are expanded to their
    real family equivalents so find_font_file() can locate them on disk.
    """
    names: list[str] = []
    for raw in font_family.split(","):
        name = raw.strip().strip('"').strip("'")
        if name in _GENERIC_FONTS:
            names.extend(_GENERIC_FONTS[name])
        else:
            names.append(name)
    return names


class FontRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: FontNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params

        font_family_val = params.get("font-family")
        font_family = font_family_val.value if isinstance(font_family_val, StringValue) else "sans-serif"
        font_size_val = params.get("font-size")
        font_size = self._px(canvas, font_size_val) if isinstance(font_size_val, LengthValue) else self._s(canvas, 12)
        color_val = params.get("color")
        style_val = params.get("style")
        style = style_val.name if isinstance(style_val, IdentValue) else "normal"
        weight_val = params.get("weight")
        weight = weight_val.name if isinstance(weight_val, IdentValue) else "normal"
        align_val = params.get("align")
        align = align_val.name if isinstance(align_val, IdentValue) else "left"
        text_val = params.get("text")
        text = text_val.value if isinstance(text_val, StringValue) else ""
        pos_val = params.get("pos")
        pos_x = self._px(canvas, pos_val.x) if isinstance(pos_val, PointValue) else 0
        pos_y = self._px(canvas, pos_val.y) if isinstance(pos_val, PointValue) else 0

        scale_val = params.get("scale")
        scale = float(scale_val.number) if isinstance(scale_val, LengthValue) else 1.0
        effective_font_size = max(1, int(font_size * scale))

        rotate_val = params.get("rotate")
        rotate = float(rotate_val.number) if isinstance(rotate_val, LengthValue) else 0.0

        skew_x_val = params.get("skew-x")
        skew_x = float(skew_x_val.number) if isinstance(skew_x_val, LengthValue) else 0.0
        skew_y_val = params.get("skew-y")
        skew_y = float(skew_y_val.number) if isinstance(skew_y_val, LengthValue) else 0.0

        font = self._resolve_font(font_family, effective_font_size, style, weight)
        color = _resolve_color(color_val, canvas.mode) if isinstance(color_val, ColorValue) else (0, 0, 0)

        if skew_x != 0.0 or skew_y != 0.0:
            self._render_skewed(canvas, text, (pos_x, pos_y), font, color, align, effective_font_size, skew_x, skew_y, rotate)
        elif rotate != 0.0:
            self._render_rotated(canvas, text, (pos_x, pos_y), font, color, align, effective_font_size, rotate)
        else:
            draw = ImageDraw.Draw(canvas)
            self._render_multiline(draw, text, (pos_x, pos_y), font, color, align, effective_font_size)

    @staticmethod
    def _measure_lines(
        text: str,
        font: ImageFont.ImageFont,
    ) -> list[int]:
        probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        return [
            max(1, probe.textbbox((0, 0), ln, font=font)[2] - probe.textbbox((0, 0), ln, font=font)[0])
            for ln in text.split("\n")
        ]

    @staticmethod
    def _aligned_anchor_x(
        anchor_x: int,
        block_width: int,
        align: str,
    ) -> int:
        if align == "center":
            return anchor_x - block_width // 2
        if align == "right":
            return anchor_x - block_width
        return anchor_x

    @staticmethod
    def _surface_line_x(
        surface_width: int,
        line_width: int,
        align: str,
    ) -> int:
        if align == "center":
            return (surface_width - line_width) // 2
        if align == "right":
            return surface_width - line_width
        return 0

    def _resolve_font(
        self,
        font_family: str,
        font_size: int,
        style: str,
        weight: str,
    ) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Font resolution chain: named → generic family → default fallback.

        Resolves each family name to an actual font file path via the
        font_discovery index so that the correct glyph set (including
        non-ASCII / Hungarian characters) is loaded.
        """
        style_label = _style_label(style, weight)
        for name in _family_chain(font_family):
            path = find_font_file(name, style_label)
            if path:
                try:
                    return ImageFont.truetype(path, font_size)
                except (OSError, IOError):
                    continue
        # Final fallback — Pillow built-in bitmap font (ASCII only)
        return ImageFont.load_default()

    def _render_skewed(
        self,
        canvas: Image.Image,
        text: str,
        pos: tuple[int, int],
        font: ImageFont.ImageFont,
        color: tuple | int,
        align: str,
        font_size: int,
        skew_x: float,
        skew_y: float,
        rotate: float,
    ) -> None:
        lines = text.split("\n")
        line_height = int(font_size * 1.2)

        line_widths = self._measure_lines(text, font)
        text_w = max(line_widths)
        text_h = line_height * len(lines)

        surf = Image.new("RGBA", (max(1, text_w), max(1, text_h)), (0, 0, 0, 0))
        surf_draw = ImageDraw.Draw(surf)
        y = 0
        for ln, line_width in zip(lines, line_widths):
            surf_draw.text((self._surface_line_x(text_w, line_width, align), y), ln, fill=color, font=font)
            y += line_height

        # Apply affine shear (same convention as square_renderer._apply_skew).
        tan_x = math.tan(math.radians(skew_x))
        tan_y = math.tan(math.radians(skew_y))
        w, h = surf.size
        extra_w = math.ceil(abs(tan_x) * h)
        extra_h = math.ceil(abs(tan_y) * w)
        cx = -extra_w if tan_x >= 0 else 0
        fy = -extra_h if tan_y >= 0 else 0
        surf = surf.transform(
            (w + extra_w, h + extra_h),
            Image.AFFINE,
            (1, tan_x, cx, tan_y, 1, fy),
            Image.BICUBIC,
        )

        # Optional rotation on top of skew (DSL clockwise → PIL negate).
        if rotate != 0.0:
            surf = surf.rotate(-rotate, expand=True, resample=Image.BICUBIC)

        canvas_rgba = canvas.convert("RGBA")
        anchor_x = self._aligned_anchor_x(pos[0], text_w, align)
        canvas_rgba.paste(surf, (anchor_x, pos[1]), surf)
        canvas.paste(canvas_rgba.convert(canvas.mode))

    def _render_rotated(
        self,
        canvas: Image.Image,
        text: str,
        pos: tuple[int, int],
        font: ImageFont.ImageFont,
        color: tuple | int,
        align: str,
        font_size: int,
        rotate: float,
    ) -> None:
        lines = text.split("\n")
        line_height = int(font_size * 1.2)

        # Measure each line to size the temporary surface.
        line_widths = self._measure_lines(text, font)
        text_w = max(line_widths)
        text_h = line_height * len(lines)

        # Render text onto a transparent RGBA surface.
        surf = Image.new("RGBA", (max(1, text_w), max(1, text_h)), (0, 0, 0, 0))
        surf_draw = ImageDraw.Draw(surf)
        y = 0
        for ln, line_width in zip(lines, line_widths):
            surf_draw.text((self._surface_line_x(text_w, line_width, align), y), ln, fill=color, font=font)
            y += line_height

        # Rotate clockwise: DSL is clockwise, PIL is counter-clockwise → negate.
        rotated = surf.rotate(-rotate, expand=True, resample=Image.BICUBIC)

        # Keep the center of the aligned unrotated text block fixed at the requested anchor.
        anchor_x = self._aligned_anchor_x(pos[0], text_w, align)
        cx = anchor_x + text_w // 2
        cy = pos[1] + text_h // 2
        px = cx - rotated.width // 2
        py = cy - rotated.height // 2

        canvas_rgba = canvas.convert("RGBA")
        canvas_rgba.paste(rotated, (px, py), rotated)
        canvas.paste(canvas_rgba.convert(canvas.mode))

    @staticmethod
    def _render_multiline(
        draw: ImageDraw.Draw,
        text: str,
        pos: tuple[int, int],
        font: ImageFont.ImageFont,
        color: tuple | int,
        align: str,
        font_size: int,
    ) -> None:
        """Split on \\n and draw each line at font_size × 1.2 spacing."""
        line_height = int(font_size * 1.2)
        x, y = pos
        for line in text.split("\n"):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = max(1, bbox[2] - bbox[0])
            draw_x = FontRenderer._aligned_anchor_x(x, line_width, align)
            draw.text((draw_x, y), line, fill=color, font=font)
            y += line_height
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
