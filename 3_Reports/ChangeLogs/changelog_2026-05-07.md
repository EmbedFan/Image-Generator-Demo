# Daily Changelog — 2026-05-07
### 2026-05-07 21:04:48 - Documentation update - FEA-008 comparison expressions and bounded loops
- Files: `2_Docs/FEA-008-prompt-comparison-expressions-do-while-loop.md`, `2_Docs/my_vision.md`, `2_Docs/requirements.md`, `2_Docs/system_design.md`, `2_Docs/DSL_grammar_description.md`, `2_Docs/DSL_user_guide.md`
- Action: Created/Updated
- Details: Added the feature request and extended the vision, requirements, system design, grammar reference, and user guide for numeric comparison expressions and bounded `do ... while` loops.

### 2026-05-07 21:04:48 — Bug fix — function args collapsed to zero in function bodies
- File: `imagegen/rendering/function_executor.py`
- Action: Updated
- Details: `_bind_args()` now preserves actual argument value types instead of forcing non-`LengthValue` args to `0.0`. Numeric `ExprFactor(LengthValue(...))` args are unwrapped correctly, string params stay `StringValue`, and unresolved names in function bodies fall back to `IdentValue` instead of becoming `0px`.

### 2026-05-07 20:43:30 — Bug fix — object shadows clipped during instantiation
- File: `imagegen/rendering/object_instantiator.py`
- Action: Updated
- Details: Added object-level shadow composition after the object is rendered and resized, with padded shadow canvas and paste-origin correction. Shadows on instantiated objects can now extend outside the object bounds instead of being cut off.

### 2026-05-07 20:18:27 — Bug fix — object resize clipped right/bottom borders
- File: `imagegen/rendering/object_instantiator.py`
- Action: Updated
- Details: Switched object-instance resizing back to native-size render plus final bitmap resize. Body attribute substitution now keeps native `width`/`height` while still applying merged style attributes like `background`, so resized objects no longer overflow and clip on the right/bottom edges.

### 2026-05-07 19:30:06 — Bug fix — extended CSS-3 named colors resolved as black
- File: `imagegen/parser.py`
- Action: Updated
- Details: Expanded `_NAMED_COLOR_MAP` from 20 entries to the full CSS-3 set (~147 names) matching the lexer. Colors like `lightblue`, `crimson`, `coral` etc. now resolve to their correct RGB values instead of silent black.

### 2026-05-07 18:43:41 — Bug fix — scale/rotate ignored on square, circle, polygon
- File: `imagegen/rendering/primitives/square_renderer.py`
- File: `imagegen/rendering/primitives/circle_renderer.py`
- File: `imagegen/rendering/primitives/polygon_renderer.py`
- Action: Updated (all three)
- Details: Square — isolated surface pipeline: scale→skew→rotate, centered composite. Circle — scale applied to radius directly. Polygon — bbox-local surface pipeline: scale→rotate, centered composite.

### 2026-05-07 18:32:09 — Bug fix — skew affine offset clipping (square + font)
- File: `imagegen/rendering/primitives/square_renderer.py`
- File: `imagegen/rendering/primitives/font_renderer.py`
- Action: Updated (both)
- Details: Replaced wrong `-extra/2` centering offset with `-extra` (positive skew) or `0` (negative skew); `int()` → `math.ceil()`. Bottom-left (skew-x) and top-right (skew-y) corners no longer clip.

### 2026-05-07 18:24:20 — Bug fix — font skew-x= / skew-y= not applied
- File: `imagegen/rendering/primitives/font_renderer.py`
- Action: Updated
- Details: Added `_render_skewed()` — renders text to temp RGBA surface, applies PIL affine shear, optionally rotates, composites at pos. Branch order: skew → `_render_skewed`; rotate-only → `_render_rotated`; neither → direct draw.

### 2026-05-07 18:08:03 — Bug fix — square skew-x= / skew-y= not applied
- File: `imagegen/rendering/primitives/square_renderer.py`
- Action: Updated
- Details: Added `_apply_skew()` helper (PIL affine shear) and a skew branch in `render()`. Non-zero skew draws the rectangle on an isolated `(w, h)` surface then composites the affine-transformed result at `(x, y)`. Zero skew uses the existing fast path unchanged.

### 2026-05-07 18:00:38 — Bug fix — font rotate= parameter not applied
- File: `imagegen/rendering/primitives/font_renderer.py`
- Action: Updated
- Details: Added `rotate` param extraction and `_render_rotated()` method. Text is rendered to a temp RGBA surface, rotated with `expand=True` (DSL clockwise → PIL negated), then composited back centered on `pos`. Zero-rotation uses the existing fast path unchanged.

### 2026-05-07 17:39:06 — Bug fix — font scale= parameter not applied
- File: `imagegen/rendering/primitives/font_renderer.py`
- Action: Updated
- Details: `FontRenderer.render()` now reads the `scale` param and computes `effective_font_size = max(1, int(font_size * scale))` before resolving the font and drawing text. Previously the `scale=` value on `font()` DSL commands was silently ignored.


