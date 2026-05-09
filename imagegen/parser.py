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
"""Recursive-descent parser for the Technical Image Generator DSL.

Disambiguation rules:
  1. 'image' keyword: if the next token is LPAREN → ImagePrimNode (drawing primitive);
     otherwise → ImageDef (canvas statement).
  2. '#RRGGBB': handled by the Lexer in value-position context; the parser
     receives COLOR_HEX tokens only when syntactically valid.
  3. Arithmetic expressions (<expr>) are only allowed in value positions inside
     begin_func bodies (in_func_body=True).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from imagegen.token_type import TokenType
from imagegen.ast_nodes import (
    Script, FrameDef, ObjTemplate, FuncDecl, IncludeStmt, PaletteDef,
    ImageDef, Background, GridNode,
    LineNode, CircleNode, SquareNode, PolygonNode, PathNode,
    PieNode, ArcNode, ConnectorNode, FontNode, ImagePrimNode,
    ObjectInst, FuncCall,
    VarDeclStmt, AssignStmt, NamedDrawCmd, DoWhileStmt,
    ObjAttr,
    LengthValue, ColorValue, ColorNone, PaletteRef, PointValue, PointList, ShadowValue,
    BoolValue, StringValue, IdentValue,
    ExprFactor, ExprBinOp, ExprBboxAccess, ExprPoint, ComparisonExpr,
    TopLevelStmt, DrawingCmd, Value, ExprNode,
)

if TYPE_CHECKING:
    from imagegen.lexer import Token
    from imagegen.error_reporter import ErrorReporter

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PRIMITIVE_KEYWORDS = frozenset({
    "line", "circle", "square", "polygon", "path",
    "pie", "arc", "connector", "font",
})

_NAMED_COLORS_SET = frozenset({
    "black", "white", "red", "green", "blue", "cyan", "magenta",
    "yellow", "orange", "purple", "pink", "gray", "darkgray",
    "lightgray", "brown", "lime", "navy", "teal", "silver", "gold",
    "transparent", "aqua", "aquamarine", "azure", "beige", "bisque",
    "blanchedalmond", "blueviolet", "burlywood", "cadetblue", "chartreuse",
    "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson",
    "darkblue", "darkcyan", "darkgoldenrod", "darkgreen", "darkkhaki",
    "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred",
    "darksalmon", "darkseagreen", "darkslateblue", "darkslategray",
    "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray",
    "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia",
    "gainsboro", "ghostwhite", "goldenrod", "greenyellow", "honeydew",
    "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender",
    "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral",
    "lightcyan", "lightgoldenrodyellow", "lightgreen", "lightpink",
    "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray",
    "lightsteelblue", "lightyellow", "limegreen", "linen", "maroon",
    "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple",
    "mediumseagreen", "mediumslateblue", "mediumspringgreen",
    "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream",
    "mistyrose", "moccasin", "navajowhite", "none", "oldlace", "olive",
    "olivedrab", "orangered", "orchid", "palegoldenrod", "palegreen",
    "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru",
    "plum", "powderblue", "rosybrown", "royalblue", "saddlebrown",
    "salmon", "sandybrown", "seagreen", "seashell", "sienna", "skyblue",
    "slateblue", "slategray", "snow", "springgreen", "steelblue", "tan",
    "thistle", "tomato", "turquoise", "violet", "wheat", "whitesmoke",
    "yellowgreen",
})

_BOOLEAN_VALUES = frozenset({"true", "false"})

# Object template attribute keys (colon syntax)
_OBJ_ATTR_KEYS = frozenset({
    "width", "height", "background", "border", "shadow",
    "clip-bounds", "clip-shape",
})


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class Parser:
    def __init__(self, reporter: ErrorReporter) -> None:
        self._reporter = reporter
        self._tokens: list[Token] = []
        self._pos = 0
        self._filename = ""

    def parse(self, tokens: list[Token]) -> Script:
        """Entry point. Returns Script AST or raises ParseError.

        Disambiguation:
          - 'image' followed by LPAREN → image drawing primitive
          - 'image' not followed by LPAREN → canvas statement (ImageDef)
          - '#RRGGBB' is only emitted by the Lexer in value positions.
        """
        self._tokens = tokens
        self._pos = 0
        self._filename = tokens[0].file if tokens else ""

        statements: list[TopLevelStmt] = []
        self._skip_terminators()
        while self._peek().type != TokenType.EOF:
            statements.append(self._parse_top_level())
            self._skip_terminators()

        return Script(statements=tuple(statements))

    # ------------------------------------------------------------------
    # Top-level dispatch
    # ------------------------------------------------------------------

    def _parse_top_level(self) -> TopLevelStmt:
        tok = self._peek()
        if tok.type != TokenType.KEYWORD:
            self._reporter.parse_error(tok.file, tok.line,
                f"expected top-level statement, got {tok.value!r}")
        kw = tok.value
        if kw == "begin_frame":
            return self._parse_frame()
        if kw == "begin_obj":
            return self._parse_obj_template()
        if kw == "begin_func":
            return self._parse_func_decl()
        if kw == "include":
            return self._parse_include()
        if kw == "begin_palette":
            return self._parse_palette_def()
        if kw == "do":
            self._reporter.parse_error(
                tok.file, tok.line,
                "do-while loop is only permitted inside begin_frame / begin_func bodies"
            )
        self._reporter.parse_error(tok.file, tok.line,
            f"unexpected keyword {kw!r} at top level")

    # ------------------------------------------------------------------
    # Frame
    # ------------------------------------------------------------------

    def _parse_frame(self) -> FrameDef:
        start = self._consume(TokenType.KEYWORD)  # begin_frame
        name_tok = self._consume(TokenType.IDENTIFIER)
        self._skip_terminators()

        hold_time = 100.0
        frame_mode = "one-run"
        colorspace_attr = ""
        image_def: ImageDef | None = None

        # Frame attributes and image statement may be interleaved before body
        while True:
            tok = self._peek()
            if tok.type == TokenType.KEYWORD and tok.value == "image":
                # 'image' without LPAREN → canvas statement
                if self._peek_ahead(1).type != TokenType.LPAREN:
                    image_def = self._parse_image_def()
                    self._skip_terminators()
                    break
                else:
                    # image( → already a drawing primitive; end of attributes
                    break
            if tok.type == TokenType.KEYWORD and tok.value == "hold-time":
                self._consume()
                self._consume(TokenType.EQUALS)
                num_tok = self._consume(TokenType.NUMBER)
                hold_time = float(num_tok.value.rstrip("px pt em cm mm %".split()[0]))
                self._skip_terminators()
                continue
            if tok.type == TokenType.KEYWORD and tok.value == "frame-mode":
                self._consume()
                self._consume(TokenType.EQUALS)
                mode_tok = self._consume(TokenType.KEYWORD)
                frame_mode = mode_tok.value
                self._skip_terminators()
                continue
            if tok.type == TokenType.KEYWORD and tok.value == "colorspace":
                self._consume()
                self._consume(TokenType.EQUALS)
                cs_tok = self._consume(TokenType.KEYWORD)
                colorspace_attr = cs_tok.value
                self._skip_terminators()
                continue
            break

        if image_def is None:
            self._reporter.parse_error(start.file, start.line,
                f"frame '{name_tok.value}': missing 'image' canvas statement")

        body = self._parse_drawing_commands(
            "end_frame",
            in_func_body=True,
            allow_var_stmts=True,
            allow_loop_stmts=True,
        )
        self._consume(TokenType.KEYWORD)  # end_frame

        return FrameDef(
            name=name_tok.value,
            hold_time=hold_time,
            frame_mode=frame_mode,
            colorspace_attr=colorspace_attr,
            image_def=image_def,
            body=tuple(body),
            source_file=start.file,
            line=start.line,
        )

    # ------------------------------------------------------------------
    # Image canvas statement
    # ------------------------------------------------------------------

    def _parse_image_def(self) -> ImageDef:
        tok = self._consume(TokenType.KEYWORD)  # 'image'
        params: dict[str, str] = {}

        while True:
            pt = self._peek()
            if pt.type in (TokenType.NEWLINE, TokenType.SEMICOLON):
                self._consume()
                # Multi-line image statement: continue if next line is still an image param
                if self._peek().type == TokenType.KEYWORD and self._peek().value in (
                    "width", "height", "colorspace", "dpi", "output-format"
                ):
                    continue
                break
            if pt.type == TokenType.KEYWORD and pt.value in (
                "width", "height", "colorspace", "dpi", "output-format"
            ):
                key_tok = self._consume()
                self._consume(TokenType.EQUALS)
                val_tok = self._consume()
                params[key_tok.value] = val_tok.value
            else:
                break

        # Apply defaults
        width = self._parse_length_str(params.get("width", "800px"), tok)
        height = self._parse_length_str(params.get("height", "600px"), tok)
        colorspace = params.get("colorspace", "RGB")
        dpi = float(params.get("dpi", "96"))
        output_format = params.get("output-format", "png")

        return ImageDef(
            width=width, height=height,
            colorspace=colorspace, dpi=dpi,
            output_format=output_format,
            source_file=tok.file, line=tok.line,
        )

    def _parse_length_str(self, s: str, ref_tok: Token) -> LengthValue:
        """Parse a length string like '800px' into a LengthValue."""
        for unit in ("px", "pt", "em", "cm", "mm", "%"):
            if s.endswith(unit):
                return LengthValue(number=float(s[: -len(unit)]), unit=unit)
        try:
            return LengthValue(number=float(s), unit="")
        except ValueError:
            self._reporter.parse_error(ref_tok.file, ref_tok.line,
                f"invalid length value: {s!r}")

    # ------------------------------------------------------------------
    # Object template
    # ------------------------------------------------------------------

    def _parse_obj_template(self) -> ObjTemplate:
        start = self._consume(TokenType.KEYWORD)  # begin_obj
        name_tok = self._consume(TokenType.IDENTIFIER)
        self._skip_terminators()

        attributes: list[ObjAttr] = []
        # Object attributes use colon syntax: key: value
        while self._peek().type == TokenType.KEYWORD and self._peek().value in _OBJ_ATTR_KEYS:
            attr_tok = self._consume()
            self._consume(TokenType.COLON)
            val = self._parse_obj_attr_value(attr_tok.value, attr_tok)
            attributes.append(ObjAttr(key=attr_tok.value, value=val,
                                      source_file=attr_tok.file, line=attr_tok.line))
            self._skip_terminators()

        body = self._parse_drawing_commands("end_obj")
        self._consume(TokenType.KEYWORD)  # end_obj

        return ObjTemplate(
            name=name_tok.value,
            attributes=tuple(attributes),
            body=tuple(body),
            source_file=start.file,
            line=start.line,
        )

    def _parse_obj_attr_value(self, key: str, ref_tok: Token) -> Value:
        """Parse the value side of an object attribute (colon syntax)."""
        if key in ("width", "height"):
            return self._parse_length_token()
        if key == "background":
            return self._parse_color_value(ref_tok)
        if key == "clip-shape":
            if self._peek().type in (TokenType.IDENTIFIER, TokenType.KEYWORD):
                id_tok = self._consume(self._peek().type)
            else:
                self._reporter.parse_error(ref_tok.file, ref_tok.line,
                    f"expected IDENTIFIER or KEYWORD for clip-shape, got {self._peek().type.name}")
            return IdentValue(name=id_tok.value)
        if key == "clip-bounds":
            self._consume(TokenType.LPAREN)
            x1 = self._parse_length_token()
            self._consume(TokenType.COMMA)
            y1 = self._parse_length_token()
            self._consume(TokenType.COMMA)
            x2 = self._parse_length_token()
            self._consume(TokenType.COMMA)
            y2 = self._parse_length_token()
            self._consume(TokenType.RPAREN)
            return PointList(points=(
                PointValue(x=x1, y=y1),
                PointValue(x=x2, y=y2),
            ))
        if key == "border":
            # border: <line-type> <length> <color>
            lt_tok = self._consume(TokenType.KEYWORD)
            length = self._parse_length_token()
            color = self._parse_color_value(ref_tok)
            return StringValue(value=f"{lt_tok.value} {length.number}{length.unit}")
        if key == "shadow":
            # shadow: dx dy blur color
            dx = self._parse_length_token()
            dy = self._parse_length_token()
            blur = self._parse_length_token()
            color = self._parse_color_value(ref_tok)
            if isinstance(color, ColorNone):
                return ShadowValue(dx=dx, dy=dy, blur=blur, color=ColorValue(r=0, g=0, b=0, a=0.0))
            return ShadowValue(dx=dx, dy=dy, blur=blur, color=color)
        return self._parse_value(in_func_body=False)

    # ------------------------------------------------------------------
    # Function declaration
    # ------------------------------------------------------------------

    def _parse_func_decl(self) -> FuncDecl:
        """Parse begin_func … end_func.

        Arithmetic expressions (<expr>) are allowed in named-parameter value
        positions within the function body (in_func_body=True).
        """
        start = self._consume(TokenType.KEYWORD)  # begin_func
        name_tok = self._consume(TokenType.IDENTIFIER)
        self._consume(TokenType.LPAREN)

        params: list[str] = []
        if self._peek().type != TokenType.RPAREN:
            params.append(self._consume(TokenType.IDENTIFIER).value)
            while self._peek().type == TokenType.COMMA:
                self._consume()
                params.append(self._consume(TokenType.IDENTIFIER).value)
        self._consume(TokenType.RPAREN)
        self._skip_terminators()

        body = self._parse_drawing_commands(
            "end_func",
            in_func_body=True,
            allow_var_stmts=True,
            allow_loop_stmts=True,
        )
        self._consume(TokenType.KEYWORD)  # end_func

        return FuncDecl(
            name=name_tok.value,
            params=tuple(params),
            body=tuple(body),
            source_file=start.file,
            line=start.line,
        )

    # ------------------------------------------------------------------
    # Include
    # ------------------------------------------------------------------

    def _parse_include(self) -> IncludeStmt:
        tok = self._consume(TokenType.KEYWORD)  # include
        path_tok = self._consume(TokenType.STRING)
        return IncludeStmt(path=path_tok.value, source_file=tok.file, line=tok.line)

    # ------------------------------------------------------------------
    # Palette definition  (FEA-006, REQ-0040)
    # ------------------------------------------------------------------

    def _parse_palette_def(self) -> PaletteDef:
        """Parse begin_palette <name> <alias>=<color> ... end_palette."""
        start = self._consume(TokenType.KEYWORD)  # begin_palette
        name_tok = self._consume(TokenType.IDENTIFIER)
        self._skip_terminators()

        entries: dict[str, ColorValue | ColorNone] = {}

        while True:
            tok = self._peek()
            if tok.type == TokenType.EOF:
                self._reporter.parse_error(
                    start.file, start.line,
                    f"palette '{name_tok.value}': unexpected end of file; expected 'end_palette'"
                )
            if tok.type == TokenType.KEYWORD and tok.value == "end_palette":
                break
            if tok.type == TokenType.KEYWORD and tok.value == "do":
                self._reporter.parse_error(
                    tok.file, tok.line,
                    "do-while loop is not permitted inside a palette body"
                )
            if tok.type in (TokenType.NEWLINE, TokenType.SEMICOLON):
                self._consume()
                continue

            # Entry: <identifier> = <color_value>
            alias_tok = self._consume(TokenType.IDENTIFIER)
            self._consume(TokenType.EQUALS)
            color = self._parse_color_value(alias_tok)

            if alias_tok.value in entries:
                self._reporter.parse_error(
                    alias_tok.file, alias_tok.line,
                    f"palette '{name_tok.value}': duplicate alias '{alias_tok.value}'"
                )
            entries[alias_tok.value] = color
            self._skip_terminators()

        if not entries:
            self._reporter.parse_error(
                start.file, start.line,
                f"palette '{name_tok.value}' has no entries; "
                "a palette block must contain at least one color alias"
            )

        self._consume(TokenType.KEYWORD)  # end_palette

        return PaletteDef(
            palette_name=name_tok.value,
            entries=entries,
            source_file=start.file,
            line=start.line,
        )

    # ------------------------------------------------------------------
    # Drawing commands
    # ------------------------------------------------------------------

    def _parse_drawing_commands(
        self,
        stop_keyword: str,
        in_func_body: bool = False,
        allow_var_stmts: bool = False,
        allow_loop_stmts: bool = False,
    ) -> list[DrawingCmd]:
        cmds: list[DrawingCmd] = []
        self._skip_terminators()
        while True:
            tok = self._peek()
            if tok.type == TokenType.EOF:
                self._reporter.parse_error(tok.file, tok.line,
                    f"unexpected end of file; expected '{stop_keyword}'")
            if tok.type == TokenType.KEYWORD and tok.value == stop_keyword:
                break
            cmd = self._parse_drawing_stmt(in_func_body, allow_var_stmts, allow_loop_stmts)
            if cmd is not None:
                cmds.append(cmd)
            self._skip_terminators()
        return cmds

    def _parse_drawing_stmt(
        self,
        in_func_body: bool,
        allow_var_stmts: bool = False,
        allow_loop_stmts: bool = False,
    ) -> DrawingCmd | None:
        tok = self._peek()

        if tok.type == TokenType.KEYWORD:
            kw = tok.value
            if kw == "background":
                return self._parse_background()
            if kw == "grid":
                return self._parse_grid()
            if kw in _PRIMITIVE_KEYWORDS:
                return self._parse_primitive(kw, in_func_body)
            if kw == "image":
                # Must be image( → image drawing primitive
                if self._peek_ahead(1).type == TokenType.LPAREN:
                    return self._parse_primitive("image", in_func_body)
                # image without ( inside a body is an error
                self._reporter.parse_error(tok.file, tok.line,
                    "unexpected 'image' canvas statement inside a body block")
            if kw == "var":
                # Variable declaration (FEA-007): var x, y;
                if not allow_var_stmts:
                    self._reporter.parse_error(tok.file, tok.line,
                        "'var' declaration is not allowed in object template bodies")
                return self._parse_var_decl()
            if kw == "do":
                if not allow_loop_stmts:
                    self._reporter.parse_error(
                        tok.file, tok.line,
                        "do-while loop is not permitted inside an object template body"
                    )
                return self._parse_do_while(in_func_body, allow_var_stmts, allow_loop_stmts)

        if tok.type == TokenType.IDENTIFIER:
            # Named assignment or named primitive (FEA-007): ident = ...
            if self._peek_ahead(1).type == TokenType.EQUALS:
                if not allow_var_stmts:
                    self._reporter.parse_error(tok.file, tok.line,
                        "variable assignment is not allowed in object template bodies")
                return self._parse_named_or_assign(in_func_body)
            # Otherwise: object instantiation or function call — both use name(...)
            return self._parse_inst_or_call(in_func_body)

        # Tolerate stray terminators
        if tok.type in (TokenType.NEWLINE, TokenType.SEMICOLON):
            self._consume()
            return None

        self._reporter.parse_error(tok.file, tok.line,
            f"unexpected token {tok.value!r} in drawing commands")

    # ------------------------------------------------------------------
    # Background
    # ------------------------------------------------------------------

    def _parse_background(self) -> Background:
        tok = self._consume(TokenType.KEYWORD)  # background
        self._consume(TokenType.LPAREN)
        params = self._parse_named_param_list(in_func_body=False)
        self._consume(TokenType.RPAREN)
        return Background(params=params, source_file=tok.file, line=tok.line)

    def _parse_grid(self) -> GridNode:
        tok = self._consume(TokenType.KEYWORD)  # grid
        self._consume(TokenType.LPAREN)
        params = self._parse_named_param_list(in_func_body=False)
        self._consume(TokenType.RPAREN)
        return GridNode(params=params, source_file=tok.file, line=tok.line)

    # ------------------------------------------------------------------
    # Variable declarations and assignments (FEA-007)
    # ------------------------------------------------------------------

    def _parse_var_decl(self) -> VarDeclStmt:
        """Parse: var x, y;"""
        var_tok = self._consume(TokenType.KEYWORD)  # 'var'
        names: list[str] = [self._consume(TokenType.IDENTIFIER).value]
        while self._peek().type == TokenType.COMMA:
            self._consume()
            names.append(self._consume(TokenType.IDENTIFIER).value)
        return VarDeclStmt(
            names=tuple(names),
            source_file=var_tok.file,
            line=var_tok.line,
        )

    def _parse_named_or_assign(self, in_func_body: bool) -> AssignStmt | NamedDrawCmd:
        """Parse: name = square(...) or name = expr (where expr can include bbox access).

        If RHS is a primitive keyword followed by '(', produces NamedDrawCmd.
        Otherwise produces AssignStmt with an arithmetic expression as RHS.
        """
        name_tok = self._consume(TokenType.IDENTIFIER)
        self._consume(TokenType.EQUALS)

        tok = self._peek()
        # RHS is a primitive drawing command: rect1 = square(...)
        if tok.type == TokenType.KEYWORD and tok.value in _PRIMITIVE_KEYWORDS:
            cmd = self._parse_primitive(tok.value, in_func_body)
            return NamedDrawCmd(
                binding_name=name_tok.value,
                cmd=cmd,
                source_file=name_tok.file,
                line=name_tok.line,
            )
        # RHS is also an image primitive: rect1 = image(...)
        if tok.type == TokenType.KEYWORD and tok.value == "image" and self._peek_ahead(1).type == TokenType.LPAREN:
            cmd = self._parse_primitive("image", in_func_body)
            return NamedDrawCmd(
                binding_name=name_tok.value,
                cmd=cmd,
                source_file=name_tok.file,
                line=name_tok.line,
            )

        # RHS is an arithmetic expression (may include bbox access)
        expr = self._parse_expr(in_func_body=True)  # always allow exprs on RHS
        return AssignStmt(
            target=name_tok.value,
            value=expr,
            source_file=name_tok.file,
            line=name_tok.line,
        )

    def _parse_do_while(
        self,
        in_func_body: bool,
        allow_var_stmts: bool,
        allow_loop_stmts: bool,
    ) -> DoWhileStmt:
        start_tok = self._consume(TokenType.KEYWORD)  # do
        self._skip_terminators()
        body = self._parse_drawing_commands(
            "while",
            in_func_body=in_func_body,
            allow_var_stmts=allow_var_stmts,
            allow_loop_stmts=allow_loop_stmts,
        )

        if self._peek().type != TokenType.KEYWORD or self._peek().value != "while":
            self._reporter.parse_error(
                start_tok.file, start_tok.line,
                "do-while loop requires a trailing comparison condition"
            )
        self._consume(TokenType.KEYWORD)  # while
        condition = self._parse_comparison_expr(in_func_body=True)
        return DoWhileStmt(
            body=tuple(body),
            condition=condition,
            source_file=start_tok.file,
            line=start_tok.line,
        )

    def _parse_comparison_expr(self, in_func_body: bool) -> ComparisonExpr:
        left = self._parse_expr(in_func_body)
        op_tok = self._peek()
        valid_ops = {
            TokenType.EQEQ: "==",
            TokenType.NEQ: "!=",
            TokenType.LT: "<",
            TokenType.LTE: "<=",
            TokenType.GT: ">",
            TokenType.GTE: ">=",
        }
        if op_tok.type not in valid_ops:
            self._reporter.parse_error(
                op_tok.file, op_tok.line,
                "do-while condition must be a comparison expression"
            )
        self._consume()
        if op_tok.type == TokenType.LT and self._peek().type == TokenType.GT:
            bad_tok = self._consume()
            self._reporter.parse_error(
                bad_tok.file, bad_tok.line,
                "unsupported comparison operator '<>'"
            )
        right = self._parse_expr(in_func_body)
        return ComparisonExpr(
            left=left,
            op=valid_ops[op_tok.type],
            right=right,
            source_file=op_tok.file,
            line=op_tok.line,
        )

    def _parse_bbox_access(self) -> ExprBboxAccess:
        """Parse: obj.bbox.x (or .y, .width, .height).

        Called from _parse_expr_factor when IDENTIFIER DOT is detected.
        'width' and 'height' are KEYWORD tokens; 'x' and 'y' are IDENTIFIER.
        """
        obj_tok = self._consume(TokenType.IDENTIFIER)
        self._consume(TokenType.DOT)
        bbox_tok = self._consume(TokenType.IDENTIFIER)
        if bbox_tok.value != "bbox":
            self._reporter.parse_error(
                bbox_tok.file, bbox_tok.line,
                f"expected 'bbox' after '{obj_tok.value}.', got {bbox_tok.value!r}"
            )
        self._consume(TokenType.DOT)
        # property token — IDENTIFIER for x/y, KEYWORD for width/height
        prop_tok = self._consume()
        if prop_tok.type not in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            self._reporter.parse_error(
                prop_tok.file, prop_tok.line,
                f"expected bbox property (x, y, width, height), got {prop_tok.value!r}"
            )
        if prop_tok.value not in ("x", "y", "width", "height"):
            self._reporter.parse_error(
                prop_tok.file, prop_tok.line,
                f"unknown bbox property {prop_tok.value!r}; expected x, y, width, or height"
            )
        return ExprBboxAccess(
            object_name=obj_tok.value,
            prop=prop_tok.value,
            source_file=obj_tok.file,
            line=obj_tok.line,
        )

    # ------------------------------------------------------------------
    # Primitives
    # ------------------------------------------------------------------

    _PRIM_NODE_MAP = {
        "line":      LineNode,
        "circle":    CircleNode,
        "square":    SquareNode,
        "polygon":   PolygonNode,
        "path":      PathNode,
        "pie":       PieNode,
        "arc":       ArcNode,
        "connector": ConnectorNode,
        "font":      FontNode,
        "image":     ImagePrimNode,
    }

    def _parse_primitive(self, keyword: str, in_func_body: bool) -> DrawingCmd:
        tok = self._consume(TokenType.KEYWORD)  # the keyword itself
        self._consume(TokenType.LPAREN)
        params = self._parse_named_param_list(in_func_body=in_func_body)
        self._consume(TokenType.RPAREN)
        cls = self._PRIM_NODE_MAP[keyword]
        return cls(params=params, source_file=tok.file, line=tok.line)

    # ------------------------------------------------------------------
    # Object instantiation / function call
    # ------------------------------------------------------------------

    def _parse_inst_or_call(self, in_func_body: bool) -> DrawingCmd:
        name_tok = self._consume(TokenType.IDENTIFIER)
        self._consume(TokenType.LPAREN)

        # Determine by content: named params → ObjectInst, positional → FuncCall.
        # Peek: if first real token is IDENTIFIER followed by EQUALS → named params.
        tok = self._peek()
        if tok.type == TokenType.RPAREN:
            # Empty parens — treat as FuncCall with no args
            self._consume()
            return FuncCall(name=name_tok.value, args=(),
                            source_file=name_tok.file, line=name_tok.line)

        # Check for named-param style (key=value).
        # Keys can be IDENTIFIER (pos, scale, rotate, color …) or KEYWORD
        # (width, height, start, end …), so accept both token types here.
        is_named = (
            tok.type in (TokenType.IDENTIFIER, TokenType.KEYWORD)
            and self._peek_ahead(1).type == TokenType.EQUALS
        )

        if is_named:
            params = self._parse_named_param_list(in_func_body=in_func_body)
            self._consume(TokenType.RPAREN)
            return ObjectInst(name=name_tok.value, params=params,
                              source_file=name_tok.file, line=name_tok.line)
        else:
            args = self._parse_arg_list(in_func_body=in_func_body)
            self._consume(TokenType.RPAREN)
            return FuncCall(name=name_tok.value, args=tuple(args),
                            source_file=name_tok.file, line=name_tok.line)

    # ------------------------------------------------------------------
    # Named parameter list
    # ------------------------------------------------------------------

    def _parse_named_param_list(self, in_func_body: bool) -> dict[str, Value]:
        """Parse key=value pairs; duplicate keys are a parse error (REQ-0028)."""
        params: dict[str, Value] = {}
        if self._peek().type == TokenType.RPAREN:
            return params

        key, val = self._parse_named_param(in_func_body)
        if key in params:
            tok = self._peek()
            self._reporter.parse_error(tok.file, tok.line,
                f"duplicate parameter '{key}'")
        params[key] = val

        while self._peek().type == TokenType.COMMA:
            self._consume()
            # Trailing comma before ) is allowed
            if self._peek().type == TokenType.RPAREN:
                break
            key, val = self._parse_named_param(in_func_body)
            if key in params:
                tok = self._peek()
                self._reporter.parse_error(tok.file, tok.line,
                    f"duplicate parameter '{key}'")
            params[key] = val

        return params

    def _parse_named_param(self, in_func_body: bool) -> tuple[str, Value]:
        key_tok = self._peek()
        # Key can be a KEYWORD (e.g. 'color', 'fill', 'start', 'end') or IDENTIFIER
        if key_tok.type not in (TokenType.IDENTIFIER, TokenType.KEYWORD):
            self._reporter.parse_error(key_tok.file, key_tok.line,
                f"expected parameter name, got {key_tok.value!r}")
        self._consume()
        self._consume(TokenType.EQUALS)
        val = self._parse_value(in_func_body=in_func_body)
        return key_tok.value, val

    # ------------------------------------------------------------------
    # Positional argument list (function calls)
    # ------------------------------------------------------------------

    def _parse_arg_list(self, in_func_body: bool) -> list[Value]:
        args: list[Value] = []
        if self._peek().type == TokenType.RPAREN:
            return args
        args.append(self._parse_value(in_func_body=in_func_body))
        while self._peek().type == TokenType.COMMA:
            self._consume()
            if self._peek().type == TokenType.RPAREN:
                break
            args.append(self._parse_value(in_func_body=in_func_body))
        return args

    # ------------------------------------------------------------------
    # Value parsing
    # ------------------------------------------------------------------

    def _parse_value(self, in_func_body: bool) -> Value:
        tok = self._peek()

        # Point list: [(...), (...), ...]
        if tok.type == TokenType.LBRACKET:
            return self._parse_point_list()

        # Point: (x, y)
        if tok.type == TokenType.LPAREN:
            return self._parse_point(in_func_body)

        # Palette reference: @alias
        if tok.type == TokenType.AT_SIGN:
            return self._parse_palette_ref()

        # Color hex: #RRGGBB
        if tok.type == TokenType.COLOR_HEX:
            self._consume()
            return self._hex_to_color(tok.value, tok)

        # Named color or 'none'
        if tok.type == TokenType.COLOR_NAMED:
            self._consume()
            if tok.value == "none":
                return ColorNone()
            return self._named_color_to_color(tok.value)

        # RGB(...) / RGBA(...) functional color
        if tok.type == TokenType.KEYWORD and tok.value in ("RGB", "RGBA"):
            return self._parse_functional_color(tok)

        # Boolean
        if tok.type == TokenType.KEYWORD and tok.value in _BOOLEAN_VALUES:
            self._consume()
            return BoolValue(value=(tok.value == "true"))

        # Number (possibly start of arithmetic expression in func body)
        if tok.type == TokenType.NUMBER:
            if in_func_body:
                return self._parse_expr(in_func_body)
            length = self._parse_length_token()
            return length

        # Identifier — in func/frame body it may be a variable/parameter reference in an expr.
        # Disambiguation between variable references (e.g. height=bh) and enum-like IdentValues
        # (e.g. weight=bold) is done at dispatch time via the VariableStore scope check.
        if tok.type == TokenType.IDENTIFIER:
            if in_func_body:
                return self._parse_expr(in_func_body)
            self._consume()
            return IdentValue(name=tok.value)

        # Keyword used as value (e.g. line-type='solid', colorspace='RGB')
        if tok.type == TokenType.KEYWORD:
            self._consume()
            return IdentValue(name=tok.value)

        # String
        if tok.type == TokenType.STRING:
            self._consume()
            return StringValue(value=tok.value)

        self._reporter.parse_error(tok.file, tok.line,
            f"expected a value, got {tok.value!r}")

    # ------------------------------------------------------------------
    # Arithmetic expressions (function bodies only)
    # ------------------------------------------------------------------

    def _parse_expr(self, in_func_body: bool) -> ExprNode:
        """Parse additive expression: term (('+' | '-') term)*."""
        left = self._parse_expr_term(in_func_body)
        while self._peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_tok = self._consume()
            right = self._parse_expr_term(in_func_body)
            left = ExprBinOp(left=left, op=op_tok.value, right=right)
        return left

    def _parse_expr_term(self, in_func_body: bool) -> ExprNode:
        """Parse multiplicative expression: factor (('*' | '/') factor)*."""
        left = self._parse_expr_factor(in_func_body)
        while self._peek().type in (TokenType.STAR, TokenType.SLASH):
            op_tok = self._consume()
            right = self._parse_expr_factor(in_func_body)
            left = ExprBinOp(left=left, op=op_tok.value, right=right)
        return left

    def _parse_expr_factor(self, in_func_body: bool) -> ExprNode:
        """Parse a factor: number | identifier (variable/param) | obj.bbox.prop | '(' expr ')'."""
        tok = self._peek()
        if tok.type == TokenType.LPAREN:
            self._consume()
            inner = self._parse_expr(in_func_body)
            self._consume(TokenType.RPAREN)
            return inner
        if tok.type == TokenType.NUMBER:
            length = self._parse_length_token()
            return ExprFactor(value=length)
        if tok.type == TokenType.IDENTIFIER:
            # Check for bbox access pattern: identifier DOT ...  (FEA-007)
            if self._peek_ahead(1).type == TokenType.DOT:
                return self._parse_bbox_access()
            self._consume()
            return ExprFactor(value=tok.value)  # variable or parameter name reference
        self._reporter.parse_error(tok.file, tok.line,
            f"expected expression factor, got {tok.value!r}")

    # ------------------------------------------------------------------
    # Point / point-list
    # ------------------------------------------------------------------

    def _parse_point(self, in_func_body: bool) -> PointValue | ExprPoint:
        self._consume(TokenType.LPAREN)
        if in_func_body:
            x = self._parse_expr(in_func_body)
            self._consume(TokenType.COMMA)
            y = self._parse_expr(in_func_body)
            self._consume(TokenType.RPAREN)
            # If both sides are plain LengthValue factors, return PointValue
            if (isinstance(x, ExprFactor) and isinstance(x.value, LengthValue)
                    and isinstance(y, ExprFactor) and isinstance(y.value, LengthValue)):
                return PointValue(x=x.value, y=y.value)
            return ExprPoint(x=x, y=y)
        x = self._parse_length_token()
        self._consume(TokenType.COMMA)
        y = self._parse_length_token()
        self._consume(TokenType.RPAREN)
        return PointValue(x=x, y=y)

    def _parse_point_list(self) -> PointList:
        self._consume(TokenType.LBRACKET)
        points: list[PointValue] = []
        points.append(self._parse_point(in_func_body=False))  # type: ignore[arg-type]
        while self._peek().type == TokenType.COMMA:
            self._consume()
            if self._peek().type == TokenType.RBRACKET:
                break
            points.append(self._parse_point(in_func_body=False))  # type: ignore[arg-type]
        self._consume(TokenType.RBRACKET)
        return PointList(points=tuple(points))

    # ------------------------------------------------------------------
    # Length token
    # ------------------------------------------------------------------

    def _parse_length_token(self) -> LengthValue:
        tok = self._consume(TokenType.NUMBER)
        raw = tok.value
        for unit in ("px", "pt", "em", "cm", "mm", "%"):
            if raw.endswith(unit):
                return LengthValue(number=float(raw[: -len(unit)]), unit=unit)
        return LengthValue(number=float(raw), unit="")

    # ------------------------------------------------------------------
    # Color helpers
    # ------------------------------------------------------------------

    def _parse_color_value(self, ref_tok: Token) -> ColorValue | ColorNone:
        tok = self._peek()
        if tok.type == TokenType.COLOR_HEX:
            self._consume()
            return self._hex_to_color(tok.value, tok)
        if tok.type == TokenType.COLOR_NAMED:
            self._consume()
            if tok.value == "none":
                return ColorNone()
            return self._named_color_to_color(tok.value)
        if tok.type == TokenType.KEYWORD and tok.value in ("RGB", "RGBA"):
            return self._parse_functional_color(tok)
        # Note: AT_SIGN (@alias) is NOT allowed inside palette entry values.
        # It IS allowed in _parse_value (drawing command parameters).
        self._reporter.parse_error(ref_tok.file, ref_tok.line,
            f"expected color value, got {tok.value!r}")

    def _parse_palette_ref(self) -> PaletteRef:
        """Parse @<identifier> as an unresolved palette reference."""
        at_tok = self._consume(TokenType.AT_SIGN)
        alias_tok = self._consume(TokenType.IDENTIFIER)
        return PaletteRef(
            alias=alias_tok.value,
            source_file=at_tok.file,
            line=at_tok.line,
        )

    def _parse_functional_color(self, ref_tok: Token) -> ColorValue:
        func_tok = self._consume(TokenType.KEYWORD)  # 'RGB' or 'RGBA'
        self._consume(TokenType.LPAREN)
        r = int(self._consume(TokenType.NUMBER).value)
        self._consume(TokenType.COMMA)
        g = int(self._consume(TokenType.NUMBER).value)
        self._consume(TokenType.COMMA)
        b = int(self._consume(TokenType.NUMBER).value)
        a = 1.0
        if func_tok.value == "RGBA":
            self._consume(TokenType.COMMA)
            a = float(self._consume(TokenType.NUMBER).value)
        self._consume(TokenType.RPAREN)
        return ColorValue(r=r, g=g, b=b, a=a)

    @staticmethod
    def _hex_to_color(hex_str: str, ref_tok: Token) -> ColorValue:
        h = hex_str.lstrip("#")
        return ColorValue(
            r=int(h[0:2], 16),
            g=int(h[2:4], 16),
            b=int(h[4:6], 16),
            a=1.0,
        )

    # Full CSS-3 named-color table — matches every name accepted by the lexer.
    _NAMED_COLOR_MAP: dict[str, tuple[int, int, int]] = {
        # Basic set
        "black": (0, 0, 0),           "white": (255, 255, 255),
        "red": (255, 0, 0),           "green": (0, 128, 0),
        "blue": (0, 0, 255),          "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),     "yellow": (255, 255, 0),
        "orange": (255, 165, 0),      "purple": (128, 0, 128),
        "pink": (255, 192, 203),      "gray": (128, 128, 128),
        "darkgray": (169, 169, 169),  "lightgray": (211, 211, 211),
        "brown": (165, 42, 42),       "lime": (0, 255, 0),
        "navy": (0, 0, 128),          "teal": (0, 128, 128),
        "silver": (192, 192, 192),    "gold": (255, 215, 0),
        "transparent": (0, 0, 0),
        # Extended CSS Color Level 3
        "aqua": (0, 255, 255),                    "aquamarine": (127, 255, 212),
        "azure": (240, 255, 255),                 "beige": (245, 245, 220),
        "bisque": (255, 228, 196),                "blanchedalmond": (255, 235, 205),
        "blueviolet": (138, 43, 226),             "burlywood": (222, 184, 135),
        "cadetblue": (95, 158, 160),              "chartreuse": (127, 255, 0),
        "chocolate": (210, 105, 30),              "coral": (255, 127, 80),
        "cornflowerblue": (100, 149, 237),        "cornsilk": (255, 248, 220),
        "crimson": (220, 20, 60),                 "darkblue": (0, 0, 139),
        "darkcyan": (0, 139, 139),                "darkgoldenrod": (184, 134, 11),
        "darkgreen": (0, 100, 0),                 "darkkhaki": (189, 183, 107),
        "darkmagenta": (139, 0, 139),             "darkolivegreen": (85, 107, 47),
        "darkorange": (255, 140, 0),              "darkorchid": (153, 50, 204),
        "darkred": (139, 0, 0),                   "darksalmon": (233, 150, 122),
        "darkseagreen": (143, 188, 143),          "darkslateblue": (72, 61, 139),
        "darkslategray": (47, 79, 79),            "darkturquoise": (0, 206, 209),
        "darkviolet": (148, 0, 211),              "deeppink": (255, 20, 147),
        "deepskyblue": (0, 191, 255),             "dimgray": (105, 105, 105),
        "dodgerblue": (30, 144, 255),             "firebrick": (178, 34, 34),
        "floralwhite": (255, 250, 240),           "forestgreen": (34, 139, 34),
        "fuchsia": (255, 0, 255),                 "gainsboro": (220, 220, 220),
        "ghostwhite": (248, 248, 255),            "goldenrod": (218, 165, 32),
        "greenyellow": (173, 255, 47),            "honeydew": (240, 255, 240),
        "hotpink": (255, 105, 180),               "indianred": (205, 92, 92),
        "indigo": (75, 0, 130),                   "ivory": (255, 255, 240),
        "khaki": (240, 230, 140),                 "lavender": (230, 230, 250),
        "lavenderblush": (255, 240, 245),         "lawngreen": (124, 252, 0),
        "lemonchiffon": (255, 250, 205),          "lightblue": (173, 216, 230),
        "lightcoral": (240, 128, 128),            "lightcyan": (224, 255, 255),
        "lightgoldenrodyellow": (250, 250, 210),  "lightgreen": (144, 238, 144),
        "lightpink": (255, 182, 193),             "lightsalmon": (255, 160, 122),
        "lightseagreen": (32, 178, 170),          "lightskyblue": (135, 206, 250),
        "lightslategray": (119, 136, 153),        "lightsteelblue": (176, 196, 222),
        "lightyellow": (255, 255, 224),           "limegreen": (50, 205, 50),
        "linen": (250, 240, 230),                 "maroon": (128, 0, 0),
        "mediumaquamarine": (102, 205, 170),      "mediumblue": (0, 0, 205),
        "mediumorchid": (186, 85, 211),           "mediumpurple": (147, 112, 219),
        "mediumseagreen": (60, 179, 113),         "mediumslateblue": (123, 104, 238),
        "mediumspringgreen": (0, 250, 154),       "mediumturquoise": (72, 209, 204),
        "mediumvioletred": (199, 21, 133),        "midnightblue": (25, 25, 112),
        "mintcream": (245, 255, 250),             "mistyrose": (255, 228, 225),
        "moccasin": (255, 228, 181),              "navajowhite": (255, 222, 173),
        "oldlace": (253, 245, 230),               "olive": (128, 128, 0),
        "olivedrab": (107, 142, 35),              "orangered": (255, 69, 0),
        "orchid": (218, 112, 214),                "palegoldenrod": (238, 232, 170),
        "palegreen": (152, 251, 152),             "paleturquoise": (175, 238, 238),
        "palevioletred": (219, 112, 147),         "papayawhip": (255, 239, 213),
        "peachpuff": (255, 218, 185),             "peru": (205, 133, 63),
        "plum": (221, 160, 221),                  "powderblue": (176, 224, 230),
        "rosybrown": (188, 143, 143),             "royalblue": (65, 105, 225),
        "saddlebrown": (139, 69, 19),             "salmon": (250, 128, 114),
        "sandybrown": (244, 164, 96),             "seagreen": (46, 139, 87),
        "seashell": (255, 245, 238),              "sienna": (160, 82, 45),
        "skyblue": (135, 206, 235),               "slateblue": (106, 90, 205),
        "slategray": (112, 128, 144),             "snow": (255, 250, 250),
        "springgreen": (0, 255, 127),             "steelblue": (70, 130, 180),
        "tan": (210, 180, 140),                   "thistle": (216, 191, 216),
        "tomato": (255, 99, 71),                  "turquoise": (64, 224, 208),
        "violet": (238, 130, 238),                "wheat": (245, 222, 179),
        "whitesmoke": (245, 245, 245),            "yellowgreen": (154, 205, 50),
    }

    def _named_color_to_color(self, name: str) -> ColorValue:
        if name == "transparent":
            return ColorValue(r=0, g=0, b=0, a=0.0)
        rgb = self._NAMED_COLOR_MAP.get(name)
        if rgb:
            return ColorValue(r=rgb[0], g=rgb[1], b=rgb[2], a=1.0)
        return ColorValue(r=0, g=0, b=0, a=1.0)

    # ------------------------------------------------------------------
    # Token navigation helpers
    # ------------------------------------------------------------------

    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _peek_ahead(self, offset: int) -> Token:
        idx = self._pos + offset
        if idx >= len(self._tokens):
            return self._tokens[-1]  # EOF
        return self._tokens[idx]

    def _consume(self, expected: TokenType | None = None) -> Token:
        tok = self._tokens[self._pos]
        if expected is not None and tok.type != expected:
            self._reporter.parse_error(tok.file, tok.line,
                f"expected {expected.name}, got {tok.type.name} ({tok.value!r})")
        self._pos += 1
        return tok

    def _skip_terminators(self) -> None:
        while self._peek().type in (TokenType.NEWLINE, TokenType.SEMICOLON):
            self._consume()
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
