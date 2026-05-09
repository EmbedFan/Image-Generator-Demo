# Implementation Plan — Technical Image Generator

| Field | Value |
|---|---|
| **Description** | Implementation plan: module breakdown, file structure, class/function definitions, technology stack, step-by-step plan, and REQ mapping |
| **Created at** | 2026-05-01 20:06:36 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## Table of Contents

1. [Technology Stack](#1-technology-stack)
2. [File Structure](#2-file-structure)
3. [Module Breakdown](#3-module-breakdown)
   - 3.1 CLI Entry Point
   - 3.2 Error Reporter
   - 3.3 AST Nodes
   - 3.4 Token Types
   - 3.5 Symbol Table
   - 3.6 Lexer
   - 3.7 Parser
   - 3.8 Resolver (Pass 1)
   - 3.9 Semantic Validator
   - 3.10 Frame Runner
   - 3.11 Canvas Factory
   - 3.12 Background Renderer
   - 3.13 Transform Applier
   - 3.14 Base Renderer
   - 3.15 Primitive Renderers (Line … Image)
   - 3.16 Connector Sub-system
   - 3.17 Primitive Dispatcher
   - 3.18 Object Instantiator
   - 3.19 Function Executor
   - 3.20 Output Formatter
   - 3.21 Engine Orchestrator
4. [Step-by-Step Implementation Plan](#4-step-by-step-implementation-plan)
5. [REQ ID Mapping](#5-req-id-mapping)

---

## 1. Technology Stack

| Layer | Library / Module | Version | Purpose |
|---|---|---|---|
| **Runtime** | Python | 3.10+ | Language; uses `dataclasses`, `match`/`case` not required |
| **Image rendering** | Pillow (PIL) | ≥ 10.0 | Canvas, drawing, PNG/JPEG/GIF I/O |
| **SVG rasterisation** | cairosvg | ≥ 2.7 (optional) | Convert SVG assets to PNG in-memory |
| **SVG fallback** | svglib + reportlab | — | Alternative if cairosvg unavailable |
| **CLI** | argparse | stdlib | Argument parsing |
| **Path handling** | pathlib | stdlib | Cross-platform path resolution |
| **Math / geometry** | math | stdlib | Angle normalisation, coordinate transforms |
| **Tokenising** | re | stdlib | Regex-based tokeniser |
| **Deep copy** | copy | stdlib | Object template instance attribute cloning |
| **System I/O** | sys, os | stdlib | Exit codes, stderr |

**No virtual environment is assumed** — the tool must run with `python imagegen.py <input.dsl>` against a standard Python 3.10+ installation with Pillow installed.

---

## 2. File Structure

```
imagegen.py                                   # CLI entry point
imagegen/
    __init__.py
    orchestrator.py                           # Engine orchestrator (two-pass coordinator)
    error_reporter.py                         # Centralised error/warning emit + halt
    token_type.py                             # TokenType enum
    ast_nodes.py                              # AST node dataclasses (all constructs)
    symbol_table.py                           # SymbolTable dataclass
    lexer.py                                  # Tokenizer
    parser.py                                 # AST builder
    resolver.py                               # Pass 1: include resolver + symbol collector
    semantic_validator.py                     # Pass 2: type/constraint validation
    frame_runner.py                           # Pass 2: frame execution coordinator
    rendering/
        __init__.py
        canvas_factory.py                     # Blank canvas creation per frame
        background_renderer.py                # Solid / gradient / image-file backgrounds
        primitive_dispatcher.py               # Z-index sort + route to primitive renderer
        transform_applier.py                  # position → scale → skew → rotate
        object_instantiator.py                # Object template lookup + parameter merge
        function_executor.py                  # Function declaration lookup + body execution
        primitives/
            __init__.py
            base_renderer.py                  # Abstract base class for all primitives
            line_renderer.py
            circle_renderer.py
            square_renderer.py
            polygon_renderer.py
            path_renderer.py
            pie_renderer.py
            arc_renderer.py
            font_renderer.py
            image_renderer.py
            connector/
                __init__.py
                connector_renderer.py         # Connector orchestrator
                route_builder.py              # straight / curved / step geometry
                corner_styler.py              # sharp / rounded / beveled corners
                cap_renderer.py               # start-cap / end-cap arrowheads
                label_renderer.py             # inline connector label
                pattern_engine.py             # dash/dot/arrow/zigzag tiling + animation
    output/
        __init__.py
        output_formatter.py                   # PNG / JPEG / GIF / images writer
```

**Naming convention:** all file names and identifiers use `snake_case`. Package name `imagegen` matches the entry-point script.

---

## 3. Module Breakdown

Each section lists: purpose, public classes / functions with signatures, and inline documentation expectations.

---

### 3.1 `imagegen.py` — CLI Entry Point

**REQ:** REQ-0030, REQ-0031

**Purpose:** Parse CLI arguments, validate input file existence, invoke `Engine.run()`, translate exceptions to exit codes.

```python
def main() -> None: ...
```

- `argparse.ArgumentParser` configured with two arguments: `input_file` (required), `output_path` (optional).
- On success: exit code `0`.
- On `ParseError` / `ValidationError`: exit code `1`.
- On `RuntimeError`: exit code `2`.
- On `IOError`: exit code `3`.

**Inline doc expectations:**
- Module docstring: one-line description of the tool and invocation syntax.
- Inline comment on each exit code constant explaining the error class it represents.

---

### 3.2 `imagegen/error_reporter.py` — Error Reporter

**REQ:** REQ-0031, REQ-0025

**Purpose:** Format and emit parse/validation/runtime/warning messages to stderr. Raise typed exceptions to halt execution.

```python
class ParseError(Exception): ...
class ValidationError(Exception): ...
class DslRuntimeError(Exception): ...
class DslIOError(Exception): ...

class ErrorReporter:
    def error(self, file: str, line: int, primitive: str, message: str) -> None: ...
    def warning(self, file: str, line: int, message: str) -> None: ...
    def parse_error(self, file: str, line: int, message: str) -> None: ...        # raises ParseError
    def validation_error(self, file: str, line: int, message: str) -> None: ...  # raises ValidationError
    def runtime_error(self, file: str, line: int, message: str) -> None: ...     # raises DslRuntimeError
    def io_error(self, file: str, line: int, message: str) -> None: ...          # raises DslIOError
```

**Message format** emitted to `sys.stderr`:
```
<file>:<line>: error: <primitive>: <message>
<file>:<line>: warning: <message>
```

**Inline doc expectations:**
- Class docstring: note that all `*_error` methods raise immediately — callers need not check return values.
- Comment on each exception subclass naming the CLI exit code it maps to.

---

### 3.3 `imagegen/ast_nodes.py` — AST Node Dataclasses

**Purpose:** Typed in-memory representation of every DSL construct produced by the parser.

All nodes are frozen `@dataclass` instances. Each carries `source_file: str` and `line: int` for error reporting.

```python
@dataclass(frozen=True)
class Script:
    statements: tuple[TopLevelStmt, ...]

@dataclass(frozen=True)
class IncludeStmt:
    path: str
    source_file: str
    line: int

@dataclass(frozen=True)
class FrameDef:
    name: str
    hold_time: float        # ms; default 100
    frame_mode: str         # 'one-run' | 'cyclic-run'
    image_def: ImageDef
    body: tuple[DrawingCmd, ...]
    source_file: str
    line: int

@dataclass(frozen=True)
class ImageDef:
    width: LengthValue
    height: LengthValue
    colorspace: str         # 'RGB' | 'RGBA' | 'GRAY'
    dpi: float
    output_format: str      # 'png' | 'jpeg' | 'gif' | 'images'
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
    params: tuple[str, ...]
    body: tuple[DrawingCmd, ...]
    source_file: str
    line: int

# DrawingCmd union: Background | PrimitiveNode | ObjectInst | FuncCall
# PrimitiveNode union: LineNode | CircleNode | SquareNode | PolygonNode |
#                      PathNode | PieNode | ArcNode | ConnectorNode |
#                      FontNode | ImagePrimNode

@dataclass(frozen=True)
class Background:
    params: dict[str, Value]
    source_file: str
    line: int

@dataclass(frozen=True)
class LineNode:
    params: dict[str, Value]
    source_file: str
    line: int

# ... one dataclass per primitive (CircleNode, SquareNode, PolygonNode,
#     PathNode, PieNode, ArcNode, ConnectorNode, FontNode, ImagePrimNode)

@dataclass(frozen=True)
class ObjectInst:
    name: str
    params: dict[str, Value]
    source_file: str
    line: int

@dataclass(frozen=True)
class FuncCall:
    name: str
    args: tuple[Value, ...]
    source_file: str
    line: int

# Value types
@dataclass(frozen=True)
class LengthValue:
    number: float
    unit: str   # 'px' | 'pt' | 'em' | 'cm' | 'mm' | '%' | '' (bare px)

@dataclass(frozen=True)
class ColorValue:
    r: int; g: int; b: int; a: float  # a=1.0 for opaque

@dataclass(frozen=True)
class PointValue:
    x: LengthValue
    y: LengthValue

@dataclass(frozen=True)
class PointList:
    points: tuple[PointValue, ...]

# ObjAttr union for object template attributes
@dataclass(frozen=True)
class ObjAttr:
    key: str
    value: Value
```

**Inline doc expectations:**
- Module docstring listing the four top-level statement types and the DrawingCmd union members.
- No per-field comments — field names are self-documenting.

---

### 3.4 `imagegen/token_type.py` — Token Type Enum

**Purpose:** Enumerate all token kinds the lexer emits.

```python
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD      = auto()   # begin_frame, end_frame, begin_obj, end_obj, etc.
    IDENTIFIER   = auto()   # user-defined names
    NUMBER       = auto()   # numeric literal (with optional unit)
    STRING       = auto()   # double-quoted string
    COLOR_HEX    = auto()   # #RRGGBB
    COLOR_NAMED  = auto()   # black, white, red, …
    LPAREN       = auto()   # (
    RPAREN       = auto()   # )
    LBRACKET     = auto()   # [
    RBRACKET     = auto()   # ]
    EQUALS       = auto()   # =
    COLON        = auto()   # :
    COMMA        = auto()   # ,
    SEMICOLON    = auto()   # ;
    NEWLINE      = auto()   # \n (statement terminator)
    PLUS         = auto()   # + (function body arithmetic)
    MINUS        = auto()   # - (function body arithmetic)
    STAR         = auto()   # *
    SLASH        = auto()   # /
    EOF          = auto()
```

**Inline doc expectations:**
- Inline comment on each value explaining its DSL role.

---

### 3.5 `imagegen/symbol_table.py` — Symbol Table

**Purpose:** Hold all `begin_obj` / `begin_func` definitions collected in Pass 1.

```python
@dataclass
class SymbolTable:
    objects: dict[str, ObjTemplate]    # name → ObjTemplate
    functions: dict[str, FuncDecl]     # name → FuncDecl

    def register_object(self, template: ObjTemplate, reporter: ErrorReporter) -> None: ...
    def register_function(self, decl: FuncDecl, reporter: ErrorReporter) -> None: ...
    def lookup_object(self, name: str) -> ObjTemplate | None: ...
    def lookup_function(self, name: str) -> FuncDecl | None: ...
```

`register_*` methods call `reporter.parse_error()` on duplicate names (REQ-0016, REQ-0028).

**Inline doc expectations:**
- Class docstring noting that the namespace is flat and shared across frames, objects, and functions.

---

### 3.6 `imagegen/lexer.py` — Lexer / Tokenizer

**REQ:** REQ-0028

**Purpose:** Convert raw DSL source text into a flat sequence of `Token` objects.

```python
@dataclass
class Token:
    type: TokenType
    value: str           # raw matched text
    file: str
    line: int

class Lexer:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def tokenize(self, source: str, filename: str) -> list[Token]:
        """Return token list; raise ParseError on unknown character."""
```

**Key implementation notes:**
- Use a single compiled `re` regex with named groups for all token patterns (one-pass).
- Handle the `#` context disambiguation (§2.3 of grammar): after `=` or `(`, treat `#RRGGBB` as `COLOR_HEX`; otherwise treat `#` as start of comment.
- Emit `NEWLINE` tokens only when they act as statement terminators (inside frame/obj/func bodies, not at top level between blocks).
- Strip all comment text before emitting tokens.

**Inline doc expectations:**
- Comment on the regex group ordering explaining the disambiguation of `#` and `image`.
- Comment on why `NEWLINE` is only emitted inside bodies.

---

### 3.7 `imagegen/parser.py` — Parser

**REQ:** REQ-0028

**Purpose:** Consume `Token` list and produce a `Script` AST node.

```python
class Parser:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def parse(self, tokens: list[Token]) -> Script:
        """Entry point. Returns Script AST or raises ParseError."""

    # Internal recursive-descent methods (snake_case, private by convention)
    def _parse_top_level(self) -> TopLevelStmt: ...
    def _parse_frame(self) -> FrameDef: ...
    def _parse_image_def(self) -> ImageDef: ...
    def _parse_obj_template(self) -> ObjTemplate: ...
    def _parse_func_decl(self) -> FuncDecl: ...
    def _parse_include(self) -> IncludeStmt: ...
    def _parse_drawing_commands(self, stop_keyword: str) -> tuple[DrawingCmd, ...]: ...
    def _parse_background(self) -> Background: ...
    def _parse_primitive(self, keyword: str) -> PrimitiveNode: ...
    def _parse_named_param_list(self) -> dict[str, Value]: ...
    def _parse_value(self, in_func_body: bool = False) -> Value: ...
    def _parse_expr(self) -> ExprNode: ...   # arithmetic, function bodies only
    def _parse_point(self, in_func_body: bool = False) -> PointValue: ...
    def _parse_point_list(self) -> PointList: ...
    def _peek(self) -> Token: ...
    def _consume(self, expected: TokenType | None = None) -> Token: ...
```

**Key implementation notes:**
- Enforce duplicate key detection in `_parse_named_param_list()` — raise `parse_error` immediately (REQ-0028).
- `image` disambiguation: after lexing `KEYWORD('image')`, peek at next token: `LPAREN` → image primitive, else → canvas statement.
- `begin_func` body: pass `in_func_body=True` into `_parse_named_param_list` to allow `<expr>` in value positions.

**Inline doc expectations:**
- `parse()` docstring explaining the two disambiguation rules (image and `#`).
- Comment in `_parse_func_decl` on the arithmetic expression grammar scope.

---

### 3.8 `imagegen/resolver.py` — Pass 1 Resolver

**REQ:** REQ-0016, REQ-0016.1, REQ-0016.2, REQ-0014, REQ-0015

**Purpose:** Recursively load `include` directives, detect circular includes, and populate the `SymbolTable`. Frame blocks inside included files are silently ignored.

```python
class Resolver:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def resolve(
        self,
        script: Script,
        base_dir: pathlib.Path,
    ) -> tuple[SymbolTable, list[FrameDef]]:
        """
        Pass 1 entry point.
        Returns the populated symbol table and ordered list of frame definitions
        from the root script only (includes contribute symbols, not frames).
        """

    def _load_file(
        self,
        path: pathlib.Path,
        include_stack: list[pathlib.Path],
    ) -> Script:
        """Load, lex, and parse one DSL file; raise DslIOError if unreadable."""

    def _collect_symbols(self, script: Script, symbol_table: SymbolTable) -> None:
        """Walk top-level statements; register obj/func; recurse into includes."""
```

**Circular include detection:** `include_stack` is a list of currently-being-resolved absolute paths. Before loading a file, check membership; presence → `parse_error`.

**Inline doc expectations:**
- `resolve()` docstring clarifying that frames in included files are ignored per REQ-0016.
- Comment in `_load_file` noting path resolution is relative to the including file's directory (REQ-0016.1).

---

### 3.9 `imagegen/semantic_validator.py` — Semantic Validator

**REQ:** REQ-0025, REQ-0025.1

**Purpose:** Validate types and constraints for each drawing command before rendering.

```python
class SemanticValidator:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def validate_frame(self, frame: FrameDef, symbol_table: SymbolTable) -> None:
        """Validate all drawing commands in a frame; halt on first error."""

    def validate_background(self, node: Background) -> None: ...
    def validate_primitive(self, node: PrimitiveNode) -> None: ...
    def validate_object_inst(self, node: ObjectInst, symbol_table: SymbolTable) -> None: ...
    def validate_func_call(self, node: FuncCall, symbol_table: SymbolTable) -> None: ...

    # Constraint helpers (private)
    def _check_radius_positive(self, node: CircleNode | PieNode | ArcNode) -> None: ...
    def _check_min_points(self, node: PolygonNode | PathNode, minimum: int) -> None: ...
    def _check_no_fill_on_arc(self, node: ArcNode) -> None: ...
    def _check_color_not_none_on_stroke(self, node: PrimitiveNode) -> None: ...
    def _check_jpeg_not_rgba(self, image_def: ImageDef) -> None: ...
    def _check_scale_non_negative(self, params: dict) -> None: ...
    def _check_angle_no_unit(self, params: dict, keys: list[str]) -> None: ...
    def _check_clip_shape_not_polygon(self, attrs: list[ObjAttr]) -> None: ...
```

**Inline doc expectations:**
- Class docstring listing all halt-immediately vs. warning-only conditions as a quick reference.

---

### 3.10 `imagegen/frame_runner.py` — Frame Runner

**REQ:** REQ-0002, REQ-0002.1, REQ-0002.2, REQ-0002.3

**Purpose:** Iterate over frame definitions; for each frame create a canvas, validate, render all drawing commands, and return a rendered PIL `Image`.

```python
class FrameRunner:
    def __init__(
        self,
        symbol_table: SymbolTable,
        reporter: ErrorReporter,
    ) -> None: ...

    def run_frames(self, frames: list[FrameDef]) -> list[tuple[FrameDef, Image.Image]]:
        """
        Iterate frames in declaration order.
        Each frame produces an independent canvas — no state is shared.
        Returns list of (FrameDef, rendered_image) pairs.
        """

    def _run_single_frame(self, frame: FrameDef) -> Image.Image: ...
```

**Inline doc expectations:**
- `run_frames()` docstring emphasising the independence invariant (no cross-frame state).

---

### 3.11 `imagegen/rendering/canvas_factory.py` — Canvas Factory

**REQ:** REQ-0003, REQ-0004.4

**Purpose:** Create a blank in-memory PIL `Image` sized and color-spaced per `ImageDef`.

```python
class CanvasFactory:
    def create(self, image_def: ImageDef) -> Image.Image:
        """
        Returns a blank PIL Image.
        Default fill: transparent (RGBA), white (RGB, GRAY).
        DPI decimal values are truncated to int before use.
        """

    def _resolve_size_px(self, image_def: ImageDef) -> tuple[int, int]:
        """Convert width/height lengths to pixel integers, respecting unit and DPI."""
```

**Inline doc expectations:**
- Comment on `dpi` truncation rule (REQ-0003).
- Comment on default fill per colorspace (REQ-0004.4).

---

### 3.12 `imagegen/rendering/background_renderer.py` — Background Renderer

**REQ:** REQ-0004.1, REQ-0004.2, REQ-0004.3

**Purpose:** Apply one of three background modes (solid, gradient, image-file) to the canvas. Enforce the one-background-per-frame rule.

```python
class BackgroundRenderer:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def render(self, canvas: Image.Image, node: Background, base_dir: pathlib.Path) -> None:
        """Dispatch to _render_solid, _render_gradient, or _render_image."""

    def _render_solid(self, canvas: Image.Image, color: ColorValue) -> None: ...
    def _render_gradient(
        self,
        canvas: Image.Image,
        color1: ColorValue,
        color2: ColorValue,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> None: ...
    def _render_image(
        self,
        canvas: Image.Image,
        src: pathlib.Path,
        mode: str,
        opacity: float,
    ) -> None: ...
```

**Key notes:**
- Identical `start`/`end` for gradient → emit warning, fill with `color1` (REQ-0004.2).
- `_render_gradient` uses manual pixel computation for linear interpolation.
- `_render_image` supports modes `fit`, `stretch`, `clip`; applies `opacity` via alpha compositing.

**Inline doc expectations:**
- Comment on the gradient identical-endpoints edge case.
- Comment on mode semantics (`fit` preserves aspect ratio, `stretch` ignores it, `clip` centres and crops).

---

### 3.13 `imagegen/rendering/transform_applier.py` — Transform Applier

**REQ:** REQ-0017

**Purpose:** Apply geometric transforms to a rendered primitive image in the fixed order: position → scale → skew → rotate.

```python
class TransformApplier:
    def apply(
        self,
        canvas: Image.Image,
        primitive_image: Image.Image,
        params: dict[str, Value],
    ) -> Image.Image:
        """
        Composite primitive_image onto canvas after applying transforms.
        Order: position → scale → skew → rotate.
        Z-index is not handled here — handled by PrimitiveDispatcher.
        """

    def _extract_transform_params(self, params: dict) -> TransformParams: ...
    def _apply_scale(self, img: Image.Image, scale: float) -> Image.Image: ...
    def _apply_skew(self, img: Image.Image, skew_x: float, skew_y: float) -> Image.Image: ...
    def _apply_rotate(self, img: Image.Image, angle: float) -> Image.Image: ...
```

**Inline doc expectations:**
- Comment on why z-index is excluded from this class (separation of concerns with dispatcher).
- Comment on negative `scale` being a validation error caught earlier.

---

### 3.14 `imagegen/rendering/primitives/base_renderer.py` — Base Renderer

**Purpose:** Abstract base class enforcing the interface all primitive renderers implement.

```python
from abc import ABC, abstractmethod

class BaseRenderer(ABC):
    def __init__(self, reporter: ErrorReporter) -> None: ...

    @abstractmethod
    def render(
        self,
        canvas: Image.Image,
        node: PrimitiveNode,
        base_dir: pathlib.Path,
    ) -> None:
        """Draw the primitive onto canvas in-place."""
```

**Inline doc expectations:**
- Docstring noting that `render()` draws directly onto the canvas image; it does not return a new image.

---

### 3.15 Primitive Renderers

Each renderer is a thin class extending `BaseRenderer` that translates its AST node into Pillow draw calls.

#### `line_renderer.py` — Line Renderer (REQ-0005)

```python
class LineRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: LineNode, base_dir: pathlib.Path) -> None: ...
    def _resolve_line_style(self, line_type: str, line_width: int) -> dict: ...
```

#### `circle_renderer.py` — Circle Renderer (REQ-0006)

```python
class CircleRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: CircleNode, base_dir: pathlib.Path) -> None: ...
```

Uses `ImageDraw.ellipse()` with equal width and height. Fill applied only when `fill ≠ none`.

#### `square_renderer.py` — Square Renderer (REQ-0007)

```python
class SquareRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: SquareNode, base_dir: pathlib.Path) -> None: ...
```

Uses `ImageDraw.rectangle()`. No corner radius (REQ-0007).

#### `polygon_renderer.py` — Polygon Renderer (REQ-0008)

```python
class PolygonRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: PolygonNode, base_dir: pathlib.Path) -> None: ...
```

Uses `ImageDraw.polygon()`. Auto-closed by Pillow. Requires ≥ 3 points (validated before render).

#### `path_renderer.py` — Path Renderer (REQ-0009)

```python
class PathRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: PathNode, base_dir: pathlib.Path) -> None: ...
```

Uses `ImageDraw.line()` with multiple segments. Open path, no fill. Requires ≥ 2 points.

#### `pie_renderer.py` — Pie Renderer (REQ-0010)

```python
class PieRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: PieNode, base_dir: pathlib.Path) -> None: ...
```

Uses `ImageDraw.pieslice()`. Clockwise arc + two radii bounding the sector.

#### `arc_renderer.py` — Arc Renderer (REQ-0010.1)

```python
class ArcRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: ArcNode, base_dir: pathlib.Path) -> None: ...
```

Uses `ImageDraw.arc()`. Stroke only — `fill` parameter on `arc` is a parse error (caught earlier).

#### `font_renderer.py` — Font / Text Renderer (REQ-0012)

```python
class FontRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: FontNode, base_dir: pathlib.Path) -> None: ...

    def _resolve_font(self, font_family: str, font_size: int, style: str, weight: str) -> ImageFont.FreeTypeFont: ...
    def _render_multiline(self, draw: ImageDraw.Draw, text: str, pos: tuple, font: ImageFont, color: tuple, align: str) -> None: ...
```

Font resolution chain: named font → system generic family (`serif`/`sans-serif`/`monospace`) → `ImageFont.load_default()`.  
Multi-line: split on `\n`; repeat `ImageDraw.text()` at `font_size × 1.2` line spacing.

#### `image_renderer.py` — Image Primitive (REQ-0013, REQ-0032)

```python
class ImageRenderer(BaseRenderer):
    def render(self, canvas: Image.Image, node: ImagePrimNode, base_dir: pathlib.Path) -> None: ...

    def _load_asset(self, src: pathlib.Path) -> Image.Image: ...
    def _rasterise_svg(self, src: pathlib.Path) -> Image.Image: ...
```

SVG detection: check file extension; attempt `cairosvg` first; fall back to `svglib`; raise `DslIOError` if neither available.  
`opacity` applied via alpha channel multiplication.

---

### 3.16 Connector Sub-system

**REQ:** REQ-0011 – REQ-0011.9

The connector is decomposed into five sub-modules under `rendering/primitives/connector/`.

#### `connector_renderer.py` (REQ-0011)

```python
class ConnectorRenderer(BaseRenderer):
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def render(self, canvas: Image.Image, node: ConnectorNode, base_dir: pathlib.Path) -> None:
        """
        Orchestrates the five sub-modules in order:
        1. RouteBuilder → geometry
        2. CornerStyler → intermediate vertex shaping
        3. draw stroke (line/dash/dot) with PatternEngine
        4. CapRenderer → arrowheads
        5. LabelRenderer → inline label
        """
```

#### `route_builder.py` (REQ-0011.2)

```python
class RouteBuilder:
    def build(self, node: ConnectorNode, canvas_size: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Returns ordered list of pixel coordinates for the connector stroke.
        Supports three connector-type values:
          'straight' — direct line between endpoints
          'curved'   — Catmull-Rom spline through all points
          'step'     — horizontal–vertical–horizontal (H-V-H) routing
        """

    def _straight(self, points: list) -> list: ...
    def _curved_catmull_rom(self, points: list) -> list: ...
    def _step_hvh(self, start: tuple, end: tuple) -> list: ...
```

#### `corner_styler.py` (REQ-0011.5)

```python
class CornerStyler:
    def apply(self, points: list[tuple], style: str) -> list[tuple]:
        """
        Modifies intermediate vertices for straight/step connectors.
        'sharp'   — no modification
        'rounded' — insert quadratic Bezier control points at corners
        'beveled' — clip corners with a fixed setback distance
        Silently ignored for curved connectors.
        """
```

#### `cap_renderer.py` (REQ-0011.3, REQ-0011.4)

```python
class CapRenderer:
    def render_cap(
        self,
        draw: ImageDraw.Draw,
        tip: tuple[int, int],
        direction_angle: float,
        cap_style: str,
        color: tuple,
    ) -> None:
        """
        Draw arrowhead at tip pointing in direction_angle.
        Supported cap_style values: 'none', 'arrow', 'filled-arrow',
        'circle', 'square', 'diamond'.
        Validates no start-cap/end-cap alias conflict.
        """
```

#### `label_renderer.py` (REQ-0011.6)

```python
class LabelRenderer:
    def render(
        self,
        canvas: Image.Image,
        route: list[tuple],
        label: str,
        label_pos: str,   # 'start' | 'center' | 'end'
        offset: tuple[int, int],
        font_renderer: FontRenderer,
    ) -> None:
        """Render label text at the specified position along the connector route."""
```

#### `pattern_engine.py` (REQ-0011.7, REQ-0011.8, REQ-0011.9)

```python
class PatternEngine:
    def draw_stroke(
        self,
        draw: ImageDraw.Draw,
        route: list[tuple],
        pattern: str,         # 'solid' | 'dash' | 'dot' | 'arrow' | 'zigzag'
        color: tuple,
        line_width: int,
        animated: bool,
        pattern_speed: float,
        frame_index: int,
    ) -> None:
        """
        Tile repeating pattern along the route.
        When animated=True, advance phase by pattern_speed × frame_index pixels.
        """
```

---

### 3.17 `imagegen/rendering/primitive_dispatcher.py` — Primitive Dispatcher

**REQ:** REQ-0018, REQ-0019

**Purpose:** Sort drawing commands by z-index, then route each to the appropriate renderer.

```python
class PrimitiveDispatcher:
    def __init__(
        self,
        renderers: dict[str, BaseRenderer],
        object_instantiator: ObjectInstantiator,
        function_executor: FunctionExecutor,
        reporter: ErrorReporter,
    ) -> None: ...

    def dispatch_all(
        self,
        canvas: Image.Image,
        commands: list[DrawingCmd],
        symbol_table: SymbolTable,
        base_dir: pathlib.Path,
        frame_index: int,
    ) -> None:
        """
        Sort commands: declarations without z-index retain order;
        declarations with explicit z-index override their slot.
        Dispatch each to the correct renderer.
        """

    def _get_z_index(self, cmd: DrawingCmd, default: int) -> int: ...
    def _sort_by_z(self, commands: list[DrawingCmd]) -> list[DrawingCmd]: ...
```

**Inline doc expectations:**
- Comment on the stable-sort invariant: commands without `z-index` must retain their declaration order relative to each other.

---

### 3.18 `imagegen/rendering/object_instantiator.py` — Object Instantiator

**REQ:** REQ-0014, REQ-0014.1, REQ-0014.2, REQ-0014.3, REQ-0014.4

**Purpose:** Look up an object template, merge instance overrides with template defaults, apply clip region, and execute the template body.

```python
class ObjectInstantiator:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def instantiate(
        self,
        canvas: Image.Image,
        node: ObjectInst,
        symbol_table: SymbolTable,
        dispatcher: PrimitiveDispatcher,
        base_dir: pathlib.Path,
        frame_index: int,
    ) -> None:
        """
        1. Lookup template in symbol_table.objects; error if not found.
        2. Deep-copy template attributes; apply instance param overrides.
        3. Apply clip-bounds and clip-shape (intersection when both present).
        4. Execute template body drawing commands via dispatcher.
        """

    def _merge_params(self, template: ObjTemplate, overrides: dict) -> dict: ...
    def _apply_clip(self, canvas: Image.Image, attrs: dict) -> Image.Image: ...
```

**Inline doc expectations:**
- Comment on `clip-shape=polygon` being a validation error (not handled here — caught by SemanticValidator).
- Comment on clip intersection rule when both `clip-bounds` and `clip-shape` are present (REQ-0014.2).

---

### 3.19 `imagegen/rendering/function_executor.py` — Function Executor

**REQ:** REQ-0015, REQ-0015.1, REQ-0015.2, REQ-0015.3

**Purpose:** Look up a function declaration, bind positional arguments to parameter names, evaluate arithmetic expressions, execute body commands. Detect and reject recursion.

```python
class FunctionExecutor:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def execute(
        self,
        canvas: Image.Image,
        node: FuncCall,
        symbol_table: SymbolTable,
        dispatcher: PrimitiveDispatcher,
        base_dir: pathlib.Path,
        frame_index: int,
        call_stack: set[str] | None = None,
    ) -> None:
        """
        1. Lookup function in symbol_table.functions.
        2. Bind args to param names (positional).
        3. Evaluate arithmetic expressions in body params.
        4. Detect recursion via call_stack; raise DslRuntimeError if found.
        5. Execute body commands via dispatcher.
        """

    def _evaluate_expr(self, expr: ExprNode, bindings: dict[str, float]) -> float: ...
    def _bind_args(self, decl: FuncDecl, args: tuple[Value, ...]) -> dict[str, float]: ...
```

**Inline doc expectations:**
- Comment on division by zero: checked in `_evaluate_expr`; raises `DslRuntimeError` (REQ-0015.3).
- Comment on recursion detection: `call_stack` set of function names currently on the stack.

---

### 3.20 `imagegen/output/output_formatter.py` — Output Formatter

**REQ:** REQ-0027, REQ-0029, REQ-0001.1, REQ-0001.2

**Purpose:** Collect rendered frame buffers and write output file(s) according to `output-format` and colorspace.

```python
class OutputFormatter:
    def __init__(self, reporter: ErrorReporter) -> None: ...

    def write(
        self,
        frames: list[tuple[FrameDef, Image.Image]],
        script_stem: str,
        output_path: pathlib.Path | None,
        base_dir: pathlib.Path,
    ) -> None:
        """
        Determine output format from first frame's ImageDef.
        Dispatch to the correct writer method.
        Warn and ignore conflicting output-format on subsequent frames.
        """

    def _write_png(self, image: Image.Image, path: pathlib.Path) -> None: ...
    def _write_jpeg(self, image: Image.Image, path: pathlib.Path) -> None: ...
    def _write_gif(self, frames: list[tuple[FrameDef, Image.Image]], path: pathlib.Path) -> None: ...
    def _write_images(
        self,
        frames: list[tuple[FrameDef, Image.Image]],
        output_dir: pathlib.Path,
    ) -> None: ...
    def _resolve_output_path(
        self,
        script_stem: str,
        output_path: pathlib.Path | None,
        base_dir: pathlib.Path,
        extension: str,
    ) -> pathlib.Path: ...
```

**Key notes:**
- Output is written to the same directory as the input `.dsl` file unless `output_path` is provided (REQ-0029).
- `images` mode: RGBA/GRAY → `.png`; RGB → `.jpeg`. Duplicate frame-id → silent overwrite with warning (REQ-0001.1).
- GIF: `hold-time` per frame → delay parameter; `frame-mode` from first frame → `loop=0` (cyclic) or `loop=1` (one-run).
- JPEG with RGBA source → validation error (caught earlier).

**Inline doc expectations:**
- Comment explaining the conflicting `output-format` warning and resolution rule (first frame wins).
- Comment on the `images` mode RGBA/GRAY → `.png` fallback rule.

---

### 3.21 `imagegen/orchestrator.py` — Engine Orchestrator

**REQ:** REQ-0001, REQ-0028

**Purpose:** Wire all components together and execute the two-pass model from a DSL file path.

```python
class Engine:
    def __init__(self) -> None:
        """Construct all sub-components with shared ErrorReporter."""

    def run(self, dsl_path: pathlib.Path, output_path: pathlib.Path | None) -> None:
        """
        Full pipeline:
        1. Read DSL source (DslIOError if unreadable).
        2. Lex → parse → AST.
        3. Pass 1: Resolver → SymbolTable + frame list.
        4. SemanticValidator validates each frame.
        5. FrameRunner executes each frame → PIL Images.
        6. OutputFormatter writes output file(s).
        """
```

---

## 4. Step-by-Step Implementation Plan

Implementation phases follow a bottom-up dependency order. Each phase can be unit-tested before the next begins.

### Phase 1 — Foundation (no rendering dependencies)

| Step | File | Deliverable |
|---|---|---|
| 1 | `imagegen/error_reporter.py` | `ErrorReporter`, exception classes |
| 2 | `imagegen/token_type.py` | `TokenType` enum |
| 3 | `imagegen/ast_nodes.py` | All AST node dataclasses |
| 4 | `imagegen/symbol_table.py` | `SymbolTable` with register/lookup |

**Test milestone:** Unit tests for `ErrorReporter` message format, `SymbolTable` duplicate detection.

---

### Phase 2 — Parsing

| Step | File | Deliverable |
|---|---|---|
| 5 | `imagegen/lexer.py` | `Lexer.tokenize()` |
| 6 | `imagegen/parser.py` | `Parser.parse()` for all grammar constructs |

**Test milestone:** Parse all DSL grammar constructs from §3–§14 of `DSL_grammar_description.md`. Verify error messages for malformed input.

---

### Phase 3 — Pass 1

| Step | File | Deliverable |
|---|---|---|
| 7 | `imagegen/resolver.py` | `Resolver.resolve()`: include loading, circular detection, symbol collection |

**Test milestone:** Resolve multi-file scripts. Verify circular include detection and duplicate name errors.

---

### Phase 4 — Semantic Validation

| Step | File | Deliverable |
|---|---|---|
| 8 | `imagegen/semantic_validator.py` | All constraint checks per §8.1 of system design |

**Test milestone:** Validation errors for: negative radius, `fill` on arc, JPEG+RGBA, `clip-shape=polygon`, angle with unit suffix.

---

### Phase 5 — Rendering Foundation

| Step | File | Deliverable |
|---|---|---|
| 9 | `imagegen/rendering/canvas_factory.py` | `CanvasFactory.create()` |
| 10 | `imagegen/rendering/background_renderer.py` | All three background modes |
| 11 | `imagegen/rendering/transform_applier.py` | position → scale → skew → rotate |

**Test milestone:** Create canvases for all colorspaces. Apply solid, gradient, image backgrounds. Verify transform order.

---

### Phase 6 — Primitive Renderers

Implement in the order shown; each is independently testable against a blank canvas.

| Step | File |
|---|---|
| 12 | `imagegen/rendering/primitives/base_renderer.py` |
| 13 | `imagegen/rendering/primitives/line_renderer.py` |
| 14 | `imagegen/rendering/primitives/circle_renderer.py` |
| 15 | `imagegen/rendering/primitives/square_renderer.py` |
| 16 | `imagegen/rendering/primitives/polygon_renderer.py` |
| 17 | `imagegen/rendering/primitives/path_renderer.py` |
| 18 | `imagegen/rendering/primitives/pie_renderer.py` |
| 19 | `imagegen/rendering/primitives/arc_renderer.py` |
| 20 | `imagegen/rendering/primitives/font_renderer.py` |
| 21 | `imagegen/rendering/primitives/image_renderer.py` |

**Test milestone:** Render each primitive onto a test canvas. Visually inspect output PNG.

---

### Phase 7 — Connector Sub-system

| Step | File |
|---|---|
| 22 | `imagegen/rendering/primitives/connector/route_builder.py` |
| 23 | `imagegen/rendering/primitives/connector/corner_styler.py` |
| 24 | `imagegen/rendering/primitives/connector/cap_renderer.py` |
| 25 | `imagegen/rendering/primitives/connector/label_renderer.py` |
| 26 | `imagegen/rendering/primitives/connector/pattern_engine.py` |
| 27 | `imagegen/rendering/primitives/connector/connector_renderer.py` |

**Test milestone:** Render straight, curved, and step connectors with all cap/corner/pattern combinations.

---

### Phase 8 — Dispatch and Composition

| Step | File | Deliverable |
|---|---|---|
| 28 | `imagegen/rendering/primitive_dispatcher.py` | Z-index sort + dispatch |
| 29 | `imagegen/rendering/object_instantiator.py` | Template lookup + clip |
| 30 | `imagegen/rendering/function_executor.py` | Arg binding + expr eval + recursion guard |

**Test milestone:** Multi-primitive frame with mixed z-indexes renders in correct order. Object templates instantiate correctly. Function calls evaluate expressions.

---

### Phase 9 — Frame Execution

| Step | File | Deliverable |
|---|---|---|
| 31 | `imagegen/frame_runner.py` | Full single-frame and multi-frame pipeline |

**Test milestone:** Multi-frame animated GIF source renders N independent frames.

---

### Phase 10 — Output

| Step | File | Deliverable |
|---|---|---|
| 32 | `imagegen/output/output_formatter.py` | PNG, JPEG, GIF, images writers |

**Test milestone:** Verify file format and dimensions for all four output modes.

---

### Phase 11 — Orchestration and CLI

| Step | File | Deliverable |
|---|---|---|
| 33 | `imagegen/orchestrator.py` | `Engine.run()` wiring all phases |
| 34 | `imagegen.py` | `main()`, argparse, exit codes |

**Test milestone:** End-to-end integration test from raw `.dsl` files to verified output files. Confirm all four exit codes.

---

## 5. REQ ID Mapping

| REQ ID | Module(s) |
|---|---|
| REQ-0001 | `orchestrator.py`, `frame_runner.py` |
| REQ-0001.1 | `output/output_formatter.py` |
| REQ-0001.2 | `output/output_formatter.py` |
| REQ-0002 | `frame_runner.py` |
| REQ-0002.1 | `frame_runner.py`, `output/output_formatter.py` |
| REQ-0002.2 | `output/output_formatter.py` |
| REQ-0002.3 | `rendering/canvas_factory.py` |
| REQ-0003 | `rendering/canvas_factory.py` |
| REQ-0004.1 | `rendering/background_renderer.py` |
| REQ-0004.2 | `rendering/background_renderer.py` |
| REQ-0004.3 | `rendering/background_renderer.py` |
| REQ-0004.4 | `rendering/canvas_factory.py` |
| REQ-0005 | `rendering/primitives/line_renderer.py` |
| REQ-0006 | `rendering/primitives/circle_renderer.py` |
| REQ-0007 | `rendering/primitives/square_renderer.py` |
| REQ-0008 | `rendering/primitives/polygon_renderer.py` |
| REQ-0009 | `rendering/primitives/path_renderer.py` |
| REQ-0010 | `rendering/primitives/pie_renderer.py` |
| REQ-0010.1 | `rendering/primitives/arc_renderer.py` |
| REQ-0011 | `rendering/primitives/connector/connector_renderer.py` |
| REQ-0011.2 | `rendering/primitives/connector/route_builder.py` |
| REQ-0011.3 | `rendering/primitives/connector/cap_renderer.py` |
| REQ-0011.4 | `rendering/primitives/connector/cap_renderer.py` |
| REQ-0011.5 | `rendering/primitives/connector/corner_styler.py` |
| REQ-0011.6 | `rendering/primitives/connector/label_renderer.py` |
| REQ-0011.7 | `rendering/primitives/connector/pattern_engine.py` |
| REQ-0011.8 | `rendering/primitives/connector/pattern_engine.py` |
| REQ-0011.9 | `rendering/primitives/connector/pattern_engine.py` |
| REQ-0012 | `rendering/primitives/font_renderer.py` |
| REQ-0013 | `rendering/primitives/image_renderer.py` |
| REQ-0014 | `resolver.py`, `symbol_table.py`, `rendering/object_instantiator.py` |
| REQ-0014.1 | `rendering/object_instantiator.py` |
| REQ-0014.2 | `rendering/object_instantiator.py` |
| REQ-0014.3 | `rendering/object_instantiator.py` |
| REQ-0014.4 | `rendering/object_instantiator.py` |
| REQ-0015 | `resolver.py`, `symbol_table.py`, `rendering/function_executor.py` |
| REQ-0015.1 | `rendering/function_executor.py` |
| REQ-0015.2 | `rendering/function_executor.py` |
| REQ-0015.3 | `rendering/function_executor.py` |
| REQ-0016 | `resolver.py` |
| REQ-0016.1 | `resolver.py` |
| REQ-0016.2 | `resolver.py` |
| REQ-0017 | `rendering/transform_applier.py` |
| REQ-0018 | `rendering/primitive_dispatcher.py` |
| REQ-0019 | `rendering/primitive_dispatcher.py` |
| REQ-0020 | `rendering/primitives/` (all shape renderers) |
| REQ-0020.1 | `rendering/canvas_factory.py` |
| REQ-0021 | `rendering/canvas_factory.py`, `rendering/transform_applier.py` |
| REQ-0022 | `rendering/primitives/line_renderer.py` |
| REQ-0023 | `lexer.py`, `rendering/primitives/font_renderer.py` |
| REQ-0024 | `parser.py` |
| REQ-0025 | `semantic_validator.py`, `error_reporter.py` |
| REQ-0025.1 | `semantic_validator.py` |
| REQ-0026 | entire codebase (Python implementation) |
| REQ-0027 | `output/output_formatter.py` |
| REQ-0028 | `lexer.py`, `parser.py`, `orchestrator.py` |
| REQ-0029 | `output/output_formatter.py` |
| REQ-0030 | `imagegen.py` |
| REQ-0031 | `imagegen.py`, `error_reporter.py` |
| REQ-0032 | `rendering/primitives/image_renderer.py`, `rendering/background_renderer.py` |
| REQ-0033 | `rendering/primitives/image_renderer.py` |
