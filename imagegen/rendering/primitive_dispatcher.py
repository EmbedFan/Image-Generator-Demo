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
"""Primitive Dispatcher (REQ-0018, REQ-0019) — z-index sort + route to renderer.

Z-order rule:
  - Primitives without explicit z-index retain their declaration order (stable sort).
  - Primitives with explicit z-index override their slot.
  - Valid z-index range: 0–1000 (validated by SemanticValidator).

Variable execution mode (FEA-007):
  - When a frame body contains VarDeclStmt, AssignStmt, or NamedDrawCmd, all
    commands in that dispatch call are executed in declaration order (no z-sort).
    This preserves the sequential evaluation semantics required for bbox access.
  - Pure drawing frames (no variable statements) continue to use z-sort.
"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

from PIL import Image

from imagegen.ast_nodes import (
    Background,
    LineNode, CircleNode, SquareNode, PolygonNode, PathNode,
    PieNode, ArcNode, ConnectorNode, FontNode, ImagePrimNode,
    ObjectInst, FuncCall,
    VarDeclStmt, AssignStmt, NamedDrawCmd, DoWhileStmt,
    LengthValue, PointValue, PointList,
    ExprFactor, ExprBinOp, ExprBboxAccess, ExprPoint, ComparisonExpr,
    StringValue,
)

if TYPE_CHECKING:
    from imagegen.ast_nodes import DrawingCmd, ExprNode, Value
    from imagegen.error_reporter import ErrorReporter
    from imagegen.symbol_table import SymbolTable
    from imagegen.rendering.primitives.base_renderer import BaseRenderer
    from imagegen.rendering.object_instantiator import ObjectInstantiator
    from imagegen.rendering.function_executor import FunctionExecutor
    from imagegen.rendering.variable_store import VariableStore


class PrimitiveDispatcher:
    MAX_DO_WHILE_ITERATIONS = 1000

    def __init__(
        self,
        renderers: dict[str, BaseRenderer],
        object_instantiator: ObjectInstantiator,
        function_executor: FunctionExecutor,
        reporter: ErrorReporter,
    ) -> None:
        self._renderers = renderers
        self._object_instantiator = object_instantiator
        self._function_executor = function_executor
        self._reporter = reporter

    def dispatch_all(
        self,
        canvas: Image.Image,
        commands: list[DrawingCmd],
        symbol_table: SymbolTable,
        base_dir: pathlib.Path,
        frame_index: int,
        variable_store: VariableStore | None = None,
    ) -> None:
        """Sort commands by z-index (stable) then dispatch, unless variable statements
        are present — in that case execute sequentially in declaration order.
        """
        has_var_stmts = any(
            isinstance(cmd, (VarDeclStmt, AssignStmt, NamedDrawCmd, DoWhileStmt))
            for cmd in commands
        )

        if has_var_stmts:
            # Sequential execution to support variable/bbox dependencies
            for cmd in commands:
                self._dispatch_one(cmd, canvas, symbol_table, base_dir, frame_index, variable_store)
        else:
            sorted_cmds = self._sort_by_z(commands)
            for cmd in sorted_cmds:
                self._dispatch_one(cmd, canvas, symbol_table, base_dir, frame_index, variable_store)

    def _dispatch_one(
        self,
        cmd: DrawingCmd,
        canvas: Image.Image,
        symbol_table: SymbolTable,
        base_dir: pathlib.Path,
        frame_index: int,
        variable_store: VariableStore | None = None,
    ) -> None:
        # ---- Variable statement nodes (FEA-007) --------------------------------

        if isinstance(cmd, VarDeclStmt):
            if variable_store is not None:
                for name in cmd.names:
                    variable_store.declare(name)
            return

        if isinstance(cmd, AssignStmt):
            if variable_store is not None:
                value = self._eval_expr(cmd.value, variable_store, cmd.source_file, cmd.line)
                variable_store.assign(cmd.target, value, cmd.source_file, cmd.line, self._reporter)
            return

        if isinstance(cmd, NamedDrawCmd):
            inner = self._resolve_cmd(cmd.cmd, variable_store)
            renderer_key = _NODE_TO_KEY.get(type(inner))
            if renderer_key is not None:
                renderer = self._renderers.get(renderer_key)
                if renderer is not None:
                    if renderer_key == "connector" and hasattr(renderer, "set_frame_index"):
                        renderer.set_frame_index(frame_index)
                    renderer.render(canvas, inner, base_dir)
            if variable_store is not None:
                bbox = _compute_dsl_bbox(inner)
                if bbox is not None:
                    variable_store.register_object(cmd.binding_name, *bbox)
            return

        if isinstance(cmd, DoWhileStmt):
            iterations = 0
            while True:
                iterations += 1
                if iterations > self.MAX_DO_WHILE_ITERATIONS:
                    self._reporter.runtime_error(
                        cmd.source_file,
                        cmd.line,
                        f"do-while loop exceeded maximum iteration count {self.MAX_DO_WHILE_ITERATIONS}"
                    )
                for inner in cmd.body:
                    self._dispatch_one(inner, canvas, symbol_table, base_dir, frame_index, variable_store)
                if not self._eval_comparison(cmd.condition, variable_store):
                    break
            return

        # ---- Existing drawing commands -----------------------------------------

        if isinstance(cmd, Background):
            return

        if isinstance(cmd, ObjectInst):
            self._object_instantiator.instantiate(
                canvas, cmd, symbol_table, self, base_dir, frame_index
            )
            return

        if isinstance(cmd, FuncCall):
            self._function_executor.execute(
                canvas, cmd, symbol_table, self, base_dir, frame_index
            )
            return

        # Primitive nodes — resolve any expression params, then render
        resolved = self._resolve_cmd(cmd, variable_store)
        renderer_key = _NODE_TO_KEY.get(type(resolved))
        if renderer_key is None:
            return

        renderer = self._renderers.get(renderer_key)
        if renderer is None:
            self._reporter.warning(
                cmd.source_file, cmd.line,
                f"no renderer registered for '{renderer_key}'"
            )
            return

        if renderer_key == "connector" and hasattr(renderer, "set_frame_index"):
            renderer.set_frame_index(frame_index)

        renderer.render(canvas, resolved, base_dir)

    # ------------------------------------------------------------------
    # Expression evaluation (FEA-007)
    # ------------------------------------------------------------------

    def _eval_expr(
        self,
        expr: ExprNode,
        variable_store: VariableStore | None,
        source_file: str,
        line: int,
    ) -> float:
        """Recursively evaluate an arithmetic expression using the variable store."""
        if isinstance(expr, ExprFactor):
            if isinstance(expr.value, LengthValue):
                return expr.value.number
            if isinstance(expr.value, str):
                if variable_store is None:
                    return 0.0
                if not variable_store.has_var(expr.value):
                    self._reporter.runtime_error(
                        source_file, line,
                        f"'{expr.value}' is not a declared variable; "
                        f"declare with 'var {expr.value};' before use in expressions"
                    )
                val = variable_store.get(expr.value)
                if val is None:
                    self._reporter.runtime_error(
                        source_file, line,
                        f"variable '{expr.value}' is used before being assigned"
                    )
                return val
            return 0.0

        if isinstance(expr, ExprBboxAccess):
            if variable_store is None:
                return 0.0
            bbox = variable_store.get_bbox(expr.object_name, expr.source_file, expr.line, self._reporter)
            return bbox[{"x": 0, "y": 1, "width": 2, "height": 3}[expr.prop]]

        if isinstance(expr, ExprBinOp):
            left = self._eval_expr(expr.left, variable_store, source_file, line)
            right = self._eval_expr(expr.right, variable_store, source_file, line)
            if expr.op == "+":
                return left + right
            if expr.op == "-":
                return left - right
            if expr.op == "*":
                return left * right
            if expr.op == "/":
                if right == 0.0:
                    self._reporter.runtime_error(source_file, line, "division by zero")
                return left / right

        return 0.0

    def _eval_comparison(
        self,
        expr: ComparisonExpr,
        variable_store: VariableStore | None,
    ) -> bool:
        left = self._eval_expr(expr.left, variable_store, expr.source_file, expr.line)
        right = self._eval_expr(expr.right, variable_store, expr.source_file, expr.line)
        if expr.op == "==":
            return left == right
        if expr.op == "!=":
            return left != right
        if expr.op == "<":
            return left < right
        if expr.op == "<=":
            return left <= right
        if expr.op == ">":
            return left > right
        if expr.op == ">=":
            return left >= right
        self._reporter.runtime_error(expr.source_file, expr.line, f"unsupported comparison operator '{expr.op}'")
        return False

    # ------------------------------------------------------------------
    # Expression resolution in command params
    # ------------------------------------------------------------------

    def _resolve_cmd(self, cmd: object, variable_store: VariableStore | None) -> object:
        """Return cmd with all ExprFactor/ExprBinOp/ExprBboxAccess/ExprPoint params resolved."""
        if variable_store is None or not hasattr(cmd, "params"):
            return cmd
        new_params: dict = {}
        changed = False
        for k, v in cmd.params.items():
            resolved = self._resolve_value(v, variable_store, cmd.source_file, cmd.line)
            new_params[k] = resolved
            if resolved is not v:
                changed = True
        if not changed:
            return cmd
        return type(cmd)(params=new_params, source_file=cmd.source_file, line=cmd.line)

    def _resolve_value(
        self,
        val: object,
        variable_store: VariableStore,
        source_file: str,
        line: int,
    ) -> object:
        if isinstance(val, ExprFactor):
            if isinstance(val.value, LengthValue):
                # Literal number wrapped by the expression parser — unwrap to LengthValue.
                return val.value
            if isinstance(val.value, str):
                # String ExprFactor: could be a frame variable or an enum-like IdentValue
                # (e.g. weight=bold).  Use the VariableStore scope to distinguish them:
                # declared variables are resolved to LengthValue; everything else falls
                # back to IdentValue for backward compatibility.
                if variable_store is not None and variable_store.has_var(val.value):
                    v = variable_store.get(val.value)
                    if v is None:
                        self._reporter.runtime_error(
                            source_file, line,
                            f"variable '{val.value}' is used before being assigned"
                        )
                    return LengthValue(number=v, unit="px")
                from imagegen.ast_nodes import IdentValue
                return IdentValue(name=val.value)
            return val

        if isinstance(val, (ExprBinOp, ExprBboxAccess)):
            num = self._eval_expr(val, variable_store, source_file, line)
            return LengthValue(number=num, unit="px")

        if isinstance(val, ExprPoint):
            x = self._eval_expr(val.x, variable_store, source_file, line)
            y = self._eval_expr(val.y, variable_store, source_file, line)
            return PointValue(
                x=LengthValue(number=x, unit="px"),
                y=LengthValue(number=y, unit="px"),
            )
        return val

    # ------------------------------------------------------------------
    # Z-sort
    # ------------------------------------------------------------------

    def _sort_by_z(self, commands: list[DrawingCmd]) -> list[DrawingCmd]:
        """Stable sort by z-index; commands without z-index use their declaration position."""
        def z_key(indexed: tuple[int, DrawingCmd]) -> tuple[int, int]:
            idx, cmd = indexed
            if hasattr(cmd, "params"):
                z_val = _unwrap_length(cmd.params.get("z-index"))
                if z_val is not None:
                    return (int(z_val.number), idx)
            return (500, idx)  # default z-index midpoint keeps relative order

        indexed = list(enumerate(commands))
        indexed.sort(key=z_key)
        return [cmd for _, cmd in indexed]


# ---------------------------------------------------------------------------
# DSL bounding-box computation (FEA-007)
# ---------------------------------------------------------------------------

def _unwrap_length(val: object) -> LengthValue | None:
    """Accept LengthValue or ExprFactor(LengthValue) produced by frame-body parsing."""
    if isinstance(val, LengthValue):
        return val
    if isinstance(val, ExprFactor) and isinstance(val.value, LengthValue):
        return val.value
    return None

def _compute_dsl_bbox(cmd: object) -> tuple[float, float, float, float] | None:
    """Compute (x, y, width, height) in DSL pixel coordinates from a primitive's params.

    Returns None when the required parameters are missing or the primitive type
    is not supported.  Coordinates are purely arithmetic on LengthValue.number
    fields — no canvas scaling is involved.
    """
    params = getattr(cmd, "params", None)
    if not isinstance(params, dict):
        return None

    if isinstance(cmd, SquareNode):
        pos = params.get("pos")
        w = params.get("width")
        h = params.get("height")
        if isinstance(pos, PointValue) and isinstance(w, LengthValue) and isinstance(h, LengthValue):
            return (pos.x.number, pos.y.number, w.number, h.number)

    elif isinstance(cmd, CircleNode):
        c = params.get("center")
        r = params.get("radius")
        if isinstance(c, PointValue) and isinstance(r, LengthValue):
            d = r.number * 2
            return (c.x.number - r.number, c.y.number - r.number, d, d)

    elif isinstance(cmd, LineNode):
        s = params.get("start")
        e = params.get("end")
        if isinstance(s, PointValue) and isinstance(e, PointValue):
            x0 = min(s.x.number, e.x.number)
            y0 = min(s.y.number, e.y.number)
            x1 = max(s.x.number, e.x.number)
            y1 = max(s.y.number, e.y.number)
            lw = params.get("line-width")
            pad = (lw.number / 2) if isinstance(lw, LengthValue) else 1.0
            return (x0 - pad, y0 - pad, x1 - x0 + pad * 2, y1 - y0 + pad * 2)

    elif isinstance(cmd, (PolygonNode, PathNode)):
        pts = params.get("points")
        if isinstance(pts, PointList) and pts.points:
            xs = [p.x.number for p in pts.points]
            ys = [p.y.number for p in pts.points]
            return (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

    elif isinstance(cmd, (PieNode, ArcNode)):
        c = params.get("center")
        r = params.get("radius")
        if isinstance(c, PointValue) and isinstance(r, LengthValue):
            d = r.number * 2
            return (c.x.number - r.number, c.y.number - r.number, d, d)

    elif isinstance(cmd, ImagePrimNode):
        pos = params.get("pos")
        w = params.get("width")
        h = params.get("height")
        if isinstance(pos, PointValue) and isinstance(w, LengthValue) and isinstance(h, LengthValue):
            return (pos.x.number, pos.y.number, w.number, h.number)

    elif isinstance(cmd, FontNode):
        pos = params.get("pos")
        size = params.get("font-size")
        text_val = params.get("text")
        if isinstance(pos, PointValue):
            fs = size.number if isinstance(size, LengthValue) else 16.0
            text_len = len(text_val.value) if isinstance(text_val, StringValue) else 8
            # Approximate bbox: width ≈ chars × 0.6 × font-size, height ≈ 1.2 × font-size
            return (pos.x.number, pos.y.number - fs, text_len * fs * 0.6, fs * 1.2)

    return None


# Map AST node type → renderer key string
_NODE_TO_KEY: dict[type, str] = {
    LineNode:      "line",
    CircleNode:    "circle",
    SquareNode:    "square",
    PolygonNode:   "polygon",
    PathNode:      "path",
    PieNode:       "pie",
    ArcNode:       "arc",
    ConnectorNode: "connector",
    FontNode:      "font",
    ImagePrimNode: "image",
}
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
