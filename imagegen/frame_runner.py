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
"""Frame Runner (REQ-0002, REQ-0002.1, REQ-0002.2, REQ-0002.3).

Iterates frame definitions in declaration order.
Each frame produces an independent canvas — no state is shared between frames.
Returns a list of (FrameDef, PIL Image) pairs for the OutputFormatter.
"""

from __future__ import annotations

import dataclasses
import pathlib
from typing import TYPE_CHECKING

from PIL import Image

from imagegen.ast_nodes import (
    Background, GridNode, FrameDef, FontNode,
    PointValue, LengthValue, IdentValue, BoolValue,
    CircleNode, PieNode, ArcNode,
    VarDeclStmt, AssignStmt, NamedDrawCmd,
)
from imagegen.rendering.canvas_factory import CanvasFactory
from imagegen.rendering.background_renderer import BackgroundRenderer
from imagegen.rendering.grid_renderer import render_grid
from imagegen.rendering.bbox_renderer import render_bbox_overlays
from imagegen.rendering.primitive_dispatcher import PrimitiveDispatcher
from imagegen.rendering.object_instantiator import ObjectInstantiator
from imagegen.rendering.function_executor import FunctionExecutor
from imagegen.rendering.variable_store import VariableStore
from imagegen.rendering.primitives.line_renderer import LineRenderer
from imagegen.rendering.primitives.circle_renderer import CircleRenderer
from imagegen.rendering.primitives.square_renderer import SquareRenderer
from imagegen.rendering.primitives.polygon_renderer import PolygonRenderer
from imagegen.rendering.primitives.path_renderer import PathRenderer
from imagegen.rendering.primitives.pie_renderer import PieRenderer
from imagegen.rendering.primitives.arc_renderer import ArcRenderer
from imagegen.rendering.primitives.font_renderer import FontRenderer
from imagegen.rendering.primitives.image_renderer import ImageRenderer
from imagegen.rendering.primitives.connector.connector_renderer import ConnectorRenderer

if TYPE_CHECKING:
    from imagegen.error_reporter import ErrorReporter
    from imagegen.symbol_table import SymbolTable

# Supersampling factor: render at AA_SCALE× resolution, downscale with LANCZOS.
# Set to 1 to disable antialiasing.
_AA_SCALE = 2


class FrameRunner:
    def __init__(
        self,
        symbol_table: SymbolTable,
        reporter: ErrorReporter,
        base_dir: pathlib.Path,
    ) -> None:
        self._symbol_table = symbol_table
        self._reporter = reporter
        self._base_dir = base_dir
        self._canvas_factory = CanvasFactory()
        self._background_renderer = BackgroundRenderer(reporter)

        # Build renderer registry
        font_renderer = FontRenderer(reporter)
        connector_renderer = ConnectorRenderer(reporter)
        connector_renderer.set_font_renderer(font_renderer)

        self._renderers = {
            "line":      LineRenderer(reporter),
            "circle":    CircleRenderer(reporter),
            "square":    SquareRenderer(reporter),
            "polygon":   PolygonRenderer(reporter),
            "path":      PathRenderer(reporter),
            "pie":       PieRenderer(reporter),
            "arc":       ArcRenderer(reporter),
            "font":      font_renderer,
            "image":     ImageRenderer(reporter),
            "connector": connector_renderer,
        }

        object_instantiator = ObjectInstantiator(reporter)
        function_executor = FunctionExecutor(reporter)

        self._dispatcher = PrimitiveDispatcher(
            renderers=self._renderers,
            object_instantiator=object_instantiator,
            function_executor=function_executor,
            reporter=reporter,
        )

    def run_frames(
        self,
        frames: list[FrameDef],
    ) -> list[tuple[FrameDef, Image.Image]]:
        """Iterate frames in declaration order.

        Each frame produces an independent canvas — no state is shared between frames.
        Returns list of (FrameDef, rendered_image) pairs.
        """
        results: list[tuple[FrameDef, Image.Image]] = []
        for frame_index, frame in enumerate(frames):
            rendered = self._run_single_frame(frame, frame_index)
            results.append((frame, rendered))
        return results

    def _run_single_frame(self, frame: FrameDef, frame_index: int) -> Image.Image:
        canvas = self._canvas_factory.create(frame.image_def, aa_scale=_AA_SCALE)

        # Render background first (must appear before other drawing commands)
        for cmd in frame.body:
            if isinstance(cmd, Background):
                self._background_renderer.render(canvas, cmd, self._base_dir)
                break  # only one background per frame; validator enforces this

        # Process commands sequentially so that each grid() activates immediately
        # for the commands that follow it.  Multiple grid() statements are allowed —
        # each one replaces the active grid for subsequent drawing commands.
        current_grid = None
        grid_nodes: list[GridNode] = []
        geometry_cmds = []
        text_cmds = []

        for cmd in frame.body:
            if isinstance(cmd, Background):
                continue
            if isinstance(cmd, GridNode):
                current_grid = cmd
                grid_nodes.append(cmd)
                continue
            # Variable statement nodes (FEA-007): always go to the geometry pass so
            # that variable assignments are available before text rendering.
            if isinstance(cmd, (VarDeclStmt, AssignStmt, NamedDrawCmd)):
                geometry_cmds.append(cmd)
                continue
            # Alignment is the last coordinate-adjustment step for each element.
            if current_grid is not None:
                cmd = _apply_snap(cmd, current_grid)
            if isinstance(cmd, FontNode):
                text_cmds.append(cmd)
            else:
                geometry_cmds.append(cmd)

        # Text (FontNode) is excluded from the supersampled pass: TrueType fonts
        # already carry their own hinting/AA, so downscaling them with LANCZOS
        # double-blurs and makes them unreadable.  Geometry gets the AA pass;
        # text is composited onto the final 1× canvas afterwards.
        # A fresh VariableStore is shared across both passes so that variables
        # set during the geometry pass are visible during the text pass (FEA-007).
        frame_vars = VariableStore()
        self._dispatcher.dispatch_all(
            canvas=canvas,
            commands=geometry_cmds,
            symbol_table=self._symbol_table,
            base_dir=self._base_dir,
            frame_index=frame_index,
            variable_store=frame_vars,
        )

        # Downscale geometry layer to target resolution with LANCZOS
        if _AA_SCALE > 1:
            target_size = canvas.info.get("target_size")
            if target_size:
                canvas = canvas.resize(target_size, Image.LANCZOS)
                # Tell renderers we are now at 1× so coordinates are not re-scaled
                canvas.info["aa_scale"] = 1

        # Render text at 1× directly on the final canvas — sharp, no LANCZOS blur
        if text_cmds:
            self._dispatcher.dispatch_all(
                canvas=canvas,
                commands=text_cmds,
                symbol_table=self._symbol_table,
                base_dir=self._base_dir,
                frame_index=frame_index,
                variable_store=frame_vars,
            )

        # Render grid lines as a post-process on the final 1× canvas, in order
        for grid_node in grid_nodes:
            render_grid(canvas, grid_node)

        # Render bounding-box overlays for elements with show-bbox=true (FEA-005)
        render_bbox_overlays(canvas, geometry_cmds + text_cmds, self._symbol_table)

        return canvas


_CENTER_BASED_NODES = (CircleNode, PieNode, ArcNode)

_VALID_ALIGN_ORIGINS = frozenset({"left-top", "right-top", "left-bottom", "right-bottom", "center"})


def _snap_axis(value: float, step: float, offset: float) -> float:
    relative = value - offset
    return round(relative / step) * step + offset


def _get_size(params: dict) -> tuple[float, float]:
    """Return (width, height) of the element's axis-aligned bounding box in px."""
    r_val = params.get("radius")
    if isinstance(r_val, LengthValue):
        d = r_val.number * 2
        return d, d
    w_val = params.get("width")
    h_val = params.get("height")
    w = w_val.number if isinstance(w_val, LengthValue) else 0.0
    h = h_val.number if isinstance(h_val, LengthValue) else 0.0
    return w, h


def _apply_snap(cmd: object, grid: GridNode) -> object:
    """Return an align-adjusted copy of cmd, or cmd unchanged when alignment doesn't apply.

    Per-element `align=true/false` overrides the grid's global `align` setting.
    `align-origin` selects which bounding-box reference point is snapped to the grid.
    Alignment is the last coordinate-adjustment step — transforms are applied by the
    renderer around the already-snapped position.
    """
    params = getattr(cmd, 'params', None)
    if not isinstance(params, dict):
        return cmd

    # Determine effective alignment: per-element override beats global grid setting
    elem_align = params.get("align")
    global_align_val = grid.params.get("align")
    global_align = isinstance(global_align_val, BoolValue) and global_align_val.value

    if isinstance(elem_align, BoolValue):
        if not elem_align.value:
            return cmd  # align=false on this element
    elif not global_align:
        return cmd  # no per-element override and global align is off

    # Determine whether this node uses center or pos as its anchor
    center_based = isinstance(cmd, _CENTER_BASED_NODES)
    if center_based:
        pos_key = "center"
    else:
        pos_key = next(
            (k for k in ("pos", "from") if k in params and isinstance(params[k], PointValue)),
            None,
        )

    if pos_key is None or not isinstance(params.get(pos_key), PointValue):
        return cmd

    anchor = params[pos_key]
    ax, ay = anchor.x.number, anchor.y.number

    # align-origin: which bounding-box point is snapped to the grid
    origin_val = params.get("align-origin")
    if isinstance(origin_val, IdentValue) and origin_val.name in _VALID_ALIGN_ORIGINS:
        origin = origin_val.name
    else:
        origin = "center" if center_based else "left-top"

    # Size of the element's bounding box (needed for non-anchor reference points)
    w, h = _get_size(params)

    # Offset from anchor to reference point
    if center_based:
        offsets = {
            "center":       ( 0.0,   0.0),
            "left-top":     (-w/2,  -h/2),
            "right-top":    ( w/2,  -h/2),
            "left-bottom":  (-w/2,   h/2),
            "right-bottom": ( w/2,   h/2),
        }
    else:
        offsets = {
            "left-top":     (0.0,  0.0),
            "center":       (w/2,  h/2),
            "right-top":    (w,    0.0),
            "left-bottom":  (0.0,  h),
            "right-bottom": (w,    h),
        }
    off_x, off_y = offsets.get(origin, (0.0, 0.0))

    # Snap the reference point
    step_x_val = grid.params.get("step-x")
    step_y_val = grid.params.get("step-y")
    offset_x_val = grid.params.get("offset-x")
    offset_y_val = grid.params.get("offset-y")
    step_x = step_x_val.number if isinstance(step_x_val, LengthValue) else 1.0
    step_y = step_y_val.number if isinstance(step_y_val, LengthValue) else 1.0
    grid_ox = offset_x_val.number if isinstance(offset_x_val, LengthValue) else 0.0
    grid_oy = offset_y_val.number if isinstance(offset_y_val, LengthValue) else 0.0

    snapped_ref_x = _snap_axis(ax + off_x, step_x, grid_ox)
    snapped_ref_y = _snap_axis(ay + off_y, step_y, grid_oy)

    # Reverse the offset to get the new anchor position
    new_pos = PointValue(
        x=LengthValue(number=snapped_ref_x - off_x, unit=anchor.x.unit),
        y=LengthValue(number=snapped_ref_y - off_y, unit=anchor.y.unit),
    )
    return dataclasses.replace(cmd, params={**params, pos_key: new_pos})
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
