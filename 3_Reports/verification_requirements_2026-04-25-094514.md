# Verification Report — Requirements vs Vision

| Field | Value |
|---|---|
| **Description** | Verification of 2_Docs/requirements.md against 2_Docs/my_vision.md |
| **Created at** | 2026-04-25 09:45:14 |
| **File version** | 1.1 |
| **Created by** | Claude Sonnet 4.6 |

---

## Inputs

| File | Role |
|---|---|
| `2_Docs/my_vision.md` | Source of truth |
| `2_Docs/requirements.md` | Document under verification |

---

## Coverage Summary

All vision items below are correctly and completely captured in the requirements.

| Vision Feature | Requirement(s) |
|---|---|
| Script processing engine | REQ-0001, REQ-0001.1, REQ-0001.2 |
| Frame definition, hold-time, frame-mode, colorspace | REQ-0002 – REQ-0002.3 |
| Image canvas (width, height, dpi, colorspace, output-format) | REQ-0003 |
| Solid / gradient / image background | REQ-0004.1 – REQ-0004.3 |
| All primitives: line, circle, square, polygon, path, pie, font, image | REQ-0005 – REQ-0013 |
| Connector: multi-segment, types, caps, cap-size, corners, label, animation, pattern | REQ-0011 – REQ-0011.9 |
| Object templates, instantiation, clipping, nesting | REQ-0014 – REQ-0014.3 |
| Function declarations, expressions, composition | REQ-0015 – REQ-0015.2 |
| Script file inclusion, path resolution, recursive includes | REQ-0016 – REQ-0016.2 |
| Transformations (rotate, skew, scale) | REQ-0017 |
| Z-order / z-index | REQ-0018 |
| Coordinate system | REQ-0019 |
| Color formats | REQ-0020 |
| Unit measurements | REQ-0021 |
| Line-type styles | REQ-0022 |
| String handling & escaping | REQ-0023 |
| Statement delimiters | REQ-0024 |
| Type validation & error handling | REQ-0025 |
| Python implementation, output formats | REQ-0026, REQ-0027 |
| Grammar, output file naming | REQ-0028, REQ-0029 |
| CLI, error messages | REQ-0030, REQ-0031 |
| External image assets, modular inclusion | REQ-0032, REQ-0033 |

---

## Issues Found

### Issue 1 — Wrong dependencies on REQ-0004.3 and REQ-0013

| Field | Value |
|---|---|
| **Severity** | High |
| **Affected requirements** | REQ-0004.3, REQ-0013 |

**Description:**  
Both REQ-0004.3 (Image Background) and REQ-0013 (image primitive) list `REQ-0033` (Modular Script Composition / `include` mechanism) as a dependency. This is incorrect — loading an external image file has no relationship to the `include` mechanism. The intended dependency is `REQ-0032` (External Image Asset Support).

Additionally, REQ-0032 already depends on REQ-0004.3 and REQ-0013, so having the reverse dependency also creates a circular reference.

**Required fix:**  
Replace `REQ-0033` with `REQ-0032` in the Dependencies field of REQ-0004.3 and REQ-0013.

---

### Issue 2 — Border shadow not covered

| Field | Value |
|---|---|
| **Severity** | Medium |
| **Affected requirements** | REQ-0014 |

**Description:**  
The vision specifies border attributes including `shadow (offset-x offset-y blur-radius color)` for objects. REQ-0014 mentions "border properties" generically but has no testable acceptance criterion for shadow rendering. Shadow is a distinct rendering feature (blur, offset, color) and needs explicit coverage.

**Required fix:**  
Add a sub-requirement (e.g., REQ-0014.4) specifying object border shadow support with `offset-x`, `offset-y`, `blur-radius`, and `color` parameters and a testable acceptance criterion.

---

### Issue 3 — Optional parameter defaults and named-param ordering not captured

| Field | Value |
|---|---|
| **Severity** | Medium |
| **Affected requirements** | None (gap) |

**Description:**  
The vision contains an explicit section on optional vs required parameters:
- Required: `color`, `line-type`, `line-width`, `center`/`pos`/`start`/`end`, `radius`/`width`/`height`
- Optional with defaults: `fill=none`, `z-index=declaration-order`, `style=normal`, `weight=normal`
- Named parameters are **order-independent**

No requirement captures: (a) the specific default values for optional parameters, or (b) that named parameters may appear in any order. Both are testable and unambiguous.

**Required fix:**  
Add a new requirement (e.g., REQ-0025.1) covering default values and named-parameter order-independence.

---

### Issue 4 — Grammar in REQ-0028 is incomplete

| Field | Value |
|---|---|
| **Severity** | Medium |
| **Affected requirements** | REQ-0028 |

**Description:**  
The grammar production rules in REQ-0028 cover frames, primitives, and objects but omit two major DSL constructs that have their own requirements:
- `begin_func` / `end_func` function declarations (REQ-0015)
- `include "..."` script inclusion (REQ-0016)

**Required fix:**  
Add the following productions to REQ-0028:
- `<func-decl> := 'begin_func' <name> '(' <param-list> ')' <drawing-commands> 'end_func'`
- `<include-stmt> := 'include' '"' <path> '"'`
- Update `<script>` to allow top-level func-decls, include-stmts, and object definitions in addition to frames.

---

### Issue 5 — `arc` primitive mentioned in vision GOAL but undefined

| Field | Value |
|---|---|
| **Severity** | Low |
| **Affected requirements** | None (gap in vision) |

**Description:**  
The vision's GOAL states: *"basic image objects such as line, paths, polygon, circle, pie, **arcs**, connectors"*. No `arc` primitive is defined in the DSL specification, and no requirement exists for it. The `pie` primitive with `start-angle`/`end-angle` provides partial arc capability (pie slice), but a standalone open arc (no lines to center) is not covered.

**Required fix:**  
Either (a) add an `arc` primitive to the vision and requirements (open arc: center, radius, start-angle, end-angle, stroke only), or (b) add a note to REQ-0010 explicitly stating that `pie` covers arc rendering when used without fill, and remove `arc` from the GOAL statement in the vision.

---

## Issue Summary

| # | Severity | Requirement(s) | Description |
|---|---|---|---|
| 1 | **High** | REQ-0004.3, REQ-0013 | Wrong dependency: `REQ-0033` should be `REQ-0032` |
| 2 | **Medium** | REQ-0014 (gap) | Border shadow attribute has no testable acceptance criteria |
| 3 | **Medium** | — (gap) | Optional parameter defaults and named-param order-independence not required |
| 4 | **Medium** | REQ-0028 | Grammar missing `begin_func`/`end_func` and `include` productions |
| 5 | **Low** | — (vision gap) | `arc` primitive in vision GOAL has no DSL definition or requirement |

---

## Re-Verification — 2026-04-25 09:58:23 (requirements.md v1.5)

### Inputs

| File | Version |
|---|---|
| `2_Docs/requirements.md` | 1.5 |
| `2_Docs/my_vision.md` | current |

### Issue Resolution Status

| # | Original Severity | Requirement(s) | Fix Applied | Status |
|---|---|---|---|---|
| 1 | **High** | REQ-0004.3, REQ-0013 | Dependencies changed from `REQ-0033` to `REQ-0032` | ✅ Resolved |
| 2 | **Medium** | REQ-0014 (gap) | REQ-0014.4 added: Object Border Shadow with testable acceptance criteria | ✅ Resolved |
| 3 | **Medium** | — (gap) | REQ-0025.1 added: Optional Parameter Defaults and Named-Parameter Ordering | ✅ Resolved |
| 4 | **Medium** | REQ-0028 | Grammar expanded with `<func-decl>`, `<func-call>`, `<include-stmt>`, updated `<script>` top-level rule; dependencies updated | ✅ Resolved |
| 5 | **Low** | — (vision gap) | REQ-0010.1 added: Primitive: arc (open curved arc, stroke only); vision updated to include arc in primitives list | ✅ Resolved |

### New Coverage Check

All previously identified gaps are now covered. Re-verification of the complete requirements document finds:

| Vision Feature | Requirement(s) |
|---|---|
| Script processing engine | REQ-0001, REQ-0001.1, REQ-0001.2 |
| Frame definition, hold-time, frame-mode, colorspace | REQ-0002 – REQ-0002.3 |
| Image canvas (width, height, dpi, colorspace, output-format) | REQ-0003 |
| Solid / gradient / image background | REQ-0004.1 – REQ-0004.3 |
| All primitives: line, circle, square, polygon, path, pie, arc, font, image | REQ-0005 – REQ-0013 (incl. REQ-0010.1) |
| Connector: multi-segment, types, caps, cap-size, corners, label, animation, pattern | REQ-0011 – REQ-0011.9 |
| Object templates, instantiation, border shadow, clipping, nesting | REQ-0014 – REQ-0014.4 |
| Function declarations, expressions, composition | REQ-0015 – REQ-0015.2 |
| Script file inclusion, path resolution, recursive includes | REQ-0016 – REQ-0016.2 |
| Transformations (rotate, skew, scale) | REQ-0017 |
| Z-order / z-index | REQ-0018 |
| Coordinate system | REQ-0019 |
| Color formats | REQ-0020 |
| Unit measurements | REQ-0021 |
| Line-type styles | REQ-0022 |
| String handling & escaping | REQ-0023 |
| Statement delimiters | REQ-0024 |
| Type validation, error handling, optional param defaults, named-param ordering | REQ-0025, REQ-0025.1 |
| Python implementation, output formats | REQ-0026, REQ-0027 |
| DSL grammar (incl. func-decl, include-stmt) | REQ-0028 |
| Output file naming | REQ-0029 |
| CLI, error messages | REQ-0030, REQ-0031 |
| External image assets, modular inclusion | REQ-0032, REQ-0033 |

### New Issues Found

None. All vision features are completely and correctly captured in the requirements.

### Verdict

**PASS** — `2_Docs/requirements.md` v1.5 is fully consistent with `2_Docs/my_vision.md`. All previously identified issues have been resolved. No new gaps detected.

---
## Changelog

### 2026-04-25 09:58:23 — Re-verification against requirements.md v1.5
- All 5 issues from the initial verification confirmed resolved.
- New coverage table added reflecting REQ-0010.1, REQ-0014.4, REQ-0025.1, and updated REQ-0028.
- Overall verdict: PASS.
