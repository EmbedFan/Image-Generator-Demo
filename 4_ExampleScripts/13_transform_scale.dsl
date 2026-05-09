# 13_transform_scale.dsl
# Category 3 — Transformations
# Demonstrates: scale= parameter on primitives and text.
# scale=0.5 → half size; scale=1.0 → original; scale=2.0 → double.
# Scaling is uniform and centered on the element's anchor point.

begin_frame transform_scale
  image width=640px; height=380px; colorspace=RGB; dpi=300; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 3: scale= Transformation",
       pos=(15, 18));
  font(color=#7F8C8D, font-size=10px,
       text="Uniform scaling centered on the element's anchor point.",
       pos=(15, 38));

  # ── Circles at the same center with different scale= ──────────────────
  font(color=#7F8C8D, font-size=11px,
       text="circle (radius=50) at same center, varying scale=:",
       pos=(15, 58));

  circle(color=#2980B9, fill=#D6EAF8, center=(100, 140), radius=50, scale=0.4);
  font(color=#2C3E50, font-size=10px, align=center, text="0.4x", pos=(100, 200));

  circle(color=#2980B9, fill=#AED6F1, center=(230, 140), radius=50, scale=0.8);
  font(color=#2C3E50, font-size=10px, align=center, text="0.8x", pos=(230, 200));

  circle(color=#2980B9, fill=#3498DB, center=(370, 140), radius=50, scale=1.0);
  font(color=#2C3E50, font-size=10px, align=center, text="1.0x (original)", pos=(370, 200));

  circle(color=#2980B9, fill=#1A5276, center=(520, 140), radius=50, scale=1.5);
  font(color=#2C3E50, font-size=10px, align=center, text="1.5x", pos=(520, 200));

  # ── Squares at the same pos with different scale= ─────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="square (width=70, height=50) at same pos, varying scale=:",
       pos=(15, 220));

  square(color=#C0392B, fill=#FADBD8, pos=(30, 240), width=70px, height=50px, scale=0.5);
  font(color=#2C3E50, font-size=10px, align=center, text="0.5x", pos=(65, 305));

  square(color=#C0392B, fill=#F1948A, pos=(165, 240), width=70px, height=50px, scale=0.8);
  font(color=#2C3E50, font-size=10px, align=center, text="0.8x", pos=(200, 305));

  square(color=#C0392B, fill=#E74C3C, pos=(300, 240), width=70px, height=50px, scale=1.0);
  font(color=#2C3E50, font-size=10px, align=center, text="1.0x", pos=(335, 305));

  square(color=#C0392B, fill=#922B21, pos=(430, 240), width=70px, height=50px, scale=1.4);
  font(color=#2C3E50, font-size=10px, align=center, text="1.4x", pos=(465, 305));

  # ── Font scale= ───────────────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="font scale=:", pos=(15, 368));
  font(color=#27AE60, font-size=18px, weight=bold, text="Text", pos=(100, 344), scale=0.5);
  font(color=#27AE60, font-size=18px, weight=bold, text="Text", pos=(175, 336), scale=1.0);
  font(color=#27AE60, font-size=18px, weight=bold, text="Text", pos=(260, 328), scale=1.5);
  font(color=#27AE60, font-size=18px, weight=bold, text="Text", pos=(380, 320), scale=2.0);

  line(color=red, line-type=dotted, line-width=2px, start=(100, 322), end=(540, 322));
  line(color=red, line-type=dotted, line-width=2px, start=(100, 354), end=(540, 354));

  font(color=#7F8C8D, font-size=9px, text="0.5x",  pos=(100, 368));
  font(color=#7F8C8D, font-size=9px, text="1.0x",  pos=(177, 368));
  font(color=#7F8C8D, font-size=9px, text="1.5x",  pos=(266, 368));
  font(color=#7F8C8D, font-size=9px, text="2.0x",  pos=(388, 368));
end_frame
