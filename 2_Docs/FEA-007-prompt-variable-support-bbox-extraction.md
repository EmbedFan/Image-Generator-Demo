# FEA-007 — Variable Support and Bounding Box Extraction in DSL

| Field | Value |
|---|---|
| **Description** | Introduce variable declarations and computed bounding box property access in the DSL to enable dynamic, data-driven layouts |
| **Created at** | 2026-05-04 18:12:00 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## Overview

Introduce variable handling and computed geometry extraction into the DSL to enable dynamic, data-driven layout behavior. This enhancement allows scripts to access engine-computed properties (such as bounding boxes) and reuse them for precise positioning, alignment, and layout chaining.

The current DSL is strictly declarative and does not expose computed values, which limits advanced composition scenarios.

---

## Problem Statement

During rendering, the DSL engine internally computes geometric properties for each object (e.g., bounding box: x, y, width, height).

These values are not accessible from the DSL script, which prevents:

- Relative positioning between objects
- Layout chaining (placing objects based on previous ones)
- Dynamic alignment depending on content size (e.g., text width)
- UI-like compositions and responsive layouts

---

## Proposed Feature

### 1. Variable Declaration

Add DSL-level variable declarations:

```
var x, y;
var width;
var height;
```

Variables are scoped to the frame or function context in which they are declared.

---

### 2. Assignment from Object Properties

Allow assigning computed values from rendered objects:

```
x = rect1.bbox.x;
y = rect1.bbox.y;
width = rect1.bbox.width;
height = rect1.bbox.height;
```

---

### 3. Bounding Box Access

Each drawable object instance exposes a read-only structure:

```
<object>.bbox.x
<object>.bbox.y
<object>.bbox.width
<object>.bbox.height
```

The bounding box reflects the final rendered geometry after all transformations (scale, rotate, etc.) have been applied.

---

### 4. Usage in Expressions

Variables are usable in parameter expressions:

```
square(pos=(x + width + 10, y), width=50, height=50);
```

This extends the existing function expression capability to general DSL frame and function body usage.

---

### 5. Execution Model Extension

Updated execution pipeline:

1. Render object
2. Compute bounding box
3. Store values in variable space
4. Allow subsequent statements to reference them

This introduces a controlled sequential evaluation within the otherwise declarative model.

---

## Constraints and Rules

- Variables are re-assignable within the same scope
- Accessing `.bbox` before the object is rendered → runtime error
- Using an undefined variable → parse or runtime error
- Circular dependencies are not allowed
- Variable names follow standard identifier rules (letters, digits, underscores; cannot start with digit)

---

## Scope Resolution

- Variables declared inside a `begin_frame`/`end_frame` block are frame-scoped
- Variables declared inside a `begin_func`/`end_func` block are function-scoped
- Frame-scoped and function-scoped variable namespaces are separate

---

## Applicability

Bounding box properties are available on all drawable elements:

- All primitives: `line`, `circle`, `square`, `polygon`, `path`, `pie`, `arc`
- `connector`
- `font` / text
- `image` primitive
- Object instances

---

## Open Questions Resolved

| Question | Resolution |
|---|---|
| Variable scoping | Frame-scoped and function-scoped |
| Reassignment | Allowed |
| Bbox applicability | All primitives, objects, text, connectors |
| When bbox is computed | After full transform pipeline |
| Compound expressions | Supported in all parameters |

---

## Documents Updated

| Document | Changes |
|---|---|
| `2_Docs/my_vision.md` | Added variable declaration and bbox access syntax to DSL language description |
| `2_Docs/requirements.md` | Added section 1.20 (Variable Support and Bounding Box Extraction) with REQ-0041 through REQ-0041.5; updated REQ-0028 grammar |
| `2_Docs/system_design.md` | Added section 3.3.11 (Variable Store and Bbox Extractor); updated architecture diagram, traceability table |
