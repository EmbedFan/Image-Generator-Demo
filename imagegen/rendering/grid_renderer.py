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
"""Grid Renderer (FEA-004, REQ-0038.1) — draws optional visual grid lines over a canvas."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.ast_nodes import ColorValue, LengthValue, BoolValue, IdentValue

if TYPE_CHECKING:
    from imagegen.ast_nodes import GridNode


def _grid_color(params: dict, canvas_mode: str) -> tuple | int:
    color = params.get("color")
    if isinstance(color, ColorValue):
        if canvas_mode == "RGBA":
            return (color.r, color.g, color.b, int(color.a * 255))
        if canvas_mode == "L":
            return int(0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
        return (color.r, color.g, color.b)
    return (200, 200, 200)  # default when render=true but no color given


def render_grid(canvas: Image.Image, node: GridNode) -> None:
    """Draw grid lines over the canvas. No-op when render=false."""
    params = node.params

    render = params.get("render")
    if not (isinstance(render, BoolValue) and render.value):
        return

    step_x_val = params.get("step-x")
    step_y_val = params.get("step-y")
    if step_x_val is None or step_y_val is None:
        return

    step_x = step_x_val.number if isinstance(step_x_val, LengthValue) else 50.0
    step_y = step_y_val.number if isinstance(step_y_val, LengthValue) else 50.0
    offset_x_val = params.get("offset-x")
    offset_y_val = params.get("offset-y")
    offset_x = offset_x_val.number if isinstance(offset_x_val, LengthValue) else 0.0
    offset_y = offset_y_val.number if isinstance(offset_y_val, LengthValue) else 0.0
    line_width_val = params.get("line-width")
    line_width = max(1, int(line_width_val.number if isinstance(line_width_val, LengthValue) else 1))
    line_type_val = params.get("line-type")
    line_type = line_type_val.name if isinstance(line_type_val, IdentValue) else "solid"

    color = _grid_color(params, canvas.mode)
    w, h = canvas.size
    draw = ImageDraw.Draw(canvas)

    # Vertical lines
    x = offset_x
    while x <= w:
        xi = int(round(x))
        _draw_grid_line(draw, (xi, 0), (xi, h), color, line_width, line_type)
        x += step_x

    # Horizontal lines
    y = offset_y
    while y <= h:
        yi = int(round(y))
        _draw_grid_line(draw, (0, yi), (w, yi), color, line_width, line_type)
        y += step_y


def _draw_grid_line(
    draw: ImageDraw.Draw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple | int,
    width: int,
    line_type: str,
) -> None:
    if line_type == "dashed":
        _draw_dashed(draw, start, end, color, width, dash=8, gap=4)
    elif line_type == "dotted":
        _draw_dashed(draw, start, end, color, width, dash=2, gap=4)
    elif line_type == "dash-dot":
        _draw_dashed(draw, start, end, color, width, dash=8, gap=3)
        # simplified — not full dash-dot, just dashes
    else:
        draw.line([start, end], fill=color, width=width)


def _draw_dashed(
    draw: ImageDraw.Draw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple | int,
    width: int,
    dash: float,
    gap: float,
) -> None:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    pos = 0.0
    drawing = True
    while pos < length:
        seg_len = dash if drawing else gap
        seg_end = min(pos + seg_len, length)
        if drawing:
            x0 = int(round(start[0] + ux * pos))
            y0 = int(round(start[1] + uy * pos))
            x1 = int(round(start[0] + ux * seg_end))
            y1 = int(round(start[1] + uy * seg_end))
            draw.line([(x0, y0), (x1, y1)], fill=color, width=width)
        pos += seg_len
        drawing = not drawing
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
