# FEA-004 Implementation Plan — Configurable Grid System with Optional Rendering and Alignment Support

| Field | Value |
|---|---|
| **Description** | Introduce an optional configurable grid system at frame level supporting non-visual layout assistance, optional rendered grid lines, global and per-element alignment/snapping |
| **Created at** | 2026-05-02 19:57:13 |
| **File version** | 1.0 |
| **Created by** | Claude Sonnet 4.6 |

---

## 1. Feature Overview

**Feature ID:** FEA-004  
**Title:** Configurable Grid System with Optional Rendering and Alignment Support  
**Related requirements:** REQ-0038, REQ-0038.1, REQ-0038.2, REQ-0038.3, REQ-0038.4  
**Type:** New feature (backward compatible)

### Description

Introduce an optional configurable grid system at the frame level of the DSL canvas. The grid provides a logical coordinate overlay that assists with precise object placement and alignment.

Key characteristics:

1. **Non-visual by default** — defining a grid has no effect on rendered output unless `render=true` is specified.
2. **Optional visual rendering** — when `render=true`, the grid is drawn over the canvas after all other primitives, with configurable `color`, `line-type`, and `line-width`.
3. **Global alignment** — `align=true` snaps all drawable elements in the frame to the nearest grid intersection.
4. **Per-element snap** — any primitive or object can carry `snap=grid-intersection|grid-x|grid-y|none` to snap individually or opt out of global alignment.
5. **Transform pipeline integration** — alignment is resolved before transforms (position → scale → skew → rotate), consistent with REQ-0017.

All parameters are optional; existing scripts without a `grid()` statement are unaffected.

---

## 2. DSL Syntax Changes

No new keywords are introduced. `grid` uses the existing `<name>(<param-list>)` call syntax.

### Grid statement (frame-level)

```dsl
grid(step-x=<value>, step-y=<value>
    [, offset-x=<value>, offset-y=<value>]
    [, render=true|false]
    [, color=<color>, line-type=<type>, line-width=<value>]
    [, align=true|false])
```

### Per-element snap parameter

```dsl
<primitive>(<existing-params>, snap=grid-intersection|grid-x|grid-y|none)
```

### Examples

```dsl
begin_frame layout_demo
image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
background(color=white);

# Grid visible for debugging — no alignment
grid(step-x=50px, step-y=50px, render=true, color=RGB(200,200,200), line-type=dashed, line-width=1px);

# Grid with global alignment enabled
# grid(step-x=50px, step-y=50px, align=true);

# Per-element snap to nearest intersection — center=(63,48) snaps to (50,50)
circle(color=black, line-width=2px, fill=red, center=(63,48), radius=20, snap=grid-intersection);

# Snap only horizontal position — x=78 snaps to 50; y=100 unchanged
square(color=black, line-width=1px, fill=blue, pos=(78,100), width=40px, height=40px, snap=grid-x);

# Opt out of global align for this element
font(font-family=Arial, font-size=12px, color=black, text="Label", pos=(63,48), snap=none);
end_frame
```

---

## 3. Files to Modify / Create

| File | Change |
|---|---|
| `imagegen/parser.py` | Add `grid` to recognized frame-level statement keywords; parse `grid()` parameters into a `GridNode` AST node; add `snap` to accepted named parameters on all primitive and object-instance parser paths |
| `imagegen/semantic_validator.py` | Validate: `step-x` and `step-y` required and > 0; at most one `grid` per frame; `snap` without a grid in the frame is a validation error; `render=true` without `color` emits a warning (defaults to `RGB(200,200,200)`) |
| `imagegen/rendering/grid_resolver.py` | **New module:** pure function `snap_position(x, y, grid, mode)` — computes snapped coordinates with no I/O |
| `imagegen/rendering/grid_renderer.py` | **New module:** `render_grid(canvas, grid)` — draws horizontal and vertical grid lines via `ImageDraw.line()` when `render=true` |
| `imagegen/rendering/frame_runner.py` | Wire grid resolver into the draw-command loop (before Transform Applier); wire grid renderer as a post-process step after all primitives |

---

## 4. Implementation Steps

### Step 1 — Extend the parser

**File:** `imagegen/parser.py`

Add `grid` as a recognized frame-level statement (alongside `background`, `image`, `hold-time`, `frame-mode`). Parse it into a `GridNode` dataclass:

```python
@dataclass
class GridNode:
    step_x:     float          # resolved to px
    step_y:     float          # resolved to px
    offset_x:   float = 0.0
    offset_y:   float = 0.0
    render:     bool  = False
    color:      Optional[str] = None
    line_type:  str   = 'solid'
    line_width: float = 1.0
    align:      bool  = False
    file: str = ''
    line: int = 0
```

Add `snap` to the accepted named-parameter set for all primitive and object-instance parsers. Valid string values: `'grid-intersection'`, `'grid-x'`, `'grid-y'`, `'none'`.

### Step 2 — Add validation rules

**File:** `imagegen/semantic_validator.py`

```python
# step-x and step-y must be positive
if grid_node.step_x <= 0 or grid_node.step_y <= 0:
    raise ValidationError("grid: step-x and step-y must be > 0")

# at most one grid per frame
if frame.grid is not None:
    raise ValidationError("frame may contain at most one grid() statement")

# snap without grid definition
if node.snap is not None and frame.grid is None:
    raise ValidationError(
        f"{node.file}:{node.line}: snap={node.snap!r} used but no grid() is defined in this frame"
    )

# render=true without color — default with warning
if grid_node.render and grid_node.color is None:
    reporter.warning(
        f"{grid_node.file}:{grid_node.line}: warning: "
        f"grid render=true without color; defaulting to RGB(200,200,200)"
    )
    grid_node.color = 'RGB(200,200,200)'
```

### Step 3 — Implement Grid Resolver

**File:** `imagegen/rendering/grid_resolver.py`

```python
from __future__ import annotations
from imagegen.ast_nodes import GridNode

def snap_position(
    x: float, y: float, grid: GridNode, mode: str
) -> tuple[float, float]:
    """Snap (x, y) to the grid according to the given snap mode."""

    def snap_axis(value: float, step: float, offset: float) -> float:
        relative = value - offset
        snapped  = round(relative / step) * step
        return snapped + offset

    if mode in ('grid-intersection', 'grid-x'):
        x = snap_axis(x, grid.step_x, grid.offset_x)
    if mode in ('grid-intersection', 'grid-y'):
        y = snap_axis(y, grid.step_y, grid.offset_y)
    return x, y
```

### Step 4 — Implement Grid Renderer

**File:** `imagegen/rendering/grid_renderer.py`

```python
from __future__ import annotations
from PIL import ImageDraw
from imagegen.ast_nodes import GridNode

def render_grid(canvas, grid: GridNode) -> None:
    """Draw grid lines over the canvas. No-op when render=False."""
    if not grid.render:
        return
    draw = ImageDraw.Draw(canvas)
    w, h = canvas.size
    color = grid.color
    width = max(1, int(grid.line_width))

    x = grid.offset_x
    while x <= w:
        draw.line([(x, 0), (x, h)], fill=color, width=width)
        x += grid.step_x

    y = grid.offset_y
    while y <= h:
        draw.line([(0, y), (w, y)], fill=color, width=width)
        y += grid.step_y
```

### Step 5 — Wire into Frame Runner

**File:** `imagegen/rendering/frame_runner.py`

In the main draw-command loop, before passing element coordinates to the Transform Applier:

```python
from imagegen.rendering.grid_resolver import snap_position

# Determine effective snap mode for this element
snap_mode = node.snap  # per-element snap (may be None)
if snap_mode is None and frame.grid and frame.grid.align:
    snap_mode = 'grid-intersection'  # inherit global align

if snap_mode and snap_mode != 'none' and frame.grid:
    node.pos_x, node.pos_y = snap_position(
        node.pos_x, node.pos_y, frame.grid, snap_mode
    )
```

After all primitives are rendered, call:

```python
from imagegen.rendering.grid_renderer import render_grid

if frame.grid:
    render_grid(canvas, frame.grid)
```

---

## 5. Testing Plan

| Test | Input | Expected Result |
|---|---|---|
| No grid defined | Frame without `grid()` | Renders identically to current behavior |
| Grid defined, no render, no align | `grid(step-x=50px, step-y=50px)` | No visual change to output |
| Grid visual rendering | `grid(step-x=50px, step-y=50px, render=true, color=gray, line-type=dashed, line-width=1px)` | Dashed gray grid lines at 50px intervals drawn over canvas |
| Grid offset | `grid(step-x=50px, step-y=50px, offset-x=10px, offset-y=10px, render=true, color=gray)` | Grid lines shifted by 10px from origin |
| Global align | `grid(step-x=50px, step-y=50px, align=true)` + `circle(center=(63,48), ...)` | Circle rendered at (50,50) |
| Per-element snap intersection | `grid(step-x=50px, step-y=50px)` + `circle(center=(63,48), snap=grid-intersection)` | Circle snapped to (50,50) |
| Per-element snap grid-x | `grid(step-x=50px, step-y=50px)` + `circle(center=(63,48), snap=grid-x)` | Circle at x=50, y=48 (only x snapped) |
| Per-element snap grid-y | `grid(step-x=50px, step-y=50px)` + `circle(center=(63,48), snap=grid-y)` | Circle at x=63, y=50 (only y snapped) |
| snap=none overrides global align | `grid(step-x=50px, step-y=50px, align=true)` + `circle(center=(63,48), snap=none)` | Circle stays at (63,48) |
| snap without grid | `circle(center=(63,48), snap=grid-intersection)` (no grid in frame) | Validation error halts execution |
| Two grid statements | Frame with two `grid()` calls | Validation error halts execution |
| step-x = 0 | `grid(step-x=0, step-y=50px)` | Validation error halts execution |
| step-y negative | `grid(step-x=50px, step-y=-10px)` | Validation error halts execution |
| render=true without color | `grid(step-x=50px, step-y=50px, render=true)` | Warning emitted; grid drawn in RGB(200,200,200) |
| Snap + rotation | `grid(step-x=50px, step-y=50px)` + `square(pos=(63,48), ..., snap=grid-intersection, rotate=45)` | Square position snapped to (50,50) before rotation applied |

---

## 6. Notes

- **Backward compatible** — no `grid` statement means no change to any existing script.
- **No new grammar keywords** — `grid` uses the existing `<name>(<param-list>)` call syntax identical to `background()`.
- **Transform order guaranteed** — snap is applied to raw coordinates before the Transform Applier; rotation and scale are computed around the already-snapped position (REQ-0038.4).
- **Grid lines are a post-process** — they are drawn after all other primitives so they always appear on top, consistent with design/debug intent.
- **Unit support** — `step-x`, `step-y`, `offset-x`, `offset-y`, and `line-width` accept all standard units (px, pt, cm, mm, %, em) per REQ-0021.
- **snap=none** — this value is only meaningful as a per-element override when `align=true` is set globally; using it in a frame without a grid is still a validation error.
