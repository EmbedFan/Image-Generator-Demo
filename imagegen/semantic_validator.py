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
"""Semantic Validator — type and constraint checks before rendering.

Halt-immediately conditions (raises ValidationError):
  - radius ≤ 0 on circle, pie, arc
  - polygon with < 3 points; path with < 2 points
  - 'fill' parameter present on arc
  - color=none on any stroke property (line color, border color)
  - JPEG output-format with RGBA or GRAY colorspace
  - negative scale transform
  - angle parameter with a unit suffix (rotate, start-angle, end-angle)
  - clip-shape=polygon on an object template
  - duplicate background statement in a frame (also a parse error, but validated here)

Warning-only conditions (emits warning, continues):
  - colorspace conflict between frame attribute and image statement
  - identical gradient start/end endpoints
  - conflicting output-format across frames
  - duplicate frame-id in 'images' mode
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from imagegen.ast_nodes import (
    FrameDef, ImageDef, Background, GridNode,
    ArcNode, CircleNode, PieNode,
    PolygonNode, PathNode,
    PointList, LengthValue, BoolValue, IdentValue, ColorNone, ExprFactor,
    ObjAttr, ObjTemplate, ObjectInst, FuncCall,
    DrawingCmd, PrimitiveNode,
)

if TYPE_CHECKING:
    from imagegen.ast_nodes import Value
    from imagegen.error_reporter import ErrorReporter
    from imagegen.symbol_table import SymbolTable


class SemanticValidator:
    """Validate types and constraints for drawing commands before rendering.

    Halt-immediately: radius<=0, fill on arc, color=none on stroke,
    JPEG+RGBA/GRAY, negative scale, angle with unit, clip-shape=polygon.
    Warning-only: colorspace conflict, identical gradient endpoints,
    conflicting output-format, duplicate frame-id in images mode.
    """

    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    def validate_frame(self, frame: FrameDef, symbol_table: SymbolTable) -> None:
        """Validate ImageDef and all drawing commands in a frame."""
        self._validate_image_def(frame.image_def, frame)

        # Pre-scan: check whether any grid is defined (needed for align= validation below)
        any_grid = any(isinstance(cmd, GridNode) for cmd in frame.body)

        background_count = 0
        for cmd in frame.body:
            if isinstance(cmd, Background):
                background_count += 1
                if background_count > 1:
                    self._reporter.validation_error(
                        cmd.source_file, cmd.line,
                        "only one 'background' statement is allowed per frame"
                    )
                if "show-bbox" in cmd.params:
                    self._reporter.validation_error(
                        cmd.source_file, cmd.line,
                        "'show-bbox' is not valid on 'background'; "
                        "it is only accepted on drawable primitives and object instances"
                    )
                self._validate_background(cmd, frame.image_def)
            elif isinstance(cmd, GridNode):
                if "show-bbox" in cmd.params:
                    self._reporter.validation_error(
                        cmd.source_file, cmd.line,
                        "'show-bbox' is not valid on 'grid'; "
                        "it is only accepted on drawable primitives and object instances"
                    )
                self._validate_grid(cmd)
            else:
                self._validate_drawing_cmd(cmd, frame.image_def, symbol_table)
                # Validate per-element align=true requires a grid in the frame
                params = getattr(cmd, 'params', None)
                if isinstance(params, dict) and not any_grid:
                    align_val = params.get("align")
                    if isinstance(align_val, BoolValue) and align_val.value:
                        self._reporter.validation_error(
                            cmd.source_file, cmd.line,
                            "align=true used but no grid() is defined in this frame"
                        )
                # Validate align-origin values
                if isinstance(params, dict) and "align-origin" in params:
                    ao = params["align-origin"]
                    if isinstance(ao, IdentValue) and ao.name not in (
                        "left-top", "right-top", "left-bottom", "right-bottom", "center"
                    ):
                        self._reporter.validation_error(
                            cmd.source_file, cmd.line,
                            f"align-origin: invalid value '{ao.name}'; "
                            f"expected left-top, right-top, left-bottom, right-bottom, or center"
                        )

    def _validate_image_def(self, image_def: ImageDef, frame: FrameDef) -> None:
        """Check JPEG+RGBA/GRAY and colorspace conflict warnings."""
        if image_def.output_format == "jpeg":
            if image_def.colorspace in ("RGBA", "GRAY"):
                self._reporter.validation_error(
                    image_def.source_file, image_def.line,
                    f"output-format 'jpeg' is not supported with colorspace '{image_def.colorspace}'"
                )
        # Colorspace conflict between frame attribute and image statement
        if frame.colorspace_attr and frame.colorspace_attr != image_def.colorspace:
            self._reporter.warning(
                image_def.source_file, image_def.line,
                f"colorspace '{frame.colorspace_attr}' in frame attributes overridden by "
                f"'{image_def.colorspace}' in image statement"
            )

    def _validate_grid(self, node: GridNode) -> None:
        """Validate grid statement: required params, step > 0, render=true color warning.

        Multiple grid() statements are allowed per frame; each one changes the active
        grid step for the drawing commands that follow it.
        """
        params = node.params
        step_x = params.get("step-x")
        step_y = params.get("step-y")

        if step_x is None or step_y is None:
            self._reporter.validation_error(
                node.source_file, node.line,
                "grid: 'step-x' and 'step-y' are required"
            )
            return

        sx = self._extract_number(step_x)
        sy = self._extract_number(step_y)

        if sx is not None and sx <= 0:
            self._reporter.validation_error(
                node.source_file, node.line,
                f"grid: 'step-x' must be > 0, got {sx}"
            )
        if sy is not None and sy <= 0:
            self._reporter.validation_error(
                node.source_file, node.line,
                f"grid: 'step-y' must be > 0, got {sy}"
            )

        render = params.get("render")
        color = params.get("color")
        if isinstance(render, BoolValue) and render.value and color is None:
            self._reporter.warning(
                node.source_file, node.line,
                "grid: render=true without color; defaulting to RGB(200,200,200)"
            )

    def _validate_background(self, node: Background, image_def: ImageDef) -> None:
        """Validate background parameters and gradient endpoint rule."""
        params = node.params
        # Gradient with identical start/end → warning
        if "color1" in params and "color2" in params:
            start = params.get("start")
            end = params.get("end")
            if start is not None and end is not None and str(start) == str(end):
                self._reporter.warning(
                    node.source_file, node.line,
                    "gradient 'start' and 'end' are identical; filling with color1"
                )

    def _validate_drawing_cmd(
        self,
        cmd: DrawingCmd,
        image_def: ImageDef,
        symbol_table: SymbolTable,
    ) -> None:
        from imagegen.ast_nodes import (
            LineNode, CircleNode, SquareNode, PolygonNode, PathNode,
            PieNode, ArcNode, ConnectorNode, FontNode, ImagePrimNode,
            ObjectInst, FuncCall,
        )
        if isinstance(cmd, CircleNode):
            self._check_radius_positive(cmd.params, cmd.source_file, cmd.line, "circle")
            self._check_transform_params(cmd.params, cmd.source_file, cmd.line)
        elif isinstance(cmd, PieNode):
            self._check_radius_positive(cmd.params, cmd.source_file, cmd.line, "pie")
            self._check_angle_no_unit(cmd.params, ["start-angle", "end-angle"],
                                      cmd.source_file, cmd.line)
            self._check_transform_params(cmd.params, cmd.source_file, cmd.line)
        elif isinstance(cmd, ArcNode):
            self._check_radius_positive(cmd.params, cmd.source_file, cmd.line, "arc")
            self._check_no_fill_on_arc(cmd.params, cmd.source_file, cmd.line)
            self._check_angle_no_unit(cmd.params, ["start-angle", "end-angle"],
                                      cmd.source_file, cmd.line)
            self._check_transform_params(cmd.params, cmd.source_file, cmd.line)
        elif isinstance(cmd, PolygonNode):
            self._check_min_points(cmd.params, 3, "polygon", cmd.source_file, cmd.line)
            self._check_transform_params(cmd.params, cmd.source_file, cmd.line)
        elif isinstance(cmd, PathNode):
            self._check_min_points(cmd.params, 2, "path", cmd.source_file, cmd.line)
            self._check_transform_params(cmd.params, cmd.source_file, cmd.line)
        elif isinstance(cmd, LineNode):
            self._check_color_not_none_on_stroke(cmd.params, "color", "line",
                                                  cmd.source_file, cmd.line)
            self._check_transform_params(cmd.params, cmd.source_file, cmd.line)
        elif isinstance(cmd, (SquareNode, FontNode, ImagePrimNode, ConnectorNode)):
            self._check_transform_params(cmd.params, cmd.source_file, cmd.line)
        elif isinstance(cmd, ObjectInst):
            self._validate_object_inst(cmd, symbol_table)
        elif isinstance(cmd, FuncCall):
            self._validate_func_call(cmd, symbol_table)

    # ------------------------------------------------------------------
    # Constraint helpers
    # ------------------------------------------------------------------

    def _check_radius_positive(
        self,
        params: dict,
        source_file: str,
        line: int,
        primitive: str,
    ) -> None:
        radius = params.get("radius")
        if radius is None:
            return
        num = self._extract_number(radius)
        if num is not None and num <= 0:
            self._reporter.validation_error(
                source_file, line,
                f"{primitive}: 'radius' must be > 0, got {num}"
            )

    def _check_min_points(
        self,
        params: dict,
        minimum: int,
        primitive: str,
        source_file: str,
        line: int,
    ) -> None:
        points = params.get("points")
        if points is None:
            return
        if isinstance(points, PointList):
            count = len(points.points)
            if count < minimum:
                self._reporter.validation_error(
                    source_file, line,
                    f"{primitive}: requires at least {minimum} points, got {count}"
                )

    def _check_no_fill_on_arc(self, params: dict, source_file: str, line: int) -> None:
        if "fill" in params:
            self._reporter.validation_error(
                source_file, line,
                "arc: 'fill' parameter is not supported on arc"
            )

    def _check_color_not_none_on_stroke(
        self,
        params: dict,
        key: str,
        primitive: str,
        source_file: str,
        line: int,
    ) -> None:
        val = params.get(key)
        if isinstance(val, ColorNone):
            self._reporter.validation_error(
                source_file, line,
                f"{primitive}: 'color=none' is not valid on a stroke-only primitive"
            )

    def _check_transform_params(self, params: dict, source_file: str, line: int) -> None:
        """Check scale >= 0 and angle parameters carry no unit suffix."""
        scale = params.get("scale")
        if scale is not None:
            num = self._extract_number(scale)
            if num is not None and num < 0:
                self._reporter.validation_error(
                    source_file, line,
                    "transform: 'scale' must be >= 0"
                )
        self._check_angle_no_unit(params, ["rotate"], source_file, line)

    def _check_angle_no_unit(
        self,
        params: dict,
        keys: list[str],
        source_file: str,
        line: int,
    ) -> None:
        """Angle parameters must be bare numbers without a unit suffix."""
        for key in keys:
            val = params.get(key)
            if val is None:
                continue
            if isinstance(val, LengthValue) and val.unit != "":
                self._reporter.validation_error(
                    source_file, line,
                    f"angle parameter '{key}' does not accept a unit suffix (got '{val.unit}')"
                )

    def _validate_object_inst(self, node: ObjectInst, symbol_table: SymbolTable) -> None:
        template = symbol_table.lookup_object(node.name)
        if template is None:
            self._reporter.validation_error(
                node.source_file, node.line,
                f"undefined object template '{node.name}'"
            )
        # clip-shape=polygon check (REQ-0025)
        for attr in template.attributes:
            if attr.key == "clip-shape":
                if isinstance(attr.value, IdentValue) and attr.value.name == "polygon":
                    self._reporter.validation_error(
                        attr.source_file, attr.line,
                        "object template: 'clip-shape=polygon' is not supported"
                    )
        # FEA-003: instance-time size and rotation validation (REQ-0036, REQ-0036.1, REQ-0036.2, REQ-0037)
        scale_val = node.params.get("scale")
        if scale_val is not None:
            num = self._extract_number(scale_val)
            if num is not None and num <= 0:
                self._reporter.validation_error(
                    node.source_file, node.line,
                    f"object '{node.name}': 'scale' must be > 0"
                )
        resize_mode = self._extract_ident_name(node.params.get("resize-mode"))
        if resize_mode is not None and resize_mode not in ("layout", "default"):
            self._reporter.validation_error(
                node.source_file, node.line,
                f"object '{node.name}': invalid resize-mode '{resize_mode}'; expected 'layout' or 'default'"
            )
        rotate_val = node.params.get("rotate")
        if rotate_val is not None:
            rotate_length = self._extract_length(rotate_val)
            if isinstance(rotate_length, LengthValue) and rotate_length.unit != "":
                self._reporter.validation_error(
                    node.source_file, node.line,
                    f"object '{node.name}': 'rotate' does not accept a unit suffix"
                )
            num = self._extract_number(rotate_val)
            if num is not None and num < 0:
                self._reporter.validation_error(
                    node.source_file, node.line,
                    f"object '{node.name}': 'rotate' must be >= 0"
                )
        # Warning: explicit width/height overrides scale (REQ-0036.2)
        has_explicit_size = "width" in node.params or "height" in node.params
        if has_explicit_size and scale_val is not None and resize_mode != "layout":
            self._reporter.warning(
                node.source_file, node.line,
                f"object '{node.name}': explicit width/height provided together with scale; scale is ignored"
            )

    def _validate_func_call(self, node: FuncCall, symbol_table: SymbolTable) -> None:
        decl = symbol_table.lookup_function(node.name)
        if decl is None:
            self._reporter.validation_error(
                node.source_file, node.line,
                f"undefined function '{node.name}'"
            )
        if len(node.args) != len(decl.params):
            self._reporter.validation_error(
                node.source_file, node.line,
                f"function '{node.name}' expects {len(decl.params)} argument(s), "
                f"got {len(node.args)}"
            )

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_number(val: object) -> float | None:
        if isinstance(val, LengthValue):
            return val.number
        if isinstance(val, ExprFactor) and isinstance(val.value, LengthValue):
            return val.value.number
        return None

    @staticmethod
    def _extract_length(val: object) -> LengthValue | None:
        if isinstance(val, LengthValue):
            return val
        if isinstance(val, ExprFactor) and isinstance(val.value, LengthValue):
            return val.value
        return None

    @staticmethod
    def _extract_ident_name(val: object) -> str | None:
        if isinstance(val, IdentValue):
            return val.name
        if isinstance(val, ExprFactor) and isinstance(val.value, str):
            return val.value
        return None
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
