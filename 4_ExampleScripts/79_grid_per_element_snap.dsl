# 79_grid_per_element_snap.dsl
# Category 15 — Grid System
# Demonstrates: per-element snap= parameter values on the same frame.
# Values: grid-intersection (snap both x and y), grid-x (snap x only),
# grid-y (snap y only), none (opt out even when global align=true is active).

begin_frame grid_per_element_snap
  image width=620px; height=360px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 15: Per-Element snap= Values",
       pos=(15, 18));

  # Define a 60px grid (non-visual)
  grid(step-x=60px, step-y=60px);

  # ── Row labels ────────────────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="snap=grid-intersection", pos=(15, 55));
  font(color=#7F8C8D, font-size=11px, text="snap=grid-x only",       pos=(15, 135));
  font(color=#7F8C8D, font-size=11px, text="snap=grid-y only",       pos=(15, 215));
  font(color=#7F8C8D, font-size=11px, text="snap=none (no snap)",    pos=(15, 295));

  # ── grid-intersection: snap both x and y ─────────────────────────────
  # Input: center=(83, 72) — nearest 60px intersection → (60, 60)
  circle(color=#3498DB, fill=#85C1E9, center=(83, 72), radius=22,
         snap=grid-intersection);
  font(color=#2C3E50, font-size=10px,
       text="in:(83,72) → snapped to (60,60)",
       pos=(220, 72));

  circle(color=#9B59B6, fill=#C39BD3, center=(205, 88), radius=22,
         snap=grid-intersection);
  font(color=#2C3E50, font-size=10px,
       text="in:(205,88) → snapped to (180,60)",
       pos=(380, 88));

  # ── grid-x: snap x only, y stays as given ────────────────────────────
  # center=(83, 148) → x snapped to 60, y stays 148
  circle(color=#E74C3C, fill=#F1948A, center=(83, 148), radius=22,
         snap=grid-x);
  font(color=#2C3E50, font-size=10px,
       text="in:(83,148) → x snapped: (60,148)",
       pos=(220, 148));

  circle(color=#E67E22, fill=#FAD7A0, center=(205, 140), radius=22,
         snap=grid-x);
  font(color=#2C3E50, font-size=10px,
       text="in:(205,140) → x snapped: (180,140)",
       pos=(380, 140));

  # ── grid-y: snap y only, x stays as given ────────────────────────────
  # center=(83, 228) → y snapped to 240, x stays 83
  circle(color=#27AE60, fill=#82E0AA, center=(83, 228), radius=22,
         snap=grid-y);
  font(color=#2C3E50, font-size=10px,
       text="in:(83,228) → y snapped: (83,240)",
       pos=(220, 228));

  circle(color=#16A085, fill=#76D7C4, center=(205, 222), radius=22,
         snap=grid-y);
  font(color=#2C3E50, font-size=10px,
       text="in:(205,222) → y snapped: (205,240)",
       pos=(380, 222));

  # ── snap=none: no snapping — exact coordinates used ──────────────────
  circle(color=#F39C12, fill=#F9E79F, center=(83, 305), radius=22,
         snap=none);
  font(color=#2C3E50, font-size=10px,
       text="in:(83,305) → no snap: stays (83,305)",
       pos=(220, 305));

  circle(color=#D35400, fill=#FAD7A0, center=(205, 298), radius=22,
         snap=none);
  font(color=#2C3E50, font-size=10px,
       text="in:(205,298) → no snap: stays (205,298)",
       pos=(380, 298));

  font(color=#7F8C8D, font-size=11px,
       text="snap=none overrides global align=true for that individual element.",
       pos=(15, 340));
end_frame
