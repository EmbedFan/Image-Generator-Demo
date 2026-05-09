# 77_grid_visible.dsl
# Category 15 — Grid System
# Demonstrates: visible grid overlay with render=true.
# Shows three grid configurations on the same canvas using different
# step sizes, colors, and line-types.

begin_frame grid_visible
  image width=620px; height=340px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 15: Visible Grid Overlay (render=true)",
       pos=(15, 18));

  # ── Left panel: 50px solid gray grid ─────────────────────────────────
  square(color=#BDC3C7, fill=#F8F9FA, pos=(15, 40), width=180px, height=180px);
  # The grid is rendered ON TOP of all other primitives when render=true
  grid(step-x=30px, step-y=30px,
       offset-x=15, offset-y=40,
       render=true,
       color=RGB(180,180,180),
       line-type=solid, line-width=1px);
  font(color=#2C3E50, font-size=11px, align=center,
       text="step=30px, solid, gray", pos=(105, 232));

  # ── Center panel: 40px dashed blue grid ──────────────────────────────
  square(color=#BDC3C7, fill=#EBF5FB, pos=(220, 40), width=180px, height=180px);
  grid(step-x=40px, step-y=40px,
       offset-x=220, offset-y=40,
       render=true,
       color=RGB(52,152,219),
       line-type=dashed, line-width=1px);
  font(color=#2980B9, font-size=11px, align=center,
       text="step=40px, dashed, blue", pos=(310, 232));

  # ── Right panel: 25px dotted green grid ──────────────────────────────
  square(color=#BDC3C7, fill=#EAFAF1, pos=(425, 40), width=180px, height=180px);
  grid(step-x=25px, step-y=25px,
       offset-x=425, offset-y=40,
       render=true,
       color=RGB(39,174,96),
       line-type=dotted, line-width=1px);
  font(color=#27AE60, font-size=11px, align=center,
       text="step=25px, dotted, green", pos=(515, 232));

  # ── Shapes drawn on top of the grids to show overlay order ───────────
  circle(color=#E74C3C, fill=RGBA(231,76,60,0.5),
         center=(105, 130), radius=35);
  circle(color=#2980B9, fill=RGBA(52,152,219,0.5),
         center=(310, 130), radius=35);
  circle(color=#27AE60, fill=RGBA(39,174,96,0.5),
         center=(515, 130), radius=35);

  font(color=#7F8C8D, font-size=11px,
       text="Grid lines render on top of all other primitives when render=true.",
       pos=(15, 260));
  font(color=#7F8C8D, font-size=11px,
       text="Use offset-x / offset-y to shift the grid origin from (0,0).",
       pos=(15, 277));
  font(color=#7F8C8D, font-size=11px,
       text="line-type accepts: solid  |  dashed  |  dotted  |  dash-dot",
       pos=(15, 294));
end_frame
