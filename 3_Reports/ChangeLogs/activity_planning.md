# Activity Log — Planning

### 2026-04-25 09:27:35 — Update connector definition in vision
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Expanded connector primitive with multi-segment points, label + font properties, start-cap/end-cap shapes (replacing start-arrow/end-arrow), corner styles for multi-segment joints, and animated rolling pattern support for multi-frame GIF output.

### 2026-04-25 09:38:19 — Create requirements document
- File: `3_Reports/requirements_2026-04-25-093459.md`
- Action: Created
- Details: Full structured requirements document (REQ-0001 through REQ-0033) covering Functional, Non-Functional, Data, UI/UX, and Integration requirements derived from my_vision.md.

### 2026-04-25 10:10:16 — Create DSL grammar description
- File: `2_Docs/DSL_grammar_description.md`
- Action: Created
- Details: Comprehensive DSL grammar reference document covering EBNF formal grammar, lexical conventions, all drawing primitives, object templates, function declarations, include mechanism, data types, default values, annotated examples, and error reference.

### 2026-04-25 10:24:36 — Create DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Created
- Details: 100% coverage. Found 3 High and 2 Medium issues in DSL_grammar_description.md.

### 2026-04-25 10:25:43 — Fix DSL grammar issues 1-5
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Fixed all 5 issues: undefined EBNF key token, missing obj-attr rules, border/shadow nesting, none in color grammar, output-format default inconsistency. Version bumped to 1.1.

### 2026-04-25 11:49:42 — Fix Issue 6: transparent/none semantics
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Section 15.1 expanded with explicit bullets distinguishing `none` (no-paint, fill/background-only, parse error on stroke) from `transparent` (general named color, any property). File version bumped to 1.2.

### 2026-04-25 11:52:21 — Fix Issue 7: background EBNF parameter ordering
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: `<background-params>` rewritten to use `<named-param-list>`; three fixed-order sub-rules removed; comment block added for key-presence disambiguation. File version bumped to 1.3.

### 2026-04-25 11:54:44 — Fix Issue 8: output-format=images file naming
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: `<frame-id>.png`/`.jpeg` naming rule added to §6 `output-format` parameter description. File version bumped to 1.4.

### 2026-04-25 12:01:19 — Fix DSL grammar Issues 9-12 (re-verification of v1.4)
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Issue 9: added arithmetic expression EBNF rules (`<expr>`, `<expr-term>`, `<expr-factor>`, `<expr-point>`). Issue 10: trailing terminator for `<image-def>`. Issue 11: optional terminators for frame/obj attributes. Issue 12: removed duplicate `image` keyword. File version bumped to 1.5.

### 2026-04-25 12:01:19 — Re-verify DSL grammar description v1.4 (Issues 9-12)
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: 4 new issues found and all resolved. Summary table extended to 12 issues. Report version bumped to 2.0.

### 2026-04-25 12:08:40 — Fix DSL grammar Issues 13-20 (re-verification of v1.5)
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added `<string>`, `<line-type>`, `<number>` EBNF rules; removed redundant `<number>` from `<value>`; fixed `<number-0-1>` empty-match bug; added `{n}` to notation legend; fixed unquoted font-family in examples; corrected §4 forward-reference prose. File version bumped to 1.6.

### 2026-04-25 12:08:40 — Re-verify DSL grammar description v1.5 (Issues 13-20)
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: 8 new issues (13-20) found and all resolved. Report version bumped to 2.1. All 20 issues resolved.

### 2026-04-25 12:43:00 — Semantic correctness review of DSL grammar v1.6 (Issues 21-31)
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: 11 semantic issues found and fixed. Transform order corrected, identifier-hyphen disambiguation added, circular include detection, zero-param grammar, `%` fallback, `none` semantic error correction, connector mutual exclusivity, arg count mismatch error, hold-time/dpi type fix, coordinate scope wording, fill-on-line/path error table entries. File version bumped to 1.7.

### 2026-04-25 12:43:00 — Update verification report for semantic review (Issues 21-31)
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: 11 new issues (21-31) documented, all resolved. Summary table extended to 31 rows (8H/14M/9L). Report version bumped to 2.2.

### 2026-04-29 19:58:12 — Create DSL user guide
- File: `2_Docs/DSL_user_guide.md`
- Action: Created
- Details: New practical user guide for DSL script authors. 17 sections covering all language features with annotated examples and a common mistakes reference.

### 2026-04-29 20:21:41 — Create example scripts plan
- File: `3_Reports/example_scripts_plan_2026-04-29-202005.md`
- Action: Created
- Details: Prioritized plan for 50 AI-generated DSL example scripts. 12 categories from BEGINNER to ADVANCED, 30 MUST-HAVE and 20 NICE-TO-HAVE scripts, with a 4-wave generation order based on feature dependencies.

### 2026-05-05 19:17:51 — Create etalon image generator/checker implementation plan
- File: `Tools/AIPrompts/impl_generate_check_etalonn_imageset.md`
- Action: Created
- Details: Documented a CLI-driven plan for generating and verifying `_etalon` image copies.

### 2026-05-09 06:44:42 - Add FEA-009 documentation for decoupled object resizing and scaling
- Files: `2_Docs/my_vision.md`, `2_Docs/requirements.md`, `2_Docs/system_design.md`, `2_Docs/FEA-009-prompt-decoupled-object-resizing-scaling-behavior.md`
- Action: Created/Updated
- Details: Added a new feature prompt and aligned the core architecture documents around an opt-in layout-resize mode that separates object bounding-box resizing from explicit geometric scaling while preserving the current default behavior.
