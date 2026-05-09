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
"""Engine Orchestrator (REQ-0001, REQ-0028) — two-pass pipeline coordinator.

Full pipeline executed by Engine.run():
  1. Read DSL source  (DslIOError if unreadable)
  2. Lex → parse → Script AST
  3. Pass 1: Resolver → SymbolTable + ordered frame list
  4. SemanticValidator validates every frame
  5. FrameRunner executes every frame → PIL Images
  6. OutputFormatter writes output file(s)
"""

from __future__ import annotations

import pathlib

from imagegen.error_reporter import ErrorReporter
from imagegen.lexer import Lexer
from imagegen.parser import Parser
from imagegen.resolver import Resolver
from imagegen.semantic_validator import SemanticValidator
from imagegen.frame_runner import FrameRunner
from imagegen.output.output_formatter import OutputFormatter


class Engine:
    def __init__(self) -> None:
        """Construct all sub-components sharing a single ErrorReporter."""
        self._reporter = ErrorReporter()

    def run(
        self,
        dsl_path: pathlib.Path,
        output_path: pathlib.Path | None,
    ) -> None:
        """Execute the full two-pass pipeline from a DSL file path."""
        reporter = self._reporter
        base_dir = dsl_path.parent
        script_stem = dsl_path.stem

        # 1. Read source
        try:
            source = dsl_path.read_text(encoding="utf-8").lstrip('﻿')
        except UnicodeDecodeError as exc:
            reporter.io_error(str(dsl_path), 0,
                f"file is not valid UTF-8 (byte position ~{exc.start}); "
                f"save the file as UTF-8 and retry")
        except OSError as exc:
            reporter.io_error(str(dsl_path), 0,
                f"cannot read input file: {exc}")

        # 2. Lex → parse
        lexer = Lexer(reporter)
        tokens = lexer.tokenize(source, str(dsl_path))
        parser = Parser(reporter)
        script = parser.parse(tokens)

        # 3. Pass 1: include resolution + symbol collection
        resolver = Resolver(reporter)
        symbol_table, frames = resolver.resolve(script, base_dir)

        if not frames:
            reporter.warning(str(dsl_path), 0, "no frames found; no output produced")
            return

        # 4. Semantic validation
        validator = SemanticValidator(reporter)
        for frame in frames:
            validator.validate_frame(frame, symbol_table)

        # 5. Pass 2: frame rendering
        runner = FrameRunner(symbol_table, reporter, base_dir)
        rendered_frames = runner.run_frames(frames)

        # 6. Output
        formatter = OutputFormatter(reporter)
        formatter.write(
            frames=rendered_frames,
            script_stem=script_stem,
            output_path=output_path,
            base_dir=base_dir,
        )
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
