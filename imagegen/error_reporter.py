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
"""Centralised error/warning formatting and halting for the DSL engine.

All *_error methods raise immediately — callers need not check return values.
"""

import sys


class ParseError(Exception):
    """Raised on malformed syntax, unknown keywords, duplicate parameters. Exit code 1."""


class ValidationError(Exception):
    """Raised on type/constraint violations (negative radius, JPEG+RGBA, etc.). Exit code 1."""


class DslRuntimeError(Exception):
    """Raised on runtime faults: division by zero, recursion. Exit code 2."""


class DslIOError(Exception):
    """Raised when input/include files are unreadable or output cannot be written. Exit code 3."""


class ErrorReporter:
    """Format and emit DSL error/warning messages to stderr.

    All *_error methods print the message then raise immediately.
    The warning() method prints but continues execution.
    """

    def error(self, file: str, line: int, primitive: str, message: str) -> None:
        """Print a generic error message without raising."""
        print(f"{file}:{line}: error: {primitive}: {message}", file=sys.stderr)

    def warning(self, file: str, line: int, message: str) -> None:
        """Print a warning; execution continues."""
        print(f"{file}:{line}: warning: {message}", file=sys.stderr)

    def parse_error(self, file: str, line: int, message: str) -> None:
        """Print and raise ParseError — halts execution immediately."""
        print(f"{file}:{line}: error: {message}", file=sys.stderr)
        raise ParseError(f"{file}:{line}: {message}")

    def validation_error(self, file: str, line: int, message: str) -> None:
        """Print and raise ValidationError — halts execution immediately."""
        print(f"{file}:{line}: error: {message}", file=sys.stderr)
        raise ValidationError(f"{file}:{line}: {message}")

    def runtime_error(self, file: str, line: int, message: str) -> None:
        """Print and raise DslRuntimeError — halts execution immediately."""
        print(f"{file}:{line}: error: {message}", file=sys.stderr)
        raise DslRuntimeError(f"{file}:{line}: {message}")

    def io_error(self, file: str, line: int, message: str) -> None:
        """Print and raise DslIOError — halts execution immediately."""
        print(f"{file}:{line}: error: {message}", file=sys.stderr)
        raise DslIOError(f"{file}:{line}: {message}")
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
