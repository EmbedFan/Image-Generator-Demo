# Changelog 2026-04-25

### 2026-04-25 09:27:35 — Agent — Update connector definition in vision
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Expanded connector primitive with multi-segment points, label + font properties, start-cap/end-cap shapes (replacing start-arrow/end-arrow), corner styles for multi-segment joints, and animated rolling pattern support for multi-frame GIF output.

### 2026-04-25 09:38:19 — Agent — Create requirements document
- File: `3_Reports/requirements_2026-04-25-093459.md`
- Action: Created
- Details: Full structured requirements document (REQ-0001 through REQ-0033) covering Functional, Non-Functional, Data, UI/UX, and Integration requirements derived from my_vision.md.

### 2026-04-25 09:45:57 — Agent — Create requirements verification report
- File: `3_Reports/verification_requirements_2026-04-25-094514.md`
- Action: Created
- Details: Verified 2_Docs/requirements.md against 2_Docs/my_vision.md. Found 5 issues: 1 High (wrong dependency REQ-0004.3/REQ-0013), 3 Medium (border shadow gap, optional param defaults gap, grammar incomplete), 1 Low (arc primitive undefined).

### 2026-04-25 09:47:37 — Agent — Fix Issue 1 in requirements
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Fixed wrong dependency in REQ-0004.3 and REQ-0013: replaced REQ-0033 with REQ-0032 (External Image Asset Support).

### 2026-04-25 09:49:09 — Agent — Fix Issue 2 in requirements
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added REQ-0014.4 (Object Border Shadow) with shadow(offset-x offset-y blur-radius color) parameters, acceptance criteria for blur and hard-edged shadow. File version bumped to 1.2.

### 2026-04-25 09:50:34 — Agent — Fix Issue 3 in requirements
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added REQ-0025.1 (Optional Parameter Defaults and Named-Parameter Ordering): defaults fill=none, z-index=declaration-order, style=normal, weight=normal; named params are order-independent. File version bumped to 1.3.

### 2026-04-25 09:52:25 — Agent — Fix Issue 4 in requirements
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Expanded REQ-0028 grammar: new top-level rule allows frames/func-decls/obj-templates/include-stmts; added func-decl, func-call, object-inst, include-stmt productions; updated dependencies and acceptance criteria. File version bumped to 1.4.

### 2026-04-25 09:56:09 — Agent — Fix Issue 5: add arc primitive to vision and requirements
- File: `2_Docs/my_vision.md`
- Action: Updated
- Details: Added arc primitive definition after pie: open curved arc, stroke only, no fill, no lines to center.

### 2026-04-25 09:56:09 — Agent — Fix Issue 5: add arc primitive to vision and requirements
- File: `2_Docs/requirements.md`
- Action: Updated
- Details: Added REQ-0010.1 (Primitive: arc) with acceptance criteria distinguishing arc from pie. File version bumped to 1.5.

### 2026-04-25 09:58:23 — Agent — Re-verify requirements against vision
- File: `3_Reports/verification_requirements_2026-04-25-094514.md`
- Action: Updated

### 2026-04-25 10:10:16 — Agent — Create DSL grammar description
- File: `2_Docs/DSL_grammar_description.md`
- Action: Created
- Details: Comprehensive DSL grammar reference document covering EBNF grammar, all primitives, object templates, functions, include, data types, parameter tables, annotated examples, and error reference.

### 2026-04-25 10:24:36 — Agent — Create DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Created
- Details: Verified DSL_grammar_description.md against requirements.md and my_vision.md. 100% coverage. Found 5 issues: 3 High (undefined EBNF token, missing obj-attr rules, wrong border/shadow nesting), 2 Medium (none not in color grammar, output-format default contradiction).

### 2026-04-25 10:25:43 — Agent — Fix DSL grammar issues 1-5
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Fixed all 5 issues from verification report. Removed undefined `<key>` token; added shadow/clip-bounds/clip-shape to obj-attr EBNF; separated shadow from border-value; added `none` to color grammar; clarified output-format defaults. File version bumped to 1.1.

### 2026-04-25 11:32:44 — Agent — Resolve Issue 1 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Marked Issue 1 (undefined `<key>` token) as RESOLVED. Added Status column to issue summary table. File version bumped to 1.1.

### 2026-04-25 11:37:39 — Agent — Resolve Issue 2 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Marked Issue 2 (`shadow`/`clip-bounds`/`clip-shape` missing from `<obj-attr>` EBNF) as RESOLVED. Issue summary table updated. File version bumped to 1.2.

### 2026-04-25 11:38:57 — Agent — Resolve Issue 3 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Marked Issue 3 (`shadow` incorrectly nested inside `<border-value>`) as RESOLVED. All High issues now resolved. Issue summary table updated. File version bumped to 1.3.

### 2026-04-25 11:40:06 — Agent — Resolve Issue 4 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Marked Issue 4 (`none` not in `<color>` EBNF) as RESOLVED. Issue summary table updated. File version bumped to 1.4.

### 2026-04-25 11:41:09 — Agent — Resolve Issue 5 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Marked Issue 5 (`output-format` default contradiction) as RESOLVED. All 5 issues resolved. Stats updated. File version bumped to 1.5.

### 2026-04-25 11:46:12 — Agent — Re-verify DSL grammar description v1.1
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Re-verified `2_Docs/DSL_grammar_description.md` v1.1. Found 3 new issues: Issue 6 (Medium — `transparent`/`none` semantics undocumented), Issue 7 (Medium — background EBNF parameter ordering), Issue 8 (Low — `output-format=images` file naming missing). Report bumped to v1.6.

### 2026-04-25 11:49:42 — Agent — Fix Issue 6: transparent/none semantics
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Section 15.1 expanded with explicit bullets distinguishing `none` (no-paint, fill/background-only) from `transparent` (general named color, any property). File version bumped to 1.2.

### 2026-04-25 11:49:42 — Agent — Resolve Issue 6 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Issue 6 marked as RESOLVED. Summary table, stats, and recommendation updated. File version bumped to 1.7.

### 2026-04-25 11:52:21 — Agent — Fix Issue 7: background EBNF parameter ordering
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: `<background-params>` rewritten to use `<named-param-list>`; three fixed-order sub-rules removed; comment block added for key-presence disambiguation. File version bumped to 1.3.

### 2026-04-25 11:52:21 — Agent — Resolve Issue 7 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Issue 7 marked as RESOLVED. All Medium issues now resolved. Stats updated. File version bumped to 1.8.

### 2026-04-25 11:54:44 — Agent — Fix Issue 8: output-format=images file naming
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: `<frame-id>.png`/`.jpeg` naming rule added to §6 `output-format` parameter description. File version bumped to 1.4.

### 2026-04-25 11:54:44 — Agent — Resolve Issue 8 in DSL grammar verification report
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Issue 8 marked as RESOLVED. §2 REQ-0029 updated to ✓. All 8 issues resolved. File version bumped to 1.9.

### 2026-04-25 12:01:19 — Agent — Fix DSL grammar Issues 9-12 (re-verification of v1.4)
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Issue 9 (High): added `<expr>`, `<expr-term>`, `<expr-factor>`, `<expr-point>` EBNF rules for arithmetic expressions in function bodies. Issue 10 (Medium): added trailing `<terminator>?` to `<image-def>` rule. Issue 11 (Low): updated `<frame>` and `<obj-template>` rules to use optional-terminator pattern for attributes. Issue 12 (Low): removed duplicate `image` from §2.8 keywords list. File version bumped to 1.5.

### 2026-04-25 12:01:19 — Agent — Re-verify DSL grammar description v1.4 (Issues 9-12)
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: Re-verified `2_Docs/DSL_grammar_description.md` v1.4. Found and resolved 4 new issues (Issues 9-12). §3 extended with 4 new issue blocks; §4 summary table updated (12 total, all resolved); §5 recommendation updated. Report bumped to v2.0.

### 2026-04-25 12:08:40 — Agent — Fix DSL grammar Issues 13-20 (re-verification of v1.5)
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Issues 13-14 (High): added `<string>` and `<line-type>` EBNF production rules. Issue 15: added `<number>` to EBNF block. Issue 16: removed redundant `<number>` from `<value>`. Issue 17: fixed `<number-0-1>` empty-match bug. Issue 18: added `{n}` to notation legend. Issue 19: corrected unquoted font-family in §5, §12.5, §17.3 examples. Issue 20: rewrote §4 forward-reference prose. File version bumped to 1.6.

### 2026-04-25 12:08:40 — Agent — Re-verify DSL grammar description v1.5 (Issues 13-20)
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: 8 new issues (13-20) found and all resolved. Summary table extended to 20 rows (6H/8M/6L all resolved). Report version bumped to 2.1.

### 2026-04-25 12:43:00 — Agent — Semantic correctness review of DSL grammar v1.6 (Issues 21-31)
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: 11 issues found and fixed: Issue 21 (High) — `translate` in transform order replaced with `position`; Issue 22 (High) — identifier-hyphen disambiguation rules added to §2.5 and §13.3; Issue 23 (Medium) — circular include detection added to §14 and §18.1; Issue 24 (Medium) — `<param-names>`/`<arg-list>` updated to allow zero items; Issue 25 (Medium) — `%` fallback to canvas dimensions documented; Issue 26 (Medium) — `none` on stroke corrected to “semantic error”; Issue 27 (Medium) — connector mutual-exclusivity rule and error table entry added; Issue 28 (Medium) — function argument count mismatch error table entry added; Issue 29 (Low) — `hold-time`/`dpi` type corrected to `number` with truncation note; Issue 30 (Low) — §12.4 coordinate scope reworded to cover all drawing commands; Issue 31 (Low) — `fill` on `line`/`path` added to §18.1 error table. File version bumped to 1.7.

### 2026-04-25 12:43:00 — Agent — Update verification report for semantic review (Issues 21-31)
- File: `3_Reports/verification_dsl_grammar_2026-04-25-102436.md`
- Action: Updated
- Details: 11 new issues (21-31) documented and all resolved. §1 scope updated; §3 extended with Issue 21-31 blocks; §4 summary table extended to 31 rows (8H/14M/9L all resolved); §5 recommendation updated. Report version bumped to 2.2.

### 2026-04-25 13:00:44 — Agent — Create completeness review of DSL grammar description
- File: `3_Reports/completeness_review_dsl_grammar_2026-04-25-130044.md`
- Action: Created
- Details: Completeness review of 2_Docs/DSL_grammar_description.md v1.7. Found 18 issues: 4 High (output file naming undefined, image keyword disambiguation missing, font alignment absent, multi-line text rendering undocumented), 6 Medium, 8 Low. Full prioritised action list included.

### 2026-04-25 13:05:18 — Agent — Fix H-01: output file naming in DSL grammar description
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added `### Output File Naming` subsection to §6. Documents naming rule per output-format value (png/jpeg/gif/images), script-name derivation, per-frame naming for images mode, duplicate frame-id overwrite warning, and explicit output-path override semantics. File version bumped to 1.8.

### 2026-04-25 13:06:57 — Agent — Fix H-02: image keyword disambiguation in DSL grammar description
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added disambiguation block to §2.8 explaining lookahead rule (image without `(` = canvas statement; image followed by `(` = drawing primitive). Added cross-reference notes to §6 and §11. File version bumped to 1.9.

