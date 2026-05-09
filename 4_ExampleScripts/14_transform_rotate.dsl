# 14_transform_rotate.dsl
# Category 3 — Transformations
# Demonstrates: rotate= parameter. Rotation is CLOCKWISE, 0–360 degrees.
# No unit suffix — write rotate=45 (not rotate=45px or rotate=45deg).
# Rotation is applied around the element's center point.

begin_frame transform_rotate
  image width=640px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F8F9FA);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 3: rotate= Transformation (clockwise degrees)",
       pos=(15, 18));

  # ── Square at different angles ─────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="square (width=70px, height=50px) — same pos, varying rotate=:",
       pos=(15, 45));

  square(color=#2980B9, fill=#AED6F1, pos=(30, 65), width=70px, height=50px, rotate=0);
  font(color=#2C3E50, font-size=10px, align=center, text="0°",   pos=(65, 135));

  square(color=#2980B9, fill=#5DADE2, pos=(145, 65), width=70px, height=50px, rotate=15);
  font(color=#2C3E50, font-size=10px, align=center, text="15°",  pos=(180, 135));

  square(color=#2980B9, fill=#3498DB, pos=(270, 65), width=70px, height=50px, rotate=30);
  font(color=#2C3E50, font-size=10px, align=center, text="30°",  pos=(305, 135));

  square(color=#2980B9, fill=#2471A3, pos=(390, 65), width=70px, height=50px, rotate=45);
  font(color=#2C3E50, font-size=10px, align=center, text="45°",  pos=(425, 135));

  square(color=#2980B9, fill=#1A5276, pos=(510, 65), width=70px, height=50px, rotate=90);
  font(color=#2C3E50, font-size=10px, align=center, text="90°",  pos=(545, 135));

  # ── Pie fan — same pie slice rotated 60° steps ─────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="Pie slices — same shape, rotate= incremented by 60°:", pos=(15, 158));

  pie(color=#C0392B, fill=#E74C3C, center=(160, 255), radius=65, start-angle=0, end-angle=55, rotate=0);
  pie(color=#D35400, fill=#E67E22, center=(160, 255), radius=65, start-angle=0, end-angle=55, rotate=60);
  pie(color=#1E8449, fill=#27AE60, center=(160, 255), radius=65, start-angle=0, end-angle=55, rotate=120);
  pie(color=#1A5276, fill=#3498DB, center=(160, 255), radius=65, start-angle=0, end-angle=55, rotate=180);
  pie(color=#6C3483, fill=#8E44AD, center=(160, 255), radius=65, start-angle=0, end-angle=55, rotate=240);
  pie(color=#7D6608, fill=#F1C40F, center=(160, 255), radius=65, start-angle=0, end-angle=55, rotate=300);
  font(color=#7F8C8D, font-size=10px, align=center,
       text="6 identical slices\nrotate= 0°, 60°, 120°, 180°, 240°, 300°",
       pos=(160, 338));

  # ── Rotated text labels ────────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="Rotated text:", pos=(340, 158));
  font(color=#2C3E50, font-size=15px, weight=bold, text="0°",  pos=(380, 180), rotate=0);
  font(color=#E74C3C, font-size=15px, weight=bold, text="30°", pos=(440, 195), rotate=30);
  font(color=#27AE60, font-size=15px, weight=bold, text="60°", pos=(530, 175), rotate=60);
  font(color=#9B59B6, font-size=15px, weight=bold, text="90°", pos=(590, 240), rotate=90);
  font(color=#E67E22, font-size=15px, weight=bold, text="45°", pos=(490, 300), rotate=45);

  font(color=#E74C3C, font-size=11px,
       text="Do NOT write rotate=45px — angle parameters never take a unit suffix.",
       pos=(15, 380));
end_frame
