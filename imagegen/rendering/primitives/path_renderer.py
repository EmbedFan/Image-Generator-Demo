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
"""Path Renderer (REQ-0009) — open polyline; stroke-only, no fill; ≥ 2 points required."""

from __future__ import annotations

import math
import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import ColorValue, LengthValue, PointList
from imagegen.rendering.primitives.line_renderer import _resolve_color

if TYPE_CHECKING:
    from imagegen.ast_nodes import PathNode
    from imagegen.error_reporter import ErrorReporter


class PathRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: PathNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params
        color = params.get("color")
        points_val = params.get("points")
        s = canvas.info.get("aa_scale", 1)
        line_width = self._px(canvas, params["line-width"]) if isinstance(params.get("line-width"), LengthValue) else s
        line_type_val = params.get("line-type")
        line_type = line_type_val.name if hasattr(line_type_val, "name") else "solid"

        if not isinstance(points_val, PointList) or len(points_val.points) < 2:
            return  # SemanticValidator should have caught this

        xy = [(self._px(canvas, p.x), self._px(canvas, p.y)) for p in points_val.points]
        stroke_color = _resolve_color(color, "RGBA") if isinstance(color, ColorValue) else (0, 0, 0, 255)

        temp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp)

        if line_type in ("solid", ""):
            draw.line(xy, fill=stroke_color, width=line_width)
        elif line_type == "dashed":
            self._draw_dashed_poly(draw, xy, stroke_color, line_width, dash=8 * s, gap=4 * s)
        elif line_type == "dotted":
            self._draw_dashed_poly(draw, xy, stroke_color, line_width, dash=2 * s, gap=4 * s)
        elif line_type == "dash-dot":
            self._draw_dash_dot_poly(draw, xy, stroke_color, line_width, scale=s)
        else:
            draw.line(xy, fill=stroke_color, width=line_width)

        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), temp).convert(canvas.mode))

    @staticmethod
    def _draw_dashed_poly(
        draw: ImageDraw.Draw,
        xy: list[tuple[int, int]],
        color: tuple | int,
        width: int,
        dash: float,
        gap: float,
    ) -> None:
        """Continuous dashed polyline — dash phase carries across vertices."""
        pos_in_pattern = 0.0
        drawing = True
        for i in range(len(xy) - 1):
            start, end = xy[i], xy[i + 1]
            dx, dy = end[0] - start[0], end[1] - start[1]
            seg_len = math.hypot(dx, dy)
            if seg_len == 0:
                continue
            ux, uy = dx / seg_len, dy / seg_len
            pos = 0.0
            while pos < seg_len:
                current = dash if drawing else gap
                if current <= 0:
                    break
                remaining = current - pos_in_pattern
                dist = min(remaining, seg_len - pos)
                if drawing:
                    x0 = start[0] + ux * pos
                    y0 = start[1] + uy * pos
                    x1 = start[0] + ux * (pos + dist)
                    y1 = start[1] + uy * (pos + dist)
                    draw.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=color, width=width)
                pos += dist
                pos_in_pattern += dist
                if pos_in_pattern >= current:
                    pos_in_pattern = 0.0
                    drawing = not drawing

    @staticmethod
    def _draw_dash_dot_poly(
        draw: ImageDraw.Draw,
        xy: list[tuple[int, int]],
        color: tuple | int,
        width: int,
        scale: int = 1,
    ) -> None:
        """Continuous dash-dot polyline — pattern phase carries across vertices."""
        pattern = [8 * scale, 3 * scale, 2 * scale, 3 * scale]  # dash, gap, dot, gap
        pat_idx = 0
        pos_in_seg = 0.0
        for i in range(len(xy) - 1):
            start, end = xy[i], xy[i + 1]
            dx, dy = end[0] - start[0], end[1] - start[1]
            seg_len = math.hypot(dx, dy)
            if seg_len == 0:
                continue
            ux, uy = dx / seg_len, dy / seg_len
            pos = 0.0
            while pos < seg_len:
                current = pattern[pat_idx % len(pattern)]
                if current <= 0:
                    pat_idx += 1
                    continue
                dist = min(current - pos_in_seg, seg_len - pos)
                if pat_idx % 2 == 0:
                    x0 = start[0] + ux * pos
                    y0 = start[1] + uy * pos
                    x1 = start[0] + ux * (pos + dist)
                    y1 = start[1] + uy * (pos + dist)
                    draw.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=color, width=width)
                pos += dist
                pos_in_seg += dist
                if pos_in_seg >= current:
                    pos_in_seg = 0.0
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
