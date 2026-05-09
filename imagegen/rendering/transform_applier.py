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
"""Transform Applier — applies position, scale, skew, and rotate to primitives.

Transform order: position → scale → skew → rotate (REQ-0017).
Z-index is NOT handled here — that is the Primitive Dispatcher's responsibility.
Negative scale is a validation error caught before rendering reaches this module.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PIL import Image

from imagegen.ast_nodes import LengthValue

if TYPE_CHECKING:
    from imagegen.ast_nodes import Value


@dataclass
class TransformParams:
    pos_x: int = 0
    pos_y: int = 0
    scale: float = 1.0
    skew_x: float = 0.0   # degrees
    skew_y: float = 0.0   # degrees
    rotate: float = 0.0   # degrees, clockwise


class TransformApplier:
    """Apply geometric transforms and composite a primitive onto the canvas.

    Transform order: position → scale → skew → rotate.
    Z-index is excluded from this class — handled by PrimitiveDispatcher.
    Negative scale is treated as 0 (should have been caught by SemanticValidator).
    """

    def apply(
        self,
        canvas: Image.Image,
        primitive_image: Image.Image,
        params: dict[str, Value],
    ) -> None:
        """Composite primitive_image onto canvas after applying transforms in order:
        position → scale → skew → rotate.
        """
        aa_scale = canvas.info.get("aa_scale", 1)
        tp = self._extract_transform_params(params, aa_scale)
        img = primitive_image.convert("RGBA")

        img = self._apply_scale(img, tp.scale)
        img = self._apply_skew(img, tp.skew_x, tp.skew_y)
        img = self._apply_rotate(img, tp.rotate)

        # Composite onto canvas at the resolved position
        canvas_rgba = canvas.convert("RGBA")
        if canvas_rgba is not canvas:
            # in-place: we'll paste back
            pass
        canvas_rgba.paste(img, (tp.pos_x, tp.pos_y), img)

        # Write result back to canvas (handles mode conversion)
        result = canvas_rgba.convert(canvas.mode)
        canvas.paste(result)

    def _extract_transform_params(self, params: dict[str, Value], aa_scale: int = 1) -> TransformParams:
        tp = TransformParams()

        pos = params.get("pos")
        if pos is not None and hasattr(pos, "x"):
            tp.pos_x = int(round(pos.x.number * aa_scale))
            tp.pos_y = int(round(pos.y.number * aa_scale))

        scale_val = params.get("scale")
        if isinstance(scale_val, LengthValue):
            tp.scale = max(0.0, scale_val.number)

        skew_x_val = params.get("skew-x")
        if isinstance(skew_x_val, LengthValue):
            tp.skew_x = skew_x_val.number

        skew_y_val = params.get("skew-y")
        if isinstance(skew_y_val, LengthValue):
            tp.skew_y = skew_y_val.number

        rotate_val = params.get("rotate")
        if isinstance(rotate_val, LengthValue):
            tp.rotate = rotate_val.number

        return tp

    @staticmethod
    def _apply_scale(img: Image.Image, scale: float) -> Image.Image:
        if scale == 1.0 or scale <= 0:
            return img
        new_w = max(1, int(img.width * scale))
        new_h = max(1, int(img.height * scale))
        return img.resize((new_w, new_h), Image.LANCZOS)

    @staticmethod
    def _apply_skew(img: Image.Image, skew_x: float, skew_y: float) -> Image.Image:
        if skew_x == 0.0 and skew_y == 0.0:
            return img
        tan_x = math.tan(math.radians(skew_x))
        tan_y = math.tan(math.radians(skew_y))
        # Affine matrix for shear: [1, tan_x, 0, tan_y, 1, 0]
        w, h = img.size
        extra_w = int(abs(tan_x) * h)
        extra_h = int(abs(tan_y) * w)
        new_w = w + extra_w
        new_h = h + extra_h
        data = (1, tan_x, -extra_w / 2, tan_y, 1, -extra_h / 2)
        return img.transform((new_w, new_h), Image.AFFINE, data, Image.BICUBIC)

    @staticmethod
    def _apply_rotate(img: Image.Image, angle: float) -> Image.Image:
        if angle == 0.0:
            return img
        # PIL rotates counter-clockwise; DSL specifies clockwise → negate
        return img.rotate(-angle, expand=True, resample=Image.BICUBIC)
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
