# Daily Changelog — 2026-05-04

| Field | Value |
|---|---|
| **Description** | Daily changelog for 2026-05-04 |
| **Created at** | 2026-05-04 09:20:20 |
| **File version** | 1.1 |
| **Created by** | Claude Sonnet 4.6 |

---

## FEA-006 — Named Color Palette Support

### imagegen/token_type.py

- Added `AT_SIGN = auto()` token type for the `@` palette reference prefix
- Placed between `LBRACKET`/`RBRACKET` group and `PLUS`; before `MINUS`

### imagegen/lexer.py

- Added `"begin_palette"` and `"end_palette"` to the `_KEYWORDS` frozenset
- Added `(?P<AT_SIGN>@)` regex group to `_TOKEN_RE`, inserted after `COLOR_HEX` and before `IDENT`
- Added `AT_SIGN` handling in `tokenize()`: emits `Token(TokenType.AT_SIGN, ...)` and resets `in_value_pos`
- Extended depth-tracking to cover `begin_palette`/`end_palette` (increments/decrements `depth` so that newlines inside palette bodies are correctly emitted as statement terminators)

### imagegen/ast_nodes.py

- Added `PaletteRef` frozen dataclass (fields: `alias: str`, `source_file: str`, `line: int`): represents an unresolved `@alias` color reference produced by the parser
- Added `PaletteDef` frozen dataclass (fields: `palette_name: str`, `entries: dict`, `source_file: str`, `line: int`): represents a `begin_palette`/`end_palette` block
- Added `PaletteRef` to the `Value` union type
- Added `PaletteDef` to the `TopLevelStmt` union type

### imagegen/parser.py

- Added `PaletteDef`, `PaletteRef` to imports from `imagegen.ast_nodes`
- Added `"begin_palette"` dispatch in `_parse_top_level()` → calls `_parse_palette_def()`
- Added `_parse_palette_def()` method: parses `begin_palette <name>` … `end_palette`; collects alias entries via `_parse_color_value()`; raises parse errors for empty blocks and duplicate aliases within the same block
- Added `AT_SIGN` branch in `_parse_value()` → calls `_parse_palette_ref()`
- Added `_parse_palette_ref()` method: consumes `AT_SIGN` + `IDENTIFIER`; returns `PaletteRef` node

### imagegen/symbol_table.py

- Added `palettes: dict[str, ColorValue | ColorNone]` field (default empty dict)
- Added `register_palette(palette_def, reporter)` method: merges all alias entries into `palettes`; raises parse error on duplicate alias name
- Added `lookup_palette_alias(alias)` method: returns `ColorValue | ColorNone | None`

### imagegen/resolver.py

- Added imports: `replace` from `dataclasses`, `PaletteDef`, `PaletteRef`, `ColorValue`, `ColorNone`, `Value`, `ObjAttr`, `FuncCall`, `DrawingCmd` from `imagegen.ast_nodes`
- Added `PaletteDef` case in `_collect_symbols()`: calls `symbol_table.register_palette()`
- `resolve()` now calls `_resolve_palette_refs()` before returning; fast-path when no palettes are defined
- Added `_resolve_palette_refs()`: replaces `PaletteRef` values in all frame bodies, object template bodies/attributes, and function bodies
- Added `_resolve_frame()`, `_resolve_obj_template()`, `_resolve_func_decl()`, `_resolve_cmd()`, `_resolve_value()` helpers
- `_resolve_value()` raises parse error for any unresolved `@alias` after full collection

### 2_Docs/DSL_grammar_description.md (version 3.3 → 3.4)

- §2.8 Keywords: added `begin_palette`/`end_palette`; added `@` prefix callout note
- §3 EBNF: added `<palette-def>` to `<top-level-stmt>`; added `<palette-def>` and `<color-entry>` productions; added `<palette-ref>` to `<color>` production; added `<palette-ref>` non-terminal
- §4 Top-Level Structure: updated Pass 1 description; added `Palette` row to summary table
- §14 Include: added `begin_palette` to imported-definitions list; added duplicate-alias-error note
- §15.1 Color Values: added `Palette alias` row to the formats table; added `@<alias>` bullet in notes
- Added §15.7 Palette Definitions and Alias References: full syntax, constraints, resolution timing, example
- §18.1 Parse Errors: added five new palette error rows

### 2_Docs/DSL_user_guide.md (version 1.3 → 1.4)

- ToC: added §17 Named Color Palettes; renumbered Units Reference → §18, Common Mistakes → §19
- §3 Script Structure: added `begin_palette`/`end_palette` to code block and table; updated namespace note
- §16 Colors Reference: added `Palette alias` row to formats table
- Added §17 Named Color Palettes: palette syntax, `@alias` usage, library-file pattern, forward references, rules summary
- Added Common Mistakes §15/16/17: `@alias` in palette body, duplicate alias, undefined alias

---

## FEA-007 — Variable Support and Bounding Box Extraction in DSL

### 2026-05-04 18:12:00 — FEA-007 feature documents

- File: `2_Docs/FEA-007-prompt-variable-support-bbox-extraction.md`
- Action: Created
- Details: Feature prompt document for FEA-007; covers variable declarations, bbox property access, assignment syntax, expression usage, sequential execution model, scope rules, open questions resolved

### 2026-05-04 18:12:00 — FEA-007 my_vision.md update

- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Added "Variable declarations and bounding box extraction" section to DSL language description; covers var syntax, identifier rules, scope, reassignment, bbox properties, assignment syntax, expression usage, error conditions, and example script

### 2026-05-04 18:12:00 — FEA-007 requirements.md update

- File: `2_Docs/requirements.md`
- Action: Updated (version 2.1 → 2.2)
- Details: Updated REQ-0028 grammar with var-decl/var-assign/bbox-access productions; added section 1.20 with REQ-0041 (var declaration), REQ-0041.1 (bbox property access), REQ-0041.2 (assignment from bbox), REQ-0041.3 (variable usage in expressions), REQ-0041.4 (sequential execution model), REQ-0041.5 (error handling)

### 2026-05-04 18:12:00 — FEA-007 system_design.md update

- File: `2_Docs/system_design.md`
- Action: Updated (version 1.6 → 1.7)
- Details: Updated architecture diagram with Variable Store / Bbox Extractor step; added section 3.3.11 (Variable Store and Bbox Extractor) with scope model, processing steps, error conditions, new module variable_store.py; updated traceability table with new row covering REQ-0041 through REQ-0041.5
