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
"""BBox Overlay Renderer (FEA-005, REQ-0039–REQ-0039.6).

Draws a dashed, contrast-aware bounding box over each drawable element
that carries show-bbox=true.  Called as a post-process step on the final
1× canvas, after grid rendering.

Color algorithm: sample the average luminance of the canvas region covered
by the AABB and snap to black (0) or white (255) for maximum contrast.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.ast_nodes import (
    BoolValue, LengthValue, PointValue, PointList,
    ExprFactor,
    LineNode, CircleNode, SquareNode, PolygonNode, PathNode,
    PieNode, ArcNode, ConnectorNode, FontNode, ImagePrimNode,
    ObjectInst,
)

if TYPE_CHECKING:
    from imagegen.ast_nodes import DrawingCmd
    from imagegen.symbol_table import SymbolTable

_DASH = 8
_GAP = 4
_LINE_WIDTH = 1


def _unwrap_length(val: object) -> LengthValue | None:
    """Accept LengthValue or ExprFactor(LengthValue) produced by in_func_body parsing."""
    if isinstance(val, LengthValue):
        return val
    if isinstance(val, ExprFactor) and isinstance(val.value, LengthValue):
        return val.value
    return None


def render_bbox_overlays(
    canvas: Image.Image,
    commands: list[DrawingCmd],
    symbol_table: SymbolTable | None = None,
) -> None:
    """Draw dashed bounding-box overlays for all commands with show-bbox=true."""
    draw = ImageDraw.Draw(canvas)
    cw, ch = canvas.size
    for cmd in commands:
        if not _wants_bbox(cmd):
            continue
        aabb = _compute_aabb(cmd, symbol_table)
        if aabb is None:
            continue
        x0 = max(0, int(aabb[0]))
        y0 = max(0, int(aabb[1]))
        x1 = min(cw - 1, int(aabb[2]))
        y1 = min(ch - 1, int(aabb[3]))
        if x1 <= x0 or y1 <= y0:
            continue
        color = _contrast_color(canvas, (x0, y0, x1, y1))
        _draw_dashed_rect(draw, x0, y0, x1, y1, color)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _wants_bbox(cmd: object) -> bool:
    """Return True when the command has show-bbox=true."""
    params = getattr(cmd, "params", None)
    if not isinstance(params, dict):
        return False
    val = params.get("show-bbox")
    return isinstance(val, BoolValue) and val.value


def _arc_aabb(
    cx: float, cy: float, r: float,
    start_angle: float, end_angle: float,
    line_width: float = 1.0,
    include_center: bool = False,
) -> tuple[float, float, float, float]:
    """Tight AABB by rendering the shape onto a temp image and scanning actual pixel extents."""
    margin = int(line_width) + 2
    size = int(2 * r) + 2 * margin + 4
    cx_t = size // 2
    cy_t = size // 2
    r_int = int(r)

    tmp = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(tmp)
    bbox_t = [cx_t - r_int, cy_t - r_int, cx_t + r_int, cy_t + r_int]

    # DSL angles are clockwise from north; convert to PIL convention
    pil_start = -(end_angle - 90)
    pil_end = -(start_angle - 90)
    lw = max(1, int(line_width))

    if include_center:
        draw.pieslice(bbox_t, start=pil_start, end=pil_end, fill=255, outline=255, width=lw)
    else:
        draw.arc(bbox_t, start=pil_start, end=pil_end, fill=255, width=lw)

    actual = tmp.getbbox()
    if actual is None:
        return (cx - r, cy - r, cx + r, cy + r)

    return (
        cx - cx_t + actual[0],
        cy - cy_t + actual[1],
        cx - cx_t + actual[2] - 1,
        cy - cy_t + actual[3] - 1,
    )


def _compute_aabb(
    cmd: object,
    symbol_table: SymbolTable | None,
) -> tuple[float, float, float, float] | None:
    """Return (x0, y0, x1, y1) axis-aligned bounding box in 1× canvas pixels."""
    params = getattr(cmd, "params", None)
    if not isinstance(params, dict):
        return None

    if isinstance(cmd, CircleNode):
        center = params.get("center")
        r_lv = _unwrap_length(params.get("radius"))
        if isinstance(center, PointValue) and r_lv is not None:
            cx, cy, r = center.x.number, center.y.number, r_lv.number
            return (cx - r, cy - r, cx + r, cy + r)

    elif isinstance(cmd, (PieNode, ArcNode)):
        center = params.get("center")
        r_lv = _unwrap_length(params.get("radius"))
        start_lv = _unwrap_length(params.get("start-angle"))
        end_lv = _unwrap_length(params.get("end-angle"))
        lw_lv = _unwrap_length(params.get("line-width"))
        if isinstance(center, PointValue) and r_lv is not None:
            cx, cy, r = center.x.number, center.y.number, r_lv.number
            start_angle = float(start_lv.number) if start_lv is not None else 0.0
            end_angle = float(end_lv.number) if end_lv is not None else 90.0
            line_width = float(lw_lv.number) if lw_lv is not None else 1.0
            return _arc_aabb(cx, cy, r, start_angle, end_angle, line_width, isinstance(cmd, PieNode))

    elif isinstance(cmd, SquareNode):
        pos = params.get("pos")
        w_lv = _unwrap_length(params.get("width"))
        h_lv = _unwrap_length(params.get("height"))
        if isinstance(pos, PointValue):
            x, y = pos.x.number, pos.y.number
            w = w_lv.number if w_lv is not None else 0.0
            h = h_lv.number if h_lv is not None else 0.0
            return (x, y, x + w, y + h)

    elif isinstance(cmd, LineNode):
        start = params.get("start")
        end = params.get("end")
        if isinstance(start, PointValue) and isinstance(end, PointValue):
            x0 = min(start.x.number, end.x.number)
            y0 = min(start.y.number, end.y.number)
            x1 = max(start.x.number, end.x.number)
            y1 = max(start.y.number, end.y.number)
            # Ensure non-degenerate bbox for axis-aligned lines
            if x0 == x1:
                x1 += 1.0
            if y0 == y1:
                y1 += 1.0
            return (x0, y0, x1, y1)

    elif isinstance(cmd, (PolygonNode, PathNode)):
        pts = params.get("points")
        if isinstance(pts, PointList) and pts.points:
            xs = [p.x.number for p in pts.points]
            ys = [p.y.number for p in pts.points]
            return (min(xs), min(ys), max(xs), max(ys))

    elif isinstance(cmd, ConnectorNode):
        pts = params.get("points")
        if isinstance(pts, PointList) and pts.points:
            xs = [p.x.number for p in pts.points]
            ys = [p.y.number for p in pts.points]
            x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
        else:
            start = params.get("start")
            end = params.get("end")
            if not (isinstance(start, PointValue) and isinstance(end, PointValue)):
                return None
            x0 = min(start.x.number, end.x.number)
            y0 = min(start.y.number, end.y.number)
            x1 = max(start.x.number, end.x.number)
            y1 = max(start.y.number, end.y.number)
        # Ensure non-degenerate bbox for axis-aligned connectors
        if x0 == x1:
            x1 += 1.0
        if y0 == y1:
            y1 += 1.0
        return (x0, y0, x1, y1)

    elif isinstance(cmd, FontNode):
        pos = params.get("pos")
        size_lv = _unwrap_length(params.get("font-size"))
        text_val = params.get("text")
        if isinstance(pos, PointValue):
            x, y = pos.x.number, pos.y.number
            font_size = size_lv.number if size_lv is not None else 12.0
            text = text_val.value if hasattr(text_val, "value") else ""
            lines = text.split("\n") if text else [""]
            max_chars = max((len(ln) for ln in lines), default=0)
            w = max_chars * font_size * 0.6
            h = len(lines) * font_size * 1.2
            return (x, y, x + w, y + h)

    elif isinstance(cmd, ImagePrimNode):
        pos = params.get("pos")
        w_lv = _unwrap_length(params.get("width"))
        h_lv = _unwrap_length(params.get("height"))
        if isinstance(pos, PointValue):
            x, y = pos.x.number, pos.y.number
            w = w_lv.number if w_lv is not None else 100.0
            h = h_lv.number if h_lv is not None else 100.0
            return (x, y, x + w, y + h)

    elif isinstance(cmd, ObjectInst):
        return _object_inst_aabb(cmd, symbol_table)

    return None


def _object_inst_aabb(
    cmd: ObjectInst,
    symbol_table: SymbolTable | None,
) -> tuple[float, float, float, float] | None:
    params = cmd.params
    pos = params.get("pos")
    if not isinstance(pos, PointValue):
        return None
    x, y = pos.x.number, pos.y.number

    # Resolve width/height: instance params > scale > template attributes
    w_lv = _unwrap_length(params.get("width"))
    h_lv = _unwrap_length(params.get("height"))
    w = w_lv.number if w_lv is not None else None
    h = h_lv.number if h_lv is not None else None

    if (w is None or h is None) and symbol_table is not None:
        template = symbol_table.lookup_object(cmd.name)
        if template is not None:
            for attr in template.attributes:
                if attr.key == "width" and isinstance(attr.value, LengthValue) and w is None:
                    w = attr.value.number
                if attr.key == "height" and isinstance(attr.value, LengthValue) and h is None:
                    h = attr.value.number

    resize_mode = None
    resize_mode_val = params.get("resize-mode")
    if isinstance(resize_mode_val, ExprFactor) and isinstance(resize_mode_val.value, str):
        resize_mode = resize_mode_val.value
    elif hasattr(resize_mode_val, "name"):
        resize_mode = getattr(resize_mode_val, "name", None)

    scale_lv = _unwrap_length(params.get("scale"))
    if scale_lv is not None and scale_lv.number > 0:
        has_explicit = "width" in params or "height" in params
        if resize_mode == "layout" or not has_explicit:
            w = (w or 0.0) * scale_lv.number
            h = (h or 0.0) * scale_lv.number

    w = w or 0.0
    h = h or 0.0

    # Apply rotation to expand the AABB (object instantiator rotates around centre)
    rotate_lv = _unwrap_length(params.get("rotate"))
    if rotate_lv is not None and rotate_lv.number != 0 and w > 0 and h > 0:
        theta = math.radians(rotate_lv.number)
        cos_t = abs(math.cos(theta))
        sin_t = abs(math.sin(theta))
        new_w = w * cos_t + h * sin_t
        new_h = w * sin_t + h * cos_t
        cx, cy = x + w / 2, y + h / 2
        x = cx - new_w / 2
        y = cy - new_h / 2
        w, h = new_w, new_h

    return (x, y, x + w, y + h)


def _contrast_color(
    canvas: Image.Image,
    bbox: tuple[int, int, int, int],
) -> tuple | int:
    """Return black or white, whichever has higher contrast vs. the bbox region."""
    x0, y0, x1, y1 = bbox
    try:
        region = canvas.crop((x0, y0, x1 + 1, y1 + 1))
        gray = region.convert("L")
        data = list(gray.getdata())
        avg_lum = sum(data) / len(data) if data else 128
    except Exception:
        avg_lum = 128
    # Snap to black or white — never a mid-grey that blends in
    inv = 0 if avg_lum >= 128 else 255
    if canvas.mode == "L":
        return inv
    if canvas.mode == "RGBA":
        return (inv, inv, inv, 255)
    return (inv, inv, inv)


def _draw_dashed_rect(
    draw: ImageDraw.Draw,
    x0: int, y0: int, x1: int, y1: int,
    color: tuple | int,
) -> None:
    """Draw four dashed line segments forming a rectangle."""
    sides = [
        ((x0, y0), (x1, y0)),  # top
        ((x1, y0), (x1, y1)),  # right
        ((x1, y1), (x0, y1)),  # bottom
        ((x0, y1), (x0, y0)),  # left
    ]
    for start, end in sides:
        _draw_dashed_segment(draw, start, end, color)


def _draw_dashed_segment(
    draw: ImageDraw.Draw,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple | int,
) -> None:
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    pos = 0.0
    drawing = True
    while pos < length:
        seg_len = float(_DASH if drawing else _GAP)
        x0f = start[0] + ux * pos
        y0f = start[1] + uy * pos
        pos = min(pos + seg_len, length)
        x1f = start[0] + ux * pos
        y1f = start[1] + uy * pos
        if drawing:
            draw.line(
                [(int(round(x0f)), int(round(y0f))), (int(round(x1f)), int(round(y1f)))],
                fill=color,
                width=_LINE_WIDTH,
            )
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
