# 74_vars_arithmetic.dsl
# Category 14 — Variables and Layout Chaining
# Demonstrates: all four arithmetic operators (+, -, *, /) on variables and
# .bbox values. Shows computed positions, scaled sizes, and inset rectangles.

begin_frame vars_arithmetic
  image width=600px; height=340px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F8F9FA);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 14: Variables — Arithmetic Operators",
       pos=(20, 22));

  # ── Left column: + and * demos ─────────────────────────────────────────
  var unit, base_x, base_y;
  unit   = 50;
  base_x = 30;
  base_y = 50;

  # Addition — shift right by unit
  square(color=#2980B9, fill=#3498DB,
         pos=(base_x, base_y), width=unit, height=unit);
  font(color=black, font-size=10px, text="base_x",
       pos=(base_x, base_y + unit + 12));

  square(color=#27AE60, fill=#2ECC71,
         pos=(base_x + unit + 10, base_y), width=unit, height=unit);
  font(color=black, font-size=10px, text="base_x + unit + 10",
       pos=(base_x + unit + 10, base_y + unit + 12));

  # Multiplication — double width
  var wide_w, wide_h;
  wide_w = unit * 2;
  wide_h = unit;
  square(color=#8E44AD, fill=#9B59B6,
         pos=(base_x, base_y + unit + 30), width=wide_w, height=wide_h);
  font(color=white, font-size=11px, align=center,
       text="unit * 2",
       pos=(base_x + wide_w / 2, base_y + unit + 30 + wide_h / 2 + 4));

  # Division — radius = unit / 2
  var r, cx, cy;
  r  = unit / 2;
  cx = base_x + r;
  cy = base_y + unit + 30 + wide_h + 30 + r;
  circle(color=#C0392B, fill=#E74C3C, center=(cx, cy), radius=r);
  font(color=white, font-size=11px, align=center,
       text="unit/2",
       pos=(cx, cy + 4));

  # ── Right column: subtraction (inset) using bbox ───────────────────────
  ref = square(color=#16A085, fill=#1ABC9C,
               pos=(280, 50), width=220px, height=170px);
  var rx, ry, rw, rh, inset;
  rx    = ref.bbox.x;
  ry    = ref.bbox.y;
  rw    = ref.bbox.width;
  rh    = ref.bbox.height;
  inset = 18;

  # Inner rectangle: pos shifted +inset, size shrunk by inset*2 on each axis
  square(color=white, fill=RGBA(255,255,255,0.35),
         pos=(rx + inset, ry + inset),
         width=rw - inset * 2, height=rh - inset * 2);
  font(color=white, font-size=12px, align=center,
       text="rw - inset*2",
       pos=(rx + rw / 2, ry + rh / 2 - 6));
  font(color=white, font-size=12px, align=center,
       text="rh - inset*2",
       pos=(rx + rw / 2, ry + rh / 2 + 10));

  # Inset dimension annotations
  line(color=white, line-type=dashed, line-width=1px,
       start=(rx, ry + rh + 20), end=(rx + inset, ry + rh + 20));
  font(color=white, font-size=10px, text="inset=18",
       pos=(rx + 2, ry + rh + 32));

  # ── Bottom: division to center a circle on the right block ────────────
  var mid_x, mid_y;
  mid_x = rx + rw / 2;
  mid_y = ry + rh + 50;
  circle(color=#8E44AD, fill=#9B59B6,
         center=(mid_x, mid_y), radius=22);
  font(color=white, font-size=11px, align=center,
       text="rw/2",
       pos=(mid_x, mid_y + 4));
  font(color=#2C3E50, font-size=11px,
       text="center=(rx + rw/2, ...)",
       pos=(rx, ry + rh + 82));

  font(color=#7F8C8D, font-size=11px,
       text="Operators: + - * /   |   Grouped with ( )",
       pos=(20, 315));
end_frame
