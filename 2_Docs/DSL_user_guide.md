# DSL User Guide — Technical Image Generator

| Field | Value |
|---|---|
| **Description** | Practical user guide for writing DSL scripts — concepts, examples, and common patterns |
| **Created at** | 2026-04-29 19:56:01 |
| **File version** | 1.6 |
| **Created by** | Claude Sonnet 4.6 |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Your First Script](#2-your-first-script)
3. [Script Structure](#3-script-structure)
4. [Canvas Setup](#4-canvas-setup)
5. [Backgrounds](#5-backgrounds)
6. [Drawing Shapes](#6-drawing-shapes)
7. [Text](#7-text)
8. [Connectors and Arrows](#8-connectors-and-arrows)
9. [Embedding Images](#9-embedding-images)
10. [Transforms](#10-transforms)
11. [Reusable Objects](#11-reusable-objects)
12. [Reusable Functions](#12-reusable-functions)
13. [Library Files and Include](#13-library-files-and-include)
14. [Animated GIFs](#14-animated-gifs)
15. [Grid System](#15-grid-system)
16. [Colors Reference](#16-colors-reference)
17. [Named Color Palettes](#17-named-color-palettes)
18. [Units Reference](#18-units-reference)
19. [Common Mistakes](#19-common-mistakes)
20. [Variables and Layout Chaining](#20-variables-and-layout-chaining)
21. [Comparison Expressions and Loops](#21-comparison-expressions-and-loops)

---

## 1. Introduction

The Technical Image Generator DSL is a simple text language for describing images and animations. You write a `.dsl` script, run it through the engine, and get a PNG, JPEG, or animated GIF as output.

**Key ideas:**
- Everything is inside a `begin_frame` / `end_frame` block.
- Parameters are always named: `color=black`, `radius=50px`.
- Order of parameters does not matter.
- Keywords are lowercase — `begin_frame` is valid, `Begin_Frame` is not.
- Comments start with `#`.

---

## 2. Your First Script

```
begin_frame hello
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  font(font-family="Arial", font-size=32px, color=black, weight=bold,
       text="Hello, World!", pos=(50,80));
end_frame
```

Save this as `hello.dsl`. The engine produces `hello.png` in the same folder.

**What each line does:**
- `begin_frame hello` — starts a frame named `hello`.
- `image ...` — sets the canvas size and output format.
- `background(color=white)` — fills the canvas white.
- `font(...)` — draws text at position (50, 80).
- `end_frame` — closes the frame.

---

## 3. Script Structure

A script file is a sequence of top-level blocks. There is no outer wrapper.

```
[include "..."]           # optional library imports
[begin_palette ... end_palette]  # optional named color palettes
[begin_obj ... end_obj]   # optional reusable objects
[begin_func ... end_func] # optional reusable functions
begin_frame ...
  ...
end_frame
begin_frame ...           # more frames = animated GIF
  ...
end_frame
```

| Block | Purpose |
|---|---|
| `begin_frame` / `end_frame` | One image frame (required, at least one) |
| `begin_obj` / `end_obj` | Reusable composite object template |
| `begin_func` / `end_func` | Reusable parameterized drawing function |
| `begin_palette` / `end_palette` | Named color aliases (reference with `@alias`) |
| `include "path"` | Import objects, functions, and palettes from another file |

All names (frames, objects, functions) share one global namespace — duplicates are an error. Palette alias names share a separate global namespace — duplicate aliases across any loaded palette are also an error.

---

## 4. Canvas Setup

The `image` statement is **required** inside every frame. It sets up the drawing surface.

```
image width=800px; height=600px; colorspace=RGB; dpi=96; output-format=png;
```

| Parameter | Required | Default | Notes |
|---|---|---|---|
| `width` | Yes | — | Canvas width |
| `height` | Yes | — | Canvas height |
| `colorspace` | No | `RGB` | Use `RGBA` for transparency, `GRAY` for greyscale |
| `dpi` | No | `96` | Affects pt, cm, mm unit conversion |
| `output-format` | No | `png` (single) / `gif` (multi) | `png`, `jpeg`, `gif`, or `images` |

**Output file naming:**
- `output-format=png` → `<script-name>.png`
- `output-format=gif` → `<script-name>.gif`
- `output-format=images` → one file per frame named `<frame-id>.png`

> JPEG does not support transparency — do not combine `output-format=jpeg` with `colorspace=RGBA`.

---

## 5. Backgrounds

Set the background once per frame, after the `image` statement.

### Solid color

```
background(color=white)
background(color=#F0F0F0)
background(color=RGB(240,240,240))
```

### Gradient

```
background(color1=white, color2=navy, start=(0,0), end=(800,600))
```

The color transitions linearly from `color1` at the `start` point to `color2` at the `end` point.

### Image file

```
background(src="assets/photo.jpg", mode=stretch, opacity=0.8)
background(src="tile.png", mode=fit)
background(src="photo.jpg", mode=clip, x=100, y=50, width=400, height=300)
```

| Mode | Effect |
|---|---|
| `fit` | Preserve aspect ratio, fit inside canvas (default) |
| `stretch` | Fill canvas, ignore aspect ratio |
| `clip` | Show only the sub-region defined by x, y, width, height |

> Only one `background` statement is allowed per frame.

---

## 6. Drawing Shapes

All shapes use named parameters and may appear in any order inside a frame.

### Coordinate system

- `(0, 0)` is the **top-left** corner.
- X increases rightward, Y increases downward.

### Line

```
line(color=black, line-type=solid, line-width=2px, start=(0,0), end=(300,200))
line(color=red, line-type=dashed, start=(10,10), end=(200,10))
```

`line` has stroke only — no fill.

### Circle

```
circle(color=black, fill=yellow, center=(200,150), radius=80)
circle(color=blue, fill=none, center=(100,100), radius=50, line-width=3px)
```

### Rectangle (`square`)

Despite the name, `square` draws rectangles with independent width and height.

```
square(color=black, fill=lightblue, pos=(50,50), width=200px, height=100px)
square(color=red, line-type=dashed, fill=none, pos=(0,0), width=100%; height=100%)
```

`pos` is the **top-left** corner.

### Polygon

A closed shape through any number of vertices (minimum 3).

```
polygon(color=black, fill=orange, points=[(100,50),(175,200),(25,200)])
polygon(color=navy, line-width=2px, fill=lightblue,
        points=[(300,40),(380,100),(350,195),(250,195),(220,100)])
```

The path closes automatically from the last point back to the first.

### Path (open polyline)

An open stroke through a sequence of points (minimum 2). No fill.

```
path(color=blue, line-width=2px,
     points=[(10,10),(50,80),(90,10),(130,80)])
```

### Pie slice

A filled sector (arc + two radial lines to center).

```
pie(color=black, fill=red, center=(200,200), radius=100, start-angle=0, end-angle=90)
```

Angles: 0° = rightward (3 o'clock), increasing clockwise.

### Arc

Only the curved segment — no radial lines, no fill.

```
arc(color=gray, line-type=dashed, center=(200,150), radius=80, start-angle=45, end-angle=135)
```

> `fill` is not allowed on `arc` — even `fill=none` is an error.

### Line styles

| Value | Appearance |
|---|---|
| `solid` | Continuous line (default) |
| `dashed` | Long dashes |
| `dotted` | Dots |
| `dash-dot` | Alternating dash and dot |

---

## 7. Text

```
font(font-family="Arial, Helvetica, sans-serif", font-size=24px,
     color=black, style=normal, weight=bold,
     align=left, text="Hello World", pos=(100,100))
```

| Parameter | Default | Notes |
|---|---|---|
| `font-family` | system monospace | Comma-separated fallback chain |
| `font-size` | `12px` | Supports all length units |
| `color` | — (required) | Text color |
| `style` | `normal` | `normal` or `italic` |
| `weight` | `normal` | `normal` or `bold` |
| `align` | `left` | `left`, `center`, or `right` |
| `text` | — (required) | String content |
| `pos` | — (required) | Baseline anchor point |

**Text alignment:** `pos` anchors the baseline. With `align=left`, `pos.x` is the left edge. With `align=center`, `pos.x` is the horizontal center. With `align=right`, `pos.x` is the right edge.

**Multi-line text:** Use `\n` inside the string. Lines are spaced at `font-size × 1.2`.

```
font(color=black, font-size=16px, text="Line one\nLine two\nLine three", pos=(50,50))
```

**Escape sequences in strings:**

| Escape | Meaning |
|---|---|
| `\"` | Double-quote character |
| `\\` | Backslash |
| `\n` | New line |
| `\t` | Tab |

---

## 8. Connectors and Arrows

The `connector` primitive draws lines between points with optional arrowheads, labels, and animation.

### Basic arrow

```
connector(color=black, line-width=1px, start=(50,100), end=(350,100), end-cap=triangle)
```

### Multi-segment with routing

```
connector(color=blue, line-width=2px,
          points=[(10,10),(200,10),(200,200)],
          connector-type=step, corner=rounded, corner-radius=10px,
          end-cap=filled-circle, cap-size=small)
```

### Connector types

| Value | Effect |
|---|---|
| `straight` | Straight line segments (default) |
| `curved` | Smooth Catmull-Rom spline (needs ≥ 3 points for visible curve) |
| `step` | Right-angle routing (H-V-H between each pair of points) |

### Arrowhead shapes

| Value | Shape |
|---|---|
| `none` | No cap (default) |
| `triangle` | Filled arrowhead |
| `open-triangle` | Outlined arrowhead |
| `circle` | Hollow circle |
| `filled-circle` | Filled circle |
| `diamond` | Hollow diamond |
| `filled-diamond` | Filled diamond |
| `square` | Hollow square |
| `filled-square` | Filled square |

Use `start-cap` / `end-cap` to set the shape at each end. `cap-size` is `small`, `medium` (default), or `large`.

### Label on a connector

```
connector(color=black, line-width=1px, start=(50,50), end=(350,50),
          end-cap=triangle,
          label="data flow", label-pos=center, label-font-size=12px)
```

### Animated flowing connector

```
connector(color=blue, line-width=2px,
          start=(50,100), end=(450,100),
          animated=true, pattern=arrow, pattern-speed=6px,
          end-cap=triangle)
```

`animated=true` works in multi-frame GIF scripts — the pattern advances `pattern-speed` pixels per frame.

---

## 9. Embedding Images

Draw an external image file (PNG, JPEG, GIF, SVG) onto the canvas.

```
image(src="logo.png", pos=(10,10), width=200px, opacity=0.9)
image(src="chart.jpeg", pos=(50,50), width=400px, height=300px)
image(src="icon.svg", pos=(0,0), width=64px, rotate=45)
```

- `pos` is the **top-left** corner.
- Omit `height` to auto-scale preserving aspect ratio (and vice versa).
- Omit both `width` and `height` to use the image's natural size.
- `opacity`: 0.0 = invisible, 1.0 = fully opaque (default).

> Note: `image(src=...)` is the drawing primitive. `image width=... height=...` (without parentheses) is the canvas statement (§4). They are distinguished by the presence of `(`.

---

## 10. Transforms

All drawing primitives accept these optional transform parameters:

| Parameter | Default | Description |
|---|---|---|
| `rotate` | `0` | Clockwise rotation in degrees (0–360), no unit suffix |
| `skew-x` | `0` | Horizontal skew angle in degrees |
| `skew-y` | `0` | Vertical skew angle in degrees |
| `scale` | `1.0` | Uniform scale (0.5 = half size, 2.0 = double) |
| `z-index` | draw order | Rendering layer; higher = on top (0–1000) |

Transform order: **position → scale → skew → rotate**.

```
square(color=black, fill=gold, pos=(100,100), width=100px, height=100px, rotate=45)
circle(color=red, fill=none, center=(200,200), radius=60, scale=0.5)
font(color=black, font-size=20px, text="Tilted", pos=(150,150), rotate=30)
```

> Angle parameters (`rotate`, `start-angle`, `end-angle`) must not have a unit suffix — write `rotate=45` not `rotate=45px`.

> For transparency on a shape, use `RGBA(r,g,b,a)` as the color value — there is no per-primitive `opacity` parameter (except on `image(src=...)`).

---

## 11. Reusable Objects

Object templates define composite shapes you can stamp multiple times. Attributes use `:` (not `=`).

### Defining an object

```
begin_obj card
  width: 200px; height: 120px;
  background: white;
  border: solid 1px #AAAAAA;
  shadow: 2px 2px 4px RGBA(0,0,0,0.3);
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Card Title", pos=(10,15));
  line(color=#CCCCCC, line-width=1px, start=(0,35), end=(200,35));
end_obj
```

Coordinates inside the object body are **relative to the object's own top-left corner**.

### Placing instances

```
begin_frame dashboard
  image width=800px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#EEEEEE);
  card(pos=(20,50));
  card(pos=(240,50), background=RGB(200,230,255));
  card(pos=(460,50), background=RGB(255,220,200));
end_frame
```

`pos` is required. You can override any template attribute per instance.

### Instance-time size and rotation

At call time you can optionally resize or rotate an object instance without modifying the template.

**Explicit box size** — override `width` and/or `height`:

```
card(pos=(20,50), width=300px, height=80px)
card(pos=(20,150), width=300px)          # only width changed; height stays at template default
```

**Uniform scale** — multiply all template dimensions by a factor:

```
card(pos=(20,50), scale=1.6)             # 160 % of template size
card(pos=(20,200), scale=0.5)            # 50 % of template size
```

> In the default mode, when both explicit `width`/`height` and `scale` are provided, explicit size wins and a warning is emitted.

**Layout resize mode** â€” use `resize-mode=layout` when you want the object's `width` and `height` to redefine the layout box without automatically scaling all internal geometry:

```
card(pos=(20,50), width=300px, height=80px, resize-mode=layout)
card(pos=(20,150), width=260px, height=90px, resize-mode=layout, scale=1.2)
```

> In `resize-mode=layout`, `scale` is still applied. This is the main difference from the default object-instantiation path.

**Rotation** — clockwise, around the object's center (no unit suffix):

```
card(pos=(20,50), rotate=45)
card(pos=(200,50), scale=1.2, rotate=90)
```

> `rotate < 0` and `scale ≤ 0` are validation errors. `rotate` must not have a unit suffix.

### Object attributes (template definition syntax)

| Attribute | Syntax | Example |
|---|---|---|
| `width` | `width: <length>` | `width: 200px` |
| `height` | `height: <length>` | `height: 100px` |
| `background` | `background: <color>` | `background: white` |
| `border` | `border: <style> <width> <color>` | `border: solid 1px gray` |
| `shadow` | `shadow: <dx> <dy> <blur> <color>` | `shadow: 3px 3px 5px RGBA(0,0,0,0.25)` |
| `clip-bounds` | `clip-bounds: (x1,y1,x2,y2)` | `clip-bounds: (0,0,100,100)` |
| `clip-shape` | `clip-shape: circle \| square` | `clip-shape: circle` |

---

## 12. Reusable Functions

Functions are parameterized drawing procedures. Parameters are positional.

### Defining a function

```
begin_func badge(x, y, label)
  circle(color=black, fill=white, center=(x, y), radius=20);
  font(color=black, font-size=12px, text=label, pos=(x - 6, y - 6));
end_func
```

Inside a function body you can use arithmetic on parameters:

| Operator | Example |
|---|---|
| `+` | `pos=(x + 10, y + 5)` |
| `-` | `pos=(x - 6, y - 6)` |
| `*` | `radius=size * 2` |
| `/` | `pos=(x + width/2, y)` |

> Surround `-` with spaces for subtraction: `x - 10` subtracts 10; `skew-x` is an identifier.

### Calling a function

```
begin_frame icons
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  badge(50, 100, "A");
  badge(150, 100, "B");
  badge(250, 100, "C");
end_frame
```

Arguments are passed in the order they were declared. Recursion is not supported.

---

## 13. Library Files and Include

Split reusable objects and functions into separate `.dsl` files and import them.

```
include "components/buttons.dsl"
include "styles/shapes.dsl"
```

- Paths can be relative (from the current file) or absolute.
- Only `begin_obj` and `begin_func` definitions are imported. Frame definitions in included files are ignored.
- `include` must appear at the **top level** — not inside any frame, object, or function body.
- Circular includes are detected and produce an error.

**Example:**

`components/shapes.dsl`:
```
begin_obj icon_circle
  width: 60px; height: 60px;
  border: solid 2px black;
  circle(color=black, fill=white, center=(30,30), radius=28);
end_obj
```

`main.dsl`:
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

## 14. Animated GIFs

A script with multiple `begin_frame` blocks produces an animated GIF. Each frame becomes one animation frame.

```
begin_frame frame_0
  image width=500px; height=300px; colorspace=RGB; dpi=96;
  hold-time=500; frame-mode=cyclic-run;
  background(color=white);
  circle(color=red, fill=yellow, center=(100,150), radius=50);
end_frame

begin_frame frame_1
  image width=500px; height=300px; colorspace=RGB; dpi=96;
  hold-time=500; frame-mode=cyclic-run;
  background(color=white);
  circle(color=blue, fill=cyan, center=(250,150), radius=50);
end_frame
```

### Frame attributes

| Attribute | Default | Description |
|---|---|---|
| `hold-time` | `100` (ms) | How long this frame is shown |
| `frame-mode` | `one-run` | `one-run` plays once; `cyclic-run` loops forever |

- `frame-mode` from the **first** frame sets the GIF loop behavior; subsequent frames are ignored.
- All frames must use the same `output-format`.
- Omit `output-format` in multi-frame scripts to get the default `gif`.

### Animated connector tip

Add multiple frames with the same connector using `animated=true`. The engine advances the pattern `pattern-speed` pixels per frame automatically — you do not need to calculate offsets manually.

---

## 15. Grid System

The grid system provides an optional coordinate overlay for precise object placement and alignment. A frame may contain multiple `grid()` statements — each one activates a new grid configuration for the drawing commands that follow it.

### Defining a grid

```
grid(step-x=50px, step-y=50px)
```

`step-x` and `step-y` set the horizontal and vertical spacing. Use `offset-x` and `offset-y` to shift the grid origin away from (0,0).

The grid is **non-visual by default** — adding `grid()` alone has no effect on the output image.

### Visible grid (design and debug)

Add `render=true` to draw grid lines on top of all other primitives:

```
grid(step-x=50px, step-y=50px, render=true, color=RGB(200,200,200), line-type=dashed, line-width=1px)
```

If you omit `color` while `render=true`, the engine defaults to `RGB(200,200,200)` and emits a warning.

### Global alignment

Set `align=true` to snap every drawable element in the frame to the nearest grid intersection before rendering:

```
begin_frame aligned_layout
  image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  grid(step-x=50px, step-y=50px, align=true);
  circle(color=black, fill=red, center=(63,48), radius=20);  # snapped to (50,50)
  square(color=black, fill=blue, pos=(78,100), width=40px, height=40px);  # snapped to (50,100)
end_frame
```

### Per-element snap

Use the `snap=` parameter on any individual primitive or object to control snapping independently:

| Value | Effect |
|---|---|
| `grid-intersection` | Snap both x and y to the nearest grid intersection |
| `grid-x` | Snap only x; y stays as-is |
| `grid-y` | Snap only y; x stays as-is |
| `none` | No snapping; overrides global `align=true` for this element |

```
grid(step-x=50px, step-y=50px);
circle(color=black, fill=red, center=(63,48), radius=20, snap=grid-intersection);
# center snapped from (63,48) → (50,50)

square(color=black, fill=blue, pos=(78,100), width=40px, height=40px, snap=grid-x);
# pos snapped from (78,100) → (50,100) — only x snapped

font(font-family="Arial", font-size=12px, color=black, text="Label", pos=(63,48), snap=none);
# stays at (63,48) — opt-out
```

`snap` requires a `grid()` statement in the same frame. Using `snap` without a grid defined is a **validation error**.

### Alignment and transforms

Snapping is applied **before** any transforms. A rotated element rotates around its already-snapped position:

```
grid(step-x=50px, step-y=50px);
square(color=black, fill=gold, pos=(63,48), width=40px, height=40px,
       snap=grid-intersection, rotate=45);
# pos snapped to (50,50) FIRST, then rotated 45° around (50,50)
```

### align-origin — choosing which corner snaps

By default, snapping moves an element so that its **anchor point** (center for `circle`/`pie`/`arc`, top-left for everything else) lands on a grid point. Use `align-origin` to snap a different reference point instead:

| Value | Snapped point |
|---|---|
| `left-top` | Top-left corner of the bounding box (default for pos-based elements) |
| `right-top` | Top-right corner |
| `left-bottom` | Bottom-left corner |
| `right-bottom` | Bottom-right corner |
| `center` | Center of the bounding box (default for circle/pie/arc) |

```
grid(step-x=50px, step-y=50px, align=true);

# Snap the RIGHT edge of a rectangle to the grid rather than the left
square(color=black, fill=lightblue, pos=(78,100), width=40px, height=40px,
       align-origin=right-top);
# right edge x = 78+40 = 118 → snapped to 100; pos.x becomes 60

# Snap the center of a text block (useful for centered labels)
font(color=black, font-size=14px, text="Centered", pos=(63,48), align-origin=center);
```

> `align-origin` is ignored when there is no active grid or when snapping is disabled for the element.

### Multiple grids in one frame

Multiple `grid()` statements are allowed. Each one sets the active grid for the commands that follow — you can switch grid spacing mid-frame:

```
begin_frame multi_grid
  image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Fine 20 px grid for top section
  grid(step-x=20px, step-y=20px, align=true);
  circle(color=red, fill=none, center=(63,48), radius=20);   # snapped to 20px grid

  # Coarse 100 px grid for bottom section
  grid(step-x=100px, step-y=100px, align=true);
  square(color=blue, fill=none, pos=(130,200), width=60px, height=60px); # snapped to 100px grid
end_frame
```

Both grids are rendered (if `render=true`) and both contribute their snapping behaviour to their respective regions.

### Bounding box debug overlay (`show-bbox`)

Add `show-bbox=true` to any primitive or object instance to draw a **dashed bounding-box outline** around it after rendering. The outline color is chosen automatically for contrast (black on light backgrounds, white on dark ones).

This is purely a **debugging aid** — use it to check layout, alignment, and sizing, then remove it before the final output.

```
grid(step-x=50px, step-y=50px, align=true);
square(color=black, fill=lightblue, pos=(78,100), width=120px, height=60px,
       show-bbox=true);
circle(color=red, fill=none, center=(200,150), radius=50, show-bbox=true);
```

> `show-bbox` is **not valid** on `background()` or `grid()` — those are not drawable elements. Adding it there is a validation error.

---

## 16. Colors Reference

### Named colors

`black`, `white`, `red`, `green`, `blue`, `cyan`, `magenta`, `yellow`, `orange`, `purple`, `pink`, `gray`, `darkgray`, `lightgray`, `brown`, `lime`, `navy`, `teal`, `silver`, `gold`, `transparent`

Plus all 147 standard CSS Color Level 3 names (e.g., `cornflowerblue`, `tomato`, `slategray`).

### Color formats

| Format | Example | Notes |
|---|---|---|
| Named | `red` | Case-sensitive, always lowercase |
| Hex | `#FF5733` | 6 digits only — `#RGB` shorthand is not supported |
| RGB | `RGB(255,87,51)` | Components 0–255 |
| RGBA | `RGBA(0,0,0,0.5)` | Alpha 0.0 (transparent) – 1.0 (opaque) |
| `none` | `fill=none` | No paint; valid only for `fill` and `background` |
| `transparent` | `color=transparent` | Equivalent to `RGBA(0,0,0,0)`; valid everywhere |
| Palette alias | `@primary` | Reference to a named alias defined in a `begin_palette` block (see §17) |

> Using `none` for a stroke `color` (e.g., `color=none` on a line) is an error. Use `transparent` instead if you need a fully invisible stroke.

---

## 17. Named Color Palettes

A palette gives your colors meaningful names. Instead of scattering `#2342C8` throughout a script, you define it once as `@primary` and use the alias everywhere.

### Defining a palette

```
begin_palette brand
  primary   = #2342C8
  secondary = #F5F5F5
  accent    = RGB(255, 140, 0)
  bg        = RGBA(245, 245, 245, 1.0)
end_palette
```

- The name after `begin_palette` is just a label for error messages — alias lookup uses only the alias name, not the palette name.
- Each line is `alias = color_value`. Any color format works: named, hex, `RGB()`, `RGBA()`.
- You **cannot** use `@alias` inside a palette body — only direct color literals are allowed there.
- An empty palette block (no entries) is an error.

### Using aliases

Put `@alias` anywhere a color is expected — in any drawing command, object template, or function call:

```
begin_frame styled
  image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  square(color=@primary, fill=@secondary, pos=(50,50), width=200px, height=150px);
  font(color=@accent, font-size=18px, weight=bold, text="Palette Demo", pos=(60,250));
end_frame
```

### Palette in a library file

Palettes can live in an included file — any script that `include`s the file gets all its aliases:

`styles/colors.dsl`:
```
begin_palette brand
  primary   = #2342C8
  secondary = #F5F5F5
  accent    = RGB(255, 140, 0)
  bg        = RGBA(245, 245, 245, 1.0)
end_palette
```

`main.dsl`:
```
include "styles/colors.dsl"

begin_frame diagram
  image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  circle(color=@primary, fill=@secondary, center=(300,200), radius=80);
end_frame
```

### Forward references

You can use `@alias` before the palette that defines it — the engine resolves all aliases after loading every file:

```
begin_frame early_use
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);          # @bg is not defined yet ...
end_frame

begin_palette brand               # ... but it is defined here, which is fine
  bg = white
end_palette
```

### Rules to remember

- Alias names are **global** across all loaded palettes (including included files). Defining the same alias twice — even in different `begin_palette` blocks — is a parse error.
- An `@alias` that is never defined anywhere is a parse error.
- `@alias` is not allowed inside a `begin_palette` body.

---

## 18. Units Reference

| Suffix | Meaning | Resolved as |
|---|---|---|
| `px` | Pixels (default) | 1 px |
| `pt` | Points | DPI ÷ 72 px |
| `cm` | Centimeters | DPI ÷ 2.54 px |
| `mm` | Millimeters | DPI ÷ 25.4 px |
| `em` | Font-relative | 1 em = current font size (12 px outside `font` primitive) |
| `%` | Percentage | Of parent width (x) / parent height (y); of canvas width for scalar params |

Omitting a unit defaults to `px`.

> Angle parameters (`rotate`, `start-angle`, `end-angle`) are always degrees — do not add a unit suffix.

---

## 19. Common Mistakes

### 1. Wrong case

```
# WRONG
Begin_Frame my_image
  IMAGE width=400px; height=300px;

# CORRECT
begin_frame my_image
  image width=400px; height=300px;
```

### 2. Missing `image` statement

Every frame must contain an `image` canvas statement — it is not optional.

### 3. Unit suffix on an angle

```
# WRONG
circle(... rotate=45px)

# CORRECT
circle(... rotate=45)
```

### 4. `fill` on `arc` or `line` or `path`

```
# WRONG — arc does not support fill
arc(color=blue, fill=none, center=(100,100), radius=50, start-angle=0, end-angle=180)

# CORRECT — just leave fill out
arc(color=blue, center=(100,100), radius=50, start-angle=0, end-angle=180)
```

### 5. Colon vs equals in objects

```
# WRONG — object attributes need ':'
begin_obj box
  width = 100px
end_obj

# CORRECT
begin_obj box
  width: 100px
end_obj
```

### 6. `start-cap` and `start-arrow` together

These are aliases — use one or the other, not both.

```
# WRONG
connector(... start-cap=triangle, start-arrow=circle, ...)

# CORRECT
connector(... start-cap=triangle, ...)
```

### 7. `#RGB` hex shorthand

Only 6-digit hex is supported.

```
# WRONG
circle(color=#F00, ...)

# CORRECT
circle(color=#FF0000, ...)
```

### 8. JPEG with RGBA

JPEG does not support an alpha channel.

```
# WRONG
image width=800px; height=600px; colorspace=RGBA; output-format=jpeg;

# CORRECT — use png for transparency
image width=800px; height=600px; colorspace=RGBA; output-format=png;
```

### 9. `include` inside a frame or object

```
# WRONG
begin_frame my_frame
  include "library.dsl"
  ...
end_frame

# CORRECT — include at top level only
include "library.dsl"
begin_frame my_frame
  ...
end_frame
```

### 10. Subtraction vs identifier hyphen

```
# WRONG — 'x-6' is parsed as an identifier, not subtraction
font(... pos=(x-6, y))

# CORRECT — spaces around minus for arithmetic
font(... pos=(x - 6, y))
```

### 11. Unit suffix on object `rotate`

```
# WRONG
card(pos=(100,100), rotate=45px)

# CORRECT — angle is always bare degrees
card(pos=(100,100), rotate=45)
```

### 12. `scale=0` on an object instance

Unlike primitives (where `scale=0` silently renders nothing), `scale=0` on an object instantiation is a **validation error**.

```
# WRONG
card(pos=(100,100), scale=0)

# CORRECT — use scale > 0, or omit scale entirely
card(pos=(100,100), scale=0.1)
```

### 13. `snap` without a grid

`snap` requires a `grid()` statement in the same frame.

```
# WRONG — no grid() defined in this frame
circle(color=red, fill=none, center=(63,48), radius=20, snap=grid-intersection)

# CORRECT — define grid() first
grid(step-x=50px, step-y=50px);
circle(color=red, fill=none, center=(63,48), radius=20, snap=grid-intersection)
```

### 14. `show-bbox` on `background` or `grid`

`show-bbox=true` is only valid on drawable primitives and object instances, not on `background()` or `grid()`.

```
# WRONG
background(color=white, show-bbox=true)
grid(step-x=50px, step-y=50px, show-bbox=true)

# CORRECT — use show-bbox on primitives
background(color=white)
grid(step-x=50px, step-y=50px)
circle(color=red, fill=none, center=(100,100), radius=40, show-bbox=true)
```

### 15. `@alias` inside a palette body

Palette entries must use direct color literals — you cannot reference another alias inside the palette.

```
# WRONG
begin_palette ui
  base   = #2342C8
  hover  = @base    # error: @alias not allowed inside begin_palette
end_palette

# CORRECT — repeat the literal or use a different value
begin_palette ui
  base   = #2342C8
  hover  = #1A35A0
end_palette
```

### 16. Duplicate palette alias

Each alias name must be unique across **all** loaded palettes, including palettes from included files.

```
# WRONG — 'primary' appears in two different palette blocks
begin_palette brand
  primary = #2342C8
end_palette

begin_palette theme
  primary = red       # error: 'primary' already defined
end_palette

# CORRECT — use distinct alias names or consolidate into one palette
begin_palette brand
  brand-primary = #2342C8
  theme-primary = red
end_palette
```

### 17. Using `@alias` without defining a palette

An `@alias` reference that has no matching `begin_palette` entry is a parse error.

```
# WRONG — @primary is never defined
begin_frame chart
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@primary)
end_frame

# CORRECT — define the palette first (order does not matter)
begin_palette brand
  primary = #2342C8
end_palette

begin_frame chart
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@primary)
end_frame
```

### 18. Using a bbox before the named primitive is rendered

The named primitive must appear **before** any `.bbox` access in the script.

```
# WRONG — block1 is not yet rendered when bx is assigned
var bx;
bx = block1.bbox.x;
block1 = square(pos=(20, 70), width=120, height=60, fill=blue, color=black);

# CORRECT — render (name) the primitive first, then read its bbox
block1 = square(pos=(20, 70), width=120, height=60, fill=blue, color=black);
var bx;
bx = block1.bbox.x;
```

### 19. Using a variable without declaring it with `var`

Every variable must be declared before it is assigned or used in an expression.

```
# WRONG — gap is not declared
gap = 20;
square(pos=(10 + gap, 50), width=100, height=60, fill=blue, color=black);

# CORRECT — declare with 'var' first
var gap;
gap = 20;
square(pos=(10 + gap, 50), width=100, height=60, fill=blue, color=black);
```

### 20. Using `var` inside an object template body

Variable declarations are only allowed inside `begin_frame` and `begin_func` bodies — not inside `begin_obj`.

```
# WRONG — var is not permitted inside begin_obj
begin_obj my_panel
  width: 200px; height: 100px;
  var padding;    # error
  padding = 10;
  circle(color=black, fill=white, center=(10, 10), radius=8);
end_obj

# CORRECT — move var logic into the frame
begin_frame demo
  image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  var padding;
  padding = 10;
  circle(color=black, fill=white, center=(padding, padding), radius=8);
end_frame
```

### 21. Using `do ... while` outside a frame or function body

Loops are only valid inside `begin_frame` and `begin_func` bodies.

```
# WRONG - top-level loop
do
  circle(color=black, fill=blue, center=(40, 40), radius=10);
while 1 < 2;
```

### 22. Using a non-comparison loop condition

The `while` part must compare two numeric expressions.

```
# WRONG - condition is not a comparison
begin_frame demo
  image width=300px; height=120px; colorspace=RGB; dpi=96; output-format=png;
  var i;
  i = 0;
  do
    i = i + 1;
  while i;
end_frame
```

### 23. Forgetting to update the loop variable

If the condition never becomes false, the engine stops the loop after 1000 iterations and raises a runtime error.

```
# WRONG - i never changes, so the loop guard will fire
begin_frame demo
  image width=300px; height=120px; colorspace=RGB; dpi=96; output-format=png;
  var i;
  i = 0;
  do
    circle(color=black, fill=blue, center=(40, 40), radius=10);
  while i < 5;
end_frame
```

---

## 20. Variables and Layout Chaining

Variables enable data-driven layout within frame and function bodies. You can draw a shape, capture its rendered bounding box, and use those coordinates to position the next shape.

### Declaring variables

Declare one or more variables with `var` before using them:

```
var x, y;
var gap;
```

Variables are numeric and scoped to the enclosing frame or function. They have no value until assigned.

### Assigning values

Assign a literal number or arithmetic expression:

```
gap = 20;
x = 50;
y = gap + 10;
```

Supported operators: `+`, `-`, `*`, `/`. Division by zero is a runtime error. Unary minus is not supported — use `0 - x` instead.

### Naming a primitive

Prefix a drawing command with `name =` to bind it to a name:

```
block1 = square(pos=(20, 70), width=120, height=60, fill=#89b4fa, color=none);
```

The primitive renders immediately at that point in the script.

### Accessing a bounding box

After a named primitive is rendered, read its bounding box:

```
var bx, by, bw, bh;
bx = block1.bbox.x;
by = block1.bbox.y;
bw = block1.bbox.width;
bh = block1.bbox.height;
```

| Property | Meaning |
|---|---|
| `.bbox.x` | Left edge of the element |
| `.bbox.y` | Top edge of the element |
| `.bbox.width` | Width of the element |
| `.bbox.height` | Height of the element |

Coordinates are in the same DSL pixel space as all other positions (top-left = 0, 0).

### Using variables in parameters

Variables and expressions work anywhere a numeric parameter is expected:

```
block2 = square(pos=(bx + bw + gap, by), width=100, height=bh, fill=#a6e3a1, color=none);
```

Arithmetic expressions (`+`, `-`, `*`, `/`) and bbox accesses may be combined freely:

```
var cx, cy;
cx = bx + bw / 2;
cy = by + bh / 2;
circle(center=(cx, cy), radius=25, color=#cdd6f4, line-width=2, fill=none);
```

### Sequential execution note

Frames that use `var`, assignment, or named drawing commands execute **top to bottom** in declaration order. Z-index sorting is disabled for such frames — place elements in the order you want them drawn.

### Variables in functions

Variables declared inside `begin_func` / `end_func` work the same way. Each call to the function gets a fresh scope — values are not shared between calls.

### Scope rules

| Scope | Where declared | Accessible from |
|---|---|---|
| Frame scope | `begin_frame` body | Only within that frame |
| Function scope | `begin_func` body | Only within that function call |

Frame variables are not visible inside function calls and vice versa. Object template bodies (`begin_obj`) do not support `var`.

### Complete example

```
begin_frame chained_layout
  image width=600 height=200 output-format=png;
  background(color=#1e1e2e);

  var gap;
  gap = 20;

  block1 = square(pos=(20, 70), width=120, height=60, fill=#89b4fa, color=none);

  var bx, by, bw, bh;
  bx = block1.bbox.x;
  by = block1.bbox.y;
  bw = block1.bbox.width;
  bh = block1.bbox.height;

  block2 = square(pos=(bx + bw + gap, by), width=100, height=bh, fill=#a6e3a1, color=none);

  var bx2, bw2;
  bx2 = block2.bbox.x;
  bw2 = block2.bbox.width;

  block3 = square(pos=(bx2 + bw2 + gap, by), width=80, height=bh, fill=#fab387, color=none);

  var cx, cy;
  cx = bx + bw / 2;
  cy = by + bh / 2;
  circle(center=(cx, cy), radius=25, color=#cdd6f4, line-width=2, fill=none);
end_frame
```

---

## 21. Comparison Expressions and Loops

Comparison expressions let you ask simple numeric questions such as `i < 5` or `gap != 0`. The first place you use them is in the bounded `do ... while` loop.

### Comparison operators

Supported operators:

- `==`
- `!=`
- `<`
- `<=`
- `>`
- `>=`

Each side of the comparison is an ordinary numeric expression, so arithmetic still works:

```dsl
i < 5
counter <= max_count
current_x + width < canvas_limit
gap != 0
```

### Simple `do ... while` example

The loop body runs once before the condition is checked.

```dsl
begin_frame loop_basic
  image width=320px; height=160px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  var i;
  i = 0;

  do
    circle(color=black, fill=lightblue, center=(40 + i * 50, 80), radius=14);
    i = i + 1;
  while i < 5;
end_frame
```

### Repeated shape drawing example

```dsl
begin_frame bars
  image width=360px; height=220px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#f8fafc);

  var x;
  x = 30;

  do
    square(pos=(x, 60), width=30, height=100, color=#1f2937, fill=#93c5fd);
    x = x + 45;
  while x <= 210;
end_frame
```

### Function body example

Loops also work inside reusable functions.

```dsl
begin_func dot_row(start_x, y)
  var i;
  i = 0;

  do
    circle(color=black, fill=lightgreen, center=(start_x + i * 24, y), radius=8);
    i = i + 1;
  while i < 6;
end_func

begin_frame function_loop
  image width=260px; height=140px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);
  dot_row(40, 70);
end_frame
```

### Scope and safety rules

- `do ... while` is allowed only inside `begin_frame` and `begin_func`.
- It is not allowed at top level or inside `begin_obj` / `begin_palette`.
- The condition must be a comparison expression.
- Every loop has a fixed safety guard of 1000 iterations.

## Changelog

### 2026-05-05 — FEA-007: variable support and bounding box extraction

- Updated Table of Contents: added §20 Variables and Layout Chaining
- Added Common Mistakes §18 (bbox before render), §19 (missing `var`), §20 (`var` in object body)
- Added §20 Variables and Layout Chaining: `var` declarations, assignment, named primitives, bbox access syntax table, arithmetic expressions, sequential-execution note, function scope, scope rules table, complete chained-layout example
- File version 1.4 → 1.5

### 2026-05-04 — FEA-006: named color palette support

- Updated Table of Contents: added §17 Named Color Palettes; shifted Units Reference → §18, Common Mistakes → §19
- Updated §3 Script Structure: added `begin_palette`/`end_palette` to the code block and the block summary table; updated namespace note to mention palette alias namespace
- Updated §16 Colors Reference: added `Palette alias` row to the color formats table with reference to §17
- Added §17 Named Color Palettes: palette syntax, `@alias` usage in commands, library-file pattern, forward-reference rule, and rules summary
- Added Common Mistakes §15 (`@alias` inside palette body), §16 (duplicate alias), §17 (undefined alias)
- File version 1.3 → 1.4

### 2026-05-03 — FEA-005: show-bbox overlay; align-origin; multiple grids per frame
- Updated §15 Grid System intro: multiple grid() statements are now allowed per frame
- Added §15 "align-origin" subsection: explains the five reference-point values with a usage example
- Added §15 "Multiple grids in one frame" subsection: shows how each grid() replaces the active grid for subsequent commands
- Added §15 "Bounding box debug overlay (show-bbox)" subsection: explains show-bbox=true on primitives and objects, with examples
- Updated Common Mistakes #14: replaced "two grids is wrong" with "show-bbox on background/grid is wrong" (multiple grids are now allowed)
- File version 1.2 → 1.3

### 2026-05-03 07:57:16 — FEA-004: configurable grid system
- Updated Table of Contents: added §15 Grid System; shifted Colors Reference → §16, Units Reference → §17, Common Mistakes → §18
- Added §15 Grid System: grid() syntax, visible grid, global align=true, per-element snap table with four modes, alignment-before-transforms example
- Renamed section headings: §15 Colors Reference → §16, §16 Units Reference → §17, §17 Common Mistakes → §18
- Added Common Mistakes §13 (snap without grid) and §14 (two grid() statements in one frame)
- File version 1.1 → 1.2


### 2026-05-07 - FEA-008: comparison expressions and bounded do ... while
- Updated Table of Contents: added Section 21 Comparison Expressions and Loops
- Added Common Mistakes 21-23 for invalid loop scope, non-comparison conditions, and guard-triggering infinite loops
- Added Section 21 with comparison operators, a simple loop example, a repeated-shapes example, a function-body example, and scope/safety rules
- File version 1.5 -> 1.6
