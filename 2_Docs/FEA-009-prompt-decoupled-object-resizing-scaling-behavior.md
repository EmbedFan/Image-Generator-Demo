# FEA-009 - Decoupled Object Resizing and Scaling Behavior

| Field | Value |
|---|---|
| **Description** | Separate object bounding-box resizing from geometric scaling for DSL object instances |
| **Created at** | 2026-05-09 06:44:42 |
| **File version** | 1.0 |
| **Created by** | GPT-5 Codex |

---

## Overview

This feature introduces an explicit separation between two object-instance behaviors that are currently coupled:

1. Bounding-box resizing through `width` and `height`
2. Geometric scaling of the object's internal content

The goal is to keep the current behavior fully intact by default while adding an opt-in mode for layout-driven, UI-like objects that need to resize without distorting their internal geometry.

---

## Problem Statement

Today, overriding `width` and/or `height` on an object instance implicitly scales the object's internal geometry.

That default is useful for many diagram-style objects, but it is limiting for objects that should behave more like UI components or responsive containers. In those cases:

- the container should become wider or taller
- borders or background areas may stretch
- child elements may reposition from layout logic
- fixed-size content such as icons or text should not necessarily scale

Because resizing and scaling are currently coupled, the DSL cannot express that distinction cleanly.

---

## Proposed Feature

Add an explicit opt-in object-instance mode that disables implicit geometry scaling when `width` and `height` are overridden.

In that mode:

- `width` and `height` redefine the instance bounding box
- object-local layout expressions resolve against the new dimensions
- internal geometry is not automatically scaled just because the box changed
- `scale` remains the explicit control for geometric scaling

The exact DSL keyword for the mode can be finalized during implementation. Example candidate shapes include a dedicated mode attribute such as `resize-mode=layout`.

---

## Behavior Model

### 1. Default behavior (backward compatible)

Keep the current behavior unchanged:

- `width` and `height` continue to imply proportional scaling of internal geometry
- `scale` continues to work as it does now
- if both explicit `width`/`height` and `scale` are provided in the default mode, the current precedence rule remains in force

### 2. Layout-resize behavior (new, opt-in)

When the explicit layout-resize mode is enabled:

- `width` and `height` affect layout space, not implicit geometry scaling
- `scale` is the explicit geometric scaling control
- `width`/`height` and `scale` may be combined without treating them as conflicting by default

---

## Intended Use Cases

- Dialog boxes whose borders stretch while title text stays readable
- Panels whose internal content repositions from expressions based on object width/height
- Responsive template objects driven by bbox calculations and arithmetic layout logic
- Reusable UI-like components where container growth should not distort fixed-size glyphs or icons

---

## Documentation Impact

The following project documents should reflect the feature:

| Document | Required update |
|---|---|
| `2_Docs/my_vision.md` | Describe the new separation between default scaling behavior and opt-in layout resizing |
| `2_Docs/requirements.md` | Define the opt-in behavior, backward-compatibility rule, and explicit-scale semantics |
| `2_Docs/system_design.md` | Describe the two object-instantiation execution paths and layout-context handling |

---

## Acceptance Criteria

The feature is considered documented correctly when:

- the default object-instance behavior remains explicitly backward compatible
- the new opt-in layout-resize behavior is described without forcing a final implementation keyword prematurely
- `scale` remains documented as the explicit geometric scaling control in the new mode
- layout-driven reflow is captured as a first-class use case
- the three core project documents are updated consistently
