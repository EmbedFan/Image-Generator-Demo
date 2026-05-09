# Changelog 2026-05-02

### 2026-05-02 19:57:13 — FEA-004 — configurable-grid-system
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Added grid system section after transformations entry — syntax for grid(), render=,
  align=, per-element snap=, alignment-before-transforms rule, backward-compatibility note.

### 2026-05-02 19:57:13 — FEA-004 — configurable-grid-system
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added section 1.17 Grid System: REQ-0038 (grid definition, at most one per frame),
  REQ-0038.1 (visual rendering with color/line-type/line-width), REQ-0038.2 (global align=true),
  REQ-0038.3 (per-element snap with snap=none opt-out), REQ-0038.4 (alignment before transforms).
  File version 1.8 → 1.9.

### 2026-05-02 19:57:13 — FEA-004 — configurable-grid-system
- File: `2_Docs/system_design.md`
- Action: Updated
- Details: Added Grid Resolver to architecture diagram (between Background Renderer and Primitive
  Dispatcher) and Grid Renderer post-process step; added section 3.3.9 Grid System (attributes
  table, processing steps, snap semantics, new modules grid_resolver.py / grid_renderer.py);
  updated section 9 traceability with Grid System row. File version 1.3 → 1.4.

### 2026-05-03 07:57:16 — FEA-004 — configurable-grid-system
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added <grid-stmt> to EBNF drawing-stmt; added §7.4 Grid Statement (param table, snap semantics,
  constraints, examples); added snap row to §8.0 shared params with grid dependency note; added
  3 parse error rows to §18.1; added 2 validation rows to §18.2. File version 3.1 → 3.2.

### 2026-05-03 07:57:16 — FEA-004 — configurable-grid-system
- File: `2_Docs/DSL_user_guide.md`
- Action: Updated
- Details: Added §15 Grid System (grid() syntax, visible grid, global align, per-element snap,
  transform-order note); renumbered old §15-17 to §16-18; added Common Mistakes §13 (snap without
  grid) and §14 (two grid() statements). File version 1.1 → 1.2.

### 2026-05-02 19:57:13 — FEA-004 — configurable-grid-system
- File: `2_Docs/FEA-004-prompt-configurable-grid-system.md`
- Action: Created
- Details: Implementation plan: DSL syntax examples, 5 files to modify/create, 5-step guide
  with code snippets (GridNode dataclass, snap_position(), render_grid(), frame runner wiring),
  14-case testing plan, and backward-compatibility notes.

### 2026-05-02 19:45:00 — FEA-003 fix — render-at-target-size
- File: `imagegen/rendering/object_instantiator.py`
- Action: Updated
- Details: Replaced render-native-then-bitmap-resize with render-directly-at-target-size approach.
  The off-screen buffer is now created at target pixel dimensions and obj_canvas.info["aa_scale"]
  is set to aa_scale * (target/native) so all primitive renderers naturally draw at the scaled
  coordinate space, filling the full buffer. No Image.resize() post-process step remains.
  Clip mask also receives the scaled render_aa so clip-bounds coordinates map correctly.

### 2026-05-02 19:28:12 — FEA-003: optional size and rotation parameters for DSL objects
- Added "Instance-time size and rotation" subsection to §11 (Reusable Objects) with examples for explicit width/height, scale factor, and rotate
- Renamed former "Object attributes" table heading to clarify it covers template-definition syntax
- Added Common Mistakes §11 (rotate with unit suffix) and §12 (scale=0 on object instance)
- File version 1.0 → 1.1


### 2026-05-02 08:12:13 — FEA-001 — font-discovery-cli
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added section 4.2 Font Discovery Command with REQ-0034 (--list-fonts CLI flag),
  REQ-0034.1 (DSL font names), REQ-0034.2 (style enumeration),
  REQ-0034.3 (size info), REQ-0034.4 (Hungarian glyph detection). File version 1.5 → 1.6.

### 2026-05-02 08:12:13 — FEA-001 — font-discovery-cli
- File: `2_Docs/system_design.md`
- Action: Updated
- Details: Added section 3.6 (Font Discovery Command), updated section 6.1 (--list-fonts flag),
  added section 7.5 (matplotlib + fonttools dependencies), updated section 9 (traceability).
  File version 1.0 → 1.1.

### 2026-05-02 08:12:13 — FEA-001 — font-discovery-cli
- File: `2_Docs/FEA-001-prompt-font-list-cli.md`
- Action: Created
- Details: Implementation plan for the font discovery CLI command: CLI interface design,
  font_discovery.py module, step-by-step implementation guide, files to create/modify,
  and testing plan with 9 test cases.

### 2026-05-02 08:49:26 — FEA-001 implementation — font-discovery-cli
- File: `imagegen/font_discovery.py`
- Action: Created
- Details: Full implementation of font discovery module: _collect_families() via matplotlib
  font_manager, _map_style() with weight normalisation for int/str weights, _get_size_info()
  with fonttools EBLC/CBLC bitmap detection, _has_hungarian_glyphs() checking 18 code points,
  list_fonts() printing structured report to stdout.

### 2026-05-02 08:49:26 — FEA-001 implementation — font-discovery-cli
- File: `imagegen.py`
- Action: Updated
- Details: Added --list-fonts flag (argparse); made input_file optional (nargs='?');
  added mutual-exclusivity guard; dispatch to imagegen.font_discovery.list_fonts(); updated
  docstring with new usage form and exit code 0 for --list-fonts.

### 2026-05-02 08:49:26 — FEA-001 implementation — font-discovery-cli
- File: `requirements.txt`
- Action: Created
- Details: Added Pillow>=9.0, matplotlib>=3.5, fonttools>=4.0 as project dependencies.

### 2026-05-02 17:30:45 — FEA-002 — utf8-encoding-fix
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added section 1.15 Encoding with REQ-0035 (explicit UTF-8 file reading, non-UTF-8 → I/O error)
  and REQ-0035.1 (silent BOM strip). File version 1.6 → 1.7.

### 2026-05-02 17:30:45 — FEA-002 — utf8-encoding-fix
- File: `2_Docs/system_design.md`
- Action: Updated
- Details: Updated section 3.2 Lexer/Parser row (UTF-8 + BOM), section 5.1 Input Files (UTF-8
  enforcement note), section 8.1 I/O error row (byte position in error), section 9 traceability
  (Encoding row). File version 1.1 → 1.2.

### 2026-05-02 17:30:45 — FEA-002 — utf8-encoding-fix
- File: `2_Docs/FEA-002-prompt-utf8-encoding-fix.md`
- Action: Created
- Details: Implementation plan: problem description, 2 files to modify (lexer.py, resolver.py),
  3 implementation steps (encoding fix, BOM strip, included files), 6-case testing plan, notes
  on editor behavior (VS Code, Notepad).

### 2026-05-02 17:35:31 — FEA-002 implementation — utf8-encoding-fix
- File: `imagegen/orchestrator.py`
- Action: Updated
- Details: Added BOM strip (lstrip ﻿) on main DSL file read; added UnicodeDecodeError
  handler reporting file path and byte position via reporter.io_error().

### 2026-05-02 17:35:31 — FEA-002 implementation — utf8-encoding-fix
- File: `imagegen/resolver.py`
- Action: Updated
- Details: Added BOM strip (lstrip ﻿) on included DSL file read; added UnicodeDecodeError
  handler reporting file path and byte position via reporter.io_error().

### 2026-05-02 17:35:31 — FEA-002 implementation — utf8-encoding-fix
- File: `2_Docs/FEA-002-prompt-utf8-encoding-fix.md`
- Action: Updated
- Details: Corrected "Files to Modify" table — actual file reads are in orchestrator.py and
  resolver.py, not lexer.py (lexer only tokenises strings passed in).

### 2026-05-02 18:59:02 — FEA-003 — dsl-object-size-rotation
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Extended Object instantiation and reuse section with 5 new bullet points covering
  optional width/height override, scale factor, precedence rule, rotate parameter, and
  backward compatibility note.

### 2026-05-02 18:59:02 — FEA-003 — dsl-object-size-rotation
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added section 1.16 Object Instance Size and Rotation with REQ-0036 (explicit width/height),
  REQ-0036.1 (scale factor), REQ-0036.2 (size precedence over scale, with warning),
  REQ-0037 (clockwise rotation). File version 1.7 → 1.8.

### 2026-05-02 18:59:02 — FEA-003 — dsl-object-size-rotation
- File: `2_Docs/system_design.md`
- Action: Updated
- Details: Updated section 3.3.7 REQ coverage and added instance-time size/rotation parameters
  table (width, height, scale, rotate); updated section 9 traceability row for Object Template
  Instantiator. File version 1.2 → 1.3.

### 2026-05-02 18:59:02 — FEA-003 — dsl-object-size-rotation
- File: `2_Docs/FEA-003-prompt-dsl-object-size-rotation.md`
- Action: Created
- Details: Implementation plan: DSL syntax examples, 3 files to modify (parser, validator,
  instantiator), 3-step implementation guide with code snippets, 13-case testing plan,
  and backward-compatibility notes.

### 2026-05-02 18:59:02 — FEA-003 implementation — dsl-object-size-rotation
- File: `imagegen/parser.py`
- Action: Updated
- Details: Fixed is_named disambiguation in _parse_inst_or_call to also accept KEYWORD tokens
  (e.g. width=, height=) as the start of a named-parameter list, not just IDENTIFIER tokens.

### 2026-05-02 18:59:02 — FEA-003 implementation — dsl-object-size-rotation
- File: `imagegen/semantic_validator.py`
- Action: Updated
- Details: Added FEA-003 validation in _validate_object_inst: scale > 0 error; rotate >= 0 error;
  rotate with unit suffix error; warning when both explicit width/height and scale provided.

### 2026-05-02 18:59:02 — FEA-003 implementation — dsl-object-size-rotation
- File: `imagegen/rendering/object_instantiator.py`
- Action: Updated
- Details: Replaced fixed size computation with priority logic (explicit w/h > scale > template
  default); added clockwise rotation via PIL rotate(-angle, expand=True) with paste-position
  correction to keep visual centre anchored at pos + half-size.

### 2026-05-02 19:28:12 — FEA-003 documentation — dsl-object-size-rotation
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Updated §12.3 (Object Instantiation): added instance-time size/rotation parameter table
  (width, height, scale, rotate); precedence rule; validation error and warning message patterns;
  five DSL usage examples. File version 3.0 → 3.1.

### 2026-05-02 19:28:12 — FEA-003 documentation — dsl-object-size-rotation
- File: `2_Docs/DSL_user_guide.md`
- Action: Updated
- Details: Added "Instance-time size and rotation" subsection to §11 with code examples for
  explicit width/height, scale, rotate, and combined usage; added Common Mistakes §11 (rotate
  with unit) and §12 (scale=0 on object instance). File version 1.0 → 1.1.
