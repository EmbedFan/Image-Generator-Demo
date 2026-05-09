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
"""Pie Renderer (REQ-0010) — pie slice: clockwise arc + two radii; fill supported."""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import ColorValue, ColorNone, LengthValue, PointValue
from imagegen.rendering.primitives.line_renderer import _resolve_color

if TYPE_CHECKING:
    from imagegen.ast_nodes import PieNode
    from imagegen.error_reporter import ErrorReporter


class PieRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: PieNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params
        color = params.get("color")
        fill = params.get("fill")
        center = params.get("center")
        radius_val = params.get("radius")
        start_angle_val = params.get("start-angle")
        end_angle_val = params.get("end-angle")

        cx = self._px(canvas, center.x) if isinstance(center, PointValue) else 0
        cy = self._px(canvas, center.y) if isinstance(center, PointValue) else 0
        r = self._px(canvas, radius_val) if isinstance(radius_val, LengthValue) else self._s(canvas, 50)
        start_angle = float(start_angle_val.number) if isinstance(start_angle_val, LengthValue) else 0.0
        end_angle = float(end_angle_val.number) if isinstance(end_angle_val, LengthValue) else 90.0

        bbox = [cx - r, cy - r, cx + r, cy + r]
        line_width = self._px(canvas, params["line-width"]) if isinstance(params.get("line-width"), LengthValue) else canvas.info.get("aa_scale", 1)

        stroke_color = _resolve_color(color, "RGBA") if isinstance(color, ColorValue) else None
        fill_color: tuple | None = None
        if fill is not None and not isinstance(fill, ColorNone):
            fill_color = _resolve_color(fill, "RGBA") if isinstance(fill, ColorValue) else None

        # PIL pieslice angles are counter-clockwise from 3 o'clock;
        # DSL specifies clockwise from 12 o'clock → convert:
        pil_start = -(end_angle - 90)
        pil_end = -(start_angle - 90)

        temp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ImageDraw.Draw(temp).pieslice(bbox, start=pil_start, end=pil_end,
                                      fill=fill_color, outline=stroke_color, width=line_width)
        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), temp).convert(canvas.mode))
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
