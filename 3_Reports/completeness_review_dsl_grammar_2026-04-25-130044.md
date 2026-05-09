# Completeness Review — DSL Grammar Description

| Field | Value |
|---|---|
| **Description** | Completeness review of 2_Docs/DSL_grammar_description.md (v1.7 → v2.6) |
| **Created at** | 2026-04-25 13:00:44 |
| **File version** | 1.4 |
| **Created by** | Claude Sonnet 4.6 |

---

## Subject File

`2_Docs/DSL_grammar_description.md` — version **1.7** (initial review) → **2.5** (re-review 2026-04-27) → **2.6** (all LOW issues fixed 2026-04-27) → **2.6** re-verified 2026-04-27 → **2.7** (all 10 new issues fixed 2026-04-27)

---

## Review Scope

This review checks whether the DSL grammar description document is **complete** — meaning every feature implied by the grammar, the data types, and the runtime behaviour is sufficiently documented and internally consistent. It does **not** re-run the earlier semantic correctness checks (those were addressed in v1.1–v1.7).

---

## Executive Summary

The document is well-structured with 18 sections, a formal EBNF grammar, per-primitive parameter tables, a defaults summary, a capability matrix, and annotated examples. Most areas are solid. However, **4 high-priority gaps** were identified — most notably the complete absence of **output file naming** semantics and a missing **text alignment** parameter for the `font` primitive. There are also **6 medium** and **8 low** findings for a total of **18 issues**.

| Severity | Count |
|---|---|
| High | 4 |
| Medium | 6 |
| Low | 8 |
| **Total** | **18** |

---

## Findings

### HIGH — H-01: Output file naming convention is undefined

**Location:** §1 Overview, §5 Frame Definition, §6 Image Canvas Statement  
**Description:** The document never states what the output file(s) are named. There is no explanation of whether the output filename is derived from the script filename, the frame ID, or configured elsewhere. The `output-format=images` variant references `<frame-id>.png` / `<frame-id>.jpeg` naming, but the default (single-file) naming is completely absent.  
**Impact:** Implementors and users cannot predict output artefacts without additional out-of-band knowledge.  
**Suggested fix:** Add a subsection to §6 (or §1) defining the output file naming rule for each `output-format` value.

---

### HIGH — H-02: `image` keyword dual-use disambiguation missing

**Location:** §6 Image Canvas Statement, §11 Image Primitive, §2.8 Keywords  
**Description:** The keyword `image` serves two entirely different purposes: (a) the `image` canvas-definition statement (`image width=... height=...`, no parentheses) and (b) the `image(src=...)` drawing primitive (parenthesised named-param call). The document treats these in separate sections but never explicitly calls out the disambiguation rule (presence or absence of `(` after the token).  
**Impact:** Without a clear disambiguation statement, implementors of a parser may incorrectly handle the ambiguity.  
**Suggested fix:** Add a note in §6 and/or §11 — or a dedicated sub-section in §2 or §3 — explaining that the parser distinguishes both uses by the presence of `(` immediately following the `image` token.

---

### HIGH — H-03: `font` primitive has no text-alignment parameter

**Location:** §10 Font / Text Primitive  
**Description:** The `font` primitive positions text at a "baseline left anchor" (`pos`). There is no `align` or `text-align` parameter (e.g., `left`, `center`, `right`). For any non-trivial layout (centred labels, right-aligned numbers), the caller must manually compute the x offset, which requires knowing the rendered text width — information the script author does not have at authoring time.  
**Impact:** Major usability gap for text layout; examples §17.3 and §17.4 work around it by manually computing positions, which is error-prone.  
**Suggested fix:** Document an `align` parameter (`left` | `center` | `right`, default `left`) with a note on the anchor point used for each mode, or explicitly state that text alignment is not supported and justify the decision.

---

### HIGH — H-04: Multi-line text rendering behaviour not documented

**Location:** §10 Font / Text Primitive, §2.6 String Literals  
**Description:** §2.6 states that `\n` is a supported escape sequence in strings. The `font` primitive accepts `text` as a string, so multi-line text is syntactically valid. However, §10 contains no description of how newlines are rendered: line height, leading, vertical offset from `pos`, or whether each line uses the same baseline anchor.  
**Impact:** Authors cannot reliably use multi-line text without knowing line-height/spacing behaviour.  
**Suggested fix:** Add a paragraph to §10 describing multi-line rendering: line spacing formula (e.g., 120% of `font-size`), how `pos` anchors the first line's baseline, and any limits on line count.

---

### MEDIUM — M-05: `include` placement restriction not stated in prose

**Location:** §14 Include Statement, §3 Formal Grammar  
**Description:** The EBNF grammar unambiguously restricts `<include-stmt>` to `<top-level-stmt>` only, but §14 never explicitly states in prose that `include` may **not** appear inside `begin_frame`, `begin_obj`, or `begin_func` bodies. A reader scanning §14 without reading the EBNF would not know this restriction exists.  
**Impact:** Confusing for authors who naturally expect `include` to work anywhere.  
**Suggested fix:** Add one sentence to §14: *"`include` directives may only appear at the top level of a script; they are not permitted inside `begin_frame`, `begin_obj`, or `begin_func` bodies."*

---

### MEDIUM — M-06: Unrecognised parameter name has no defined error

**Location:** §18.1 Parse Errors  
**Description:** The error table covers unrecognised color formats, insufficient points, fill-on-arc, and similar type-level errors, but there is no entry for an **unknown/unrecognised parameter key** (e.g., `circle(color=black, bogus=5, ...)`). It is not stated whether this is silently ignored or halts execution.  
**Impact:** Ambiguous engine behaviour; typos in parameter names could silently produce wrong output.  
**Suggested fix:** Add an entry to §18.1: unknown named parameter → parse error (or validation warning, if silently ignored — but document the chosen behaviour).

---

### MEDIUM — M-07: `connector-type=step` routing algorithm not described

**Location:** §9.2 Connector Type  
**Description:** `straight` and `curved` semantics are adequately described, but `step` is only characterised as "axis-aligned right-angle routing". There is no description of the algorithm used to produce the steps (e.g., horizontal-first, vertical-first, midpoint split), which affects how multi-segment connectors route between points.  
**Impact:** Authors cannot predict the visual output of step connectors with multi-point paths.  
**Suggested fix:** Add a sentence or diagram note describing the step-routing heuristic (e.g., "each segment pair is joined with a horizontal then vertical leg at the midpoint").

---

### MEDIUM — M-08: `label-font-style` and `label-font-weight` defaults missing from §16.2

**Location:** §16.2 Default Values Summary  
**Description:** The connector's `label-font-style` and `label-font-weight` parameters (defined in §9.5) have defaults `normal` and `normal` respectively, but these are not listed in the §16.2 default values table.  
**Impact:** Incomplete reference table; authors must cross-reference §9.5 to find these defaults.  
**Suggested fix:** Add rows for `label-font-style` (`normal`) and `label-font-weight` (`normal`) to Table 16.2.

---

### MEDIUM — M-09: Case sensitivity of keywords not stated

**Location:** §2.8 Keywords, §2.5 Identifiers  
**Description:** The document never states whether DSL keywords and named-color tokens are case-sensitive. For example, is `BEGIN_FRAME` equivalent to `begin_frame`? Is `Black` equivalent to `black`? The EBNF uses lowercase literals, but this is not declared as a rule.  
**Impact:** Parser implementors may make inconsistent choices; authors may receive confusing errors.  
**Suggested fix:** Add a sentence to §2.8 (or §2.5): *"All keywords are case-sensitive and must be written in lowercase. Named color tokens are also case-sensitive."*

---

### MEDIUM — M-10: Scope rules for functions and objects not defined

**Location:** §13.1 Function Declaration, §12.1 Template Declaration  
**Description:** It is not stated whether function names and object template names share the same namespace, or whether a name collision (same identifier for both a function and an object) is an error. The grammar allows both as top-level statements but does not address naming conflicts.  
**Impact:** Ambiguous behaviour when a function and an object share a name; a call `foo(pos=(0,0))` could be interpreted as either.  
**Suggested fix:** Add a note to §13.1 or §4: *"Function names, object template names, and frame names all share a single global namespace. Defining two top-level entities with the same name is a parse error."*

---

### LOW — L-11: No example for the `path` primitive

**Location:** §17 Complete Annotated Examples  
**Description:** All seven examples in §17 use `line`, `circle`, `square`, `connector`, `font`, and `image`, but none demonstrates the `path` primitive — even though it is the only open-polyline stroke primitive.  
**Impact:** Minor; authors must rely solely on the §8.5 description without a full-frame usage example.  
**Suggested fix:** Either add an example (§17.8) or add a `path` call to one of the existing examples.

---

### LOW — L-12: `skew-x` / `skew-y` direction not defined

**Location:** §8.0 Shared Transform Parameters  
**Description:** The `rotate` parameter is documented as "clockwise rotation". The `skew-x` and `skew-y` parameters are described only as "horizontal/vertical skew angle" with no indication of the positive direction of skew (clockwise, counterclockwise, rightward, leftward).  
**Impact:** Ambiguous output for non-zero skew values.  
**Suggested fix:** Add a brief direction note: e.g., *"Positive `skew-x` shears the element to the right; positive `skew-y` shears the element downward."*

---

### LOW — L-13: `z-index` out-of-range behaviour not defined

**Location:** §8.0 Shared Transform Parameters, §18.2 Validation Warnings/Errors  
**Description:** `z-index` is documented as accepting integers 0–1000. §18.2 does not include any entry for values outside this range (negative or > 1000).  
**Impact:** Undefined engine behaviour for out-of-range z-index values.  
**Suggested fix:** Add an entry to §18.2: *"`z-index` outside 0–1000 → value clamped to the nearest bound"* (or error, whichever is intended).

---

### LOW — L-14: Duplicate parameter names in a primitive call not addressed

**Location:** §3 Formal Grammar, §18 Error Reference  
**Description:** The grammar for `<named-param-list>` does not prohibit duplicate keys (e.g., `circle(color=black, color=red, ...)`). No error entry covers this case.  
**Impact:** Ambiguous behaviour — last-wins, first-wins, or error?  
**Suggested fix:** Add one sentence to §3 or §18.1 defining the behaviour for duplicate keys (recommended: parse error).

---

### LOW — L-15: `fill=none` on `arc` vs. unspecified `fill` on `arc`

**Location:** §8.7 `arc`, §18.1 Parse Errors  
**Description:** §18.1 states "`fill` specified on `arc` is a parse error". It is ambiguous whether `fill=none` (semantically a no-op) is also an error, or only non-`none` fill values.  
**Impact:** Minor inconsistency that could cause confusion when authors write `arc(..., fill=none)` defensively.  
**Suggested fix:** Clarify: *"Any `fill` parameter on `arc` — including `fill=none` — is a parse error."* (or define `fill=none` as silently accepted.)

---

### LOW — L-16: Division by zero in arithmetic expressions not documented

**Location:** §13.3 Arithmetic Expressions  
**Description:** The four arithmetic operators (`+`, `-`, `*`, `/`) are listed but there is no statement about what happens when a division-by-zero occurs at call time.  
**Impact:** Undefined runtime behaviour.  
**Suggested fix:** Add one sentence: *"Division by zero causes a runtime error that halts execution with an appropriate message."*

---

### LOW — L-17: `corner-radius` for `square` (rounded rectangles) not mentioned

**Location:** §8.3 `square` (Rectangle)  
**Description:** The `square` primitive has no `corner-radius` parameter listed. It is unclear whether rounded rectangles are unsupported or simply omitted.  
**Impact:** Minor feature completeness question.  
**Suggested fix:** Either add `corner-radius` to §8.3 (if supported), or add an explicit note: *"Rounded corners are not supported for the `square` primitive."*

---

### LOW — L-18: Per-primitive opacity not documented

**Location:** §8 Drawing Primitives  
**Description:** The `image` primitive (§11) and `background(src=...)` (§7.3) both support an `opacity` parameter. However, the standard drawing primitives (`line`, `circle`, `square`, `polygon`, `path`, `pie`, `arc`) have no `opacity` parameter in their definitions. It is not stated whether per-primitive opacity is intentionally unsupported or accidentally omitted.  
**Impact:** Authors expecting to layer semi-transparent shapes will find no documented mechanism.  
**Suggested fix:** Either add `opacity` to §8.0 Shared Transform Parameters (if supported), or add an explicit statement: *"Per-primitive stroke/fill opacity is not supported; use `RGBA(r,g,b,a)` color values to achieve transparency."*

---

## Section Coverage Summary

| Section | Status | Notes |
|---|---|---|
| §1 Overview | Partial | Output file naming absent (H-01) |
| §2 Lexical Conventions | Partial | Case sensitivity not stated (M-09) |
| §3 Formal Grammar (EBNF) | Partial | Duplicate key rule absent (L-14) |
| §4 Top-Level Structure | Partial | Namespace collision not covered (M-10) |
| §5 Frame Definition | Complete | — |
| §6 Image Canvas Statement | Partial | Output file naming absent (H-01); `image` disambiguation absent (H-02) |
| §7 Background Statement | Complete | — |
| §8 Drawing Primitives | Partial | Skew direction (L-12), opacity (L-18), rounded square (L-17) |
| §9 Connector | Partial | Step routing algorithm (M-07) |
| §10 Font / Text | Partial | No alignment param (H-03), multi-line rendering (H-04) |
| §11 Image Primitive | Partial | `image` disambiguation absent (H-02) |
| §12 Object Templates | Complete | — |
| §13 Function Declarations | Partial | Division by zero (L-16), scope/namespace (M-10) |
| §14 Include Statement | Partial | Top-level restriction not in prose (M-05) |
| §15 Data Types | Complete | — |
| §16 Parameter Reference | Partial | Missing connector label defaults (M-08), z-index range (L-13) |
| §17 Examples | Partial | No `path` example (L-11) |
| §18 Error Reference | Partial | Unknown param key (M-06), fill=none on arc (L-15), div-by-zero (L-16), z-index range (L-13), duplicate keys (L-14) |

---

## Prioritised Action List

| # | ID | Severity | Section(s) | Action |
|---|---|---|---|---|
| 1 | H-01 | High | §1, §6 | Define output file naming convention for all `output-format` values |
| 2 | H-02 | High | §6, §11 | Add `image` keyword disambiguation note (with vs. without `(`) |
| 3 | H-03 | High | §10 | Add `align` parameter to `font` or document its absence with justification |
| 4 | H-04 | High | §10 | Document multi-line text rendering: line height, spacing, baseline anchor |
| 5 | M-05 | Medium | §14 | State explicitly that `include` is top-level only |
| 6 | M-06 | Medium | §18.1 | Define error behaviour for unrecognised parameter keys |
| 7 | M-07 | Medium | §9.2 | Describe `step` connector routing algorithm |
| 8 | M-08 | Medium | §16.2 | Add `label-font-style` and `label-font-weight` to defaults table |
| 9 | M-09 | Medium | §2.8 | State that keywords and color names are case-sensitive lowercase |
| 10 | M-10 | Medium | §4, §13.1 | Define namespace rules; document that name collisions are parse errors |
| 11 | L-11 | Low | §17 | Add a `path` primitive usage example |
| 12 | L-12 | Low | §8.0 | Clarify positive direction of `skew-x` / `skew-y` |
| 13 | L-13 | Low | §8.0, §18.2 | Document `z-index` out-of-range clamping or error behaviour |
| 14 | L-14 | Low | §3, §18.1 | Define duplicate named-parameter key behaviour |
| 15 | L-15 | Low | §8.7, §18.1 | Clarify whether `fill=none` on `arc` is an error or silently accepted |
| 16 | L-16 | Low | §13.3 | Define division-by-zero runtime behaviour |
| 17 | L-17 | Low | §8.3 | Clarify whether `corner-radius` is supported on `square` |
| 18 | L-18 | Low | §8, §8.0 | Clarify per-primitive opacity: add to shared params or explicitly exclude |

---

## Re-Review — 2026-04-27 16:54:45 (DSL Grammar v2.5)

The DSL grammar description has been updated from v1.7 to v2.5, incorporating fixes for all HIGH and MEDIUM findings from this report. This section documents the updated status of every finding.

### Issue Status

| ID | Severity | Status | Resolution |
|---|---|---|---|
| H-01 | High | **Resolved** | §6 now has a dedicated "Output File Naming" subsection covering all four `output-format` values, `<script-name>` derivation, per-frame naming for `images` mode, duplicate frame-id warning, and output-path override semantics. |
| H-02 | High | **Resolved** | §2.8 has a disambiguation block; §6 and §11 each carry a cross-reference note. The first-lookahead rule (`(` present/absent) is stated clearly. |
| H-03 | High | **Resolved** | `align` (`left` \| `center` \| `right`, default `left`) added to the `font` primitive syntax block, parameter table, and §16.2 defaults table; two usage examples added. |
| H-04 | High | **Resolved** | §10 has a "Multi-line text rendering" block: `pos` anchors the first-line baseline; spacing = `font-size × 1.2`; `align` applies per-line; no line limit; no automatic word-wrap. |
| M-05 | Medium | **Resolved** | §14 has a placement-restriction callout stating that `include` is top-level only; placing it inside any block is a parse error. Entry also added to §18.1. |
| M-06 | Medium | **Resolved** | §18.1 now includes an "Unrecognised parameter key" row with its message pattern; commentary added to §3 EBNF. |
| M-07 | Medium | **Resolved** | §9.2 has a full algorithm description: H-V-H routing between each pair of vertices via the midpoint x-coordinate; `corner`/`corner-radius` applies to every right-angle turn. |
| M-08 | Medium | **Resolved** | `label-font-style` (`normal`) and `label-font-weight` (`normal`) rows added to §16.2. |
| M-09 | Medium | **Resolved** | §2.8 has a "Case sensitivity" callout: all keywords and named color tokens are case-sensitive lowercase; user-defined identifiers are also case-sensitive. |
| M-10 | Medium | **Resolved** | §4 has a "Global Namespace" subsection stating that frame names, object names, and function names share one namespace; duplicate name is a parse error; includes participate in the same namespace. §13.1 has a corresponding note. |
| L-11 | Low | **Resolved** | Added §17.8 with a full annotated `path` example: open zigzag polyline and a dashed path; notes state path is open, min 2 points, and fill is unsupported. |
| L-12 | Low | **Resolved** | §8.0 `skew-x` and `skew-y` descriptions updated: positive `skew-x` shears right; positive `skew-y` shears downward. |
| L-13 | Low | **Resolved** | §18.2 has new row: `z-index` outside 0–1000 is clamped to the nearest bound with a warning message. |
| L-14 | Low | **Resolved** | Duplicate-key constraint added to `<named-param-list>` EBNF comment in §3; new error row added to §18.1 with message pattern. |
| L-15 | Low | **Resolved** | §8.7 text and §18.1 entry both clarified: `fill` on `arc` is a parse error for **any** value including `fill=none`. |
| L-16 | Low | **Resolved** | §13.3 has a new note: division by zero halts execution with `<file>:<line>: error: division by zero in expression`. |
| L-17 | Low | **Resolved** | §8.3 has a new note: `corner-radius` is not supported on `square`; all corners are sharp right angles. |
| L-18 | Low | **Resolved** | §8.0 has a new per-primitive opacity note: no `opacity` transform param; use `RGBA()` color values; `opacity` is image/background-only. |

### New Issues Found

No new completeness gaps were identified in the content added by v1.8–v2.6.

### Updated Section Coverage

| Section | Status | Notes |
|---|---|---|
| §1 Overview | **Complete** | — |
| §2 Lexical Conventions | **Complete** | — |
| §3 Formal Grammar (EBNF) | **Complete** | — |
| §4 Top-Level Structure | **Complete** | — |
| §5 Frame Definition | **Complete** | — |
| §6 Image Canvas Statement | **Complete** | — |
| §7 Background Statement | **Complete** | — |
| §8 Drawing Primitives | **Complete** | — |
| §9 Connector | **Complete** | — |
| §10 Font / Text | **Complete** | — |
| §11 Image Primitive | **Complete** | — |
| §12 Object Templates | **Complete** | — |
| §13 Function Declarations | **Complete** | — |
| §14 Include Statement | **Complete** | — |
| §15 Data Types | **Complete** | — |
| §16 Parameter Reference | **Complete** | — |
| §17 Examples | **Complete** | — |
| §18 Error Reference | **Complete** | — |

### Overall Assessment

All **18 issues** identified in the original v1.7 review have been resolved. All 18 sections are now marked **Complete**. The document is ready for implementation use.

| Severity | Original | Resolved | Remaining |
|---|---|---|---|
| High | 4 | 4 | 0 |
| Medium | 6 | 6 | 0 |
| Low | 8 | 8 | 0 |
| **Total** | **18** | **18** | **0** |

---

## Changelog

### 2026-04-27 18:04:59 — Fix all 10 new issues (M-N1 through L-N10); DSL grammar → v2.7
- Updated `File version` to `1.4`; updated `Subject File` line to include v2.7.
- Added "Re-Review — 2026-04-27 18:04:59" section with resolved status for all 10 new issues.
- M-N1 **Resolved**: §7 single-background-per-frame constraint added.
- M-N2 **Resolved**: §15.1 GRAY colorspace CCIR 601 conversion note added.
- M-N3 **Resolved**: §15.3 `em`-outside-font-context note added (resolves to 12px).
- L-N4 **Resolved**: §18.2 angle normalisation row expanded to name `rotate`, `start-angle`, `end-angle`.
- L-N5 **Resolved**: §8.0 `scale` row updated — negative values are a validation error.
- L-N6 **Resolved**: §12.2 `clip-shape` row clarified — fixed keywords only, not template names.
- L-N7 **Resolved**: §9.6 static-pattern-rendering note added.
- L-N8 **Resolved**: §13.1 recursion policy added — recursion not supported, runtime error.
- L-N9 **Resolved**: §17.9 (polygon + pie) and §17.10 (arc) examples added.
- L-N10 **Resolved**: §14 frames-in-includes sentence rewritten — frames ignored, only obj/func imported.
- Updated section coverage table — all 18 sections now **Complete**.
- Updated overall assessment — 28/28 total issues resolved, 0 open.

### 2026-04-27 17:49:53 — Full re-verification of DSL Grammar v2.6; 10 new issues found
- Updated `File version` to `1.3`; updated `Description` and `Subject File` line to reflect v2.6 re-verification.
- Corrected DSL grammar document header version from 2.5 to 2.6 (administrative fix).
- Added "Re-Review — 2026-04-27 17:49:53" section with 10 new findings: M-N1 (multiple background calls), M-N2 (GRAY colorspace), M-N3 (em outside font), L-N4 (rotate range), L-N5 (negative scale), L-N6 (clip-shape type), L-N7 (pattern static), L-N8 (recursion), L-N9 (missing polygon/pie/arc examples), L-N10 (frames-in-includes wording).
- Added new section coverage table and updated overall assessment (0 open → 10 open).

### 2026-04-27 17:19:56 — Fix all 8 remaining LOW issues (L-11 through L-18)
- Updated `File version` to `1.2`; updated `Description` to reflect version range → v2.6.
- Updated Subject File line to include v2.6.
- L-11 **Resolved**: §17.8 `path` example added.
- L-12 **Resolved**: §8.0 `skew-x`/`skew-y` positive direction documented.
- L-13 **Resolved**: §18.2 `z-index` out-of-range clamping + warning documented.
- L-14 **Resolved**: §3 EBNF duplicate-key constraint added; §18.1 error row added.
- L-15 **Resolved**: §8.7 and §18.1 clarified that `fill=none` on `arc` is also a parse error.
- L-16 **Resolved**: §13.3 division-by-zero runtime error note added.
- L-17 **Resolved**: §8.3 note added that `corner-radius` is not supported on `square`.
- L-18 **Resolved**: §8.0 per-primitive opacity note added; directs authors to `RGBA()` color values.
- Updated all L-11..L-18 rows to **Resolved** in the Issue Status table.
- Updated Section Coverage table — all 18 sections now **Complete**.
- Updated Overall Assessment summary — all 18 issues resolved, 0 remaining.

### 2026-04-27 16:54:45 — Re-review for DSL Grammar v2.5
- Updated `File version` to `1.1`; updated `Description` to reflect version range v1.7→v2.5.
- Added "Re-Review" section documenting status of all 18 original findings.
- All 4 HIGH and 6 MEDIUM issues confirmed resolved; 8 LOW issues remain open.
- Updated Section Coverage table to reflect current state.
- No new issues found in v1.8–v2.5 additions.

---

## Re-Review — 2026-04-27 17:49:53 (DSL Grammar v2.6)

A full re-read of v2.6 was performed to identify any remaining or new completeness gaps after all 18 prior issues were resolved.

**Administrative correction:** The document header in v2.6 still showed `File version: 2.5`; this was corrected to `2.6`.

### New Findings Summary

| Severity | Count |
|---|---|
| Medium | 3 |
| Low | 7 |
| **Total** | **10** |

### Findings

#### MEDIUM — M-N1: Multiple `background()` calls in one frame — behavior undefined

**Location:** §7 Background Statement  
**Description:** The document does not state what happens when `background()` is called more than once within the same frame. It is not defined whether the last call wins (overwrites), the first call wins, or whether multiple calls are a parse/validation error.  
**Impact:** Authors may produce unexpected output when compositing backgrounds, especially when mixing solid and image backgrounds.  
**Suggested fix:** Add a note to §7: *"A frame may contain at most one `background` call; specifying more than one is a validation error — `<file>:<line>: error: duplicate background statement`."* (or document last-wins semantics if that is the intended behavior.)

---

#### MEDIUM — M-N2: `colorspace=GRAY` — greyscale conversion not documented

**Location:** §5 Frame Definition, §6 Image Canvas Statement, §7 Background Statement  
**Description:** `colorspace=GRAY` is a valid value in the EBNF and in the parameter tables (§5, §6), but nowhere in the document is it explained how colors are converted to greyscale — whether it uses luminance weighting (`0.299R + 0.587G + 0.114B`), simple averaging, or another method. RGB, RGBA, and named colors are all valid color inputs, yet the conversion rules are completely absent.  
**Impact:** Implementors cannot produce consistent greyscale output without this specification.  
**Suggested fix:** Add a paragraph to §6 (or §15.1) describing greyscale conversion: e.g., *"When `colorspace=GRAY`, all color values are converted to single-channel luminance using standard CCIR 601 weighting: `Y = 0.299×R + 0.587×G + 0.114×B`."*

---

#### MEDIUM — M-N3: `em` unit outside font primitive context — "current font-size" undefined

**Location:** §15.3 Unit Measurements, §8 Drawing Primitives  
**Description:** §15.3 defines `em` as "1em = current font-size px", but the "current font-size" is only meaningful inside a `font` primitive. When `em` is used in other primitives (e.g., `line-width=1em`, `radius=2em`), there is no defined concept of "current font-size". It is not stated whether `em` resolves to the default font size (`12px`), the most recently declared font size in the same frame, or is a validation error outside font contexts.  
**Impact:** Ambiguous unit resolution for non-font primitives.  
**Suggested fix:** Add a note to §15.3: *"When `em` is used outside a `font` primitive, it resolves to the default font size of `12px`."* (or define it as a validation error.)

---

#### LOW — L-N4: `rotate` out-of-range behavior not explicitly attributed

**Location:** §8.0 Shared Transform Parameters, §18.2 Validation Warnings / Errors  
**Description:** §8.0 defines `rotate` as "degrees (0–360)". §18.2 has the entry "Angle outside 0–360 → Normalised modulo 360". However, it is not clear whether this §18.2 rule covers the `rotate` transform parameter or only the arc/pie `start-angle`/`end-angle` parameters. The §18.2 row uses the generic word "Angle" with no explicit reference.  
**Impact:** An implementor might apply normalisation only to arc/pie angles, not to `rotate`.  
**Suggested fix:** Expand the §18.2 row to: *"Angle parameter (`rotate`, `start-angle`, `end-angle`) outside 0–360 → normalised modulo 360."*

---

#### LOW — L-N5: Negative `scale` value (mirroring) behavior not documented

**Location:** §8.0 Shared Transform Parameters  
**Description:** The `scale` parameter is described as "Uniform scale multiplier (`0.5` = half, `2.0` = double)" with no mention of negative values. A negative scale would produce a mirror reflection in standard 2D transform semantics, but this behavior is not stated or prohibited.  
**Impact:** Authors cannot predict whether `scale=-1` mirrors the element or causes an error.  
**Suggested fix:** Add a sentence: *"Negative scale values are not supported and result in a validation error."* (or document mirroring behavior if it is intended.)

---

#### LOW — L-N6: `clip-shape` valid values — keywords vs. user identifiers not clarified

**Location:** §12.2 Object Attributes  
**Description:** The `clip-shape` attribute is described as accepting "shape name" with the examples `circle`, `square`, `polygon`. It is not stated whether these are fixed DSL keywords or user-defined object template names. If they are keywords, any object of that geometry type would clip; if they are identifiers, an author could pass the name of a `begin_obj` template.  
**Impact:** Authors cannot reliably use `clip-shape` without knowing whether to pass a keyword or a template name.  
**Suggested fix:** Clarify: *"`clip-shape` accepts one of the fixed shape keywords `circle`, `square`, or `polygon`; these refer to the built-in geometry, not to user-defined object templates."*

---

#### LOW — L-N7: `pattern` parameters on a non-animated connector — static rendering not defined

**Location:** §9.6 Animation and Pattern  
**Description:** The `pattern` parameter description says "Repeating pattern unit replacing the plain stroke." The `animated` description says "When `true`, pattern advances per frame." It is not stated what happens when `pattern` is specified but `animated=false` (the default): does the pattern render statically as a styled stroke, or are the pattern parameters silently ignored?  
**Impact:** Authors cannot predict whether they can use `pattern=dot` to produce a static dot-stroke connector.  
**Suggested fix:** Add a clarifying sentence: *"When `animated=false`, the pattern is rendered statically as a repeating stroke style (the pattern does not advance between frames)."*

---

#### LOW — L-N8: Function recursion — allowed or error not documented

**Location:** §13.1 Function Declaration  
**Description:** The document does not state whether a function may call itself recursively (directly or indirectly). In many scripting DSLs, recursion is prohibited to guarantee termination; in others it is allowed with a depth limit. The current documentation is silent on this behavior.  
**Impact:** Undefined behavior for recursive function calls; implementors may handle this inconsistently.  
**Suggested fix:** Add one sentence: *"Recursive function calls — direct or indirect — are not supported. A function call that would result in re-entering the same function halts execution with: `<file>:<line>: error: recursive call to function '<name>' is not permitted`."*

---

#### LOW — L-N9: §17 Examples do not cover `polygon`, `pie`, or `arc` primitives

**Location:** §17 Complete Annotated Examples  
**Description:** The eight examples in §17 use `line`, `circle`, `square`, `path`, `connector`, `font`, and `image`, but none demonstrates the `polygon`, `pie`, or `arc` primitives. These three primitives — particularly `pie` (with its angle semantics) and `polygon` (with its point-list syntax) — have unique parameter patterns that benefit from a concrete example.  
**Impact:** Minor; authors must rely solely on the §8.4/§8.6/§8.7 descriptions without a full-frame usage example.  
**Suggested fix:** Add examples §17.9 (polygon and pie) and §17.10 (arc) or add calls to these primitives within an existing example.

---

#### LOW — L-N10: "Available for reference" for frames in included files is misleading

**Location:** §14 Include Statement  
**Description:** §14 states: "Frame definitions in included files are **not** executed (they are available for reference but do not produce output unless the top-level script directly references them)." The phrase "available for reference" is unclear — frames cannot be called like functions or instantiated like objects. There is no mechanism in the language to "reference" a frame from another frame, making this phrasing confusing.  
**Impact:** Authors may believe they can reference or invoke frames from included files, which is not supported.  
**Suggested fix:** Rewrite as: *"Frame definitions in included files are **ignored**; they do not produce any output. Only `begin_obj` and `begin_func` definitions are imported by `include`."*

---

### Section Coverage (v2.6)

| Section | Status | Notes |
|---|---|---|
| §1 Overview | **Complete** | — |
| §2 Lexical Conventions | **Complete** | — |
| §3 Formal Grammar (EBNF) | **Complete** | — |
| §4 Top-Level Structure | **Complete** | — |
| §5 Frame Definition | Partial | GRAY colorspace conversion absent (M-N2) |
| §6 Image Canvas Statement | Partial | GRAY colorspace conversion absent (M-N2) |
| §7 Background Statement | Partial | Multiple `background()` calls undefined (M-N1) |
| §8 Drawing Primitives | Partial | Negative scale (L-N5); rotate range attribution (L-N4) |
| §9 Connector | Partial | Pattern static rendering (L-N7) |
| §10 Font / Text | **Complete** | — |
| §11 Image Primitive | **Complete** | — |
| §12 Object Templates | Partial | `clip-shape` value type (L-N6) |
| §13 Function Declarations | Partial | Recursion (L-N8) |
| §14 Include Statement | Partial | Frames-in-includes wording (L-N10) |
| §15 Data Types | Partial | `em` outside font context (M-N3) |
| §16 Parameter Reference | **Complete** | — |
| §17 Examples | Partial | No `polygon`, `pie`, or `arc` examples (L-N9) |
| §18 Error Reference | **Complete** | — |

### New Issues Action List

| # | ID | Severity | Section(s) | Action |
|---|---|---|---|---|
| 1 | M-N1 | Medium | §7 | Define behavior for multiple `background()` calls in one frame |
| 2 | M-N2 | Medium | §6, §15.1 | Document greyscale conversion formula for `colorspace=GRAY` |
| 3 | M-N3 | Medium | §15.3 | Define `em` unit resolution outside `font` primitive context |
| 4 | L-N4 | Low | §8.0, §18.2 | Explicitly attribute §18.2 angle normalisation rule to `rotate` parameter |
| 5 | L-N5 | Low | §8.0 | Document negative `scale` behavior (error or mirroring) |
| 6 | L-N6 | Low | §12.2 | Clarify whether `clip-shape` accepts keywords or user template names |
| 7 | L-N7 | Low | §9.6 | State whether `pattern` renders statically when `animated=false` |
| 8 | L-N8 | Low | §13.1 | Document recursion policy (allowed or error) |
| 9 | L-N9 | Low | §17 | Add examples for `polygon`, `pie`, and `arc` primitives |
| 10 | L-N10 | Low | §14 | Rewrite "available for reference" phrase for frames in included files |

### Overall Assessment (v2.6)

All 18 original issues are resolved. A fresh full-document review of v2.6 identified **10 new issues** (3 medium, 7 low). The document remains highly usable; the medium-severity gaps (multiple background calls, GRAY colorspace, `em` context) should be resolved before implementation to avoid ambiguity.

| Category | Original | Resolved | New in v2.6 | Total Open |
|---|---|---|---|---|
| High | 4 | 4 | 0 | 0 |
| Medium | 6 | 6 | 3 | 3 |
| Low | 8 | 8 | 7 | 7 |
| **Total** | **18** | **18** | **10** | **10** |

---

## Re-Review — 2026-04-27 18:04:59 (DSL Grammar v2.7 — Fix all 10 new issues)

All 10 issues identified in the 2026-04-27 17:49:53 re-verification have been fixed. The DSL grammar document is now at **v2.7**.

### Issue Status

| ID | Severity | Status | Resolution |
|---|---|---|---|
| M-N1 | Medium | **Resolved** | Added single-background-per-frame constraint to §7: more than one `background()` call in the same frame is a validation error with message `<file>:<line>: error: duplicate background statement in frame '<frame-id>'`. |
| M-N2 | Medium | **Resolved** | Added CCIR 601 greyscale conversion note to §15.1: `Y = 0.299×R + 0.587×G + 0.114×B`; alpha channel discarded; `colorspace=RGBA` recommended for transparency alongside greyscale. |
| M-N3 | Medium | **Resolved** | Added `em`-outside-font-context note to §15.3: `em` outside a `font` primitive resolves to the default font size of `12px`. |
| L-N4 | Low | **Resolved** | Updated §18.2 angle normalisation row to explicitly name all three angle parameters: `rotate`, `start-angle`, and `end-angle` — all normalised modulo 360. |
| L-N5 | Low | **Resolved** | Updated §8.0 `scale` row description: negative values are not supported and result in a validation error. |
| L-N6 | Low | **Resolved** | Updated §12.2 `clip-shape` row: clarifies that it accepts fixed shape keywords (`circle`, `square`, `polygon`) referring to built-in primitive geometry, not user-defined template names. |
| L-N7 | Low | **Resolved** | Added static-pattern-rendering note to §9.6: when `animated=false`, the `pattern` value is rendered as a static repeating stroke style without advancing between frames. |
| L-N8 | Low | **Resolved** | Added recursion policy to §13.1: direct and indirect recursion is not supported; results in a runtime error `<file>:<line>: error: recursive call to function '<name>' is not permitted`. |
| L-N9 | Low | **Resolved** | Added §17.9 (polygon and pie primitives) and §17.10 (arc primitive) — fully annotated examples covering point-list syntax, angle semantics, and fill restrictions. |
| L-N10 | Low | **Resolved** | Rewrote §14 frames-in-included-files sentence: frame definitions in included files are **ignored** and produce no output; only `begin_obj` and `begin_func` definitions are imported. |

### Updated Section Coverage (v2.7)

| Section | Status | Notes |
|---|---|---|
| §1 Overview | **Complete** | — |
| §2 Lexical Conventions | **Complete** | — |
| §3 Formal Grammar (EBNF) | **Complete** | — |
| §4 Top-Level Structure | **Complete** | — |
| §5 Frame Definition | **Complete** | — |
| §6 Image Canvas Statement | **Complete** | — |
| §7 Background Statement | **Complete** | M-N1 resolved |
| §8 Drawing Primitives | **Complete** | L-N4, L-N5 resolved |
| §9 Connector | **Complete** | L-N7 resolved |
| §10 Font / Text | **Complete** | — |
| §11 Image Primitive | **Complete** | — |
| §12 Object Templates | **Complete** | L-N6 resolved |
| §13 Function Declarations | **Complete** | L-N8 resolved |
| §14 Include Statement | **Complete** | L-N10 resolved |
| §15 Data Types | **Complete** | M-N2, M-N3 resolved |
| §16 Parameter Reference | **Complete** | — |
| §17 Examples | **Complete** | L-N9 resolved |
| §18 Error Reference | **Complete** | L-N4 resolved |

### Overall Assessment (v2.7)

All **28 issues** (18 original + 10 new) are now resolved. All 18 sections are **Complete**. The document is ready for implementation use.

| Category | Original | Resolved | New in v2.6 | Total Resolved | Open |
|---|---|---|---|---|---|
| High | 4 | 4 | 0 | 4 | 0 |
| Medium | 6 | 6 | 3 | 9 | 0 |
| Low | 8 | 8 | 7 | 15 | 0 |
| **Total** | **18** | **18** | **10** | **28** | **0** |
