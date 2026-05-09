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
"""Function Executor (REQ-0015, REQ-0015.1–REQ-0015.3).

Steps per execution:
  1. Lookup function declaration in symbol_table.functions.
  2. Bind positional arguments to parameter names.
  3. Evaluate arithmetic expressions in body params using bindings.
  4. Detect recursion via call_stack; raise DslRuntimeError if found.
  5. Execute body drawing commands via the dispatcher.

Division by zero in _evaluate_expr raises DslRuntimeError (REQ-0015.3).
Recursion detection uses a frozenset of names currently on the call stack.

Variable support (FEA-007):
  Function bodies may also contain VarDeclStmt, AssignStmt, NamedDrawCmd.
  These are partially resolved (function parameter references substituted) by
  _resolve_cmd, then executed at dispatch time with a fresh function-scoped
  VariableStore.
"""

from __future__ import annotations

import copy
import pathlib
from typing import TYPE_CHECKING

from PIL import Image

from imagegen.ast_nodes import (
    FuncCall,
    ExprFactor, ExprBinOp, ExprBboxAccess, ExprPoint, ComparisonExpr,
    LengthValue, PointValue, StringValue, IdentValue,
    DrawingCmd,
    VarDeclStmt, AssignStmt, NamedDrawCmd, DoWhileStmt,
)
from imagegen.rendering.variable_store import VariableStore

if TYPE_CHECKING:
    from imagegen.ast_nodes import FuncCall, FuncDecl, Value, ExprNode
    from imagegen.error_reporter import ErrorReporter
    from imagegen.symbol_table import SymbolTable
    from imagegen.rendering.primitive_dispatcher import PrimitiveDispatcher


class FunctionExecutor:
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    def execute(
        self,
        canvas: Image.Image,
        node: FuncCall,
        symbol_table: SymbolTable,
        dispatcher: PrimitiveDispatcher,
        base_dir: pathlib.Path,
        frame_index: int,
        call_stack: frozenset[str] | None = None,
    ) -> None:
        """Lookup, bind args, evaluate exprs, detect recursion, execute body."""
        if call_stack is None:
            call_stack = frozenset()

        decl = symbol_table.lookup_function(node.name)
        if decl is None:
            self._reporter.validation_error(
                node.source_file, node.line,
                f"undefined function '{node.name}'"
            )

        # Recursion detection: a function that calls itself (REQ-0015.3)
        if node.name in call_stack:
            self._reporter.runtime_error(
                node.source_file, node.line,
                f"recursion detected: function '{node.name}' calls itself"
            )

        bindings = self._bind_args(decl, node.args, node.source_file, node.line)

        new_call_stack = call_stack | {node.name}

        # Rewrite body commands: substitute function parameter expr nodes with concrete values.
        # VarDeclStmt / AssignStmt / NamedDrawCmd are handled by the dispatcher at runtime
        # using a fresh function-scoped VariableStore.
        resolved_body = [
            self._resolve_cmd(cmd, bindings, node.source_file, node.line)
            for cmd in decl.body
        ]

        # Fresh variable store for this function invocation (separate from frame scope)
        func_var_store = VariableStore()

        dispatcher.dispatch_all(
            canvas, resolved_body, symbol_table, base_dir, frame_index,
            variable_store=func_var_store,
        )

    def _bind_args(
        self,
        decl: FuncDecl,
        args: tuple[Value, ...],
        source_file: str,
        line: int,
    ) -> dict[str, Value]:
        """Map positional arguments to parameter names, preserving their value types."""
        if len(args) != len(decl.params):
            self._reporter.runtime_error(
                source_file, line,
                f"function '{decl.name}' expects {len(decl.params)} argument(s), "
                f"got {len(args)}"
            )
        bindings: dict[str, Value] = {}
        for name, val in zip(decl.params, args):
            if isinstance(val, ExprFactor) and isinstance(val.value, LengthValue):
                bindings[name] = val.value
            else:
                bindings[name] = copy.deepcopy(val)
        return bindings

    def _evaluate_expr(
        self,
        expr: ExprNode,
        bindings: dict[str, Value],
        source_file: str,
        line: int,
    ) -> float:
        """Recursively evaluate an arithmetic expression against function parameter bindings.

        Division by zero raises DslRuntimeError (REQ-0015.3).
        ExprBboxAccess cannot be pre-resolved at function-binding time — returns 0.0
        (it will be resolved at runtime by the dispatcher via the function VariableStore).
        """
        if isinstance(expr, ExprFactor):
            if isinstance(expr.value, LengthValue):
                return expr.value.number
            if isinstance(expr.value, str):
                bound = bindings.get(expr.value)
                if isinstance(bound, LengthValue):
                    return bound.number
                return 0.0
            return 0.0
        if isinstance(expr, ExprBboxAccess):
            # Cannot pre-evaluate at binding time; leave for runtime resolution
            return 0.0
        if isinstance(expr, ExprBinOp):
            left = self._evaluate_expr(expr.left, bindings, source_file, line)
            right = self._evaluate_expr(expr.right, bindings, source_file, line)
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

    def _resolve_cmd(
        self,
        cmd: DrawingCmd,
        bindings: dict[str, Value],
        source_file: str,
        line: int,
    ) -> DrawingCmd:
        """Rewrite a drawing command: substitute function param expr nodes with LengthValues.

        For VarDeclStmt: returned unchanged (no params).
        For AssignStmt: expression partially resolved — param refs substituted, bbox
          accesses left as ExprBboxAccess for runtime evaluation by the dispatcher.
        For NamedDrawCmd: inner primitive's params are resolved against bindings.
        """
        if isinstance(cmd, VarDeclStmt):
            return cmd

        if isinstance(cmd, AssignStmt):
            resolved_val = self._partially_resolve_expr(cmd.value, bindings)
            if resolved_val is cmd.value:
                return cmd
            return AssignStmt(
                target=cmd.target,
                value=resolved_val,
                source_file=cmd.source_file,
                line=cmd.line,
            )

        if isinstance(cmd, NamedDrawCmd):
            resolved_inner = self._resolve_cmd(cmd.cmd, bindings, source_file, line)
            if resolved_inner is cmd.cmd:
                return cmd
            return NamedDrawCmd(
                binding_name=cmd.binding_name,
                cmd=resolved_inner,
                source_file=cmd.source_file,
                line=cmd.line,
            )

        if isinstance(cmd, DoWhileStmt):
            resolved_body = tuple(
                self._resolve_cmd(inner, bindings, source_file, line)
                for inner in cmd.body
            )
            resolved_condition = self._partially_resolve_comparison(cmd.condition, bindings)
            if resolved_body == cmd.body and resolved_condition is cmd.condition:
                return cmd
            return DoWhileStmt(
                body=resolved_body,
                condition=resolved_condition,
                source_file=cmd.source_file,
                line=cmd.line,
            )

        if isinstance(cmd, FuncCall):
            resolved_args = tuple(
                self._resolve_value(arg, bindings, source_file, line)
                for arg in cmd.args
            )
            if resolved_args == cmd.args:
                return cmd
            return FuncCall(
                name=cmd.name,
                args=resolved_args,
                source_file=cmd.source_file,
                line=cmd.line,
            )

        if not hasattr(cmd, "params"):
            return cmd
        new_params = {}
        for k, v in cmd.params.items():
            new_params[k] = self._resolve_value(v, bindings, source_file, line)
        return type(cmd)(params=new_params, source_file=cmd.source_file, line=cmd.line)

    def _partially_resolve_expr(
        self,
        expr: ExprNode,
        bindings: dict[str, Value],
    ) -> ExprNode:
        """Substitute function parameter references in expr; leave ExprBboxAccess intact."""
        if isinstance(expr, ExprFactor):
            if isinstance(expr.value, str) and expr.value in bindings:
                bound = bindings[expr.value]
                if isinstance(bound, LengthValue):
                    return ExprFactor(value=copy.deepcopy(bound))
            return expr
        if isinstance(expr, ExprBboxAccess):
            return expr  # resolved at runtime by the dispatcher
        if isinstance(expr, ExprBinOp):
            left = self._partially_resolve_expr(expr.left, bindings)
            right = self._partially_resolve_expr(expr.right, bindings)
            if left is expr.left and right is expr.right:
                return expr
            return ExprBinOp(left=left, op=expr.op, right=right)
        return expr

    def _partially_resolve_comparison(
        self,
        expr: ComparisonExpr,
        bindings: dict[str, Value],
    ) -> ComparisonExpr:
        left = self._partially_resolve_expr(expr.left, bindings)
        right = self._partially_resolve_expr(expr.right, bindings)
        if left is expr.left and right is expr.right:
            return expr
        return ComparisonExpr(
            left=left,
            op=expr.op,
            right=right,
            source_file=expr.source_file,
            line=expr.line,
        )

    def _resolve_value(
        self,
        val: Value,
        bindings: dict[str, Value],
        source_file: str,
        line: int,
    ) -> Value:
        """Substitute function parameters while preserving runtime-local expressions.

        Function arguments such as `start_x` and `y` are replaced eagerly, but
        function-local variables declared with `var` (for example loop counters)
        must remain as expression nodes so the PrimitiveDispatcher can evaluate
        them against the function's VariableStore at runtime.
        """
        if isinstance(val, ExprFactor):
            if isinstance(val.value, LengthValue):
                return val.value
            if isinstance(val.value, str) and val.value in bindings:
                return copy.deepcopy(bindings[val.value])
            return IdentValue(name=val.value) if isinstance(val.value, str) else val
        if isinstance(val, ExprBinOp):
            return self._partially_resolve_expr(val, bindings)
        if isinstance(val, ExprBboxAccess):
            # Cannot resolve at binding time; leave as-is for runtime resolution
            return val
        if isinstance(val, ExprPoint):
            x = self._partially_resolve_expr(val.x, bindings)
            y = self._partially_resolve_expr(val.y, bindings)
            if (isinstance(x, ExprFactor) and isinstance(x.value, LengthValue)
                    and isinstance(y, ExprFactor) and isinstance(y.value, LengthValue)):
                return PointValue(x=x.value, y=y.value)
            return ExprPoint(x=x, y=y)
        return val
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
