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
"""Arc Renderer (REQ-0010.1) — stroke-only arc; 'fill' on arc is a parse error caught earlier."""

from __future__ import annotations

import math
import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import ColorValue, LengthValue, PointValue
from imagegen.rendering.primitives.line_renderer import _resolve_color

if TYPE_CHECKING:
    from imagegen.ast_nodes import ArcNode
    from imagegen.error_reporter import ErrorReporter


class ArcRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: ArcNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params
        color = params.get("color")
        center = params.get("center")
        radius_val = params.get("radius")
        start_angle_val = params.get("start-angle")
        end_angle_val = params.get("end-angle")
        s = canvas.info.get("aa_scale", 1)
        line_width = self._px(canvas, params["line-width"]) if isinstance(params.get("line-width"), LengthValue) else s
        line_type_val = params.get("line-type")
        line_type = line_type_val.name if hasattr(line_type_val, "name") else "solid"

        cx = self._px(canvas, center.x) if isinstance(center, PointValue) else 0
        cy = self._px(canvas, center.y) if isinstance(center, PointValue) else 0
        r = self._px(canvas, radius_val) if isinstance(radius_val, LengthValue) else self._s(canvas, 50)
        start_angle = float(start_angle_val.number) if isinstance(start_angle_val, LengthValue) else 0.0
        end_angle = float(end_angle_val.number) if isinstance(end_angle_val, LengthValue) else 90.0

        bbox = [cx - r, cy - r, cx + r, cy + r]
        stroke_color = _resolve_color(color, "RGBA") if isinstance(color, ColorValue) else (0, 0, 0, 255)

        # Convert clockwise-from-12 to PIL counter-clockwise-from-3
        pil_start = -(end_angle - 90)
        pil_end = -(start_angle - 90)

        temp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp)

        if line_type in ("solid", ""):
            draw.arc(bbox, start=pil_start, end=pil_end, fill=stroke_color, width=line_width)
        elif line_type == "dashed":
            self._draw_dashed_arc(draw, bbox, pil_start, pil_end, stroke_color, line_width, r,
                                   dash_px=8 * s, gap_px=4 * s)
        elif line_type == "dotted":
            self._draw_dashed_arc(draw, bbox, pil_start, pil_end, stroke_color, line_width, r,
                                   dash_px=2 * s, gap_px=4 * s)
        elif line_type == "dash-dot":
            self._draw_dash_dot_arc(draw, bbox, pil_start, pil_end, stroke_color, line_width, r, s)
        else:
            draw.arc(bbox, start=pil_start, end=pil_end, fill=stroke_color, width=line_width)

        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), temp).convert(canvas.mode))

    @staticmethod
    def _draw_dashed_arc(
        draw: ImageDraw.Draw,
        bbox: list,
        pil_start: float,
        pil_end: float,
        color: tuple | int,
        width: int,
        radius: float,
        dash_px: float,
        gap_px: float,
    ) -> None:
        circumference = 2 * math.pi * radius
        if circumference == 0:
            return
        dash_deg = dash_px / circumference * 360
        gap_deg = gap_px / circumference * 360
        if dash_deg <= 0 or gap_deg <= 0:
            draw.arc(bbox, start=pil_start, end=pil_end, fill=color, width=width)
            return
        span = pil_end - pil_start
        if span <= 0:
            span += 360
        if span <= 0:
            return
        pos = 0.0
        drawing = True
        while pos < span:
            seg = dash_deg if drawing else gap_deg
            end_pos = min(pos + seg, span)
            if drawing:
                draw.arc(bbox, start=pil_start + pos, end=pil_start + end_pos,
                         fill=color, width=width)
            pos = end_pos
            drawing = not drawing

    @staticmethod
    def _draw_dash_dot_arc(
        draw: ImageDraw.Draw,
        bbox: list,
        pil_start: float,
        pil_end: float,
        color: tuple | int,
        width: int,
        radius: float,
        scale: int = 1,
    ) -> None:
        circumference = 2 * math.pi * radius
        if circumference == 0:
            return
        pattern_px = [8 * scale, 3 * scale, 2 * scale, 3 * scale]  # dash, gap, dot, gap
        pattern_deg = [px / circumference * 360 for px in pattern_px]
        if any(d <= 0 for d in pattern_deg):
            draw.arc(bbox, start=pil_start, end=pil_end, fill=color, width=width)
            return
        span = pil_end - pil_start
        if span <= 0:
            span += 360
        if span <= 0:
            return
        pos = 0.0
        pat_idx = 0
        while pos < span:
            seg = pattern_deg[pat_idx % len(pattern_deg)]
            end_pos = min(pos + seg, span)
            if pat_idx % 2 == 0:
                draw.arc(bbox, start=pil_start + pos, end=pil_start + end_pos,
                         fill=color, width=width)
            pos = end_pos
            pat_idx += 1
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
