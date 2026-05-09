# 71_vars_basic.dsl
# Category 14 — Variables and Layout Chaining
# Demonstrates: var declarations, numeric assignment, and using variables
# in primitive parameters (pos, width, height, radius).
# Variables eliminate hard-coded numbers and allow formula-driven layouts.

begin_frame vars_basic
  image width=520px; height=320px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F0F4F8);

  # --- Declare layout variables ---
  var margin, box_w, box_h, gap;
  margin = 30;
  box_w  = 120;
  box_h  = 55;
  gap    = 12;

  # Use variables in pos= and width=/height= parameters
  square(color=#2C3E50, fill=#3498DB,
         pos=(margin, margin),
         width=box_w, height=box_h);

  square(color=#2C3E50, fill=#2ECC71,
         pos=(margin, margin + box_h + gap),
         width=box_w, height=box_h);

  square(color=#2C3E50, fill=#E74C3C,
         pos=(margin, margin + (box_h + gap) * 2),
         width=box_w, height=box_h);

  # Static labels on each box
  font(color=white, font-size=12px, weight=bold, align=center,
       text="Box A",
       pos=(margin + box_w / 2, margin + box_h / 2 + 4));
  font(color=white, font-size=12px, weight=bold, align=center,
       text="Box B",
       pos=(margin + box_w / 2, margin + box_h + gap + box_h / 2 + 4));
  font(color=white, font-size=12px, weight=bold, align=center,
       text="Box C",
       pos=(margin + box_w / 2, margin + (box_h + gap) * 2 + box_h / 2 + 4));

  # Variable arithmetic for radius — half of box height
  var r, cx, cy;
  r  = box_h / 2;
  cx = margin + box_w + gap * 3 + r;
  cy = margin + r;

  # Circle whose radius is computed from box_h
  circle(color=#8E44AD, fill=#9B59B6, center=(cx, cy), radius=r);
  font(color=white, font-size=11px, align=center,
       text="r = box_h/2", pos=(cx, cy + 4));

  # Second circle: r scaled by 1.5 using multiplication
  var r2;
  r2 = r * 1;
  circle(color=#16A085, fill=none, line-width=2px,
         center=(cx, cy + r + gap + r2),
         radius=r2);
  font(color=#16A085, font-size=11px, align=center,
       text="stroke only", pos=(cx, cy + r + gap + r2 + 4));

  # Annotation block on the right
  font(color=#7F8C8D, font-size=11px,
       text="var margin = 30;",   pos=(margin + box_w + gap * 3 + r * 2 + 10, margin + 10));
  font(color=#7F8C8D, font-size=11px,
       text="var box_w  = 120;",  pos=(margin + box_w + gap * 3 + r * 2 + 10, margin + 25));
  font(color=#7F8C8D, font-size=11px,
       text="var box_h  = 55;",   pos=(margin + box_w + gap * 3 + r * 2 + 10, margin + 40));
  font(color=#7F8C8D, font-size=11px,
       text="var gap    = 12;",   pos=(margin + box_w + gap * 3 + r * 2 + 10, margin + 55));

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 14: Variables — Declarations and Arithmetic",
       pos=(30, 295));
end_frame
