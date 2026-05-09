# Example script generator 

Acts as a professional software developer

---

## Before anything else — load skills

Read all three skill files now, before any other action:
1. `.github/skills/report-management/SKILL.md`
2. `.github/skills/get-current-timestamp-for-filename/SKILL.md`
3. `.github/skills/get-current-timestamp-for-document/SKILL.md`

---

## Task

  - Generates example scripts for DSL language using DSL language user guide.
  - Create a TODO list and show on the screen the progress. Every step of the TODO list is a standalone example script generation, or complex script branch under a subdirectory.

--

## Input 

  2_Docs\DSL_scripting_user_guide.md ( ** USE THIS AS MAIN INPUT ** )
  2_Docs\implementation.md           ( ** use it only on demand, try avoid usage of it **)

---

## Output
  
  The output directory: 4_ExampleScripts
  The output file names shall express the subject of the example.
  Every example in a unique file <subject_of_script.dsl> 
  Where more files shall be use - included scripts - the full example shall be put under subdirectories like:  4_ExampleScripts\<subject_of_script_using_includes>

---

## Examples to Create

### Category 1: Basic Primitives (Simple Examples)
**Priority: MUST-HAVE** | **Complexity: BEGINNER** | **Time: 30 min** | **Lines of Code: 20-50 per file**

**Purpose:** Learn the 9 primitive types by creating simple standalone examples. Each file introduces one or two primitives with basic styling, establishing foundational drawing skills.

- `01_simple_line.dsl` - Draw lines with different styles (solid, dashed, dotted)
- `02_simple_circle.dsl` - Draw circles with and without fill
- `03_simple_square.dsl` - Draw rectangles with borders and fills
- `04_simple_polygon.dsl` - Draw triangles and polygons
- `05_simple_path.dsl` - Draw open polylines
- `06_simple_pie.dsl` - Draw pie slices and arcs
- `07_simple_connector.dsl` - Draw lines with arrow endpoints
- `08_simple_text.dsl` - Render text with different fonts and sizes
- `09_simple_image.dsl` - Embed and display images

### Category 2: Colors and Styling
**Priority: MUST-HAVE** | **Complexity: BEGINNER** | **Time: 20 min** | **Lines of Code: 30-60 per file**

**Purpose:** Master color definitions and visual styling. Learn all color formats (RGB, RGBA, hex, named), line styles (solid, dashed, dotted, dash-dot), and fill techniques. Critical for creating visually polished outputs.

Demonstrate color formats, line styles, and fill options.

- `10_color_formats.dsl` - All color formats (RGB, RGBA, hex, named)
- `11_line_styles.dsl` - All line styles with varying widths
- `12_fill_vs_stroke.dsl` - Shapes with different fill and stroke combinations

### Category 3: Transformations
**Priority: MUST-HAVE** | **Complexity: INTERMEDIATE** | **Time: 30 min** | **Lines of Code: 40-80 per file**

**Purpose:** Understand geometric transformations and their interaction order. Learn scale (0.1-10.0x), rotate (0-360°), and skew (0-90°) operations, and understand why transform order matters (Scale → Skew → Rotate).

Demonstrate scale, skew, and rotate operations.

- `13_transform_scale.dsl` - Scale transformations
- `14_transform_rotate.dsl` - Rotation transformations
- `15_transform_skew.dsl` - Skew transformations
- `16_transform_combined.dsl` - Multiple transforms on single primitives

### Category 4: Clipping and Masking
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE** | **Time: 35 min** | **Lines of Code: 50-100 per file**

**Purpose:** Apply advanced masking techniques to create complex shapes and constrain drawing areas. Learn rectangular bounds and shape-based clipping (circle, polygon), enabling creative visual compositions.

Demonstrate clipping regions and shape-based masking.

- `17_clip_rectangular.dsl` - Rectangular clipping bounds
- `18_clip_shape_circle.dsl` - Circle-based clipping
- `19_clip_shape_polygon.dsl` - Polygon-based clipping
- `20_clip_combined.dsl` - Multiple clips combined

### Category 5: Backgrounds
**Priority: MUST-HAVE** | **Complexity: BEGINNER-INTERMEDIATE** | **Time: 25 min** | **Lines of Code: 35-70 per file**

**Purpose:** Create professional canvas foundations. Learn solid colors, linear gradients, and image backgrounds (fit/stretch/clip modes), including layering primitives on background contexts.

Demonstrate solid, gradient, and image backgrounds.

- `21_background_solid.dsl` - Solid color backgrounds
- `22_background_gradient.dsl` - Linear gradient backgrounds
- `23_background_image.dsl` - Image backgrounds with sizing modes
- `24_background_with_primitives.dsl` - Layering primitives on backgrounds

### Category 6: Object Templates and Reuse
**Priority: MUST-HAVE** | **Complexity: INTERMEDIATE** | **Time: 40 min** | **Lines of Code: 60-120 per file**

**Purpose:** Reduce code duplication through component design. Learn defining reusable objects (buttons, panels, containers), instantiating with parameter overrides, and nesting objects for complex UI compositions.

Demonstrate object definition and instantiation.

- `25_object_simple_button.dsl` - Reusable button component
- `26_object_ui_panel.dsl` - Reusable panel/container
- `27_object_nested.dsl` - Nested objects with parameter overrides
- `28_object_grid.dsl` - Grid of repeated objects

### Category 7: Functions and Parameters
**Priority: MUST-HAVE** | **Complexity: INTERMEDIATE-ADVANCED** | **Time: 45 min** | **Lines of Code: 70-150 per file**

**Purpose:** Build programmable drawing logic. Learn parameterized functions with calculated positioning, nested function calls, and generators for algorithmic drawing patterns like grids and sequences.

Demonstrate function definitions and parameter substitution.

- `29_function_simple.dsl` - Basic function with parameters
- `30_function_parametric_drawing.dsl` - Function with calculated positions
- `31_function_nested_calls.dsl` - Functions calling other functions
- `32_function_grid_generator.dsl` - Function generating grid patterns

### Category 8: Animation
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE** | **Time: 50 min** | **Lines of Code: 100-200 per file**

**Purpose:** Create motion and temporal sequences. Learn multi-frame definitions, hold-time (milliseconds), frame-modes (one-run vs cyclic-run), and GIF generation for animated visualizations.

Demonstrate multi-frame animations and frame timing.

- `33_animation_bouncing_ball.dsl` - Simple bouncing animation
- `34_animation_rotating_shape.dsl` - Rotating shape animation
- `35_animation_color_transition.dsl` - Color changing animation
- `36_animation_position_sequence.dsl` - Objects moving across frames

### Category 9: Complex Diagrams (Real-world Examples)
**Priority: MUST-HAVE** | **Complexity: ADVANCED** | **Time: 60 min** | **Lines of Code: 150-300 per file**

**Purpose:** Validate real-world use cases and composition skills. Create architecture diagrams, flowcharts, network topologies, and UI mockups that integrate multiple primitives, colors, transforms, and styling into professional outputs.

Multi-primitive complex compositions.

- `37_diagram_architecture.dsl` - System architecture diagram
- `38_diagram_flowchart.dsl` - Process flowchart
- `39_diagram_network_topology.dsl` - Network diagram
- `40_diagram_ui_mockup.dsl` - UI/UX mockup with multiple components

### Category 10: Script Inclusion and Modularity
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE-ADVANCED** | **Time: 60 min** | **Lines of Code: 200-400 total per project**

**Purpose:** Organize large projects across multiple files. Learn include statements for modularity, managing dependencies, component libraries, and shared styling/color definitions across project subdirectories.

Multi-file projects demonstrating include statements.

Complex examples with includes (in subdirectories):
- `41_project_component_library/` - Reusable components in separate file
  - `main.dsl` - Main project file
  - `lib/components.dsl` - Shared components
  
- `42_project_color_theme/` - Color definitions in separate file
  - `main.dsl` - Main project file
  - `lib/colors.dsl` - Color definitions
  - `lib/styles.dsl` - Style definitions

- `43_project_complex_diagram/` - Large diagram split across files
  - `main.dsl` - Main diagram
  - `sections/header.dsl` - Header section
  - `sections/content.dsl` - Content section
  - `sections/footer.dsl` - Footer section

### Category 11: Advanced Features
**Priority: NICE-TO-HAVE** | **Complexity: ADVANCED** | **Time: 50 min** | **Lines of Code: 100-200 per file**

**Purpose:** Master advanced techniques for optimization and polish. Learn z-order layering, transparency/opacity, font fallback chains, and combining clipping with transformations for sophisticated visual effects.

Demonstrate advanced combinations and edge cases.

- `44_advanced_z_order.dsl` - Layering and z-index demonstration
- `45_advanced_opacity.dsl` - Transparent and semi-transparent elements
- `46_advanced_font_fallback.dsl` - Font family fallback chains
- `47_advanced_clipping_with_transforms.dsl` - Clipping and transformations combined

### Category 12: Complete Examples
**Priority: NICE-TO-HAVE** | **Complexity: ADVANCED** | **Time: 90 min** | **Lines of Code: 200-400 per file**

**Purpose:** Demonstrate end-to-end mastery of all DSL features. Create production-ready dashboards, technical illustrations, and animated presentations that integrate primitives, objects, functions, transformations, and styling into comprehensive showcases.

Comprehensive examples combining multiple features.

- `48_example_dashboard.dsl` - Dashboard-like UI
- `49_example_technical_diagram.dsl` - Complex technical illustration
- `50_example_animated_presentation.dsl` - Multi-frame presentation

---

### Category 13: Color Palette Examples
**Priority: MUST-HAVE** | **Complexity: BEGINNER-INTERMEDIATE** | **Time: 40 min** | **Lines of Code: 30-90 per file**

**Purpose:** Teach named color palette usage, alias references, palette files, inline palette blocks, and included palette libraries. Examples should demonstrate both `begin_palette` inline definitions and `include`-based palette reuse.

- `51_palette_basic_inline.dsl` - Inline palette with 5 named colors used in simple shapes
- `52_palette_gradient_inline.dsl` - Inline palette plus gradient background and palette-based fill colors
- `53_palette_text_styles.dsl` - Inline palette used for text color themes and headings
- `54_palette_buttons_inline.dsl` - Inline palette for reusable button objects with palette aliases
- `55_palette_chart_inline.dsl` - Inline palette for chart bars, axes, and labels
- `56_palette_library_include/main.dsl` - Include palette file with multiple objects using shared colors
- `57_palette_library_include/lib/colors.dsl` - Library file defining a reusable named palette
- `58_palette_dual_mode.dsl` - Example using both inline palette plus included palette for local overrides
- `59_palette_theme_switch.dsl` - Inline palette block and parameterized frame style selection
- `60_palette_icon_set.dsl` - Inline palette for icon and symbol colors with palette alias references
- `61_palette_branding_include/main.dsl` - Brand palette include with color definitions for logos and headers
- `62_palette_branding_include/lib/branding_colors.dsl` - Included palette definition file for reusable brand colors
- `63_palette_dashboard_inline.dsl` - Dashboard example using inline palette aliases across panels and charts
- `64_palette_overlay_include/main.dsl` - Overlay example with included palette colors and transparency
- `65_palette_overlay_include/lib/overlay_colors.dsl` - Included palette file for overlay and accent colors
- `66_palette_ui_theme.dsl` - Inline palette for UI theme elements, panels, buttons, and text
- `67_palette_icon_library_include/main.dsl` - Include palette and icon object library with shared colors
- `68_palette_icon_library_include/lib/icon_palette.dsl` - Included palette file for icon theme aliases
- `69_palette_complex_diagram.dsl` - Complex diagram using inline palette aliases and consistent color grouping
- `70_palette_includes_combined/main.dsl` - Combined include example importing palettes and object libraries, showing modular palette reuse

---

### Category 14: Variables and Layout Chaining
**Priority: MUST-HAVE** | **Complexity: INTERMEDIATE-ADVANCED** | **Time: 50 min** | **Lines of Code: 60-150 per file**

**Purpose:** Cover the FEA-007 variable and bounding-box feature set — `var` declarations, assignment, named drawing commands, and `.bbox` property access. Examples show how to capture a rendered element's geometry and use it to position the next element, enabling fully data-driven auto-layout. This feature area is completely absent from Categories 1–13 and documents a distinct DSL subsystem.

- `71_vars_basic.dsl` - `var` declarations, numeric assignment, and using variables in primitive parameters (pos, radius, width)
- `72_vars_bbox_access.dsl` - Named primitive (`name = square(...)`) and reading `.bbox.x`, `.bbox.y`, `.bbox.width`, `.bbox.height`
- `73_vars_chained_layout.dsl` - Sequential chained layout: three blocks placed by reading the previous block's bbox (replicates the §20 complete example)
- `74_vars_arithmetic.dsl` - Arithmetic expressions (`+`, `-`, `*`, `/`) combining variables, literals, and bbox values; computed center points and offsets
- `75_vars_in_functions.dsl` - Variables declared inside `begin_func` / `end_func` bodies; fresh scope per call demonstrated with two independent function invocations
- `76_vars_complex_auto_layout.dsl` - Full auto-layout: named connectors anchored to computed bbox edges, circle centered on a block, multi-column layout built entirely from bbox chaining

---

### Category 15: Grid System
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE** | **Time: 40 min** | **Lines of Code: 40-100 per file**

**Purpose:** Demonstrate the complete grid coordinate system — visible grids, global and per-element snapping, `align-origin` reference points, multiple grids per frame, and the `show-bbox` debug overlay. Establishes precise alignment workflows without manual coordinate calculation. None of these grid sub-features appear in Categories 1–13.

- `77_grid_visible.dsl` - Visible grid overlay (`render=true`) with custom `color`, `line-type`, `line-width`, and `step-x`/`step-y` sizes
- `78_grid_global_align.dsl` - Global snapping with `align=true` — before-and-after showing coordinates snapping to nearest grid intersection
- `79_grid_per_element_snap.dsl` - Per-element `snap` values on the same frame: `grid-intersection`, `grid-x`, `grid-y`, and `none` opt-out override
- `80_grid_align_origin.dsl` - `align-origin` parameter: snapping `left-top`, `right-top`, `left-bottom`, `right-bottom`, and `center` reference points on different shapes
- `81_grid_multiple.dsl` - Multiple `grid()` statements in one frame: fine 20 px grid for top section, coarse 100 px grid for bottom section
- `82_grid_show_bbox.dsl` - `show-bbox=true` debug overlay on various primitives and an object instance; demonstrates bounding-box visualization during layout design

---

### Category 16: Advanced Connector Features
**Priority: NICE-TO-HAVE** | **Complexity: INTERMEDIATE-ADVANCED** | **Time: 50 min** | **Lines of Code: 60-150 per file**

**Purpose:** Cover the full connector feature surface beyond the basics shown in `07_simple_connector.dsl`: all three routing types, all nine cap shapes, corner styles, label typography options, and static and animated stroke patterns. Each sub-feature has its own parameter set that deserves a focused example.

- `83_connector_types.dsl` - All `connector-type` values: `straight` (default), `curved` (Catmull-Rom spline with 3+ points), and `step` (H-V-H right-angle routing)
- `84_connector_all_caps.dsl` - All nine cap shapes: `none`, `triangle`, `open-triangle`, `circle`, `filled-circle`, `diamond`, `filled-diamond`, `square`, `filled-square`; `start-cap-size` / `end-cap-size` per-end overrides; `cap-size` values `small`, `medium`, `large`
- `85_connector_corner_styles.dsl` - Corner styles on step and straight multi-segment connectors: `sharp`, `rounded`, `beveled`; varying `corner-radius` values
- `86_connector_label_advanced.dsl` - Connector label with `label-offset`, `label-pos` (`start`/`center`/`end`), `label-font-style`, `label-font-weight`, `label-font-color`, and `label-font-family`
- `87_connector_patterns_static.dsl` - Static stroke patterns (`animated=false`): all four pattern types `dash`, `dot`, `arrow`, `zigzag`; `pattern-length`, `pattern-gap`, `pattern-color` parameters
- `88_connector_animated_patterns.dsl` - Multi-frame GIF with `animated=true` connector; all four pattern types across separate frames; `pattern-speed` controls advance per frame

---

### Category 17: Colorspaces, Output Formats, and Units
**Priority: NICE-TO-HAVE** | **Complexity: BEGINNER-INTERMEDIATE** | **Time: 35 min** | **Lines of Code: 30-80 per file**

**Purpose:** Cover the three colorspace modes (`RGB`, `RGBA`, `GRAY`), the `output-format=images` per-frame file mode, and all six unit suffixes. These cross-cutting features affect every script but are not demonstrated as standalone examples in earlier categories.

- `89_colorspace_gray.dsl` - `colorspace=GRAY` canvas: CCIR 601 luminance conversion of named, hex, `RGB()`, and `RGBA()` colors shown side-by-side
- `90_colorspace_rgba_transparent.dsl` - `colorspace=RGBA` canvas with `background(color=transparent)`; semi-transparent RGBA fills and an embedded PNG image with `opacity`
- `91_output_images_format.dsl` - `output-format=images`: three-frame script where each frame is saved as a separate named PNG file (`<frame-id>.png`)
- `92_units_all.dsl` - All six unit suffixes in one frame: `px` (default), `pt` (point), `cm`, `mm`, `em` (inside `font` and outside), and `%` (canvas-relative for positions and scalar usage for `radius`/`line-width`)

---

## Expected Output Format

Each generated .dsl file should have:
- **File Size:** 0.5 KB to 15 KB per file (based on complexity)
- **Structure:** Complete begin_frame/end_frame blocks with all required parameters
- **Styling:** Demonstration of the feature with clean, readable code
- **Comments:** Comments in examples describing the demonstrated feature
- **Validity:** All examples must be syntactically valid according to DSL_scripting_user_guide.md

Multi-file projects should have:
- **Directory Structure:** Organized subdirectories with main.dsl and supporting files
- **Dependencies:** Clear include statements showing file relationships
- **Documentation:** README or comments explaining project organization

---

## Category Dependencies

**Recommended Generation Order:**

1. **Foundation First** (Categories 1-2, ~1-1.5 hours)
   - Basic Primitives + Colors establish drawing fundamentals
   - No dependencies

2. **Core Features** (Categories 3, 5-7, ~2-2.5 hours)
   - Transformations, Backgrounds, Objects, Functions
   - Depend on: Foundation (1-2)
   - Can be done in any order

3. **Real-world Validation** (Category 9, ~1 hour)
   - Complex Diagrams use all foundation + core features
   - Depends on: Foundation + Core Features (1-7)

4. **Advanced Features** (Categories 4, 8, 10-12, ~2.5 hours)
   - Clipping, Animation, Modularity, Advanced techniques, Complete examples
   - Can be done after Categories 1-9
   - No hard dependencies, but benefit from solid foundation

5. **Variables and Grid** (Categories 14-15, ~1.5 hours)
   - Variables & Layout Chaining, Grid System
   - Can be done independently; Category 14 benefits from Categories 1-3 foundation
   - Category 15 (Grid) can be done any time after Category 1

6. **Advanced Connector and Output** (Categories 16-17, ~1.5 hours)
   - Advanced Connector Features, Colorspaces/Output Formats/Units
   - Category 16 depends on Category 1 (basic primitives) foundation
   - Category 17 is self-contained; can be done any time

---

## Restrictions

  - Do NOT guess or invent DSL syntax - use only documented features from the user guide
  - Each example must be self-contained and runnable independently
  - Examples should progress from simple to complex
  - Include comments in complex examples explaining what is being demonstrated
  - Test all examples to ensure they conform to DSL syntax
  - Follow file naming convention: ##_descriptive_name.dsl (numbering 01-50)
  - Ensure output files are placed in ExampleScripts directory with appropriate subdirectories for multi-file projects

--

