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
"""DSL Lexer — converts raw source text into a flat Token list.

Key disambiguation rules implemented here:
  1. '#' disambiguation: in a value position (immediately after '=' or '('),
     '#' followed by exactly 6 hex digits is a COLOR_HEX token.  In any other
     position '#' starts a single-line comment.
  2. 'image' disambiguation: handled at parse time (peek at next char); the
     lexer always emits KEYWORD for 'image'.
  3. NEWLINE tokens are only emitted while inside a frame/obj/func body
     (depth > 0) because top-level newlines between blocks carry no meaning.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from imagegen.token_type import TokenType

if TYPE_CHECKING:
    from imagegen.error_reporter import ErrorReporter


# ---------------------------------------------------------------------------
# DSL reserved keywords
# ---------------------------------------------------------------------------

_KEYWORDS: frozenset[str] = frozenset({
    "begin_frame", "end_frame",
    "begin_obj", "end_obj",
    "begin_func", "end_func",
    "begin_palette", "end_palette",
    "include",
    "image",
    "background",
    "grid",
    "line", "circle", "square", "polygon", "path",
    "pie", "arc", "connector", "font",
    "var",  # FEA-007: variable declaration
    "do", "while",  # FEA-008: bounded loop support
})

# Frame/obj/func attribute keywords (not primitives, but still keyword tokens)
_FRAME_ATTR_KEYWORDS: frozenset[str] = frozenset({
    "hold-time", "frame-mode", "colorspace",
    "width", "height", "dpi", "output-format",
    "one-run", "cyclic-run",
    "RGB", "RGBA", "GRAY",
    "png", "jpeg", "gif", "images",
    "solid", "dashed", "dotted", "dash-dot",
    "fit", "stretch", "clip",
    "start", "end", "center",
    "sharp", "rounded", "beveled",
    "straight", "curved", "step",
    "arrow", "filled-arrow", "diamond", "none",
    "true", "false",
    "border", "shadow", "clip-bounds", "clip-shape",
})

# Named colors — subset used for COLOR_NAMED token type (full CSS-3 set)
_NAMED_COLORS: frozenset[str] = frozenset({
    "black", "white", "red", "green", "blue",
    "cyan", "magenta", "yellow", "orange",
    "purple", "pink", "gray", "darkgray",
    "lightgray", "brown", "lime", "navy",
    "teal", "silver", "gold", "transparent",
    # Extended CSS Color Level 3 names (147 total — frequently used subset)
    "aqua", "aquamarine", "azure", "beige", "bisque", "blanchedalmond",
    "blueviolet", "burlywood", "cadetblue", "chartreuse", "chocolate",
    "coral", "cornflowerblue", "cornsilk", "crimson", "darkblue",
    "darkcyan", "darkgoldenrod", "darkgreen", "darkkhaki", "darkmagenta",
    "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon",
    "darkseagreen", "darkslateblue", "darkslategray", "darkturquoise",
    "darkviolet", "deeppink", "deepskyblue", "dimgray", "dodgerblue",
    "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
    "ghostwhite", "goldenrod", "greenyellow", "honeydew", "hotpink",
    "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush",
    "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan",
    "lightgoldenrodyellow", "lightgreen", "lightpink", "lightsalmon",
    "lightseagreen", "lightskyblue", "lightslategray", "lightsteelblue",
    "lightyellow", "limegreen", "linen", "maroon", "mediumaquamarine",
    "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen",
    "mediumslateblue", "mediumspringgreen", "mediumturquoise",
    "mediumvioletred", "midnightblue", "mintcream", "mistyrose",
    "moccasin", "navajowhite", "oldlace", "olive", "olivedrab",
    "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise",
    "palevioletred", "papayawhip", "peachpuff", "peru", "plum",
    "powderblue", "rosybrown", "royalblue", "saddlebrown", "salmon",
    "sandybrown", "seagreen", "seashell", "sienna", "skyblue",
    "slateblue", "slategray", "snow", "springgreen", "steelblue",
    "tan", "thistle", "tomato", "turquoise", "violet", "wheat",
    "whitesmoke", "yellowgreen",
})


# ---------------------------------------------------------------------------
# Token dataclass
# ---------------------------------------------------------------------------

@dataclass
class Token:
    type: TokenType
    value: str    # raw matched text (number includes unit suffix)
    file: str
    line: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.file}:{self.line})"


# ---------------------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------------------

# Master regex — groups are tried left-to-right; first match wins.
# Groups are named to aid debugging; only the group that matched is non-None.
#
# ORDER MATTERS:
#   1. Whitespace (skip, not emitted)
#   2. Comment (skip — must come before '#' color check)
#   3. String literal
#   4. Number with unit (must precede bare number)
#   5. Color hex — emitted only in value position (handled by _in_value_pos flag)
#   6. Named colors / boolean / identifier-like keywords
#   7. Operators and punctuation
#   8. Newline (conditionally emitted)
#   9. Catch-all for illegal characters

_TOKEN_RE = re.compile(
    r'(?P<WHITESPACE>[ \t]+)'
    r'|(?P<COMMENT>#(?![0-9A-Fa-f]{6}(?:[^0-9A-Fa-f]|$))[^\n]*)'  # # not followed by 6 hex = comment
    r'|(?P<STRING>"(?:[^"\\]|\\["\\nt])*")'
    r'|(?P<NUMBER>[0-9]+(?:\.[0-9]+)?(?:px|pt|em|cm|mm|%)?)'
    r'|(?P<COLOR_HEX>#[0-9A-Fa-f]{6})'
    r'|(?P<AT_SIGN>@)'
    r'|(?P<IDENT>[A-Za-z_][A-Za-z0-9_-]*)'
    r'|(?P<LPAREN>\()'
    r'|(?P<RPAREN>\))'
    r'|(?P<LBRACKET>\[)'
    r'|(?P<RBRACKET>\])'
    r'|(?P<EQEQ>==)'
    r'|(?P<NEQ>!=)'
    r'|(?P<LTE><=)'
    r'|(?P<GTE>>=)'
    r'|(?P<EQUALS>=)'
    r'|(?P<COLON>:)'
    r'|(?P<COMMA>,)'
    r'|(?P<SEMICOLON>;)'
    r'|(?P<LT><)'
    r'|(?P<GT>>)'
    r'|(?P<PLUS>\+)'
    r'|(?P<MINUS>-)'
    r'|(?P<STAR>\*)'
    r'|(?P<SLASH>/)'
    r'|(?P<DOT>\.)'
    r'|(?P<NEWLINE>\n)'
    r'|(?P<ILLEGAL>.)',
    re.MULTILINE,
)


class Lexer:
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter

    def tokenize(self, source: str, filename: str) -> list[Token]:
        """Tokenize DSL source into a flat Token list.

        Raises ParseError on any character that cannot be matched.
        NEWLINE tokens are only emitted inside body blocks (depth > 0).
        COLOR_HEX tokens are only valid when the previous non-whitespace
        token was EQUALS or LPAREN (value position).
        """
        tokens: list[Token] = []
        line = 1
        # depth tracks nesting: begin_frame/obj/func increments, end_* decrements.
        # Newlines are only meaningful (i.e. emitted) when depth > 0.
        depth = 0
        # paren_depth tracks open parentheses.  Newlines inside (...) are NOT
        # statement terminators — they are line continuations within argument lists.
        paren_depth = 0
        # Tracks whether the last substantive token was EQUALS or LPAREN so
        # that '#RRGGBB' can be recognised as COLOR_HEX rather than a comment.
        in_value_pos = False
        # Tracks whether an object attribute value has started after ':'
        # so hex colors remain valid later in the same value sequence.
        in_colon_value = False

        for m in _TOKEN_RE.finditer(source):
            kind = m.lastgroup
            text = m.group()

            if kind == "WHITESPACE":
                continue

            if kind == "NEWLINE":
                line += 1
                # Only emit NEWLINE inside a body AND outside parentheses.
                # NEWLINEs inside (...) are line continuations, not terminators.
                if depth > 0 and paren_depth == 0:
                    if tokens and tokens[-1].type not in (TokenType.NEWLINE, TokenType.SEMICOLON):
                        tokens.append(Token(TokenType.NEWLINE, "\n", filename, line - 1))
                in_value_pos = False
                in_colon_value = False
                continue

            if kind == "COMMENT":
                in_value_pos = False
                in_colon_value = False
                continue

            if kind == "AT_SIGN":
                tokens.append(Token(TokenType.AT_SIGN, text, filename, line))
                in_value_pos = False
                continue

            if kind == "ILLEGAL":
                self._reporter.parse_error(filename, line, f"unexpected character: {text!r}")

            if kind == "STRING":
                # Strip surrounding quotes and unescape sequences
                inner = text[1:-1]
                inner = inner.replace("\\n", "\n").replace("\\t", "\t")
                inner = inner.replace('\\"', '"').replace("\\\\", "\\")
                tokens.append(Token(TokenType.STRING, inner, filename, line))
                in_value_pos = False
                continue

            if kind == "NUMBER":
                tokens.append(Token(TokenType.NUMBER, text, filename, line))
                in_value_pos = False
                continue

            if kind == "COLOR_HEX":
                if in_value_pos or in_colon_value:
                    tokens.append(Token(TokenType.COLOR_HEX, text, filename, line))
                else:
                    # '#' not in value position — treat the whole match as a comment
                    # (the comment regex should have caught it, but guard here too)
                    in_value_pos = False
                continue

            if kind == "IDENT":
                tok_type, tok_text = self._classify_ident(text)
                tokens.append(Token(tok_type, tok_text, filename, line))
                # Track depth for NEWLINE suppression
                if tok_text in ("begin_frame", "begin_obj", "begin_func", "begin_palette"):
                    depth += 1
                elif tok_text in ("end_frame", "end_obj", "end_func", "end_palette"):
                    depth = max(0, depth - 1)
                in_value_pos = False
                continue

            # Punctuation / operators (AT_SIGN is handled above)
            punc_map = {
                "LPAREN":   TokenType.LPAREN,
                "RPAREN":   TokenType.RPAREN,
                "LBRACKET": TokenType.LBRACKET,
                "RBRACKET": TokenType.RBRACKET,
                "EQUALS":   TokenType.EQUALS,
                "COLON":    TokenType.COLON,
                "COMMA":    TokenType.COMMA,
                "SEMICOLON": TokenType.SEMICOLON,
                "EQEQ":     TokenType.EQEQ,
                "NEQ":      TokenType.NEQ,
                "LT":       TokenType.LT,
                "LTE":      TokenType.LTE,
                "GT":       TokenType.GT,
                "GTE":      TokenType.GTE,
                "PLUS":     TokenType.PLUS,
                "MINUS":    TokenType.MINUS,
                "STAR":     TokenType.STAR,
                "SLASH":    TokenType.SLASH,
                "DOT":      TokenType.DOT,
            }
            tt = punc_map[kind]
            tokens.append(Token(tt, text, filename, line))
            # Track parenthesis depth to suppress NEWLINE inside argument lists
            if tt == TokenType.LPAREN:
                paren_depth += 1
            elif tt == TokenType.RPAREN:
                paren_depth = max(0, paren_depth - 1)
            # EQUALS, LPAREN, and COLON open a value position for the next token
            in_value_pos = tt in (TokenType.EQUALS, TokenType.LPAREN, TokenType.COLON)
            if tt == TokenType.COLON:
                in_colon_value = True
            # SEMICOLON acts like a statement terminator inside bodies
            if tt == TokenType.SEMICOLON and depth > 0:
                in_colon_value = False
                # Normalise: keep SEMICOLON as-is (parser accepts both)
                pass

        tokens.append(Token(TokenType.EOF, "", filename, line))
        return tokens

    @staticmethod
    def _classify_ident(text: str) -> tuple[TokenType, str]:
        """Classify an identifier token as KEYWORD, COLOR_NAMED, or IDENTIFIER."""
        if text in _KEYWORDS:
            return TokenType.KEYWORD, text
        if text in _FRAME_ATTR_KEYWORDS:
            # Frame/canvas attribute values are emitted as KEYWORD so the parser
            # can match them directly without extra identifier look-ups.
            return TokenType.KEYWORD, text
        if text in _NAMED_COLORS:
            return TokenType.COLOR_NAMED, text
        return TokenType.IDENTIFIER, text
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
