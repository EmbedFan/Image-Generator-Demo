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
"""Polygon Renderer (REQ-0008) — filled or stroked closed polygon; ≥ 3 points required."""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.ast_nodes import ColorValue, ColorNone, LengthValue, PointList
from imagegen.rendering.primitives.line_renderer import _resolve_color

if TYPE_CHECKING:
    from imagegen.ast_nodes import PolygonNode
    from imagegen.error_reporter import ErrorReporter


class PolygonRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: PolygonNode, base_dir: pathlib.Path) -> None:  # type: ignore[override]
        params = node.params
        color = params.get("color")
        fill = params.get("fill")
        points_val = params.get("points")
        line_width = self._px(canvas, params["line-width"]) if isinstance(params.get("line-width"), LengthValue) else canvas.info.get("aa_scale", 1)

        if not isinstance(points_val, PointList) or len(points_val.points) < 3:
            return  # SemanticValidator should have caught this

        xy = [(self._px(canvas, p.x), self._px(canvas, p.y)) for p in points_val.points]

        scale_val = params.get("scale")
        scale = float(scale_val.number) if isinstance(scale_val, LengthValue) else 1.0
        rotate_val = params.get("rotate")
        rotate = float(rotate_val.number) if isinstance(rotate_val, LengthValue) else 0.0

        stroke_color = _resolve_color(color, "RGBA") if isinstance(color, ColorValue) else None
        fill_color: tuple | None = None
        if fill is not None and not isinstance(fill, ColorNone):
            fill_color = _resolve_color(fill, "RGBA") if isinstance(fill, ColorValue) else None

        if scale == 1.0 and rotate == 0.0:
            # Fast path: no transforms — draw at absolute canvas coordinates.
            temp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            ImageDraw.Draw(temp).polygon(xy, fill=fill_color, outline=stroke_color, width=line_width)
            canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), temp).convert(canvas.mode))
        else:
            # Transform path: draw on bbox-local surface → scale → rotate → composite.
            xs = [p[0] for p in xy]
            ys = [p[1] for p in xy]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            surf_w = max(1, max_x - min_x + 1)
            surf_h = max(1, max_y - min_y + 1)
            local_xy = [(px - min_x, py - min_y) for px, py in xy]

            surf = Image.new("RGBA", (surf_w, surf_h), (0, 0, 0, 0))
            ImageDraw.Draw(surf).polygon(local_xy, fill=fill_color, outline=stroke_color, width=line_width)

            if scale != 1.0 and scale > 0:
                surf = surf.resize(
                    (max(1, int(surf_w * scale)), max(1, int(surf_h * scale))), Image.LANCZOS
                )
            if rotate != 0.0:
                surf = surf.rotate(-rotate, expand=True, resample=Image.BICUBIC)

            # Composite centered on the original bounding-box center.
            elem_cx = (min_x + max_x) // 2
            elem_cy = (min_y + max_y) // 2
            px = elem_cx - surf.width // 2
            py = elem_cy - surf.height // 2
            canvas_rgba = canvas.convert("RGBA")
            canvas_rgba.paste(surf, (px, py), surf)
            canvas.paste(canvas_rgba.convert(canvas.mode))
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
