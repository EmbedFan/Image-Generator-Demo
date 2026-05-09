# 78_grid_global_align.dsl
# Category 15 — Grid System
# Demonstrates: global snapping with align=true.
# Elements with slightly off-grid coordinates are automatically snapped
# to the nearest grid intersection before rendering.

begin_frame grid_global_align
  image width=620px; height=340px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#FAFAFA);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 15: Global Grid Alignment (align=true)",
       pos=(15, 18));

  # ── Left panel: WITHOUT grid alignment ───────────────────────────────
  square(color=#BDC3C7, fill=white, pos=(15, 45), width=270px, height=230px);
  font(color=#E74C3C, font-size=12px, weight=bold,
       text="Without align=true", pos=(25, 60));
  font(color=#7F8C8D, font-size=10px,
       text="Shapes stay at exact coordinates", pos=(25, 75));

  # Elements drawn at odd, non-grid coordinates — no snapping
  circle(color=#3498DB, fill=#85C1E9, center=(78, 138), radius=28);
  font(color=#2C3E50, font-size=9px, align=center,
       text="(78,138)", pos=(78, 180));

  square(color=#E74C3C, fill=#F1948A,
         pos=(133, 112), width=60px, height=55px);
  font(color=#2C3E50, font-size=9px, align=center,
       text="(133,112)", pos=(163, 180));

  circle(color=#27AE60, fill=#82E0AA, center=(240, 148), radius=20);
  font(color=#2C3E50, font-size=9px, align=center,
       text="(240,148)", pos=(240, 180));

  # ── Right panel: WITH global align=true on 50px grid ─────────────────
  square(color=#BDC3C7, fill=white, pos=(335, 45), width=270px, height=230px);
  font(color=#27AE60, font-size=12px, weight=bold,
       text="With align=true (50px grid)", pos=(345, 60));
  font(color=#7F8C8D, font-size=10px,
       text="All elements snapped to nearest intersection", pos=(345, 75));

  # Grid with align=true — all subsequent primitives are snapped
  grid(step-x=50px, step-y=50px,
       offset-x=335, offset-y=45,
       render=true,
       color=RGB(200,230,200), line-type=dashed, line-width=1px,
       align=true);

  # Same off-grid coordinates — engine snaps them to 50px intersections
  # (78→50, 138→150, center snapped to nearest 50px from offset)
  circle(color=#3498DB, fill=#85C1E9, center=(390, 145), radius=28);
  font(color=#2C3E50, font-size=9px, align=center,
       text="(390,145)→snapped", pos=(390, 190));

  square(color=#E74C3C, fill=#F1948A,
         pos=(450, 95), width=60px, height=55px);
  font(color=#2C3E50, font-size=9px, align=center,
       text="(450,95)→snapped", pos=(480, 190));

  circle(color=#27AE60, fill=#82E0AA, center=(565, 145), radius=20);
  font(color=#2C3E50, font-size=9px, align=center,
       text="(565,145)→snapped", pos=(565, 190));

  font(color=#7F8C8D, font-size=11px,
       text="align=true snaps ALL primitives in the frame to the nearest grid intersection.",
       pos=(15, 309), align=false);
  font(color=#7F8C8D, font-size=11px,
       text="Snapping applies before any transforms (scale, skew, rotate).",
       pos=(15, 290));
end_frame
