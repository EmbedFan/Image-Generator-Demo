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
"""Background Renderer — applies solid, gradient, or image-file backgrounds.

Gradient identical start/end edge case: warning is emitted by SemanticValidator;
here we detect it again and fill with color1 silently (REQ-0004.2).

Image background modes (REQ-0004.3):
  'fit'     — scale to fit inside canvas preserving aspect ratio; pad with default fill
  'stretch' — scale to exactly fill canvas ignoring aspect ratio
  'clip'    — scale so the shorter dimension fills, then centre-crop
"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.ast_nodes import ColorValue, ColorNone, PointValue, LengthValue, IdentValue

if TYPE_CHECKING:
    from imagegen.ast_nodes import Background, Value
    from imagegen.error_reporter import ErrorReporter


def _color_tuple(c: ColorValue, mode: str) -> tuple:
    """Convert ColorValue to a PIL colour tuple for the given mode."""
    if mode == "RGBA":
        return (c.r, c.g, c.b, int(c.a * 255))
    if mode == "L":
        # CCIR 601 luminance
        lum = int(0.299 * c.r + 0.587 * c.g + 0.114 * c.b)
        return lum
    return (c.r, c.g, c.b)


class BackgroundRenderer:
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    def render(
        self,
        canvas: Image.Image,
        node: Background,
        base_dir: pathlib.Path,
    ) -> None:
        """Dispatch to _render_solid, _render_gradient, or _render_image."""
        params = node.params

        if "src" in params:
            src_val = params["src"]
            src_str = src_val.value if hasattr(src_val, "value") else str(src_val)
            src_path = (base_dir / src_str).resolve()
            mode_val = params.get("mode")
            mode = mode_val.name if isinstance(mode_val, IdentValue) else "fit"
            opacity_val = params.get("opacity")
            opacity = float(opacity_val.number) if isinstance(opacity_val, LengthValue) else 1.0
            self._render_image(canvas, src_path, mode, opacity)
            return

        if "color1" in params and "color2" in params:
            c1 = params["color1"]
            c2 = params["color2"]
            start = params.get("start")
            end = params.get("end")
            self._render_gradient(canvas, c1, c2, start, end)
            return

        if "color" in params:
            self._render_solid(canvas, params["color"])
            return

        self._reporter.warning(
            node.source_file, node.line,
            "background: no recognised parameters; statement has no effect"
        )

    def _render_solid(self, canvas: Image.Image, color: ColorValue | object) -> None:
        """Fill entire canvas with a solid colour (REQ-0004.1)."""
        if not isinstance(color, ColorValue):
            return
        draw = ImageDraw.Draw(canvas)
        fill = _color_tuple(color, canvas.mode)
        draw.rectangle([0, 0, canvas.width - 1, canvas.height - 1], fill=fill)

    def _render_gradient(
        self,
        canvas: Image.Image,
        color1: ColorValue | object,
        color2: ColorValue | object,
        start: object | None,
        end: object | None,
    ) -> None:
        """Apply linear gradient from color1 to color2 (REQ-0004.2).

        Identical start/end: fills with color1 (warning already emitted by validator).
        Uses manual pixel computation for linear interpolation along the gradient axis.
        """
        if not isinstance(color1, ColorValue) or not isinstance(color2, ColorValue):
            return

        w, h = canvas.width, canvas.height
        s = canvas.info.get("aa_scale", 1)

        def _point_to_px(p: object) -> tuple[int, int]:
            if isinstance(p, PointValue):
                return (int(round(p.x.number * s)), int(round(p.y.number * s)))
            return (0, 0)

        sx, sy = _point_to_px(start) if start else (0, 0)
        ex, ey = _point_to_px(end) if end else (w - 1, 0)

        # Vector from start to end
        dx, dy = ex - sx, ey - sy
        length_sq = dx * dx + dy * dy

        if length_sq == 0:
            # Identical endpoints — fill with color1
            self._render_solid(canvas, color1)
            return

        pixels = canvas.load()
        for y in range(h):
            for x in range(w):
                # Project (x-sx, y-sy) onto the gradient vector
                t = ((x - sx) * dx + (y - sy) * dy) / length_sq
                t = max(0.0, min(1.0, t))
                r = int(color1.r + t * (color2.r - color1.r))
                g = int(color1.g + t * (color2.g - color1.g))
                b = int(color1.b + t * (color2.b - color1.b))
                a = color1.a + t * (color2.a - color1.a)

                if canvas.mode == "RGBA":
                    pixels[x, y] = (r, g, b, int(a * 255))
                elif canvas.mode == "L":
                    pixels[x, y] = int(0.299 * r + 0.587 * g + 0.114 * b)
                else:
                    pixels[x, y] = (r, g, b)

    def _render_image(
        self,
        canvas: Image.Image,
        src: pathlib.Path,
        mode: str,
        opacity: float,
    ) -> None:
        """Composite an image file onto the canvas (REQ-0004.3).

        Modes:
          'fit'     — preserve aspect ratio, letterbox/pillarbox padding.
          'stretch' — ignore aspect ratio, fill exactly.
          'clip'    — scale so shorter dimension fills, centre-crop excess.
        """
        if not src.exists():
            self._reporter.io_error(str(src), 0,
                f"background image asset not found: '{src}'")

        bg = Image.open(src).convert("RGBA")
        cw, ch = canvas.width, canvas.height
        bw, bh = bg.size

        if mode == "stretch":
            bg = bg.resize((cw, ch), Image.LANCZOS)
        elif mode == "clip":
            # Scale so the image covers the canvas, then centre-crop
            scale = max(cw / bw, ch / bh)
            new_w, new_h = int(bw * scale), int(bh * scale)
            bg = bg.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - cw) // 2
            top = (new_h - ch) // 2
            bg = bg.crop((left, top, left + cw, top + ch))
        else:  # 'fit' — preserve aspect ratio, pad with default background
            scale = min(cw / bw, ch / bh)
            new_w, new_h = int(bw * scale), int(bh * scale)
            bg = bg.resize((new_w, new_h), Image.LANCZOS)

        # Apply opacity
        if opacity < 1.0:
            r, g, b, a = bg.split()
            a = a.point(lambda v: int(v * opacity))
            bg = Image.merge("RGBA", (r, g, b, a))

        # Composite onto canvas
        canvas_rgba = canvas.convert("RGBA")
        paste_x = (cw - bg.width) // 2
        paste_y = (ch - bg.height) // 2
        canvas_rgba.paste(bg, (paste_x, paste_y), bg)

        # Convert back to original mode
        result = canvas_rgba.convert(canvas.mode)
        canvas.paste(result)
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
