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
"""Pattern Engine (REQ-0011.7, REQ-0011.8, REQ-0011.9).

Tiles repeating patterns along a connector route.
When animated=True, the phase is advanced by pattern_speed × frame_index pixels,
creating the illusion of flow along the connector.

Patterns: 'solid', 'dash', 'dot', 'arrow', 'zigzag'.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PIL import ImageDraw


class PatternEngine:
    def draw_stroke(
        self,
        draw: ImageDraw.Draw,
        route: list[tuple[int, int]],
        pattern: str,
        color: tuple | int,
        line_width: int,
        animated: bool,
        pattern_speed: float,
        frame_index: int,
        aa_scale: int = 1,
    ) -> None:
        """Tile repeating pattern along the route.

        When animated=True, advance phase by pattern_speed × frame_index pixels.
        aa_scale is applied to all hardcoded pixel constants.
        """
        if len(route) < 2:
            return

        phase = (pattern_speed * frame_index) if animated else 0.0

        if pattern == "solid" or pattern is None:
            self._draw_solid(draw, route, color, line_width)
        elif pattern == "dash":
            self._draw_tiled(draw, route, color, line_width, on=10 * aa_scale, off=6 * aa_scale, phase=phase)
        elif pattern == "dot":
            self._draw_tiled(draw, route, color, line_width, on=2 * aa_scale, off=6 * aa_scale, phase=phase)
        elif pattern == "arrow":
            self._draw_arrows(draw, route, color, line_width, spacing=20 * aa_scale, phase=phase)
        elif pattern == "zigzag":
            self._draw_zigzag(draw, route, color, line_width, amplitude=6 * aa_scale, period=12 * aa_scale, phase=phase)
        else:
            self._draw_solid(draw, route, color, line_width)

    @staticmethod
    def _draw_solid(
        draw: ImageDraw.Draw,
        route: list[tuple[int, int]],
        color: tuple | int,
        width: int,
    ) -> None:
        if len(route) >= 2:
            draw.line(route, fill=color, width=width)

    @staticmethod
    def _draw_tiled(
        draw: ImageDraw.Draw,
        route: list[tuple[int, int]],
        color: tuple | int,
        width: int,
        on: float,
        off: float,
        phase: float,
    ) -> None:
        """Walk the route arc-length and draw 'on' segments, skip 'off' gaps."""
        period = on + off
        dist = phase % period  # current position within the dash cycle
        drawing = dist < on

        prev = route[0]
        for curr in route[1:]:
            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
            seg_len = math.hypot(dx, dy)
            if seg_len == 0:
                prev = curr
                continue
            ux, uy = dx / seg_len, dy / seg_len
            pos = 0.0
            while pos < seg_len:
                remaining_in_phase = (on if drawing else off) - (dist % (on + off) if drawing else dist % (on + off) - on)
                step = min(seg_len - pos, max(0.1, (on if drawing else off) - (dist % period if drawing else dist % period - on)))
                # Simpler: just toggle at boundaries
                step = min(seg_len - pos, (on - dist % period) if drawing else (period - dist % period))
                step = max(step, 0.1)
                x0 = prev[0] + ux * pos
                y0 = prev[1] + uy * pos
                x1 = prev[0] + ux * (pos + step)
                y1 = prev[1] + uy * (pos + step)
                if drawing:
                    draw.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=color, width=width)
                pos += step
                dist = (dist + step) % period
                drawing = dist < on
            prev = curr

    @staticmethod
    def _draw_arrows(
        draw: ImageDraw.Draw,
        route: list[tuple[int, int]],
        color: tuple | int,
        width: int,
        spacing: float,
        phase: float,
    ) -> None:
        """Draw small arrowheads at regular intervals along the route."""
        # First draw the base line
        draw.line(route, fill=color, width=width)
        # Then overlay arrowheads
        dist = phase % spacing
        prev = route[0]
        for curr in route[1:]:
            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
            seg_len = math.hypot(dx, dy)
            if seg_len == 0:
                prev = curr
                continue
            ux, uy = dx / seg_len, dy / seg_len
            angle = math.atan2(dy, dx)
            sz = spacing // 3  # arrow size proportional to spacing
            while dist < seg_len:
                ax = int(prev[0] + ux * dist)
                ay = int(prev[1] + uy * dist)
                spread = math.radians(25)
                x1 = ax - sz * math.cos(angle - spread)
                y1 = ay - sz * math.sin(angle - spread)
                x2 = ax - sz * math.cos(angle + spread)
                y2 = ay - sz * math.sin(angle + spread)
                draw.line([(ax, ay), (int(x1), int(y1))], fill=color, width=width)
                draw.line([(ax, ay), (int(x2), int(y2))], fill=color, width=width)
                dist += spacing
            dist -= seg_len
            prev = curr

    @staticmethod
    def _draw_zigzag(
        draw: ImageDraw.Draw,
        route: list[tuple[int, int]],
        color: tuple | int,
        width: int,
        amplitude: float,
        period: float,
        phase: float,
    ) -> None:
        """Draw a zigzag pattern offset perpendicular to the route."""
        draw.line(route, fill=color, width=width)  # base line
        prev = route[0]
        for curr in route[1:]:
            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
            seg_len = math.hypot(dx, dy)
            if seg_len == 0:
                prev = curr
                continue
            ux, uy = dx / seg_len, dy / seg_len
            # Perpendicular
            px, py = -uy, ux
            steps = max(2, int(seg_len / 4))
            pts = []
            for s in range(steps + 1):
                t = s / steps
                along = t * seg_len
                zz = amplitude * math.sin(2 * math.pi * (along + phase) / period)
                x = prev[0] + ux * along + px * zz
                y = prev[1] + uy * along + py * zz
                pts.append((int(x), int(y)))
            if len(pts) >= 2:
                draw.line(pts, fill=color, width=width)
            prev = curr
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
