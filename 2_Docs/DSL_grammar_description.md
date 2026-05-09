# DSL Grammar Description — Technical Image Generator

| Field | Value |
|---|---|
| **Description** | Complete formal grammar and reference for the Technical Image Generator DSL |
| **Created at** | 2026-04-25 10:10:16 |
| **File version** | 3.6 |
| **Created by** | Claude Sonnet 4.6 |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Lexical Conventions](#2-lexical-conventions)
3. [Formal Grammar (EBNF)](#3-formal-grammar-ebnf)
4. [Top-Level Structure](#4-top-level-structure)
5. [Frame Definition](#5-frame-definition)
6. [Image Canvas Statement](#6-image-canvas-statement)
7. [Background Statement](#7-background-statement)
8. [Drawing Primitives](#8-drawing-primitives)
9. [Connector Primitive](#9-connector-primitive)
10. [Font / Text Primitive](#10-font--text-primitive)
11. [Image Primitive](#11-image-primitive)
12. [Object Templates](#12-object-templates)
13. [Function Declarations and Calls](#13-function-declarations-and-calls)
14. [Variable Support and Bounding Box Extraction](#14-variable-support-and-bounding-box-extraction)
15. [Include Statement](#15-include-statement)
16. [Data Types and Value Formats](#16-data-types-and-value-formats)
17. [Parameter Reference Tables](#17-parameter-reference-tables)
18. [Complete Annotated Examples](#18-complete-annotated-examples)
19. [Error Reference](#19-error-reference)

---

## 1. Overview

The Technical Image Generator DSL (Domain-Specific Language) is a text-based scripting language that describes technical images and animations. A DSL script is processed by the image generator engine to produce one or more image files in PNG, JPEG, or animated GIF format.

### Design Principles

- **Frame-based**: every image is defined inside a `begin_frame` / `end_frame` block.
- **Declarative**: the script describes *what* to draw; the engine handles *how*.
- **Named parameters**: all primitive and attribute parameters are named (key=value) and order-independent.
- **Composable**: object templates and function declarations enable reuse and composition.
- **Extensible**: `include` allows library files to be imported into any script.

### File Extension

DSL script files use the `.dsl` extension.

---

## 2. Lexical Conventions

### 2.1 Character Encoding

All DSL source files are **UTF-8** encoded. Non-ASCII characters are permitted inside string literals and comments.

### 2.2 Whitespace

Whitespace (space `U+0020`, horizontal tab `U+0009`) is **insignificant** except:
- It separates adjacent tokens.
- Inside string literals, whitespace is preserved literally.

Blank lines are ignored.

### 2.3 Comments

Single-line comments begin with `#` and extend to the end of the line.

```
# This is a comment
circle(color=black, radius=10)  # inline comment
```

Block comments are **not** supported.

> **`#` token disambiguation:** The `#` character is context-sensitive. When the tokeniser is in a value-position context (after `=` in a named parameter or after `(` in an argument list), `#` followed by exactly 6 hexadecimal digits is tokenised as the start of a `<color>` hex token. In any other position — start of a statement, or `#` not followed by exactly 6 hex digits — `#` begins a single-line comment.

### 2.4 Statement Terminators

Inside frame, object, and function bodies, statements are terminated by:
- A **newline** character (`\n`), or
- A **semicolon** (`;`).

Both styles may be freely mixed on the same line:

```
image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
```

### 2.5 Identifiers

Identifiers name frames, objects, functions, and parameters.

```
identifier  ::=  [A-Za-z_][A-Za-z0-9_-]*
```

Examples: `my_frame`, `card`, `btn`, `font-size`, `start-cap`.

> **Disambiguation in arithmetic expressions:** Inside `begin_func` bodies (§13.3), a hyphen is treated as part of an identifier token only when it is **not preceded by whitespace** (maximal-munch rule). To express subtraction, surround `-` with spaces: `width - 10` is subtraction; `line-width` is a single identifier. See §13.3 for details.

### 2.6 String Literals

Strings are enclosed in **double quotes**. Supported escape sequences:

| Escape | Meaning |
|---|---|
| `\"` | Literal double-quote character |
| `\\` | Literal backslash character |
| `\n` | Newline |
| `\t` | Horizontal tab |

```
text="Hello, World!"
text="Line 1\nLine 2"
text="Say \"hello\""
```

### 2.7 Numeric Literals

Integer or decimal values, optionally followed by a **unit suffix**:

```
number   ::=  [0-9]+ ('.' [0-9]+)?
```

Valid unit suffixes: `px`, `pt`, `em`, `cm`, `mm`, `%`

Omitting a unit suffix defaults to **`px`** (pixels) for length values.

Angle values are always **degrees** (no unit suffix needed).

> **Angle parameters and unit suffixes:** The angle parameters `rotate`, `start-angle`, and `end-angle` must be supplied as plain numbers without a unit suffix. Providing a unit suffix (e.g., `rotate=45px`) is a validation error: `<file>:<line>: error: angle parameter '<key>' does not accept a unit suffix`.

### 2.8 Keywords

The following identifiers are **reserved** and may not be used as user-defined names:

```
begin_frame  end_frame
begin_obj    end_obj
begin_func   end_func
begin_palette  end_palette
include
image
background
var
line  circle  square  polygon  path  pie  arc  connector  font
```

> **`@` palette reference prefix:** The `@` character is a single-character token. When followed immediately by an identifier, it forms a palette alias reference (`@primary`, `@accent`). The `@` character is only valid in a value position (after `=` or inside `(`); in any other position it is a parse error.

> **`image` keyword disambiguation:** The token `image` is used for two syntactically distinct constructs. The parser distinguishes them by the character that immediately follows the token:
> - `image` **without** an opening parenthesis `(` → **canvas statement** (§6): `image width=... height=...`
> - `image` **followed by** `(` → **image drawing primitive** (§11): `image(src=..., pos=..., ...)`
>
> Both forms are unambiguous at the first lookahead character after the `image` token.

> **Case sensitivity:** All DSL keywords and named color tokens are **case-sensitive** and must be written in **lowercase** exactly as shown. For example, `begin_frame` is valid; `Begin_Frame` or `BEGIN_FRAME` are parse errors. User-defined identifiers (frame names, object names, function names, parameter names) are also case-sensitive.

---

## 3. Formal Grammar (EBNF)

> Notation:  
> `::=` definition  
> `|` alternation  
> `*` zero or more  
> `+` one or more  
> `?` optional (zero or one)  
> `{n}` exactly n repetitions  
> `( )` grouping  
> `[ ]` character class  
> `'...'` literal terminal  
> `< >` non-terminal  

```ebnf
(* ── Top-level ─────────────────────────────────────────── *)
<script>           ::= <top-level-stmt>+

<top-level-stmt>   ::= <frame>
                     | <func-decl>
                     | <obj-template>
                     | <include-stmt>
                     | <palette-def>

(* ── Include ─────────────────────────────────────────────  *)
<include-stmt>     ::= 'include' '"' <path> '"'
<path>             ::= <any-utf8-chars-except-double-quote>

(* ── Palette definitions ─────────────────────────────────  *)
<palette-def>      ::= 'begin_palette' <identifier>
                         (<color-entry> <terminator>?)*
                       'end_palette'

<color-entry>      ::= <identifier> '=' <color-literal>
  (* <color-literal> is any <color> form that is NOT a <palette-ref>:
     named-color, 'none', '#RRGGBB', RGB(), or RGBA().
     @alias refs are not permitted inside a palette body (parse error).
     An empty begin_palette / end_palette block is a parse error.
     Duplicate alias names across any loaded palette are a parse error. *)

(* ── Frame ────────────────────────────────────────────── *)
<frame>            ::= 'begin_frame' <identifier>
                         (<frame-attr> <terminator>?)*
                         <image-def>
                         (<frame-attr> <terminator>?)*
                         <drawing-commands>
                       'end_frame'

<frame-attr>       ::= 'hold-time' '=' <number>
                     | 'frame-mode' '=' ('one-run' | 'cyclic-run')
                     | 'colorspace' '=' ('RGB' | 'RGBA' | 'GRAY')

(* ── Image canvas ─────────────────────────────────────── *)
<image-def>        ::= 'image' <image-param> (<terminator> <image-param>)* <terminator>?
<image-param>      ::= 'width' '=' <length>
                     | 'height' '=' <length>
                     | 'colorspace' '=' ('RGB' | 'RGBA' | 'GRAY')
                     | 'dpi' '=' <number>
                     | 'output-format' '=' ('png' | 'jpeg' | 'gif' | 'images')

(* ── Drawing commands ─────────────────────────────────── *)
<drawing-commands> ::= (<drawing-stmt> <terminator>?)*
<drawing-stmt>     ::= <primitive>
                     | <background>
                     | <grid-stmt>          (* multiple per frame allowed; each replaces the active grid *)
                     | <object-inst>
                     | <func-call>
                     | <var-decl-stmt>      (* frame and func bodies only; not in obj bodies *)
                     | <assign-stmt>        (* frame and func bodies only *)
                     | <named-draw-cmd>     (* frame and func bodies only *)

(* ── Background ────────────────────────────────────────── *)
<background>       ::= 'background' '(' <background-params> ')'
<background-params>::= <named-param-list>
  (* Parameters are order-independent (named key=value). The engine
     distinguishes background forms by key presence:
       solid:    'color' present, no 'color1'/'color2'/'src'
       gradient: 'color1' and 'color2' present (also 'start', 'end')
       image:    'src' present
     Valid named parameters:
       solid    — color
       gradient — color1, color2, start, end
       image    — src, mode=(fit|stretch|clip), x, y, width, height, opacity *)

(* ── Grid statement ─────────────────────────────────────── *)
<grid-stmt>        ::= 'grid' '(' <named-param-list> ')'
  (* Named parameters (all order-independent):
       Required: step-x, step-y (both must be > 0)
       Optional: offset-x (default=0), offset-y (default=0),
                 render (boolean, default=false),
                 color (default=RGB(200,200,200); warning if omitted when render=true),
                 line-type (default=solid), line-width (default=1px),
                 align (boolean, default=false)
     Multiple grid() statements are allowed per frame; each one activates a new
     grid for the drawing commands that follow it (the previous grid is replaced).
     snap= or align=true on any primitive/object-inst requires at least one
     grid() to have been defined earlier in the same frame. *)

<snap-mode>        ::= 'grid-intersection' | 'grid-x' | 'grid-y' | 'none'
  (* Snap mode values are identifiers; validated semantically, not syntactically. *)

(* ── Primitives ────────────────────────────────────────── *)
<primitive>        ::= <line-prim>
                     | <circle-prim>
                     | <square-prim>
                     | <polygon-prim>
                     | <path-prim>
                     | <pie-prim>
                     | <arc-prim>
                     | <connector-prim>
                     | <font-prim>
                     | <image-prim>

<line-prim>        ::= 'line' '(' <named-param-list> ')'
<circle-prim>      ::= 'circle' '(' <named-param-list> ')'
<square-prim>      ::= 'square' '(' <named-param-list> ')'
<polygon-prim>     ::= 'polygon' '(' <named-param-list> ')'
<path-prim>        ::= 'path' '(' <named-param-list> ')'
<pie-prim>         ::= 'pie' '(' <named-param-list> ')'
<arc-prim>         ::= 'arc' '(' <named-param-list> ')'
<connector-prim>   ::= 'connector' '(' <named-param-list> ')'
<font-prim>        ::= 'font' '(' <named-param-list> ')'
<image-prim>       ::= 'image' '(' <named-param-list> ')'

(* ── Object templates ─────────────────────────────────── *)
<obj-template>     ::= 'begin_obj' <identifier>
                         (<obj-attr> <terminator>?)*
                         <drawing-commands>
                       'end_obj'

<obj-attr>         ::= 'width' ':' <length>
                     | 'height' ':' <length>
                     | 'background' ':' <color>
                     | 'border' ':' <border-value>
                     | 'shadow' ':' <shadow-value>
                     | 'clip-bounds' ':' '(' <length> ',' <length> ',' <length> ',' <length> ')'
                     | 'clip-shape' ':' <identifier>

<border-value>     ::= <line-type> <length> <color>
<shadow-value>     ::= <length> <length> <length> <color>

<object-inst>      ::= <identifier> '(' <named-param-list> ')'

(* ── Functions ─────────────────────────────────────────── *)
<func-decl>        ::= 'begin_func' <identifier> '(' <param-names> ')'
                         <drawing-commands>
                         (* Note: within a func body, <value>/<point>/<length> in named
                            params may be replaced by <expr>/<expr-point> (see below). *)
                       'end_func'

<param-names>      ::= <identifier> (',' <identifier>)*
                     | (* empty — zero-parameter function *)

<func-call>        ::= <identifier> '(' <arg-list> ')'
<arg-list>         ::= <value> (',' <value>)*
                     | (* empty — zero-argument call *)

(* ── Parameter list ────────────────────────────────────── *)
<named-param-list> ::= <named-param> (',' <named-param>)*
<named-param>      ::= <identifier> '=' <value>
(* Note: duplicate keys within one <named-param-list> (e.g. color=black, color=red)
   are a parse error: <file>:<line>: error: '<primitive>': duplicate parameter '<key>' *)

(* ── Value types ───────────────────────────────────────── *)
<value>            ::= <length>
                     | <color>
                     | <string>
                     | <point>
                     | <point-list>
                     | <boolean>
                     | <identifier>

<length>           ::= <number> <unit>?
<unit>             ::= 'px' | 'pt' | 'em' | 'cm' | 'mm' | '%'

<point>            ::= '(' <length> ',' <length> ')'

<point-list>       ::= '[' <point> (',' <point>)+ ']'

<boolean>          ::= 'true' | 'false'

(* ── String literal ───────────────────────────────────────── *)
(* A string is a double-quoted UTF-8 sequence (see §2.6 for escape rules). *)
<string>           ::= '"' <string-char>* '"'
<string-char>      ::= <any-UTF8-char-except-backslash-and-double-quote>
                     | '\\' ('"' | '\\' | 'n' | 't')

(* ── Arithmetic expressions (frame and function bodies) ─── *)
(* Within both begin_frame … end_frame and begin_func … end_func bodies,
   <value> alternatives that resolve to <length> or <point> in named
   parameters are generalised to <expr> and <expr-point> respectively.
   In frame bodies, <identifier> refers to a declared frame variable (§14).
   In function bodies, <identifier> refers to a declared function parameter.
   Object-template bodies do not support arithmetic expressions — all numeric
   values must be plain <length> literals. *)
<expr>             ::= <expr-term> (('+' | '-') <expr-term>)*
<expr-term>        ::= <expr-factor> (('*' | '/') <expr-factor>)*
<expr-factor>      ::= <length>
                     | <identifier>            (* declared variable or function parameter *)
                     | <bbox-access>           (* named-primitive bounding box property *)
                     | '(' <expr> ')'
<expr-point>       ::= '(' <expr> ',' <expr> ')'

(* ── Variable and bbox statements (frame and func bodies, FEA-007) ── *)
<var-decl-stmt>    ::= 'var' <identifier> (',' <identifier>)* ';'
  (* Declares one or more numeric variables. Must be declared before assignment
     or reference. Not permitted inside begin_obj bodies — parse error. *)

<assign-stmt>      ::= <identifier> '=' <expr> ';'
  (* The target <identifier> must name a previously declared variable.
     Using an undeclared identifier is a runtime error. *)

<named-draw-cmd>   ::= <identifier> '=' <primitive-call> ';'
  (* Renders the primitive and binds it to a name for subsequent <bbox-access>.
     The right-hand side must be a primitive keyword call (line, circle, square,
     polygon, path, pie, arc, connector, font, image) — func-call and
     object-inst are not valid on the right-hand side of a named draw cmd. *)

<bbox-access>      ::= <identifier> '.' 'bbox' '.' ('x' | 'y' | 'width' | 'height')
  (* Accesses a computed bounding box property of a named primitive.
     Runtime error if the named primitive has not yet been rendered (is not yet
     bound in the variable store at the point of evaluation). *)

<color>            ::= <named-color>
                     | 'none'                          (* fill-only: transparent / no paint *)
                     | '#' [0-9A-Fa-f]{6}
                     | 'RGB'  '(' <byte> ',' <byte> ',' <byte> ')'
                     | 'RGBA' '(' <byte> ',' <byte> ',' <byte> ',' <number-0-1> ')'
                     | <palette-ref>                   (* @alias — resolved in Pass 1 *)

<palette-ref>      ::= '@' <identifier>
  (* Resolved to a ColorValue or ColorNone by the resolver after all palette
     definitions have been collected in Pass 1.  An @alias that is not defined
     in any loaded palette is a parse error.  <palette-ref> is not permitted
     inside a <color-entry> (palette body). *)

<byte>             ::= [0-9]+ (* 0–255 *)
<number-0-1>       ::= [0-9]+ ('.' [0-9]*)?
                     | '.' [0-9]+
                     (* 0.0–1.0; at least one digit required *)
<named-color>      ::= 'black' | 'white' | 'red' | 'green' | 'blue'
                     | 'cyan' | 'magenta' | 'yellow' | 'orange'
                     | 'purple' | 'pink' | 'gray' | 'darkgray'
                     | 'lightgray' | 'brown' | 'lime' | 'navy'
                     | 'teal' | 'silver' | 'gold' | 'transparent'
                     | (* any other CSS Color Level 3 named color — 147 names total *)

<terminator>       ::= '\n' | ';'
<identifier>       ::= [A-Za-z_][A-Za-z0-9_-]*
<number>           ::= [0-9]+ ('.' [0-9]+)?
<line-type>        ::= 'solid' | 'dashed' | 'dotted' | 'dash-dot'
```

---

## 4. Top-Level Structure

A script file is a flat sequence of one or more **top-level statements**. There is no enclosing block.

Thanks to the two-pass processing model, object templates and function declarations may appear in **any order** relative to their call sites within the same script. `include` directives are resolved in Pass 1; any referenced file must exist and be readable at parse time.

### Global Namespace

Frame names, object template names, and function names all share a **single global namespace**. Defining two top-level entities with the same identifier — regardless of kind — is a **parse error**:

```
<file>:<line>: error: '<name>' is already defined
```

Names imported via `include` participate in the same namespace; a collision between an included name and a local name is also a parse error.

### Execution Model

1. The engine performs a **two-pass read**:
   - Pass 1: collect all `include` directives and load referenced files; collect all `begin_obj` / `end_obj`, `begin_func` / `end_func`, and `begin_palette` / `end_palette` definitions; resolve all `@alias` palette references.
   - Pass 2: execute `begin_frame` / `end_frame` blocks in order, resolving object instances and function calls. Frame bodies that contain `var` declarations, assignments, or named drawing commands execute **sequentially** in declaration order; z-index sorting is disabled for such frames (see §14.5).
2. Output files are emitted after all frames are processed.

### Top-Level Statement Summary

| Statement | Keyword(s) | Purpose |
|---|---|---|
| Frame | `begin_frame` … `end_frame` | Defines one image frame |
| Object template | `begin_obj` … `end_obj` | Defines a reusable composite object |
| Function declaration | `begin_func` … `end_func` | Defines a reusable parameterized drawing procedure |
| Include | `include "path"` | Imports definitions from another DSL file |
| Palette | `begin_palette` … `end_palette` | Defines named color aliases usable as `@alias` references |

---

## 5. Frame Definition

A frame is the top-level rendering unit. Each frame produces one image.

### Syntax

```
begin_frame <frame-id>
  [<frame-attribute>*]
  image <canvas-params>
  [<frame-attribute>*]
  <drawing-commands>
end_frame
```

### Frame Attributes

Frame attributes may appear **before or after** the `image` statement but **before** any drawing commands.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `hold-time` | number (ms) | `100` | Duration this frame is shown in an animated GIF before advancing. Decimal values are truncated to integer. |
| `frame-mode` | `one-run` \| `cyclic-run` | `one-run` | `one-run`: GIF plays once and stops. `cyclic-run`: GIF loops indefinitely |
| `colorspace` | `RGB` \| `RGBA` \| `GRAY` | `RGB` | Color space applied to the output image |

> **Note:** `hold-time` and `frame-mode` are relevant only for multi-frame (animated GIF) output. In single-frame scripts they are silently ignored.

> **Multi-frame `frame-mode`:** For multi-frame GIF output, the `frame-mode` of the **first** frame determines the GIF loop setting; `frame-mode` values on subsequent frames are ignored with no warning.

> **`colorspace` precedence:** If `colorspace` appears in both the frame attributes (`<frame-attr>`) and the `image` canvas statement, the **`image` statement value takes precedence**. Specifying conflicting values emits a warning:
> ```
> <file>:<line>: warning: colorspace '<frame-value>' in frame attributes overridden by '<image-value>' in image statement
> ```

### Example

```
begin_frame intro
  image width=800px; height=600px; colorspace=RGB; dpi=96; output-format=png;
  hold-time=1000;
  frame-mode=cyclic-run;
  background(color=white);
  font(font-family="Arial", font-size=32px, color=black, text="Hello", pos=(50,50));
end_frame
```

---

## 6. Image Canvas Statement

The `image` statement is **mandatory** inside every frame and defines the canvas properties.

> **Note:** The `image` keyword is also used for the image drawing primitive (§11). The two forms are distinguished by the presence of `(` — see §2.8 for the disambiguation rule.

### Syntax

```
image <param> (';' <param>)*
```

Parameters may be written on one line (semicolon-separated) or on separate lines.

### Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `width` | length | Yes | — | Canvas width |
| `height` | length | Yes | — | Canvas height |
| `colorspace` | `RGB` \| `RGBA` \| `GRAY` | No | `RGB` | Pixel color model |
| `dpi` | number | No | `96` | Dots per inch (affects unit conversions for pt, cm, mm). Decimal values are truncated to integer. |
| `output-format` | `png` \| `jpeg` \| `gif` \| `images` | No | `png` (single-frame) / `gif` (multi-frame) | Output file type. When omitted, the engine defaults to `png` for a single frame and `gif` for multiple frames. `images` produces one file per frame named `<frame-id>.png` or `<frame-id>.jpeg` (matching the frame's colorspace; RGBA uses `.png`) |

### Example

```
image width=1920px; height=1080px; colorspace=RGBA; dpi=144; output-format=png;
```

### Output File Naming

The engine derives output file name(s) from the **DSL script file name** (without the `.dsl` extension) and the selected `output-format`. All output files are written to the **same directory as the script file** unless the engine is invoked with an explicit output path override.

| `output-format` | File(s) produced | Naming rule |
|---|---|---|
| `png` | One file | `<script-name>.png` |
| `jpeg` | One file | `<script-name>.jpeg` |
| `gif` | One file | `<script-name>.gif` |
| `images` | One file per frame | `<frame-id>.png` or `<frame-id>.jpeg` (`RGBA` and `GRAY` frames always use `.png`; `RGB` frames use `.jpeg`) |

- `<script-name>` is the base name of the `.dsl` file (e.g., script `diagram.dsl` → `diagram.png`).
- `<frame-id>` is the identifier given in `begin_frame <frame-id>` (e.g., `begin_frame intro` → `intro.png`).
- For `output-format=images`, if two frames share the same `frame-id`, the second file **overwrites** the first; frame IDs should be unique within a script.
- When the engine is invoked with an explicit output path, that path overrides the default naming for single-file formats (`png`, `jpeg`, `gif`); for `images` mode, an explicit path is treated as the output **directory**.

> **`jpeg` and `colorspace=RGBA`:** Specifying `output-format=jpeg` with `colorspace=RGBA` is a **validation error** — JPEG does not support an alpha channel:
> ```
> <file>:<line>: error: jpeg output does not support RGBA colorspace
> ```

> **Consistent `output-format` across frames:** In a multi-frame script, all frames must declare the same `output-format` value. If frames declare conflicting values, the first frame's value is used for the output and a warning is emitted for each conflicting frame:
> ```
> <file>:<line>: warning: output-format '<value>' ignored; using '<first-value>' from first frame '<frame-id>'
> ```

---

## 7. Background Statement

Defines the canvas background. Must appear inside a frame body, after the `image` statement.

> **Initial canvas state:** If no `background` statement is present in a frame, the canvas is initialised as **fully transparent** for `colorspace=RGBA`, and **white (`#FFFFFF`)** for `colorspace=RGB` or `colorspace=GRAY`.

### 7.1 Solid Color Background

```
background(color=<color>)
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | color | Yes | Fill color for the entire canvas |

```
background(color=white)
background(color=#F0F0F0)
background(color=RGB(240,240,240))
```

### 7.2 Gradient Background

Linear gradient from `color1` at `start` point to `color2` at `end` point. Pixels are linearly interpolated.

```
background(color1=<color>, color2=<color>, start=<point>, end=<point>)
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color1` | color | Yes | Start color |
| `color2` | color | Yes | End color |
| `start` | point | Yes | Coordinates where `color1` is applied |
| `end` | point | Yes | Coordinates where `color2` is applied |

```
background(color1=white, color2=RGB(200,200,255), start=(0,0), end=(800,600))
```

> **Identical `start` and `end` points:** If `start` and `end` are the same coordinate, the entire canvas is filled with `color1` and a warning is emitted: `<file>:<line>: warning: gradient start and end are identical; rendering as solid color1`.

### 7.3 Image Background

Render an external image as the canvas background.

```
background(src=<string> [, mode=<mode>] [, x=<length>] [, y=<length>]
           [, width=<length>] [, height=<length>] [, opacity=<0-1>])
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `src` | string (path) | — | Path to external image (PNG, JPEG, GIF, SVG). Relative paths resolved from the DSL file location |
| `mode` | `fit` \| `stretch` \| `clip` | `fit` | Sizing mode: `fit` preserves aspect ratio inside canvas; `stretch` fills canvas ignoring aspect ratio; `clip` uses the sub-region defined by `x`,`y`,`width`,`height` |
| `x` | length | `0` | X offset of clip region (clip mode) |
| `y` | length | `0` | Y offset of clip region (clip mode) |
| `width` | length | canvas width | Width of clip region (clip mode) |
| `height` | length | canvas height | Height of clip region (clip mode) |
| `opacity` | 0.0–1.0 | `1.0` | Transparency of the background image |

```
background(src="assets/bg.png", mode=stretch, opacity=0.8)
background(src="photo.jpg", mode=clip, x=100, y=50, width=400, height=300)
```

> **Single background per frame:** A frame may contain **at most one** `background` call. Specifying more than one `background` statement in the same frame is a validation error:
> ```
> <file>:<line>: error: duplicate background statement in frame '<frame-id>'
> ```

---

### 7.4 Grid Statement

Defines a coordinate grid for the current frame. Multiple `grid()` statements are permitted per frame; each one activates a new grid configuration for the drawing commands that follow it.

```
grid(step-x=<length>, step-y=<length>
     [, offset-x=<length>] [, offset-y=<length>]
     [, render=<boolean>]
     [, color=<color>] [, line-type=<line-type>] [, line-width=<length>]
     [, align=<boolean>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `step-x` | length | Yes | — | Horizontal grid spacing. Must be > 0. |
| `step-y` | length | Yes | — | Vertical grid spacing. Must be > 0. |
| `offset-x` | length | No | `0` | Horizontal origin shift |
| `offset-y` | length | No | `0` | Vertical origin shift |
| `render` | boolean | No | `false` | When `true`, draws grid lines over the canvas after all other primitives |
| `color` | color | No | `RGB(200,200,200)` | Grid line color (used when `render=true`; defaults to gray with a warning if omitted while `render=true`) |
| `line-type` | line-type | No | `solid` | Grid line style |
| `line-width` | length | No | `1px` | Grid line stroke width |
| `align` | boolean | No | `false` | When `true`, snaps all drawable elements to the nearest grid intersection before transforms |

#### Grid Alignment, `snap`, and `align-origin`

The `snap` parameter (see §8.0) may be added to any primitive or object-instance call to control per-element snapping:

| `snap` value | Effect |
|---|---|
| `grid-intersection` | Snap both x and y to nearest grid intersection |
| `grid-x` | Snap only x to nearest vertical grid line; y unchanged |
| `grid-y` | Snap only y to nearest horizontal grid line; x unchanged |
| `none` | Do not snap this element; overrides global `align=true` |

The `align-origin` parameter (see §8.0) selects which reference point of the element's bounding box is snapped to the grid:

| `align-origin` value | Snapped point |
|---|---|
| `left-top` | Top-left corner of the bounding box |
| `right-top` | Top-right corner |
| `left-bottom` | Bottom-left corner |
| `right-bottom` | Bottom-right corner |
| `center` | Center of the bounding box |

Default: `center` for center-based nodes (`circle`, `pie`, `arc`); `left-top` for all other nodes.

**Alignment pipeline order:** snap/align → position → scale → skew → rotate. Snapping is resolved first so that all subsequent transforms operate on the already-snapped coordinates.

#### Constraints

- `step-x` and `step-y` must each be > 0.
- Multiple `grid()` statements are allowed per frame; each one replaces the active grid for commands that follow it.
- Using `snap=` or `align=true` on any element without a preceding `grid()` in the same frame is a **validation error**.

#### Examples

```
# Non-visual grid for alignment
grid(step-x=50px, step-y=50px, align=true);

# Visible debug grid
grid(step-x=50px, step-y=50px, render=true, color=gray, line-type=dashed, line-width=1px);

# Per-element snap
grid(step-x=50px, step-y=50px);
circle(color=red, fill=none, center=(63,48), radius=20, snap=grid-intersection);

# Opt one element out of global align
grid(step-x=50px, step-y=50px, align=true);
font(color=black, font-size=12px, text="Label", pos=(63,48), snap=none);

# align-origin: snap the right edge of a rectangle to the grid
grid(step-x=50px, step-y=50px, align=true);
square(color=black, fill=none, pos=(78,100), width=40px, height=40px,
       align-origin=right-bottom);
# right-bottom corner (118,140) snapped to (100,150); pos adjusted to (60,110)

# Two grids in one frame — different spacing for different regions
grid(step-x=20px, step-y=20px, align=true);
circle(color=red, fill=none, center=(63,48), radius=20);   # snapped to 20px grid
grid(step-x=100px, step-y=100px, align=true);
square(color=blue, fill=none, pos=(130,80), width=60px, height=60px); # snapped to 100px grid
```

---

## 8. Drawing Primitives

All drawing primitives share a common set of **optional transform parameters** that may be appended to any primitive's parameter list.

### 8.0 Shared Transform Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `rotate` | degrees (0–360) | `0` | Clockwise rotation around the element's center |
| `skew-x` | degrees | `0` | Horizontal skew angle. Positive values shear the element to the **right**. |
| `skew-y` | degrees | `0` | Vertical skew angle. Positive values shear the element **downward**. |
| `scale` | number | `1.0` | Uniform scale multiplier (`0.5` = half, `2.0` = double). Negative values are **not** supported and result in a validation error. `scale=0` is valid and renders the element as invisible (zero-size). |
| `z-index` | integer (0–1000) | declaration order | Z-order override; higher value = rendered on top |
| `snap` | `grid-intersection` \| `grid-x` \| `grid-y` \| `none` | omitted | Snap this element to the grid before transforms. `none` opts out of a global `align=true`. Requires a `grid()` in the same frame (validation error otherwise). See §7.4. |
| `align` | boolean | omitted | Per-element override for the grid's global `align` setting. `align=true` enables snapping for this element even if the grid has `align=false`; `align=false` disables snapping for this element even if the grid has `align=true`. |
| `align-origin` | `left-top` \| `right-top` \| `left-bottom` \| `right-bottom` \| `center` | `center` (center-based) / `left-top` (pos-based) | Selects which bounding-box reference point is snapped to the grid. `center-based` nodes are `circle`, `pie`, `arc`. All other nodes use `left-top` as the default. Invalid values produce a validation error. |
| `show-bbox` | boolean | `false` | Debug overlay: when `true`, draws a dashed bounding-box outline over the element after rendering. The outline color is chosen automatically for maximum contrast against the underlying canvas content (black or white). Not valid on `background` or `grid` (validation error). |

Transform application order: **snap/align (if grid active) → position → scale → skew → rotate**.

> **`snap` and grid dependency:** The `snap` and `align=true` parameters are only valid when a `grid()` statement has been defined earlier in the same frame. Using them without a preceding `grid()` halts execution:
> ```
> <file>:<line>: error: '<primitive>': snap= requires a grid() statement in the frame
> <file>:<line>: error: align=true used but no grid() is defined in this frame
> ```

> **`align-origin` invalid value:**
> ```
> <file>:<line>: error: align-origin: invalid value '<value>'; expected left-top, right-top, left-bottom, right-bottom, or center
> ```

> **Note:** "Position" is not a transform parameter — it is established by each primitive's own positioning parameter (`pos`, `center`, `start`/`end`, or `points`). The transform parameters above are composed relative to that position.

> **Per-primitive opacity:** The shared parameters do **not** include an `opacity` parameter. To render a primitive with partial transparency, use an `RGBA(r,g,b,a)` color value for its `color` and/or `fill` parameter (e.g., `fill=RGBA(255,0,0,0.5)` for a 50 % transparent red fill). The `opacity` parameter is supported only on the `image` primitive (§11) and on `background(src=...)` (§7.3).

> **`show-bbox` on `background` or `grid`:** Adding `show-bbox=true` to a `background()` or `grid()` call is a **validation error**:
> ```
> <file>:<line>: error: 'show-bbox' is not valid on 'background'; it is only accepted on drawable primitives and object instances
> <file>:<line>: error: 'show-bbox' is not valid on 'grid'; it is only accepted on drawable primitives and object instances
> ```

### 8.0.1 Coordinate System

- Origin `(0, 0)` is at the **top-left** corner of the canvas.
- **X** increases rightward.
- **Y** increases downward.
- All coordinate values accept any valid length unit (default `px`).

### 8.1 `line`

Renders a straight line stroke between two points.

**Stroke only — no fill.**

```
line(color=<color>, line-type=<line-type>, line-width=<length>,
     start=<point>, end=<point>
     [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `color` | color | Yes | — | Stroke color |
| `line-type` | line-type | No | `solid` | Stroke style |
| `line-width` | length | No | `1px` | Stroke width |
| `start` | point | Yes | — | Start coordinate `(x1,y1)` |
| `end` | point | Yes | — | End coordinate `(x2,y2)` |

```
line(color=black, line-type=solid, line-width=2px, start=(0,0), end=(200,200))
line(color=#FF0000, line-type=dashed, line-width=1pt, start=(10,10), end=(90,10))
```

### 8.2 `circle`

Renders a circle. Supports stroke and/or fill.

```
circle(color=<color>, line-type=<line-type>, line-width=<length>,
       fill=<color>, center=<point>, radius=<length>
       [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `color` | color | Yes | — | Stroke color |
| `line-type` | line-type | No | `solid` | Stroke style |
| `line-width` | length | No | `1px` | Stroke width |
| `fill` | color | No | `none` | Fill color; `none` = transparent |
| `center` | point | Yes | — | Center coordinate `(xc,yc)` |
| `radius` | length | Yes | — | Radius (must be > 0) |

```
circle(color=black, line-type=solid, line-width=1px, fill=yellow, center=(100,100), radius=50)
circle(color=blue, fill=none, center=(200,150), radius=75, rotate=0)
```

### 8.3 `square` (Rectangle)

Renders a rectangle. Despite the name, width and height are independent. Supports stroke and/or fill.

```
square(color=<color>, line-type=<line-type>, line-width=<length>,
       fill=<color>, pos=<point>, width=<length>, height=<length>
       [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `color` | color | Yes | — | Stroke color |
| `line-type` | line-type | No | `solid` | Stroke style |
| `line-width` | length | No | `1px` | Stroke width |
| `fill` | color | No | `none` | Fill color |
| `pos` | point | Yes | — | Top-left corner `(x1,y1)` |
| `width` | length | Yes | — | Rectangle width |
| `height` | length | Yes | — | Rectangle height |

> **Rounded corners:** The `square` primitive does **not** support a `corner-radius` parameter. Rounded rectangles are not available; all corners are sharp right angles.

```
square(color=black, fill=RGB(200,200,200), pos=(50,50), width=120px, height=80px)
square(color=red, line-type=dashed, line-width=2px, fill=none, pos=(0,0), width=100%, height=100%)
```

### 8.4 `polygon`

Renders a closed polygon. Minimum 3 points; path is automatically closed. Supports stroke and/or fill.

```
polygon(color=<color>, line-type=<line-type>, line-width=<length>,
        fill=<color>, points=<point-list>
        [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `color` | color | Yes | — | Stroke color |
| `line-type` | line-type | No | `solid` | Stroke style |
| `line-width` | length | No | `1px` | Stroke width |
| `fill` | color | No | `none` | Fill color |
| `points` | point-list | Yes | — | Ordered vertex list; minimum 3 points; auto-closed |

**Parse error** if fewer than 3 points are supplied.

```
polygon(color=black, fill=RGB(255,165,0), points=[(100,50),(150,150),(50,150)])
polygon(color=navy, line-width=2px, fill=lightblue, points=[(0,100),(100,0),(200,100),(200,200),(0,200)])
```

### 8.5 `path`

Renders an open (non-closed) stroke through a sequence of points. Minimum 2 points. **Stroke only — no fill.**

```
path(color=<color>, line-type=<line-type>, line-width=<length>,
     points=<point-list>
     [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `color` | color | Yes | — | Stroke color |
| `line-type` | line-type | No | `solid` | Stroke style |
| `line-width` | length | No | `1px` | Stroke width |
| `points` | point-list | Yes | — | Ordered vertex list; minimum 2 points; path is **not** closed |

**Parse error** if fewer than 2 points are supplied.

```
path(color=blue, line-type=solid, line-width=2px, points=[(10,10),(50,80),(90,10),(130,80)])
```

### 8.6 `pie`

Renders a pie slice (sector) defined by a center, radius, and two angles. Supports stroke and/or fill.

```
pie(color=<color>, line-type=<line-type>, line-width=<length>,
    fill=<color>, center=<point>, radius=<length>,
    start-angle=<degrees>, end-angle=<degrees>
    [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `color` | color | Yes | — | Stroke color |
| `line-type` | line-type | No | `solid` | Stroke style |
| `line-width` | length | No | `1px` | Stroke width |
| `fill` | color | No | `none` | Fill color |
| `center` | point | Yes | — | Center coordinate `(xc,yc)` |
| `radius` | length | Yes | — | Radius (must be > 0) |
| `start-angle` | degrees | Yes | — | Starting angle (0° = rightward, increasing clockwise) |
| `end-angle` | degrees | Yes | — | Ending angle |

The pie shape consists of the arc segment **plus two radial lines** back to the center.

> **Arc sweep direction:** The arc is always drawn **clockwise** from `start-angle` to `end-angle`. If `start-angle >= end-angle` after normalisation (modulo 360), the arc sweeps clockwise through 360° (e.g., `start-angle=270, end-angle=90` produces a 180° arc passing through 0°). If `start-angle == end-angle` after normalisation, nothing is rendered.

```
pie(color=black, fill=red, center=(200,200), radius=100, start-angle=0, end-angle=90)
```

### 8.7 `arc`

Renders only the **curved arc segment** between two angles. No lines to the center. No fill. **Stroke only.**

```
arc(color=<color>, line-type=<line-type>, line-width=<length>,
    center=<point>, radius=<length>,
    start-angle=<degrees>, end-angle=<degrees>
    [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `color` | color | Yes | — | Stroke color |
| `line-type` | line-type | No | `solid` | Stroke style |
| `line-width` | length | No | `1px` | Stroke width |
| `center` | point | Yes | — | Center coordinate |
| `radius` | length | Yes | — | Radius (must be > 0) |
| `start-angle` | degrees | Yes | — | Starting angle |
| `end-angle` | degrees | Yes | — | Ending angle |

> **Arc sweep direction:** The arc is always drawn **clockwise** from `start-angle` to `end-angle`. If `start-angle >= end-angle` after normalisation (modulo 360), the arc sweeps clockwise through 360° (e.g., `start-angle=270, end-angle=90` produces a 180° arc passing through 0°). If `start-angle == end-angle` after normalisation, nothing is rendered.

Specifying `fill` on an `arc` is a **parse error** — this applies to **any** `fill` value, including `fill=none`.

```
arc(color=gray, line-type=dashed, line-width=1px, center=(100,100), radius=80, start-angle=45, end-angle=135)
```

---

## 9. Connector Primitive

The connector is a rich drawing primitive for linking two or more points with optional labels, arrows, and animation.

**Stroke only — no fill.**

```
connector(
  color=<color>,
  line-width=<length>,
  line-type=<line-type>,
  points=<point-list> | (start=<point>, end=<point>),
  [connector-type=<connector-type>,]
  [start-cap=<cap-type>,]    [end-cap=<cap-type>,]
  [start-arrow=<cap-type>,]  [end-arrow=<cap-type>,]   (* aliases *)
  [cap-size=<cap-size>,]
  [start-cap-size=<cap-size>,]  [end-cap-size=<cap-size>,]
  [corner=<corner-style>,]
  [corner-radius=<length>,]
  [label=<string>,]
  [label-pos=<label-pos>,]
  [label-offset=<point>,]
  [label-font-family=<string>,]
  [label-font-size=<length>,]
  [label-font-color=<color>,]
  [label-font-style=<font-style>,]
  [label-font-weight=<font-weight>,]
  [animated=<boolean>,]
  [pattern=<pattern-type>,]
  [pattern-length=<length>,]
  [pattern-gap=<length>,]
  [pattern-color=<color>,]
  [pattern-speed=<length>,]
  [<transform-params>]
)
```

### 9.1 Points / Routing

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `points` | point-list | Yes* | — | Ordered list of ≥2 vertices. 2 points = single segment; 3+ = multi-segment |
| `start` | point | Yes* | — | Shorthand for first point (two-point connector only) |
| `end` | point | Yes* | — | Shorthand for last point (two-point connector only) |

\* Either `points` or both `start`+`end` must be supplied. Specifying both `points` and `start`/`end` in the same call is a **parse error**. Specifying only `start` without `end` (or only `end` without `start`) is also a **parse error**.

### 9.2 Connector Type

| Parameter | Type | Default | Description |
|---|---|---|---|
| `connector-type` | `straight` \| `curved` \| `step` | `straight` | `straight`: straight line segments; `curved`: smooth Catmull-Rom spline through all points; `step`: axis-aligned right-angle routing (see below) |

> **`curved` with exactly 2 points:** With exactly 2 points, `connector-type=curved` renders a single straight segment (equivalent to `straight`), as Catmull-Rom spline curvature requires at least 3 control points.

**`step` routing algorithm:**

For each consecutive pair of vertices `(x1, y1)` → `(x2, y2)` in the point list, the engine inserts a two-segment right-angle path:
1. A **horizontal leg** from `(x1, y1)` to the midpoint x-coordinate `(xm, y1)`, where `xm = (x1 + x2) / 2`.
2. A **vertical leg** from `(xm, y1)` to `(xm, y2)`.
3. A **horizontal leg** from `(xm, y2)` to `(x2, y2)`.

This produces an H-V-H (horizontal–vertical–horizontal) route between each pair of points. The `corner` and `corner-radius` parameters (§9.4) apply to every right-angle turn produced by the step routing.

### 9.3 Caps (Arrowheads)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `start-cap` | cap-type | `none` | Shape at the first point |
| `end-cap` | cap-type | `none` | Shape at the last point |
| `start-arrow` | cap-type | — | Alias for `start-cap` |
| `end-arrow` | cap-type | — | Alias for `end-cap` |
| `cap-size` | `small` \| `medium` \| `large` | `medium` | Controls cap size relative to `line-width` |

> **Alias conflict:** If both `start-cap` and `start-arrow` (or both `end-cap` and `end-arrow`) appear in the same call, a parse error is raised: `<file>:<line>: error: connector: 'start-cap' and 'start-arrow' are aliases and cannot both be specified`.
| `start-cap-size` | `small` \| `medium` \| `large` | `cap-size` | Per-end cap size override at start |
| `end-cap-size` | `small` \| `medium` \| `large` | `cap-size` | Per-end cap size override at end |

**Cap type values:**

| Value | Shape |
|---|---|
| `none` | No cap |
| `triangle` | Filled triangle arrowhead |
| `open-triangle` | Outlined triangle arrowhead |
| `circle` | Hollow circle |
| `filled-circle` | Filled circle |
| `diamond` | Hollow diamond |
| `filled-diamond` | Filled diamond |
| `square` | Hollow square |
| `filled-square` | Filled square |

### 9.4 Corner Style (Multi-Segment)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `corner` | `sharp` \| `rounded` \| `beveled` | `sharp` | Style applied at each intermediate vertex |
| `corner-radius` | length | `5px` | Arc radius for `rounded` corners |

> **Note:** `corner` and `corner-radius` apply only to `straight` and `step` connectors; they are silently ignored when `connector-type=curved`.

### 9.5 Label

| Parameter | Type | Default | Description |
|---|---|---|---|
| `label` | string | — | Text to render along the connector |
| `label-pos` | `start` \| `center` \| `end` | `center` | Label anchor position |
| `label-offset` | point | `(0,0)` | Pixel offset from the anchor |
| `label-font-family` | string | system sans-serif | Font family (fallback chain supported) |
| `label-font-size` | length | `12px` | Font size |
| `label-font-color` | color | same as `color` | Label text color |
| `label-font-style` | `normal` \| `italic` | `normal` | Font style |
| `label-font-weight` | `normal` \| `bold` | `normal` | Font weight |

### 9.6 Animation and Pattern

| Parameter | Type | Default | Description |
|---|---|---|---|
| `animated` | boolean | `false` | When `true`, pattern advances per frame in multi-frame GIF |
| `pattern` | `dash` \| `dot` \| `arrow` \| `zigzag` | `dash` | Repeating pattern unit replacing the plain stroke |
| `pattern-length` | length | `8px` | Length of one pattern unit |
| `pattern-gap` | length | `4px` | Gap between pattern units |
| `pattern-color` | color | connector `color` | Color of pattern units |
| `pattern-speed` | length | `4px` | Pixels the pattern advances per frame (animation only) |

> **Static pattern rendering:** When `animated=false` (the default), a `pattern` value is rendered as a **static repeating stroke style** — the pattern tiles along the connector stroke without advancing between frames. Only when `animated=true` does the pattern offset advance by `pattern-speed` per frame.

### Connector Examples

```
connector(color=black, line-width=1px, start=(50,50), end=(250,50), end-cap=triangle)

connector(color=blue, line-width=2px, line-type=dashed,
          points=[(10,10),(200,10),(200,200)],
          connector-type=step, corner=rounded, corner-radius=10px,
          end-cap=filled-circle, cap-size=small)

connector(color=red, line-width=1px,
          start=(0,100), end=(400,100),
          animated=true, pattern=dot, pattern-speed=6px,
          label="data flow", label-pos=center, label-font-size=11px)
```

---

## 10. Font / Text Primitive

Renders a text string at a specified position.

```
font(font-family=<string>, font-size=<length>, color=<color>,
     style=<font-style>, weight=<font-weight>,
     align=<text-align>,
     text=<string>, pos=<point>
     [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `font-family` | string | No | system monospace | Font name or fallback chain (e.g., `"Arial, Helvetica, sans-serif"`) |
| `font-size` | length | No | `12px` | Font size |
| `color` | color | Yes | — | Text color |
| `style` | `normal` \| `italic` | No | `normal` | Font style |
| `weight` | `normal` \| `bold` | No | `normal` | Font weight |
| `align` | `left` \| `center` \| `right` | No | `left` | Horizontal text alignment relative to `pos`. `left`: `pos` is the baseline left anchor. `center`: `pos` is the baseline horizontal centre of the text. `right`: `pos` is the baseline right anchor. |
| `text` | string | Yes | — | Text content; supports escape sequences `\"`, `\\`, `\n`, `\t` |
| `pos` | point | Yes | — | Anchor point on the text baseline; the role of the x-coordinate varies with `align` (see above) |

**Font resolution order:**
1. Try each font name in the fallback chain (comma-separated).
2. Try system defaults: `serif`, `sans-serif`, `monospace`.
3. Fall back to **system monospace** as final fallback.

**Multi-line text rendering:**

When the `text` value contains one or more `\n` escape sequences, the string is split into individual lines and rendered top-to-bottom.

- **`pos` anchors the baseline of the first line.** Subsequent lines are rendered below the first.
- **Line spacing** (the distance between consecutive baselines) is **`font-size × 1.2`** (120 % of the font size), rounded to the nearest pixel. For example, a `font-size=20px` text block has a 24 px baseline-to-baseline gap.
- The **`align`** parameter applies to every line independently, using the same x-coordinate from `pos` as the anchor for each line.
- There is **no built-in limit** on the number of lines; lines that extend below the canvas bottom are silently clipped.
- Automatic word-wrapping is **not** supported; line breaks must be inserted explicitly with `\n`.

```
font(font-family="Arial, Helvetica, sans-serif", font-size=24px,
     color=black, style=normal, weight=bold, text="Hello World", pos=(100,100))

# Multi-line text: two lines, baselines at y=10 and y=10+14*1.2=26.8≈27
font(color=red, font-size=14pt, text="Warning!\nCheck values.", pos=(10,10))

# Centre-aligned label over a shape
font(color=black, font-size=14px, align=center, text="Total", pos=(200,50))

# Right-aligned value flush to the right edge of a 400px canvas
font(color=black, font-size=12px, align=right, text="99%", pos=(400,80))
```

---

## 11. Image Primitive

Renders an external image file onto the canvas.

> **Note:** The `image` keyword is also used for the canvas statement (§6). The two forms are distinguished by the presence of `(` — see §2.8 for the disambiguation rule.

```
image(src=<string>, pos=<point>, width=<length>, height=<length>,
      opacity=<0-1>
      [, <transform-params>])
```

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `src` | string | Yes | — | Path to image file (PNG, JPEG, GIF, SVG). Relative to DSL file location |
| `pos` | point | Yes | — | Top-left corner of the rendered image |
| `width` | length | No* | — | Target width |
| `height` | length | No* | — | Target height |
| `opacity` | 0.0–1.0 | No | `1.0` | Transparency (0 = fully transparent) |

\* If only `width` is given, `height` auto-scales to preserve aspect ratio, and vice versa. If neither is given, the image is rendered at its natural size.

```
image(src="logo.png", pos=(10,10), width=200px, opacity=0.9)
image(src="chart.jpeg", pos=(50,50), width=400px, height=300px)
image(src="icon.svg", pos=(0,0), width=64px, rotate=45)
```

---

## 12. Object Templates

Object templates define **reusable composite shapes**. A template declaration does not render anything; it is instantiated with `<name>(...)`.

### 12.1 Template Declaration

```
begin_obj <name>
  [width: <length>;]
  [height: <length>;]
  [background: <color>;]
  [border: <line-type> <length> <color>;]
  [shadow: <dx> <dy> <blur-radius> <color>;]
  [clip-bounds: (<x1>,<y1>,<x2>,<y2>);]
  [clip-shape: <shape-name>;]
  <drawing-commands>
end_obj
```

> **Note:** Object attribute declarations use a **colon** (`:`), not `=`.

### 12.2 Object Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `width` | length | — | Bounding box width |
| `height` | length | — | Bounding box height |
| `background` | color | `transparent` | Object background fill |
| `border` | line-type + length + color | none | Object border: style, width, color |
| `shadow` | 4 values | none | Drop shadow: `offset-x offset-y blur-radius color`. `blur-radius=0` = hard shadow. Positive `offset-x` shifts the shadow **rightward**; positive `offset-y` shifts it **downward**, consistent with the canvas coordinate system (§8.0.1). |
| `clip-bounds` | `(x1,y1,x2,y2)` | none | Rectangular clip; content outside is not rendered |
| `clip-shape` | shape name | none | Shape-based clip mask. Accepts `circle` or `square`. `circle` clips to an ellipse inscribed in the bounding box; `square` clips to the bounding box rectangle. `polygon` is **not** a supported value (no mechanism exists to supply vertex data); specifying `clip-shape=polygon` is a validation error: `<file>:<line>: error: clip-shape 'polygon' is not supported; use 'circle' or 'square'`. |

> **Combined `clip-bounds` + `clip-shape`:** When both `clip-bounds` and `clip-shape` are specified on the same object, the effective clip region is the **intersection** of the two clip areas.

### 12.3 Object Instantiation

```
<name>(pos=<point> [, <override-params>])
```

**Core instance parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pos` | point | Yes | Top-left position of the object instance |
| `<any-template-attr>` | varies | No | Override any template attribute for this instance |

Instance parameters take precedence over template defaults. Unspecified parameters inherit template values.

**Instance-time size and rotation parameters (FEA-003):**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | length | template `width` | Override the bounding-box width for this instance only |
| `height` | length | template `height` | Override the bounding-box height for this instance only |
| `scale` | number > 0 | `1.0` | Uniformly scale all template dimensions by this factor |
| `resize-mode` | `layout` \| `default` | `default` | `layout` disables implicit geometry scaling when `width` and/or `height` are overridden |
| `rotate` | degrees ≥ 0 | `0` | Rotate the object clockwise around its center; no unit suffix |

**Precedence rule:** In the default mode, when both explicit `width`/`height` and `scale` are provided in the same call, explicit `width`/`height` takes precedence and `scale` is ignored (a warning is emitted). In `resize-mode=layout`, `width`/`height` define the layout box and `scale` remains active as an additional geometric scaling step.

**Validation:**
- `scale ≤ 0` → validation error: `<file>:<line>: error: object '<name>': 'scale' must be > 0`
- `rotate < 0` → validation error: `<file>:<line>: error: object '<name>': 'rotate' must be >= 0`
- `rotate` with a unit suffix (e.g., `rotate=45px`) → validation error: `<file>:<line>: error: object '<name>': 'rotate' does not accept a unit suffix`
- `width`/`height` and `scale` both present → warning: `<file>:<line>: warning: object '<name>': explicit width/height provided together with scale; scale is ignored`

**Examples:**

```
card(pos=(100,100), width=300px, height=80px)          # explicit size override
card(pos=(200,100), scale=1.6)                          # 160 % of template size
card(pos=(300,100), rotate=45)                          # clockwise rotation
card(pos=(400,100), width=200px, height=60px, rotate=30) # size + rotation
card(pos=(500,100), scale=0.5, rotate=90)               # scale + rotation
card(pos=(600,100), width=260px, height=120px, resize-mode=layout) # layout resize, no implicit content scaling
card(pos=(760,100), width=220px, height=90px, resize-mode=layout, scale=1.2) # layout resize + geometric scale
```

### 12.4 Nested Objects

Objects may contain other objects. **All drawing-command coordinates inside an object template** — primitives, nested object instantiations, and function calls — are **relative to the object's own top-left corner** (`pos`). Nested objects inherit parent properties unless explicitly overridden.

### 12.5 Example

```
begin_obj card
  width: 200px; height: 120px; background: RGB(255,255,255);
  border: solid 1px #AAAAAA;
  shadow: 2px 2px 4px RGBA(0,0,0,0.3);
  circle(color=gray, fill=none, center=(20,20), radius=15);
  font(font-family="Arial", font-size=14px, color=black, weight=bold, text="Title", pos=(45,15));
  line(color=#CCCCCC, line-width=1px, start=(0,35), end=(200,35));
end_obj

begin_frame diagram
  image width=800px; height=600px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F5F5F5);
  card(pos=(50,50));
  card(pos=(300,50), background=RGB(200,230,255));
end_frame
```

---

## 13. Function Declarations and Calls

Functions encapsulate drawing logic with named parameters, enabling parameterized reuse.

### 13.1 Function Declaration

```
begin_func <name>(<param1>, <param2>, ...)
  <drawing-commands>
end_func
```

- Parameters are positional identifiers.
- Parameters can be used in arithmetic expressions within the function body (e.g., `pos=(x+10, y+5)`).
- Functions may call other functions and instantiate object templates.
- Function names share the global namespace with object template names and frame names (see §4). A function name that duplicates any existing top-level name is a parse error.
- **Recursion is not supported.** A function call that would result in re-entering the same function — directly or indirectly — halts execution with a runtime error: `<file>:<line>: error: recursive call to function '<name>' is not permitted`.

### 13.2 Function Call

```
<name>(<value1>, <value2>, ...)
```

Arguments are passed **positionally** in the order declared.

### 13.3 Arithmetic Expressions in Parameters

Inside function bodies (and frame bodies with variable declarations — see §14), parameter values support basic arithmetic:

| Operator | Description |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |

Expressions are evaluated at call time with the supplied argument values.

> **Division by zero:** If a `/` expression evaluates to a denominator of zero at call time, the engine halts execution with a runtime error: `<file>:<line>: error: division by zero in expression`.

> **Unary minus:** Unary negation is **not** supported in expressions. To negate a value, subtract from zero: `0 - x`.

> **Disambiguation:** To subtract from a parameter, surround `-` with spaces: `x - 10` is subtraction. Without a preceding space, a hyphen is treated as part of the identifier: `skew-x` is the identifier `skew-x`, not `skew` minus `x`. See §2.5.

```
begin_func badge(x, y, label)
  circle(color=black, fill=white, center=(x, y), radius=20);
  font(color=black, font-size=12px, text=label, pos=(x-6, y-6));
end_func

begin_frame icons
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  badge(50, 100, "A");
  badge(150, 100, "B");
  badge(250, 100, "C");
end_frame
```

---

## 14. Variable Support and Bounding Box Extraction

Variables enable data-driven layout within frame and function bodies. A variable holds a numeric value computed at runtime; its primary use is to capture a rendered primitive's bounding box and feed that geometry into subsequent drawing commands.

### 14.1 Variable Declarations

```
var <identifier> (',' <identifier>)* ;
```

Declares one or more numeric variables in the current frame or function scope.

```
var x;
var gap, padding;
```

- Variable names follow the standard identifier rules (§2.5).
- A variable must be declared before it is assigned or referenced in an expression.
- Declaring the same name twice in the same scope is a runtime error.
- `var` is **not** permitted inside `begin_obj` / `end_obj` bodies — it is a parse error.

### 14.2 Assignment Statements

```
<identifier> = <expr> ;
```

Assigns the result of an arithmetic expression to a declared variable. The right-hand side is a full `<expr>` (§3): it may reference other declared variables, arithmetic operators, numeric literals, and bbox-access expressions.

```
gap = 20;
x = block1.bbox.x + block1.bbox.width + gap;
```

- The target identifier must have been declared with `var`; assigning to an undeclared name is a runtime error.
- Variables may be reassigned any number of times.

### 14.3 Named Drawing Commands

```
<identifier> = <primitive-call> ;
```

Renders a primitive immediately and binds it to a name so its bounding box can be accessed later.

```
block1 = square(pos=(20, 70), width=120, height=60, fill=#89b4fa, color=none);
```

- The right-hand side must be a **primitive keyword call** (`line`, `circle`, `square`, `polygon`, `path`, `pie`, `arc`, `connector`, `font`, `image`).
- `func-call` and `object-inst` are **not** valid on the right-hand side — a parse error is raised.
- The primitive is rendered at the point in the script where the statement appears.
- The binding name exists only in the variable store's object registry — it is not a global name and does not collide with frame, object, or function names.

### 14.4 Bounding Box Access

After a named primitive has been rendered, its bounding box is readable as:

```
<identifier> '.' 'bbox' '.' ('x' | 'y' | 'width' | 'height')
```

| Property | Meaning |
|---|---|
| `.bbox.x` | Left edge of the bounding box (x coordinate of top-left corner) |
| `.bbox.y` | Top edge of the bounding box (y coordinate of top-left corner) |
| `.bbox.width` | Bounding box width in DSL pixels |
| `.bbox.height` | Bounding box height in DSL pixels |

Bounding box coordinates are in **DSL pixel space** — the same coordinate system as all other positions (origin `(0,0)` at top-left; no anti-aliasing scale). The specific geometry per primitive type:

| Primitive | Bbox origin | Bbox size |
|---|---|---|
| `square` | `pos` (top-left corner) | `width` × `height` |
| `circle` | `(center.x − radius, center.y − radius)` | `diameter` × `diameter` |
| `line` | min of start/end, padded by `line-width / 2` | span + padding |
| `polygon`, `path` | min vertex coordinates | extent of all vertices |
| `pie`, `arc` | `(center.x − radius, center.y − radius)` | `diameter` × `diameter` |
| `image` | `pos` | `width` × `height` |
| `font` | `pos` (top-left of rendered text block) | approximate character extent |

A `<bbox-access>` expression may appear anywhere an `<expr>` is valid — in arithmetic, as a direct assignment value, or inline in a drawing-command parameter.

**Runtime error conditions:**
- Accessing `.bbox` before the named primitive has been rendered → runtime error: `<file>:<line>: error: object '<name>' has not been rendered yet`
- Accessing `.bbox` on an undeclared name → runtime error: `<file>:<line>: error: unknown object '<name>'`

### 14.5 Scope and Sequential Execution

**Scope:**

| Context | Variable scope | Fresh scope per call? |
|---|---|---|
| `begin_frame` body | Frame-scoped | Yes (each frame is independent) |
| `begin_func` body | Function-scoped | Yes (each call gets a fresh scope) |
| `begin_obj` body | Not supported | — |

Frame and function scopes are completely separate. Frame variables are not visible inside function calls invoked from that frame, and vice versa.

**Sequential execution:**

When a frame or function body contains any `var` declaration, assignment, or named drawing command, **all commands in that scope execute sequentially** in declaration order. Z-index sorting is **not applied**. This ensures variable values and bbox data are available to subsequent statements.

Frames and functions with no variable statements retain z-index sorting behavior.

**Error conditions:**
- Using a declared variable before its first assignment → runtime error: `<file>:<line>: error: variable '<name>' is used before being assigned`
- Using an undeclared identifier in an expression context → runtime error: `<file>:<line>: error: '<name>' is not a declared variable`
- Division by zero in an expression → runtime error: `<file>:<line>: error: division by zero in expression`

### 14.6 Grammar Summary

```ebnf
<var-decl-stmt>   ::= 'var' <identifier> (',' <identifier>)* ';'
<assign-stmt>     ::= <identifier> '=' <expr> ';'
<named-draw-cmd>  ::= <identifier> '=' <primitive-call> ';'
<bbox-access>     ::= <identifier> '.' 'bbox' '.' ('x' | 'y' | 'width' | 'height')
<expr-factor>     ::= <length>
                    | <identifier>
                    | <bbox-access>
                    | '(' <expr> ')'
```

### 14.7 Example

```
begin_frame chained_layout
  image width=600 height=200 output-format=png;
  background(color=#1e1e2e);

  # Declare the gap variable and assign it
  var gap;
  gap = 20;

  # Draw first block; bind to name so its bbox is accessible
  block1 = square(pos=(20, 70), width=120, height=60, fill=#89b4fa, color=none);

  # Capture block1 bbox
  var bx, by, bw, bh;
  bx = block1.bbox.x;
  by = block1.bbox.y;
  bw = block1.bbox.width;
  bh = block1.bbox.height;

  # Place second block immediately after the first
  block2 = square(pos=(bx + bw + gap, by), width=100, height=bh, fill=#a6e3a1, color=none);
  var bx2, bw2;
  bx2 = block2.bbox.x;
  bw2 = block2.bbox.width;

  # Third block after second
  block3 = square(pos=(bx2 + bw2 + gap, by), width=80, height=bh, fill=#fab387, color=none);

  # Circle centered on block1
  var cx, cy;
  cx = bx + bw / 2;
  cy = by + bh / 2;
  circle(center=(cx, cy), radius=25, color=#cdd6f4, line-width=2, fill=none);
end_frame
```

### 14.8 Comparison Expressions and `do ... while` Loops

Comparison expressions add boolean conditions on top of the existing arithmetic expression system. The first supported use is the `do ... while` loop condition.

#### Comparison grammar

```ebnf
<comparison-expr> ::= <expr> <comp-op> <expr>
<comp-op>         ::= '==' | '!=' | '<' | '<=' | '>' | '>='
```

- Both sides of the comparison are numeric expressions.
- Arithmetic evaluation happens first; the comparison is then applied to the two numeric results.
- A malformed comparison or unsupported operator is a parse error.

Examples:

```dsl
i < 5
counter <= max_count
current_x + width < canvas_limit
gap != 0
```

#### `do ... while` grammar

```ebnf
<loop-stmt> ::= 'do' <loop-body> 'while' <comparison-expr> ';'
<loop-body> ::= (<primitive-call>
               | <object-inst>
               | <func-call>
               | <var-decl-stmt>
               | <assign-stmt>
               | <named-draw-cmd>
               | <loop-stmt>)*
```

#### Scope rules

- Allowed in `begin_frame` and `begin_func` bodies.
- Not allowed at top level.
- Not allowed inside `begin_obj` or `begin_palette` bodies.
- Using a loop in a forbidden scope is a parse error.

#### Execution rules

- The loop body always executes once before the first condition check.
- After each iteration, the engine evaluates the comparison expression.
- The loop continues while the comparison remains true.
- Loop bodies follow the same sequential execution model already used for variables, bbox access, and named drawing commands.

#### Runtime guard

Every loop is protected by a fixed maximum iteration count of `1000`.

If the guard is exceeded, execution stops with:

```text
<file>:<line>: error: do-while loop exceeded maximum iteration count 1000
```

#### Error examples

| Condition | Error |
|---|---|
| `do` block without trailing `while ...;` | Parse error at loop statement |
| `while i;` | Parse error: loop condition must be a comparison expression |
| `while i <> 5;` | Parse error: unsupported comparison operator |
| `do ... while` inside `begin_obj` | Parse error: loop is not permitted inside an object template body |
| Loop exceeds 1000 iterations | Runtime error with file and line |

---

## 15. Include Statement

Imports all definitions (objects, functions) from another DSL file.

> **Placement restriction:** `include` directives may only appear at the **top level** of a script. They are not permitted inside `begin_frame`, `begin_obj`, or `begin_func` bodies. Placing an `include` inside any block body is a **parse error**.

### Syntax

```
include "<path>"
```

- `<path>` is either a **relative** path (resolved from the directory of the including file) or an **absolute** path.
- Includes may be **nested**: included files may include other files; there is no depth limit.
- Circular includes — where a file directly or transitively includes itself — are **detected at parse time** and result in a parse error.
- All `begin_obj` / `end_obj`, `begin_func` / `end_func`, and `begin_palette` / `end_palette` definitions from the included file become available in the including script. Palette alias names from included files are merged into the global palette namespace — a duplicate alias name is a parse error regardless of which file defines it.
- Frame definitions in included files are **ignored**; they do not produce any output. Only `begin_obj`, `begin_func`, and `begin_palette` definitions are imported by `include`.

```
include "components/buttons.dsl"
include "styles/colors.dsl"
include "C:/shared/common.dsl"
```

---

## 16. Data Types and Value Formats

### 16.1 Color Values

A color may be specified in four forms:

| Form | Syntax | Example |
|---|---|---|
| Named | `<name>` | `black`, `white`, `red`, `blue`, `green`, `yellow`, `cyan`, `magenta`, `orange`, `purple`, `pink`, `gray`, `transparent` |
| Hex | `#RRGGBB` | `#FF5733`, `#0000FF` |
| RGB | `RGB(r,g,b)` | `RGB(255,87,51)` |
| RGBA | `RGBA(r,g,b,a)` | `RGBA(0,0,0,0.5)` |
| Palette alias | `@<alias>` | `@primary`, `@accent`, `@bg` |

- `r`, `g`, `b` are integers **0–255**.
- `a` (alpha) is a decimal **0.0–1.0** (0 = fully transparent, 1 = fully opaque).
- An unrecognised color format is a **parse error** that halts execution.
- `none` is a special color value meaning “no paint” (valid for `fill` and `background` properties **only**; not a general color token). Using `none` on a stroke property (e.g., `color=none`) is a **semantic error** (the grammar accepts it syntactically, but the engine rejects it at validation time).
- `transparent` is a standard named color (equivalent to `RGBA(0,0,0,0)`) and may be used on **any** color property — stroke, fill, or background. Unlike `none`, it is not restricted to fill/background-only contexts.
- `@<alias>` is a palette alias reference (see §16.7). It is resolved to its concrete color value in Pass 1; no `@alias` token survives to Pass 2. An undefined alias is a parse error.

> **3-digit hex not supported:** Only 6-digit hex notation (`#RRGGBB`) is supported. The 3-digit shorthand (`#RGB`) is not valid and produces an 'unrecognised color format' parse error.

> **Greyscale conversion (`colorspace=GRAY`):** When a frame or canvas uses `colorspace=GRAY`, all color values (named, hex, RGB, RGBA) are converted to single-channel luminance using **CCIR 601 weighting**: `Y = 0.299×R + 0.587×G + 0.114×B`. The alpha channel is discarded during conversion; use `colorspace=RGBA` to preserve transparency alongside greyscale-mapped rendering.

### 16.2 Line Types

| Value | Appearance |
|---|---|
| `solid` | Continuous line |
| `dashed` | Long dash pattern |
| `dotted` | Dot pattern |
| `dash-dot` | Alternating dash and dot |

An unrecognised `line-type` value is a **parse error** that halts execution.

### 16.3 Unit Measurements

| Suffix | Meaning | Conversion |
|---|---|---|
| `px` | Pixels (default) | 1px = 1px |
| `pt` | Points | 1pt = DPI / 72 px |
| `em` | Relative to current font size | 1em = current font-size px |
| `cm` | Centimeters | 1cm = DPI / 2.54 px |
| `mm` | Millimeters | 1mm = DPI / 25.4 px |
| `%` | Percentage of parent container | x%: of parent width; y%: of parent height. When used inside an object template that declares no `width`/`height`, `%` resolves relative to the canvas dimensions. When used on a scalar (non-positional) length parameter (e.g., `radius`, `line-width`, `corner-radius`), `%` resolves relative to the **canvas width**. |

Omitting a unit defaults to **`px`**.

> **`em` outside a `font` primitive:** When `em` is used in a parameter of any primitive other than `font` (e.g., `line-width=1em`, `radius=2em`), it resolves to the **default font size of `12px`**. There is no "current font-size" concept outside a `font` primitive context.

### 16.4 Points

A point is a coordinate pair: `(x, y)`. Both x and y accept any valid length value.

```
(100, 200)
(50%, 50%)
(2cm, 3cm)
```

### 16.5 Point Lists

A bracketed, comma-separated list of two or more points:

```
[(x1,y1), (x2,y2), ..., (xn,yn)]
```

### 16.6 Boolean

| Value | Meaning |
|---|---|
| `true` | Enabled / yes |
| `false` | Disabled / no |

### 16.7 Palette Definitions and Alias References

Named color palettes collect color aliases under a single block name. Aliases are referenced with the `@` prefix anywhere a `<color>` value is accepted.

#### Defining a palette

```
begin_palette <name>
  <alias> = <color-literal>
  ...
end_palette
```

- `<name>` is the palette block's identifier (used only in error messages; it is not part of the alias lookup key).
- Each entry maps an alias identifier to a **direct color literal** — named color, hex, `RGB()`, or `RGBA()`. `@alias` refs are not permitted inside a palette body; using one is a **parse error**.
- An **empty** `begin_palette` / `end_palette` block (no entries) is a parse error.
- Alias names are **global**: all aliases from all loaded palettes (including palettes imported via `include`) share one flat namespace. Duplicate alias names are a parse error regardless of which file defines them.

#### Using palette aliases

A `@<alias>` reference may be used as a `<color>` value in any drawing-command parameter, object-template attribute (`background:`, `border:`, `shadow:`), or function call argument that accepts a color.

```
begin_palette brand
  primary   = #2342C8
  secondary = #F5F5F5
  accent    = RGB(255,140,0)
  bg        = RGBA(245,245,245,1.0)
end_palette

begin_frame styled_chart
  image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@primary, fill=@secondary, pos=(50,50), width=200px, height=150px);
  font(color=@accent, font-size=18px, weight=bold, text="Palette Demo", pos=(60,250));
end_frame
```

#### Resolution timing

All `@alias` references are resolved at the **end of Pass 1**, after every palette definition from every file (including all transitive `include` files) has been collected. This means:

- **Forward references** are supported: `@alias` may appear before the `begin_palette` block that defines it, as long as both are in the same script (or its transitively included files).
- **Cross-file references** work: an alias defined in an included file's palette is available to the including script and to any other included file.
- An `@alias` that is not defined in any loaded palette is a **parse error** (not a silent default).

---

## 17. Parameter Reference Tables

### 17.1 Common Stroke Parameters

| Parameter | Type | Default | Applicable to |
|---|---|---|---|
| `color` | color | — (required) | All stroke primitives |
| `line-type` | line-type | `solid` | All stroke primitives |
| `line-width` | length | `1px` | All stroke primitives |
| `fill` | color | `none` | `circle`, `square`, `polygon`, `pie`, objects |

### 17.2 Default Values Summary

| Parameter | Default |
|---|---|
| `fill` | `none` (transparent) |
| `z-index` | Declaration order |
| `style` (font) | `normal` |
| `weight` (font) | `normal` |
| `align` (font) | `left` |
| `line-type` | `solid` |
| `line-width` | `1px` |
| `opacity` | `1.0` |
| `connector-type` | `straight` |
| `start-cap` / `end-cap` | `none` |
| `cap-size` | `medium` |
| `corner` | `sharp` |
| `corner-radius` | `5px` |
| `pattern` | `dash` |
| `pattern-length` | `8px` |
| `pattern-gap` | `4px` |
| `pattern-color` | connector `color` |
| `pattern-speed` | `4px` |
| `animated` | `false` |
| `label-pos` | `center` |
| `label-offset` | `(0,0)` |
| `label-font-style` | `normal` |
| `label-font-weight` | `normal` |
| `rotate` | `0` |
| `skew-x` | `0` |
| `skew-y` | `0` |
| `scale` | `1.0` |
| `dpi` | `96` |
| `output-format` | `png` (single-frame); `gif` (multi-frame) |
| `colorspace` | `RGB` |
| `hold-time` | `100` (ms) |
| `frame-mode` | `one-run` |
| `font-family` (font primitive) | system monospace |
| `font-size` (font primitive) | `12px` |
| `label-font-family` | system sans-serif |
| `label-font-size` | `12px` |
| `label-font-color` | same as connector `color` |

### 17.3 Primitive Capability Matrix

| Primitive | Stroke | Fill | Points | Center+Radius | Angles | Transform |
|---|---|---|---|---|---|---|
| `line` | ✓ | — | start/end | — | — | ✓ |
| `circle` | ✓ | ✓ | center | ✓ | — | ✓ |
| `square` | ✓ | ✓ | pos (TL) | — | — | ✓ |
| `polygon` | ✓ | ✓ | point-list | — | — | ✓ |
| `path` | ✓ | — | point-list | — | — | ✓ |
| `pie` | ✓ | ✓ | center | ✓ | start/end | ✓ |
| `arc` | ✓ | — | center | ✓ | start/end | ✓ |
| `connector` | ✓ | — | point-list | — | — | ✓ |
| `font` | — | — | pos | — | — | ✓ |
| `image` | — | — | pos | — | — | ✓ |

---

## 18. Complete Annotated Examples

### 18.1 Minimal Static PNG

```
begin_frame hello_world
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  font(font-family="Arial", font-size=32px, color=black, weight=bold,
       text="Hello, World!", pos=(50, 80));
end_frame
```

**Notes:**
- Single frame → single PNG output.
- `hold-time` and `frame-mode` are omitted (irrelevant for static image).

---

### 18.2 Multi-Frame Animated GIF

```
begin_frame frame_0
  image width=500px; height=300px; colorspace=RGB; dpi=96;
  hold-time=500; frame-mode=cyclic-run;
  background(color=white);
  circle(color=red, line-type=solid, line-width=2px, fill=yellow,
         center=(100,150), radius=50);
end_frame

begin_frame frame_1
  image width=500px; height=300px; colorspace=RGB; dpi=96;
  hold-time=500; frame-mode=cyclic-run;
  background(color=white);
  circle(color=blue, line-type=solid, line-width=2px, fill=cyan,
         center=(250,150), radius=50);
end_frame

begin_frame frame_2
  image width=500px; height=300px; colorspace=RGB; dpi=96;
  hold-time=500; frame-mode=cyclic-run;
  background(color=white);
  circle(color=green, line-type=solid, line-width=2px, fill=lime,
         center=(400,150), radius=50);
end_frame
```

**Notes:**
- 3 frames → one animated GIF (default `output-format=gif`).
- Each frame shown for 500 ms; loops indefinitely.
- `frame-mode` applies to the first frame and propagates to GIF loop settings.

---

### 18.3 Object Template with Multiple Instances

```
begin_obj card
  width: 180px; height: 100px;
  background: white;
  border: solid 1px gray;
  shadow: 3px 3px 5px RGBA(0,0,0,0.25);
  font(font-family="Arial", font-size=14px, color=#333333,
       weight=bold, text="Card Title", pos=(10,15));
  line(color=#DDDDDD, line-width=1px, start=(0,32), end=(180,32));
end_obj

begin_frame dashboard
  image width=800px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#EEEEEE);
  card(pos=(20,50));
  card(pos=(220,50), background=RGB(200,230,255));
  card(pos=(420,50), background=RGB(255,220,200));
end_frame
```

---

### 18.4 Reusable Function

```
begin_func labeled_arrow(x1, y1, x2, y2, label_text)
  connector(color=black, line-width=1px, start=(x1,y1), end=(x2,y2),
            end-cap=triangle, cap-size=medium);
  font(color=black, font-size=11px, text=label_text,
       pos=(x1+(x2-x1)/2, y1+(y2-y1)/2-14));
end_func

begin_frame flowchart
  image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  square(color=black, fill=RGB(220,235,255), pos=(50,50),   width=120px, height=50px);
  square(color=black, fill=RGB(220,235,255), pos=(400,50),  width=120px, height=50px);
  square(color=black, fill=RGB(220,235,255), pos=(225,200), width=120px, height=50px);
  font(color=black, font-size=12px, text="Start",   pos=(95, 80));
  font(color=black, font-size=12px, text="End",     pos=(448, 80));
  font(color=black, font-size=12px, text="Process", pos=(248, 230));
  labeled_arrow(170, 75, 225, 225, "step 1");
  labeled_arrow(345, 225, 400, 75, "step 2");
end_frame
```

---

### 18.5 Include and Library Reuse

**File: `components/shapes.dsl`**
```
begin_obj icon_circle
  width: 60px; height: 60px;
  background: transparent;
  border: solid 2px black;
  circle(color=black, fill=white, center=(30,30), radius=28);
end_obj
```

**File: `main.dsl`**
```
include "components/shapes.dsl"

begin_frame layout
  image width=400px; height=200px; colorspace=RGBA; dpi=96; output-format=png;
  background(color=transparent);
  icon_circle(pos=(20,70));
  icon_circle(pos=(160,70), background=yellow);
end_frame
```

---

### 18.6 Gradient Background with Z-Order

```
begin_frame layered
  image width=500px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color1=white, color2=RGB(30,100,200), start=(0,0), end=(500,400));
  square(color=black, fill=RGB(255,200,0), pos=(50,50), width=200px, height=150px, z-index=1);
  circle(color=black, fill=white, center=(150,125), radius=80, z-index=2);
  font(color=black, font-size=18px, weight=bold, text="Layer Test",
       pos=(75,120), z-index=3);
end_frame
```

---

### 18.7 Animated Connector (Flowing Data)

```
begin_frame data_flow_0
  image width=600px; height=200px; colorspace=RGB; dpi=96;
  hold-time=100; frame-mode=cyclic-run;
  background(color=white);
  square(color=gray, fill=RGB(220,220,255), pos=(20,75), width=100px, height=50px);
  font(color=black, font-size=12px, text="Source", pos=(40,105));
  square(color=gray, fill=RGB(255,220,220), pos=(480,75), width=100px, height=50px);
  font(color=black, font-size=12px, text="Target", pos=(502,105));
  connector(color=blue, line-width=2px, start=(120,100), end=(480,100),
            animated=true, pattern=arrow, pattern-speed=6px,
            end-cap=triangle, cap-size=medium);
end_frame
```

*(Repeat `begin_frame` blocks with incrementing pattern offsets for smooth animation.)*

---

### 18.8 Path Primitive

```
begin_frame path_demo
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Open polyline — zigzag stroke
  path(color=blue, line-type=solid, line-width=2px,
       points=[(20,150),(80,50),(140,150),(200,50),(260,150),(320,50),(380,150)]);

  # Dashed open path
  path(color=red, line-type=dashed, line-width=1px,
       points=[(20,170),(200,130),(380,170)]);
end_frame
```

**Notes:**
- `path` is an open polyline (no automatic closing); use `polygon` for a closed shape.
- Minimum 2 points required; a parse error is raised for fewer.
- `fill` is not supported on `path`.

---

### 18.9 Polygon and Pie Primitives

```
begin_frame shapes_demo
  image width=500px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Filled triangle (polygon — minimum 3 points)
  polygon(color=black, line-width=1px, fill=RGB(255,165,0),
          points=[(100,50),(175,200),(25,200)]);

  # Pentagon outline
  polygon(color=navy, line-width=2px, fill=lightblue,
          points=[(300,40),(380,100),(350,195),(250,195),(220,100)]);

  # Pie slice: 25% of a circle (0° to 90°)
  pie(color=black, line-width=1px, fill=red,
      center=(430,150), radius=80,
      start-angle=0, end-angle=90);
end_frame
```

**Notes:**
- `polygon` automatically closes the path from the last point back to the first point.
- `pie` draws the arc segment **and** two radial lines from the endpoints back to the center.
- Angles use 0° = rightward (3 o'clock), increasing clockwise.

---

### 18.10 Arc Primitive

```
begin_frame arc_demo
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Solid arc: upper semicircle (180° to 360°)
  arc(color=blue, line-width=3px,
      center=(200,150), radius=100,
      start-angle=180, end-angle=360);

  # Dashed quarter-arc (0° to 90°)
  arc(color=red, line-type=dashed, line-width=2px,
      center=(200,150), radius=60,
      start-angle=0, end-angle=90);
end_frame
```

**Notes:**
- `arc` renders **only** the curved segment; there are no radial lines (compare with `pie`).
- `fill` is not supported on `arc` — specifying any `fill` value (including `fill=none`) is a parse error.

---

## 19. Error Reference

### 19.1 Parse Errors (Execution Halted)

| Error Condition | Message Pattern |
|---|---|
| Unrecognised color format | `<file>:<line>: error: unrecognised color value '<value>'` |
| Unrecognised `line-type` | `<file>:<line>: error: unrecognised line-type '<value>'` |
| `polygon` with fewer than 3 points | `<file>:<line>: error: polygon requires at least 3 points, got <n>` |
| `path` with fewer than 2 points | `<file>:<line>: error: path requires at least 2 points, got <n>` |
| `connector` with fewer than 2 points | `<file>:<line>: error: connector requires at least 2 points, got <n>` |
| `fill` specified on `arc` (any value, including `fill=none`) | `<file>:<line>: error: arc does not support fill parameter` |
| Duplicate named-parameter key in a single call | `<file>:<line>: error: '<primitive>': duplicate parameter '<key>'` |
| Unclosed `begin_frame` | `<file>:<line>: error: missing end_frame for frame '<name>'` |
| Unclosed `begin_obj` | `<file>:<line>: error: missing end_obj for object '<name>'` |
| Unclosed `begin_func` | `<file>:<line>: error: missing end_func for function '<name>'` |
| Unresolved include path | `<file>:<line>: error: cannot open include file '<path>'` |
| Circular `include` detected | `<file>:<line>: error: circular include: '<path>' already being processed` |
| `include` inside a block body | `<file>:<line>: error: include directive is not permitted inside begin_frame / begin_obj / begin_func` |
| `none` used as stroke `color` | `<file>:<line>: error: 'none' is not valid for stroke color` |
| `fill` specified on `line` | `<file>:<line>: error: line does not support fill parameter` |
| `fill` specified on `path` | `<file>:<line>: error: path does not support fill parameter` |
| `points` and `start`/`end` both specified on `connector` | `<file>:<line>: error: connector: use 'points' or 'start'+'end', not both` |
| Only `start` or only `end` specified on `connector` (not both) | `<file>:<line>: error: connector: 'start' and 'end' must both be specified` |
| Required parameter missing from a primitive call | `<file>:<line>: error: '<primitive>': required parameter '<key>' is missing` |
| Function argument count mismatch | `<file>:<line>: error: '<name>' expects <n> argument(s), got <m>` |
| Unrecognised parameter key | `<file>:<line>: error: '<primitive>': unknown parameter '<key>'` |
| Duplicate top-level name | `<file>:<line>: error: '<name>' is already defined` |
| Case-incorrect keyword | `<file>:<line>: error: unexpected token '<token>'` |
| `begin_frame` body with no `image` statement | `<file>:<line>: error: frame '<name>': missing required 'image' canvas statement` |
| `background()` with no parameters | `<file>:<line>: error: background: no parameters supplied` |
| `background()` with conflicting form keys (e.g., both `color` and `color1`) | `<file>:<line>: error: background: ambiguous parameter combination — cannot determine background form` |
| Gradient `background()` missing `color2`, `start`, or `end` | `<file>:<line>: error: background: gradient form requires 'color1', 'color2', 'start', and 'end'` |
| `start-cap` and `start-arrow` (or `end-cap` and `end-arrow`) both specified | `<file>:<line>: error: connector: 'start-cap' and 'start-arrow' are aliases and cannot both be specified` |
| Angle parameter supplied with a unit suffix (e.g., `rotate=45px`) | `<file>:<line>: error: angle parameter '<key>' does not accept a unit suffix` |
| `snap=` used without a `grid()` in the frame | `<file>:<line>: error: '<primitive>': snap= requires a grid() statement in the frame` |
| `align=true` used without a `grid()` in the frame | `<file>:<line>: error: align=true used but no grid() is defined in this frame` |
| `align-origin` with an invalid value | `<file>:<line>: error: align-origin: invalid value '<value>'; expected left-top, right-top, left-bottom, right-bottom, or center` |
| `show-bbox=true` on `background` | `<file>:<line>: error: 'show-bbox' is not valid on 'background'; it is only accepted on drawable primitives and object instances` |
| `show-bbox=true` on `grid` | `<file>:<line>: error: 'show-bbox' is not valid on 'grid'; it is only accepted on drawable primitives and object instances` |
| `grid()` missing `step-x` or `step-y` | `<file>:<line>: error: grid: required parameter 'step-x'/'step-y' is missing` |
| `@alias` reference to an undefined palette alias | `<file>:<line>: error: undefined palette alias '@<alias>'` |
| Duplicate palette alias name across any loaded palette | `<file>:<line>: error: duplicate palette alias '<alias>' (already defined in a previously loaded palette)` |
| Empty `begin_palette` / `end_palette` block (no entries) | `<file>:<line>: error: palette '<name>': a palette block must contain at least one alias entry` |
| `@alias` reference used inside a palette body | `<file>:<line>: error: palette alias references (@...) are not permitted inside a begin_palette body` |
| Unclosed `begin_palette` | `<file>:<line>: error: missing end_palette for palette '<name>'` |
| `var` declaration inside a `begin_obj` body | `<file>:<line>: error: 'var' is not permitted inside an object template body` |
| Named draw command (`x = func(...)` or `x = obj(...)`) with non-primitive RHS | `<file>:<line>: error: named draw command: right-hand side must be a primitive keyword call` |
| Variable used before being assigned | `<file>:<line>: error: variable '<name>' is used before being assigned` |
| Undeclared identifier used in expression context | `<file>:<line>: error: '<name>' is not a declared variable; declare with 'var <name>;' before use` |
| `.bbox` access before the named primitive is rendered | `<file>:<line>: error: object '<name>' has not been rendered yet` |
| `.bbox` access on an unknown name | `<file>:<line>: error: unknown object '<name>'` |
| `do ... while` at top level | `<file>:<line>: error: do-while loop is only permitted inside begin_frame / begin_func bodies` |
| `do ... while` inside `begin_obj` | `<file>:<line>: error: do-while loop is not permitted inside an object template body` |
| `do ... while` inside `begin_palette` | `<file>:<line>: error: do-while loop is not permitted inside a palette body` |
| `do` block without `while <comparison>;` | `<file>:<line>: error: do-while loop requires a trailing comparison condition` |
| Loop condition is not a comparison expression | `<file>:<line>: error: do-while condition must be a comparison expression` |
| Unsupported comparison operator | `<file>:<line>: error: unsupported comparison operator '<op>'` |

### 19.2 Validation Warnings / Errors

| Condition | Behaviour |
|---|---|
| Negative numeric value for `radius`, `width`, `height` | Error halted: `<file>:<line>: error: '<param>' must be positive, got <value>` |
| `RGB`/`RGBA` component `r`, `g`, or `b` outside 0–255 | Error halted: `<file>:<line>: error: color component '<n>' is out of range 0–255` |
| `RGBA` alpha value outside 0.0–1.0 | Error halted: `<file>:<line>: error: alpha value '<n>' is out of range 0.0–1.0` |
| `width` or `height` of zero in `image` canvas statement | Error halted: `<file>:<line>: error: canvas '<param>' must be greater than zero` |
| `scale` value less than 0 | Error halted: `<file>:<line>: error: scale value must be non-negative, got <value>` |
| `dpi` value ≤ 0 in `image` canvas statement | Error halted: `<file>:<line>: error: 'dpi' must be greater than zero, got <value>` |
| `opacity` value outside 0.0–1.0 | Error halted: `<file>:<line>: error: 'opacity' value '<n>' is out of range 0.0–1.0` |
| `hold-time` value < 1 (after integer truncation) | Error halted: `<file>:<line>: error: 'hold-time' must be at least 1 ms, got <value>` |
| Angle parameter (`rotate`, `start-angle`, `end-angle`) outside 0–360 | Normalised modulo 360 |
| Out-of-bounds coordinates | Silently clipped to canvas bounds |
| `animated=true` on a single-frame script | Silently ignored (rendered as static) |
| `z-index` value outside 0–1000 | Value clamped to the nearest bound (0 if negative, 1000 if > 1000); warning emitted: `<file>:<line>: warning: z-index <n> clamped to <bound>` |
| Unresolved `src` path (image/background) | Error halted with descriptive message |
| `grid step-x` or `step-y` ≤ 0 | Error halted: `<file>:<line>: error: grid: 'step-x'/'step-y' must be greater than zero, got <value>` |
| `grid render=true` without `color` | Warning (execution continues): `<file>:<line>: warning: grid render=true without color; defaulting to RGB(200,200,200)` |

### 19.3 Error Message Format

All errors include:

```
<filename>:<line-number>: <severity>: <description>
```

Example:

```
main.dsl:17: error: polygon requires at least 3 points, got 2
main.dsl:42: error: unrecognised color value 'badval'
```

---

## Changelog

### 2026-05-05 — FEA-007: variable support and bounding box extraction

- Updated §2.8 Keywords: added `var` to the reserved keyword list
- Updated §3 EBNF:
  - Added `<var-decl-stmt>`, `<assign-stmt>`, `<named-draw-cmd>` alternatives to `<drawing-stmt>`
  - Updated arithmetic-expression comment from "function bodies only" to "frame and function bodies"; added cross-reference to §14
  - Updated `<expr-factor>` to include `<bbox-access>` alternative
  - Added `<var-decl-stmt>`, `<assign-stmt>`, `<named-draw-cmd>`, and `<bbox-access>` non-terminal productions with inline constraint comments
- Updated §4 Execution Model: Pass 2 description notes sequential execution for frames containing variable statements; cross-reference to §14.5
- Updated §13.3 Arithmetic Expressions in Parameters: updated opening sentence to mention frame bodies; added cross-reference to §14
- Added new §14 Variable Support and Bounding Box Extraction (7 subsections):
  - §14.1 Variable Declarations — syntax, rules, restriction in obj bodies
  - §14.2 Assignment Statements — syntax, reassignment, error conditions
  - §14.3 Named Drawing Commands — syntax, primitive-only restriction, binding behavior
  - §14.4 Bounding Box Access — property table, per-primitive bbox geometry table, runtime error conditions
  - §14.5 Scope and Sequential Execution — scope table, sequential-execution rule, runtime error list
  - §14.6 Grammar Summary — compact EBNF repeat
  - §14.7 Example — complete chained-layout DSL script
- Renumbered §14 Include → §15; §15 Data Types → §16 (all subsections 15.x → 16.x); §16 Parameter Reference → §17 (all subsections); §17 Examples → §18 (all subsections 17.x → 18.x); §18 Error Reference → §19 (all subsections)
- Updated cross-reference `§15.7` → `§16.7` in §16.1 Color Values
- Updated §19.1 Parse Errors: added eight new error rows for FEA-007 variable, assignment, named-draw, and bbox error conditions
- File version 3.4 → 3.5

### 2026-05-04 — FEA-006: named color palette support

- Updated §2.8 Keywords: added `begin_palette` / `end_palette`; added `@` palette-reference-prefix callout note
- Updated §3 EBNF: added `<palette-def>` alternative to `<top-level-stmt>`; added `<palette-def>` and `<color-entry>` productions with inline constraint comments; added `<palette-ref>` alternative to `<color>` production; added `<palette-ref>` non-terminal definition
- Updated §4 Top-Level Structure: expanded Pass 1 description to include palette collection and `@alias` resolution; added `Palette` row to the Top-Level Statement Summary table
- Updated §14 Include: added `begin_palette` to the list of imported definitions; added note about merged alias namespace and duplicate alias error
- Updated §15.1 Color Values: added `Palette alias` row to the color-forms table; added `@<alias>` bullet to the notes list
- Added §15.7 Palette Definitions and Alias References: palette syntax, alias lookup rules, resolution timing (forward refs and cross-file refs), full example
- Updated §18.1 Parse Errors: added five new error rows for undefined alias, duplicate alias, empty palette, `@alias` in palette body, unclosed `begin_palette`
- File version 3.3 → 3.4

### 2026-05-03 — FEA-005: show-bbox debug overlay; align-origin; multiple grids per frame
- Updated §3 EBNF `<grid-stmt>` comment: replaced "at most one grid() per frame" constraint with note that multiple grid() statements are allowed, each replacing the active grid for subsequent commands
- Updated §7.4 (Grid Statement): section intro no longer states one-grid-per-frame restriction; expanded alignment sub-heading to cover `align-origin`; added `align-origin` value table; updated Constraints list; added two new examples (align-origin and two grids in one frame)
- Updated §8.0 (Shared Transform Parameters): added `align` (per-element override), `align-origin`, and `show-bbox` parameter rows to the table; updated callout notes for `snap`/`align=true` dependency and `show-bbox` restrictions
- Updated §18.1 (Parse Errors): removed stale "more than one grid() in a frame" error row (no longer an error); added `align=true` without grid, `align-origin` invalid value, and two `show-bbox` validation error rows
- File version 3.2 → 3.3

### 2026-05-03 07:57:16 — FEA-004: configurable grid system
- Updated §3 EBNF: added `<grid-stmt>` to `<drawing-stmt>`; added `<grid-stmt>` production with inline parameter documentation; added `<snap-mode>` non-terminal
- Added §7.4 (Grid Statement): full parameter table, alignment pipeline order, `snap` mode semantics table, constraints, and four DSL examples
- Updated §8.0 (Shared Transform Parameters): added `snap` row; updated transform order line to include snap step
- Updated §18.1 (Parse Errors): added three new error rows for multiple grid(), snap without grid, and missing step-x/step-y
- Updated §18.2 (Validation Warnings/Errors): added grid step ≤ 0 error and render-without-color warning rows
- File version 3.1 → 3.2

### 2026-05-02 19:28:12 — FEA-003: optional size and rotation parameters for DSL objects
- Updated §12.3 (Object Instantiation): split parameter table into "core" and "instance-time size/rotation" groups
- Added `width`, `height`, `scale`, `rotate` parameter rows with types, defaults, and descriptions
- Added precedence rule (explicit width/height over scale)
- Added validation error and warning message patterns for scale ≤ 0, rotate < 0, rotate with unit, simultaneous size+scale
- Added five DSL examples illustrating all parameter combinations
- File version 3.0 → 3.1

### 2026-04-29 14:23:28 — Fix W-01 through W-11 (all 11 gaps from gap_report_dsl_v29)
- W-01: Added `#` context-sensitive token disambiguation note to §2.3 — hex color vs comment.
- W-02: Added missing-`image`-statement error row to §18.1 with message pattern.
- W-03: Added `dpi≤0` validation error row to §18.2 — must be greater than zero.
- W-04: Added `opacity` out-of-range error row to §18.2 — must be 0.0–1.0.
- W-05: Updated §6 `output-format=images` naming rule — RGBA and GRAY frames use `.png`; RGB uses `.jpeg`.
- W-06: Replaced `clip-shape` `polygon` value in §12.2 — `polygon` is not supported; validation error emitted.
- W-07: Added `background()` invalid parameter combination error rows to §18.1 — no-params, ambiguous form, incomplete gradient.
- W-08: Added `start-cap`/`start-arrow` alias conflict parse error note to §9.3 and §18.1.
- W-09: Added `%` on scalar length parameters note to §15.3 — resolves relative to canvas width.
- W-10: Added `hold-time<1` validation error row to §18.2.
- W-11: Added angle parameter unit suffix validation error note to §2.7 and §18.1.
- V-01: Added `colorspace` conflict precedence note to §5 — `image` statement value overrides frame-attr value; warning emitted.
- V-02: Added missing-required-parameter error row to §18.1 with message pattern.
- V-03: Added `curved` connector with exactly 2 points note to §9.2 — degrades to straight segment.
- V-04: Added arc sweep direction note to §8.6 and §8.7 — always clockwise; `start>=end` wraps through 360°; `start==end` renders nothing.
- V-05: Added RGB/RGBA out-of-range component error rows to §18.2 — byte >255 and alpha >1.0 both error halted.
- V-06: Added zero canvas dimension validation error row to §18.2 — `width=0` or `height=0` is error halted.
- V-07: Extended `scale` description in §8.0 — `scale=0` is valid and renders element as invisible.
- V-08: Added `pattern-color` default row to §16.2 defaults table — default is connector `color`.
- V-09: Added 3-digit hex note to §15.1 — only `#RRGGBB` 6-digit hex supported; `#RGB` is parse error.
- V-10: Added identical `start`/`end` gradient fallback note to §7.2 — fills with `color1` + warning.
- V-11: Extended `shadow` attribute description in §12.2 — positive offset-x = rightward, positive offset-y = downward.
- G-01: Added `scale < 0` row to §18.2 with message pattern.
- G-02: Extended §18.2 "negative radius/width/height" row with explicit message pattern.
- G-03: Added `jpeg` + `colorspace=RGBA` validation error note to §6 (Output File Naming).
- G-04: Added consistent `output-format` across frames rule + warning to §6.
- G-05: Added initial canvas state note to §7 — RGBA=transparent, RGB/GRAY=white.
- G-06: Added note to §9.4 — `corner`/`corner-radius` silently ignored for `curved` connectors.
- G-07: Extended §9.1 footnote for partial `start`/`end`; added corresponding §18.1 error row.
- G-08: Added 5 missing defaults to §16.2 table — `font-family`, `font-size`, `label-font-family`, `label-font-size`, `label-font-color`.
- G-09: Added combined `clip-bounds` + `clip-shape` intersection note to §12.2.
- G-10: Added multi-frame `frame-mode` propagation rule to §5 (first frame wins).
- G-11: Added unary minus restriction note to §13.3 — use `0 - x` workaround.
- G-12: Updated §3 EBNF `<named-color>` comment to specify CSS Color Level 3 (147 names).

### 2026-04-27 18:04:59 — Fix M-N1 through L-N10 (all 10 new issues from v2.6 re-verification)
- M-N1: Added single-background-per-frame constraint to §7 — more than one `background()` call in a frame is a validation error with message pattern.
- M-N2: Added GRAY colorspace conversion note to §15.1 — CCIR 601 luminance weighting `Y = 0.299×R + 0.587×G + 0.114×B`; alpha channel discarded.
- M-N3: Added `em`-outside-font-context note to §15.3 — resolves to default 12px when used outside a `font` primitive.
- L-N4: Expanded §18.2 angle normalisation row to explicitly name `rotate`, `start-angle`, and `end-angle` parameters.
- L-N5: Updated §8.0 `scale` row to state that negative values are not supported and result in a validation error.
- L-N6: Updated §12.2 `clip-shape` row to clarify it accepts fixed keywords (`circle`, `square`, `polygon`), not user-defined template names.
- L-N7: Added static-pattern-rendering note to §9.6 — when `animated=false`, pattern tiles statically without advancing between frames.
- L-N8: Added recursion policy to §13.1 — direct and indirect recursion is not supported; triggers runtime error.
- L-N9: Added §17.9 (polygon and pie) and §17.10 (arc) annotated examples.
- L-N10: Rewrote §14 frames-in-included-files sentence — frame definitions in included files are ignored; only `begin_obj` and `begin_func` definitions are imported.

### 2026-04-27 17:19:56 — Fix L-11 through L-18 (all remaining LOW issues)
- L-11: Added §17.8 with a full annotated `path` primitive example (open zigzag polyline and a dashed path).
- L-12: Updated §8.0 `skew-x`/`skew-y` descriptions to state positive direction (right / downward).
- L-13: Added `z-index` out-of-range row to §18.2 — value clamped to 0–1000 with a warning message.
- L-14: Added duplicate-key constraint comment to `<named-param-list>` EBNF rule in §3; added duplicate-parameter-key error row to §18.1.
- L-15: Clarified §8.7 and §18.1 — `fill` on `arc` is a parse error for **any** value including `fill=none`.
- L-16: Added division-by-zero runtime error note to §13.3 with message pattern.
- L-17: Added rounded-corner note to §8.3 — `corner-radius` is not supported; all `square` corners are sharp.
- L-18: Added per-primitive opacity note to §8.0 — no `opacity` transform param; use `RGBA()` color values instead; `opacity` is image/background-only.

### 2026-04-27 15:28:20 — Fix M-08 / M-09 / M-10
- M-08: Added `label-font-style` (`normal`) and `label-font-weight` (`normal`) rows to the §16.2 default values table.
- M-09: Added **Case sensitivity** callout block to §2.8 — all keywords and named color tokens are case-sensitive lowercase; user-defined identifiers are also case-sensitive.
- M-10: Added **Global Namespace** subsection to §4 stating that frame names, object names, and function names share one namespace; duplicate name is a parse error; includes participate in the same namespace. Added corresponding note to §13.1.

### 2026-04-27 15:26:59 — Fix M-07: Describe `step` connector routing algorithm in §9.2
- Replaced the single-line `step` description in the §9.2 table with a dedicated algorithm block: H-V-H routing between each pair of points via the midpoint x-coordinate; noted that `corner`/`corner-radius` apply to all right-angle turns.
- Updated `curved` description to name the spline type (Catmull-Rom).

### 2026-04-27 15:25:05 — Fix M-06: Define error for unrecognised parameter keys
- Added validation note to the `<named-param-list>` EBNF rule in §3 stating that unrecognised keys are a parse error.
- Added `Unrecognised parameter key` row to the §18.1 parse-error table with its message pattern.

### 2026-04-27 15:24:01 — Fix M-05: State `include` top-level-only restriction in §14 prose
- Added a placement-restriction callout block to §14 stating that `include` is only permitted at the top level and that placing it inside any block body is a parse error.

### 2026-04-27 15:20:15 — Fix H-04: Document multi-line text rendering in §10
- Added **Multi-line text rendering** block to §10 specifying: `pos` anchors the first-line baseline; line spacing = `font-size × 1.2`; `align` applies per-line; no line limit (clipped at canvas edge); no automatic word-wrap.
- Annotated the existing multi-line example with the baseline calculation.

### 2026-04-27 15:18:24 — Fix H-03: Add `align` parameter to `font` primitive
- Added `align` (`left` | `center` | `right`, default `left`) to the `font` primitive syntax block, parameter table, and `pos` description.
- Added two usage examples (center-aligned label, right-aligned value).
- Added `align (font)` row to the §16.2 default values table.

### 2026-04-25 13:06:57 — Fix H-02: Add `image` keyword disambiguation notes to §2.8, §6, §11
- Added a disambiguation block to §2.8 explaining that `image` without `(` is the canvas statement (§6) and `image(` is the drawing primitive (§11), resolved by first lookahead character.
- Added cross-reference notes to §6 and §11 pointing to the §2.8 disambiguation rule.

### 2026-04-25 13:05:18 — Fix H-01: Add output file naming subsection to §6
- Added `### Output File Naming` subsection to §6 documenting the naming rule for each `output-format` value (`png`, `jpeg`, `gif`, `images`); covers script-name derivation, per-frame naming for `images` mode, duplicate frame-id warning, and explicit output-path override semantics.

### 2026-04-25 12:43:00 — Fix Issues 21-31 from semantic correctness review
- Issue 21 (High): Corrected §8.0 transform application order — replaced undefined `translate` with `position`; added clarifying note that position comes from each primitive's own `pos`/`center`/`start`/`points` parameter.
- Issue 22 (High): Added identifier-hyphen disambiguation rule in §2.5 and §13.3 — maximal-munch for identifiers; subtraction `-` requires a preceding space in expression contexts.
- Issue 23 (Medium): Added circular-include detection rule to §14 and §18.1 error table.
- Issue 24 (Medium): Updated EBNF `<param-names>` and `<arg-list>` to allow zero items (zero-parameter functions and zero-argument calls now valid).
- Issue 25 (Medium): Clarified `%` unit behaviour in §15.3 when object template declares no `width`/`height` — resolves to canvas dimensions.
- Issue 26 (Medium): Corrected §15.1 — `none` on stroke is a **semantic error**, not a parse error (grammar allows it; validation rejects it); added corresponding entry to §18.1 error table.
- Issue 27 (Medium): Added mutual-exclusivity rule to §9.1 — providing both `points` and `start`/`end` is a parse error; added to §18.1 error table.
- Issue 28 (Medium): Added function argument count mismatch entry to §18.1 error table.
- Issue 29 (Low): Corrected type description of `hold-time` (§5) and `dpi` (§6) from `integer` to `number`; added note that decimal values are truncated to integer.
- Issue 30 (Low): Rewrote §12.4 first sentence — "all drawing-command coordinates inside an object template" are relative to the object's origin (not just nested objects).
- Issue 31 (Low): Added `fill` on `line` and `fill` on `path` error entries to §18.1 error table.

### 2026-04-25 12:08:40 — Fix Issues 13-20 from verification re-verification
- Issue 13: Added `<string>` EBNF production rule (`<string-char>` sub-rule) with escape-sequence support; referenced from §2.6.
- Issue 14: Added `<line-type>` EBNF production rule (`solid | dashed | dotted | dash-dot`).
- Issue 15: Added `<number>` production rule to the EBNF block (was only in §2.7 prose).
- Issue 16: Removed redundant `<number>` alternative from `<value>` rule — `<length> ::= <number> <unit>?` already subsumes bare numbers; removing avoids ambiguity.
- Issue 17: Fixed `<number-0-1>` — old rule `[0-9]* ('.' [0-9]+)?` matched empty string; replaced with two-alternative rule requiring at least one digit.
- Issue 18: Added `{n}` (exactly n repetitions) to the EBNF notation legend.
- Issue 19: Fixed unquoted `font-family=Arial` in §5, §12.5, and §17.3 examples to use proper string syntax `font-family="Arial"`.
- Issue 20: Rewrote §4 opening paragraph — removed incorrect "defined before it is used" constraint; replaced with accurate description of the two-pass model (definitions collected in Pass 1, forward references are valid).

### 2026-04-25 12:01:19 — Fix Issues 9-12 from verification re-verification
- Issue 9: Added `<expr>`, `<expr-term>`, `<expr-factor>`, `<expr-point>` EBNF rules for arithmetic expressions used in function body parameter values; added explanatory comment to `<func-decl>` rule.
- Issue 10: Added trailing `<terminator>?` to `<image-def>` rule to allow the trailing semicolons used in all examples.
- Issue 11: Updated `<frame>` and `<obj-template>` rules to use `(<frame-attr> <terminator>?)*` and `(<obj-attr> <terminator>?)*`, matching the optional-terminator pattern used for drawing commands.
- Issue 12: Removed duplicate `image` entry from §2.8 reserved keywords list.

### 2026-04-25 10:25:43 — Fix Issues 1-5 from verification report
- Issue 1: Removed undefined `<key>` token from `<frame-attr>` and `<obj-attr>` EBNF rules; replaced with explicit identifier-based alternatives.
- Issue 2: Added `shadow`, `clip-bounds`, `clip-shape` as explicit alternatives in `<obj-attr>` EBNF rule.
- Issue 3: Removed incorrect nesting of `shadow` inside `<border-value>`; `shadow` is now a standalone `<obj-attr>` alternative.
- Issue 4: Added `none` as an explicit alternative in the `<color>` EBNF rule, annotated as fill-only.
- Issue 5: Clarified `output-format` default in Section 6 parameter table and Section 16.2 defaults table — defaults to `png` for single-frame, `gif` for multi-frame.
- Issue 6: Clarified semantic difference between `transparent` (general named color, usable on any color property) and `none` (no-paint token restricted to `fill` and `background` only) in Section 15.1.
- Issue 7: Rewrote `<background-params>` EBNF rule to use `<named-param-list>` (order-independent) with a comment block documenting the three background forms and their valid keys. Removed fixed-order `<solid-bg-params>`, `<gradient-bg-params>`, `<image-bg-params>` sub-rules.
- Issue 8: Added `output-format=images` per-frame file naming convention to Section 6 parameter table (`<frame-id>.png` / `<frame-id>.jpeg`).

---

### 2026-05-07 - FEA-008: comparison expressions and bounded do ... while
- Added section 14.8: comparison-expression grammar, do ... while grammar, scope restrictions, runtime guard, and error examples
- Updated section 19.1 parse-error table with invalid loop scope, missing condition, non-comparison condition, and unsupported-operator rows
- File version 3.5 -> 3.6
*End of DSL Grammar Description — Technical Image Generator*


