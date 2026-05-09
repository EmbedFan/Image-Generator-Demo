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
"""Technical Image Generator — CLI entry point.

Usage:
  python imagegen.py <input.dsl> [output-path]
  python imagegen.py --list-fonts

Exit codes:
  0  Success — all output files written, or --list-fonts completed
  1  Parse error, validation error, or usage error
  2  Runtime error (division by zero, recursion)
  3  I/O error (input file not found, asset unreadable, output not writable)
"""

import argparse
import pathlib
import sys

from imagegen.orchestrator import Engine
from imagegen.error_reporter import ParseError, ValidationError, DslRuntimeError, DslIOError


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="imagegen",
        description="Generate PNG, JPEG, or animated GIF images from a DSL script.",
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default=None,
        help="Path to the .dsl script file",
    )
    parser.add_argument(
        "output_path",
        nargs="?",
        default=None,
        help="Optional output file or directory (overrides default next to input file)",
    )
    parser.add_argument(
        "--list-fonts",
        action="store_true",
        help="List all available system fonts and exit",
    )
    args = parser.parse_args()

    if args.list_fonts:
        if args.input_file:
            print(
                "imagegen: error: --list-fonts cannot be used together with an input file",
                file=sys.stderr,
            )
            sys.exit(1)
        from imagegen.font_discovery import list_fonts
        list_fonts()
        sys.exit(0)

    if not args.input_file:
        parser.print_usage(sys.stderr)
        print("imagegen: error: the following arguments are required: input_file", file=sys.stderr)
        sys.exit(1)

    dsl_path = pathlib.Path(args.input_file)
    if not dsl_path.exists():
        print(f"imagegen: error: input file not found: '{dsl_path}'", file=sys.stderr)
        sys.exit(3)

    output_path = pathlib.Path(args.output_path) if args.output_path else None

    engine = Engine()
    try:
        engine.run(dsl_path, output_path)
    except (ParseError, ValidationError):
        sys.exit(1)
    except DslRuntimeError:
        sys.exit(2)
    except DslIOError:
        sys.exit(3)

    sys.exit(0)


if __name__ == "__main__":
    main()
