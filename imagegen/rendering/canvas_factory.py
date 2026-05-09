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
"""Canvas Factory — creates blank PIL Image buffers per frame.

Default fills (REQ-0004.4):
  RGBA  → transparent (0, 0, 0, 0)
  RGB   → white (255, 255, 255)
  GRAY  → white (255)

DPI decimal values are truncated to int before use (REQ-0003).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from imagegen.ast_nodes import ImageDef, LengthValue

# Unit conversion factors to pixels at a given DPI
_CM_PER_INCH = 2.54
_MM_PER_INCH = 25.4
_PT_PER_INCH = 72.0


class CanvasFactory:
    def create(self, image_def: ImageDef, aa_scale: int = 1) -> Image.Image:
        """Return a blank PIL Image sized and colour-spaced per image_def.

        DPI decimal values are truncated to int before use (REQ-0003).
        Default fill: transparent for RGBA, white for RGB and GRAY (REQ-0004.4).
        aa_scale > 1 creates an oversized canvas for supersampling antialiasing;
        FrameRunner downscales it with LANCZOS after rendering.
        """
        dpi = int(image_def.dpi)  # truncate, not round (REQ-0003)
        width_px, height_px = self._resolve_size_px(image_def, dpi)

        colorspace = image_def.colorspace  # 'RGB' | 'RGBA' | 'GRAY'
        pil_mode = "L" if colorspace == "GRAY" else colorspace

        # Default background colour per colorspace
        if pil_mode == "RGBA":
            default_color: int | tuple = (0, 0, 0, 0)  # transparent
        elif pil_mode == "RGB":
            default_color = (255, 255, 255)             # white
        else:  # GRAY / L
            default_color = 255                         # white

        scaled_w = width_px * aa_scale
        scaled_h = height_px * aa_scale
        img = Image.new(pil_mode, (scaled_w, scaled_h), default_color)
        # Embed DPI metadata for JPEG/PNG writers
        img.info["dpi"] = (dpi, dpi)
        # Store AA metadata so renderers can scale coordinates
        img.info["aa_scale"] = aa_scale
        img.info["target_size"] = (width_px, height_px)
        return img

    def _resolve_size_px(self, image_def: ImageDef, dpi: int) -> tuple[int, int]:
        """Convert width/height LengthValues to pixel integers using DPI."""
        width_px = self._length_to_px(image_def.width, dpi)
        height_px = self._length_to_px(image_def.height, dpi)
        return width_px, height_px

    @staticmethod
    def _length_to_px(length: LengthValue, dpi: int) -> int:
        """Convert a LengthValue to a pixel integer."""
        n = length.number
        unit = length.unit
        if unit in ("px", ""):
            return max(1, int(n))
        if unit == "pt":
            return max(1, int(n / _PT_PER_INCH * dpi))
        if unit == "cm":
            return max(1, int(n / _CM_PER_INCH * dpi))
        if unit == "mm":
            return max(1, int(n / _MM_PER_INCH * dpi))
        if unit == "em":
            # 1em = 12pt by convention when no font context is available
            return max(1, int(n * 12 / _PT_PER_INCH * dpi))
        if unit == "%":
            # Percentage with no parent context — treat as percentage of 1000px
            return max(1, int(n / 100.0 * 1000))
        return max(1, int(n))
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
