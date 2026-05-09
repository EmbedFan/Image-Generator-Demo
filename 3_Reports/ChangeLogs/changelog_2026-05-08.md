# Daily Changelog - 2026-05-08

### 2026-05-08 21:47:14 - Bug fix - z-index sorting now honors wrapped frame-body values
- Files: `imagegen/rendering/primitive_dispatcher.py`
- Action: Updated
- Details: Updated z-order sorting to unwrap `ExprFactor(LengthValue)` values for `z-index`, so explicit layering is no longer lost in frame bodies and later declarations no longer incorrectly cover higher-layer elements.

### 2026-05-08 20:28:04 - Bug fix - font alignment now honors center and right anchors
- Files: `imagegen/rendering/primitives/font_renderer.py`
- Action: Updated
- Details: Implemented real `align=center` and `align=right` handling for direct, rotated, and skewed text rendering so `font()` x anchors now match the documented semantics instead of always behaving like left alignment.

### 2026-05-08 19:32:47 - Example generation - items 32-49 created and validated
- Files: `4_ExampleScripts/32_function_grid_generator.dsl`, `4_ExampleScripts/33_animation_bouncing_ball.dsl`, `4_ExampleScripts/34_animation_rotating_shape.dsl`, `4_ExampleScripts/35_animation_color_transition.dsl`, `4_ExampleScripts/36_animation_position_sequence.dsl`, `4_ExampleScripts/37_diagram_architecture.dsl`, `4_ExampleScripts/38_diagram_flowchart.dsl`, `4_ExampleScripts/39_diagram_network_topology.dsl`, `4_ExampleScripts/40_diagram_ui_mockup.dsl`, `4_ExampleScripts/41_project_component_library/main.dsl`, `4_ExampleScripts/41_project_component_library/lib/components.dsl`, `4_ExampleScripts/42_project_color_theme/main.dsl`, `4_ExampleScripts/42_project_color_theme/lib/colors.dsl`, `4_ExampleScripts/42_project_color_theme/lib/styles.dsl`, `4_ExampleScripts/43_project_complex_diagram/main.dsl`, `4_ExampleScripts/43_project_complex_diagram/sections/header.dsl`, `4_ExampleScripts/43_project_complex_diagram/sections/content.dsl`, `4_ExampleScripts/43_project_complex_diagram/sections/footer.dsl`, `4_ExampleScripts/44_advanced_z_order.dsl`, `4_ExampleScripts/45_advanced_opacity.dsl`, `4_ExampleScripts/46_advanced_font_fallback.dsl`, `4_ExampleScripts/47_advanced_clipping_with_transforms.dsl`, `4_ExampleScripts/48_example_dashboard.dsl`, `4_ExampleScripts/49_example_technical_diagram.dsl`
- Action: Created/Updated
- Details: Added the missing Category 7-12 example scripts, including animations, diagrams, modular include-based projects, advanced rendering examples, and complete showcase files. Adjusted several scripts to match current parser/runtime limits and verified the full `32`-`49` range with successful `imagegen.py` renders.

### 2026-05-08 19:05:52 - Bug fix - connector corner styling now honors `corner=` and `corner-radius=`
- Files: `imagegen/rendering/primitives/connector/connector_renderer.py`, `imagegen/rendering/primitives/connector/corner_styler.py`
- Action: Updated
- Details: The connector renderer now reads the DSL-facing `corner=` parameter, keeps `corner-style=` as a compatibility alias, and passes `corner-radius=` into the styler so rounded and beveled connectors render visibly distinct corners.

### 2026-05-08 18:20:00 - Example fix - object button labels now use local object coordinates
- File: `4_ExampleScripts/54_palette_buttons_inline.dsl`
- Action: Updated
- Details: Reworked the `button` object to use a native `220x60` local canvas, draw its square at `(0,0)`, and place `label_pos` relative to the object instead of passing frame-absolute coordinates into the object body.

### 2026-05-08 18:10:23 - Bug fix - function-loop local variables preserved for runtime evaluation
- File: `imagegen/rendering/function_executor.py`
- Action: Updated
- Details: Stopped eagerly collapsing `ExprBinOp` and `ExprPoint` nodes inside function bodies when they still depend on function-local `var` values such as loop counters. Function loops now draw repeated geometry at distinct positions instead of stacking all iterations at the first coordinate.

### 2026-05-08 17:40:05 - Feature implementation - FEA-008 comparison expressions and bounded do-while loops
- Files:
  `imagegen/ast_nodes.py`,
  `imagegen/token_type.py`,
  `imagegen/lexer.py`,
  `imagegen/parser.py`,
  `imagegen/rendering/primitive_dispatcher.py`,
  `imagegen/rendering/function_executor.py`,
  `4_ExampleScripts/93_loop_basic_circles.dsl`,
  `4_ExampleScripts/94_loop_repeated_rectangles.dsl`,
  `4_ExampleScripts/95_loop_with_bbox_chaining.dsl`,
  `4_ExampleScripts/96_loop_in_function.dsl`,
  `4_ExampleScripts/97_loop_comparison_operators.dsl`,
  `4_ExampleScripts/98_loop_guard_error_example.dsl`
- Action: Created/Updated
- Details: Added comparison-expression parsing and bounded `do ... while` execution for frame/function bodies, enforced loop-scope restrictions and a 1000-iteration runtime guard, and added focused example scripts including a negative guard example.
