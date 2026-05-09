# 16_transform_combined.dsl
# Category 3 — Transformations
# Demonstrates: multiple transforms applied together on single primitives.
# Transform application order: position → scale → skew → rotate
# All four shared transform params: scale, skew-x, skew-y, rotate

begin_frame transform_combined
  image width=640px; height=440px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F0F4F8);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 3: Combined Transforms",
       pos=(15, 18));
  font(color=#7F8C8D, font-size=10px,
       text="Application order: position  →  scale  →  skew  →  rotate",
       pos=(15, 38));

  # ── scale + rotate ────────────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="scale + rotate:", pos=(15, 58));

  square(color=#2C3E50, fill=#AED6F1, pos=(30, 80), width=65px, height=55px,
         scale=1.5, rotate=30);
  font(color=#2C3E50, font-size=10px, align=center,
       text="s=1.5 r=30", pos=(75, 175));

  square(color=#2C3E50, fill=#3498DB, pos=(170, 80), width=65px, height=55px,
         scale=0.7, rotate=45);
  font(color=#2C3E50, font-size=10px, align=center,
       text="s=0.7 r=45", pos=(200, 175));

  circle(color=#2C3E50, fill=#1A5276, center=(340, 120), radius=45,
         scale=1.2, rotate=60);
  font(color=#2C3E50, font-size=10px, align=center,
       text="s=1.2 r=60", pos=(340, 175));

  polygon(color=#2C3E50, fill=#5DADE2,
          points=[(430,80),(490,80),(490,150),(430,150)],
          scale=0.8, rotate=30);
  font(color=#2C3E50, font-size=10px, align=center,
       text="s=0.8 r=30", pos=(460, 175));

  # ── skew + rotate ─────────────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="skew + rotate:", pos=(15, 200));

  square(color=#8E44AD, fill=#D7BDE2, pos=(30, 218), width=75px, height=55px,
         skew-x=20, rotate=15);
  font(color=#2C3E50, font-size=10px, align=center,
       text="sx=20 r=15", pos=(68, 300));

  square(color=#E67E22, fill=#FAD7A0, pos=(180, 218), width=75px, height=55px,
         skew-x=30, rotate=30);
  font(color=#2C3E50, font-size=10px, align=center,
       text="sx=30 r=30", pos=(218, 300));

  square(color=#E74C3C, fill=#FADBD8, pos=(330, 218), width=75px, height=55px,
         skew-y=20, rotate=10);
  font(color=#2C3E50, font-size=10px, align=center,
       text="sy=20 r=10", pos=(368, 300));

  # ── scale + skew + rotate (all three) ────────────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="scale + skew-x + skew-y + rotate:", pos=(15, 323));

  square(color=#2C3E50, fill=#A9DFBF, pos=(30, 340), width=70px, height=55px,
         scale=1.3, skew-x=15, rotate=20);
  font(color=#2C3E50, font-size=10px, align=center,
       text="s=1.3 sx=15 r=20", pos=(80, 392));

  square(color=#2C3E50, fill=#27AE60, pos=(190, 340), width=70px, height=55px,
         scale=0.9, skew-x=20, skew-y=10, rotate=35);
  font(color=#2C3E50, font-size=10px, align=center,
       text="s=0.9 sx=20 sy=10 r=35", pos=(240, 392));

  # Text with all transforms
  font(color=#C0392B, font-size=18px, weight=bold, text="DSL Transforms",
       pos=(420, 360), scale=1.1, skew-x=8, rotate=5);
  font(color=#7F8C8D, font-size=9px,
       text="scale=1.1 skew-x=8 rotate=5", pos=(420, 390));
end_frame
