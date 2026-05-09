# 81_grid_multiple.dsl
# Category 15 — Grid System
# Demonstrates: multiple grid() statements in one frame.
# Each grid() replaces the active grid for commands that follow it.
# Fine grid at the top, coarse grid at the bottom — same canvas.

begin_frame grid_multiple
  image width=620px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 15: Multiple grid() Statements per Frame",
       pos=(15, 18));

  # ── Divider between regions ──────────────────────────────────────────
  line(color=#BDC3C7, line-type=solid, line-width=1px,
       start=(0, 195), end=(620, 195));
  font(color=#3498DB, font-size=11px,
       text="--- Fine 20px grid region (top) ---",
       pos=(200, 40));
  font(color=#E67E22, font-size=11px,
       text="--- Coarse 100px grid region (bottom) ---",
       pos=(170, 220));

  # ── FIRST grid: fine 20px, for top region ─────────────────────────────
  # Applies to all drawing commands until the next grid() call
  grid(step-x=20px, step-y=20px, align=true,
       render=true, color=RGB(200,220,255), line-type=dotted, line-width=1px);

  # These shapes snap to the 20px fine grid
  circle(color=#3498DB, fill=#85C1E9, center=(63, 118), radius=28);
  font(color=#2C3E50, font-size=10px, align=center,
       text="20px snap", pos=(63, 162));

  square(color=#3498DB, fill=RGBA(52,152,219,0.3),
         pos=(145, 88), width=55px, height=55px);
  font(color=#2C3E50, font-size=10px, align=center,
       text="20px snap", pos=(172, 155));

  circle(color=#9B59B6, fill=#C39BD3, center=(268, 108), radius=22);
  font(color=#2C3E50, font-size=10px, align=center,
       text="20px snap", pos=(268, 144));

  square(color=#9B59B6, fill=RGBA(155,89,182,0.3),
         pos=(332, 92), width=45px, height=45px);
  font(color=#2C3E50, font-size=10px, align=center,
       text="20px snap", pos=(354, 150));

  # ── SECOND grid: coarse 100px, for bottom region ─────────────────────
  # This grid() call replaces the first grid — all subsequent commands
  # snap to the 100px coarse grid instead
  grid(step-x=100px, step-y=100px, align=true,
       render=true, color=RGB(255,220,180), line-type=dashed, line-width=1px);

  # These shapes snap to the 100px coarse grid
  circle(color=#E67E22, fill=#FAD7A0, center=(63, 298), radius=38);
  font(color=#2C3E50, font-size=10px, align=center,
       text="100px snap", pos=(63, 350));

  square(color=#E67E22, fill=RGBA(230,126,34,0.25),
         pos=(155, 255), width=80px, height=80px);
  font(color=#2C3E50, font-size=10px, align=center,
       text="100px snap", pos=(195, 350));

  circle(color=#C0392B, fill=#F1948A, center=(388, 298), radius=28);
  font(color=#2C3E50, font-size=10px, align=center,
       text="100px snap", pos=(388, 350));

  square(color=#C0392B, fill=RGBA(192,57,43,0.25),
         pos=(448, 260), width=75px, height=70px);
  font(color=#2C3E50, font-size=10px, align=center,
       text="100px snap", pos=(485, 350));

  font(color=#7F8C8D, font-size=11px,
       text="Each grid() replaces the active grid for commands that follow it.",
       pos=(15, 378));
end_frame
