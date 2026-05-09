# System Design — Technical Image Generator

| Field | Value |
|---|---|
| **Description** | System design for the Technical Image Generator — architecture, components, data flow, storage, API, and integrations |
| **Created at** | 2026-04-30 11:24:16 |
| **File version** | 1.9 |
| **Created by** | Claude Sonnet 4.6 |

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [Components and Responsibilities](#3-components-and-responsibilities)
4. [Data Flow](#4-data-flow)
5. [Storage Design](#5-storage-design)
6. [API Definition (CLI)](#6-api-definition-cli)
7. [External Integrations](#7-external-integrations)
8. [Error Handling Strategy](#8-error-handling-strategy)
9. [Requirements Traceability](#9-requirements-traceability)

---

## 1. System Overview

The Technical Image Generator is a command-line Python tool that accepts a DSL script file as input and produces one or more image files (PNG, JPEG, or animated GIF) as output. The system is entirely self-contained, runs from the command line, and has no network or database dependencies.

**REQ coverage:** REQ-0001, REQ-0026, REQ-0027, REQ-0030

### Key Design Principles

- **Two-pass processing**: Pass 1 resolves includes and collects all symbol definitions (objects, functions). Pass 2 executes frames in declaration order.
- **Named-parameter model**: All primitive parameters are named and order-independent.
- **Strict validation**: Parse errors and semantic errors halt execution immediately with a descriptive message referencing file name and line number.
- **No runtime state across frames**: Each frame renders independently on a fresh canvas.

---

## 2. Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                          CLI Entry Point                             │
│                        imagegen.py  (REQ-0030)                       │
│   Usage: python imagegen.py <input.dsl> [output-path]                │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────────────┐
│                       Engine Orchestrator                            │
│                   Two-pass model  (REQ-0001, REQ-0028)               │
│                                                                      │
│   ┌───────────────────────────────────────────────────────────────┐  │
│   │                    PASS 1 — Resolver                          │  │
│   │                                                               │  │
│   │   ┌─────────────────────┐   ┌───────────────────────────┐     │  │
│   │   │   Include Resolver  │   │    Symbol Collector       │     │  │
│   │   │   (REQ-0016,        │   │  begin_obj  → obj-table   │     │  │
│   │   │    REQ-0016.1,      │   │  begin_func → func-table  │     │  │
│   │   │    REQ-0016.2)      │   │  (REQ-0014, REQ-0015)     │     │  │
│   │   └─────────────────────┘   └───────────────────────────┘     │  │
│   └───────────────────────────────────────────────────────────────┘  │
│                                                                      │
│   ┌───────────────────────────────────────────────────────────────┐  │
│   │                   PASS 2 — Frame Executor                     │  │
│   │                                                               │  │
│   │   ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐  │  │
│   │   │  Lexer /     │  │  Semantic    │  │  Frame Runner      │  │  │
│   │   │  Parser      │  │  Validator   │  │  (iterates frames) │  │  │
│   │   │  (REQ-0028)  │  │  (REQ-0025)  │  │  (REQ-0002)        │  │  │
│   │   └──────────────┘  └──────────────┘  └────────────────────┘  │  │
│   └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────────┘
                              │  (one canvas per frame)
┌─────────────────────────────▼────────────────────────────────────────┐
│                       Rendering Pipeline                             │
│                                                                      │
│  Canvas Factory                                                      │
│  └─► (width × height, colorspace, dpi)  (REQ-0003)                   │
│        │                                                             │
│        ▼                                                             │
│  Background Renderer   (REQ-0004.1 / REQ-0004.2 / REQ-0004.3 /       │
│  └─► solid | gradient | image-file        REQ-0004.4)                │
│        │                                                             │
│        ▼                                                             │
│  Grid Resolver  (REQ-0038, REQ-0038.2, REQ-0038.3, REQ-0038.4)       │
│  └─► snap element positions before Transform Applier (if grid set)   │
│        │                                                             │
│        ▼                                                             │
│  Primitive Dispatcher  (order = declaration order + z-index sort)    │
│  │                     (REQ-0018, REQ-0025)                          │
│  ├── Line Renderer         (REQ-0005)                                │
│  ├── Circle Renderer       (REQ-0006)                                │
│  ├── Square Renderer       (REQ-0007)                                │
│  ├── Polygon Renderer      (REQ-0008)                                │
│  ├── Path Renderer         (REQ-0009)                                │
│  ├── Pie Renderer          (REQ-0010)                                │
│  ├── Arc Renderer          (REQ-0010.1)                              │
│  ├── Connector Renderer    (REQ-0011 … REQ-0011.9)                   │
│  ├── Font/Text Renderer    (REQ-0012)                                │
│  └── Image Primitive       (REQ-0013)                                │
│        │                                                             │
│        ▼                                                             │
│  Transform Applier                                                   │
│  └─► position → scale → skew → rotate  (REQ-0017)                    │
│        │                                                             │
│        ▼                                                             │
│  Object Template Instantiator  (REQ-0014, REQ-0014.1 … REQ-0014.4)   │
│  Function Call Executor        (REQ-0015, REQ-0015.1, REQ-0015.2,    │
│                                            REQ-0015.3)               │
│        │                                                             │
│        ▼                                                             │
│  Variable Store / Bbox Extractor  (REQ-0041 … REQ-0041.5)            │
│  └─► per statement: execute var-decl / var-assign; after element     │
│      rendered, compute AABB and write to variable namespace          │
│        │                                                             │
│        ▼                                                             │
│  BBox Overlay Renderer  (REQ-0039 … REQ-0039.6)                      │
│  └─► per-element: if show-bbox=true, compute post-transform AABB,    │
│      sample background luminance, draw dashed contrast-aware overlay │
│        │                                                             │
│        ▼                                                             │
│  Grid Renderer  (REQ-0038.1)                                         │
│  └─► draw grid lines over canvas if render=true (post-process)       │
└─────────────────────────────┬────────────────────────────────────────┘
                              │  (rendered frame buffer(s))
┌─────────────────────────────▼────────────────────────────────────────┐
│                        Output Formatter                              │
│                                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐     │
│   │  PNG Writer  │  │  JPEG Writer │  │   GIF Assembler        │     │
│   │  (REQ-0027)  │  │  (REQ-0027)  │  │   animated / static    │     │
│   └──────────────┘  └──────────────┘  │   (REQ-0001.2,         │     │
│                                       │    REQ-0002.1,         │     │
│                                       │    REQ-0002.2)         │     │
│                                       └────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Components and Responsibilities

### 3.1 CLI Entry Point (`imagegen.py`)

**Responsibility:** Parse command-line arguments, validate file existence, invoke the Engine Orchestrator, and exit with code 0 (success) or non-zero (error).

**REQ:** REQ-0030, REQ-0031

**Interface:**
```
python imagegen.py <input.dsl> [output-path]
```

- `<input.dsl>` — required; path to DSL script.
- `[output-path]` — optional override for output file path or directory (for `images` mode).
- Missing or invalid arguments → print usage and exit with error.

---

### 3.2 Engine Orchestrator

**Responsibility:** Coordinate the two-pass execution model. Accept the resolved AST from the parser and drive Pass 1 and Pass 2.

**REQ:** REQ-0001, REQ-0028

#### Pass 1 — Resolver

| Sub-component | Responsibility | REQ |
|---|---|---|
| **Include Resolver** | Recursively load `include` directives; detect circular includes; resolve paths relative to including file | REQ-0016, REQ-0016.1, REQ-0016.2 |
| **Symbol Collector** | Collect all `begin_obj`/`end_obj` and `begin_func`/`end_func` definitions into the global symbol table; detect duplicate names | REQ-0014, REQ-0015, REQ-0016 |
| **Palette Collector** | Collect all `begin_palette`/`end_palette` definitions (local and from included files) into the global alias table; detect duplicate alias names and palette names | REQ-0040, REQ-0040.1, REQ-0040.3, REQ-0040.4 |

**Global symbol table structure:**
```
symbol_table = {
    "objects":   { name  → ObjectTemplate },
    "functions": { name  → FunctionDecl   },
    "palettes":  { alias → ColorValue     },  # merged from all begin_palette blocks
}
```

Namespace is flat and shared across frames, objects, and functions. Collision on any duplicate name (object, function, or palette alias) raises a parse error. (REQ-0028, REQ-0016, REQ-0040.1)

#### Pass 2 — Frame Executor

| Sub-component | Responsibility | REQ |
|---|---|---|
| **Lexer / Parser** | Tokenise DSL source; build AST; enforce grammar; report `<file>:<line>: error:` messages; open all source files with explicit UTF-8 encoding; strip leading BOM; raise `DslIOError` on decode failure | REQ-0028, REQ-0031, REQ-0035, REQ-0035.1 |
| **Semantic Validator** | Validate types (colors, units, angles, enum values); check constraints (radius > 0, path ≥ 2 points, etc.); resolve `@<alias>` palette references to concrete color values; report undefined aliases as parse errors | REQ-0025, REQ-0025.1, REQ-0040.2, REQ-0040.5 |
| **Frame Runner** | Iterate `begin_frame` blocks; create a fresh canvas per frame; dispatch drawing commands | REQ-0002, REQ-0002.1, REQ-0002.2 |

---

### 3.3 Rendering Pipeline

#### 3.3.1 Canvas Factory

**Responsibility:** Create a blank in-memory image buffer for each frame according to `width`, `height`, `colorspace`, and `dpi`.

**REQ:** REQ-0003, REQ-0004.4

- Default state when no `background` is present: transparent (RGBA), white (RGB / GRAY). (REQ-0004.4)
- `dpi` decimal values are truncated to integer before use. (REQ-0003)

#### 3.3.2 Background Renderer

**Responsibility:** Apply one of three background modes to the canvas.

**REQ:** REQ-0004.1, REQ-0004.2, REQ-0004.3

| Mode | Trigger | Notes |
|---|---|---|
| Solid | `color=` present | Fills entire canvas; duplicate background = validation error |
| Gradient | `color1=` and `color2=` present | Linear interpolation; identical `start`/`end` → fills `color1` + warning |
| Image file | `src=` present | Modes: `fit`, `stretch`, `clip`; `opacity` supported |

Only one `background` statement is allowed per frame. (REQ-0004.1)

#### 3.3.3 Primitive Dispatcher

**Responsibility:** Route each drawing command to the correct renderer; apply z-index sorting before rendering.

**REQ:** REQ-0018

Z-order: primitives without explicit `z-index` are rendered in declaration order. Primitives with `z-index` override their slot in the render sequence. (REQ-0018)

#### 3.3.4 Primitive Renderers

| Renderer | Parameters | Fill | Notes | REQ |
|---|---|---|---|---|
| **Line** | `color`, `line-type`, `line-width`, `start`, `end` | No | Stroke only | REQ-0005 |
| **Circle** | `color`, `fill`, `center`, `radius`, `line-type`, `line-width` | Yes | radius > 0 required | REQ-0006 |
| **Square** | `color`, `fill`, `pos`, `width`, `height`, `line-type`, `line-width` | Yes | No corner-radius | REQ-0007 |
| **Polygon** | `color`, `fill`, `points`, `line-type`, `line-width` | Yes | ≥ 3 points; auto-closed | REQ-0008 |
| **Path** | `color`, `points`, `line-type`, `line-width` | No | ≥ 2 points; open | REQ-0009 |
| **Pie** | `color`, `fill`, `center`, `radius`, `start-angle`, `end-angle` | Yes | Clockwise; arc + two radii | REQ-0010 |
| **Arc** | `color`, `center`, `radius`, `start-angle`, `end-angle` | No | Stroke only; `fill` = parse error | REQ-0010.1 |
| **Connector** | `color`, `points`/`start`+`end`, caps, label, pattern, animation | No | Rich sub-system (§3.3.5) | REQ-0011–REQ-0011.9 |
| **Font** | `font-family`, `font-size`, `color`, `style`, `weight`, `align`, `text`, `pos` | N/A | Multi-line via `\n` | REQ-0012 |
| **Image** | `src`, `pos`, `width`, `height`, `opacity` | N/A | Aspect-ratio auto-scale | REQ-0013 |

#### 3.3.5 Connector Sub-system

The Connector is the most complex primitive and is internally decomposed:

| Sub-module | Responsibility | REQ |
|---|---|---|
| **Route Builder** | Compute geometry for `straight`, `curved` (Catmull-Rom), or `step` (H-V-H) types | REQ-0011.2 |
| **Corner Styler** | Apply `sharp`, `rounded`, or `beveled` corners at intermediate vertices (straight/step only; silently ignored for curved) | REQ-0011.5 |
| **Cap Renderer** | Draw arrowhead shape at `start-cap` and/or `end-cap`; validate no alias conflict | REQ-0011.3, REQ-0011.4 |
| **Label Renderer** | Render text label at `start`, `center`, or `end` with offset; uses Font Renderer internally | REQ-0011.6 |
| **Pattern Engine** | Tile repeating `dash`/`dot`/`arrow`/`zigzag` pattern along stroke; advance by `pattern-speed` per frame when `animated=true` | REQ-0011.7, REQ-0011.8, REQ-0011.9 |

#### 3.3.6 Transform Applier

**Responsibility:** Apply geometric transforms to every primitive in the order: **position → scale → skew → rotate**. Z-index is not a geometric transform; it is handled by the Dispatcher.

**REQ:** REQ-0017

| Parameter | Type | Default | Constraint |
|---|---|---|---|
| `rotate` | degrees 0–360 | 0 | No unit suffix; negative = validation error |
| `skew-x` | degrees | 0 | — |
| `skew-y` | degrees | 0 | — |
| `scale` | multiplier | 1.0 | Negative = error; 0 = invisible, valid |
| `z-index` | int 0–1000 | declaration order | — |

#### 3.3.7 Object Template Instantiator

**Responsibility:** Look up object templates from the symbol table; merge instance parameter overrides with template defaults; execute internal drawing commands in the object's local coordinate space; support both the default scale-on-resize path and the opt-in layout-resize path for object instances.

**REQ:** REQ-0014, REQ-0014.1, REQ-0014.2, REQ-0014.3, REQ-0014.4, REQ-0036, REQ-0036.1, REQ-0036.2, REQ-0037, REQ-0044, REQ-0044.1, REQ-0044.2, REQ-0044.3

Supported object attributes (colon syntax):

| Attribute | Type | Notes |
|---|---|---|
| `width` | length | Bounding box width |
| `height` | length | Bounding box height |
| `background` | color | Object fill |
| `border` | line-type + length + color | Border stroke |
| `shadow` | dx dy blur color | Drop shadow; `blur=0` = hard edge |
| `clip-bounds` | (x1,y1,x2,y2) | Rectangular clip |
| `clip-shape` | `circle` \| `square` | Shape clip; `polygon` = validation error |

When both `clip-bounds` and `clip-shape` are present, the effective region is their **intersection**. (REQ-0014.2)

**Instance-time size and rotation parameters** (passed at call site, override template defaults for that instance only):

| Parameter | Type | Notes |
|---|---|---|
| `width` | length | Overrides template `width` for this instance (REQ-0036) |
| `height` | length | Overrides template `height` for this instance (REQ-0036) |
| `scale` | multiplier > 0 | Uniform scale of template dimensions; in the default path it is ignored with warning if `width`/`height` are also provided (REQ-0036.1, REQ-0036.2, REQ-0044.1) |
| `resize-mode` | `layout` \| `default` | Optional opt-in switch for layout-resize behavior; `resize-mode=layout` enables the new path, while omission or `default` keeps the existing scale-on-resize behavior (REQ-0044) |
| `rotate` | degrees 0–360 | Clockwise rotation around object center; same transform rules as REQ-0017 (REQ-0037) |

**Sizing paths:**

- **Default path:** Render the object body against its template-local geometry, then apply the existing scale-on-resize behavior when instance `width`/`height` overrides are used. In this path, `width`/`height` still take precedence over `scale` with a warning.
- **Layout-resize path:** Bind the instance `width`/`height` into the object-local layout context before executing the body, do not implicitly scale authored child geometry, and allow expressions based on object-local dimensions or bbox-derived values to reflow content.
- **Explicit scale in layout-resize path:** If `scale` is also present, apply it as a separate geometric transform after layout resolution rather than treating it as conflicting with `width`/`height`.

#### 3.3.8 Function Call Executor

**Responsibility:** Look up function declarations from the symbol table; bind positional arguments to parameter names; evaluate arithmetic expressions; execute body drawing commands; detect and reject recursion.

**REQ:** REQ-0015, REQ-0015.1, REQ-0015.2, REQ-0015.3

Supported expression operators: `+`, `-`, `*`, `/`. Unary minus is not supported. Division by zero at call time = runtime error. (REQ-0015.3)

#### 3.3.9 Grid System

**Responsibility:** Process the optional `grid()` frame-level statement; resolve per-element and global snap positions before passing coordinates to the Transform Applier; optionally render grid lines after all other primitives.

**REQ:** REQ-0038, REQ-0038.1, REQ-0038.2, REQ-0038.3, REQ-0038.4

**Grid model attributes:**

| Attribute | Type | Default | Notes |
|---|---|---|---|
| `step-x` | length | — | Horizontal grid spacing (required) |
| `step-y` | length | — | Vertical grid spacing (required) |
| `offset-x` | length | `0` | Grid origin horizontal shift |
| `offset-y` | length | `0` | Grid origin vertical shift |
| `render` | bool | `false` | When `true`, draws grid lines over canvas after all other primitives |
| `color` | color | `RGB(200,200,200)` | Grid line color; required when `render=true`; defaults to gray with warning if omitted |
| `line-type` | enum | `solid` | Grid line style: solid, dashed, dotted, dash-dot |
| `line-width` | length | `1px` | Grid line stroke width |
| `align` | bool | `false` | When `true`, globally snaps all elements to nearest grid intersection |

**Processing steps:**

| Step | Action | REQ |
|---|---|---|
| 1. Parse | Read `grid()` statement; validate `step-x` > 0 and `step-y` > 0; enforce at most one `grid` per frame | REQ-0038 |
| 2. Snap resolution | For each drawing command: if global `align=true` or per-element `snap=<mode>`, compute snapped position before coordinates are passed to Transform Applier; `snap=none` overrides global `align=true` for that element | REQ-0038.2, REQ-0038.3, REQ-0038.4 |
| 3. Grid render | If `render=true`, after all primitives are drawn, draw horizontal and vertical lines across the full canvas using configured style | REQ-0038.1 |

**Snap mode semantics:**

| Mode | Behaviour |
|---|---|
| `grid-intersection` | Snap both x and y to nearest grid intersection |
| `grid-x` | Snap only x to nearest vertical grid line; y unchanged |
| `grid-y` | Snap only y to nearest horizontal grid line; x unchanged |
| `none` | Per-element opt-out; overrides global `align=true` for that element |

**New modules:**

| Module | Responsibility |
|---|---|
| `imagegen/rendering/grid_resolver.py` | Pure function `snap_position(x, y, grid, mode)` — computes snapped coordinates |
| `imagegen/rendering/grid_renderer.py` | `render_grid(canvas, grid)` — draws grid lines via `ImageDraw.line()` when `render=true` |

#### 3.3.10 BBox Overlay Renderer

**Responsibility:** After each element is rendered and its transforms applied, check if `show-bbox=true` is set. If so, compute the axis-aligned bounding box (AABB) of the element's transformed pixel extents, sample the average background luminance in that region, and draw a dashed 1px overlay rectangle using a contrast-aware color derived from inverted luminance.

**REQ:** REQ-0039, REQ-0039.1, REQ-0039.2, REQ-0039.3, REQ-0039.4, REQ-0039.5, REQ-0039.6

**Processing steps:**

| Step | Action | REQ |
|---|---|---|
| 1. Check flag | If `show-bbox=false` or omitted, skip entirely — output is unchanged | REQ-0039, REQ-0039.6 |
| 2. Compute AABB | Derive the axis-aligned bounding box from all transformed vertices / pixel extents of the element (post-Transform Applier) | REQ-0039.1 |
| 3. Sample luminance | Read the average luminance of the canvas pixels within the AABB region (from the canvas state after the element is drawn) | REQ-0039.3 |
| 4. Compute color | Invert sampled luminance: `bbox_luminance = 255 − avg_luminance`; use as greyscale bbox color for maximum contrast | REQ-0039.3 |
| 5. Draw overlay | Draw the AABB as a dashed, 1px-wide rectangle in the computed color; drawn after the element, always on top | REQ-0039.2, REQ-0039.4 |

**Applicability table:**

| Drawable Element | AABB Derivation |
|---|---|
| `line` | AABB enclosing the stroke between transformed start and end points |
| `circle` | AABB of the bounding square of the (scaled/rotated) ellipse |
| `square` | AABB of the four transformed corner points |
| `polygon` | AABB of all transformed vertex points |
| `path` | AABB of all transformed control points |
| `pie` / `arc` | AABB of the enclosing sector / arc arc segment |
| `connector` | AABB of all transformed route points including caps |
| `font` / text | AABB of the rendered text pixel extents |
| `image` primitive | AABB of the placed / scaled / rotated image pixel extents |
| Object instance | AABB of the entire rendered object (all children included) |

**Notes:**
- The BBox Overlay Renderer operates independently per element; rendering order is: draw element → compute AABB → draw bbox overlay → proceed to next element.
- The bbox overlay is drawn before the Grid Renderer post-process step so that grid lines appear on top of debug overlays.
- No new DSL keyword or separate statement is required; `show-bbox` is a named parameter on existing drawable elements.

#### 3.3.11 Variable Store and Bbox Extractor

**Responsibility:** Maintain a scoped variable namespace for each frame and function execution context; process `var` declarations and bbox assignment statements; make variable values available for expression evaluation in subsequent drawing commands.

**REQ:** REQ-0041, REQ-0041.1, REQ-0041.2, REQ-0041.3, REQ-0041.4, REQ-0041.5

**Variable Store structure (per frame / per function call):**

```python
variable_store = {
    "frame:<frame_name>": { var_name → value | None },
    "func:<func_name>:<call_id>": { var_name → value | None },
}
```

Frame-scope and function-scope stores are independent; a variable declared in a frame is not visible inside a function called from that frame and vice versa.

**Processing steps:**

| Step | Action | REQ |
|---|---|---|
| 1. `var` declaration | On `var x, y;` — allocate entries in the current scope store, initialized to `None` (unassigned) | REQ-0041 |
| 2. Element render | Execute the drawing command normally via the Primitive Dispatcher / Object Instantiator / Function Executor | REQ-0041.4 |
| 3. Bbox computation | After the element is rendered, compute its post-transform AABB (same algorithm as BBox Overlay Renderer, §3.3.10) and cache the result keyed by element reference name | REQ-0041.1 |
| 4. Assignment statement | On `bx = rect1.bbox.x;` — look up `rect1` in the bbox cache; if absent (not yet rendered) raise a runtime error; store the property value into the current scope store under `bx` | REQ-0041.2 |
| 5. Expression resolution | When evaluating any parameter expression, resolve variable references from the current scope store; if a variable is unassigned (`None`), raise a runtime error | REQ-0041.3 |

**Error conditions:**

| Condition | Error type | REQ |
|---|---|---|
| `var` name conflicts with existing function / object name | Parse error | REQ-0041 |
| Assignment to name not declared with `var` | Parse error | REQ-0041.2 |
| `<name>.bbox.<prop>` before element rendered | Runtime error (file:line, element name) | REQ-0041.1, REQ-0041.5 |
| Using an undeclared or unassigned variable in expression | Parse or runtime error | REQ-0041.3, REQ-0041.5 |
| Circular variable dependency detected | Runtime error | REQ-0041.5 |

**New module:** `imagegen/rendering/variable_store.py`

Provides:
- `VariableStore` class with `declare(name)`, `assign(name, value)`, `resolve(name)` methods
- `BboxCache` class with `store(element_name, aabb)` and `get(element_name, prop)` methods

**Expression evaluator extension:** The existing arithmetic expression evaluator (used in Function Call Executor, §3.3.8) is extended to resolve `<name>` tokens against the current `VariableStore` in addition to the function parameter bindings.

---

#### 3.3.12 Comparison Evaluator and Loop Executor

**Responsibility:** Parse numeric comparison conditions and execute bounded `do ... while` loops in frame and function bodies.

**REQ:** REQ-0042, REQ-0042.1, REQ-0042.2, REQ-0043, REQ-0043.1, REQ-0043.2, REQ-0043.3, REQ-0043.5

| Responsibility | Design | REQ |
|---|---|---|
| Parse comparison conditions | Extend the parser with a `ComparisonExpr` node that stores `left-expr`, `operator`, and `right-expr` after ordinary arithmetic parsing completes | REQ-0042, REQ-0042.2 |
| Restrict loop placement | Permit `DoWhileStmt` nodes only in frame and function command lists; raise a parse error if encountered at top level or inside object/palette bodies | REQ-0043.1 |
| Execute loop body | Reuse the existing sequential statement dispatcher so loop bodies can run the same allowed statements as ordinary frame/function bodies | REQ-0043, REQ-0043.2 |
| Evaluate the condition after each body execution | Resolve both arithmetic sides against the current variable store and function bindings, then apply the comparison operator; continue only while the condition remains true | REQ-0042.1, REQ-0043 |
| Guard against infinite loops | Maintain an iteration counter per loop node and raise a runtime error once the count exceeds 1000 | REQ-0043.3 |
| Preserve old behavior | Keep arithmetic parameter evaluation unchanged outside loop-condition parsing so existing scripts remain unaffected | REQ-0043.5 |

**Parser / AST changes:**

| Artifact | Change |
|---|---|
| Lexer | Reserve `do` and `while` as keywords |
| AST | Add `ComparisonExpr` and `DoWhileStmt` nodes with source file and line metadata |
| Parser | Parse `do <body> while <comparison-expr>;` only in frame/function statement lists |
| Validator | Reject malformed comparisons, unsupported operators, and loops placed outside valid scopes |

**Runtime guard behavior:**

Expose a fixed engine-level constant such as `MAX_DO_WHILE_ITERATIONS = 1000`. When exceeded, the loop executor raises:

```text
<file>:<line>: error: do-while loop exceeded maximum iteration count 1000
```

The reported source location is the loop statement itself, not the last statement in the loop body.

---

### 3.4 Output Formatter

**Responsibility:** Collect rendered frame buffers and write output file(s) according to `output-format` and colorspace.

**REQ:** REQ-0027, REQ-0029

| Format | Trigger | Output | Notes |
|---|---|---|---|
| `png` | single frame or explicit | `<script-name>.png` | Supports RGBA, RGB, GRAY |
| `jpeg` | single frame explicit | `<script-name>.jpeg` | RGB only; RGBA = validation error |
| `gif` | multi-frame default | `<script-name>.gif` | Animated; `hold-time` per frame; loop from first frame's `frame-mode` |
| `images` | explicit | `<frame-id>.png` or `<frame-id>.jpeg` | RGBA/GRAY → always `.png`; RGB → `.jpeg`; duplicate frame-id = silent overwrite |

---

### 3.5 Error Reporter

**Responsibility:** Format and emit all parse, validation, and runtime errors to stderr. All messages include file name and line number.

**REQ:** REQ-0031, REQ-0025

Message format:
```
<file>:<line>: error: <description>
<file>:<line>: warning: <description>
```

Error categories and behaviour:

| Category | Action |
|---|---|
| Parse error | Halt immediately; no output produced |
| Validation error | Halt immediately; no output produced |
| Semantic error (e.g., `color=none` on stroke) | Halt immediately |
| Warning (e.g., conflicting `output-format`, identical gradient endpoints) | Log to stderr; continue execution |
| Runtime error (division by zero, recursion) | Halt immediately |

---

### 3.6 Font Discovery Command

**Responsibility:** Enumerate all fonts installed on the host system, inspect each for available style variants, scalability, and Hungarian glyph coverage, and write a structured report to stdout.

**REQ:** REQ-0034, REQ-0034.1, REQ-0034.2, REQ-0034.3, REQ-0034.4

**Module:** `font_discovery.py` (new module, invoked from the CLI entry point when `--list-fonts` is passed)

#### Processing Steps

| Step | Action | REQ |
|---|---|---|
| 1. Enumerate | Discover all installed font files via `matplotlib.font_manager.FontManager().ttflist` (cross-platform) | REQ-0034 |
| 2. Group | Group `FontEntry` objects by family name; the `.name` attribute is the DSL-usable `font-family` string | REQ-0034.1 |
| 3. Detect styles | Map `(style, weight)` → `normal` / `bold` / `italic` / `bold-italic`; report only variants with a file on disk | REQ-0034.2 |
| 4. Classify size | Inspect representative font file via `fonttools.ttLib.TTFont`; if `EBLC`/`CBLC` table present → list pixel sizes; else → `scalable` | REQ-0034.3 |
| 5. Check Hungarian | Load `cmap` table; verify all 18 code points present in at least one variant file | REQ-0034.4 |
| 6. Output | Print one block per family to stdout in alphabetical order (case-insensitive); blank line between entries | REQ-0034 |

#### Output Format

```
Font: Arial
  DSL name : Arial
  Styles   : normal, bold, italic, bold-italic
  Sizes    : scalable
  Hungarian: yes
```

#### Required Code Points (Hungarian Check)

Á (U+00C1), á (U+00E1), É (U+00C9), é (U+00E9), Í (U+00CD), í (U+00ED), Ó (U+00D3), ó (U+00F3), Ö (U+00D6), ö (U+00F6), Ő (U+0150), ő (U+0151), Ú (U+00DA), ú (U+00FA), Ü (U+00DC), ü (U+00FC), Ű (U+0170), ű (U+0171)

---

## 4. Data Flow

### 4.1 Single-Frame Script

```
input.dsl
    │
    ▼
[Lexer / Parser]
    │  AST
    ▼
[Pass 1 — Resolver]
    │  symbol table (obj + func defs, resolved includes)
    ▼
[Pass 2 — Frame Executor]
    │  validated drawing command list
    ▼
[Canvas Factory]  →  blank image buffer (w × h, colorspace)
    │
    ▼
[Background Renderer]  →  fills canvas
    │
    ▼
[Primitive Dispatcher]  →  sorts by z-index, dispatches each command
    │  (line, circle, square, polygon, path, pie, arc,
    │   connector, font, image primitives)
    ▼
[Transform Applier]  →  applies per-primitive transforms
    │
    ▼
[Output Formatter]  →  encodes final buffer
    │
    ▼
output.png / output.jpeg
```

### 4.2 Multi-Frame Script (Animated GIF)

```
input.dsl  (N begin_frame blocks)
    │
    ▼
[Pass 1 — Resolver]
    │
    ▼
[Pass 2 — Frame Executor]  (iterates frames 0 … N-1)
    │
    ├── Frame 0 → render → frame buffer 0  (hold-time, frame-mode)
    ├── Frame 1 → render → frame buffer 1  (hold-time)
    │   ...
    └── Frame N → render → frame buffer N  (hold-time)
    │
    ▼
[GIF Assembler]
    │  apply hold-time per frame; set loop from first frame's frame-mode
    ▼
output.gif
```

### 4.3 Script with Includes

```
main.dsl
    ├── include "lib/shapes.dsl"
    │       └── include "lib/colors.dsl"   (nested OK, no depth limit)
    └── include "lib/buttons.dsl"

[Pass 1 — Include Resolver]
    │  loads all files; checks for circular includes
    │  merges all begin_obj / begin_func into symbol table
    │  frame blocks inside included files → ignored
    ▼
[Symbol Table]
    obj-table:  { icon_circle, primary_button, ... }
    func-table: { badge, draw_grid, ... }
    │
    ▼
[Pass 2 — Frame Executor]
    │  references resolved from merged symbol table
    ▼
output
```

---

## 5. Storage Design

The system has no persistent database or network storage. All I/O is file-based.

### 5.1 Input Files

| File type | Role | Notes |
|---|---|---|
| `.dsl` (main script) | Primary input | Read with **explicit UTF-8** encoding; BOM stripped if present; non-UTF-8 bytes → I/O error with file path and byte position (REQ-0035, REQ-0035.1) |
| `.dsl` (library files) | Imported via `include` | Same UTF-8 encoding rules as main script; relative paths resolved from including file's directory (REQ-0016.1, REQ-0035) |
| `.png`, `.jpeg`, `.gif`, `.svg` | External image assets | Referenced in `background(src=...)` or `image(src=...)`; relative to DSL file (REQ-0032) |

### 5.2 Output Files

| Format | Condition | File name |
|---|---|---|
| `.png` | `output-format=png` (single) or RGBA/GRAY in `images` mode | `<script-name>.png` or `<frame-id>.png` |
| `.jpeg` | `output-format=jpeg` (single) or RGB in `images` mode | `<script-name>.jpeg` or `<frame-id>.jpeg` |
| `.gif` | `output-format=gif` or multi-frame default | `<script-name>.gif` |

Output is written to the **same directory as the input `.dsl` file** unless an explicit output path is supplied on the CLI.

### 5.3 In-Memory Data Structures

| Structure | Description |
|---|---|
| **AST** | Tree of parsed tokens from the DSL source; discarded after rendering |
| **Symbol Table** | Flat dict of object templates and function declarations; populated in Pass 1 |
| **Frame Buffer** | Per-frame in-memory RGBA/RGB/GRAY pixel array (Pillow `Image` object); discarded after encoding |
| **GIF Frame List** | Ordered list of encoded frame buffers held in memory until final GIF assembly |

---

## 6. API Definition (CLI)

The system exposes a single public interface: the command-line.

**REQ:** REQ-0030, REQ-0031

### 6.1 Invocation Syntax

**Standard image generation:**
```
python imagegen.py <input-file> [output-path]
```

**Font discovery:**
```
python imagegen.py --list-fonts
```

| Argument / Flag | Required | Description |
|---|---|---|
| `<input-file>` | Yes (without `--list-fonts`) | Path to the `.dsl` script file to process |
| `[output-path]` | No | Override for output file (single-output formats) or directory (`images` mode) |
| `--list-fonts` | No | Enumerate all system fonts and exit; mutually exclusive with `<input-file>` |

### 6.2 Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success — all output files written |
| `1` | Parse error or validation error — no output produced |
| `2` | Runtime error (e.g., division by zero, recursion) |
| `3` | I/O error (input file not found, output directory not writable, asset not found) |

### 6.3 Stdout / Stderr

| Stream | Content |
|---|---|
| `stdout` | Empty on success |
| `stderr` | Error and warning messages, each prefixed with `<file>:<line>: error:` or `<file>:<line>: warning:` |

### 6.4 Error Message Format

**REQ:** REQ-0031

```
<file>:<line>: error: <primitive>: <description>
<file>:<line>: warning: <description>
```

Examples:
```
main.dsl:12: error: circle: duplicate parameter 'color'
main.dsl:8: error: arc: 'fill' parameter is not supported on arc
main.dsl:5: warning: output-format 'jpeg' ignored; using 'png' from first frame 'intro'
lib/shapes.dsl:3: error: 'icon_circle' is already defined
```

---

## 7. External Integrations

The system depends on the following Python libraries. All are resolved at import time; no network calls are made during execution.

**REQ:** REQ-0026 (Python implementation)

### 7.1 Image Rendering — Pillow (PIL)

| Capability | Pillow API Used | REQ |
|---|---|---|
| Canvas creation (RGB / RGBA / GRAY) | `Image.new(mode, size)` | REQ-0003, REQ-0002.3 |
| Solid background | `ImageDraw.rectangle()` full canvas | REQ-0004.1 |
| Gradient background | Manual pixel computation or `ImageDraw` | REQ-0004.2 |
| Image background / primitive | `Image.open()`, `Image.paste()`, resize | REQ-0004.3, REQ-0013 |
| Line, arc, polygon, ellipse | `ImageDraw.line/arc/polygon/ellipse` | REQ-0005–REQ-0010 |
| Pie slice | `ImageDraw.pieslice()` | REQ-0010 |
| Text rendering | `ImageDraw.text()` with `ImageFont` | REQ-0012 |
| PNG / JPEG write | `Image.save(format='PNG'/'JPEG')` | REQ-0027 |
| Animated GIF assembly | `Image.save(format='GIF', save_all=True, append_images=[...], loop=...)` | REQ-0001.2, REQ-0002.2 |
| Greyscale conversion (CCIR 601) | `Image.convert('L')` | REQ-0020.1 |

### 7.2 Font Rendering — Pillow + FreeType

| Capability | Mechanism | REQ |
|---|---|---|
| Named font resolution with fallback chain | `ImageFont.truetype()` called for each name in the chain | REQ-0012 |
| System generic families (`serif`, `sans-serif`, `monospace`) | Platform font discovery or bundled fallback font | REQ-0012 |
| Final fallback (system monospace) | Pillow built-in bitmap font via `ImageFont.load_default()` | REQ-0012 |
| Multi-line text | Manual newline split; repeated `ImageDraw.text()` calls at `font-size × 1.2` spacing | REQ-0012 |

### 7.3 SVG Rendering (Image Primitive)

SVG files referenced by `image(src=...)` or `background(src=...)` require rasterisation before compositing.

**REQ:** REQ-0013, REQ-0032

| Option | Notes |
|---|---|
| **cairosvg** | Preferred; pure Python binding; converts SVG to PNG in-memory |
| **svglib + reportlab** | Alternative; wider compatibility |

If no SVG library is available, loading an SVG asset produces a descriptive error.

### 7.4 Standard Library Modules

| Module | Usage |
|---|---|
| `argparse` | CLI argument parsing (REQ-0030) |
| `os`, `pathlib` | File path resolution, include path normalisation (REQ-0016.1) |
| `sys` | Exit codes, stderr output |
| `math` | Angle normalisation, coordinate transforms |
| `re` | Tokeniser regex patterns |
| `copy` | Deep-copy of object template attribute dicts for instance overrides |

### 7.5 Font Discovery — matplotlib + fonttools

Required for the `--list-fonts` command (Section 3.6, REQ-0034–REQ-0034.4).

| Capability | Library | Usage |
|---|---|---|
| Font file discovery (cross-platform) | `matplotlib.font_manager` | `FontManager().ttflist` returns all installed font paths and metadata |
| Font metadata (family, subfamily) | `fonttools.ttLib.TTFont` | Reads `name` table (nameID 1 = family name, nameID 2 = subfamily/style) |
| Bitmap size detection | `fonttools.ttLib.TTFont` | Presence of `EBLC`/`CBLC` table indicates bitmap font; `strikes` list gives pixel sizes |
| Hungarian glyph check | `fonttools.ttLib.TTFont` | `getBestCmap()` returns Unicode → glyph mapping; check all 18 required code points |

**New pip dependency:** `fonttools >= 4.0`  
Add to `requirements.txt` if not already present: `matplotlib >= 3.5` and `fonttools >= 4.0`.

---

## 8. Error Handling Strategy

**REQ:** REQ-0025, REQ-0025.1, REQ-0031

### 8.1 Error Classification

| Class | When raised | Execution |
|---|---|---|
| **Parse error** | Malformed syntax, unknown keyword, duplicate parameter key, `fill` on `arc` | Halt immediately |
| **Validation error** | Invalid color format, negative radius/width, insufficient points, negative scale, `color=none` on stroke, `clip-shape=polygon`, JPEG + RGBA | Halt immediately |
| **Semantic error** | `color=none` on stroke property | Halt immediately |
| **Runtime error** | Division by zero in expression, recursion detected | Halt during frame execution |
| **I/O error** | Missing include file, unreadable asset, unwritable output, non-UTF-8 byte sequence in DSL source (REQ-0035) | Halt immediately; error includes file path and byte position |
| **Warning** | Conflicting `output-format`, conflicting `colorspace`, identical gradient endpoints, duplicate frame-id in `images` mode | Log to stderr; continue |

### 8.2 Coordinate Clipping

Primitives positioned partially or fully outside the canvas bounds are silently clipped to the canvas rectangle — no error is raised. (REQ-0025)

### 8.3 Circular Include Detection

Detected in Pass 1 by maintaining a set of currently-being-resolved file paths. A file that appears in its own resolution chain triggers a parse error before any rendering begins. (REQ-0016.2)

---

## 9. Requirements Traceability

| Component / Section | REQ IDs |
|---|---|
| CLI Entry Point | REQ-0030, REQ-0031 |
| Engine Orchestrator (two-pass) | REQ-0001, REQ-0028 |
| Include Resolver | REQ-0016, REQ-0016.1, REQ-0016.2 |
| Symbol Collector | REQ-0014, REQ-0015 |
| Lexer / Parser | REQ-0028, REQ-0023, REQ-0024 |
| Semantic Validator | REQ-0025, REQ-0025.1 |
| Frame Runner | REQ-0002, REQ-0002.1, REQ-0002.2, REQ-0002.3 |
| Canvas Factory | REQ-0003, REQ-0004.4 |
| Background Renderer | REQ-0004.1, REQ-0004.2, REQ-0004.3 |
| Primitive Dispatcher | REQ-0018, REQ-0019 |
| Line Renderer | REQ-0005, REQ-0022 |
| Circle Renderer | REQ-0006, REQ-0020, REQ-0021 |
| Square Renderer | REQ-0007, REQ-0020, REQ-0021 |
| Polygon Renderer | REQ-0008, REQ-0020, REQ-0021 |
| Path Renderer | REQ-0009, REQ-0020, REQ-0021 |
| Pie Renderer | REQ-0010, REQ-0020 |
| Arc Renderer | REQ-0010.1, REQ-0020 |
| Connector Renderer | REQ-0011, REQ-0011.1–REQ-0011.9 |
| Font / Text Renderer | REQ-0012, REQ-0020, REQ-0021, REQ-0023 |
| Image Primitive | REQ-0013, REQ-0032 |
| Transform Applier | REQ-0017 |
| Object Template Instantiator | REQ-0014, REQ-0014.1–REQ-0014.4, REQ-0036, REQ-0036.1, REQ-0036.2, REQ-0037 |
| Function Call Executor | REQ-0015, REQ-0015.1–REQ-0015.3 |
| Output Formatter | REQ-0001.1, REQ-0001.2, REQ-0027, REQ-0029 |
| Error Reporter | REQ-0025, REQ-0031 |
| Color System | REQ-0020, REQ-0020.1, REQ-0040.2 |
| Color Palette Support (Pass 1 + Semantic Validator) | REQ-0040, REQ-0040.1, REQ-0040.2, REQ-0040.3, REQ-0040.4, REQ-0040.5, REQ-0040.6 |
| Unit System | REQ-0021 |
| External image assets | REQ-0032, REQ-0033 |
| Font Discovery Command | REQ-0034, REQ-0034.1, REQ-0034.2, REQ-0034.3, REQ-0034.4 |
| Encoding (Lexer / Resolver) | REQ-0035, REQ-0035.1 |
| Grid System | REQ-0038, REQ-0038.1, REQ-0038.2, REQ-0038.3, REQ-0038.4 |
| BBox Overlay Renderer | REQ-0039, REQ-0039.1, REQ-0039.2, REQ-0039.3, REQ-0039.4, REQ-0039.5, REQ-0039.6 |
| Variable Store and Bbox Extractor | REQ-0041, REQ-0041.1, REQ-0041.2, REQ-0041.3, REQ-0041.4, REQ-0041.5 |
| Comparison Evaluator and Loop Executor | REQ-0042, REQ-0042.1, REQ-0042.2, REQ-0043, REQ-0043.1, REQ-0043.2, REQ-0043.3, REQ-0043.5 |

---

## Changelog

### 2026-05-02 08:12:13 — FEA-001: font discovery CLI command
- Added section 3.6 (Font Discovery Command): --list-fonts flag, font_discovery.py module design, output format, Hungarian code points table
- Updated section 6.1 (Invocation Syntax): added --list-fonts invocation form and mutual-exclusivity rule to argument table
- Added section 7.5 (matplotlib + fonttools): font discovery dependencies and API usage table
- Updated section 9 (Requirements Traceability): added Font Discovery Command row covering REQ-0034 through REQ-0034.4
- File version 1.0 → 1.1

### 2026-05-02 17:30:45 — FEA-002: UTF-8 encoding fix
- Updated section 3.2 (Lexer / Parser table): added UTF-8 encoding, BOM strip, DslIOError on decode failure; added REQ-0035 and REQ-0035.1 references
- Updated section 5.1 (Input Files): clarified explicit UTF-8 enforcement and BOM handling for all DSL files
- Updated section 8.1 (Error Classification): expanded I/O error row to cover non-UTF-8 byte sequences with file path and byte position
- Updated section 9 (Requirements Traceability): added Encoding row for REQ-0035 and REQ-0035.1
- File version 1.1 → 1.2

### 2026-05-02 18:59:02 — FEA-003: optional size and rotation parameters for DSL objects
- Updated section 3.3.7 (Object Template Instantiator): added REQ coverage for REQ-0036–REQ-0037;
  added instance-time size and rotation parameters table (width, height, scale, rotate)
- Updated section 9 (Requirements Traceability): expanded Object Template Instantiator row
  to include REQ-0036, REQ-0036.1, REQ-0036.2, REQ-0037
- File version 1.2 → 1.3

### 2026-05-03 09:47:19 — FEA-005: optional bounding box rendering
- Updated architecture diagram: added BBox Overlay Renderer step between Transform/Object/Function executors and Grid Renderer
- Added section 3.3.10 (BBox Overlay Renderer): processing steps table, per-element AABB derivation table, and design notes
- Updated section 9 (Requirements Traceability): added BBox Overlay Renderer row covering REQ-0039 through REQ-0039.6
- File version 1.4 → 1.5

### 2026-05-02 19:57:13 — FEA-004: configurable grid system
- Updated architecture diagram: added Grid Resolver between Background Renderer and Primitive Dispatcher;
  added Grid Renderer post-process step after Function Call Executor
- Added section 3.3.9 (Grid System): grid model attributes table, processing steps, snap mode semantics,
  new module list (grid_resolver.py, grid_renderer.py)
- Updated section 9 (Requirements Traceability): added Grid System row covering REQ-0038–REQ-0038.4
- File version 1.3 → 1.4

### 2026-05-03 20:46:05 — FEA-006: named color palette support
- Updated Pass 1 Symbol Collector table (section 3.2): added Palette Collector row covering begin_palette/end_palette collection and alias deduplication
- Updated global symbol table structure: added `"palettes": { alias → ColorValue }` entry
- Updated namespace note: duplicate detection now explicitly covers palette alias names
- Updated Pass 2 Semantic Validator row: added @alias resolution and undefined-alias error reporting
- Updated section 9 (Requirements Traceability): extended Color System row; added Color Palette Support row covering REQ-0040 through REQ-0040.6
- File version 1.5 → 1.6

### 2026-05-04 18:12:00 — FEA-007: variable support and bounding box extraction
- Updated architecture diagram: added Variable Store / Bbox Extractor step between Function Call Executor and BBox Overlay Renderer
- Added section 3.3.11 (Variable Store and Bbox Extractor): scope model, processing steps table, error conditions table, new module `variable_store.py`, expression evaluator extension note
- Updated section 9 (Requirements Traceability): added Variable Store and Bbox Extractor row covering REQ-0041 through REQ-0041.5
- File version 1.6 → 1.7


### 2026-05-07 21:04:48 - FEA-008: comparison expressions and bounded do ... while
- Added section 3.3.12 (Comparison Evaluator and Loop Executor): parser/AST changes, loop placement rules, sequential execution reuse, and fixed-guard runtime error behavior
- Updated section 9 (Requirements Traceability): added Comparison Evaluator and Loop Executor row covering REQ-0042 through REQ-0043.5
- File version 1.7 -> 1.8

### 2026-05-09 06:44:42 - FEA-009: decoupled object resizing and scaling behavior
- Updated section 3.3.7 (Object Template Instantiator) with separate default resize-scaling and opt-in layout-resize execution paths
- Added explicit mode-flag handling notes and clarified that `scale` remains available in layout-resize mode
- Extended requirements coverage in the object-instantiation design to include REQ-0044 through REQ-0044.3
- File version 1.8 -> 1.9
