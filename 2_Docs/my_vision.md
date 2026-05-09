# Vision for Technical Image Generator app

Act as a professional software architect.

## GOAL
Creating a software tool which gets a script that describes a technical image and outputs the described image.
The image description script is a pure language only for defining complex image objects using basic image objects such as line, paths, polygon, circle, pie, arcs, connectors.
The added value of the software is that, it can generate animated GIFs. 

## User requirements
 - The implementation language is Python.
 - The software main aim is to generate an image. The image can be: png, jpeg, gif
 - The language of the image description:
   - every image is a frame, a begin_frame and an end_frame, if more frames exist the output image can be one GIF image or more images with image frame ID in their name.
   - colorspace can be RGB, RGBA, GRAY
   - when more frames exist, specify by frame:
     - hold-time (millisec) {the frame is shown before next frame drawn}
     - frame-mode: one-run, cyclic-run
   - inside the frame there are the image description commands.
     - image width, height, colorspace, dpi
     - background (color=color) {simple colored background}
     - background (color1=color, color2=color, start=(x1,y1), end=(x2,y2)) {gradient/fade: start color at start point, ends at end point with color2; linear interpolation between points}
     - background (src=path, mode=fit|stretch|clip, x=xpos, y=ypos, width=w, height=h) {image background: src is path to PNG/JPEG/GIF/SVG; mode controls sizing (fit=fit to width/height, stretch=fill container, clip=use partial image); x,y,width,height define clip region for clip mode; opacity parameter supported (0-1)}
     - line-type values: solid, dashed, dotted, dash-dot (used by all shapes with stroke)
     - color format: RGB(r,g,b), RGBA(r,g,b,a), hex (#RRGGBB), or named colors (e.g., black, white, red, blue, green, etc.)
     - named color palettes: reusable color aliases declared at script level using `begin_palette <name>` … `end_palette`; each entry: `<alias> = <color_value>` (any valid color format); palette entries referenced in any color parameter as `@<alias>` (e.g., `color=@primary`, `fill=@accent`); multiple palettes allowed per script; aliases from all palettes and included files share a single global namespace; alias name collisions (local or included) are a parse error; referencing an undefined alias is a parse error
     - unit measurements: px (pixels), pt (points), em (relative to font size), cm (centimeters), mm (millimeters), % (percentage of parent container width for x-coordinates, height for y-coordinates; e.g., pos=(50%,50%) = center of parent)
     - border attributes: style (solid, dashed, dotted, dash-dot), color (any valid color format), width (numeric value with units), shadow (offset-x offset-y blur-radius color)
     - statement delimiters inside objects: each primitive/attribute on new line or semicolon-separated on same line; can mix both styles (newline ends statement, semicolon also ends statement); whitespace (newlines, spaces, tabs) ignored except as statement terminators
     - z-order (layering): primitives are rendered in the order they appear in the object definition; first primitive drawn = lowest layer, last primitive drawn = highest layer (on top); use z-index parameter (0-1000) to override default order if needed
     - coordinate system: (0,0) is at top-left corner; x increases rightward, y increases downward
     - coordinate units: same as unit measurements (px, pt, em, cm, mm, %); if no unit specified, defaults to px
     - transformations (optional parameters on any drawable primitive or object): rotate=degrees (0-360), skew-x=degrees, skew-y=degrees, scale=multiplier (1.0=normal, 0.5=half, 2.0=double); transformations applied around object center (pos or center); multiple transforms compose as: translate→scale→skew→rotate
     - grid system (optional, defined at frame level): provides a logical layout structure for precise object placement and alignment
       - grid(step-x=<value>, step-y=<value>[, offset-x=<value>, offset-y=<value>]) — defines horizontal and vertical grid spacing; non-visual by default
       - render=true|false (default false): when true, grid lines are drawn over the canvas after all other primitives for design/debugging purposes; visual style: color=<color>, line-type=<type>, line-width=<value>
       - align=true|false (default false): when true, snap-to-grid is applied globally to all drawable elements in the frame
       - per-element snap: snap=grid-intersection|grid-x|grid-y|none on any primitive or object; snaps to nearest grid point or line; snap=none overrides global align=true for that element; omitting snap inherits global align setting
       - alignment is resolved before applying transforms (position → scale → skew → rotate), consistent with the existing rendering pipeline
       - the grid operates as an auxiliary coordinate system layered on top of the canvas coordinate system without modifying it
       - if no grid is defined, or neither render=true nor alignment is requested, all existing behavior is unchanged (fully backward compatible)
     - bounding box overlay (optional debug/diagnostic parameter on any drawable primitive or object instance):
       - show-bbox=true|false (default false); when true, the engine renders the axis-aligned bounding box of the element as a visual overlay
       - the bbox represents the final transformed geometry — it encloses the element after all transforms (scale, skew, rotate) have been applied
       - the bbox is drawn as an overlay on top of the element; it does not affect layout, z-ordering, or clipping of any element
       - bbox color is automatically computed for maximum contrast against the canvas background (inverted luminance of the background region); no manual color setting is supported
       - the bbox line style is dashed by default (1px, non-configurable) to distinguish it from normal drawn primitives
       - accepted on all drawable entities: all primitives, connectors, font/text elements, image primitives, and object instances; not accepted on non-drawable constructs (parse error)
       - disabled by default; all existing scripts without show-bbox produce identical output (fully backward compatible)
     - image primitives
       - line (color=color, line-type=type, line-width=width, start=(x1,y1), end=(x2,y2)) {stroke only, no fill}
       - circle (color=color, line-type=type, line-width=width, fill=fill-color, center=(xc,yc), radius=r) {can have both stroke and fill}
       - square (color=color, line-type=type, line-width=width, fill=fill-color, pos=(x1,y1), width=w, height=h) {can have both stroke and fill}
       - polygon (color=color, line-type=type, line-width=width, fill=fill-color, points=[(x1,y1), (x2,y2), ..., (xn,yn)]) where points list is comma-separated and closed automatically {can have both stroke and fill}
       - path (color=color, line-type=type, line-width=width, points=[(x1,y1), (x2,y2), (x3,y3), ...]) where points list is comma-separated, open curve (not closed) {stroke only, no fill}
       - pie (color=color, line-type=type, line-width=width, fill=fill-color, center=(xc,yc), radius=r, start-angle=degrees, end-angle=degrees) {can have both stroke and fill}
       - arc (color=color, line-type=type, line-width=width, center=(xc,yc), radius=r, start-angle=degrees, end-angle=degrees) {open curved arc — no lines to center, no fill; stroke only}
       - connector (color=color, line-width=width, line-type=solid|dashed|dotted|dash-dot, points=[(x1,y1), (x2,y2), ..., (xn,yn)], connector-type=straight|curved|step, start-cap=cap-type, end-cap=cap-type, cap-size=small|medium|large, corner=sharp|rounded|beveled, corner-radius=r, label=text, label-font-family=name, label-font-size=size, label-font-color=color, label-font-style=normal|italic, label-font-weight=normal|bold, label-pos=start|center|end, label-offset=(dx,dy), animated=true|false, pattern=dash|dot|arrow|zigzag, pattern-length=n, pattern-gap=n, pattern-speed=n, pattern-color=color)
         - `points`: ordered list of two or more (x,y) vertices; two points = single-segment; three or more points = multi-segment connector; shorthand `start=(x1,y1), end=(x2,y2)` still accepted for two-point connectors
         - `connector-type`: straight = straight line segments between points; curved = smooth spline through points; step = axis-aligned segments (like a right-angle routing); default=straight
         - `start-cap` / `end-cap`: shape drawn at the first / last point; options: none|triangle|open-triangle|circle|filled-circle|diamond|filled-diamond|square|filled-square; default=none; `start-arrow`/`end-arrow` accepted as aliases for backward compatibility
         - `cap-size`: small|medium|large (default=medium); controls cap dimensions proportional to line-width; individual overrides `start-cap-size` and `end-cap-size` also supported
         - `corner`: style applied at every intermediate vertex of a multi-segment connector; sharp = exact vertex point; rounded = circular arc tangent to both segments; beveled = straight cut across the corner; default=sharp; `corner-radius` sets arc radius for rounded (default=5px)
         - `label` / label font properties: optional text drawn along the connector; `label-pos` controls placement: start (near first point), center (midpoint of connector), end (near last point); `label-offset=(dx,dy)` shifts the label relative to its anchor; font properties match the `font` primitive (font-family, font-size, font-color, font-style, font-weight)
         - `animated`: when true the connector line is drawn with a moving pattern across frames (requires multi-frame GIF output); default=false
         - `pattern`: the repeating unit drawn instead of a plain line; dash = filled dash; dot = filled dot; arrow = small arrow chevron indicating direction; zigzag = zigzag stroke; default=dash
         - `pattern-length`: length of one pattern unit in px; default=8px
         - `pattern-gap`: gap between pattern units in px; default=4px
         - `pattern-color`: color of the pattern units; defaults to connector `color`
         - `pattern-speed`: number of pixels the pattern advances per frame; creates a rolling/flowing animation in multi-frame output; default=4px; direction follows the connector from start to end
         - {stroke only, no fill}
       - font (font-family=name, font-size=size, color=color, style=normal|italic, weight=normal|bold, text=string, pos=(x,y)) where font-family supports fallback chain: "Arial, Helvetica, sans-serif" tries Arial first, then Helvetica, then system default sans-serif; system default fonts available: serif (Times New Roman/Linux Libertine), sans-serif (Arial/DejaVu Sans), monospace (Courier/DejaVu Mono); if font not available, fallback chain is used; if no fallback matches, uses system monospace as final fallback
       - image (src=path, pos=(x,y), width=w, height=h, opacity=0-1) where src is relative or absolute path to PNG/JPEG/GIF/SVG file; width/height scales image (if both specified, aspect ratio ignored; if only one specified, other auto-scales); opacity=0 transparent, opacity=1 opaque (default); supports rotation/skew/scale transforms like other primitives
     - Using image primitives, complex objects can be defined, the definition starts at begin_obj and ends at end_obj.
       - Base attributes width, height, background
       - border style, color, width, shadow
       - clipping and masking: clip-bounds=(x1,y1,x2,y2) defines rectangular clipping region for all contents of object (anything outside bounds not rendered); clip-shape=shape_name uses predefined shape (circle, square, polygon) as clipping mask (only inside mask shape rendered); objects can have clip-bounds and/or clip-shape to combine rectangular and shape-based clipping
       - nested objects: objects can contain other objects; nested objects use local coordinate system relative to parent object; nested objects inherit parent's properties unless overridden
         example script (single frame/static image with object definition and reuse):
         '''
         begin_frame static_frame
         image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
         background(color=white);
         
         begin_obj card
         width: 400px; height: 150px; background: RGB(123,222,45);
         border: solid 2px black;
         circle(color=black, line-type=solid, line-width=1px, fill=white, center=(50,50), radius=30);
         line(color=black, line-type=solid, line-width=2px, start=(20,20), end=(100,100));
         font(font-family=Arial, font-size=16px, color=black, style=normal, weight=bold, text="Sample Text", pos=(50,130));
         end_obj
         
         card(pos=(100,100));
         card(pos=(300,100), background=RGB(100,150,200));
         end_frame
         '''
         
         example script (multi-frame animated GIF):
         '''
         begin_frame frame_0
         image width=500px; height=300px; colorspace=RGB; dpi=96;
         hold-time=500; frame-mode=cyclic-run;
         background(color=white);
         circle(color=red, line-type=solid, line-width=2px, fill=yellow, center=(100,150), radius=50);
         end_frame
         
         begin_frame frame_1
         image width=500px; height=300px; colorspace=RGB; dpi=96;
         hold-time=500; frame-mode=cyclic-run;
         background(color=white);
         circle(color=blue, line-type=solid, line-width=2px, fill=cyan, center=(150,150), radius=50);
         end_frame
         
         begin_frame frame_2
         image width=500px; height=300px; colorspace=RGB; dpi=96;
         hold-time=500; frame-mode=cyclic-run;
         background(color=white);
         circle(color=green, line-type=solid, line-width=2px, fill=lime, center=(200,150), radius=50);
         end_frame
         '''
         
         example script (function declarations and usage):
         '''
         begin_func button(x, y, width, height, label, bg_color)
         square(pos=(x,y), width=width, height=height, background=bg_color, color=black, line-width=1px);
         font(font-family=Arial, font-size=12px, color=black, text=label, pos=(x+5,y+5));
         end_func
         
         begin_func labeled_circle(cx, cy, rad, label)
         circle(center=(cx,cy), radius=rad, color=black, line-width=2px, fill=lightblue);
         font(font-family=Arial, font-size=10px, color=black, text=label, pos=(cx-15,cy-5));
         end_func
         
         begin_frame ui_demo
         image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
         background(color=white);
         
         button(50, 50, 100, 30, "OK", gray);
         button(200, 50, 100, 30, "Cancel", lightgray);
         labeled_circle(100, 150, 40, "Node1");
         labeled_circle(300, 150, 40, "Node2");
         connector(start=(140,150), end=(260,150), color=black, connector-type=straight, end-arrow=triangle);
         end_frame
         '''
         
         example script (script inclusion):
         
         file: ui_components.dsl
         '''
         begin_func button(x, y, label)
         square(pos=(x,y), width=80, height=30, background=gray, color=black, line-width=1px);
         font(font-family=Arial, font-size=12px, color=white, text=label, pos=(x+5,y+7));
         end_func
         
         begin_func checkbox(x, y, label)
         square(pos=(x,y), width=20, height=20, background=white, color=black, line-width=1px);
         font(font-family=Arial, font-size=12px, color=black, text=label, pos=(x+25,y+3));
         end_func
         '''
         
         file: main_dialog.dsl
         '''
         include "ui_components.dsl"
         
         begin_frame dialog_frame
         image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
         background(color=RGB(240,240,240));
         
         square(pos=(10,10), width=380, height=280, color=black, line-width=2px, fill=white);
         font(font-family=Arial, font-size=16px, color=black, weight=bold, text="Settings", pos=(20,20));
         
         checkbox(30, 60, "Enable notifications");
         checkbox(30, 100, "Auto-save");
         checkbox(30, 140, "Dark mode");
         
         button(150, 240, "OK");
         button(250, 240, "Cancel");
         end_frame
         '''
     - **String handling and escaping:**
       - Strings enclosed in double quotes: `text="Sample Text"`
       - Escape sequences: `\"` for quotes, `\\` for backslash, `\n` for newline, `\t` for tab
       - Unicode characters supported (UTF-8 encoding)
       - Example: `text="Line 1\nLine 2"` produces multi-line text
     - **Optional vs required parameters:**
       - Required: color, line-type, line-width, center/pos/start/end, radius/width/height
       - Optional with defaults: fill=none (transparent), z-index=declaration-order, style=normal, weight=normal
       - Optional parameters can be omitted; order doesn't matter for named params
     - **Type validation and error handling:**
       - color: must be valid RGB/RGBA/hex/named format; invalid format = error halts parsing
       - numeric values (radius, width, angle): must be positive numbers; negative = error or warning
       - line-type: must be one of [solid|dashed|dotted|dash-dot]; invalid type = error
       - points list: minimum 2 points for path, minimum 3 for polygon; insufficient points = error
       - coordinates: must be within image bounds or offscreen (no error, just clipped to bounds)
     - **Basic Grammar (key constructs):**
       - `<script> := <top-level-stmt>+`
       - `<top-level-stmt> := <frame> | <func-decl> | <obj-template> | <include-stmt> | <palette-def>`
       - `<palette-def> := 'begin_palette' <name> <color-entry>+ 'end_palette'`
       - `<color-entry> := <name> '=' <color-value>`
       - `<frame> := 'begin_frame' <name> <image-def> <drawing-commands> 'end_frame'`
       - `<image-def> := 'image' <key>=<value> (';' <key>=<value>)*`
       - `<drawing-commands> := (<primitive> | <object>)+`
       - `<primitive> := <prim-type> '(' <param-list> ')'`
       - `<param-list> := <name>=<value> (',' <name>=<value>)*`
       - `<object> := 'begin_obj' <name> <attributes> <drawing-commands> 'end_obj'`
     - **Output format specification:**
       - Single frame: image is output as PNG, JPEG, or GIF based on file extension in output filename
       - Multiple frames: output as GIF (animated) by default; use `output-format=gif|images` in image-def
       - `output-format=images`: outputs separate PNG/JPEG files named `<frame-id>.png` or `<frame-id>.jpeg`
       - `output-format=gif`: outputs single animated GIF file with frame timings from hold-time
       - Example: `image width=500px; height=300px; output-format=gif;` creates animated GIF
     - **Object instantiation and reuse:**
       - Objects defined with `begin_obj <name>` are templates; to use in frames, reference with `<name>(pos=(x,y))`
       - Instance parameters override template defaults: `card(pos=(100,100), background=blue)` overrides card's background
       - Example: `card()` uses all defaults; `card(pos=(200,200))` places at new position with other defaults inherited
       - Optional `width=<value>` and `height=<value>` parameters override the template box dimensions at call time: `card(pos=(100,100), width=300px, height=80px)`
       - Optional `scale=<multiplier>` applies uniform scaling to template dimensions: `card(pos=(100,100), scale=1.6)` renders at 1.6× its template size
       - When both `width`/`height` and `scale` are provided, explicit `width`/`height` takes precedence; a warning is emitted
       - The current `width`/`height` behavior remains the default object-instance sizing mode, meaning size overrides continue to proportionally scale internal geometry for backward compatibility
       - An additional opt-in layout-resize mode is available on object instances through `resize-mode=layout` so `width` and `height` can redefine the instance bounding box without implicitly scaling internal geometry
       - In layout-resize mode, child primitives and nested objects may reflow or reposition from object-local `width`, `height`, and bbox-driven expressions, enabling responsive UI-like objects whose borders stretch while fixed-size content such as icons remains unchanged
       - In layout-resize mode, `scale=<multiplier>` remains the explicit way to request geometric scaling and may be combined with `width` and `height`
       - Optional `rotate=<degrees>` parameter rotates the object clockwise around its center following existing transform rules: `card(pos=(100,100), rotate=45)`
       - All size and rotation parameters are optional and backward compatible; omitting them uses template defaults with no rotation
     - **Function declarations:**
       - Functions encapsulate reusable rendering logic with parameters
       - Syntax: `begin_func <name>(<param1>, <param2>, ...) <drawing-commands> end_func`
       - Functions can draw primitives and instantiate objects with passed-in parameters
       - Function parameters are variables that can be used in expressions within function body (e.g., `pos=(param_x, param_y)`)
       - Functions are called within frames: `<function_name>(arg1, arg2, ...)`
       - Functions can call other functions and instantiate objects, enabling complex reusable components
       - Example function: `begin_func button(x, y, label) square(pos=(x,y), width=80, height=30, background=gray); font(pos=(x+10,y+8), text=label, color=black); end_func`
       - Example call: `button(100, 100, "Click Me")` renders button at (100,100) with text "Click Me"
     - **Script file inclusion:**
       - DSL scripts can include other DSL script files to modularize code and reuse function definitions
       - Syntax: `include "path/to/file.dsl"` or `include "path/to/file.dsl";`
       - Include paths can be relative (relative to current DSL file) or absolute
       - Included files can declare functions and objects that are available in the including script
       - No depth limit on includes; scripts can include other scripts recursively
       - Include processing: all function and object definitions from included file are added to current scope before parsing rest of script
       - Example structure:
         - `ui_components.dsl` - defines reusable functions: button, textbox, panel
         - `diagram.dsl` - includes "ui_components.dsl" and uses those functions
         - `main.dsl` - includes "diagram.dsl" and combines all components in frames
       - Circular includes are detected and rejected (including file that includes current file)
       - Example: `include "common_shapes.dsl"` loads button, checkbox, and other common UI shapes for use in current script
     - **Variable declarations and bounding box extraction:**
       - Variables can be declared inside a frame or function body: `var x;` or `var x, y, width;`
       - Variable names follow standard identifier rules (letters, digits, underscores; must not start with a digit)
       - Variables are scoped to the enclosing frame or function block; frame-scope and function-scope are separate namespaces
       - Reassignment is allowed: a variable can be assigned more than once within its scope
       - Every rendered drawable element exposes a read-only bounding box after it has been drawn:
         - `<name>.bbox.x` — left edge of the axis-aligned bounding box after all transforms
         - `<name>.bbox.y` — top edge of the axis-aligned bounding box after all transforms
         - `<name>.bbox.width` — width of the bounding box
         - `<name>.bbox.height` — height of the bounding box
       - The bounding box reflects the final rendered geometry after the full transform pipeline (scale, skew, rotate)
       - Assignment syntax: `varname = <object>.bbox.<property>;`
       - Variables can be used in any parameter expression: `square(pos=(x + width + 10, y), width=50, height=50);`
       - Accessing `.bbox` on an object before it has been rendered → runtime error
       - Using an undefined variable in an expression → parse or runtime error
       - Circular assignments (variable depends on itself through a chain) → runtime error
       - The execution model within a frame is sequential: render → compute bbox → store in variable → next statement may use variable
       - Example:
         ```
         begin_frame layout_demo
         image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;
         background(color=white);

         var bx, by, bw;

         square(color=black, line-width=1px, fill=lightblue, pos=(50,50), width=120, height=60);
         bx = square.bbox.x;
         by = square.bbox.y;
         bw = square.bbox.width;

         circle(center=(bx + bw + 60, by + 30), radius=30, color=black, line-width=1px, fill=lightyellow);
         end_frame
         ```
     - **Comparison expressions and bounded loops:**
       - Numeric comparison expressions are supported on top of arithmetic expressions: `==`, `!=`, `<`, `<=`, `>`, `>=`
       - Comparison expressions are intended for control-flow conditions such as `i < 5` or `current_x + width <= limit`
       - A minimal `do ... while` loop is supported for repeated drawing and layout logic
       - The loop executes the body first, then evaluates the condition after each iteration
       - `do ... while` is only allowed inside `begin_frame ... end_frame` and `begin_func ... end_func`
       - `do ... while` is not allowed at top level or inside `begin_obj` / `begin_palette`
       - Every loop is protected by a fixed maximum-iteration guard of 1000 iterations
       - Example:
         ```
         begin_frame loop_demo
         image width=400px; height=200px; colorspace=RGB; dpi=96; output-format=png;
         background(color=white);

         var i;
         i = 0;

         do
           circle(color=black, fill=blue, center=(50 + i * 40, 100), radius=12);
           i = i + 1;
         while i < 5;
         end_frame
         ```

## Changelog

### 2026-05-07 21:04:48 - FEA-008: comparison expressions and bounded `do ... while`

- Added numeric comparison-expression goals with operators `==`, `!=`, `<`, `<=`, `>`, `>=`
- Added a minimal `do ... while` loop concept for repeated drawing and layout logic
- Defined allowed scopes as frame and function bodies only
- Defined forbidden scopes as top-level, object-template, and palette bodies
- Added a fixed 1000-iteration runtime safety guard to the vision

### 2026-05-09 06:44:42 - FEA-009: decoupled object resizing and scaling behavior

- Clarified that current object-instance `width` and `height` semantics remain the default scaling behavior
- Added an opt-in layout-resize mode concept for object instances so bounding-box resizing can happen without implicit geometry scaling
- Stated that layout-resize mode should support responsive reflow using object-local dimensions while keeping explicit `scale` as the geometric scaling control
