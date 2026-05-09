# Changelog 2026-04-27

### 2026-04-27 15:18:24 — Agent — Fix H-03: add align parameter to font primitive
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added `align` (left|center|right, default left) parameter to §10 font syntax block, parameter table, and pos description. Added two examples (center-aligned, right-aligned). Added align (font) row to §16.2 defaults table. File version bumped to 2.0.

### 2026-04-27 15:20:15 — Agent — Fix H-04: document multi-line text rendering in §10
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added Multi-line text rendering block to §10: pos anchors first-line baseline; line spacing = font-size × 1.2; align applies per-line; no line-count limit (clipped at canvas); no automatic word-wrap. Annotated existing multi-line example with baseline calculation. File version bumped to 2.1.

### 2026-04-27 15:24:01 — Agent — Fix M-05: state include top-level restriction in §14 prose
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added placement-restriction callout block to §14: `include` is top-level only; placing it inside begin_frame, begin_obj, or begin_func is a parse error. Added corresponding §18.1 error table entry. File version bumped to 2.2.

### 2026-04-27 15:25:05 — Agent — Fix M-06: define error for unrecognised parameter keys
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Added validation note to <named-param-list> EBNF rule in §3 stating unrecognised keys are a parse error. Added `Unrecognised parameter key` row to §18.1 parse-error table with message pattern. File version bumped to 2.3.

### 2026-04-27 15:26:59 — Agent — Fix M-07: describe step connector routing algorithm in §9.2
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Expanded §9.2 step connector description with H-V-H routing algorithm (horizontal leg to midpoint x, vertical leg, horizontal leg to destination). Updated curved description to name Catmull-Rom spline. Noted corner/corner-radius apply to all step turns. File version bumped to 2.4.

### 2026-04-27 15:28:20 — Agent — Fix M-08 / M-09 / M-10
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: M-08: added label-font-style and label-font-weight rows to §16.2 defaults table. M-09: added case-sensitivity callout block to §2.8. M-10: added Global Namespace subsection to §4 (shared namespace for frames/objects/functions, duplicate name = parse error, includes participate); added note to §13.1; added duplicate-name and case-incorrect-keyword entries to §18.1. File version bumped to 2.5.

### 2026-04-27 18:04:59 — Agent — Fix all 10 new completeness issues; DSL grammar → v2.7
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Bumped `File version` to 2.7. Fixed M-N1 (§7 duplicate background error), M-N2 (§15.1 GRAY colorspace CCIR 601 conversion), M-N3 (§15.3 em outside font resolves to 12px), L-N4 (§18.2 rotate/start-angle/end-angle normalisation), L-N5 (§8.0 negative scale validation error), L-N6 (§12.2 clip-shape fixed keywords clarification), L-N7 (§9.6 static pattern rendering note), L-N8 (§13.1 recursion not supported runtime error), L-N9 (§17.9 polygon+pie and §17.10 arc examples added), L-N10 (§14 frames in includes rewritten).

### 2026-04-27 18:04:59 — Agent — Completeness review report updated for v2.7 (all issues resolved)
- File: `3_Reports/completeness_review_dsl_grammar_2026-04-25-130044.md`
- Action: Updated
- Details: File version bumped to 1.4. Added Re-Review section with resolved status for all 10 new issues one by one. Updated section coverage (all 18 sections Complete). Updated overall assessment: 28/28 total issues resolved, 0 open.

### 2026-04-27 17:49:53 — Agent — Full re-verification of DSL Grammar v2.6
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: Corrected header version from 2.5 to 2.6 (administrative fix missed in previous session).

### 2026-04-27 17:49:53 — Agent — Completeness review report updated for v2.6 re-verification
- File: `3_Reports/completeness_review_dsl_grammar_2026-04-25-130044.md`
- Action: Updated
- Details: File version bumped to 1.3. Added Re-Review section with 10 new findings (3 Medium: M-N1 multiple background calls, M-N2 GRAY colorspace, M-N3 em outside font; 7 Low: L-N4 rotate range, L-N5 negative scale, L-N6 clip-shape type, L-N7 pattern static, L-N8 recursion, L-N9 missing polygon/pie/arc examples, L-N10 frames-in-includes wording). Updated section coverage and overall assessment.

### 2026-04-27 17:19:56 — Agent — Fix all 8 LOW issues in DSL grammar (L-11 through L-18)
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: L-11 §17.8 path example added; L-12 skew-x/skew-y direction stated; L-13 z-index clamping in §18.2; L-14 duplicate param key in §3 EBNF + §18.1; L-15 fill=none on arc clarified; L-16 div-by-zero note in §13.3; L-17 corner-radius note in §8.3; L-18 per-primitive opacity note in §8.0. File version bumped to 2.6.

### 2026-04-27 17:19:56 — Agent — Update completeness review report for v2.6
- File: `3_Reports/completeness_review_dsl_grammar_2026-04-25-130044.md`
- Action: Updated
- Details: File version bumped to 1.2. All 8 LOW issues marked Resolved. Section coverage table updated to all Complete. Overall assessment updated to 18/18 resolved, 0 remaining.

### 2026-04-27 16:54:45 — Agent — Re-review completeness for DSL Grammar v2.5
- File: `3_Reports/completeness_review_dsl_grammar_2026-04-25-130044.md`
- Action: Updated
- Details: File version bumped to 1.1. Added "Re-Review" section: all 4 HIGH and 6 MEDIUM issues confirmed resolved in v2.5; 8 LOW issues remain open (L-11 through L-18); no new issues found; updated section coverage table and overall assessment summary.

### 2026-04-27 18:23:57 — Agent — Gap analysis of DSL Grammar v2.7 (12 new gaps found)
- File: `3_Reports/gap_report_dsl_v27_2026-04-27-182357.md`
- Action: Created
- Details: Independent uncovered-requirement scan of v2.7. Found 12 gaps: 4 High (G-01 negative scale no §18 entry, G-02 missing message patterns in §18.2, G-03 jpeg+RGBA conflict, G-04 output-format conflict across frames, G-05 canvas initial state), 5 Medium (G-06 corner on curved connector, G-07 partial start/end connector error, G-08 5 missing defaults in §16.2, G-09 clip-bounds+clip-shape combined, G-10 frame-mode only in example notes), 3 Low (G-11 unary minus undocumented, G-12 CSS color level unspecified).

### 2026-04-27 18:29:06 — Agent — Fix all 12 gaps; DSL grammar → v2.8
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: File version bumped to 2.8. G-01 (§18.2 scale<0 row+message), G-02 (§18.2 radius/width/height message pattern), G-03 (§6 jpeg+RGBA validation error), G-04 (§6 output-format conflict rule), G-05 (§7 initial canvas state), G-06 (§9.4 corner ignored for curved), G-07 (§9.1+§18.1 partial start/end error), G-08 (§16.2 five missing defaults), G-09 (§12.2 clip intersection), G-10 (§5 frame-mode propagation note), G-11 (§13.3 unary minus restriction), G-12 (§3 CSS Color Level 3).

### 2026-04-27 18:29:06 — Agent — Gap report updated; all 12 gaps resolved
- File: `3_Reports/gap_report_dsl_v27_2026-04-27-182357.md`
- Action: Updated
- Details: File version bumped to 1.1. Added Resolution section marking all G-01–G-12 as Resolved against DSL v2.8. Added Changelog block.

### 2026-04-27 18:35:31 — Agent — Gap analysis of DSL Grammar v2.8 (11 new gaps found)
- File: `3_Reports/gap_report_dsl_v28_2026-04-27-183531.md`
- Action: Created
- Details: Independent uncovered-requirement scan of v2.8. Found 11 gaps: 2 High (V-01 colorspace
  conflict between frame-attr and image-param, V-02 missing required-parameter error in §18.1),
  5 Medium (V-03 curved connector with 2 points, V-04 arc start>=end sweep undefined, V-05
  RGB/RGBA out-of-range components, V-06 zero canvas dimension, V-07 scale=0 validity),
  4 Low (V-08 pattern-color missing from §16.2, V-09 3-digit hex not documented, V-10 gradient
  identical start/end, V-11 shadow offset direction convention).

### 2026-04-27 18:40:54 — Agent — Fix V-01 through V-11 in DSL Grammar → v2.9
- File: `2_Docs/DSL_grammar_description.md`
- Action: Updated
- Details: File version bumped to 2.9. Applied all 11 fixes: V-01 colorspace conflict precedence (§5), V-02 required-parameter error row (§18.1), V-03 curved/2-points note (§9.2), V-04 arc sweep direction (§8.6, §8.7), V-05 RGB/RGBA out-of-range errors (§18.2), V-06 zero canvas dimension error (§18.2), V-07 scale=0 validity (§8.0), V-08 pattern-color default (§16.2), V-09 #RGB not supported note (§15.1), V-10 gradient identical start/end fallback (§7.2), V-11 shadow offset direction (§12.2).

### 2026-04-27 18:40:54 — Agent — Gap report v2.8 updated → v1.1 (all resolved)
- File: `3_Reports/gap_report_dsl_v28_2026-04-27-183531.md`
- Action: Updated
- Details: File version bumped to 1.1. Added Resolution section marking all V-01–V-11 as Resolved against DSL v2.9. Added Changelog block.

### 2026-04-27 18:53:13 — Agent — Gap analysis of DSL Grammar v2.9 (11 new gaps found)
- File: `3_Reports/gap_report_dsl_v29_2026-04-27-185313.md`
- Action: Created
- Details: Independent uncovered-requirement scan of v2.9. Found 11 gaps: 2 High (W-01 `#` token
  disambiguation hex-vs-comment undocumented, W-02 no §18.1 error for frame missing `image`
  statement), 5 Medium (W-03 dpi≤0 division-by-zero, W-04 opacity out-of-range, W-05 GRAY
  colorspace file extension in images mode, W-06 clip-shape=polygon geometry undefined, W-07
  background() invalid parameter combinations), 4 Low (W-08 start-cap/start-arrow alias
  conflict, W-09 % on scalar lengths, W-10 hold-time<1, W-11 unit suffix on angle values).
