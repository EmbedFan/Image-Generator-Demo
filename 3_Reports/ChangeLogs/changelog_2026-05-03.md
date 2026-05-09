# Changelog 2026-05-03

### 2026-05-03 09:47:19 — FEA-005 — Optional Bounding Box Rendering — my_vision.md
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Added bounding box overlay parameter documentation after the grid system section.
  Describes show-bbox=true|false, post-transform AABB geometry, overlay rendering semantics,
  contrast-aware color computation (inverted luminance), dashed line style, applicability to
  all drawable elements, and backward-compatibility guarantee.

### 2026-05-03 09:47:19 — FEA-005 — Optional Bounding Box Rendering — requirements.md
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added section 1.18 Bounding Box Visualization with six new requirements:
  REQ-0039 (optional show-bbox parameter; parse error on non-drawable),
  REQ-0039.1 (AABB from post-transform geometry),
  REQ-0039.2 (overlay; no layout/z-index/clipping impact),
  REQ-0039.3 (inverted-luminance contrast-aware color; non-configurable),
  REQ-0039.4 (dashed 1px line; fixed),
  REQ-0039.5 (applies to all primitive and object types),
  REQ-0039.6 (backward compatible; omitting parameter = identical output).
  File version 1.9 → 2.0.

### 2026-05-03 09:47:19 — FEA-005 — Optional Bounding Box Rendering — system_design.md
- File: `2_Docs/system_design.md`
- Action: Updated
- Details: Architecture diagram extended with BBox Overlay Renderer step (post-transform,
  pre-Grid Renderer). Added section 3.3.10 with processing steps, per-element AABB derivation
  table, and design notes. Traceability table updated with BBox Overlay Renderer row.
  File version 1.4 → 1.5.

### 2026-05-03 15:20:19 — FEA-005 — Optional Bounding Box Rendering — implementation
- File: `imagegen/rendering/bbox_renderer.py`
- Action: Created
- Details: New post-process BBox Overlay Renderer module. render_bbox_overlays() iterates
  all drawable commands with show-bbox=true, computes per-type AABB (circle, square, line,
  polygon, path, pie, arc, connector, font, image, object instance), samples avg canvas
  luminance in the AABB region to derive contrast-aware black/white overlay color, draws
  dashed 1px rectangle using _draw_dashed_segment(). ObjectInst AABB accounts for rotation.
  Degenerate (zero-height/width) bboxes padded by 1px.

### 2026-05-03 15:20:19 — FEA-005 — Optional Bounding Box Rendering — frame_runner.py
- File: `imagegen/frame_runner.py`
- Action: Updated
- Details: Added import of render_bbox_overlays; added call after grid rendering step,
  passing combined geometry_cmds + text_cmds and symbol_table for ObjectInst lookup.

### 2026-05-03 15:20:19 — FEA-005 — Optional Bounding Box Rendering — semantic_validator.py
- File: `imagegen/semantic_validator.py`
- Action: Updated
- Details: Added validation errors for show-bbox on Background and GridNode nodes;
  emits descriptive error message directing users to drawable primitives and object instances.

### 2026-05-03 09:47:19 — FEA-005 — Optional Bounding Box Rendering — FEA-005 prompt file
- File: `2_Docs/FEA-005-prompt-optional-bounding-box-rendering.md`
- Action: Created
- Details: Feature prompt file for FEA-005 documenting the feature description, requirements
  summary (geometry, visualization, applicability, parameter conventions), and goal.

### 2026-05-03 20:46:05 — FEA-006 — Named Color Palette Support — FEA-006 prompt file
- File: `2_Docs/FEA-006-prompt-named-color-palette.md`
- Action: Created
- Details: Feature prompt file for FEA-006 documenting the palette definition syntax
  (begin_palette/end_palette), color entry format, @alias reference syntax with examples,
  requirements summary, and goal.

### 2026-05-03 20:46:05 — FEA-006 — Named Color Palette Support — my_vision.md
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Added named color palettes entry in the language reference (after color format line)
  describing begin_palette/end_palette syntax, alias=color_value entries, @alias reference
  in color params, global namespace, and parse error on undefined alias.
  Updated Basic Grammar section: <script> now <top-level-stmt>+; added <palette-def> and
  <color-entry> productions.

### 2026-05-03 20:46:05 — FEA-006 — Named Color Palette Support — requirements.md
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Updated REQ-0020 to include @alias as accepted color format. Updated REQ-0028 DSL
  grammar with <palette-def> and <color-entry> productions. Added section 1.19 Named Color
  Palette Support: REQ-0040 (block definition), REQ-0040.1 (color entries), REQ-0040.2
  (@alias reference), REQ-0040.3 (global scope), REQ-0040.4 (included files), REQ-0040.5
  (undefined alias error), REQ-0040.6 (backward compatibility). File version 2.0 → 2.1.

### 2026-05-03 20:46:05 — FEA-006 — Named Color Palette Support — system_design.md
- File: `2_Docs/system_design.md`
- Action: Updated
- Details: Added Palette Collector row to Pass 1 Symbol Collector table. Added palettes entry
  to global symbol table structure. Updated namespace collision note. Updated Semantic
  Validator row to include @alias resolution. Extended Color System row in traceability table;
  added Color Palette Support row covering REQ-0040–REQ-0040.6. File version 1.5 → 1.6.
