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
"""AST node dataclasses for the Technical Image Generator DSL.

Top-level statement types:
  FrameDef, ObjTemplate, FuncDecl, IncludeStmt, PaletteDef

DrawingCmd union:
  Background, GridNode, LineNode, CircleNode, SquareNode, PolygonNode, PathNode,
  PieNode, ArcNode, ConnectorNode, FontNode, ImagePrimNode,
  ObjectInst, FuncCall,
  VarDeclStmt, AssignStmt, NamedDrawCmd, DoWhileStmt

Value types:
  LengthValue, ColorValue, ColorNone, PaletteRef, PointValue, PointList, ShadowValue,
  BoolValue, StringValue, IdentValue, ExprNode, ExprBinOp, ExprFactor, ExprBboxAccess,
  ComparisonExpr

All nodes are frozen dataclasses carrying source_file and line for error reporting.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union


# ---------------------------------------------------------------------------
# Value types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LengthValue:
    number: float
    unit: str  # 'px' | 'pt' | 'em' | 'cm' | 'mm' | '%' | '' (bare — treated as px)


@dataclass(frozen=True)
class ColorValue:
    r: int
    g: int
    b: int
    a: float  # 0.0–1.0; 1.0 = fully opaque


@dataclass(frozen=True)
class ColorNone:
    """Represents color=none (transparent / no paint). Valid only on fill parameters."""


@dataclass(frozen=True)
class PaletteRef:
    """An unresolved palette color alias reference, e.g. @primary.

    Produced by the parser; resolved to ColorValue or ColorNone by the
    resolver after all PaletteDef entries have been collected in Pass 1.
    No PaletteRef survives past the resolver — any that do indicate an
    undefined alias and are reported as parse errors.
    """
    alias: str
    source_file: str
    line: int


@dataclass(frozen=True)
class PointValue:
    x: LengthValue
    y: LengthValue


@dataclass(frozen=True)
class PointList:
    points: tuple[PointValue, ...]


@dataclass(frozen=True)
class ShadowValue:
    dx: LengthValue
    dy: LengthValue
    blur: LengthValue
    color: ColorValue


@dataclass(frozen=True)
class BoolValue:
    value: bool


@dataclass(frozen=True)
class StringValue:
    value: str


@dataclass(frozen=True)
class IdentValue:
    name: str  # enum/keyword value used as a parameter (e.g. line-type='solid', colorspace='RGB')


# Arithmetic expression nodes (used inside begin_func and begin_frame bodies)

@dataclass(frozen=True)
class ExprFactor:
    """A leaf in an arithmetic expression: a LengthValue or a variable/parameter name."""
    value: Union[LengthValue, str]  # str = variable or parameter name


@dataclass(frozen=True)
class ExprBinOp:
    """Binary arithmetic operation: left op right."""
    left: ExprNode
    op: str   # '+' | '-' | '*' | '/'
    right: ExprNode


@dataclass(frozen=True)
class ExprBboxAccess:
    """Leaf: read a bounding-box property of a named rendered object (FEA-007).

    object_name is the binding name set by NamedDrawCmd.
    prop is one of: 'x', 'y', 'width', 'height'.
    Evaluated at runtime after the named object has been rendered.
    """
    object_name: str
    prop: str
    source_file: str
    line: int


@dataclass(frozen=True)
class ExprPoint:
    """A point whose coordinates are arithmetic expressions."""
    x: ExprNode
    y: ExprNode


# ExprNode is a recursive union — includes bbox access for FEA-007
ExprNode = Union[ExprFactor, ExprBinOp, ExprBboxAccess]


@dataclass(frozen=True)
class ComparisonExpr:
    """Binary numeric comparison used by do ... while loop conditions."""
    left: ExprNode
    op: str   # '==' | '!=' | '<' | '<=' | '>' | '>='
    right: ExprNode
    source_file: str
    line: int

# Value is the union of all value types a parameter can hold
Value = Union[
    LengthValue, ColorValue, ColorNone, PaletteRef,
    PointValue, PointList,
    ShadowValue,
    BoolValue, StringValue, IdentValue,
    ExprFactor, ExprBinOp, ExprPoint,
]


# ---------------------------------------------------------------------------
# Object template attribute
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ObjAttr:
    """A single colon-syntax attribute on an object template (e.g. width: 200px)."""
    key: str
    value: Value
    source_file: str
    line: int


# ---------------------------------------------------------------------------
# Drawing commands
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Background:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class GridNode:
    """Frame-level grid definition (FEA-004, REQ-0038)."""
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class LineNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class CircleNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class SquareNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class PolygonNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class PathNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class PieNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class ArcNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class ConnectorNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class FontNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class ImagePrimNode:
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class ObjectInst:
    """Instantiation of a named object template."""
    name: str
    params: dict[str, Value]
    source_file: str
    line: int


@dataclass(frozen=True)
class FuncCall:
    """Call to a named function with positional arguments."""
    name: str
    args: tuple[Value, ...]
    source_file: str
    line: int


# PrimitiveNode is the union of all standalone drawing primitive nodes
PrimitiveNode = Union[
    LineNode, CircleNode, SquareNode, PolygonNode, PathNode,
    PieNode, ArcNode, ConnectorNode, FontNode, ImagePrimNode,
]


# ---------------------------------------------------------------------------
# Variable / bounding-box statement nodes (FEA-007)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class VarDeclStmt:
    """Variable declaration inside a frame or function body (FEA-007).

    Syntax: var x, y;
    Declares one or more numeric variables in the current scope.
    Variables are initialised to None until assigned.
    """
    names: tuple[str, ...]
    source_file: str
    line: int


@dataclass(frozen=True)
class AssignStmt:
    """Assign an expression (possibly containing bbox accesses) to a variable (FEA-007).

    Syntax: x = rect1.bbox.x;   or   x = rect1.bbox.x + 10;
    The variable must have been declared with VarDeclStmt in the same scope.
    The value is an ExprNode that may include ExprBboxAccess leaves.
    """
    target: str
    value: ExprNode
    source_file: str
    line: int


@dataclass(frozen=True)
class NamedDrawCmd:
    """A primitive drawing command bound to a name for later bbox access (FEA-007).

    Syntax: rect1 = square(pos=(10, 10), width=100, height=50);
    Renders the inner primitive and registers it under binding_name so that
    subsequent AssignStmt nodes can read rect1.bbox.x / y / width / height.
    """
    binding_name: str
    cmd: PrimitiveNode  # the underlying primitive (resolved expressions before render)
    source_file: str
    line: int


@dataclass(frozen=True)
class DoWhileStmt:
    """A bounded post-condition loop allowed in frame/function bodies."""
    body: tuple[DrawingCmd, ...]
    condition: ComparisonExpr
    source_file: str
    line: int


# DrawingCmd is everything that can appear inside a frame/obj/func body
DrawingCmd = Union[
    Background, GridNode, PrimitiveNode, ObjectInst, FuncCall,
    VarDeclStmt, AssignStmt, NamedDrawCmd, DoWhileStmt,
]


# ---------------------------------------------------------------------------
# Canvas / image definition
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ImageDef:
    """Canvas properties declared with the 'image' statement inside a frame."""
    width: LengthValue
    height: LengthValue
    colorspace: str    # 'RGB' | 'RGBA' | 'GRAY'
    dpi: float
    output_format: str  # 'png' | 'jpeg' | 'gif' | 'images'
    source_file: str
    line: int


# ---------------------------------------------------------------------------
# Top-level statements
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FrameDef:
    name: str
    hold_time: float        # ms; default 100
    frame_mode: str         # 'one-run' | 'cyclic-run'
    colorspace_attr: str    # colorspace from frame attributes ('' if not set)
    image_def: ImageDef
    body: tuple[DrawingCmd, ...]
    source_file: str
    line: int


@dataclass(frozen=True)
class ObjTemplate:
    name: str
    attributes: tuple[ObjAttr, ...]
    body: tuple[DrawingCmd, ...]
    source_file: str
    line: int


@dataclass(frozen=True)
class FuncDecl:
    name: str
    params: tuple[str, ...]  # parameter names in declaration order
    body: tuple[DrawingCmd, ...]
    source_file: str
    line: int


@dataclass(frozen=True)
class IncludeStmt:
    path: str  # raw path string as written in the DSL
    source_file: str
    line: int


@dataclass(frozen=True)
class PaletteDef:
    """A begin_palette / end_palette block defining named color aliases (FEA-006).

    entries maps alias name → resolved color value (ColorValue or ColorNone).
    Entries are only direct color literals — @alias refs are not allowed inside
    a palette body.
    """
    palette_name: str
    entries: dict  # alias: str → ColorValue | ColorNone
    source_file: str
    line: int


# TopLevelStmt is any statement valid at the script's top level
TopLevelStmt = Union[FrameDef, ObjTemplate, FuncDecl, IncludeStmt, PaletteDef]


@dataclass(frozen=True)
class Script:
    """Root AST node produced by the parser."""
    statements: tuple[TopLevelStmt, ...]
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
