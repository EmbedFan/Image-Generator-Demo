# FEA-003 Implementation Plan — Optional Size and Rotation Parameters for DSL Objects

| Field | Value |
|---|---|
| **Description** | Add optional width/height override, uniform scale factor, and clockwise rotation to DSL object instantiation calls |
| **Created at** | 2026-05-02 18:59:02 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## 1. Feature Overview

**Feature ID:** FEA-003  
**Title:** Optional Size and Rotation Parameters for DSL Objects  
**Related requirements:** REQ-0036, REQ-0036.1, REQ-0036.2, REQ-0037  
**Type:** New feature (backward compatible)

### Description

DSL object instantiation calls currently support `pos` and attribute overrides (e.g., `background`). This feature extends the call syntax so that object instances may optionally receive:

1. **Explicit box size** — `width=<value>` and/or `height=<value>` override the template's declared dimensions for that instance only.
2. **Uniform scale factor** — `scale=<multiplier>` scales all template dimensions proportionally (e.g., `scale=1.6` renders at 160% of template size).
3. **Rotation** — `rotate=<degrees>` rotates the object clockwise around its center, following the same transform rules already used for primitives.

**Precedence rule:** When both explicit `width`/`height` and `scale` are provided, explicit dimensions take priority and a warning is emitted.

All parameters are optional; existing scripts are unaffected (backward compatible).

---

## 2. DSL Syntax Changes

No new keywords are introduced. The existing named-parameter call syntax is extended.

### Before (existing)
```dsl
card(pos=(100,100));
card(pos=(300,100), background=RGB(100,150,200));
```

### After (new optional parameters)
```dsl
# Explicit box size
card(pos=(100,100), width=300px, height=80px);

# Uniform scale
card(pos=(200,100), scale=1.6);

# Rotation only
card(pos=(300,100), rotate=45);

# Combined: size + rotation
card(pos=(400,100), width=200px, height=60px, rotate=30);

# Combined: scale + rotation
card(pos=(500,100), scale=0.5, rotate=90);

# Conflict: explicit size + scale → explicit size wins, warning emitted
card(pos=(600,100), width=200px, height=60px, scale=2.0, rotate=15);
```

---

## 3. Files to Modify

| File | Change |
|---|---|
| `imagegen/parser.py` | Fix `is_named` disambiguation to also accept KEYWORD tokens (e.g. `width=`, `height=`) as the start of a named-parameter list |
| `imagegen/semantic_validator.py` | Validate: `scale` > 0 (error on ≤ 0); `rotate` ≥ 0 (error on negative); `rotate` with unit suffix (error); warning when both `width`/`height` and `scale` are provided |
| `imagegen/rendering/object_instantiator.py` | Apply size priority logic (explicit w/h > scale > template default); apply clockwise rotation with paste-position correction |

---

## 4. Implementation Steps

### Step 1 — Extend the parser to accept instance-time size/rotation parameters

**File:** `imagegen/parser.py`

In the object instantiation call handler, add `width`, `height`, `scale`, and `rotate` to the set of accepted named parameters. These are treated identically to other named parameters at parse time — no special grammar rule is needed.

```python
OBJECT_INSTANCE_PARAMS = {
    'pos', 'background', 'border', 'shadow',
    'clip-bounds', 'clip-shape',
    # FEA-003: instance-time size and rotation
    'width', 'height', 'scale', 'rotate',
}
```

### Step 2 — Add validation rules

**File:** `imagegen/validator.py`

Add the following checks when validating object instantiation nodes:

```python
# scale must be a positive non-zero number
if 'scale' in params:
    if params['scale'] <= 0:
        raise ValidationError("object instance 'scale' must be > 0")

# rotate must be non-negative
if 'rotate' in params:
    if params['rotate'] < 0:
        raise ValidationError("object instance 'rotate' must be >= 0")

# precedence warning: explicit size overrides scale
if ('width' in params or 'height' in params) and 'scale' in params:
    reporter.warning(
        f"{node.file}:{node.line}: warning: object '{node.name}': "
        f"explicit width/height provided together with scale; scale is ignored"
    )
```

### Step 3 — Apply size and rotation in the instantiator

**File:** `imagegen/instantiator.py`

In the `_resolve_instance_size()` helper (or equivalent method that merges template attributes with instance overrides):

```python
def _resolve_instance_size(template, instance_params):
    """Return (width, height) for this instance."""
    has_explicit_w = 'width' in instance_params
    has_explicit_h = 'height' in instance_params
    has_scale      = 'scale' in instance_params

    if has_explicit_w or has_explicit_h:
        # Explicit size takes precedence; scale is ignored (warning already emitted by validator)
        w = instance_params.get('width',  template.width)
        h = instance_params.get('height', template.height)
    elif has_scale:
        factor = instance_params['scale']
        w = template.width  * factor
        h = template.height * factor
    else:
        w = template.width
        h = template.height

    return w, h
```

After resolving the size, apply the rotation transform around the object center:

```python
rotate_deg = instance_params.get('rotate', 0)
# rotation is applied via the existing Transform Applier (REQ-0017)
# pass rotate_deg to the transform pipeline for this object's render context
```

---

## 5. Testing Plan

| Test | Input | Expected Result |
|---|---|---|
| No size/rotation params | `card(pos=(100,100))` | Renders at template dimensions, no rotation — identical to current behavior |
| Explicit width only | `card(pos=(100,100), width=300px)` | Width = 300px; height = template default |
| Explicit height only | `card(pos=(100,100), height=50px)` | Height = 50px; width = template default |
| Explicit width + height | `card(pos=(100,100), width=300px, height=80px)` | Renders at 300×80 regardless of template |
| Scale factor | `card(pos=(100,100), scale=1.6)` | Width and height each multiplied by 1.6 |
| Scale = 0 | `card(pos=(100,100), scale=0)` | Validation error halts execution |
| Scale negative | `card(pos=(100,100), scale=-1)` | Validation error halts execution |
| Rotation 45° | `card(pos=(100,100), rotate=45)` | Object rendered rotated 45° clockwise around its center |
| Rotation 0° | `card(pos=(100,100), rotate=0)` | No rotation — same as omitting `rotate` |
| Rotation negative | `card(pos=(100,100), rotate=-10)` | Validation error halts execution |
| Scale + rotation | `card(pos=(100,100), scale=0.5, rotate=90)` | Object at 50% size, rotated 90° |
| Explicit size + scale (conflict) | `card(pos=(100,100), width=200px, height=60px, scale=2.0)` | Renders at 200×60; warning emitted; `scale` ignored |
| Explicit size + rotation | `card(pos=(100,100), width=200px, height=60px, rotate=30)` | Renders at 200×60 and rotated 30° |

---

## 6. Notes

- **No DSL grammar change** — the new parameters reuse the existing named-parameter syntax; no new keywords.
- **Backward compatible** — scripts without `width`, `height`, `scale`, or `rotate` in object calls are unaffected.
- **`scale=0` is an error for object instances** — unlike primitive-level `scale=0` (valid but invisible per REQ-0025), an object instance scaled to zero is always a user mistake, so it is treated as a validation error.
- **Transform order** — rotation at the instance level is applied after size resolution, consistent with the existing transform pipeline (position → scale → skew → rotate, REQ-0017).
