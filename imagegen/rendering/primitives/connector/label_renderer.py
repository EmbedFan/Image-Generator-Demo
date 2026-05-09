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
"""Label Renderer (REQ-0011.6) — inline text label along a connector route."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont

from imagegen.ast_nodes import StringValue, IdentValue, LengthValue, PointValue

if TYPE_CHECKING:
    from imagegen.rendering.primitives.font_renderer import FontRenderer


class LabelRenderer:
    def render(
        self,
        canvas: Image.Image,
        route: list[tuple[int, int]],
        params: dict,
        font_renderer: FontRenderer,
        aa_scale: int = 1,
    ) -> None:
        """Render label text at 'start', 'center', or 'end' along the connector route."""
        label_val = params.get("label")
        if label_val is None:
            return
        label = label_val.value if isinstance(label_val, StringValue) else str(label_val)
        if not label:
            return

        label_pos_val = params.get("label-pos")
        label_pos = label_pos_val.name if isinstance(label_pos_val, IdentValue) else "center"

        offset_val = params.get("label-offset")
        off_x = int(round(offset_val.x.number * aa_scale)) if isinstance(offset_val, PointValue) else 0
        off_y = int(round(offset_val.y.number * aa_scale)) if isinstance(offset_val, PointValue) else -12 * aa_scale

        color_val = params.get("color")

        if not route:
            return

        if label_pos == "start":
            pt = route[0]
        elif label_pos == "end":
            pt = route[-1]
        else:  # center
            pt = route[len(route) // 2]

        x = pt[0] + off_x
        y = pt[1] + off_y

        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()
        fill = (0, 0, 0)
        if hasattr(color_val, "r"):
            fill = (color_val.r, color_val.g, color_val.b)
        draw.text((x, y), label, fill=fill, font=font)
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
