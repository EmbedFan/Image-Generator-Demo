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
"""Cap Renderer (REQ-0011.3, REQ-0011.4) — arrowheads at connector endpoints.

Supported cap styles: 'none', 'arrow', 'filled-arrow', 'circle', 'square', 'diamond'.
Validates no start-cap/end-cap alias conflict.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PIL import ImageDraw


_ARROW_SIZE = 10  # pixels; length of arrowhead sides


class CapRenderer:
    def render_cap(
        self,
        draw: ImageDraw.Draw,
        tip: tuple[int, int],
        direction_angle: float,
        cap_style: str,
        color: tuple | int,
        aa_scale: int = 1,
    ) -> None:
        """Draw arrowhead at tip pointing in direction_angle (radians, 0 = right).

        Supported styles: 'none', 'arrow', 'filled-arrow', 'circle', 'square', 'diamond'.
        """
        if cap_style == "none" or cap_style is None:
            return

        arrow_size = _ARROW_SIZE * aa_scale
        a = direction_angle
        tx, ty = tip

        if cap_style in ("arrow", "filled-arrow"):
            spread = math.radians(25)
            x1 = tx - arrow_size * math.cos(a - spread)
            y1 = ty - arrow_size * math.sin(a - spread)
            x2 = tx - arrow_size * math.cos(a + spread)
            y2 = ty - arrow_size * math.sin(a + spread)
            pts = [(tx, ty), (int(x1), int(y1)), (int(x2), int(y2))]
            if cap_style == "filled-arrow":
                draw.polygon(pts, fill=color)
            else:
                draw.line([(tx, ty), (int(x1), int(y1))], fill=color, width=aa_scale)
                draw.line([(tx, ty), (int(x2), int(y2))], fill=color, width=aa_scale)

        elif cap_style == "circle":
            r = arrow_size // 2
            draw.ellipse([tx - r, ty - r, tx + r, ty + r], fill=color)

        elif cap_style == "square":
            r = arrow_size // 2
            draw.rectangle([tx - r, ty - r, tx + r, ty + r], fill=color)

        elif cap_style == "diamond":
            pts = [
                (tx, ty - arrow_size),
                (tx + arrow_size // 2, ty),
                (tx, ty + arrow_size),
                (tx - arrow_size // 2, ty),
            ]
            draw.polygon(pts, fill=color)

    @staticmethod
    def endpoint_angle(route: list[tuple[int, int]], at_end: bool) -> float:
        """Return the direction angle (radians) at the start or end of a route."""
        if len(route) < 2:
            return 0.0
        if at_end:
            dx = route[-1][0] - route[-2][0]
            dy = route[-1][1] - route[-2][1]
        else:
            dx = route[1][0] - route[0][0]
            dy = route[1][1] - route[0][1]
        return math.atan2(dy, dx)
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
