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
"""Variable store for DSL frame/function scopes (FEA-007).

Holds numeric variable values and named-object bounding boxes for a single
frame or function execution.  A fresh VariableStore is created for each frame;
function calls create their own separate store.

Bounding boxes are stored as (x, y, width, height) in DSL pixel coordinates.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imagegen.error_reporter import ErrorReporter


class VariableStore:
    def __init__(self) -> None:
        # Declared variables: name → float value (None = declared but not yet assigned)
        self._vars: dict[str, float | None] = {}
        # Named objects: binding_name → (x, y, width, height) in DSL px
        self._objects: dict[str, tuple[float, float, float, float]] = {}

    # ------------------------------------------------------------------
    # Variable operations
    # ------------------------------------------------------------------

    def declare(self, name: str) -> None:
        """Declare a variable (sets to None if not already declared)."""
        if name not in self._vars:
            self._vars[name] = None

    def assign(
        self,
        name: str,
        value: float,
        source_file: str,
        line: int,
        reporter: ErrorReporter,
    ) -> None:
        """Assign a value to a declared variable; raises DslRuntimeError if undeclared."""
        if name not in self._vars:
            reporter.runtime_error(
                source_file, line,
                f"assignment to undeclared variable '{name}'; declare with 'var {name};' first"
            )
        self._vars[name] = value

    def get(self, name: str) -> float | None:
        """Return the variable's value, or None if undeclared or unassigned."""
        return self._vars.get(name)

    def has_var(self, name: str) -> bool:
        return name in self._vars

    # ------------------------------------------------------------------
    # Named object / bbox operations
    # ------------------------------------------------------------------

    def register_object(
        self,
        name: str,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        """Register a rendered object's bounding box under binding_name."""
        self._objects[name] = (x, y, width, height)

    def get_bbox(
        self,
        name: str,
        source_file: str,
        line: int,
        reporter: ErrorReporter,
    ) -> tuple[float, float, float, float]:
        """Return (x, y, width, height) for a named object; runtime error if unknown."""
        bbox = self._objects.get(name)
        if bbox is None:
            reporter.runtime_error(
                source_file, line,
                f"bbox access on '{name}': object has not been rendered yet "
                f"(use 'name = primitive(...)' before accessing .bbox)"
            )
        return bbox

    def has_object(self, name: str) -> bool:
        return name in self._objects
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
