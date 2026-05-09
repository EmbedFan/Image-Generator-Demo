# Activity Log — Implementation

| Field | Value |
|---|---|
| **Description** | Chronological log of source-code implementation activities |
| **Created at** | 2026-05-05 05:05:12 |
| **File version** | 1.10 |
| **Created by** | Claude Sonnet 4.6 |

---

## 2026-05-08 21:47:14 - Bug fix: z-index sorting ignored wrapped numeric values in frame bodies

### Summary
Fixed z-order evaluation so explicit `z-index=` values on frame-body primitives are honored even when the parser wraps numeric literals as `ExprFactor(LengthValue(...))`. This restores expected layering for later-declared images and shapes, including the `_My/address_plate.dsl` case where `bonika.png` should remain behind higher z-index text and border elements.

### Root cause
`PrimitiveDispatcher._sort_by_z()` only accepted raw `LengthValue` nodes for `z-index`. In frame bodies, numeric parameters can arrive wrapped as `ExprFactor(LengthValue(...))`, so the sorter ignored those explicit z-values and fell back to declaration order. As a result, later commands were painted on top even when they had a lower declared z-index.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitive_dispatcher.py` | Added `_unwrap_length()` and updated `_sort_by_z()` to accept both `LengthValue` and `ExprFactor(LengthValue)` for `z-index` |

### Verification
Rendered and checked:
- `python .\imagegen.py .\_My\address_plate.dsl`
- `python .\imagegen.py .\4_ExampleScripts\44_advanced_z_order.dsl`

## 2026-05-08 20:28:04 - Bug fix: font align=center and align=right were ignored by the text renderer

### Summary
Fixed text alignment so `font(..., align=center, ...)` and `font(..., align=right, ...)` now honor the documented horizontal anchor semantics instead of always drawing from the left edge. The fix applies to normal text rendering as well as rotated and skewed text paths.

### Root cause
`FontRenderer.render()` parsed the `align` parameter correctly, but `_render_multiline()` ignored it and always passed the raw `(x, y)` position to `draw.text()`. The rotated and skewed paths also rendered every line from x=`0` on their temporary surfaces and anchored the composed block as if all text were left-aligned.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/font_renderer.py` | Added line measurement and alignment helpers; applied `left` / `center` / `right` x-offset logic to direct, rotated, and skewed text rendering paths |

### Verification
Rendered and checked:
- `python .\imagegen.py .\4_ExampleScripts\43_project_complex_diagram\main.dsl`
- `python .\imagegen.py .\4_ExampleScripts\54_palette_buttons_inline.dsl`
- `python .\imagegen.py .\4_ExampleScripts\86_connector_label_advanced.dsl`
- `python .\imagegen.py .\4_ExampleScripts\39_diagram_network_topology.dsl`

## 2026-05-08 19:32:47 - Example generation: added and validated example scripts 32-49

### Summary
Generated the missing Category 7-12 example scripts covering function-generated grids, animation, complex diagrams, include-based modular projects, advanced rendering features, and two complete showcase examples. Adjusted several scripts to match current parser and runtime constraints, then rendered every item from `32` through `49` successfully.

### Files changed
| File | Change |
|---|---|
| `4_ExampleScripts/32_function_grid_generator.dsl` | Added function-based grid pattern example; simplified nested color passing to stay within current function argument support |
| `4_ExampleScripts/33_animation_bouncing_ball.dsl` | Added multi-frame bouncing-ball animation example |
| `4_ExampleScripts/34_animation_rotating_shape.dsl` | Added rotating-shape animation example |
| `4_ExampleScripts/35_animation_color_transition.dsl` | Added color-transition animation example |
| `4_ExampleScripts/36_animation_position_sequence.dsl` | Added moving-object multi-frame example |
| `4_ExampleScripts/37_diagram_architecture.dsl` | Added architecture-diagram example |
| `4_ExampleScripts/38_diagram_flowchart.dsl` | Added flowchart example with step connectors |
| `4_ExampleScripts/39_diagram_network_topology.dsl` | Added network-topology example |
| `4_ExampleScripts/40_diagram_ui_mockup.dsl` | Added UI mockup example |
| `4_ExampleScripts/41_project_component_library/main.dsl` | Added modular include-based component library main file |
| `4_ExampleScripts/41_project_component_library/lib/components.dsl` | Added reusable object library for Project 41 |
| `4_ExampleScripts/42_project_color_theme/main.dsl` | Added color-theme modular main file |
| `4_ExampleScripts/42_project_color_theme/lib/colors.dsl` | Added shared palette definitions for Project 42 |
| `4_ExampleScripts/42_project_color_theme/lib/styles.dsl` | Added shared styled object definitions for Project 42 |
| `4_ExampleScripts/43_project_complex_diagram/main.dsl` | Added multi-file complex-diagram main file |
| `4_ExampleScripts/43_project_complex_diagram/sections/header.dsl` | Added Project 43 header section |
| `4_ExampleScripts/43_project_complex_diagram/sections/content.dsl` | Added Project 43 content section |
| `4_ExampleScripts/43_project_complex_diagram/sections/footer.dsl` | Added Project 43 footer section |
| `4_ExampleScripts/44_advanced_z_order.dsl` | Added z-index layering example |
| `4_ExampleScripts/45_advanced_opacity.dsl` | Added RGBA transparency example |
| `4_ExampleScripts/46_advanced_font_fallback.dsl` | Added font fallback chain example |
| `4_ExampleScripts/47_advanced_clipping_with_transforms.dsl` | Added clipping plus transform example |
| `4_ExampleScripts/48_example_dashboard.dsl` | Added dashboard showcase example and adapted connector usage to runtime-supported start/end expressions |
| `4_ExampleScripts/49_example_technical_diagram.dsl` | Added technical-illustration showcase example and adjusted function arguments to supported value types |

### Verification
Rendered successfully:
- `python .\imagegen.py .\4_ExampleScripts\32_function_grid_generator.dsl`
- `python .\imagegen.py .\4_ExampleScripts\33_animation_bouncing_ball.dsl`
- `python .\imagegen.py .\4_ExampleScripts\34_animation_rotating_shape.dsl`
- `python .\imagegen.py .\4_ExampleScripts\35_animation_color_transition.dsl`
- `python .\imagegen.py .\4_ExampleScripts\36_animation_position_sequence.dsl`
- `python .\imagegen.py .\4_ExampleScripts\37_diagram_architecture.dsl`
- `python .\imagegen.py .\4_ExampleScripts\38_diagram_flowchart.dsl`
- `python .\imagegen.py .\4_ExampleScripts\39_diagram_network_topology.dsl`
- `python .\imagegen.py .\4_ExampleScripts\40_diagram_ui_mockup.dsl`
- `python .\imagegen.py .\4_ExampleScripts\41_project_component_library\main.dsl`
- `python .\imagegen.py .\4_ExampleScripts\42_project_color_theme\main.dsl`
- `python .\imagegen.py .\4_ExampleScripts\43_project_complex_diagram\main.dsl`
- `python .\imagegen.py .\4_ExampleScripts\44_advanced_z_order.dsl`
- `python .\imagegen.py .\4_ExampleScripts\45_advanced_opacity.dsl`
- `python .\imagegen.py .\4_ExampleScripts\46_advanced_font_fallback.dsl`
- `python .\imagegen.py .\4_ExampleScripts\47_advanced_clipping_with_transforms.dsl`
- `python .\imagegen.py .\4_ExampleScripts\48_example_dashboard.dsl`
- `python .\imagegen.py .\4_ExampleScripts\49_example_technical_diagram.dsl`

## 2026-05-08 19:05:52 - Bug fix: connector corner styling ignored DSL corner parameters

### Summary
Fixed connector corner styling so the renderer honors the DSL-facing `corner=` parameter and uses `corner-radius=` to control rounded and beveled corner setback. This restores visible rounded and beveled corners in `85_connector_corner_styles.dsl`.

### Root cause
`ConnectorRenderer` looked for `corner-style` instead of the example's `corner` parameter, so all connectors silently fell back to `sharp`. In addition, `CornerStyler` ignored `corner-radius` completely and always used its internal fixed setback constant.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/connector/connector_renderer.py` | Accept `corner=` as the primary DSL key, keep `corner-style=` as an alias, and pass `corner-radius` through to the styler |
| `imagegen/rendering/primitives/connector/corner_styler.py` | Use the passed radius/setback for rounded and beveled corners instead of the fixed default only |

### Verification
Rendered and checked:
- `python .\imagegen.py .\4_ExampleScripts\85_connector_corner_styles.dsl`
- `python .\imagegen.py .\4_ExampleScripts\84_connector_all_caps.dsl`

Sanity check:
- `85_connector_corner_styles.png` now renders distinct sharp, rounded, and beveled connector variants using the example's `corner=` and `corner-radius=` parameters.

## 2026-05-08 18:20:00 - Example fix: object button labels used frame coordinates instead of local coordinates

### Summary
Fixed `54_palette_buttons_inline.dsl` so the `button` object uses object-local coordinates for both its square and text label. The previous example mixed frame-absolute coordinates into the object body, which caused the button content to be positioned twice during instantiation and made the labels appear missing.

### Files changed
| File | Change |
|---|---|
| `4_ExampleScripts/54_palette_buttons_inline.dsl` | Added native object size, changed the button square to `pos=(0,0)`, and updated `label_pos` values to be local to the object |

### Verification
Rendered and checked:
- `python .\imagegen.py .\4_ExampleScripts\54_palette_buttons_inline.dsl`

Pixel sanity check:
- `4_ExampleScripts/54_palette_buttons_inline.png` now contains non-background label pixels in the first button label area with bbox `x=157..262`, `y=96..125`.

## 2026-05-08 18:10:23 - Bug fix: function-loop local variables were frozen during pre-resolution

### Summary
Fixed function-body expression resolution so loop-local variables declared with `var` remain live until runtime. This restores correct repeated positioning in function loops such as `dot_row(start_x, y)`, where each iteration should draw at a new x-coordinate instead of stacking all circles on top of each other.

### Root cause
`FunctionExecutor._resolve_value()` still eagerly evaluated `ExprBinOp` and `ExprPoint` nodes against function argument bindings. That worked for pure parameter expressions, but it collapsed function-local runtime variables like `i` to `0` because they are not part of the argument-binding map. As a result, expressions like `start_x + i * 28` were frozen at the first-iteration value before the loop executed.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/function_executor.py` | Preserve partially-resolved `ExprBinOp` and `ExprPoint` nodes so function-local loop variables are evaluated by the runtime `VariableStore` inside the dispatcher |

### Verification
Rendered and checked:
- `python .\imagegen.py .\4_ExampleScripts\96_loop_in_function.dsl`
- `python .\imagegen.py .\4_ExampleScripts\31_function_nested_calls.dsl`
- `python .\imagegen.py .\4_ExampleScripts\93_loop_basic_circles.dsl`

Pixel sanity check:
- `4_ExampleScripts/96_loop_in_function.png` now contains non-white pixels spanning `x=38` to `x=201`, confirming a horizontal row rather than a single overlapping circle.

## 2026-05-08 17:40:05 - Feature implementation: FEA-008 comparison expressions and bounded do-while loops

### Summary
Implemented numeric comparison expressions and a bounded `do ... while` loop for frame and function bodies. The parser now accepts loop statements and comparison operators, the dispatcher executes loop bodies sequentially with a fixed 1000-iteration guard, and function-body loop nodes preserve parameter substitution through the existing function executor.

### Files changed
| File | Change |
|---|---|
| `imagegen/ast_nodes.py` | Added `ComparisonExpr` and `DoWhileStmt` AST nodes; extended `DrawingCmd` union |
| `imagegen/token_type.py` | Added token types for `==`, `!=`, `<`, `<=`, `>`, `>=` |
| `imagegen/lexer.py` | Reserved `do` / `while` keywords and tokenized comparison operators |
| `imagegen/parser.py` | Parsed `do ... while` blocks and comparison expressions; added clear scope-restriction parse errors for top-level, object-body, and palette-body misuse |
| `imagegen/rendering/primitive_dispatcher.py` | Executed loop bodies sequentially and enforced the fixed max-iteration runtime guard |
| `imagegen/rendering/function_executor.py` | Resolved loop bodies and comparison conditions inside function calls |
| `4_ExampleScripts/93_loop_basic_circles.dsl` | Added basic frame-loop example |
| `4_ExampleScripts/94_loop_repeated_rectangles.dsl` | Added repeated-rectangle loop example |
| `4_ExampleScripts/95_loop_with_bbox_chaining.dsl` | Added bbox-driven loop example |
| `4_ExampleScripts/96_loop_in_function.dsl` | Added function-body loop example |
| `4_ExampleScripts/97_loop_comparison_operators.dsl` | Added comparison-operator coverage example |
| `4_ExampleScripts/98_loop_guard_error_example.dsl` | Added negative example for guard behavior |

### Verification
Rendered successfully:
- `python .\imagegen.py .\4_ExampleScripts\93_loop_basic_circles.dsl`
- `python .\imagegen.py .\4_ExampleScripts\94_loop_repeated_rectangles.dsl`
- `python .\imagegen.py .\4_ExampleScripts\95_loop_with_bbox_chaining.dsl`
- `python .\imagegen.py .\4_ExampleScripts\96_loop_in_function.dsl`
- `python .\imagegen.py .\4_ExampleScripts\97_loop_comparison_operators.dsl`
- `python .\imagegen.py .\4_ExampleScripts\29_function_simple.dsl`
- `python .\imagegen.py .\4_ExampleScripts\25_object_simple_button.dsl`

Expected failure checks:
- `python .\imagegen.py .\4_ExampleScripts\98_loop_guard_error_example.dsl`
- top-level loop temp script -> `do-while loop is only permitted inside begin_frame / begin_func bodies`
- object-body loop temp script -> `do-while loop is not permitted inside an object template body`
## 2026-05-07 21:04:48 — Bug fix: function arguments collapsed to zero in function bodies

### Summary
Fixed function parameter binding so positional arguments passed into `begin_func` / `end_func` bodies preserve their real value types. Numeric position args such as `x` and `y` now resolve correctly, and string args such as `label_text` no longer collapse to `0px`.

### Root cause
`FunctionExecutor._bind_args()` only accepted raw `LengthValue` and converted every other argument type to `0.0`. But frame-body function calls are parsed with `in_func_body=True`, so numeric args arrive as `ExprFactor(LengthValue(...))`, and string args arrive as `StringValue`. Both were therefore dropped to zero. Later `_resolve_value()` treated string parameter references like `label_text` as numeric expressions and rewrote them to `LengthValue(0px)`.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/function_executor.py` | Preserve original bound argument value types, unwrap numeric `ExprFactor(LengthValue)`, resolve string params to `StringValue`, and keep enum-like unresolved names as `IdentValue` instead of coercing them to `0px` |

### Verification
Rendered and checked:
- `4_ExampleScripts/29_function_simple.dsl`
- `4_ExampleScripts/30_function_parametric_drawing.dsl`
- `4_ExampleScripts/31_function_nested_calls.dsl`

## 2026-05-07 20:43:30 — Bug fix: object shadows were clipped away during instantiation

### Summary
Fixed object-level shadows on instantiated objects such as `panel()` so the shadow can extend beyond the object's own bounding box instead of being clipped away on the temporary object canvas.

### Root cause
`square()` could render a shadow on its isolated surface, but when used inside an object template the rendered result was pasted into an object canvas sized only to the object's declared width/height. Any shadow extending outside those bounds was clipped before the final object was composited onto the frame.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/object_instantiator.py` | Added object-level shadow composition after object rendering/clip/resize, including padded shadow canvas and paste-origin correction |

### Verification
Rendered and checked:
- `4_ExampleScripts/26_object_ui_panel.dsl`
- `4_ExampleScripts/27_object_nested.dsl`
- `4_ExampleScripts/28_object_grid.dsl`
- `4_ExampleScripts/82_grid_show_bbox.dsl`

## 2026-05-07 20:18:27 — Bug fix: resized object instances clipped right/bottom borders

### Summary
Fixed object-instance resizing so explicit `width=` / `height=` overrides no longer clip the right and bottom edges of object bodies such as `button()` in `25_object_simple_button.dsl`.

### Root cause
`ObjectInstantiator` rendered object bodies onto a target-sized off-screen canvas using a single averaged `aa_scale` derived from independent width and height resize factors. For non-uniform instance resizing, body geometry was scaled beyond the target buffer and got clipped on the positive edges. After the object-attribute substitution fix, body references like `width=width` and `height=height` made this clipping visible immediately.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/object_instantiator.py` | Render object bodies at native template size, preserve native `width` / `height` for body attribute substitution, apply clip in native space, then resize the composed RGBA object bitmap to the requested instance size |

### Verification
Rendered and checked:
- `4_ExampleScripts/25_object_simple_button.dsl`
- `4_ExampleScripts/26_object_ui_panel.dsl`
- `4_ExampleScripts/27_object_nested.dsl`
- `4_ExampleScripts/28_object_grid.dsl`

## 2026-05-05 06:30:00 — FEA-007 Docs: DSL Grammar and User Guide Updated

### Summary
Updated both documentation files to reflect FEA-007 (variable support and bounding box extraction).

### Files changed
| File | Change |
|---|---|
| `2_Docs/DSL_grammar_description.md` | v3.4 → v3.5: added `var` keyword, new EBNF productions, new §14, renumbered §14–§18 to §15–§19 |
| `2_Docs/DSL_user_guide.md` | v1.4 → v1.5: added §20 Variables and Layout Chaining, three new Common Mistakes |

---

## 2026-05-05 05:45:00 — Regression Fix: Rotation / Scale / BBox Overlay Restored

**Plan:** `3_Reports/impl_rot_bbox_fix_2026-05-05-053000.md`

### Summary
Fixed two silent regressions introduced by FEA-007. All example scripts pass with zero errors or warnings.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/bbox_renderer.py` | Added `ExprFactor` import + `_unwrap_length()` helper; updated `_compute_aabb` and `_object_inst_aabb` |
| `imagegen/rendering/object_instantiator.py` | Added `ExprFactor` import + `_unwrap_length()` helper; updated `instantiate` scale/rotate resolution |

### Regression test
All example DSL scripts pass with zero errors or warnings.

---

## 2026-05-05 05:30:00 — Regression Investigation: Rotation / Scale / BBox Overlay Fix Plan

**Plan:** `3_Reports/impl_rot_bbox_fix_2026-05-05-053000.md`

### Summary
Identified root cause of two silent regressions introduced by FEA-007: bounding-box overlays not rendered and object rotate/scale params silently ignored. Created a detailed implementation plan; no Python source was modified.

### Root cause
FEA-007 changed frame-body parsing to `in_func_body=True`, wrapping all bare NUMBER params as `ExprFactor(LengthValue(...))`. `PrimitiveDispatcher._resolve_cmd` correctly unwraps these before primitive renderers run, but two consumers receive the original unresolved AST nodes:
- `bbox_renderer._compute_aabb` — called from `frame_runner` with raw command lists; all `isinstance(x, LengthValue)` guards fail → overlays skipped.
- `object_instantiator.instantiate` — receives the original `ObjectInst` node directly; `isinstance(scale_param, LengthValue)` and `isinstance(rotate_param, LengthValue)` fail → transforms silently skipped.

### Planned fix (implementation pending)
Add `_unwrap_length(val) -> LengthValue | None` helper in both affected files. Handles both `LengthValue` (object-body, unchanged) and `ExprFactor(LengthValue)` (frame-body, FEA-007). Apply at every `isinstance(x, LengthValue)` guard that receives potentially-wrapped values.

### Files planned for change
| File | Change |
|---|---|
| `imagegen/rendering/bbox_renderer.py` | Add `_unwrap_length`; update `_compute_aabb` (CircleNode, PieNode/ArcNode, SquareNode, FontNode, ImagePrimNode) and `_object_inst_aabb` (scale, rotate) |
| `imagegen/rendering/object_instantiator.py` | Add `_unwrap_length`; update `instantiate` (width/height/scale lines 68–81, rotate lines 119–127) |

---

## 2026-05-05 19:17:51 — Implement etalon image generator/checker tool

### Summary
Created a new CLI utility for recursive `_etalon` image generation and verification, supporting `.jpg`, `.png`, and `.gif` files.

### Files changed
| File | Change |
|---|---|
| `Tools/AIPrompts/impl_generate_check_etalonn_imageset.md` | Added implementation plan for generation and verification logic |
| `Tools/generate_check_etalonn_imageset.py` | Added CLI script, file discovery, copy/generation, comparison, missing-file handling, and summary reporting |

---

## 2026-05-07 19:30:06 — Bug fix: extended CSS-3 named colors silently rendered as black

### Summary
~125 CSS-3 color names accepted by the lexer (e.g. `lightblue`, `crimson`, `coral`, `goldenrod`) were silently resolved to black `(0,0,0)` because `_NAMED_COLOR_MAP` in the parser contained only 20 basic colors. The fallback for any unknown name was `ColorValue(r=0, g=0, b=0)`.

### Root cause
Two lists were out of sync: the lexer's `_NAMED_COLORS` frozenset (~147 names) and the parser's `_NAMED_COLOR_MAP` (~20 names). Any name the lexer accepted but the map didn't contain produced silent black output with no error.

### Files changed
| File | Change |
|---|---|
| `imagegen/parser.py` | Expanded `_NAMED_COLOR_MAP` from 20 entries to the full CSS-3 set (all names present in the lexer's `_NAMED_COLORS`); removed the "stub (0,0,0)" fallback comment |

---

## 2026-05-07 18:43:41 — Bug fix: scale and rotate ignored on SquareRenderer, CircleRenderer, PolygonRenderer

### Summary
All three shape renderers drew primitives directly at final canvas coordinates on a full-canvas temp image, making per-element scale and rotate impossible to apply. SquareRenderer also ignored scale and rotate even in the existing skew path.

### Fix approach — same pattern for all three
- **SquareRenderer**: unified transform path — draw on isolated `(w, h)` surface → `scale` (resize) → `skew` (_apply_skew) → `rotate` (PIL rotate) → composite centered at `(x + w//2, y + h//2)`. Zero-transform fast path unchanged.
- **CircleRenderer**: scale applied directly to radius (`effective_r = r * scale`) — most efficient for a symmetric shape. Rotate is a visual no-op on a circle; silently accepted. Existing full-canvas draw approach retained.
- **PolygonRenderer**: transform path computes point bounding box, draws on local `(bbox_w, bbox_h)` surface with offset points → `scale` (resize) → `rotate` (PIL rotate) → composite centered at original bbox center. Zero-transform fast path unchanged.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/square_renderer.py` | Extracted `scale`, `rotate`; unified skew+scale+rotate into single transform path; centered composite anchor |
| `imagegen/rendering/primitives/circle_renderer.py` | Extracted `scale`; applied to radius before draw |
| `imagegen/rendering/primitives/polygon_renderer.py` | Extracted `scale`, `rotate`; added bbox-local surface + resize + rotate transform path |

---

## 2026-05-07 18:32:09 — Bug fix: skew affine offset wrong — bottom-left / top-right clipping

### Summary
Fixed corner clipping in skewed squares and fonts. The affine translation offset `-extra_w / 2` was wrong (half-centering), causing the bottom-left corner (skew-x) and top-right corner (skew-y) to map to negative output coordinates and get clipped. Also replaced `int()` with `math.ceil()` to prevent off-by-one clipping at extreme values.

### Root cause
PIL `Image.AFFINE` maps output→input. For positive `skew_x` (top shifts right), the correct x-offset is `-extra_w` (anchors the bottom-left at output x=0). The original `-extra_w / 2` left only half the required room, clipping the bottom-left corner. Same error for `skew_y` on the y-offset.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/square_renderer.py` | `_apply_skew`: `int()` → `math.ceil()`; offset `−extra/2` → `−extra` (positive) or `0` (negative direction) |
| `imagegen/rendering/primitives/font_renderer.py` | `_render_skewed`: same affine offset fix |

---

## 2026-05-07 18:24:20 — Bug fix: skew-x= / skew-y= not applied in FontRenderer

### Summary
Fixed font skew: `skew-x=` and `skew-y=` on `font()` commands were silently ignored. The "Italic-style skew" text in example 15 appeared as normal upright text.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/font_renderer.py` | Added `import math`; extracted `skew-x`/`skew-y` params; added `_render_skewed()` method (temp surface → PIL affine shear → optional rotate → composite at pos); updated branch logic in `render()` |

---

## 2026-05-07 18:08:03 — Bug fix: skew-x= / skew-y= not applied in SquareRenderer

### Summary
Fixed a silent bug where `skew-x=` and `skew-y=` parameters on `square()` DSL commands were parsed and validated but never applied during rendering. All squares appeared un-skewed regardless of the parameter values.

### Root cause
Two-layer failure: (1) `TransformApplier` — which correctly implements skew via PIL affine transform — is never imported or called anywhere in the rendering pipeline (dead code). (2) `SquareRenderer.render()` draws the rectangle directly at final canvas coordinates via a full-canvas-sized temp image, which makes post-hoc transform application impossible.

### Fix approach
Added a `_apply_skew()` module-level helper (replicating the affine math from `TransformApplier._apply_skew`) and a skew branch inside `render()`:
- Zero skew → existing fast path unchanged (no behavior change)
- Non-zero skew → draw the rectangle on an isolated `(w, h)` RGBA surface at `(0, 0)`, apply the PIL affine shear, then alpha-composite the result at `(x, y)` on the canvas

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/square_renderer.py` | Added `import math`; added `_apply_skew()` module helper; added `skew-x`/`skew-y` extraction and skew path in `render()` |

---

## 2026-05-07 18:00:38 — Bug fix: font rotate= parameter not applied in FontRenderer

### Summary
Fixed a silent bug where the `rotate=` parameter on `font()` DSL commands was parsed and validated but never used during rendering. All text was drawn at 0° regardless of the `rotate` value.

### Root cause
`FontRenderer.render()` never read `params.get("rotate")`. Unlike `scale`, rotation cannot be handled by a simple multiplier — `ImageDraw.text()` has no angle argument. The fix renders text onto a temporary RGBA surface, rotates it with `Image.rotate(-angle, expand=True)` (negated because DSL is clockwise, PIL is counter-clockwise), then alpha-composites the result back onto the canvas centered on the original `pos`.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/font_renderer.py` | Extract `rotate` param; branch on `rotate == 0.0` (fast path: existing direct draw) vs non-zero (new `_render_rotated` method: temp surface → rotate → composite) |

---

## 2026-05-07 17:39:06 — Bug fix: font scale= parameter not applied in FontRenderer

### Summary
Fixed a silent bug where the `scale=` parameter on `font()` DSL commands was parsed and validated but never used during rendering, so all font variants appeared at the base `font-size` regardless of the scale value.

### Root cause
`FontRenderer.render()` extracted every other font parameter but never read `params.get("scale")`. The effective font size passed to `_resolve_font()` and `_render_multiline()` was always the raw `font-size`, ignoring any `scale` multiplier.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/primitives/font_renderer.py` | Extract `scale` param; compute `effective_font_size = max(1, int(font_size * scale))`; pass `effective_font_size` to both `_resolve_font` and `_render_multiline` |

---

## 2026-05-06 17:50:57 — Lexer border color fix

### Summary
Fixed lexer value-position tracking so hex colors like `#888888` are accepted after object attribute colons such as `border:`.

### Files changed
| File | Change |
|---|---|
| `imagegen/lexer.py` | Updated lexer value-position state for object attribute values |

---

## 2026-05-05 05:05:12 — FEA-007: Variable Support and Bounding Box Extraction

**Spec:** `2_Docs/FEA-007-prompt-variable-support-bbox-extraction.md`

### Summary
Implemented DSL-level variable declarations, named primitive binding, bounding-box property access, and expression evaluation in frame and function bodies.

### Files changed
| File | Change |
|---|---|
| `imagegen/token_type.py` | Added `DOT` token |
| `imagegen/ast_nodes.py` | Added `ExprBboxAccess`, `VarDeclStmt`, `AssignStmt`, `NamedDrawCmd`; extended unions |
| `imagegen/lexer.py` | Added `var` keyword; added DOT to regex and punc map |
| `imagegen/parser.py` | Frame/func bodies get `in_func_body=True, allow_var_stmts=True`; new parse methods for var/assign/bbox-access |
| `imagegen/rendering/variable_store.py` | New: `VariableStore` class |
| `imagegen/rendering/primitive_dispatcher.py` | Sequential exec for var frames; handles new node types; scope-aware expression resolution |
| `imagegen/rendering/function_executor.py` | Fresh `VariableStore` per call; partial expr resolution for function params |
| `imagegen/frame_runner.py` | Per-frame `VariableStore`; routes new statement types to geometry pass |
| `4_ExampleScripts/50_fea007_variable_bbox.dsl` | New: demonstration script |

### 2026-05-06 15:58:53 — Example scripts 17-27 and engine parsing fix
- File: `4_ExampleScripts/17_clip_rectangular.dsl`
- File: `4_ExampleScripts/18_clip_shape_circle.dsl`
- File: `4_ExampleScripts/19_clip_shape_polygon.dsl`
- File: `4_ExampleScripts/20_clip_combined.dsl`
- File: `4_ExampleScripts/21_background_solid.dsl`
- File: `4_ExampleScripts/22_background_gradient.dsl`
- File: `4_ExampleScripts/23_background_image.dsl`
- File: `4_ExampleScripts/24_background_with_primitives.dsl`
- File: `4_ExampleScripts/25_object_simple_button.dsl`
- File: `4_ExampleScripts/26_object_ui_panel.dsl`
- File: `4_ExampleScripts/27_object_nested.dsl`
- File: `imagegen/lexer.py`
- File: `imagegen/parser.py`

### Regression test
All 33 existing example DSL scripts pass with no changes.

### Key design decisions
- **Sequential execution**: frames containing `VarDeclStmt`, `AssignStmt`, or `NamedDrawCmd` bypass z-sorting; pure drawing frames retain z-sort behavior.
- **Scope disambiguation at runtime**: `ExprFactor(str)` resolved via `VariableStore.has_var()` — declared variables become `LengthValue`, undeclared names fall back to `IdentValue` for backward compatibility with enum-like values (e.g. `weight=bold`).
- **DSL bbox coordinates**: `_compute_dsl_bbox` computes `(x, y, width, height)` directly from `LengthValue.number` params (no AA-scale involved).
- **Function scope isolation**: each function call gets its own `VariableStore`; function parameters are pre-resolved to `LengthValue` before dispatch, so the function's variable store handles only explicit `var` declarations.

## 2026-05-09 07:04:51 - Feature implementation: FEA-009 decoupled object resizing and scaling behavior

### Summary
Implemented `resize-mode=layout` for object instances so explicit `width` and `height` can redefine the object layout box without implicitly scaling all internal geometry. The existing resize behavior remains the default path, while layout mode keeps `scale` active as a separate geometric transform.

### Files changed
| File | Change |
|---|---|
| `imagegen/rendering/object_instantiator.py` | Added layout-resize execution path; body attributes now bind instance `width`/`height` directly in `resize-mode=layout`; explicit `scale` remains active after layout resolution |
| `imagegen/semantic_validator.py` | Validated `resize-mode`, unwrapped expression-wrapped object `scale` / `rotate` values, and suppressed the default width/height-vs-scale warning in layout mode |
| `imagegen/rendering/bbox_renderer.py` | Updated object-instance AABB calculation so `resize-mode=layout` applies explicit `scale` even when width/height overrides are present |
| `4_ExampleScripts/99_object_layout_resize_panel.dsl` | Added a focused example comparing default object scaling, `resize-mode=layout`, and `resize-mode=layout` plus explicit `scale` |
| `2_Docs/my_vision.md` | Documented the chosen DSL keyword `resize-mode=layout` |
| `2_Docs/requirements.md` | Updated REQ-0044 to name `resize-mode=layout` explicitly |
| `2_Docs/system_design.md` | Updated object-instantiator parameter table with the final keyword semantics |
| `2_Docs/DSL_grammar_description.md` | Added `resize-mode` to the object-instance parameter reference and examples |
| `2_Docs/DSL_user_guide.md` | Added user-facing guidance and examples for layout resize mode |

### Verification
Rendered successfully:
- `python .\\imagegen.py .\\4_ExampleScripts\\25_object_simple_button.dsl`
- `python .\\imagegen.py .\\4_ExampleScripts\\26_object_ui_panel.dsl`
- `python .\\imagegen.py .\\4_ExampleScripts\\99_object_layout_resize_panel.dsl`

