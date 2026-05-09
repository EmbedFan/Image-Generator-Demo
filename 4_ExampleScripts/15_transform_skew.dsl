# 15_transform_skew.dsl
# Category 3 — Transformations
# Demonstrates: skew-x= and skew-y= parameters.
#   skew-x: positive → shear rightward (top edge moves right)
#   skew-y: positive → shear downward  (left edge moves down)
# Both accept degree values. Can be combined on the same element.

begin_frame transform_skew
  image width=700px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 3: skew-x= and skew-y= Transformations",
       pos=(15, 18));

  # ── skew-x: horizontal shear ──────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="skew-x (top edge shifts right as value increases):",
       pos=(15, 48));

  square(color=#2980B9, fill=#AED6F1, pos=(15, 68), width=80px, height=55px, skew-x=0);
  font(color=#2C3E50, font-size=10px, align=center, text="skew-x=0",   pos=(55, 140));

  square(color=#2980B9, fill=#5DADE2, pos=(130, 68), width=80px, height=55px, skew-x=15);
  font(color=#2C3E50, font-size=10px, align=center, text="skew-x=15",  pos=(170, 140));

  square(color=#2980B9, fill=#3498DB, pos=(255, 68), width=80px, height=55px, skew-x=30);
  font(color=#2C3E50, font-size=10px, align=center, text="skew-x=30",  pos=(295, 140));

  square(color=#2980B9, fill=#2471A3, pos=(385, 68), width=80px, height=55px, skew-x=45);
  font(color=#2C3E50, font-size=10px, align=center, text="skew-x=45",  pos=(425, 140));

  square(color=#E74C3C, fill=#F5B7B1, pos=(510, 68), width=80px, height=55px, skew-x=60);
  font(color=#E74C3C, font-size=10px, align=center, text="skew-x=60", pos=(550, 140));

  # ── skew-y: vertical shear ────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="skew-y (left edge shifts down as value increases):",
       pos=(15, 162));

  square(color=#27AE60, fill=#A9DFBF, pos=(15, 180), width=60px, height=75px, skew-y=0);
  font(color=#2C3E50, font-size=10px, align=center, text="skew-y=0",   pos=(45, 268));

  square(color=#27AE60, fill=#58D68D, pos=(110, 180), width=60px, height=75px, skew-y=15);
  font(color=#2C3E50, font-size=10px, align=center, text="skew-y=15",  pos=(140, 268));

  square(color=#27AE60, fill=#2ECC71, pos=(210, 180), width=60px, height=75px, skew-y=25);
  font(color=#2C3E50, font-size=10px, align=center, text="skew-y=25",  pos=(240, 268));

  square(color=#E74C3C, fill=#F1948A, pos=(310, 180), width=60px, height=75px, skew-y=35);
  font(color=#E74C3C, font-size=10px, align=center, text="skew-y=35", pos=(340, 268));

  # ── Combined skew-x + skew-y ──────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="Combined skew-x + skew-y:", pos=(15, 290));

  square(color=#8E44AD, fill=#D2B4DE, pos=(15, 308), width=75px, height=55px,
         skew-x=20, skew-y=10);
  font(color=#2C3E50, font-size=10px, align=center, text="x=20, y=10", pos=(55, 375));

  square(color=#8E44AD, fill=#9B59B6, pos=(150, 308), width=75px, height=55px,
         skew-x=30, skew-y=20);
  font(color=#2C3E50, font-size=10px, align=center, text="x=30, y=20", pos=(190, 375));

  # Skewed text
  font(color=#E67E22, font-size=22px, weight=bold, text="Italic-style skew",
       pos=(300, 345), skew-x=18);
  font(color=#7F8C8D, font-size=10px,
       text="skew-x=18", pos=(300, 368));
end_frame
