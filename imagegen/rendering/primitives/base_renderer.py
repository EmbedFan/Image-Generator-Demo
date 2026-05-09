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
"""Abstract base class for all primitive renderers.

render() draws directly onto the canvas PIL Image in-place; it does not return a new image.
The TransformApplier handles position/scale/skew/rotate separately after primitives are drawn
when the renderer draws onto an off-screen buffer and composites.
"""

from __future__ import annotations

import pathlib
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from imagegen.ast_nodes import DrawingCmd, LengthValue
    from imagegen.error_reporter import ErrorReporter

_CM_PER_INCH = 2.54
_MM_PER_INCH = 25.4
_PT_PER_INCH = 72.0


class BaseRenderer(ABC):
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    @staticmethod
    def _s(canvas: Image.Image, val: float) -> int:
        """Scale a DSL pixel value by the canvas supersampling factor."""
        return int(round(val * canvas.info.get("aa_scale", 1)))

    @staticmethod
    def _px(canvas: Image.Image, length: LengthValue) -> int:
        """Convert a LengthValue to canvas pixels, applying DPI and supersampling scale."""
        n = length.number
        unit = length.unit
        dpi = canvas.info.get("dpi", (96, 96))[0]
        aa = canvas.info.get("aa_scale", 1)
        if unit in ("px", ""):
            raw = n
        elif unit == "pt":
            raw = n / _PT_PER_INCH * dpi
        elif unit == "cm":
            raw = n / _CM_PER_INCH * dpi
        elif unit == "mm":
            raw = n / _MM_PER_INCH * dpi
        elif unit == "em":
            raw = n * 12.0 / _PT_PER_INCH * dpi
        elif unit == "%":
            raw = n / 100.0 * 1000
        else:
            raw = n
        return int(round(raw * aa))

    @abstractmethod
    def render(
        self,
        canvas: Image.Image,
        node: DrawingCmd,
        base_dir: pathlib.Path,
    ) -> None:
        """Draw the primitive onto canvas in-place."""
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
