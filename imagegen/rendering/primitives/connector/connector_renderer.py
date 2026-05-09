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
"""Connector Renderer (REQ-0011) — orchestrates the five connector sub-modules.

Execution order per render() call:
  1. RouteBuilder    → geometry (list of pixel coordinates)
  2. CornerStyler    → shape intermediate vertices
  3. PatternEngine   → draw stroke with optional animation
  4. CapRenderer     → arrowheads at start-cap / end-cap
  5. LabelRenderer   → optional inline text label

frame_index must be set via set_frame_index() before render() is called when
animated connectors are present; the dispatcher handles this.
"""

from __future__ import annotations

import math
import pathlib
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw

from imagegen.rendering.primitives.base_renderer import BaseRenderer
from imagegen.rendering.primitives.connector.route_builder import RouteBuilder
from imagegen.rendering.primitives.connector.corner_styler import CornerStyler
from imagegen.rendering.primitives.connector.cap_renderer import CapRenderer
from imagegen.rendering.primitives.connector.label_renderer import LabelRenderer
from imagegen.rendering.primitives.connector.pattern_engine import PatternEngine
from imagegen.ast_nodes import ColorValue, LengthValue, IdentValue, BoolValue
from imagegen.rendering.primitives.line_renderer import _resolve_color

if TYPE_CHECKING:
    from imagegen.ast_nodes import ConnectorNode
    from imagegen.error_reporter import ErrorReporter
    from imagegen.rendering.primitives.font_renderer import FontRenderer


class ConnectorRenderer(BaseRenderer):
    def __init__(self, reporter: ErrorReporter) -> None:
        super().__init__(reporter)
        self._route_builder = RouteBuilder()
        self._corner_styler = CornerStyler()
        self._cap_renderer = CapRenderer()
        self._label_renderer = LabelRenderer()
        self._pattern_engine = PatternEngine()
        self._font_renderer: FontRenderer | None = None
        # Set by the dispatcher before each frame so animated connectors advance correctly
        self._frame_index: int = 0

    def set_font_renderer(self, font_renderer: FontRenderer) -> None:
        self._font_renderer = font_renderer

    def set_frame_index(self, frame_index: int) -> None:
        self._frame_index = frame_index

    def render(
        self,
        canvas: Image.Image,
        node: ConnectorNode,  # type: ignore[override]
        base_dir: pathlib.Path,
    ) -> None:
        params = node.params
        aa_scale = canvas.info.get("aa_scale", 1)
        color_val = params.get("color")
        color = _resolve_color(color_val, canvas.mode) if isinstance(color_val, ColorValue) else (0, 0, 0)

        line_width = self._px(canvas, params["line-width"]) if isinstance(params.get("line-width"), LengthValue) else aa_scale

        # Pattern / animation
        pattern_val = params.get("pattern")
        pattern = pattern_val.name if isinstance(pattern_val, IdentValue) else "solid"
        animated_val = params.get("animated")
        animated = animated_val.value if isinstance(animated_val, BoolValue) else False
        speed_val = params.get("pattern-speed")
        pattern_speed = float(speed_val.number) if isinstance(speed_val, LengthValue) else 5.0

        # Corner style: `corner=` is the DSL-facing key; `corner-style=` remains
        # accepted as a compatibility alias.
        corner_val = params.get("corner")
        if corner_val is None:
            corner_val = params.get("corner-style")
        corner_style = corner_val.name if isinstance(corner_val, IdentValue) else "sharp"
        corner_radius_val = params.get("corner-radius")
        corner_radius = self._px(canvas, corner_radius_val) if isinstance(corner_radius_val, LengthValue) else None

        # Cap styles
        start_cap_val = params.get("start-cap")
        end_cap_val = params.get("end-cap")
        start_cap = start_cap_val.name if isinstance(start_cap_val, IdentValue) else "none"
        end_cap = end_cap_val.name if isinstance(end_cap_val, IdentValue) else "arrow"

        # 1. Build route geometry (points scaled by aa_scale, DPI-aware)
        dpi = canvas.info.get("dpi", (96, 96))[0]
        route = self._route_builder.build(node, (canvas.width, canvas.height), aa_scale, dpi)
        if len(route) < 2:
            return

        # 2. Apply corner styling — silently skipped for curved connectors
        connector_type_val = params.get("connector-type")
        connector_type = connector_type_val.name if isinstance(connector_type_val, IdentValue) else "straight"
        if connector_type != "curved":
            route = self._corner_styler.apply(route, corner_style, aa_scale, corner_radius)

        # 3. Draw stroke with pattern engine
        draw = ImageDraw.Draw(canvas)
        self._pattern_engine.draw_stroke(
            draw=draw,
            route=route,
            pattern=pattern,
            color=color,
            line_width=line_width,
            animated=animated,
            pattern_speed=pattern_speed,
            frame_index=self._frame_index,
            aa_scale=aa_scale,
        )

        # 4. Draw caps
        if start_cap != "none":
            angle = self._cap_renderer.endpoint_angle(route, at_end=False)
            self._cap_renderer.render_cap(draw, route[0], angle + math.pi, start_cap, color, aa_scale)

        if end_cap != "none":
            angle = self._cap_renderer.endpoint_angle(route, at_end=True)
            self._cap_renderer.render_cap(draw, route[-1], angle, end_cap, color, aa_scale)

        # 5. Draw label
        if self._font_renderer is not None:
            self._label_renderer.render(canvas, route, params, self._font_renderer, aa_scale)
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
