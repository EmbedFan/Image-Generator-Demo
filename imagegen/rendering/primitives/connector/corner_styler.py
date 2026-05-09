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
"""Corner Styler (REQ-0011.5) — modifies intermediate vertices.

Styles:
  'sharp'   — no modification (pass-through)
  'rounded' — insert quadratic Bézier control points at each corner
  'beveled' — clip corners with a fixed setback distance

Silently ignored for curved connectors (the route is already smooth).
"""

from __future__ import annotations

import math


_SETBACK = 10  # pixels for bevel/round corner setback


class CornerStyler:
    def apply(
        self,
        points: list[tuple[int, int]],
        style: str,
        aa_scale: int = 1,
        radius_px: int | None = None,
    ) -> list[tuple[int, int]]:
        """Return modified point list with styled corners at intermediate vertices."""
        if style == "sharp" or len(points) < 3:
            return points
        if style == "rounded":
            return self._rounded(points, aa_scale, radius_px)
        if style == "beveled":
            return self._beveled(points, aa_scale, radius_px)
        return points

    @staticmethod
    def _beveled(
        points: list[tuple[int, int]],
        aa_scale: int = 1,
        radius_px: int | None = None,
    ) -> list[tuple[int, int]]:
        """Clip each intermediate corner at a fixed setback distance."""
        if len(points) < 3:
            return points
        setback = radius_px if radius_px is not None else _SETBACK * aa_scale
        result = [points[0]]
        for i in range(1, len(points) - 1):
            prev_ = points[i - 1]
            curr = points[i]
            next_ = points[i + 1]

            # Direction from prev to curr
            d1x, d1y = curr[0] - prev_[0], curr[1] - prev_[1]
            len1 = math.hypot(d1x, d1y) or 1
            u1x, u1y = d1x / len1, d1y / len1

            # Direction from curr to next
            d2x, d2y = next_[0] - curr[0], next_[1] - curr[1]
            len2 = math.hypot(d2x, d2y) or 1
            u2x, u2y = d2x / len2, d2y / len2

            sb = min(setback, len1 / 2, len2 / 2)
            p_in  = (int(curr[0] - u1x * sb), int(curr[1] - u1y * sb))
            p_out = (int(curr[0] + u2x * sb), int(curr[1] + u2y * sb))
            result.extend([p_in, p_out])

        result.append(points[-1])
        return result

    @staticmethod
    def _rounded(
        points: list[tuple[int, int]],
        aa_scale: int = 1,
        radius_px: int | None = None,
    ) -> list[tuple[int, int]]:
        """Approximate rounded corners with a quadratic Bézier interpolation."""
        if len(points) < 3:
            return points
        setback = radius_px if radius_px is not None else _SETBACK * aa_scale
        result = [points[0]]
        for i in range(1, len(points) - 1):
            prev_ = points[i - 1]
            curr = points[i]
            next_ = points[i + 1]

            d1x, d1y = curr[0] - prev_[0], curr[1] - prev_[1]
            len1 = math.hypot(d1x, d1y) or 1
            d2x, d2y = next_[0] - curr[0], next_[1] - curr[1]
            len2 = math.hypot(d2x, d2y) or 1

            sb = min(setback, len1 / 2, len2 / 2)
            u1x, u1y = d1x / len1, d1y / len1
            u2x, u2y = d2x / len2, d2y / len2

            p_in  = (curr[0] - u1x * sb, curr[1] - u1y * sb)
            p_out = (curr[0] + u2x * sb, curr[1] + u2y * sb)

            # Approximate the quadratic Bézier with several line segments
            steps = 8
            for s in range(steps + 1):
                t = s / steps
                x = (1 - t) ** 2 * p_in[0] + 2 * (1 - t) * t * curr[0] + t ** 2 * p_out[0]
                y = (1 - t) ** 2 * p_in[1] + 2 * (1 - t) * t * curr[1] + t ** 2 * p_out[1]
                result.append((int(x), int(y)))

        result.append(points[-1])
        return result
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
