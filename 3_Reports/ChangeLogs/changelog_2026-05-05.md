# Changelog — 2026-05-05

### 2026-05-05 05:05:12 — Claude Sonnet 4.6 / FEA-007 Implementation — Variable Support and Bounding Box Extraction

- File: `imagegen/token_type.py`
- Action: Updated
- Details: Added `DOT` token type for `.` property-access syntax (e.g. `rect1.bbox.x`)

- File: `imagegen/ast_nodes.py`
- Action: Updated
- Details: Added `ExprBboxAccess`, `VarDeclStmt`, `AssignStmt`, `NamedDrawCmd` nodes; extended `ExprNode` and `DrawingCmd` unions; moved `PrimitiveNode` definition before new nodes; updated module docstring

- File: `imagegen/lexer.py`
- Action: Updated
- Details: Added `var` to `_KEYWORDS`; added `DOT` to the master regex and punctuation map

- File: `imagegen/parser.py`
- Action: Updated
- Details: Frame and function bodies now parsed with `in_func_body=True, allow_var_stmts=True`; added `_parse_var_decl`, `_parse_named_or_assign`, `_parse_bbox_access` methods; `_parse_drawing_commands` extended with `allow_var_stmts` flag; `_parse_expr_factor` detects DOT and delegates to bbox-access parser; `_parse_drawing_stmt` handles `var` keyword and `IDENT = ...` assignment syntax

- File: `imagegen/rendering/variable_store.py`
- Action: Created
- Details: New `VariableStore` class holding numeric variable values and named-object bounding boxes for a single frame or function scope

### 2026-05-05 19:17:51 — Etalon image generator/checker implementation
- File: `Tools/AIPrompts/impl_generate_check_etalonn_imageset.md`
- Action: Created
- Details: Added an implementation plan for generating and verifying `_etalon` image copies with supported image extensions and CLI validation.

- File: `Tools/generate_check_etalonn_imageset.py`
- Action: Created
- Details: Added a Python CLI tool to copy source images to `_etalon` variants and compare etalon files against originals, with missing-file handling and summary reporting.

- File: `imagegen/rendering/primitive_dispatcher.py`
- Action: Updated
- Details: `dispatch_all` accepts optional `variable_store`; sequential execution when variable statements are present; `_dispatch_one` handles `VarDeclStmt`, `AssignStmt`, `NamedDrawCmd`; `_eval_expr` evaluates expressions with store; `_resolve_value` is scope-aware (declared variables → LengthValue, undeclared → IdentValue fallback); `_compute_dsl_bbox` module-level function extracts DSL-coord bboxes from primitives

- File: `imagegen/rendering/function_executor.py`
- Action: Updated
- Details: Creates fresh `VariableStore` for each function call; `_resolve_cmd` handles `VarDeclStmt`, `AssignStmt`, `NamedDrawCmd`; `_partially_resolve_expr` substitutes function param refs while preserving `ExprBboxAccess` for runtime resolution; `_evaluate_expr` returns 0.0 for `ExprBboxAccess` (cannot pre-resolve)

- File: `imagegen/frame_runner.py`
- Action: Updated
- Details: Imports `VarDeclStmt`, `AssignStmt`, `NamedDrawCmd`; imports `VariableStore`; creates per-frame `VariableStore` shared across geometry and text passes; preprocessing loop routes new statement types to `geometry_cmds`

- File: `4_ExampleScripts/50_fea007_variable_bbox.dsl`
- Action: Created
- Details: Example demonstrating FEA-007: three horizontally chained squares using bbox-based positioning, plus a circle centered on the first block using extracted bbox coordinates

### 2026-05-05 05:30:00 — Claude Sonnet 4.6 / Regression Investigation — Rotation / Scale / BBox Overlay Fix Plan

- File: `3_Reports/impl_rot_bbox_fix_2026-05-05-053000.md`
- Action: Created
- Details: Implementation plan documenting root cause of two silent regressions introduced by FEA-007: (1) show-bbox overlays no longer drawn for circles/squares/pies/arcs; (2) object rotate and scale params silently ignored. Root cause: frame bodies now parsed with in_func_body=True, wrapping all NUMBER params as ExprFactor(LengthValue). Plan covers exact line-level changes to bbox_renderer.py and object_instantiator.py via a new _unwrap_length() helper. No Python source modified.

### 2026-05-05 06:30:00 — Claude Sonnet 4.6 / FEA-007 Docs — DSL Grammar and User Guide Updated

- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated (v3.4 → v3.5)
- Details: Added `var` keyword; updated §3 EBNF (new `<var-decl-stmt>`, `<assign-stmt>`, `<named-draw-cmd>`, `<bbox-access>` productions; updated `<drawing-stmt>` and `<expr-factor>`); updated §4 Execution Model; updated §13.3 expression note; added full §14 Variable Support and Bounding Box Extraction (7 subsections covering declarations, assignment, named draw cmds, bbox access, scope/execution, grammar summary, complete example); renumbered §14→§15 through §18→§19; added 8 new error rows to §19.1

- File: `2_Docs/DSL_user_guide.md`
- Action: Updated (v1.4 → v1.5)
- Details: Added §20 Variables and Layout Chaining (var declarations, assignment, named primitives, bbox access table, sequential execution note, function scope, scope rules table, complete example); added Common Mistakes §18 (bbox before render), §19 (missing var), §20 (var in object body)

### 2026-05-05 05:45:00 — Claude Sonnet 4.6 / Regression Fix — Rotation / Scale / BBox Overlay Restored

- File: `imagegen/rendering/bbox_renderer.py`
- Action: Updated
- Details: Added `ExprFactor` import and `_unwrap_length()` helper; replaced all `isinstance(x, LengthValue)` guards in `_compute_aabb` (CircleNode, PieNode/ArcNode, SquareNode, FontNode, ImagePrimNode) and `_object_inst_aabb` (width, height, scale, rotate) with `_unwrap_length()` calls — restores show-bbox overlays for frame-level primitives

- File: `imagegen/rendering/object_instantiator.py`
- Action: Updated
- Details: Added `ExprFactor` import and `_unwrap_length()` helper; replaced `isinstance(scale_param/rotate_param, LengthValue)` guards in `instantiate` with `_unwrap_length()` calls — restores scale= and rotate= on object instances in frames
