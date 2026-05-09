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
"""Pass 1 Resolver — include resolution, circular detection, symbol collection,
and palette reference resolution (FEA-006).

Frames inside included files are silently ignored; only the root script's
frames are returned.  All begin_obj / begin_func / begin_palette definitions
from every included file are merged into the single flat SymbolTable.

After all symbols are collected, _resolve_palette_refs() walks every frame
body, object template body, and function body, replacing PaletteRef values
with their concrete ColorValue / ColorNone.  Any unresolved alias is a parse
error at this point.
"""

from __future__ import annotations

import pathlib
from dataclasses import replace
from typing import TYPE_CHECKING

from imagegen.ast_nodes import (
    Script, FrameDef, ObjTemplate, FuncDecl, IncludeStmt, PaletteDef,
    TopLevelStmt, DrawingCmd,
    ObjAttr, FuncCall,
    PaletteRef, ColorValue, ColorNone, Value,
)
from imagegen.symbol_table import SymbolTable

if TYPE_CHECKING:
    from imagegen.error_reporter import ErrorReporter


class Resolver:
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    def resolve(
        self,
        script: Script,
        base_dir: pathlib.Path,
    ) -> tuple[SymbolTable, list[FrameDef]]:
        """Pass 1 entry point.

        Returns (symbol_table, frames) where:
          - symbol_table contains all object/function definitions from the
            root script and all recursively included files.
          - frames is the ordered list of FrameDef nodes from the root
            script only — frames inside included files are ignored per REQ-0016.
        """
        symbol_table = SymbolTable()
        frames: list[FrameDef] = []

        self._collect_symbols(
            script=script,
            symbol_table=symbol_table,
            frames=frames,
            base_dir=base_dir,
            include_stack=[],
            is_root=True,
        )

        # Resolve all @alias PaletteRef values now that every palette is known.
        resolved_frames = self._resolve_palette_refs(frames, symbol_table)

        return symbol_table, resolved_frames

    # ------------------------------------------------------------------

    def _collect_symbols(
        self,
        script: Script,
        symbol_table: SymbolTable,
        frames: list[FrameDef],
        base_dir: pathlib.Path,
        include_stack: list[pathlib.Path],
        is_root: bool,
    ) -> None:
        """Walk top-level statements; register obj/func/palette; recurse into includes."""
        for stmt in script.statements:
            if isinstance(stmt, FrameDef):
                if is_root:
                    # Record frame name in symbol table for collision detection
                    symbol_table.register_frame_name(
                        stmt.name, self._reporter, stmt.source_file, stmt.line
                    )
                    frames.append(stmt)
                # Frames in included files are silently ignored (REQ-0016)

            elif isinstance(stmt, ObjTemplate):
                symbol_table.register_object(stmt, self._reporter)

            elif isinstance(stmt, FuncDecl):
                symbol_table.register_function(stmt, self._reporter)

            elif isinstance(stmt, PaletteDef):
                symbol_table.register_palette(stmt, self._reporter)

            elif isinstance(stmt, IncludeStmt):
                self._process_include(
                    stmt=stmt,
                    symbol_table=symbol_table,
                    base_dir=base_dir,
                    include_stack=include_stack,
                )

    def _process_include(
        self,
        stmt: IncludeStmt,
        symbol_table: SymbolTable,
        base_dir: pathlib.Path,
        include_stack: list[pathlib.Path],
    ) -> None:
        # Paths are resolved relative to the including file's directory (REQ-0016.1)
        raw_path = pathlib.Path(stmt.path)
        if not raw_path.is_absolute():
            resolved = (base_dir / raw_path).resolve()
        else:
            resolved = raw_path.resolve()

        # Circular include detection (REQ-0016.2): check the current resolution chain
        if resolved in include_stack:
            self._reporter.parse_error(
                stmt.source_file, stmt.line,
                f"circular include detected: '{resolved}'"
            )

        if not resolved.exists():
            self._reporter.io_error(
                stmt.source_file, stmt.line,
                f"include file not found: '{resolved}'"
            )

        included_script = self._load_file(resolved, include_stack)

        new_stack = include_stack + [resolved]
        self._collect_symbols(
            script=included_script,
            symbol_table=symbol_table,
            frames=[],          # frames from included files are discarded
            base_dir=resolved.parent,
            include_stack=new_stack,
            is_root=False,
        )

    # ------------------------------------------------------------------
    # Palette reference resolution  (FEA-006, REQ-0040.2, REQ-0040.5)
    # ------------------------------------------------------------------

    def _resolve_palette_refs(
        self,
        frames: list[FrameDef],
        symbol_table: SymbolTable,
    ) -> list[FrameDef]:
        """Replace every PaletteRef in frames, obj templates, and func bodies
        with its resolved ColorValue / ColorNone.  Undefined aliases are a
        parse error.  Runs after all PaletteDef entries have been collected.
        """
        if not symbol_table.palettes:
            return frames  # fast path: no palettes defined anywhere

        resolved_frames = [self._resolve_frame(f, symbol_table) for f in frames]

        # Also resolve palette refs inside object template bodies and attributes
        for name, tmpl in list(symbol_table.objects.items()):
            symbol_table.objects[name] = self._resolve_obj_template(tmpl, symbol_table)

        # Also resolve inside function declaration bodies
        for name, decl in list(symbol_table.functions.items()):
            symbol_table.functions[name] = self._resolve_func_decl(decl, symbol_table)

        return resolved_frames

    def _resolve_frame(self, frame: FrameDef, symbol_table: SymbolTable) -> FrameDef:
        new_body = tuple(self._resolve_cmd(cmd, symbol_table) for cmd in frame.body)
        return replace(frame, body=new_body)

    def _resolve_obj_template(self, tmpl: ObjTemplate, symbol_table: SymbolTable) -> ObjTemplate:
        new_attrs = tuple(
            replace(attr, value=self._resolve_value(attr.value, symbol_table))
            for attr in tmpl.attributes
        )
        new_body = tuple(self._resolve_cmd(cmd, symbol_table) for cmd in tmpl.body)
        return replace(tmpl, attributes=new_attrs, body=new_body)

    def _resolve_func_decl(self, decl: FuncDecl, symbol_table: SymbolTable) -> FuncDecl:
        new_body = tuple(self._resolve_cmd(cmd, symbol_table) for cmd in decl.body)
        return replace(decl, body=new_body)

    def _resolve_cmd(self, cmd: DrawingCmd, symbol_table: SymbolTable) -> DrawingCmd:
        """Resolve PaletteRef values in a drawing command's params or args."""
        if isinstance(cmd, FuncCall):
            new_args = tuple(self._resolve_value(v, symbol_table) for v in cmd.args)
            return replace(cmd, args=new_args)

        params = getattr(cmd, 'params', None)
        if isinstance(params, dict):
            for key, val in list(params.items()):
                if isinstance(val, PaletteRef):
                    params[key] = self._resolve_value(val, symbol_table)
        return cmd

    def _resolve_value(self, val: Value, symbol_table: SymbolTable) -> Value:
        """Return the resolved value; replace PaletteRef with its target color."""
        if not isinstance(val, PaletteRef):
            return val
        resolved = symbol_table.lookup_palette_alias(val.alias)
        if resolved is None:
            self._reporter.parse_error(
                val.source_file, val.line,
                f"undefined palette alias '@{val.alias}'"
            )
        return resolved

    # ------------------------------------------------------------------

    def _load_file(
        self,
        path: pathlib.Path,
        include_stack: list[pathlib.Path],
    ) -> Script:
        """Read, lex, and parse one DSL file.

        Path resolution is relative to the including file's directory (REQ-0016.1).
        Raises DslIOError if the file cannot be read.
        """
        # Import here to avoid circular imports at module load time
        from imagegen.lexer import Lexer
        from imagegen.parser import Parser

        try:
            source = path.read_text(encoding="utf-8").lstrip('﻿')
        except UnicodeDecodeError as exc:
            self._reporter.io_error(
                str(path), 0,
                f"'{path}' is not valid UTF-8 (byte position ~{exc.start}); "
                f"save the file as UTF-8 and retry"
            )
        except OSError as exc:
            self._reporter.io_error(
                str(path), 0,
                f"cannot read file '{path}': {exc}"
            )

        lexer = Lexer(self._reporter)
        tokens = lexer.tokenize(source, str(path))
        parser = Parser(self._reporter)
        return parser.parse(tokens)
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
