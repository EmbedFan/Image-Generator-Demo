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
"""Token type enumeration for the DSL lexer."""

from enum import Enum, auto


class TokenType(Enum):
    KEYWORD     = auto()  # begin_frame, end_frame, begin_obj, end_obj, begin_func, end_func, include, image, background, line, circle, square, polygon, path, pie, arc, connector, font
    IDENTIFIER  = auto()  # user-defined frame/object/function names and parameter names
    NUMBER      = auto()  # numeric literal with optional unit suffix (px, pt, em, cm, mm, %)
    STRING      = auto()  # double-quoted string literal
    COLOR_HEX   = auto()  # #RRGGBB six-digit hex color (only valid in value position after = or ()
    COLOR_NAMED = auto()  # named color token: black, white, red, green, blue, none, transparent, etc.
    LPAREN      = auto()  # (
    RPAREN      = auto()  # )
    LBRACKET    = auto()  # [ — opens a point-list
    RBRACKET    = auto()  # ] — closes a point-list
    EQUALS      = auto()  # = — named parameter assignment
    COLON       = auto()  # : — object attribute assignment (obj-attr syntax)
    COMMA       = auto()  # ,
    SEMICOLON   = auto()  # ; — statement terminator (alternative to newline)
    NEWLINE     = auto()  # \n — statement terminator inside frame/obj/func bodies
    AT_SIGN     = auto()  # @ — palette alias reference prefix (e.g. @primary)
    PLUS        = auto()  # + — arithmetic in function/frame bodies
    MINUS       = auto()  # - — arithmetic in function/frame bodies (whitespace-surrounded)
    STAR        = auto()  # * — arithmetic in function/frame bodies
    SLASH       = auto()  # / — arithmetic in function/frame bodies
    EQEQ        = auto()  # == — comparison in do ... while conditions
    NEQ         = auto()  # != — comparison in do ... while conditions
    LT          = auto()  # < — comparison in do ... while conditions
    LTE         = auto()  # <= — comparison in do ... while conditions
    GT          = auto()  # > — comparison in do ... while conditions
    GTE         = auto()  # >= — comparison in do ... while conditions
    DOT         = auto()  # . — property access (e.g. rect1.bbox.x)
    EOF         = auto()  # end of token stream
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
