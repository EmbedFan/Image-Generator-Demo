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
"""Route Builder (REQ-0011.2) — computes connector geometry.

Three connector-type values:
  'straight' — direct line between endpoints
  'curved'   — Catmull-Rom spline through all waypoints
  'step'     — horizontal–vertical–horizontal (H-V-H) routing
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from imagegen.ast_nodes import PointValue, PointList, LengthValue

if TYPE_CHECKING:
    from imagegen.ast_nodes import ConnectorNode

_CM_PER_INCH = 2.54
_MM_PER_INCH = 25.4
_PT_PER_INCH = 72.0


def _lv_to_px(length: LengthValue, dpi: int, aa: int) -> int:
    n = length.number
    unit = length.unit
    if unit in ("px", ""):
        raw = n
    elif unit == "pt":
        raw = n / _PT_PER_INCH * dpi
    elif unit == "cm":
        raw = n / _CM_PER_INCH * dpi
    elif unit == "mm":
        raw = n / _MM_PER_INCH * dpi
    elif unit == "em":
        raw = n * 12.0 / _PT_PER_INCH * dpi
    elif unit == "%":
        raw = n / 100.0 * 1000
    else:
        raw = n
    return int(round(raw * aa))


class RouteBuilder:
    def build(
        self,
        node: ConnectorNode,
        canvas_size: tuple[int, int],
        aa_scale: int = 1,
        dpi: int = 96,
    ) -> list[tuple[int, int]]:
        """Return ordered list of pixel coordinates for the connector stroke."""
        params = node.params

        connector_type_val = params.get("connector-type")
        connector_type = connector_type_val.name if hasattr(connector_type_val, "name") else "straight"

        # Collect control points from 'points' list or 'start'/'end' pair
        points = self._extract_points(params, aa_scale, dpi)
        if len(points) < 2:
            return points

        if connector_type == "curved":
            return self._curved_catmull_rom(points)
        if connector_type == "step":
            return self._step_hvh(points[0], points[-1])
        return self._straight(points)

    @staticmethod
    def _extract_points(params: dict, aa_scale: int = 1, dpi: int = 96) -> list[tuple[int, int]]:
        if "points" in params and isinstance(params["points"], PointList):
            return [(_lv_to_px(p.x, dpi, aa_scale), _lv_to_px(p.y, dpi, aa_scale)) for p in params["points"].points]
        pts = []
        start = params.get("start")
        end = params.get("end")
        if isinstance(start, PointValue):
            pts.append((_lv_to_px(start.x, dpi, aa_scale), _lv_to_px(start.y, dpi, aa_scale)))
        if isinstance(end, PointValue):
            pts.append((_lv_to_px(end.x, dpi, aa_scale), _lv_to_px(end.y, dpi, aa_scale)))
        return pts

    @staticmethod
    def _straight(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Direct line — return endpoints unchanged."""
        return points

    @staticmethod
    def _curved_catmull_rom(
        points: list[tuple[int, int]],
        steps: int = 20,
    ) -> list[tuple[int, int]]:
        """Catmull-Rom spline through all control points.

        Phantom points are added at both ends to ensure the spline passes
        through the first and last control points.
        """
        if len(points) < 2:
            return points

        # Extend with phantom points
        p0 = (2 * points[0][0] - points[1][0], 2 * points[0][1] - points[1][1])
        pn = (2 * points[-1][0] - points[-2][0], 2 * points[-1][1] - points[-2][1])
        pts = [p0] + points + [pn]

        result: list[tuple[int, int]] = []
        for i in range(1, len(pts) - 2):
            p0_, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
            for s in range(steps + 1):
                t = s / steps
                t2, t3 = t * t, t * t * t
                x = 0.5 * (
                    2 * p1[0]
                    + (-p0_[0] + p2[0]) * t
                    + (2 * p0_[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                    + (-p0_[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
                )
                y = 0.5 * (
                    2 * p1[1]
                    + (-p0_[1] + p2[1]) * t
                    + (2 * p0_[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                    + (-p0_[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
                )
                result.append((int(x), int(y)))
        return result

    @staticmethod
    def _step_hvh(
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """H-V-H (horizontal–vertical–horizontal) routing.

        Midpoint is the horizontal midpoint between start and end.
        """
        mid_x = (start[0] + end[0]) // 2
        return [
            start,
            (mid_x, start[1]),
            (mid_x, end[1]),
            end,
        ]
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
