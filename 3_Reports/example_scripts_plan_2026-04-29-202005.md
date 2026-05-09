# Example Scripts Plan — Technical Image Generator DSL

| Field | Value |
|---|---|
| **Description** | Prioritized plan for 50 AI-generated DSL example scripts |
| **Created at** | 2026-04-29 20:20:05 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## 1. Overview

This document defines the full set of example `.dsl` scripts to be created for the Technical Image Generator DSL. All scripts are AI-generated using Claude Sonnet 4.6, based on the language specification in `2_Docs/DSL_grammar_description.md` and the user guide in `2_Docs/DSL_user_guide.md`.

- **Total scripts:** 50 (47 single files + 3 multi-file projects)
- **Output directory:** `4_ExampleScripts/`
- **Priority levels:** MUST-HAVE (30 scripts) · NICE-TO-HAVE (20 scripts)
- **Ordering:** Simple → Advanced (foundation primitives first, complete showcases last)

---

## 2. Priority Matrix

| # | Filename | Category | Priority |
|---|---|---|---|
| 01 | `01_simple_line.dsl` | Basic Primitives | MUST-HAVE |
| 02 | `02_simple_circle.dsl` | Basic Primitives | MUST-HAVE |
| 03 | `03_simple_square.dsl` | Basic Primitives | MUST-HAVE |
| 04 | `04_simple_polygon.dsl` | Basic Primitives | MUST-HAVE |
| 05 | `05_simple_path.dsl` | Basic Primitives | MUST-HAVE |
| 06 | `06_simple_pie_arc.dsl` | Basic Primitives | MUST-HAVE |
| 07 | `07_simple_connector.dsl` | Basic Primitives | MUST-HAVE |
| 08 | `08_simple_text.dsl` | Basic Primitives | MUST-HAVE |
| 09 | `09_simple_image.dsl` | Basic Primitives | MUST-HAVE |
| 10 | `10_color_formats.dsl` | Colors & Styling | MUST-HAVE |
| 11 | `11_line_styles.dsl` | Colors & Styling | MUST-HAVE |
| 12 | `12_fill_vs_stroke.dsl` | Colors & Styling | MUST-HAVE |
| 13 | `13_transform_scale.dsl` | Transformations | MUST-HAVE |
| 14 | `14_transform_rotate.dsl` | Transformations | MUST-HAVE |
| 15 | `15_transform_skew.dsl` | Transformations | MUST-HAVE |
| 16 | `16_transform_combined.dsl` | Transformations | MUST-HAVE |
| 17 | `17_clip_rectangular.dsl` | Clipping & Masking | NICE-TO-HAVE |
| 18 | `18_clip_shape_circle.dsl` | Clipping & Masking | NICE-TO-HAVE |
| 19 | `19_clip_shape_square.dsl` | Clipping & Masking | NICE-TO-HAVE |
| 20 | `20_clip_combined.dsl` | Clipping & Masking | NICE-TO-HAVE |
| 21 | `21_background_solid.dsl` | Backgrounds | MUST-HAVE |
| 22 | `22_background_gradient.dsl` | Backgrounds | MUST-HAVE |
| 23 | `23_background_image.dsl` | Backgrounds | MUST-HAVE |
| 24 | `24_background_with_primitives.dsl` | Backgrounds | MUST-HAVE |
| 25 | `25_object_simple_button.dsl` | Object Templates | MUST-HAVE |
| 26 | `26_object_ui_panel.dsl` | Object Templates | MUST-HAVE |
| 27 | `27_object_nested.dsl` | Object Templates | MUST-HAVE |
| 28 | `28_object_grid.dsl` | Object Templates | MUST-HAVE |
| 29 | `29_function_simple.dsl` | Functions | MUST-HAVE |
| 30 | `30_function_parametric_drawing.dsl` | Functions | MUST-HAVE |
| 31 | `31_function_nested_calls.dsl` | Functions | MUST-HAVE |
| 32 | `32_function_grid_generator.dsl` | Functions | MUST-HAVE |
| 33 | `33_animation_bouncing_ball.dsl` | Animation | NICE-TO-HAVE |
| 34 | `34_animation_rotating_shape.dsl` | Animation | NICE-TO-HAVE |
| 35 | `35_animation_color_transition.dsl` | Animation | NICE-TO-HAVE |
| 36 | `36_animation_connector_flow.dsl` | Animation | NICE-TO-HAVE |
| 37 | `37_diagram_architecture.dsl` | Complex Diagrams | MUST-HAVE |
| 38 | `38_diagram_flowchart.dsl` | Complex Diagrams | MUST-HAVE |
| 39 | `39_diagram_network_topology.dsl` | Complex Diagrams | MUST-HAVE |
| 40 | `40_diagram_ui_mockup.dsl` | Complex Diagrams | MUST-HAVE |
| 41 | `41_project_component_library/` | Modularity | NICE-TO-HAVE |
| 42 | `42_project_color_theme/` | Modularity | NICE-TO-HAVE |
| 43 | `43_project_complex_diagram/` | Modularity | NICE-TO-HAVE |
| 44 | `44_advanced_z_order.dsl` | Advanced Features | NICE-TO-HAVE |
| 45 | `45_advanced_opacity.dsl` | Advanced Features | NICE-TO-HAVE |
| 46 | `46_advanced_font_fallback.dsl` | Advanced Features | NICE-TO-HAVE |
| 47 | `47_advanced_clipping_transforms.dsl` | Advanced Features | NICE-TO-HAVE |
| 48 | `48_example_dashboard.dsl` | Complete Showcases | NICE-TO-HAVE |
| 49 | `49_example_technical_diagram.dsl` | Complete Showcases | NICE-TO-HAVE |
| 50 | `50_example_animated_presentation.dsl` | Complete Showcases | NICE-TO-HAVE |

---

## 3. Detailed Script List

### Category 1 — Basic Primitives
**Priority: MUST-HAVE** | **Complexity: BEGINNER** | **Scripts: 01–09**

Each file introduces one or two primitives with basic styling to establish foundational drawing skills.

**`01_simple_line.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `line` primitive with all four stroke styles (solid, dashed, dotted, dash-dot) at varying widths and colors.

**`02_simple_circle.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `circle` primitive: filled, stroke-only, and transparent fill variations using named colors, hex values, and RGBA.

**`03_simple_square.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `square` (rectangle) primitive with independent widths and heights, fill colors, and dashed border styles.

**`04_simple_polygon.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `polygon` primitive: a triangle (3 points), a pentagon (5 points), and a hexagon (6 points), each with different fill and stroke combinations.

**`05_simple_path.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `path` primitive: open polylines in zigzag and wave shapes, confirming that the path is not auto-closed (unlike `polygon`).

**`06_simple_pie_arc.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `pie` (sector including two radial lines to center) and `arc` (curved segment only) side-by-side, making the visual difference explicit.

**`07_simple_connector.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `connector` primitive with straight arrows using triangle, filled-circle, and diamond end-caps in small, medium, and large sizes.

**`08_simple_text.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `font` primitive with varying font sizes, bold/normal weight, italic/normal style, and left/center/right alignment on a single canvas.

**`09_simple_image.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `image` drawing primitive: embedding an external file with width-only auto-scaling, height-only auto-scaling, and explicit width+height sizing.

---

### Category 2 — Colors and Styling
**Priority: MUST-HAVE** | **Complexity: BEGINNER** | **Scripts: 10–12**

Master all color formats and stroke/fill styling options.

**`10_color_formats.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating all four color formats on one canvas: named colors (`red`, `navy`), 6-digit hex (`#FF5733`), `RGB(r,g,b)`, and `RGBA(r,g,b,a)` with alpha transparency.

**`11_line_styles.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating all four `line-type` values (solid, dashed, dotted, dash-dot) rendered at three different `line-width` values for direct visual comparison.

**`12_fill_vs_stroke.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating fill-only, stroke-only, fill+stroke, and `fill=none` combinations across `circle`, `square`, and `polygon` primitives on a single canvas.

---

### Category 3 — Transformations
**Priority: MUST-HAVE** | **Complexity: INTERMEDIATE** | **Scripts: 13–16**

Understand geometric transforms and their composition order (position → scale → skew → rotate).

**`13_transform_scale.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `scale` transform: the same rectangle rendered at scale values 0.5, 1.0, 1.5, and 2.0 placed side-by-side.

**`14_transform_rotate.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the `rotate` transform: a rectangle rotated at 0°, 30°, 45°, 90°, and 180° around its center point.

**`15_transform_skew.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `skew-x` and `skew-y` separately on rectangles, showing horizontal rightward shear and vertical downward shear at increasing angles.

**`16_transform_combined.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating multiple transforms (scale + skew-x + rotate) applied to a single shape, illustrating the position→scale→skew→rotate application order.

---

### Category 4 — Clipping and Masking
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE** | **Scripts: 17–20**

Apply advanced masking techniques using object template clip attributes.

**`17_clip_rectangular.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `clip-bounds` on an object template: a richly decorated object where content outside the defined rectangular region is clipped.

**`18_clip_shape_circle.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `clip-shape: circle` on an object template: drawing content clipped to the ellipse inscribed within the object's bounding box.

**`19_clip_shape_square.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `clip-shape: square` on an object template, and comparing it visually with a `clip-bounds` of the same region to show they are equivalent.

**`20_clip_combined.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating the simultaneous use of `clip-bounds` and `clip-shape: circle`, resulting in content clipped to the intersection of both regions.

---

### Category 5 — Backgrounds
**Priority: MUST-HAVE** | **Complexity: BEGINNER–INTERMEDIATE** | **Scripts: 21–24**

Create professional canvas foundations using solid, gradient, and image backgrounds.

**`21_background_solid.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `background(color=...)` across four frames — each using a different color format: named, hex, RGB, and RGBA — to compare background rendering.

**`22_background_gradient.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `background(color1=..., color2=..., start=..., end=...)` with three gradient directions: horizontal (left→right), vertical (top→bottom), and diagonal.

**`23_background_image.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `background(src=...)` with all three modes (`fit`, `stretch`, `clip`) and varying `opacity` values on separate frames.

**`24_background_with_primitives.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating layering shapes, text, and connectors on top of a gradient background, using `z-index` to control the depth order of overlapping elements.

---

### Category 6 — Object Templates
**Priority: MUST-HAVE** | **Complexity: INTERMEDIATE** | **Scripts: 25–28**

Reduce code duplication through reusable, parameterizable composite objects.

**`25_object_simple_button.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) defining a reusable `button` object template (border, background fill, centered text label) and instantiating it in three color variants on one canvas.

**`26_object_ui_panel.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) defining a reusable `panel` container object (border, drop shadow, header divider line) and instantiating it at multiple sizes with different widths and heights.

**`27_object_nested.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating nested objects: a `card` object that contains an `icon` object, showing how inner coordinates are relative to the parent object's top-left corner.

**`28_object_grid.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) instantiating a single object template across a 3×3 grid layout, demonstrating systematic object reuse with calculated position offsets.

---

### Category 7 — Functions
**Priority: MUST-HAVE** | **Complexity: INTERMEDIATE–ADVANCED** | **Scripts: 29–32**

Build programmable, parameterized drawing logic with arithmetic expressions.

**`29_function_simple.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) defining a simple two-parameter function (`x`, `y`) that draws a labeled marker dot at the given position, called five times with different coordinates.

**`30_function_parametric_drawing.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) defining a function that uses all four arithmetic operators (+, -, *, /) to compute derived positions, sizes, and offsets from its input parameters.

**`31_function_nested_calls.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) defining two functions where the outer function calls the inner, demonstrating function composition without recursion.

**`32_function_grid_generator.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) using a function to generate a repeating grid pattern by computing cell positions from row/column index parameters and a configurable cell size.

---

### Category 8 — Animation
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE** | **Scripts: 33–36**

Create motion and temporal sequences using multi-frame GIF output.

**`33_animation_bouncing_ball.dsl`**
An AI-generated multi-frame GIF DSL script (Claude Sonnet 4.6) showing a circle moving along an arc path across 5 frames with `hold-time=100` and `frame-mode=cyclic-run` for a looping bounce animation.

**`34_animation_rotating_shape.dsl`**
An AI-generated multi-frame GIF DSL script (Claude Sonnet 4.6) showing a rectangle rotating in 45° increments across 8 frames, producing a smooth looping spin animation.

**`35_animation_color_transition.dsl`**
An AI-generated multi-frame GIF DSL script (Claude Sonnet 4.6) transitioning background and shape fill colors step-by-step across frames to simulate a color fade effect.

**`36_animation_connector_flow.dsl`**
An AI-generated multi-frame GIF DSL script (Claude Sonnet 4.6) demonstrating an animated connector (`animated=true`, `pattern=arrow`, `pattern-speed=6px`) flowing between two labeled boxes in a data-flow visualization.

---

### Category 9 — Complex Diagrams
**Priority: MUST-HAVE** | **Complexity: ADVANCED** | **Scripts: 37–40**

Real-world compositions integrating multiple primitives, objects, functions, and styling.

**`37_diagram_architecture.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) composing a system architecture diagram with labeled service boxes (object templates), database shapes (circle + rectangle composites), and directional connector arrows between components.

**`38_diagram_flowchart.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) composing a process flowchart with decision diamonds (polygon), process rectangles (square), rounded start/end shapes (circle), and labeled step connectors.

**`39_diagram_network_topology.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) composing a network topology diagram with router/switch nodes, labeled link connectors annotated with bandwidth, and a legend box in the corner.

**`40_diagram_ui_mockup.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) composing a UI/UX wireframe mockup with a navigation bar, content panels, placeholder button elements, and image frame placeholders arranged on one canvas.

---

### Category 10 — Script Inclusion and Modularity
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE–ADVANCED** | **Scripts: 41–43 (multi-file)**

Organize large projects across multiple files using `include` directives.

**`41_project_component_library/`** (2 files)
An AI-generated multi-file DSL project (Claude Sonnet 4.6):
- `lib/components.dsl` — shared button and panel object definitions
- `main.dsl` — includes the library and composes a dashboard from shared components

**`42_project_color_theme/`** (3 files)
An AI-generated multi-file DSL project (Claude Sonnet 4.6):
- `lib/colors.dsl` — named color palette definitions (via single-color objects)
- `lib/styles.dsl` — shared shape style objects using the palette
- `main.dsl` — includes both libraries and assembles a consistently themed diagram

**`43_project_complex_diagram/`** (4 files)
An AI-generated multi-file DSL project (Claude Sonnet 4.6):
- `sections/header.dsl` — header section objects and functions
- `sections/content.dsl` — main content area objects and functions
- `sections/footer.dsl` — footer section objects and functions
- `main.dsl` — includes all three sections and assembles the complete image

---

### Category 11 — Advanced Features
**Priority: NICE-TO-HAVE** | **Complexity: ADVANCED** | **Scripts: 44–47**

Advanced techniques: z-ordering, transparency, font fallback chains, combined clip and transforms.

**`44_advanced_z_order.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating `z-index` layering: overlapping shapes with explicit z-index values 1, 2, and 3, declared in reverse order to prove that draw order is overridden by z-index.

**`45_advanced_opacity.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating transparency techniques: RGBA fills and strokes on shapes, `opacity` on the `image` primitive, and `opacity` on a `background(src=...)`, all on one canvas.

**`46_advanced_font_fallback.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating multi-name font-family fallback chains, multi-line text rendering with `\n` and 1.2× line spacing, and all three text alignment modes (left, center, right).

**`47_advanced_clipping_transforms.dsl`**
An AI-generated DSL script (Claude Sonnet 4.6) demonstrating an object template with `clip-shape: circle`, then instantiating it with `rotate` and `scale` overrides, combining clipping with geometric transforms.

---

### Category 12 — Complete Showcases
**Priority: NICE-TO-HAVE** | **Complexity: ADVANCED** | **Scripts: 48–50**

End-to-end demonstrations of all DSL features combined in production-style outputs.

**`48_example_dashboard.dsl`**
An AI-generated comprehensive DSL script (Claude Sonnet 4.6) composing a data dashboard: KPI metric cards (object templates), a bar chart (positioned rectangles), a pie chart breakdown (multiple `pie` slices), and a trend line (`path`).

**`49_example_technical_diagram.dsl`**
An AI-generated comprehensive DSL script (Claude Sonnet 4.6) composing a multi-layer technical illustration integrating a gradient background, object templates, parameterized functions, annotated connectors, and z-index depth control.

**`50_example_animated_presentation.dsl`**
An AI-generated multi-frame animated GIF DSL script (Claude Sonnet 4.6) presenting a 5-slide sequence: a title card, three content frames with progressive shape reveals, and a closing summary frame — all with `cyclic-run` looping.

---

## 4. Generation Order

Recommended implementation wave sequence based on feature dependencies:

| Wave | Categories | Script Range | Dependency |
|---|---|---|---|
| **1 — Foundation** | 1 (Basic Primitives), 2 (Colors & Styling) | 01–12 | None — start here |
| **2 — Core Features** | 3 (Transforms), 5 (Backgrounds), 6 (Objects), 7 (Functions) | 13–16, 21–32 | Wave 1 |
| **3 — Real-world** | 9 (Complex Diagrams) | 37–40 | Waves 1–2 |
| **4 — Advanced** | 4 (Clipping), 8 (Animation), 10 (Modularity), 11 (Advanced), 12 (Showcases) | 17–20, 33–36, 41–50 | Waves 1–3 |
