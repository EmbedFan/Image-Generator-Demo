# 03_simple_square.dsl
# Category 1 - Basic Primitives
# Demonstrates: square primitive (draws rectangles) — fills, borders, line styles, and percentage sizing

begin_frame simple_square
  image width=640px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F5F5F5);

  # --- Section header ---
  font(font-family="Arial", font-size=15px, color=black, weight=bold,
       text="Filled rectangles", pos=(20, 25));

  # Solid fill, black border
  square(color=black, fill=lightblue, pos=(20, 40), width=160px, height=80px);

  # Solid fill, colored border, thick line
  square(color=navy, fill=gold, pos=(210, 40), width=160px, height=80px, line-width=4px);

  # Fill only — transparent stroke (no visible border)
  square(color=transparent, fill=tomato, pos=(400, 40), width=160px, height=80px);

  # --- Section header ---
  font(font-family="Arial", font-size=15px, color=black, weight=bold,
       text="Stroke-only (fill=none)", pos=(20, 155));

  # Thin solid outline
  square(color=black, fill=none, pos=(20, 170), width=160px, height=80px, line-width=1px);

  # Dashed outline
  square(color=blue, fill=none, pos=(210, 170), width=160px, height=80px,
         line-width=2px, line-type=dashed);

  # Dotted outline, heavier width
  square(color=red, fill=none, pos=(400, 170), width=160px, height=80px,
         line-width=3px, line-type=dotted);

  # --- Section header ---
  font(font-family="Arial", font-size=15px, color=black, weight=bold,
       text="Various sizes and proportions", pos=(20, 285));

  # Thin tall rectangle
  square(color=purple, fill=RGBA(128,0,128,0.3), pos=(20, 300), width=60px, height=80px);

  # Wide short rectangle
  square(color=green, fill=RGBA(0,180,0,0.3), pos=(110, 300), width=200px, height=40px,
         line-width=2px);

  # Square (equal sides)
  square(color=orange, fill=RGBA(255,165,0,0.4), pos=(340, 300), width=80px, height=80px,
         line-width=2px);

  # Dash-dot border
  square(color=darkgray, fill=none, pos=(450, 300), width=160px, height=80px,
         line-width=2px, line-type=dash-dot);

end_frame
