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
"""Symbol table for the DSL engine.

The namespace is flat and shared across frames, objects, and functions.
Any duplicate name — regardless of kind — is a parse error.
Palette aliases share their own flat namespace (palettes dict).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imagegen.ast_nodes import ObjTemplate, FuncDecl, PaletteDef, ColorValue, ColorNone
    from imagegen.error_reporter import ErrorReporter


@dataclass
class SymbolTable:
    """Holds all object template, function, and palette definitions collected in Pass 1.

    The object/function/frame namespace is intentionally flat: registering a name
    that is already present raises a parse error immediately.
    Palette aliases share a separate flat namespace (palettes dict); alias names
    must be unique across all palettes from all loaded files.
    """

    objects: dict[str, ObjTemplate] = field(default_factory=dict)
    functions: dict[str, FuncDecl] = field(default_factory=dict)
    palettes: dict[str, ColorValue | ColorNone] = field(default_factory=dict)

    # Frame names are tracked only for collision detection — frames are not
    # looked up from here; the resolver returns them as an ordered list.
    _frame_names: set[str] = field(default_factory=set, repr=False)

    def register_frame_name(self, name: str, reporter: ErrorReporter, source_file: str, line: int) -> None:
        """Record a frame name for global namespace collision detection."""
        self._check_collision(name, reporter, source_file, line)
        self._frame_names.add(name)

    def register_object(self, template: ObjTemplate, reporter: ErrorReporter) -> None:
        """Register an object template; raise ParseError on duplicate name."""
        self._check_collision(template.name, reporter, template.source_file, template.line)
        self.objects[template.name] = template

    def register_function(self, decl: FuncDecl, reporter: ErrorReporter) -> None:
        """Register a function declaration; raise ParseError on duplicate name."""
        self._check_collision(decl.name, reporter, decl.source_file, decl.line)
        self.functions[decl.name] = decl

    def register_palette(self, palette_def: PaletteDef, reporter: ErrorReporter) -> None:
        """Merge all color aliases from a PaletteDef into the global palette namespace.

        Raises ParseError if any alias is already defined (REQ-0040.1, REQ-0040.4).
        """
        for alias, color in palette_def.entries.items():
            if alias in self.palettes:
                reporter.parse_error(
                    palette_def.source_file, palette_def.line,
                    f"duplicate palette alias '{alias}' "
                    f"(already defined in a previously loaded palette)"
                )
            self.palettes[alias] = color

    def lookup_object(self, name: str) -> ObjTemplate | None:
        return self.objects.get(name)

    def lookup_function(self, name: str) -> FuncDecl | None:
        return self.functions.get(name)

    def lookup_palette_alias(self, alias: str) -> ColorValue | ColorNone | None:
        return self.palettes.get(alias)

    def _check_collision(self, name: str, reporter: ErrorReporter, source_file: str, line: int) -> None:
        if (
            name in self.objects
            or name in self.functions
            or name in self._frame_names
        ):
            reporter.parse_error(source_file, line, f"'{name}' is already defined")
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
