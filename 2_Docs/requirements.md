# Requirements — Technical Image Generator

| Field | Value |
|---|---|
| **Description** | Structured requirements derived from the Technical Image Generator vision |
| **Created at** | 2026-04-25 09:34:59 |
| **File version** | 2.4 |
| **Created by** | Claude Sonnet 4.6 |

---

## 1. Functional Requirements

### 1.1 Script Processing

| Field | Detail |
|---|---|
| **ID** | REQ-0001 |
| **Title** | Script Processing Engine |
| **Description** | The system shall accept a DSL script file as input, parse it, and produce one or more image output files. |
| **Priority** | High |
| **Acceptance Criteria** | Given a valid DSL script, the system produces the described image file(s) without error. |
| **Dependencies** | — |

| Field | Detail |
|---|---|
| **ID** | REQ-0001.1 |
| **Title** | Single-Frame Output |
| **Description** | When the script contains exactly one frame, the system shall output a single image file in PNG, JPEG, or GIF format as specified. |
| **Priority** | High |
| **Acceptance Criteria** | A script with one `begin_frame`/`end_frame` block produces exactly one output file. |
| **Dependencies** | REQ-0001 |

| Field | Detail |
|---|---|
| **ID** | REQ-0001.2 |
| **Title** | Multi-Frame Output |
| **Description** | When the script contains two or more frames, the system shall output either an animated GIF (default) or separate image files named `<frame-id>.png` / `<frame-id>.jpeg`, depending on `output-format`. |
| **Priority** | High |
| **Acceptance Criteria** | A script with N frames and `output-format=gif` produces one animated GIF; with `output-format=images` produces N separate image files. |
| **Dependencies** | REQ-0001, REQ-0003 |

---

### 1.2 Frame Definition

| Field | Detail |
|---|---|
| **ID** | REQ-0002 |
| **Title** | Frame Declaration |
| **Description** | The system shall support frame blocks delimited by `begin_frame <name>` and `end_frame`. Each frame contains exactly one image-definition statement followed by drawing commands. |
| **Priority** | High |
| **Acceptance Criteria** | A script with a correctly structured `begin_frame`/`end_frame` block parses without error; an unclosed frame raises a parse error. |
| **Dependencies** | REQ-0001 |

| Field | Detail |
|---|---|
| **ID** | REQ-0002.1 |
| **Title** | Frame Hold Time |
| **Description** | Each frame shall support a `hold-time=<milliseconds>` attribute specifying how long the frame is displayed before advancing to the next frame in an animated GIF. |
| **Priority** | High |
| **Acceptance Criteria** | A GIF produced from frames with `hold-time=500` shows each frame for 500 ms. |
| **Dependencies** | REQ-0002, REQ-0001.2 |

| Field | Detail |
|---|---|
| **ID** | REQ-0002.2 |
| **Title** | Frame Mode |
| **Description** | Each frame shall support a `frame-mode=one-run|cyclic-run` attribute. `one-run` plays the GIF once and stops; `cyclic-run` loops indefinitely. The `frame-mode` of the **first** frame determines the GIF loop setting; values on subsequent frames are **silently ignored** with no warning. |
| **Priority** | Medium |
| **Acceptance Criteria** | A GIF with `frame-mode=one-run` plays once; with `frame-mode=cyclic-run` loops. Specifying `frame-mode=one-run` on a non-first frame has no effect and produces no warning. |
| **Dependencies** | REQ-0002, REQ-0001.2 |

| Field | Detail |
|---|---|
| **ID** | REQ-0002.3 |
| **Title** | Frame Colorspace |
| **Description** | Each frame shall support a `colorspace=RGB|RGBA|GRAY` setting applied to the output image. If `colorspace` appears in both the frame-level attributes and the `image` canvas statement, the **`image` statement value takes precedence** and a warning is emitted. |
| **Priority** | High |
| **Acceptance Criteria** | A frame with `colorspace=RGBA` produces an image with an alpha channel; `colorspace=GRAY` produces a grayscale image. When the same frame declares conflicting colorspace in frame attributes and the `image` statement, the `image` statement value is used and a warning is logged. |
| **Dependencies** | REQ-0002 |

---

### 1.3 Image Canvas

| Field | Detail |
|---|---|
| **ID** | REQ-0003 |
| **Title** | Image Canvas Definition |
| **Description** | The system shall support an `image` statement within each frame defining: `width`, `height`, `colorspace`, `dpi`, and `output-format`. Decimal `dpi` values are truncated to the nearest integer. In multi-frame scripts, all frames must declare the same `output-format`; if values conflict, the first frame's value is used and a warning is emitted for each conflicting frame. |
| **Priority** | High |
| **Acceptance Criteria** | A frame with `image width=600px; height=400px; colorspace=RGB; dpi=96;` produces an image of 600×400 pixels at 96 dpi. `dpi=96.7` is treated as 96. In a multi-frame script where frame 2 declares a different `output-format`, a warning is emitted and the first frame's format is used throughout. |
| **Dependencies** | REQ-0002 |

---

### 1.4 Background

| Field | Detail |
|---|---|
| **ID** | REQ-0004.1 |
| **Title** | Solid Color Background |
| **Description** | The system shall support `background(color=<color>)` to fill the canvas with a single solid color. A frame may contain **at most one** `background` statement; specifying more than one is a **validation error**. |
| **Priority** | High |
| **Acceptance Criteria** | A canvas with `background(color=white)` renders with all pixels white. A frame containing two `background` statements produces a validation error halting execution. |
| **Dependencies** | REQ-0003 |

| Field | Detail |
|---|---|
| **ID** | REQ-0004.2 |
| **Title** | Gradient Background |
| **Description** | The system shall support `background(color1=<c>, color2=<c>, start=(x1,y1), end=(x2,y2))` to render a linear gradient from `color1` at `start` to `color2` at `end`. |
| **Priority** | Medium |
| **Acceptance Criteria** | Pixels at `start` match `color1`; pixels at `end` match `color2`; intermediate pixels are linearly interpolated. If `start` and `end` are the same coordinate, the entire canvas is filled with `color1` and a warning is emitted. |
| **Dependencies** | REQ-0003 |

| Field | Detail |
|---|---|
| **ID** | REQ-0004.3 |
| **Title** | Image Background |
| **Description** | The system shall support `background(src=<path>, mode=fit|stretch|clip, x=, y=, width=, height=, opacity=)` to render an external image as the background. |
| **Priority** | Medium |
| **Acceptance Criteria** | `mode=fit` scales the image preserving aspect ratio; `mode=stretch` fills the canvas; `mode=clip` uses the region `(x,y,width,height)` of the source. `opacity` from 0 to 1 blends the background correctly. |
| **Dependencies** | REQ-0003, REQ-0032 |

| Field | Detail |
|---|---|
| **ID** | REQ-0004.4 |
| **Title** | Implicit Canvas Default State |
| **Description** | If no `background` statement is present in a frame, the canvas initial state depends on the colorspace: for `colorspace=RGBA` the canvas is **fully transparent**; for `colorspace=RGB` or `colorspace=GRAY` the canvas is **white (`#FFFFFF`)**. |
| **Priority** | Medium |
| **Acceptance Criteria** | A frame with `colorspace=RGBA` and no `background` statement produces a fully transparent PNG. A frame with `colorspace=RGB` and no `background` statement produces a white-filled image. |
| **Dependencies** | REQ-0003, REQ-0004.1 |

---

### 1.5 Drawing Primitives

| Field | Detail |
|---|---|
| **ID** | REQ-0005 |
| **Title** | Primitive: line |
| **Description** | The system shall render a straight line with parameters: `color`, `line-type`, `line-width`, `start=(x1,y1)`, `end=(x2,y2)`. Stroke only; no fill. |
| **Priority** | High |
| **Acceptance Criteria** | A `line` primitive draws a visible stroke between the two specified points with the given color, style, and width. |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0006 |
| **Title** | Primitive: circle |
| **Description** | The system shall render a circle with parameters: `color`, `line-type`, `line-width`, `fill`, `center=(xc,yc)`, `radius=r`. Supports both stroke and fill. |
| **Priority** | High |
| **Acceptance Criteria** | A `circle` primitive renders at the correct center and radius with the specified stroke and fill colors. |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0007 |
| **Title** | Primitive: square (rectangle) |
| **Description** | The system shall render a rectangle with parameters: `color`, `line-type`, `line-width`, `fill`, `pos=(x1,y1)`, `width=w`, `height=h`. Supports both stroke and fill. |
| **Priority** | High |
| **Acceptance Criteria** | A `square` primitive renders at `pos` with the given dimensions, stroke, and fill. |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0008 |
| **Title** | Primitive: polygon |
| **Description** | The system shall render a closed polygon with parameters: `color`, `line-type`, `line-width`, `fill`, `points=[(x1,y1),(x2,y2),...,(xn,yn)]`. Minimum 3 points; path is auto-closed. Supports both stroke and fill. |
| **Priority** | High |
| **Acceptance Criteria** | A `polygon` with 3+ points renders a closed shape. Fewer than 3 points raises a parse error. |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0009 |
| **Title** | Primitive: path |
| **Description** | The system shall render an open path (curve) with parameters: `color`, `line-type`, `line-width`, `points=[(x1,y1),(x2,y2),(x3,y3),...]`. Minimum 2 points; path is not closed. Stroke only; no fill. |
| **Priority** | High |
| **Acceptance Criteria** | A `path` with 2+ points renders an open stroke through all points. Fewer than 2 points raises a parse error. |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0010 |
| **Title** | Primitive: pie |
| **Description** | The system shall render a pie slice with parameters: `color`, `line-type`, `line-width`, `fill`, `center=(xc,yc)`, `radius=r`, `start-angle=degrees`, `end-angle=degrees`. Supports both stroke and fill. |
| **Priority** | Medium |
| **Acceptance Criteria** | A `pie` primitive renders an arc from `start-angle` to `end-angle` with lines to the center, correct radius, stroke, and fill. The arc is always drawn **clockwise**. If `start-angle >= end-angle` after normalisation (modulo 360), the arc sweeps clockwise through the full 360°. If `start-angle == end-angle` after normalisation, nothing is rendered. |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0010.1 |
| **Title** | Primitive: arc |
| **Description** | The system shall render an open curved arc with parameters: `color`, `line-type`, `line-width`, `center=(xc,yc)`, `radius=r`, `start-angle=degrees`, `end-angle=degrees`. The arc is the curved line segment only — no lines are drawn to the center and no fill is supported. Stroke only. |
| **Priority** | Medium |
| **Acceptance Criteria** | An `arc` primitive renders only the curved portion between `start-angle` and `end-angle` at the given radius. No lines connect the arc endpoints to the center. Specifying `fill` on an `arc` is a **parse error** — this applies to any `fill` value, including `fill=none`. The arc sweep direction follows the same clockwise rule and normalisation as `pie` (REQ-0010). |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

---

### 1.6 Connector Primitive

| Field | Detail |
|---|---|
| **ID** | REQ-0011 |
| **Title** | Primitive: connector |
| **Description** | The system shall render connector primitives that link two or more points. Stroke only; no fill. |
| **Priority** | High |
| **Acceptance Criteria** | A `connector` primitive with valid parameters renders a visible stroke between its points. |
| **Dependencies** | REQ-0003, REQ-0020, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.1 |
| **Title** | Connector Multi-Segment Points |
| **Description** | A connector shall accept `points=[(x1,y1),(x2,y2),...,(xn,yn)]` with a minimum of 2 vertices. Two points produce a single-segment connector; three or more produce a multi-segment connector. The shorthand `start=(x1,y1), end=(x2,y2)` is accepted as an alias for a two-point `points` list. |
| **Priority** | High |
| **Acceptance Criteria** | A connector with 3 points renders two connected segments. A connector with `start=` / `end=` is equivalent to a connector with `points=[(x1,y1),(x2,y2)]`. Fewer than 2 points raises a parse error. Specifying both `points` and `start`/`end` in the same call is a parse error. Specifying only `start` without `end` (or only `end` without `start`) is also a parse error. |
| **Dependencies** | REQ-0011 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.2 |
| **Title** | Connector Type |
| **Description** | A connector shall support `connector-type=straight|curved|step`. `straight` draws straight line segments; `curved` draws a smooth spline through the points; `step` draws axis-aligned right-angle segments between points. Default is `straight`. |
| **Priority** | High |
| **Acceptance Criteria** | `connector-type=curved` renders a smooth curve passing through all points; `connector-type=step` renders only horizontal/vertical segments. |
| **Dependencies** | REQ-0011.1 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.3 |
| **Title** | Connector Caps |
| **Description** | A connector shall support `start-cap` and `end-cap` parameters specifying the shape drawn at the first and last point respectively. Valid values: `none`, `triangle`, `open-triangle`, `circle`, `filled-circle`, `diamond`, `filled-diamond`, `square`, `filled-square`. Default is `none`. The aliases `start-arrow` and `end-arrow` are accepted for backward compatibility. |
| **Priority** | High |
| **Acceptance Criteria** | A connector with `end-cap=triangle` renders a filled triangle arrowhead at the end point oriented toward the connector direction. Each cap type renders its correct shape. Specifying both `start-cap` and `start-arrow` (or both `end-cap` and `end-arrow`) in the same call is a **parse error**. |
| **Dependencies** | REQ-0011 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.4 |
| **Title** | Connector Cap Size |
| **Description** | A connector shall support `cap-size=small|medium|large` (default=`medium`) to control cap dimensions proportionally to `line-width`. Per-end overrides `start-cap-size` and `end-cap-size` are also supported. |
| **Priority** | Medium |
| **Acceptance Criteria** | `cap-size=large` renders caps visibly larger than `cap-size=small`. `start-cap-size=small, end-cap-size=large` renders different sizes at each end. |
| **Dependencies** | REQ-0011.3 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.5 |
| **Title** | Connector Corner Style |
| **Description** | A connector shall support `corner=sharp|rounded|beveled` applied at each intermediate vertex of a multi-segment connector. `sharp` renders the exact vertex; `rounded` renders a circular arc tangent to both segments; `beveled` renders a straight cut. `corner-radius` sets the arc radius for `rounded` (default=5px). |
| **Priority** | Medium |
| **Acceptance Criteria** | A 3-point connector with `corner=rounded` renders a smooth arc at the intermediate vertex. `corner=beveled` renders a chamfered corner. `corner=sharp` renders a pointed corner. `corner` and `corner-radius` are **silently ignored** when `connector-type=curved`. |
| **Dependencies** | REQ-0011.1 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.6 |
| **Title** | Connector Label |
| **Description** | A connector shall support an optional text label via the `label` parameter. Label position is controlled by `label-pos=start|center|end` (default=`center`). Position offset is adjusted with `label-offset=(dx,dy)`. Label font is configured via `label-font-family`, `label-font-size`, `label-font-color`, `label-font-style`, `label-font-weight`. |
| **Priority** | Medium |
| **Acceptance Criteria** | A connector with `label="data"` and `label-pos=center` renders the text "data" at the midpoint of the connector. `label-offset=(0,-10)` shifts it 10px upward. |
| **Dependencies** | REQ-0011, REQ-0012 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.7 |
| **Title** | Connector Animation Flag |
| **Description** | A connector shall support `animated=true|false` (default=`false`). When `true`, the connector's pattern moves across frames in a multi-frame GIF, producing a rolling/flowing visual effect. Requires multi-frame GIF output. |
| **Priority** | Medium |
| **Acceptance Criteria** | A connector with `animated=true` in a multi-frame GIF renders the pattern shifted by `pattern-speed` pixels per frame. A static image with `animated=true` renders identically to `animated=false`. |
| **Dependencies** | REQ-0011, REQ-0001.2 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.8 |
| **Title** | Connector Pattern |
| **Description** | A connector shall support a configurable repeating pattern via: `pattern=dash|dot|arrow|zigzag` (default=`dash`), `pattern-length=<px>` (default=8px), `pattern-gap=<px>` (default=4px), `pattern-color=<color>` (defaults to connector `color`). The pattern replaces the plain stroke. |
| **Priority** | Medium |
| **Acceptance Criteria** | `pattern=dot` renders evenly spaced dots along the connector. `pattern-length=16, pattern-gap=8` renders longer units with larger gaps. `pattern-color=red` renders the pattern in red independently of the connector base color. |
| **Dependencies** | REQ-0011 |

| Field | Detail |
|---|---|
| **ID** | REQ-0011.9 |
| **Title** | Connector Pattern Speed |
| **Description** | A connector shall support `pattern-speed=<px>` (default=4px) specifying how many pixels the pattern advances per frame in an animated GIF. Pattern travels from `start` toward `end` of the connector. |
| **Priority** | Medium |
| **Acceptance Criteria** | In a 5-frame GIF, a connector with `pattern-speed=4` shifts the pattern by 4px per frame. The pattern wraps around seamlessly. |
| **Dependencies** | REQ-0011.7, REQ-0011.8 |

---

### 1.7 Font / Text Primitive

| Field | Detail |
|---|---|
| **ID** | REQ-0012 |
| **Title** | Primitive: font (text) |
| **Description** | The system shall render text with parameters: `font-family`, `font-size`, `color`, `style=normal|italic`, `weight=normal|bold`, `text=<string>`, `pos=(x,y)`. `font-family` supports a fallback chain (e.g., `"Arial, Helvetica, sans-serif"`). System defaults: `serif`, `sans-serif`, `monospace`. Final fallback is system monospace. |
| **Priority** | High |
| **Acceptance Criteria** | Text renders at the specified position with the specified font. If `font-family=Arial` is unavailable, the next font in the fallback chain is used. If no fallback resolves, system monospace is used. |
| **Dependencies** | REQ-0003, REQ-0020 |

---

### 1.8 Image Primitive

| Field | Detail |
|---|---|
| **ID** | REQ-0013 |
| **Title** | Primitive: image |
| **Description** | The system shall render an embedded image with parameters: `src=<path>`, `pos=(x,y)`, `width=w`, `height=h`, `opacity=0–1`. If only one of `width`/`height` is given, the other auto-scales to preserve aspect ratio. Supports transforms (rotate, skew, scale). |
| **Priority** | Medium |
| **Acceptance Criteria** | An `image` primitive renders the source file at the given position and dimensions. Specifying only `width=100` scales height proportionally. `opacity=0.5` renders the image at 50% transparency. |
| **Dependencies** | REQ-0003, REQ-0017, REQ-0032 |

---

### 1.9 Object Templates

| Field | Detail |
|---|---|
| **ID** | REQ-0014 |
| **Title** | Object Template Definition |
| **Description** | The system shall support object template blocks defined with `begin_obj <name>` … `end_obj`. Templates may contain base attributes (`width`, `height`, `background`), border properties, and any drawing primitives. |
| **Priority** | High |
| **Acceptance Criteria** | An object template is defined once and can be instantiated multiple times. The definition block itself does not render anything. |
| **Dependencies** | REQ-0003 |

| Field | Detail |
|---|---|
| **ID** | REQ-0014.1 |
| **Title** | Object Instantiation and Parameter Override |
| **Description** | Objects are instantiated using `<name>(pos=(x,y), <override-params>)`. Instance parameters override template defaults; unspecified parameters inherit template defaults. |
| **Priority** | High |
| **Acceptance Criteria** | `card(pos=(100,100))` renders the card at (100,100) with all template defaults. `card(pos=(200,200), background=blue)` uses blue background, all other attributes from the template. |
| **Dependencies** | REQ-0014 |

| Field | Detail |
|---|---|
| **ID** | REQ-0014.2 |
| **Title** | Clipping and Masking |
| **Description** | Objects shall support `clip-bounds=(x1,y1,x2,y2)` for rectangular clipping and `clip-shape=<shape>` for shape-based clipping. Valid `clip-shape` values are `circle` (clips to an ellipse inscribed in the bounding box) and `square` (clips to the bounding box rectangle). `clip-shape=polygon` is **not** supported and shall produce a validation error. When both `clip-bounds` and `clip-shape` are specified, the effective clip region is the **intersection** of the two areas. Content outside the clip region is not rendered. |
| **Priority** | Low |
| **Acceptance Criteria** | A circle at (50,50) with `clip-bounds=(0,0,30,30)` renders only the portion inside the bounds. `clip-shape=circle` clips all content to a circular mask. `clip-shape=square` clips to the bounding box. `clip-shape=polygon` produces a validation error. When both `clip-bounds` and `clip-shape` are specified, only content inside both clip regions is rendered. |
| **Dependencies** | REQ-0014 |

| Field | Detail |
|---|---|
| **ID** | REQ-0014.3 |
| **Title** | Nested Objects |
| **Description** | Objects may contain other objects. Nested objects use a local coordinate system relative to the parent object's origin. Nested objects inherit parent properties unless explicitly overridden. |
| **Priority** | Medium |
| **Acceptance Criteria** | A nested object at `pos=(10,10)` inside a parent at `pos=(100,100)` renders at absolute position (110,110). |
| **Dependencies** | REQ-0014 |

| Field | Detail |
|---|---|
| **ID** | REQ-0014.4 |
| **Title** | Object Border Shadow |
| **Description** | Objects shall support a `shadow` border attribute defined as `shadow(offset-x offset-y blur-radius color)`. The shadow is rendered behind the object border using the specified offsets, blur radius, and color. |
| **Priority** | Medium |
| **Acceptance Criteria** | An object with `border: solid 2px black; shadow: 4px 4px 6px rgba(0,0,0,0.5);` renders a visible blurred shadow offset 4px right and 4px down from the object border. Shadow with `blur-radius=0` renders a hard-edged shadow. Shadow color supports all valid color formats including RGBA transparency. |
| **Dependencies** | REQ-0014, REQ-0020 |

---

### 1.10 Function Declarations

| Field | Detail |
|---|---|
| **ID** | REQ-0015 |
| **Title** | Function Declaration |
| **Description** | The system shall support reusable function blocks: `begin_func <name>(<param1>, <param2>, ...) <drawing-commands> end_func`. Functions encapsulate drawing logic parameterized by the declared variables. |
| **Priority** | High |
| **Acceptance Criteria** | A function defined once can be called multiple times with different arguments producing different rendered results. Recursion (direct or indirect re-entry of the same function) is not supported and shall halt execution with a runtime error identifying the recursive function name. |
| **Dependencies** | REQ-0003 |

| Field | Detail |
|---|---|
| **ID** | REQ-0015.1 |
| **Title** | Function Parameter Expressions |
| **Description** | Function parameters shall be usable in arithmetic expressions within the function body (e.g., `pos=(x+10, y+5)`). |
| **Priority** | Medium |
| **Acceptance Criteria** | `begin_func btn(x,y) square(pos=(x+2,y+2), ...) end_func` places the square offset by (2,2) from the call-site argument. |
| **Dependencies** | REQ-0015 |

| Field | Detail |
|---|---|
| **ID** | REQ-0015.2 |
| **Title** | Function Composition |
| **Description** | Functions shall be allowed to call other functions and instantiate object templates, enabling complex reusable components. |
| **Priority** | Medium |
| **Acceptance Criteria** | A function that calls another function renders the composed result correctly. |
| **Dependencies** | REQ-0015, REQ-0014 |

| Field | Detail |
|---|---|
| **ID** | REQ-0015.3 |
| **Title** | Function Expression Constraints |
| **Description** | Arithmetic expressions in function bodies are subject to two constraints: (1) **Division by zero** — if a `/` expression evaluates to a zero denominator at call time, execution halts with a runtime error. (2) **Unary minus** — unary negation (e.g., `-x`) is not supported; to negate a value, subtract from zero: `0 - x`. |
| **Priority** | Medium |
| **Acceptance Criteria** | A function body with `radius=r/0` halts with a division-by-zero runtime error when called. A function body using unary minus (e.g., `-x` without a left-hand operand) produces a parse error. |
| **Dependencies** | REQ-0015.1 |

---

### 1.11 Script File Inclusion

| Field | Detail |
|---|---|
| **ID** | REQ-0016 |
| **Title** | Script Inclusion |
| **Description** | The system shall support `include "<path>"` to include another DSL file. All function and object definitions from the included file are available in the including script. |
| **Priority** | Medium |
| **Acceptance Criteria** | A script that includes a file defining `button(...)` can call `button(...)` as if it were defined locally. A name collision between an included definition and a local definition (or between two included definitions) produces a **parse error**. |
| **Dependencies** | REQ-0015, REQ-0014 |

| Field | Detail |
|---|---|
| **ID** | REQ-0016.1 |
| **Title** | Include Path Resolution |
| **Description** | Include paths shall be resolved as relative (relative to the including DSL file) or absolute. |
| **Priority** | Medium |
| **Acceptance Criteria** | `include "components/buttons.dsl"` resolves relative to the current script's directory. |
| **Dependencies** | REQ-0016 |

| Field | Detail |
|---|---|
| **ID** | REQ-0016.2 |
| **Title** | Recursive Includes |
| **Description** | Included files may themselves include other DSL files. There is no depth limit on include nesting. |
| **Priority** | Low |
| **Acceptance Criteria** | A 3-level deep chain of includes resolves all definitions correctly. |
| **Dependencies** | REQ-0016 |

---

### 1.12 Transformations

| Field | Detail |
|---|---|
| **ID** | REQ-0017 |
| **Title** | Primitive and Object Transformations |
| **Description** | Any drawable primitive or object shall support optional transform parameters: `rotate=<degrees>` (0–360), `skew-x=<degrees>`, `skew-y=<degrees>`, `scale=<multiplier>`. Transforms are applied around the element's center in the order: translate → scale → skew → rotate. |
| **Priority** | Medium |
| **Acceptance Criteria** | A `circle` with `rotate=45` is visually rotated 45° about its center. A `square` with `scale=2.0` renders at twice its original size. Multiple transforms compose correctly. |
| **Dependencies** | REQ-0003 |

---

### 1.13 Z-Order / Layering

| Field | Detail |
|---|---|
| **ID** | REQ-0018 |
| **Title** | Z-Order Layering |
| **Description** | Primitives are rendered in declaration order: first-declared is bottommost, last-declared is topmost. An optional `z-index=<0–1000>` parameter overrides the default declaration-order stacking. |
| **Priority** | Medium |
| **Acceptance Criteria** | A circle declared before a square is rendered below the square. Setting `z-index=1000` on the circle places it above the square regardless of declaration order. |
| **Dependencies** | REQ-0003 |

---

### 1.14 DSL Language Features

| Field | Detail |
|---|---|
| **ID** | REQ-0019 |
| **Title** | Coordinate System |
| **Description** | The origin (0,0) shall be at the top-left of the canvas. The x-axis increases rightward; the y-axis increases downward. |
| **Priority** | High |
| **Acceptance Criteria** | A primitive at `pos=(0,0)` appears at the top-left corner of the output image. |
| **Dependencies** | REQ-0003 |

| Field | Detail |
|---|---|
| **ID** | REQ-0020 |
| **Title** | Color Format Support |
| **Description** | The system shall accept colors in four formats: `RGB(r,g,b)`, `RGBA(r,g,b,a)`, hex `#RRGGBB`, and named colors (e.g., `black`, `white`, `red`, `blue`, `green`). Any color parameter also accepts a palette alias reference `@<alias>` defined via a `begin_palette` block (REQ-0040.2); the reference is resolved to its concrete color value at parse time. An unrecognized color format shall halt parsing with an error. The special value `none` is valid only for `fill` and `background` properties; using `none` as a stroke `color` (e.g., `color=none`) is a **semantic error**. The value `transparent` (equivalent to `RGBA(0,0,0,0)`) is a standard named color valid on **any** color property — stroke, fill, or background. |
| **Priority** | High |
| **Acceptance Criteria** | Each of the four direct formats parses and renders the same visual color. `color=@primary` where `primary` is a defined palette alias resolves to its color value. An invalid format (e.g., `color=badval`) produces a parse error. `color=none` on a stroke property produces a semantic error halting execution. `color=transparent` is valid everywhere and renders an invisible stroke/fill. |
| **Dependencies** | REQ-0040.2 |

| Field | Detail |
|---|---|
| **ID** | REQ-0020.1 |
| **Title** | Greyscale Color Conversion |
| **Description** | When `colorspace=GRAY` is used, all color values (named, hex, RGB, RGBA) shall be converted to a single-channel luminance value using **CCIR 601 weighting**: `Y = 0.299 × R + 0.587 × G + 0.114 × B`. The alpha channel is discarded during conversion; use `colorspace=RGBA` to preserve transparency. |
| **Priority** | Low |
| **Acceptance Criteria** | A `colorspace=GRAY` frame with `fill=RGB(255,0,0)` renders a grey shade at luminance `Y ≈ 76` (0.299 × 255). An RGBA color's alpha component is ignored in GRAY output. |
| **Dependencies** | REQ-0003, REQ-0020 |

| Field | Detail |
|---|---|
| **ID** | REQ-0021 |
| **Title** | Unit Measurements |
| **Description** | Numeric parameters shall accept units: `px` (pixels), `pt` (points), `em` (relative to font size), `cm` (centimeters), `mm` (millimeters), `%` (percentage of parent width for x, parent height for y). Omitting a unit defaults to `px`. |
| **Priority** | High |
| **Acceptance Criteria** | `width=2cm` converts to the correct pixel equivalent. `pos=(50%,50%)` places the element at the center of the canvas. No-unit values are treated as pixels. |
| **Dependencies** | REQ-0003 |

| Field | Detail |
|---|---|
| **ID** | REQ-0022 |
| **Title** | Line Type Styles |
| **Description** | All stroke-capable primitives shall support `line-type=solid|dashed|dotted|dash-dot`. An unrecognized value shall halt parsing with an error. |
| **Priority** | High |
| **Acceptance Criteria** | `line-type=dashed` renders a dashed stroke. An invalid value (e.g., `line-type=wavy`) produces a parse error. |
| **Dependencies** | — |

| Field | Detail |
|---|---|
| **ID** | REQ-0023 |
| **Title** | String Handling and Escaping |
| **Description** | String values shall be enclosed in double quotes. Supported escape sequences: `\"` (quote), `\\` (backslash), `\n` (newline), `\t` (tab). Input is UTF-8 encoded. |
| **Priority** | Medium |
| **Acceptance Criteria** | `text="Line 1\nLine 2"` renders two lines of text. `text="Say \"hello\""` renders `Say "hello"`. Non-ASCII UTF-8 characters render correctly. |
| **Dependencies** | — |

| Field | Detail |
|---|---|
| **ID** | REQ-0024 |
| **Title** | Statement Delimiters |
| **Description** | Inside frames and objects, statements shall be terminated by a newline or a semicolon. Both styles may be mixed. Whitespace (spaces, tabs, extra newlines) is ignored except as a statement terminator. |
| **Priority** | High |
| **Acceptance Criteria** | `width=100px; height=200px; colorspace=RGB;` on a single line is parsed identically to the same attributes on separate lines. |
| **Dependencies** | — |

| Field | Detail |
|---|---|
| **ID** | REQ-0025 |
| **Title** | Type Validation and Error Handling |
| **Description** | The system shall validate parameter types at parse time and emit descriptive errors as follows: invalid color format → error halts; negative numeric values (radius, width) → validation error; invalid `line-type` → error halts; insufficient points (path<2, polygon<3) → error halts; out-of-bounds coordinates → silently clipped to canvas bounds; negative `scale` → validation error; `scale=0` → valid, renders element as invisible; duplicate parameter key in one call → parse error. |
| **Priority** | High |
| **Acceptance Criteria** | `color=notacolor` stops execution with a descriptive message. `radius=-5` triggers a validation error. `points=[(0,0)]` on a path triggers an insufficient-points error. A primitive positioned off-canvas renders the visible portion only. `scale=-1` triggers a validation error. `scale=0` renders without error but produces nothing visible. `circle(color=black, color=red, ...)` triggers a duplicate-parameter parse error. |
| **Dependencies** | REQ-0020, REQ-0022, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0025.1 |
| **Title** | Optional Parameter Defaults and Named-Parameter Ordering |
| **Description** | The system shall apply the following default values when optional parameters are omitted: `fill=none` (transparent), `z-index=declaration-order`, `style=normal`, `weight=normal`, `line-width=1px`, `font-size=12px`, `line-type=solid`. Named parameters shall be accepted in any order within a parameter list. |
| **Priority** | High |
| **Acceptance Criteria** | A `circle` with no `fill` parameter renders with a transparent fill. A `font` with no `style` or `weight` renders as normal/non-bold. `z-index` of a primitive with no explicit value equals its declaration position. The calls `line(color=black, line-width=1px, start=(0,0), end=(10,10))` and `line(start=(0,0), end=(10,10), line-width=1px, color=black)` produce identical output. |
| **Dependencies** | REQ-0025 |

---

### 1.15 Encoding

| Field | Detail |
|---|---|
| **ID** | REQ-0035 |
| **Title** | DSL File UTF-8 Encoding |
| **Description** | The system shall open all DSL script files (main input and all files loaded via `include`) using explicit UTF-8 encoding. If a file cannot be decoded as valid UTF-8, execution shall halt with an I/O error (exit code 3) that identifies the file path and the approximate byte position of the first invalid byte. |
| **Priority** | High |
| **Acceptance Criteria** | A DSL file saved as UTF-8 containing Hungarian characters (ő, ű, á, é, etc.) renders those characters correctly in the output image. A file saved with a non-UTF-8 encoding (e.g., Windows-1252) that contains non-ASCII bytes produces a descriptive I/O error and halts execution without producing any output. |
| **Dependencies** | REQ-0001, REQ-0016 |

| Field | Detail |
|---|---|
| **ID** | REQ-0035.1 |
| **Title** | UTF-8 BOM Handling |
| **Description** | If a DSL file begins with a UTF-8 byte-order mark (BOM, U+FEFF), the BOM shall be silently stripped before parsing. The BOM shall not cause a parse error and shall not appear as a character in any string value. |
| **Priority** | Medium |
| **Acceptance Criteria** | A DSL file saved as "UTF-8 with BOM" (as produced by some Windows editors) parses and renders identically to the same file saved as UTF-8 without BOM. |
| **Dependencies** | REQ-0035 |

---

### 1.16 Object Instance Size and Rotation

| Field | Detail |
|---|---|
| **ID** | REQ-0036 |
| **Title** | Object Instance Explicit Size Override |
| **Description** | At object instantiation, optional `width=<value>` and `height=<value>` parameters override the template dimensions for that instance only. All other template attributes remain unchanged. |
| **Priority** | Medium |
| **Acceptance Criteria** | `card(pos=(100,100), width=300px, height=80px)` renders with 300×80 dimensions regardless of the template's declared width/height. Omitting either parameter keeps the corresponding template default. |
| **Dependencies** | REQ-0014.1 |

| Field | Detail |
|---|---|
| **ID** | REQ-0036.1 |
| **Title** | Object Instance Scale Factor |
| **Description** | At object instantiation, an optional `scale=<multiplier>` parameter applies uniform scaling to the template dimensions for that instance. The scale factor must be a positive non-zero number. |
| **Priority** | Medium |
| **Acceptance Criteria** | `card(pos=(100,100), scale=1.6)` renders the card at 1.6× its template dimensions. `scale=0` is a validation error (must be > 0 for object instance scaling). Negative `scale` is a validation error. |
| **Dependencies** | REQ-0014.1, REQ-0017 |

| Field | Detail |
|---|---|
| **ID** | REQ-0036.2 |
| **Title** | Object Instance Size Precedence |
| **Description** | When both explicit `width`/`height` and `scale` are provided in the same instantiation call, explicit `width`/`height` takes precedence over `scale`. A warning is emitted when both are specified simultaneously. |
| **Priority** | Medium |
| **Acceptance Criteria** | `card(pos=(0,0), width=200px, height=100px, scale=2.0)` renders at 200×100 (not 2× template size) and emits a warning that `scale` is ignored when explicit dimensions are provided. |
| **Dependencies** | REQ-0036, REQ-0036.1 |

**Default behavior note:** REQ-0036 through REQ-0036.2 define the current default object-instance sizing path where explicit `width` and `height` imply proportional scaling of internal geometry. The opt-in alternative is defined by REQ-0044 through REQ-0044.3.

| Field | Detail |
|---|---|
| **ID** | REQ-0037 |
| **Title** | Object Instance Rotation |
| **Description** | At object instantiation, an optional `rotate=<degrees>` parameter rotates the entire object clockwise by the specified degrees, applied around the object's center following the same transform rules as REQ-0017. If not specified, no rotation is applied. |
| **Priority** | Medium |
| **Acceptance Criteria** | `card(pos=(100,100), rotate=45)` renders the card rotated 45° clockwise about its center. `rotate=0` or omitting `rotate` renders the card without rotation. Negative `rotate` values are a validation error. |
| **Dependencies** | REQ-0014.1, REQ-0017 |

---

### 1.17 Grid System

| Field | Detail |
|---|---|
| **ID** | REQ-0038 |
| **Title** | Grid Definition |
| **Description** | The system shall support an optional `grid()` statement within each frame defining: `step-x=<value>`, `step-y=<value>`, and optionally `offset-x=<value>`, `offset-y=<value>` for origin shift. The grid is non-visual by default. At most one `grid` statement is allowed per frame; specifying more than one is a validation error. If no `grid` statement is present, all existing behavior is unchanged. |
| **Priority** | Medium |
| **Acceptance Criteria** | A frame with `grid(step-x=50px, step-y=50px)` defines a 50×50 grid without any visible change to the output. A frame with two `grid` statements produces a validation error. A script without any `grid` statement renders identically to current behavior. |
| **Dependencies** | REQ-0002, REQ-0003, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0038.1 |
| **Title** | Grid Visual Rendering |
| **Description** | The system shall support `render=true` on the `grid()` statement to draw grid lines over the canvas after all other drawing commands. When `render=true`, the visual style shall be configurable via `color=<color>`, `line-type=<type>`, and `line-width=<value>`. If `render=true` is specified without `color`, a warning is emitted and the grid defaults to `RGB(200,200,200)`. Default: `render=false`. |
| **Priority** | Low |
| **Acceptance Criteria** | A frame with `grid(step-x=50px, step-y=50px, render=true, color=gray, line-type=dashed, line-width=1px)` produces an output image with visible dashed gray lines at 50px intervals drawn on top of all other primitives. When `render=false` or `render` is omitted, no grid lines appear. |
| **Dependencies** | REQ-0038, REQ-0020, REQ-0022, REQ-0021 |

| Field | Detail |
|---|---|
| **ID** | REQ-0038.2 |
| **Title** | Global Grid Alignment |
| **Description** | The system shall support `align=true` on the `grid()` statement to globally snap all drawable elements in the frame to the nearest grid intersection. Default: `align=false`. |
| **Priority** | Medium |
| **Acceptance Criteria** | With `grid(step-x=50px, step-y=50px, align=true)`, a circle placed at `center=(63,48)` is automatically snapped to `(50,50)` before rendering. When `align=false` or `align` is omitted, no snapping is performed and element positions are used as-is. |
| **Dependencies** | REQ-0038, REQ-0017 |

| Field | Detail |
|---|---|
| **ID** | REQ-0038.3 |
| **Title** | Per-Element Snap |
| **Description** | Any drawable primitive or object shall support an optional `snap=grid-intersection\|grid-x\|grid-y\|none` parameter. `grid-intersection` snaps both x and y to the nearest grid intersection. `grid-x` snaps only the x position to the nearest vertical grid line; y is unchanged. `grid-y` snaps only the y position to the nearest horizontal grid line; x is unchanged. `snap=none` explicitly opts that element out of snapping, overriding a global `align=true`. A per-element `snap` value overrides the global `align` setting for that element. Using `snap` without a defined `grid` statement in the frame is a validation error. |
| **Priority** | Medium |
| **Acceptance Criteria** | A circle with `snap=grid-x` is snapped horizontally to the nearest vertical grid line while its vertical position is unchanged. `snap=grid-y` snaps only vertical position. `snap=grid-intersection` snaps both axes. `snap=none` on an element inside a frame with `align=true` leaves that element at its original position. Using `snap` in a frame with no `grid` statement is a validation error. |
| **Dependencies** | REQ-0038, REQ-0038.2 |

| Field | Detail |
|---|---|
| **ID** | REQ-0038.4 |
| **Title** | Alignment and Transform Order |
| **Description** | Grid alignment (whether global via `align=true` or per-element via `snap=`) shall be resolved before applying any transforms to the element. The resolution order is: snap position to grid → apply transforms (position → scale → skew → rotate). The grid coordinate system is auxiliary and does not modify the canvas coordinate system (REQ-0019). |
| **Priority** | High |
| **Acceptance Criteria** | A rotated object with `snap=grid-intersection` has its pre-rotation position snapped to the nearest grid point; the rotation is then applied around that snapped center. The canvas coordinate origin (0,0) and axis directions are unaffected by the presence of a grid. |
| **Dependencies** | REQ-0038, REQ-0038.2, REQ-0038.3, REQ-0017, REQ-0019 |

---

### 1.20 Variable Support and Bounding Box Extraction

| Field | Detail |
|---|---|
| **ID** | REQ-0041 |
| **Title** | Variable Declaration |
| **Description** | The system shall support variable declarations inside frame and function bodies using the syntax `var <name> (',' <name>)* ';'`. Declared variables are scoped to the enclosing frame or function block. Frame-scoped and function-scoped variable namespaces are independent. Variable names must follow standard identifier rules (letters, digits, underscores; must not begin with a digit). Declaring a variable name that conflicts with an existing function or object template name is a parse error. |
| **Priority** | Medium |
| **Acceptance Criteria** | `var x, y;` inside a `begin_frame` block declares two frame-scoped variables. `var width;` inside a `begin_func` block declares a function-scoped variable. Redeclaring a name already declared in the same scope is a parse error. A variable declared in a frame is not visible inside a function called from that frame. |
| **Dependencies** | REQ-0002, REQ-0015 |

| Field | Detail |
|---|---|
| **ID** | REQ-0041.1 |
| **Title** | Bounding Box Property Access |
| **Description** | Every drawable element shall expose a read-only bounding box after it has been rendered, accessible via `<name>.bbox.x`, `<name>.bbox.y`, `<name>.bbox.width`, `<name>.bbox.height`. The bounding box is the final axis-aligned bounding box (AABB) computed after the full transform pipeline (scale, skew, rotate). Bbox properties are available on all drawable elements: all primitives, connectors, `font`/text, `image` primitives, and object instances. Accessing `.bbox` on an element that has not yet been rendered in the current execution sequence is a runtime error. Accessing `.bbox` on a non-drawable construct is a parse error. |
| **Priority** | Medium |
| **Acceptance Criteria** | After `square(pos=(50,50), width=120, height=60);`, the expression `square.bbox.x` evaluates to `50`, `square.bbox.y` to `50`, `square.bbox.width` to `120`, `square.bbox.height` to `60`. For a `square` with `rotate=45`, `.bbox.width` and `.bbox.height` reflect the AABB of the rotated shape (wider and taller than the original). Referencing `rect1.bbox.x` before `rect1` is drawn halts execution with a runtime error. |
| **Dependencies** | REQ-0041, REQ-0039.1, REQ-0017 |

| Field | Detail |
|---|---|
| **ID** | REQ-0041.2 |
| **Title** | Variable Assignment from Bounding Box |
| **Description** | The system shall support assignment statements of the form `<var-name> = <object-name>.bbox.<property> ;` inside frame and function bodies. The right-hand side must be a `.bbox` property access. The assigned variable must have been declared with `var` in the same scope; assigning to an undeclared name is a parse error. Reassignment of a previously assigned variable is allowed. |
| **Priority** | Medium |
| **Acceptance Criteria** | `bx = rect1.bbox.x;` stores the x-coordinate of `rect1`'s bounding box into `bx`. A second `bx = rect2.bbox.x;` in the same scope overwrites the value. `bx = rect1.bbox.x;` where `bx` was not declared with `var` is a parse error. |
| **Dependencies** | REQ-0041, REQ-0041.1 |

| Field | Detail |
|---|---|
| **ID** | REQ-0041.3 |
| **Title** | Variable Usage in Parameter Expressions |
| **Description** | Declared variables shall be usable in arithmetic parameter expressions anywhere a numeric value is accepted, using the same expression operators supported for function parameters (`+`, `-`, `*`, `/`). This applies to all named parameter values in primitives, object instantiations, and function calls within the same scope. Division by zero involving a variable at execution time is a runtime error. Unary minus on a variable is not supported; subtract from zero instead. |
| **Priority** | Medium |
| **Acceptance Criteria** | `square(pos=(bx + bw + 10, by), width=50, height=50);` correctly places the square using stored bbox values. `circle(center=(bx + 60, by + 30), radius=30, ...);` evaluates the expression at render time. Using a variable before it has been assigned a value (declared but not yet assigned) in an expression is a runtime error. |
| **Dependencies** | REQ-0041, REQ-0041.2, REQ-0015.1, REQ-0015.3 |

| Field | Detail |
|---|---|
| **ID** | REQ-0041.4 |
| **Title** | Sequential Execution Model for Variables |
| **Description** | Within a frame or function body, statements shall be executed sequentially. The engine shall process each statement in order: render the element, compute its bounding box, store any assigned values into the variable space, and proceed to the next statement. Variables hold their last assigned value for all subsequent statements in the same scope. |
| **Priority** | Medium |
| **Acceptance Criteria** | Given three statements in order — draw `rect1`, assign `bx = rect1.bbox.x`, draw `circle` using `bx` — the circle is placed correctly using `rect1`'s computed x position. Reversing the order so that `bx` is used before `rect1` is drawn produces a runtime error (undefined variable value). |
| **Dependencies** | REQ-0041.2, REQ-0041.3 |

| Field | Detail |
|---|---|
| **ID** | REQ-0041.5 |
| **Title** | Variable Error Handling |
| **Description** | The system shall enforce the following error conditions: (1) Using an undefined variable name in an expression → parse error. (2) Accessing `.bbox` on an element before it is rendered → runtime error with the element name and line number. (3) Circular variable dependencies (a variable's value chain depends on itself) → runtime error. (4) Assigning to a name not declared with `var` → parse error. The error message shall include file name, line number, and variable or element name. |
| **Priority** | High |
| **Acceptance Criteria** | `pos=(undeclared_var + 10, 50)` where `undeclared_var` was never declared produces a parse error. `bx = rect1.bbox.x;` before `rect1` is drawn produces a runtime error referencing the line and element name. A circular chain (e.g., `var a; a = b.bbox.x; b.pos` depends on `a`) produces a runtime error. |
| **Dependencies** | REQ-0041, REQ-0041.1, REQ-0041.2, REQ-0025, REQ-0031 |

### 1.21 Comparison Expressions and Bounded Looping

| Field | Detail |
|---|---|
| **ID** | REQ-0042 |
| **Title** | Numeric Comparison Expressions |
| **Description** | The DSL shall support numeric comparison expressions formed by two arithmetic expressions and one comparison operator. Supported operators are `==`, `!=`, `<`, `<=`, `>`, and `>=`. Comparison expressions produce a boolean result and are evaluated after arithmetic sub-expressions are resolved. |
| **Priority** | High |
| **Acceptance Criteria** | Conditions such as `i < 5`, `counter <= max_count`, `current_x + width > limit`, and `gap != 0` parse and evaluate correctly. Unsupported operators produce a parse error with file and line information. |
| **Dependencies** | REQ-0015.1, REQ-0041.3 |

| Field | Detail |
|---|---|
| **ID** | REQ-0042.1 |
| **Title** | Comparison Expression Scope |
| **Description** | Comparison expressions shall be valid at least in `do ... while` loop conditions. The arithmetic expression system remains unchanged and comparison is added as a higher-level condition form on top of numeric expression evaluation. |
| **Priority** | Medium |
| **Acceptance Criteria** | A `do ... while` condition such as `while i < 5;` parses as a comparison expression while existing arithmetic-only parameter expressions continue to work unchanged. |
| **Dependencies** | REQ-0042, REQ-0028 |

| Field | Detail |
|---|---|
| **ID** | REQ-0042.2 |
| **Title** | Comparison Expression Error Handling |
| **Description** | A malformed comparison expression, missing operand, or unsupported comparison operator shall produce a parse error that includes file name and line number. A `do ... while` condition that is not a comparison expression shall also be rejected as a parse error. |
| **Priority** | High |
| **Acceptance Criteria** | `while i;`, `while i <> 5;`, and `while < 5;` each fail with a descriptive parse error that points to the condition. |
| **Dependencies** | REQ-0042, REQ-0031 |

| Field | Detail |
|---|---|
| **ID** | REQ-0043 |
| **Title** | Bounded `do ... while` Loop |
| **Description** | The DSL shall support a `do ... while` loop construct that executes the loop body once before evaluating the comparison condition. The body then repeats while the condition remains true. |
| **Priority** | High |
| **Acceptance Criteria** | A frame containing `do ... while` can draw a repeated series of elements. A loop with initial `i = 0` and condition `i < 5` executes exactly five times when the body increments `i` by one. |
| **Dependencies** | REQ-0042, REQ-0042.1 |

| Field | Detail |
|---|---|
| **ID** | REQ-0043.1 |
| **Title** | Loop Scope Restriction |
| **Description** | `do ... while` shall be allowed only inside `begin_frame` / `end_frame` bodies and `begin_func` / `end_func` bodies. The construct shall be rejected at top-level script scope and inside `begin_obj` / `end_obj` and `begin_palette` / `end_palette` bodies. |
| **Priority** | High |
| **Acceptance Criteria** | A loop inside a frame body parses. A loop inside a function body parses. A loop at top level, in an object template body, or in a palette body produces a clear parse error. |
| **Dependencies** | REQ-0043, REQ-0028 |

| Field | Detail |
|---|---|
| **ID** | REQ-0043.2 |
| **Title** | Loop Body Statement Support |
| **Description** | Inside an allowed `do ... while` body, the engine shall support the same sequential statements already valid in the containing scope, including variable declarations where permitted, variable assignments, primitive drawing commands, named primitive drawing commands, bbox access after render, function calls, and object instances where already valid in that scope. |
| **Priority** | Medium |
| **Acceptance Criteria** | A loop body can increment a counter, draw primitives, assign bbox-derived values after a named primitive is rendered, and call a function or instantiate an object when those operations are valid in the surrounding scope. |
| **Dependencies** | REQ-0041, REQ-0041.1, REQ-0041.2, REQ-0041.4, REQ-0043 |

| Field | Detail |
|---|---|
| **ID** | REQ-0043.3 |
| **Title** | Maximum Iteration Guard |
| **Description** | Every `do ... while` loop shall be protected by a fixed maximum iteration guard of 1000 iterations. If a loop exceeds this limit, execution halts with a runtime error that includes the file name, line number, and the configured guard value. |
| **Priority** | High |
| **Acceptance Criteria** | A loop whose condition never becomes false halts with an error in the form `<file>:<line>: error: do-while loop exceeded maximum iteration count 1000`. |
| **Dependencies** | REQ-0043, REQ-0031 |

| Field | Detail |
|---|---|
| **ID** | REQ-0043.4 |
| **Title** | Loop Example Coverage |
| **Description** | The project documentation and example-script set shall include 4 to 6 focused scripts demonstrating comparison expressions and bounded loops, including repeated drawing in frames, repeated drawing in functions, bbox-driven loop chaining, comparison-operator coverage, and an optional guard-failure example. |
| **Priority** | Medium |
| **Acceptance Criteria** | Example scripts `93_loop_basic_circles.dsl`, `94_loop_repeated_rectangles.dsl`, `95_loop_with_bbox_chaining.dsl`, `96_loop_in_function.dsl`, and `97_loop_comparison_operators.dsl` are added. `98_loop_guard_error_example.dsl` may be included as a negative example and clearly marked as such. |
| **Dependencies** | REQ-0042, REQ-0043 |

| Field | Detail |
|---|---|
| **ID** | REQ-0043.5 |
| **Title** | Backward Compatibility for Loop Feature |
| **Description** | Existing DSL scripts that do not use comparison expressions or `do ... while` loops shall continue to parse and render unchanged. The new feature shall be additive and shall not alter the behavior of existing arithmetic expressions, frames, functions, objects, palettes, or rendering order outside the scopes where sequential execution is already required. |
| **Priority** | High |
| **Acceptance Criteria** | Existing example scripts and previously valid user scripts render identically when they do not use the new constructs. |
| **Dependencies** | REQ-0042, REQ-0043, REQ-0041.4 |

---

## 2. Non-Functional Requirements

| Field | Detail |
|---|---|
| **ID** | REQ-0026 |
| **Title** | Implementation Language |
| **Description** | The entire system shall be implemented in Python. |
| **Priority** | High |
| **Acceptance Criteria** | The tool runs using a standard Python interpreter (no compiled native code required). |
| **Dependencies** | — |

| Field | Detail |
|---|---|
| **ID** | REQ-0027 |
| **Title** | Supported Output Formats |
| **Description** | The system shall be capable of producing output images in PNG, JPEG, and GIF (including animated GIF) formats. |
| **Priority** | High |
| **Acceptance Criteria** | A script targeting each format produces a valid file of that format, verified by an image viewer or `file` command. |
| **Dependencies** | REQ-0001 |

---

## 3. Data Requirements

| Field | Detail |
|---|---|
| **ID** | REQ-0028 |
| **Title** | DSL Script Grammar |
| **Description** | The DSL shall follow the defined grammar: `<script> := <top-level-stmt>+`; `<top-level-stmt> := <frame> \| <func-decl> \| <obj-template> \| <include-stmt> \| <palette-def>`; `<palette-def> := 'begin_palette' <name> <color-entry>+ 'end_palette'`; `<color-entry> := <name> '=' <color-value>`; `<frame> := 'begin_frame' <name> <image-def> <drawing-commands> 'end_frame'`; `<image-def> := 'image' <key>=<value> (';' <key>=<value>)*`; `<drawing-commands> := (<primitive> \| <object-inst> \| <func-call> \| <var-decl> \| <var-assign> \| <loop-stmt>)+`; `<var-decl> := 'var' <name> (',' <name>)* ';'`; `<var-assign> := <name> '=' <bbox-access> ';'`; `<bbox-access> := <name> '.' 'bbox' '.' ('x' \| 'y' \| 'width' \| 'height')`; `<loop-stmt> := 'do' <drawing-commands> 'while' <comparison-expr> ';'`; `<comparison-expr> := <expr> <comp-op> <expr>`; `<comp-op> := '==' \| '!=' \| '<' \| '<=' \| '>' \| '>='`; `<primitive> := <prim-type> '(' <param-list> ')'`; `<param-list> := <name>=<value> (',' <name>=<value>)*`; `<obj-template> := 'begin_obj' <name> <attributes> <drawing-commands> 'end_obj'`; `<object-inst> := <name> '(' <param-list> ')'`; `<func-decl> := 'begin_func' <name> '(' <param-names> ')' <drawing-commands> 'end_func'`; `<param-names> := <name> (',' <name>)*`; `<func-call> := <name> '(' <arg-list> ')'`; `<arg-list> := <value> (',' <value>)*`; `<include-stmt> := 'include' '"' <path> '"'`. |
| **Priority** | High |
| **Acceptance Criteria** | Any script conforming to the grammar parses without error. A script with a top-level `begin_func`/`end_func` block parses and makes the function callable in frames. A script with `include "path"` makes all definitions from the included file available. A frame with `var x, y;` declares two variables; `x = rect1.bbox.x;` assigns the computed bbox value. Any script deviating from the grammar produces a descriptive parse error. |
| **Dependencies** | REQ-0001, REQ-0015, REQ-0016, REQ-0041 |

| Field | Detail |
|---|---|
| **ID** | REQ-0029 |
| **Title** | Output File Naming |
| **Description** | Single-frame output uses the filename specified at invocation. Multi-frame `output-format=gif` produces a single `.gif` file. Multi-frame `output-format=images` produces one file per frame: frames with `colorspace=RGBA` or `colorspace=GRAY` always produce `.png`; frames with `colorspace=RGB` produce `.jpeg`. If two frames share the same frame ID, the second file **overwrites** the first (frame IDs should be unique). |
| **Priority** | High |
| **Acceptance Criteria** | A 3-frame script with `output-format=images` produces 3 files named after each frame ID. An RGBA or GRAY frame in `images` mode produces `<frame-id>.png`. An RGB frame produces `<frame-id>.jpeg`. A duplicate frame ID causes the second output file to silently overwrite the first. |
| **Dependencies** | REQ-0001.2 |

---

## 4. UI/UX Requirements

| Field | Detail |
|---|---|
| **ID** | REQ-0030 |
| **Title** | Command-Line Interface |
| **Description** | The system shall be invoked from the command line, accepting a DSL script file path and an output file path as arguments. |
| **Priority** | High |
| **Acceptance Criteria** | Running `python imagegen.py input.dsl output.png` produces the described image. Missing or invalid arguments produce a usage message. |
| **Dependencies** | REQ-0001 |

| Field | Detail |
|---|---|
| **ID** | REQ-0031 |
| **Title** | Error Messages |
| **Description** | All parse and rendering errors shall produce a human-readable message that includes the error type, file name, and line number where the error occurred. |
| **Priority** | Medium |
| **Acceptance Criteria** | An error in `main.dsl` at line 12 produces a message referencing `main.dsl:12` with a description of the problem. |
| **Dependencies** | REQ-0025 |

---

### 4.2 Font Discovery Command

| Field | Detail |
|---|---|
| **ID** | REQ-0034 |
| **Title** | Font Discovery CLI Command |
| **Description** | The system shall provide a `--list-fonts` CLI flag that enumerates all fonts installed on the current system and prints a structured report to stdout, one entry per font family. When `--list-fonts` is specified, no DSL script is processed and no image is produced. |
| **Priority** | Medium |
| **Acceptance Criteria** | Running `python imagegen.py --list-fonts` prints the font report to stdout and exits with code 0. Specifying both `--list-fonts` and an `<input-file>` produces a usage error and exits with code 1. |
| **Dependencies** | REQ-0030 |

| Field | Detail |
|---|---|
| **ID** | REQ-0034.1 |
| **Title** | Font Name Output for DSL Use |
| **Description** | Each font entry in the `--list-fonts` report shall include the exact `font-family` name string that can be used in DSL `font(font-family=...)` calls to render that font. |
| **Priority** | Medium |
| **Acceptance Criteria** | A name printed by `--list-fonts` can be pasted verbatim into a DSL script's `font-family` parameter and resolves to that font without error. |
| **Dependencies** | REQ-0034, REQ-0012 |

| Field | Detail |
|---|---|
| **ID** | REQ-0034.2 |
| **Title** | Font Style Enumeration |
| **Description** | For each font family the report shall list only the style variants that are physically present on the system: `normal`, `bold`, `italic`, `bold-italic`. Variants with no corresponding font file on the system shall not be reported. |
| **Priority** | Medium |
| **Acceptance Criteria** | A font family that has Regular and Bold files but no Italic file reports `Styles: normal, bold`. All four variants are reported only when all four files exist. |
| **Dependencies** | REQ-0034 |

| Field | Detail |
|---|---|
| **ID** | REQ-0034.3 |
| **Title** | Font Size Information |
| **Description** | For scalable (TrueType / OpenType / vector) fonts the report shall state `scalable`. For bitmap fonts the report shall list each distinct available pixel size as a comma-separated list of integers. |
| **Priority** | Low |
| **Acceptance Criteria** | A TrueType font reports `Sizes: scalable`. A bitmap font with sizes 8, 10, 12 reports `Sizes: 8, 10, 12`. |
| **Dependencies** | REQ-0034 |

| Field | Detail |
|---|---|
| **ID** | REQ-0034.4 |
| **Title** | Hungarian Glyph Detection |
| **Description** | For each font family the report shall indicate `yes` if at least one of the family's variant files contains glyphs for all 18 Hungarian-specific characters, or `no` otherwise. Required code points: Á U+00C1, á U+00E1, É U+00C9, é U+00E9, Í U+00CD, í U+00ED, Ó U+00D3, ó U+00F3, Ö U+00D6, ö U+00F6, Ő U+0150, ő U+0151, Ú U+00DA, ú U+00FA, Ü U+00DC, ü U+00FC, Ű U+0170, ű U+0171. |
| **Priority** | Medium |
| **Acceptance Criteria** | A font containing all 18 code points in at least one variant reports `Hungarian: yes`. A font missing even one of the 18 characters in every variant reports `Hungarian: no`. |
| **Dependencies** | REQ-0034 |

---

## 5. Integration Requirements

| Field | Detail |
|---|---|
| **ID** | REQ-0032 |
| **Title** | External Image Asset Support |
| **Description** | The system shall load external image files (PNG, JPEG, GIF, SVG) for use in `background(src=...)` and `image(src=...)` primitives. Relative paths are resolved relative to the DSL script file. |
| **Priority** | Medium |
| **Acceptance Criteria** | A script referencing `src=assets/logo.png` loads the image from the path relative to the DSL file. An unreachable `src` path produces a descriptive error. |
| **Dependencies** | REQ-0004.3, REQ-0013 |

| Field | Detail |
|---|---|
| **ID** | REQ-0033 |
| **Title** | Modular Script Composition via Inclusion |
| **Description** | The include mechanism shall allow DSL scripts to import function and object definitions from other DSL files, enabling reusable component libraries. |
| **Priority** | Medium |
| **Acceptance Criteria** | A component library DSL file included in multiple scripts makes its functions and objects available in all including scripts without re-declaration. |
| **Dependencies** | REQ-0016 |

---

### 1.18 Bounding Box Visualization

| Field | Detail |
|---|---|
| **ID** | REQ-0039 |
| **Title** | Optional Bounding Box Parameter |
| **Description** | Any drawable primitive, object instance, font/text element, image primitive, or connector shall support an optional `show-bbox=true\|false` parameter. Default is `false`. When `true`, the engine renders the axis-aligned bounding box of the element as a visual overlay on the canvas. The parameter is accepted in any position within the named-parameter list following existing conventions. Using `show-bbox` on a non-drawable construct (e.g., `begin_frame`, `image` canvas statement, `begin_obj` template body) is a **parse error**. |
| **Priority** | Low |
| **Acceptance Criteria** | A `circle` with `show-bbox=true` renders a bounding box overlay. A `circle` with `show-bbox=false` or without the parameter renders with no bounding box. All existing scripts without `show-bbox` render identically to current behavior. `show-bbox` on a `begin_frame` statement is a parse error. |
| **Dependencies** | REQ-0017, REQ-0003 |

| Field | Detail |
|---|---|
| **ID** | REQ-0039.1 |
| **Title** | Transformed Bounding Box Geometry |
| **Description** | The bounding box shall represent the **final transformed** axis-aligned bounding box (AABB) of the element, computed after all transforms (scale, skew, rotate from REQ-0017) have been applied. The AABB fully encloses the rendered pixel extents of the element on the canvas. |
| **Priority** | Low |
| **Acceptance Criteria** | A `square` with `rotate=45` shows a bounding box that fully encloses the rotated square (wider and taller than the original square). A `circle` with `scale=2.0` shows a bounding box twice the diameter of the default. A non-transformed element has a bounding box equal to its natural geometry. |
| **Dependencies** | REQ-0039, REQ-0017 |

| Field | Detail |
|---|---|
| **ID** | REQ-0039.2 |
| **Title** | Overlay Rendering — No Layout Impact |
| **Description** | The bounding box shall be drawn as a canvas overlay after the element itself is rendered. It shall not affect the position or size of any element, shall not participate in z-index ordering, and shall not clip or modify any other element. |
| **Priority** | Low |
| **Acceptance Criteria** | Enabling `show-bbox=true` on any element does not alter the position, size, or appearance of any other element. The bounding box always appears visually on top of the element it belongs to. |
| **Dependencies** | REQ-0039, REQ-0018 |

| Field | Detail |
|---|---|
| **ID** | REQ-0039.3 |
| **Title** | Contrast-Aware Bounding Box Color |
| **Description** | The bounding box color shall be automatically computed to maximize visual contrast against the canvas background within the element's AABB region. The algorithm shall use inverted luminance: sample the average luminance of the background pixels in the AABB region and produce the complementary luminance value as a greyscale color. The computed color is not user-configurable. |
| **Priority** | Low |
| **Acceptance Criteria** | A bounding box over a predominantly white background region renders in a near-black color. A bounding box over a predominantly dark background region renders in a near-white color. The same element on the same canvas always produces the same bbox color (deterministic). |
| **Dependencies** | REQ-0039, REQ-0020 |

| Field | Detail |
|---|---|
| **ID** | REQ-0039.4 |
| **Title** | Bounding Box Line Style |
| **Description** | The bounding box shall be drawn as a dashed 1-pixel-wide rectangle. The line style and width are fixed and not user-configurable. |
| **Priority** | Low |
| **Acceptance Criteria** | All bounding boxes render as dashed-line rectangles. No solid-line or user-defined-width bounding box is produced regardless of other parameters on the same element. |
| **Dependencies** | REQ-0039, REQ-0022 |

| Field | Detail |
|---|---|
| **ID** | REQ-0039.5 |
| **Title** | Applicability to All Drawable Elements |
| **Description** | The `show-bbox` parameter shall be accepted uniformly by: all primitives (`line`, `circle`, `square`, `polygon`, `path`, `pie`, `arc`), connectors, `font`/text elements, `image` primitives, and object instances. It is not accepted on non-drawable constructs. |
| **Priority** | Low |
| **Acceptance Criteria** | `show-bbox=true` applied to each of the listed drawable element types individually renders the correct AABB for that element. A `line` bbox encloses the line stroke. A `circle` bbox is a square enclosing the full circle. A `font` element bbox encloses the rendered text extent. A connector bbox encloses the full connector path including any caps. |
| **Dependencies** | REQ-0039, REQ-0005, REQ-0006, REQ-0007, REQ-0008, REQ-0009, REQ-0010, REQ-0010.1, REQ-0011, REQ-0012, REQ-0013, REQ-0014.1 |

| Field | Detail |
|---|---|
| **ID** | REQ-0039.6 |
| **Title** | Backward Compatibility |
| **Description** | When `show-bbox` is omitted from any drawable element (the default `false`), the rendering output shall be **identical** to output produced before this feature was introduced. No bounding boxes shall appear in any output image unless `show-bbox=true` is explicitly specified. |
| **Priority** | High |
| **Acceptance Criteria** | All existing DSL scripts that do not use `show-bbox` produce bit-for-bit identical output images before and after this feature is implemented. |
| **Dependencies** | REQ-0039 |

---

### 1.19 Named Color Palette Support

| Field | Detail |
|---|---|
| **ID** | REQ-0040 |
| **Title** | Palette Block Definition |
| **Description** | The system shall support `begin_palette <name>` … `end_palette` blocks at the script top level to declare named color aliases. Multiple palette blocks are allowed per script. Palette names must be unique across all loaded scripts; a duplicate palette name is a parse error. A `begin_palette` block with no entries is a parse error. |
| **Priority** | Medium |
| **Acceptance Criteria** | A script with a valid `begin_palette` / `end_palette` block parses without error. Two `begin_palette` blocks sharing the same palette name produce a parse error. A `begin_palette` block containing zero entries produces a parse error. |
| **Dependencies** | REQ-0028 |

| Field | Detail |
|---|---|
| **ID** | REQ-0040.1 |
| **Title** | Palette Color Entries |
| **Description** | Each line inside a palette block shall define one color alias: `<alias> = <color_value>`. The `<color_value>` must be a valid color expression accepted by REQ-0020 (named, hex, RGB, RGBA). Alias names must be unique across all palettes in scope (local and included); a duplicate alias name is a parse error. |
| **Priority** | Medium |
| **Acceptance Criteria** | `primary = RGB(35,66,200)` defines alias `primary` with the given color. `bg = #F5F5F5` defines alias `bg` as the hex color. An entry with an invalid color value (e.g., `accent = badcolor`) produces a parse error. Two entries sharing the same alias name in any combination of loaded palettes produce a parse error. |
| **Dependencies** | REQ-0040, REQ-0020 |

| Field | Detail |
|---|---|
| **ID** | REQ-0040.2 |
| **Title** | Palette Color Reference Syntax |
| **Description** | Any color parameter in any DSL statement shall accept a palette reference using `@<alias>` syntax. The `@<alias>` value is resolved to the corresponding color value at parse time. The `@` prefix is a reserved sigil for palette references and is not used for any other purpose in the DSL. |
| **Priority** | Medium |
| **Acceptance Criteria** | `color=@primary` in a `circle` primitive resolves to the color assigned to alias `primary`. `fill=@accent` resolves the fill color from the palette. `color=@undefined_alias` where the alias has not been defined in any loaded palette is a parse error. A string value such as `text="user@email.com"` is unaffected — `@` is only interpreted as a palette reference in color parameter values. |
| **Dependencies** | REQ-0040.1, REQ-0020 |

| Field | Detail |
|---|---|
| **ID** | REQ-0040.3 |
| **Title** | Palette Global Scope |
| **Description** | All palette definitions in the script (including those from included files) shall be collected into a single global alias namespace during Pass 1. Aliases are available in all frames, function bodies, and object template bodies throughout the script. |
| **Priority** | Medium |
| **Acceptance Criteria** | A palette defined before `begin_frame` blocks is accessible inside all frame drawing commands. A palette defined in any included file is accessible in the including script's frames and functions. |
| **Dependencies** | REQ-0040, REQ-0016 |

| Field | Detail |
|---|---|
| **ID** | REQ-0040.4 |
| **Title** | Palette in Included Files |
| **Description** | Palette blocks defined in included DSL files are merged into the global alias namespace. Alias name collisions between a local palette and an included palette, or between two included palettes, are a parse error. |
| **Priority** | Medium |
| **Acceptance Criteria** | Including a file that defines `begin_palette brand_colors ... end_palette` makes all its aliases available in the including script. Defining alias `primary` both locally and in an included file produces a parse error. |
| **Dependencies** | REQ-0040.1, REQ-0040.3, REQ-0016 |

| Field | Detail |
|---|---|
| **ID** | REQ-0040.5 |
| **Title** | Undefined Palette Reference Error |
| **Description** | Referencing an alias that has not been defined in any loaded palette (`@<undefined>`) shall produce a parse error that halts execution. The error message shall include the file name, line number, and the unresolved alias name. |
| **Priority** | High |
| **Acceptance Criteria** | A script using `color=@nonexistent` where `nonexistent` is not defined in any palette produces a parse error such as `main.dsl:12: error: undefined palette alias '@nonexistent'`. |
| **Dependencies** | REQ-0040.2, REQ-0025, REQ-0031 |

| Field | Detail |
|---|---|
| **ID** | REQ-0040.6 |
| **Title** | Backward Compatibility |
| **Description** | Scripts that do not contain any `begin_palette` block shall parse and render identically to behavior before this feature was introduced. The `@` sigil is only interpreted as a palette reference in color parameter values and has no other effect on parsing. |
| **Priority** | High |
| **Acceptance Criteria** | All existing DSL scripts without palette blocks produce bit-for-bit identical output before and after this feature is implemented. |
| **Dependencies** | REQ-0040 |

---

### 1.22 Decoupled Object Resizing and Scaling

| Field | Detail |
|---|---|
| **ID** | REQ-0044 |
| **Title** | Opt-In Layout Resize Mode for Object Instances |
| **Description** | The system shall support an explicit opt-in object-instance mode, enabled via `resize-mode=layout`, that disables implicit geometry scaling when `width` and/or `height` are overridden. In this mode, `width` and `height` redefine the instance bounding box and object-local layout space instead of proportionally scaling previously defined child geometry. |
| **Priority** | High |
| **Acceptance Criteria** | An object template representing a dialog or panel can be instantiated in layout-resize mode with `width=400px` and `height=240px`, and fixed-size child content such as icons or text remains at authored size while the container box grows to 400x240. |
| **Dependencies** | REQ-0014.1, REQ-0036 |

| Field | Detail |
|---|---|
| **ID** | REQ-0044.1 |
| **Title** | Explicit Scale Remains Available in Layout Resize Mode |
| **Description** | When layout-resize mode is enabled, `scale=<multiplier>` shall remain the explicit mechanism for geometric scaling. In this mode, `scale` may be combined with `width` and `height`; it shall not be ignored merely because explicit dimensions are present. |
| **Priority** | High |
| **Acceptance Criteria** | An object instance created in layout-resize mode with explicit `width`, `height`, and `scale=1.25` uses the requested bounding box for layout calculations and still applies the explicit 1.25x geometric scaling step. No warning is emitted solely because both explicit dimensions and `scale` are present in this mode. |
| **Dependencies** | REQ-0044, REQ-0036.1 |

| Field | Detail |
|---|---|
| **ID** | REQ-0044.2 |
| **Title** | Backward-Compatible Default Sizing Behavior |
| **Description** | When the new layout-resize mode is not explicitly enabled, object instantiation shall retain the current behavior defined by REQ-0036 through REQ-0036.2. Existing scripts that override object `width` and `height` without opting into the new mode shall behave identically to prior releases. |
| **Priority** | High |
| **Acceptance Criteria** | Existing DSL scripts that use object-instance `width` or `height` overrides but do not enable layout-resize mode produce identical output before and after this feature is introduced. |
| **Dependencies** | REQ-0044, REQ-0036, REQ-0036.2 |

| Field | Detail |
|---|---|
| **ID** | REQ-0044.3 |
| **Title** | Layout-Driven Reflow in Layout Resize Mode |
| **Description** | In layout-resize mode, object-local expressions and attributes that depend on instance `width`, `height`, or derived bounding-box values shall resolve against the resized bounding box so borders, anchors, nested objects, and other layout-driven content can stretch or reposition without forcing uniform scaling of fixed-size content. |
| **Priority** | High |
| **Acceptance Criteria** | A dialog object with width-dependent border geometry and centered title placement reflows correctly when resized from 300px to 500px wide in layout-resize mode, while a fixed-size icon declared inside the object keeps its authored size. |
| **Dependencies** | REQ-0044, REQ-0041, REQ-0014 |

---
## Changelog

### 2026-04-25 09:47:37 — Fix Issue 1: wrong dependencies on REQ-0004.3 and REQ-0013
- REQ-0004.3 Dependencies: replaced `REQ-0033` with `REQ-0032`
- REQ-0013 Dependencies: replaced `REQ-0033` with `REQ-0032`

### 2026-04-25 09:49:09 — Fix Issue 2: add border shadow requirement
- Added REQ-0014.4 (Object Border Shadow) covering `shadow(offset-x offset-y blur-radius color)` attribute on objects with testable acceptance criteria.

### 2026-04-25 09:50:34 — Fix Issue 3: add optional parameter defaults and named-param ordering
- Added REQ-0025.1 (Optional Parameter Defaults and Named-Parameter Ordering) specifying defaults for fill, z-index, style, weight and that named parameters are order-independent.

### 2026-04-25 09:52:25 — Fix Issue 4: complete DSL grammar in REQ-0028
- Expanded `<script>` top-level rule to allow frames, func-decls, obj-templates, and include-stmts.
- Added `<func-decl>`, `<func-call>`, `<include-stmt>`, `<object-inst>` productions.
- Updated dependencies to include REQ-0015 and REQ-0016.
- Expanded acceptance criteria to cover func-decl and include parsing.

### 2026-04-25 09:56:09 — Fix Issue 5: add arc primitive
- Added REQ-0010.1 (Primitive: arc) — open curved arc, stroke only, no fill, no center lines.
- Arc primitive also added to 2_Docs/my_vision.md image primitives list.

### 2026-04-30 — Verification pass against DSL grammar description v3.0 and DSL user guide v1.0
**Updated existing requirements:**
- REQ-0002.2: Added that subsequent frames' `frame-mode` is silently ignored with no warning.
- REQ-0002.3: Added `colorspace` precedence rule — `image` statement overrides frame attribute with a warning.
- REQ-0003: Added `dpi` decimal truncation; added output-format consistency requirement (warning on conflict, first frame wins).
- REQ-0004.1: Added duplicate `background` statement = validation error.
- REQ-0004.2: Added identical `start`/`end` in gradient = fills with `color1` plus warning.
- REQ-0010: Added clockwise arc sweep direction and normalisation rules (reversed angles → 360°, equal → nothing rendered).
- REQ-0010.1: Clarified `fill=none` on `arc` is a parse error, not just "parse error or warning"; added reference to sweep direction rule.
- REQ-0011.1: Added parse error for mixing `points` with `start`/`end`; added parse error for `start` without `end` (or vice versa).
- REQ-0011.3: Added parse error for specifying both `start-cap` and `start-arrow` (or both `end-cap` and `end-arrow`) in the same call.
- REQ-0011.5: Added that `corner` and `corner-radius` are silently ignored for `connector-type=curved`.
- REQ-0014.2: Specified valid `clip-shape` values (`circle`, `square`); `polygon` = validation error; intersection semantics when both `clip-bounds` and `clip-shape` are present.
- REQ-0015: Added that recursion is detected at runtime and halts with a runtime error.
- REQ-0016: Added name collision between included and local (or two included) definitions = parse error.
- REQ-0020: Added `none`-on-stroke = semantic error; `transparent` valid everywhere.
- REQ-0025: Added negative `scale` = validation error; `scale=0` = valid/invisible; duplicate parameter key = parse error.
- REQ-0025.1: Added `line-width=1px`, `font-size=12px`, `line-type=solid` to default values list.
- REQ-0029: Clarified `images` mode filename extension rules (RGBA/GRAY → `.png`, RGB → `.jpeg`); added duplicate frame ID = silent overwrite.

**New requirements added:**
- REQ-0004.4: Implicit canvas default state — transparent for RGBA, white for RGB/GRAY when no `background` statement.
- REQ-0015.3: Function expression constraints — division by zero = runtime error; unary minus not supported.
- REQ-0020.1: Greyscale color conversion using CCIR 601 weighting formula.

### 2026-05-02 08:12:13 — FEA-001: font discovery CLI command
- Added section 4.2 Font Discovery Command: REQ-0034 (--list-fonts CLI flag), REQ-0034.1 (DSL font names), REQ-0034.2 (style enumeration), REQ-0034.3 (size info), REQ-0034.4 (Hungarian glyph detection)
- File version 1.5 → 1.6

### 2026-05-02 17:30:45 — FEA-002: UTF-8 encoding fix
- Added section 1.15 Encoding: REQ-0035 (explicit UTF-8 file reading, non-UTF-8 → I/O error), REQ-0035.1 (silent BOM strip)
- File version 1.6 → 1.7

### 2026-05-02 18:59:02 — FEA-003: optional size and rotation parameters for DSL objects
- Added section 1.16 Object Instance Size and Rotation:
  - REQ-0036 (explicit width/height override at call time)
  - REQ-0036.1 (uniform scale factor at call time)
  - REQ-0036.2 (precedence: explicit width/height over scale, with warning)
  - REQ-0037 (clockwise rotation parameter at call time)
- File version 1.7 → 1.8

### 2026-05-02 19:57:13 — FEA-004: configurable grid system
- Added section 1.17 Grid System:
  - REQ-0038 (grid definition at frame level: step-x, step-y, offset-x, offset-y; at most one per frame)
  - REQ-0038.1 (visual rendering: render=true draws grid lines; configurable color, line-type, line-width)
  - REQ-0038.2 (global alignment: align=true snaps all elements to nearest grid intersection)
  - REQ-0038.3 (per-element snap: snap=grid-intersection|grid-x|grid-y|none; snap=none overrides global align)
  - REQ-0038.4 (alignment resolved before transforms; grid is auxiliary coordinate system)
- File version 1.8 → 1.9

### 2026-05-03 09:47:19 — FEA-005: optional bounding box rendering
- Added section 1.18 Bounding Box Visualization:
  - REQ-0039 (optional show-bbox=true|false parameter on all drawable elements; default false; non-drawable use is parse error)
  - REQ-0039.1 (AABB computed from final post-transform geometry; encloses full pixel extent)
  - REQ-0039.2 (overlay rendering: no layout impact, no z-index participation, no clipping effect)
  - REQ-0039.3 (contrast-aware color via inverted luminance of background region; non-configurable)
  - REQ-0039.4 (dashed 1px line style; fixed, non-configurable)
  - REQ-0039.5 (accepted by all primitives, connectors, font/text, image, and object instances)
  - REQ-0039.6 (backward compatible: omitting show-bbox produces identical output)
- File version 1.9 → 2.0

### 2026-05-03 20:46:05 — FEA-006: named color palette support
- Updated REQ-0020 (Color Format Support): added `@<alias>` palette reference as an accepted color format; updated acceptance criteria and dependencies
- Updated REQ-0028 (DSL Script Grammar): added `<palette-def>` and `<color-entry>` productions; `<top-level-stmt>` extended with `| <palette-def>`
- Added section 1.19 Named Color Palette Support:
  - REQ-0040 (palette block: begin_palette/end_palette at script top-level; duplicate name = parse error; empty block = parse error)
  - REQ-0040.1 (color entries: `alias = color_value`; alias names unique across all palettes in scope)
  - REQ-0040.2 (`@<alias>` reference in any color parameter; resolved at parse time; `@` sigil reserved for palette refs)
  - REQ-0040.3 (global scope: aliases from all palettes available in all frames, functions, objects)
  - REQ-0040.4 (included files: palette entries merged into global namespace; name collision = parse error)
  - REQ-0040.5 (undefined alias: parse error with file:line and alias name)
  - REQ-0040.6 (backward compatible: scripts without palettes produce identical output)
- File version 2.0 → 2.1

### 2026-05-04 18:12:00 — FEA-007: variable support and bounding box extraction
- Updated REQ-0028 (DSL Script Grammar): extended `<drawing-commands>` with `<var-decl>` and `<var-assign>` productions; added `<bbox-access>` production; updated dependencies and acceptance criteria
- Added section 1.20 Variable Support and Bounding Box Extraction:
  - REQ-0041 (variable declaration: `var name, ...;` syntax; frame- and function-scoped; identifier rules; name collision = parse error)
  - REQ-0041.1 (bounding box property access: `<name>.bbox.x/y/width/height`; post-transform AABB; all drawable elements; pre-render access = runtime error)
  - REQ-0041.2 (variable assignment from bbox: `varname = obj.bbox.prop;`; must be declared; reassignment allowed; undeclared target = parse error)
  - REQ-0041.3 (variable usage in expressions: same operators as function params; division by zero = runtime error; unary minus not supported)
  - REQ-0041.4 (sequential execution model: render → bbox → assign → next statement; out-of-order use = runtime error)
  - REQ-0041.5 (error handling: undefined variable = parse error; bbox before render = runtime error; circular dependency = runtime error)
- File version 2.1 → 2.2


### 2026-05-07 21:04:48 - FEA-008: comparison expressions and bounded do ... while
- Updated REQ-0028 (DSL Script Grammar): added <loop-stmt>, <comparison-expr>, and <comp-op> productions; extended <drawing-commands> to permit loops in valid scopes
- Added section 1.21 Comparison Expressions and Bounded Looping covering REQ-0042 through REQ-0043.5
- File version 2.2 -> 2.3

### 2026-05-09 06:44:42 - FEA-009: decoupled object resizing and scaling behavior
- Clarified that REQ-0036 through REQ-0036.2 remain the default object-instance sizing behavior
- Added section 1.22 Decoupled Object Resizing and Scaling with REQ-0044 through REQ-0044.3
- Defined an explicit opt-in layout-resize mode, preserved explicit `scale` in that mode, and required backward compatibility for existing scripts
- File version 2.3 -> 2.4
