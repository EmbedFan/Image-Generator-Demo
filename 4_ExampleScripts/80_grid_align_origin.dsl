# 80_grid_align_origin.dsl
# Category 15 — Grid System
# Demonstrates: align-origin parameter — controls WHICH reference point
# of an element's bounding box is snapped to the grid.
# Values: left-top, right-top, left-bottom, right-bottom, center

begin_frame grid_align_origin
  image width=640px; height=380px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F8F9FA);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 15: align-origin — Which Corner Snaps",
       pos=(15, 18));

  # 80px grid, align=true globally, rendered for reference
  grid(step-x=80px, step-y=80px, align=true,
       render=true, color=RGB(210,210,210), line-type=dashed, line-width=1px);

  # ── left-top (default for pos-based elements) ─────────────────────────
  # pos=(45,62) → left-top corner snapped to (80,80) → pos becomes (80,80)
  square(color=#2980B9, fill=#AED6F1,
         pos=(45, 62), width=60px, height=50px,
         align-origin=left-top);
  font(color=#2C3E50, font-size=10px,
       text="left-top (default)", pos=(83, 136));
  font(color=#7F8C8D, font-size=9px,
       text="in pos=(45,62)", pos=(83, 148));

  # ── right-top ─────────────────────────────────────────────────────────
  # pos=(195,62), width=60 → right edge = 255 → snapped to 240 → pos.x=180
  square(color=#E74C3C, fill=#F1948A,
         pos=(195, 62), width=60px, height=50px,
         align-origin=right-top);
  font(color=#2C3E50, font-size=10px,
       text="right-top", pos=(195, 136));
  font(color=#7F8C8D, font-size=9px,
       text="right edge snaps", pos=(195, 148));

  # ── left-bottom ───────────────────────────────────────────────────────
  # pos=(350,62), height=50 → bottom = 112 → snapped to 160 → pos.y=110
  square(color=#27AE60, fill=#A9DFBF,
         pos=(350, 62), width=60px, height=50px,
         align-origin=left-bottom);
  font(color=#2C3E50, font-size=10px,
       text="left-bottom", pos=(350, 136));
  font(color=#7F8C8D, font-size=9px,
       text="bottom edge snaps", pos=(350, 148));

  # ── right-bottom ──────────────────────────────────────────────────────
  # pos=(490,62), w=60,h=50 → right=550,bottom=112 → snapped to (560,160)
  square(color=#8E44AD, fill=#D7BDE2,
         pos=(490, 62), width=60px, height=50px,
         align-origin=right-bottom);
  font(color=#2C3E50, font-size=10px,
       text="right-bottom", pos=(490, 136));
  font(color=#7F8C8D, font-size=9px,
       text="right+bottom snap", pos=(490, 148));

  # ── center (default for circle/pie/arc) ───────────────────────────────
  # center=(46,222) → snapped to (80,240) (nearest 80px intersection)
  circle(color=#E67E22, fill=#FAD7A0,
         center=(46, 222), radius=35,
         align-origin=center);
  font(color=#2C3E50, font-size=10px,
       text="center (circle default)", pos=(90, 255));
  font(color=#7F8C8D, font-size=9px,
       text="in center=(46,222)", pos=(90, 267));

  # Square with center alignment
  # center of bounding box = pos + (w/2, h/2); snap center to grid
  square(color=#16A085, fill=#76D7C4,
         pos=(250, 198), width=70px, height=50px,
         align-origin=center);
  font(color=#2C3E50, font-size=10px,
       text="center on square", pos=(250, 260));
  font(color=#7F8C8D, font-size=9px,
       text="center of bbox snaps", pos=(250, 272));

  font(color=#7F8C8D, font-size=11px,
       text="align-origin selects WHICH reference point of the bounding box snaps to the grid.",
       pos=(15, 345));
  font(color=#7F8C8D, font-size=11px,
       text="Default: center for circle/pie/arc; left-top for all other primitives.",
       pos=(15, 362));
end_frame
