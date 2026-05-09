# Python API Reference

Auto-generated from the repository's Python source files.

Generated: `2026-05-09 07:58:09`
Modules documented: `46`

## Module Index

- `imagegen/__init__.py`: No module docstring.
- `imagegen/ast_nodes.py`: AST node dataclasses for the Technical Image Generator DSL. Top-level statement types: FrameDef, ObjTemplate, FuncDecl, IncludeStmt, PaletteDef
- `imagegen/error_reporter.py`: Centralised error/warning formatting and halting for the DSL engine. All *_error methods raise immediately — callers need not check return values.
- `imagegen/font_discovery.py`: Font discovery for the --list-fonts CLI command. Enumerates all fonts installed on the current system without external dependencies — uses only fontTools (already required) and the standard library.
- `imagegen/frame_runner.py`: Frame Runner (REQ-0002, REQ-0002.1, REQ-0002.2, REQ-0002.3). Iterates frame definitions in declaration order. Each frame produces an independent canvas — no state is shared between frames.
- `imagegen/lexer.py`: DSL Lexer — converts raw source text into a flat Token list. Key disambiguation rules implemented here: 1. '#' disambiguation: in a value position (immediately after '=' or '('),
- `imagegen/orchestrator.py`: Engine Orchestrator (REQ-0001, REQ-0028) — two-pass pipeline coordinator. Full pipeline executed by Engine.run(): 1. Read DSL source (DslIOError if unreadable)
- `imagegen/output/__init__.py`: No module docstring.
- `imagegen/output/output_formatter.py`: Output Formatter (REQ-0027, REQ-0029, REQ-0001.1, REQ-0001.2). Output format resolution rules: - Format is taken from the first frame's ImageDef.output_format.
- `imagegen/parser.py`: Recursive-descent parser for the Technical Image Generator DSL. Disambiguation rules: 1. 'image' keyword: if the next token is LPAREN → ImagePrimNode (drawing primitive);
- `imagegen/rendering/__init__.py`: No module docstring.
- `imagegen/rendering/background_renderer.py`: Background Renderer — applies solid, gradient, or image-file backgrounds. Gradient identical start/end edge case: warning is emitted by SemanticValidator; here we detect it again and fill with color1 silently (REQ-0004.2).
- `imagegen/rendering/bbox_renderer.py`: BBox Overlay Renderer (FEA-005, REQ-0039–REQ-0039.6). Draws a dashed, contrast-aware bounding box over each drawable element that carries show-bbox=true. Called as a post-process step on the final
- `imagegen/rendering/canvas_factory.py`: Canvas Factory — creates blank PIL Image buffers per frame. Default fills (REQ-0004.4): RGBA → transparent (0, 0, 0, 0)
- `imagegen/rendering/function_executor.py`: Function Executor (REQ-0015, REQ-0015.1–REQ-0015.3). Steps per execution: 1. Lookup function declaration in symbol_table.functions.
- `imagegen/rendering/grid_renderer.py`: Grid Renderer (FEA-004, REQ-0038.1) — draws optional visual grid lines over a canvas.
- `imagegen/rendering/object_instantiator.py`: Object Instantiator (REQ-0014, REQ-0014.1-REQ-0014.4). Steps per instantiation: 1. Lookup template in symbol_table.objects.
- `imagegen/rendering/primitive_dispatcher.py`: Primitive Dispatcher (REQ-0018, REQ-0019) — z-index sort + route to renderer. Z-order rule: - Primitives without explicit z-index retain their declaration order (stable sort).
- `imagegen/rendering/primitives/__init__.py`: No module docstring.
- `imagegen/rendering/primitives/arc_renderer.py`: Arc Renderer (REQ-0010.1) — stroke-only arc; 'fill' on arc is a parse error caught earlier.
- `imagegen/rendering/primitives/base_renderer.py`: Abstract base class for all primitive renderers. render() draws directly onto the canvas PIL Image in-place; it does not return a new image. The TransformApplier handles position/scale/skew/rotate separately after primitives are drawn
- `imagegen/rendering/primitives/circle_renderer.py`: Circle Renderer (REQ-0006) — filled or stroked circle.
- `imagegen/rendering/primitives/connector/__init__.py`: No module docstring.
- `imagegen/rendering/primitives/connector/cap_renderer.py`: Cap Renderer (REQ-0011.3, REQ-0011.4) — arrowheads at connector endpoints. Supported cap styles: 'none', 'arrow', 'filled-arrow', 'circle', 'square', 'diamond'. Validates no start-cap/end-cap alias conflict.
- `imagegen/rendering/primitives/connector/connector_renderer.py`: Connector Renderer (REQ-0011) — orchestrates the five connector sub-modules. Execution order per render() call: 1. RouteBuilder → geometry (list of pixel coordinates)
- `imagegen/rendering/primitives/connector/corner_styler.py`: Corner Styler (REQ-0011.5) — modifies intermediate vertices. Styles: 'sharp' — no modification (pass-through)
- `imagegen/rendering/primitives/connector/label_renderer.py`: Label Renderer (REQ-0011.6) — inline text label along a connector route.
- `imagegen/rendering/primitives/connector/pattern_engine.py`: Pattern Engine (REQ-0011.7, REQ-0011.8, REQ-0011.9). Tiles repeating patterns along a connector route. When animated=True, the phase is advanced by pattern_speed × frame_index pixels,
- `imagegen/rendering/primitives/connector/route_builder.py`: Route Builder (REQ-0011.2) — computes connector geometry. Three connector-type values: 'straight' — direct line between endpoints
- `imagegen/rendering/primitives/font_renderer.py`: Font / Text Renderer (REQ-0012). Font resolution chain: 1. Named font (truetype via ImageFont.truetype)
- `imagegen/rendering/primitives/image_renderer.py`: Image Primitive Renderer (REQ-0013, REQ-0032). SVG rasterisation: 1. Attempt cairosvg (preferred, pure-Python binding).
- `imagegen/rendering/primitives/line_renderer.py`: Line Renderer (REQ-0005) — stroke-only straight line.
- `imagegen/rendering/primitives/path_renderer.py`: Path Renderer (REQ-0009) — open polyline; stroke-only, no fill; ≥ 2 points required.
- `imagegen/rendering/primitives/pie_renderer.py`: Pie Renderer (REQ-0010) — pie slice: clockwise arc + two radii; fill supported.
- `imagegen/rendering/primitives/polygon_renderer.py`: Polygon Renderer (REQ-0008) — filled or stroked closed polygon; ≥ 3 points required.
- `imagegen/rendering/primitives/square_renderer.py`: Square Renderer (REQ-0007) — filled or stroked rectangle; no corner radius.
- `imagegen/rendering/transform_applier.py`: Transform Applier — applies position, scale, skew, and rotate to primitives. Transform order: position → scale → skew → rotate (REQ-0017). Z-index is NOT handled here — that is the Primitive Dispatcher's responsibility.
- `imagegen/rendering/variable_store.py`: Variable store for DSL frame/function scopes (FEA-007). Holds numeric variable values and named-object bounding boxes for a single frame or function execution. A fresh VariableStore is created for each frame;
- `imagegen/resolver.py`: Pass 1 Resolver — include resolution, circular detection, symbol collection, and palette reference resolution (FEA-006). Frames inside included files are silently ignored; only the root script's
- `imagegen/semantic_validator.py`: Semantic Validator — type and constraint checks before rendering. Halt-immediately conditions (raises ValidationError): - radius ≤ 0 on circle, pie, arc
- `imagegen/symbol_table.py`: Symbol table for the DSL engine. The namespace is flat and shared across frames, objects, and functions. Any duplicate name — regardless of kind — is a parse error.
- `imagegen/token_type.py`: Token type enumeration for the DSL lexer.
- `imagegen.py`: Technical Image Generator — CLI entry point. Usage: python imagegen.py <input.dsl> [output-path]
- `Tools/generate_check_etalonn_imageset.py`: Generate and verify etalon image copies.
- `Tools/generate_python_docs.py`: Generate Markdown API documentation from all Python files in the repo. Usage: python Tools/generate_python_docs.py
- `Tools/get_current_timestamp.py`: get_current_timestamp.py Prints the current local timestamp in one of two formats: --mode filename (default) YYYY-mm-dd-HHmmss safe for file names

## `imagegen/__init__.py`
No module docstring.

No public classes or functions found.

## `imagegen/ast_nodes.py`
AST node dataclasses for the Technical Image Generator DSL. Top-level statement types: FrameDef, ObjTemplate, FuncDecl, IncludeStmt, PaletteDef

### `LengthValue`
Fields:
- `number: float`
- `unit: str`

### `ColorValue`
Fields:
- `r: int`
- `g: int`
- `b: int`
- `a: float`

### `ColorNone`
Represents color=none (transparent / no paint). Valid only on fill parameters.

### `PaletteRef`
An unresolved palette color alias reference, e.g. @primary. Produced by the parser; resolved to ColorValue or ColorNone by the resolver after all PaletteDef entries have been collected in Pass 1.

Fields:
- `alias: str`
- `source_file: str`
- `line: int`

### `PointValue`
Fields:
- `x: LengthValue`
- `y: LengthValue`

### `PointList`
Fields:
- `points: tuple[PointValue, ...]`

### `ShadowValue`
Fields:
- `dx: LengthValue`
- `dy: LengthValue`
- `blur: LengthValue`
- `color: ColorValue`

### `BoolValue`
Fields:
- `value: bool`

### `StringValue`
Fields:
- `value: str`

### `IdentValue`
Fields:
- `name: str`

### `ExprFactor`
A leaf in an arithmetic expression: a LengthValue or a variable/parameter name.

Fields:
- `value: Union[LengthValue, str]`

### `ExprBinOp`
Binary arithmetic operation: left op right.

Fields:
- `left: ExprNode`
- `op: str`
- `right: ExprNode`

### `ExprBboxAccess`
Leaf: read a bounding-box property of a named rendered object (FEA-007). object_name is the binding name set by NamedDrawCmd. prop is one of: 'x', 'y', 'width', 'height'.

Fields:
- `object_name: str`
- `prop: str`
- `source_file: str`
- `line: int`

### `ExprPoint`
A point whose coordinates are arithmetic expressions.

Fields:
- `x: ExprNode`
- `y: ExprNode`

### `ComparisonExpr`
Binary numeric comparison used by do ... while loop conditions.

Fields:
- `left: ExprNode`
- `op: str`
- `right: ExprNode`
- `source_file: str`
- `line: int`

### `ObjAttr`
A single colon-syntax attribute on an object template (e.g. width: 200px).

Fields:
- `key: str`
- `value: Value`
- `source_file: str`
- `line: int`

### `Background`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `GridNode`
Frame-level grid definition (FEA-004, REQ-0038).

Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `LineNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `CircleNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `SquareNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `PolygonNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `PathNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `PieNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `ArcNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `ConnectorNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `FontNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `ImagePrimNode`
Fields:
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `ObjectInst`
Instantiation of a named object template.

Fields:
- `name: str`
- `params: dict[str, Value]`
- `source_file: str`
- `line: int`

### `FuncCall`
Call to a named function with positional arguments.

Fields:
- `name: str`
- `args: tuple[Value, ...]`
- `source_file: str`
- `line: int`

### `VarDeclStmt`
Variable declaration inside a frame or function body (FEA-007). Syntax: var x, y; Declares one or more numeric variables in the current scope.

Fields:
- `names: tuple[str, ...]`
- `source_file: str`
- `line: int`

### `AssignStmt`
Assign an expression (possibly containing bbox accesses) to a variable (FEA-007). Syntax: x = rect1.bbox.x; or x = rect1.bbox.x + 10; The variable must have been declared with VarDeclStmt in the same scope.

Fields:
- `target: str`
- `value: ExprNode`
- `source_file: str`
- `line: int`

### `NamedDrawCmd`
A primitive drawing command bound to a name for later bbox access (FEA-007). Syntax: rect1 = square(pos=(10, 10), width=100, height=50); Renders the inner primitive and registers it under binding_name so that

Fields:
- `binding_name: str`
- `cmd: PrimitiveNode`
- `source_file: str`
- `line: int`

### `DoWhileStmt`
A bounded post-condition loop allowed in frame/function bodies.

Fields:
- `body: tuple[DrawingCmd, ...]`
- `condition: ComparisonExpr`
- `source_file: str`
- `line: int`

### `ImageDef`
Canvas properties declared with the 'image' statement inside a frame.

Fields:
- `width: LengthValue`
- `height: LengthValue`
- `colorspace: str`
- `dpi: float`
- `output_format: str`
- `source_file: str`
- `line: int`

### `FrameDef`
Fields:
- `name: str`
- `hold_time: float`
- `frame_mode: str`
- `colorspace_attr: str`
- `image_def: ImageDef`
- `body: tuple[DrawingCmd, ...]`
- `source_file: str`
- `line: int`

### `ObjTemplate`
Fields:
- `name: str`
- `attributes: tuple[ObjAttr, ...]`
- `body: tuple[DrawingCmd, ...]`
- `source_file: str`
- `line: int`

### `FuncDecl`
Fields:
- `name: str`
- `params: tuple[str, ...]`
- `body: tuple[DrawingCmd, ...]`
- `source_file: str`
- `line: int`

### `IncludeStmt`
Fields:
- `path: str`
- `source_file: str`
- `line: int`

### `PaletteDef`
A begin_palette / end_palette block defining named color aliases (FEA-006). entries maps alias name → resolved color value (ColorValue or ColorNone). Entries are only direct color literals — @alias refs are not allowed inside

Fields:
- `palette_name: str`
- `entries: dict`
- `source_file: str`
- `line: int`

### `Script`
Root AST node produced by the parser.

Fields:
- `statements: tuple[TopLevelStmt, ...]`

## `imagegen/error_reporter.py`
Centralised error/warning formatting and halting for the DSL engine. All *_error methods raise immediately — callers need not check return values.

### `ParseError` (Exception)
Raised on malformed syntax, unknown keywords, duplicate parameters. Exit code 1.

### `ValidationError` (Exception)
Raised on type/constraint violations (negative radius, JPEG+RGBA, etc.). Exit code 1.

### `DslRuntimeError` (Exception)
Raised on runtime faults: division by zero, recursion. Exit code 2.

### `DslIOError` (Exception)
Raised when input/include files are unreadable or output cannot be written. Exit code 3.

### `ErrorReporter`
Format and emit DSL error/warning messages to stderr. All *_error methods print the message then raise immediately. The warning() method prints but continues execution.

Methods:
- `error(self, file: str, line: int, primitive: str, message: str) -> None`
  Print a generic error message without raising.
- `warning(self, file: str, line: int, message: str) -> None`
  Print a warning; execution continues.
- `parse_error(self, file: str, line: int, message: str) -> None`
  Print and raise ParseError — halts execution immediately.
- `validation_error(self, file: str, line: int, message: str) -> None`
  Print and raise ValidationError — halts execution immediately.
- `runtime_error(self, file: str, line: int, message: str) -> None`
  Print and raise DslRuntimeError — halts execution immediately.
- `io_error(self, file: str, line: int, message: str) -> None`
  Print and raise DslIOError — halts execution immediately.

## `imagegen/font_discovery.py`
Font discovery for the --list-fonts CLI command. Enumerates all fonts installed on the current system without external dependencies — uses only fontTools (already required) and the standard library.

### Module Functions
- `find_font_file(family: str, style_label: str = 'normal') -> str | None`
  Return the file path for the best matching font variant, or None. Matching is case-insensitive on family name. If the exact style variant is not available the function falls back to 'normal', then to any variant.
- `list_fonts() -> None`
  Print a structured font report to stdout.

## `imagegen/frame_runner.py`
Frame Runner (REQ-0002, REQ-0002.1, REQ-0002.2, REQ-0002.3). Iterates frame definitions in declaration order. Each frame produces an independent canvas — no state is shared between frames.

### `FrameRunner`
Methods:
- `__init__(self, symbol_table: SymbolTable, reporter: ErrorReporter, base_dir: pathlib.Path) -> None`
- `run_frames(self, frames: list[FrameDef]) -> list[tuple[FrameDef, Image.Image]]`
  Iterate frames in declaration order. Each frame produces an independent canvas — no state is shared between frames. Returns list of (FrameDef, rendered_image) pairs.

## `imagegen/lexer.py`
DSL Lexer — converts raw source text into a flat Token list. Key disambiguation rules implemented here: 1. '#' disambiguation: in a value position (immediately after '=' or '('),

### `Token`
Fields:
- `type: TokenType`
- `value: str`
- `file: str`
- `line: int`

### `Lexer`
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `tokenize(self, source: str, filename: str) -> list[Token]`
  Tokenize DSL source into a flat Token list. Raises ParseError on any character that cannot be matched. NEWLINE tokens are only emitted inside body blocks (depth > 0).

## `imagegen/orchestrator.py`
Engine Orchestrator (REQ-0001, REQ-0028) — two-pass pipeline coordinator. Full pipeline executed by Engine.run(): 1. Read DSL source (DslIOError if unreadable)

### `Engine`
Methods:
- `__init__(self) -> None`
  Construct all sub-components sharing a single ErrorReporter.
- `run(self, dsl_path: pathlib.Path, output_path: pathlib.Path | None) -> None`
  Execute the full two-pass pipeline from a DSL file path.

## `imagegen/output/__init__.py`
No module docstring.

No public classes or functions found.

## `imagegen/output/output_formatter.py`
Output Formatter (REQ-0027, REQ-0029, REQ-0001.1, REQ-0001.2). Output format resolution rules: - Format is taken from the first frame's ImageDef.output_format.

### `OutputFormatter`
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `write(self, frames: list[tuple[FrameDef, Image.Image]], script_stem: str, output_path: pathlib.Path | None, base_dir: pathlib.Path) -> None`
  Determine output format from first frame and write all output files. Conflicting output-format on subsequent frames: warning emitted, first wins.

## `imagegen/parser.py`
Recursive-descent parser for the Technical Image Generator DSL. Disambiguation rules: 1. 'image' keyword: if the next token is LPAREN → ImagePrimNode (drawing primitive);

### `Parser`
Fields:
- `_PRIM_NODE_MAP`
- `_NAMED_COLOR_MAP: dict[str, tuple[int, int, int]]`

Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `parse(self, tokens: list[Token]) -> Script`
  Entry point. Returns Script AST or raises ParseError. Disambiguation: - 'image' followed by LPAREN → image drawing primitive

## `imagegen/rendering/__init__.py`
No module docstring.

No public classes or functions found.

## `imagegen/rendering/background_renderer.py`
Background Renderer — applies solid, gradient, or image-file backgrounds. Gradient identical start/end edge case: warning is emitted by SemanticValidator; here we detect it again and fill with color1 silently (REQ-0004.2).

### `BackgroundRenderer`
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `render(self, canvas: Image.Image, node: Background, base_dir: pathlib.Path) -> None`
  Dispatch to _render_solid, _render_gradient, or _render_image.

## `imagegen/rendering/bbox_renderer.py`
BBox Overlay Renderer (FEA-005, REQ-0039–REQ-0039.6). Draws a dashed, contrast-aware bounding box over each drawable element that carries show-bbox=true. Called as a post-process step on the final

### Module Functions
- `render_bbox_overlays(canvas: Image.Image, commands: list[DrawingCmd], symbol_table: SymbolTable | None = None) -> None`
  Draw dashed bounding-box overlays for all commands with show-bbox=true.

## `imagegen/rendering/canvas_factory.py`
Canvas Factory — creates blank PIL Image buffers per frame. Default fills (REQ-0004.4): RGBA → transparent (0, 0, 0, 0)

### `CanvasFactory`
Methods:
- `create(self, image_def: ImageDef, aa_scale: int = 1) -> Image.Image`
  Return a blank PIL Image sized and colour-spaced per image_def. DPI decimal values are truncated to int before use (REQ-0003). Default fill: transparent for RGBA, white for RGB and GRAY (REQ-0004.4).

## `imagegen/rendering/function_executor.py`
Function Executor (REQ-0015, REQ-0015.1–REQ-0015.3). Steps per execution: 1. Lookup function declaration in symbol_table.functions.

### `FunctionExecutor`
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `execute(self, canvas: Image.Image, node: FuncCall, symbol_table: SymbolTable, dispatcher: PrimitiveDispatcher, base_dir: pathlib.Path, frame_index: int, call_stack: frozenset[str] | None = None) -> None`
  Lookup, bind args, evaluate exprs, detect recursion, execute body.

## `imagegen/rendering/grid_renderer.py`
Grid Renderer (FEA-004, REQ-0038.1) — draws optional visual grid lines over a canvas.

### Module Functions
- `render_grid(canvas: Image.Image, node: GridNode) -> None`
  Draw grid lines over the canvas. No-op when render=false.

## `imagegen/rendering/object_instantiator.py`
Object Instantiator (REQ-0014, REQ-0014.1-REQ-0014.4). Steps per instantiation: 1. Lookup template in symbol_table.objects.

### `ObjectInstantiator`
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `instantiate(self, canvas: Image.Image, node: ObjectInst, symbol_table: SymbolTable, dispatcher: PrimitiveDispatcher, base_dir: pathlib.Path, frame_index: int) -> None`
  Lookup, merge params, apply clip, execute body.

## `imagegen/rendering/primitive_dispatcher.py`
Primitive Dispatcher (REQ-0018, REQ-0019) — z-index sort + route to renderer. Z-order rule: - Primitives without explicit z-index retain their declaration order (stable sort).

### `PrimitiveDispatcher`
Fields:
- `MAX_DO_WHILE_ITERATIONS`

Methods:
- `__init__(self, renderers: dict[str, BaseRenderer], object_instantiator: ObjectInstantiator, function_executor: FunctionExecutor, reporter: ErrorReporter) -> None`
- `dispatch_all(self, canvas: Image.Image, commands: list[DrawingCmd], symbol_table: SymbolTable, base_dir: pathlib.Path, frame_index: int, variable_store: VariableStore | None = None) -> None`
  Sort commands by z-index (stable) then dispatch, unless variable statements are present — in that case execute sequentially in declaration order.

## `imagegen/rendering/primitives/__init__.py`
No module docstring.

No public classes or functions found.

## `imagegen/rendering/primitives/arc_renderer.py`
Arc Renderer (REQ-0010.1) — stroke-only arc; 'fill' on arc is a parse error caught earlier.

### `ArcRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: ArcNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/base_renderer.py`
Abstract base class for all primitive renderers. render() draws directly onto the canvas PIL Image in-place; it does not return a new image. The TransformApplier handles position/scale/skew/rotate separately after primitives are drawn

### `BaseRenderer` (ABC)
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `render(self, canvas: Image.Image, node: DrawingCmd, base_dir: pathlib.Path) -> None`
  Draw the primitive onto canvas in-place.

## `imagegen/rendering/primitives/circle_renderer.py`
Circle Renderer (REQ-0006) — filled or stroked circle.

### `CircleRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: CircleNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/connector/__init__.py`
No module docstring.

No public classes or functions found.

## `imagegen/rendering/primitives/connector/cap_renderer.py`
Cap Renderer (REQ-0011.3, REQ-0011.4) — arrowheads at connector endpoints. Supported cap styles: 'none', 'arrow', 'filled-arrow', 'circle', 'square', 'diamond'. Validates no start-cap/end-cap alias conflict.

### `CapRenderer`
Methods:
- `render_cap(self, draw: ImageDraw.Draw, tip: tuple[int, int], direction_angle: float, cap_style: str, color: tuple | int, aa_scale: int = 1) -> None`
  Draw arrowhead at tip pointing in direction_angle (radians, 0 = right). Supported styles: 'none', 'arrow', 'filled-arrow', 'circle', 'square', 'diamond'.
- `endpoint_angle(route: list[tuple[int, int]], at_end: bool) -> float`
  Return the direction angle (radians) at the start or end of a route.

## `imagegen/rendering/primitives/connector/connector_renderer.py`
Connector Renderer (REQ-0011) — orchestrates the five connector sub-modules. Execution order per render() call: 1. RouteBuilder → geometry (list of pixel coordinates)

### `ConnectorRenderer` (BaseRenderer)
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `set_font_renderer(self, font_renderer: FontRenderer) -> None`
- `set_frame_index(self, frame_index: int) -> None`
- `render(self, canvas: Image.Image, node: ConnectorNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/connector/corner_styler.py`
Corner Styler (REQ-0011.5) — modifies intermediate vertices. Styles: 'sharp' — no modification (pass-through)

### `CornerStyler`
Methods:
- `apply(self, points: list[tuple[int, int]], style: str, aa_scale: int = 1, radius_px: int | None = None) -> list[tuple[int, int]]`
  Return modified point list with styled corners at intermediate vertices.

## `imagegen/rendering/primitives/connector/label_renderer.py`
Label Renderer (REQ-0011.6) — inline text label along a connector route.

### `LabelRenderer`
Methods:
- `render(self, canvas: Image.Image, route: list[tuple[int, int]], params: dict, font_renderer: FontRenderer, aa_scale: int = 1) -> None`
  Render label text at 'start', 'center', or 'end' along the connector route.

## `imagegen/rendering/primitives/connector/pattern_engine.py`
Pattern Engine (REQ-0011.7, REQ-0011.8, REQ-0011.9). Tiles repeating patterns along a connector route. When animated=True, the phase is advanced by pattern_speed × frame_index pixels,

### `PatternEngine`
Methods:
- `draw_stroke(self, draw: ImageDraw.Draw, route: list[tuple[int, int]], pattern: str, color: tuple | int, line_width: int, animated: bool, pattern_speed: float, frame_index: int, aa_scale: int = 1) -> None`
  Tile repeating pattern along the route. When animated=True, advance phase by pattern_speed × frame_index pixels. aa_scale is applied to all hardcoded pixel constants.

## `imagegen/rendering/primitives/connector/route_builder.py`
Route Builder (REQ-0011.2) — computes connector geometry. Three connector-type values: 'straight' — direct line between endpoints

### `RouteBuilder`
Methods:
- `build(self, node: ConnectorNode, canvas_size: tuple[int, int], aa_scale: int = 1, dpi: int = 96) -> list[tuple[int, int]]`
  Return ordered list of pixel coordinates for the connector stroke.

## `imagegen/rendering/primitives/font_renderer.py`
Font / Text Renderer (REQ-0012). Font resolution chain: 1. Named font (truetype via ImageFont.truetype)

### `FontRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: FontNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/image_renderer.py`
Image Primitive Renderer (REQ-0013, REQ-0032). SVG rasterisation: 1. Attempt cairosvg (preferred, pure-Python binding).

### `ImageRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: ImagePrimNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/line_renderer.py`
Line Renderer (REQ-0005) — stroke-only straight line.

### `LineRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: LineNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/path_renderer.py`
Path Renderer (REQ-0009) — open polyline; stroke-only, no fill; ≥ 2 points required.

### `PathRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: PathNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/pie_renderer.py`
Pie Renderer (REQ-0010) — pie slice: clockwise arc + two radii; fill supported.

### `PieRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: PieNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/polygon_renderer.py`
Polygon Renderer (REQ-0008) — filled or stroked closed polygon; ≥ 3 points required.

### `PolygonRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: PolygonNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/primitives/square_renderer.py`
Square Renderer (REQ-0007) — filled or stroked rectangle; no corner radius.

### `SquareRenderer` (BaseRenderer)
Methods:
- `render(self, canvas: Image.Image, node: SquareNode, base_dir: pathlib.Path) -> None`

## `imagegen/rendering/transform_applier.py`
Transform Applier — applies position, scale, skew, and rotate to primitives. Transform order: position → scale → skew → rotate (REQ-0017). Z-index is NOT handled here — that is the Primitive Dispatcher's responsibility.

### `TransformParams`
Fields:
- `pos_x: int`
- `pos_y: int`
- `scale: float`
- `skew_x: float`
- `skew_y: float`
- `rotate: float`

### `TransformApplier`
Apply geometric transforms and composite a primitive onto the canvas. Transform order: position → scale → skew → rotate. Z-index is excluded from this class — handled by PrimitiveDispatcher.

Methods:
- `apply(self, canvas: Image.Image, primitive_image: Image.Image, params: dict[str, Value]) -> None`
  Composite primitive_image onto canvas after applying transforms in order: position → scale → skew → rotate.

## `imagegen/rendering/variable_store.py`
Variable store for DSL frame/function scopes (FEA-007). Holds numeric variable values and named-object bounding boxes for a single frame or function execution. A fresh VariableStore is created for each frame;

### `VariableStore`
Methods:
- `__init__(self) -> None`
- `declare(self, name: str) -> None`
  Declare a variable (sets to None if not already declared).
- `assign(self, name: str, value: float, source_file: str, line: int, reporter: ErrorReporter) -> None`
  Assign a value to a declared variable; raises DslRuntimeError if undeclared.
- `get(self, name: str) -> float | None`
  Return the variable's value, or None if undeclared or unassigned.
- `has_var(self, name: str) -> bool`
- `register_object(self, name: str, x: float, y: float, width: float, height: float) -> None`
  Register a rendered object's bounding box under binding_name.
- `get_bbox(self, name: str, source_file: str, line: int, reporter: ErrorReporter) -> tuple[float, float, float, float]`
  Return (x, y, width, height) for a named object; runtime error if unknown.
- `has_object(self, name: str) -> bool`

## `imagegen/resolver.py`
Pass 1 Resolver — include resolution, circular detection, symbol collection, and palette reference resolution (FEA-006). Frames inside included files are silently ignored; only the root script's

### `Resolver`
Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `resolve(self, script: Script, base_dir: pathlib.Path) -> tuple[SymbolTable, list[FrameDef]]`
  Pass 1 entry point. Returns (symbol_table, frames) where: - symbol_table contains all object/function definitions from the

## `imagegen/semantic_validator.py`
Semantic Validator — type and constraint checks before rendering. Halt-immediately conditions (raises ValidationError): - radius ≤ 0 on circle, pie, arc

### `SemanticValidator`
Validate types and constraints for drawing commands before rendering. Halt-immediately: radius<=0, fill on arc, color=none on stroke, JPEG+RGBA/GRAY, negative scale, angle with unit, clip-shape=polygon.

Methods:
- `__init__(self, reporter: ErrorReporter) -> None`
- `validate_frame(self, frame: FrameDef, symbol_table: SymbolTable) -> None`
  Validate ImageDef and all drawing commands in a frame.

## `imagegen/symbol_table.py`
Symbol table for the DSL engine. The namespace is flat and shared across frames, objects, and functions. Any duplicate name — regardless of kind — is a parse error.

### `SymbolTable`
Holds all object template, function, and palette definitions collected in Pass 1. The object/function/frame namespace is intentionally flat: registering a name that is already present raises a parse error immediately.

Fields:
- `objects: dict[str, ObjTemplate]`
- `functions: dict[str, FuncDecl]`
- `palettes: dict[str, ColorValue | ColorNone]`
- `_frame_names: set[str]`

Methods:
- `register_frame_name(self, name: str, reporter: ErrorReporter, source_file: str, line: int) -> None`
  Record a frame name for global namespace collision detection.
- `register_object(self, template: ObjTemplate, reporter: ErrorReporter) -> None`
  Register an object template; raise ParseError on duplicate name.
- `register_function(self, decl: FuncDecl, reporter: ErrorReporter) -> None`
  Register a function declaration; raise ParseError on duplicate name.
- `register_palette(self, palette_def: PaletteDef, reporter: ErrorReporter) -> None`
  Merge all color aliases from a PaletteDef into the global palette namespace. Raises ParseError if any alias is already defined (REQ-0040.1, REQ-0040.4).
- `lookup_object(self, name: str) -> ObjTemplate | None`
- `lookup_function(self, name: str) -> FuncDecl | None`
- `lookup_palette_alias(self, alias: str) -> ColorValue | ColorNone | None`

## `imagegen/token_type.py`
Token type enumeration for the DSL lexer.

### `TokenType` (Enum)
Fields:
- `KEYWORD`
- `IDENTIFIER`
- `NUMBER`
- `STRING`
- `COLOR_HEX`
- `COLOR_NAMED`
- `LPAREN`
- `RPAREN`
- `LBRACKET`
- `RBRACKET`
- `EQUALS`
- `COLON`
- `COMMA`
- `SEMICOLON`
- `NEWLINE`
- `AT_SIGN`
- `PLUS`
- `MINUS`
- `STAR`
- `SLASH`
- `EQEQ`
- `NEQ`
- `LT`
- `LTE`
- `GT`
- `GTE`
- `DOT`
- `EOF`

## `imagegen.py`
Technical Image Generator — CLI entry point. Usage: python imagegen.py <input.dsl> [output-path]

### Module Functions
- `main() -> None`

## `Tools/generate_check_etalonn_imageset.py`
Generate and verify etalon image copies.

### Module Functions
- `parse_args() -> argparse.Namespace`
- `supports_color() -> bool`
- `color_text(text: str, color_code: str) -> str`
- `is_supported_image(path: Path) -> bool`
- `find_image_files(root: Path) -> list[Path]`
- `make_etalon_path(source_path: Path) -> Path`
- `generate_etalon_images(root: Path) -> int`
- `derive_original_path(etalon_path: Path) -> Path | None`
- `compare_files(path_a: Path, path_b: Path) -> bool`
- `check_etalon_images(root: Path) -> tuple[int, int, int, int]`
- `main() -> int`

## `Tools/generate_python_docs.py`
Generate Markdown API documentation from all Python files in the repo. Usage: python Tools/generate_python_docs.py

### Module Functions
- `discover_python_files(root: Path) -> list[Path]`
- `safe_unparse(node: ast.AST | None) -> str`
- `clean_text(text: str) -> str`
- `format_arg(arg: ast.arg, default: ast.AST | None = None) -> str`
- `format_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str`
- `get_docstring_summary(node: ast.AST) -> str | None`
- `is_public_name(name: str) -> bool`
- `extract_fields(node: ast.ClassDef) -> list[str]`
- `extract_methods(node: ast.ClassDef) -> list[FunctionDoc]`
- `parse_module(path: Path) -> ModuleDoc`
- `render_function(function: FunctionDoc, prefix: str = '') -> list[str]`
- `render_class(cls: ClassDoc) -> list[str]`
- `render_module(module: ModuleDoc) -> list[str]`
- `build_document(modules: list[ModuleDoc]) -> str`
- `main() -> None`

### `FunctionDoc`
Fields:
- `name: str`
- `signature: str`
- `docstring: str | None`
- `lineno: int`

### `ClassDoc`
Fields:
- `name: str`
- `bases: list[str]`
- `docstring: str | None`
- `lineno: int`
- `fields: list[str]`
- `methods: list[FunctionDoc]`

### `ModuleDoc`
Fields:
- `path: str`
- `docstring: str | None`
- `classes: list[ClassDoc]`
- `functions: list[FunctionDoc]`

## `Tools/get_current_timestamp.py`
get_current_timestamp.py Prints the current local timestamp in one of two formats: --mode filename (default) YYYY-mm-dd-HHmmss safe for file names

No public classes or functions found.
