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
"""Line Renderer (REQ-0005) — stroke-only straight line."""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import ColorValue, LengthValue, PointValue

if TYPE_CHECKING:
    from imagegen.ast_nodes import LineNode
    from imagegen.error_reporter import ErrorReporter


def _resolve_color(val: object, canvas_mode: str) -> tuple | int:
    if isinstance(val, ColorValue):
        if canvas_mode == "RGBA":
            return (val.r, val.g, val.b, int(val.a * 255))
        if canvas_mode == "L":
            return int(0.299 * val.r + 0.587 * val.g + 0.114 * val.b)
        return (val.r, val.g, val.b)
    return (0, 0, 0)


def _resolve_point(val: object, scale: int = 1) -> tuple[int, int]:
    if isinstance(val, PointValue):
        return (int(round(val.x.number * scale)), int(round(val.y.number * scale)))
    return (0, 0)


def _resolve_line_style(line_type: str, line_width: int) -> dict:
    """Map DSL line-type to PIL ImageDraw kwargs."""
    if line_type == "dashed":
        return {"width": line_width}  # PIL dashes handled via manual segment drawing
    if line_type == "dotted":
        return {"width": line_width}
    return {"width": line_width}


class LineRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: LineNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params
        s = canvas.info.get("aa_scale", 1)
        color = _resolve_color(params.get("color"), "RGBA")
        start_val = params.get("start")
        start = (self._px(canvas, start_val.x), self._px(canvas, start_val.y)) if isinstance(start_val, PointValue) else (0, 0)
        end_val = params.get("end")
        end = (self._px(canvas, end_val.x), self._px(canvas, end_val.y)) if isinstance(end_val, PointValue) else (0, 0)
        line_width = self._px(canvas, params["line-width"]) if isinstance(params.get("line-width"), LengthValue) else s
        line_type_val = params.get("line-type")
        line_type = line_type_val.name if hasattr(line_type_val, "name") else "solid"

        temp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp)

        if line_type in ("solid", ""):
            draw.line([start, end], fill=color, width=line_width)
        elif line_type == "dashed":
            self._draw_dashed(draw, start, end, color, line_width, dash=8 * s, gap=4 * s)
        elif line_type == "dotted":
            self._draw_dashed(draw, start, end, color, line_width, dash=2 * s, gap=4 * s)
        elif line_type == "dash-dot":
            self._draw_dash_dot(draw, start, end, color, line_width, scale=s)
        else:
            draw.line([start, end], fill=color, width=line_width)

        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), temp).convert(canvas.mode))

    @staticmethod
    def _draw_dashed(
        draw: ImageDraw.Draw,
        start: tuple[int, int],
        end: tuple[int, int],
        color: tuple | int,
        width: int,
        dash: float,
        gap: float,
    ) -> None:
        import math
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        pos = 0.0
        drawing = True
        while pos < length:
            seg_len = dash if drawing else gap
            x0 = start[0] + ux * pos
            y0 = start[1] + uy * pos
            pos = min(pos + seg_len, length)
            x1 = start[0] + ux * pos
            y1 = start[1] + uy * pos
            if drawing:
                draw.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=color, width=width)
            pos += 0  # advance already done
            drawing = not drawing

    @staticmethod
    def _draw_dash_dot(
        draw: ImageDraw.Draw,
        start: tuple[int, int],
        end: tuple[int, int],
        color: tuple | int,
        width: int,
        scale: int = 1,
    ) -> None:
        import math
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        pattern = [8 * scale, 3 * scale, 2 * scale, 3 * scale]  # dash, gap, dot, gap
        pos = 0.0
        pat_idx = 0
        drawing = True
        while pos < length:
            seg_len = pattern[pat_idx % len(pattern)]
            x0 = start[0] + ux * pos
            y0 = start[1] + uy * pos
            end_pos = min(pos + seg_len, length)
            x1 = start[0] + ux * end_pos
            y1 = start[1] + uy * end_pos
            if pat_idx % 2 == 0:  # even indices are drawn segments
                draw.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=color, width=width)
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
