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
"""Image Primitive Renderer (REQ-0013, REQ-0032).

SVG rasterisation:
  1. Attempt cairosvg (preferred, pure-Python binding).
  2. Fall back to svglib + reportlab.
  3. If neither is available, raise DslIOError.

opacity is applied via alpha-channel multiplication before compositing.
"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from PIL import Image

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import LengthValue, PointValue, StringValue

if TYPE_CHECKING:
    from imagegen.ast_nodes import ImagePrimNode
    from imagegen.error_reporter import ErrorReporter


class ImageRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: ImagePrimNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params

        src_val = params.get("src")
        src_str = src_val.value if isinstance(src_val, StringValue) else ""
        src_path = (base_dir / src_str).resolve()

        pos_val = params.get("pos")
        pos_x = self._px(canvas, pos_val.x) if isinstance(pos_val, PointValue) else 0
        pos_y = self._px(canvas, pos_val.y) if isinstance(pos_val, PointValue) else 0

        width_val = params.get("width")
        height_val = params.get("height")
        target_w = self._px(canvas, width_val) if isinstance(width_val, LengthValue) else None
        target_h = self._px(canvas, height_val) if isinstance(height_val, LengthValue) else None

        opacity_val = params.get("opacity")
        opacity = float(opacity_val.number) if isinstance(opacity_val, LengthValue) else 1.0

        asset = self._load_asset(src_path, node.source_file, node.line)

        # Resize if explicit dimensions given; otherwise keep original size
        if target_w and target_h:
            asset = asset.resize((target_w, target_h), Image.LANCZOS)
        elif target_w:
            ratio = target_w / asset.width
            asset = asset.resize((target_w, max(1, int(asset.height * ratio))), Image.LANCZOS)
        elif target_h:
            ratio = target_h / asset.height
            asset = asset.resize((max(1, int(asset.width * ratio)), target_h), Image.LANCZOS)

        scale_val = params.get("scale")
        scale = float(scale_val.number) if isinstance(scale_val, LengthValue) else 1.0

        rotate_val = params.get("rotate")
        rotate = float(rotate_val.number) if isinstance(rotate_val, LengthValue) else 0.0

        asset = asset.convert("RGBA")

        # Apply uniform scale (separate from explicit width/height)
        if scale != 1.0 and scale > 0:
            new_w = max(1, int(asset.width * scale))
            new_h = max(1, int(asset.height * scale))
            asset = asset.resize((new_w, new_h), Image.LANCZOS)

        # Apply opacity
        if opacity < 1.0:
            r, g, b, a = asset.split()
            a = a.point(lambda v: int(v * opacity))
            asset = Image.merge("RGBA", (r, g, b, a))

        # Apply rotation (DSL is clockwise; PIL rotates counter-clockwise → negate).
        # expand=True enlarges the output to fit the rotated content without clipping.
        # Adjust paste position so the image center stays at pos + half-size.
        if rotate != 0.0:
            cx = pos_x + asset.width / 2
            cy = pos_y + asset.height / 2
            asset = asset.rotate(-rotate, expand=True, resample=Image.BICUBIC)
            pos_x = int(round(cx - asset.width / 2))
            pos_y = int(round(cy - asset.height / 2))

        canvas_rgba = canvas.convert("RGBA")
        canvas_rgba.paste(asset, (pos_x, pos_y), asset)
        result = canvas_rgba.convert(canvas.mode)
        canvas.paste(result)

    def _load_asset(self, src: pathlib.Path, source_file: str, line: int) -> Image.Image:
        if not src.exists():
            self._reporter.io_error(source_file, line,
                f"image asset not found: '{src}'")

        if src.suffix.lower() == ".svg":
            return self._rasterise_svg(src, source_file, line)

        return Image.open(src)

    def _rasterise_svg(self, src: pathlib.Path, source_file: str, line: int) -> Image.Image:
        """Rasterise an SVG file to a PIL Image.

        Tries cairosvg first (preferred); falls back to svglib+reportlab.
        Raises DslIOError if neither library is available.
        """
        try:
            import cairosvg
            import io
            png_bytes = cairosvg.svg2png(url=str(src))
            return Image.open(io.BytesIO(png_bytes))
        except ImportError:
            pass

        try:
            from svglib.svglib import svg2rlg
            from reportlab.graphics import renderPM
            import io
            drawing = svg2rlg(str(src))
            png_bytes = renderPM.drawToString(drawing, fmt="PNG")
            return Image.open(io.BytesIO(png_bytes))
        except ImportError:
            pass

        self._reporter.io_error(source_file, line,
            f"cannot render SVG '{src}': neither cairosvg nor svglib is installed")
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
