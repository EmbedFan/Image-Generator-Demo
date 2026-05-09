# 11_line_styles.dsl
# Category 2 — Colors and Styling
# Demonstrates: all four line-type values on lines, circles, squares, and connectors.
# Also shows varying line-width values (1px–10px).

begin_frame line_styles
  image width=640px; height=390px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 2: Line Styles (line-type and line-width)",
       pos=(15, 18));

  # ── Column header ─────────────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="line-type value", pos=(15, 45));
  font(color=#7F8C8D, font-size=11px, text="line primitive", pos=(130, 45));
  font(color=#7F8C8D, font-size=11px, text="circle (fill=none)", pos=(370, 45));
  font(color=#7F8C8D, font-size=11px, text="square (fill=none)", pos=(500, 45));

  # ── solid ──────────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold, text="solid",    pos=(15, 80));
  line(color=#3498DB, line-type=solid,    line-width=2px, start=(130, 80), end=(360, 80));
  circle(color=#3498DB, fill=none, line-type=solid,    line-width=2px, center=(430, 80), radius=22);
  square(color=#3498DB, fill=none, line-type=solid,    line-width=2px, pos=(500, 60), width=70px, height=40px);

  # ── dashed ─────────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold, text="dashed",   pos=(15, 140));
  line(color=#E74C3C, line-type=dashed,   line-width=2px, start=(130, 140), end=(360, 140));
  circle(color=#E74C3C, fill=none, line-type=dashed,   line-width=2px, center=(430, 140), radius=22);
  square(color=#E74C3C, fill=none, line-type=dashed,   line-width=2px, pos=(500, 120), width=70px, height=40px);

  # ── dotted ─────────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold, text="dotted",   pos=(15, 200));
  line(color=#27AE60, line-type=dotted,   line-width=2px, start=(130, 200), end=(360, 200));
  circle(color=#27AE60, fill=none, line-type=dotted,   line-width=2px, center=(430, 200), radius=22);
  square(color=#27AE60, fill=none, line-type=dotted,   line-width=2px, pos=(500, 180), width=70px, height=40px);

  # ── dash-dot ───────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold, text="dash-dot", pos=(15, 260));
  line(color=#8E44AD, line-type=dash-dot, line-width=2px, start=(130, 260), end=(360, 260));
  circle(color=#8E44AD, fill=none, line-type=dash-dot, line-width=2px, center=(430, 260), radius=22);
  square(color=#8E44AD, fill=none, line-type=dash-dot, line-width=2px, pos=(500, 240), width=70px, height=40px);

  # ── Varying line-width (solid) ─────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px, text="Varying line-width (solid):", pos=(15, 302));
  line(color=#2C3E50, line-type=solid, line-width=1px,  start=(200, 314), end=(450, 314));
  font(color=#7F8C8D, font-size=9px, text="1px",  pos=(455, 312));
  line(color=#2C3E50, line-type=solid, line-width=3px,  start=(200, 328), end=(450, 328));
  font(color=#7F8C8D, font-size=9px, text="3px",  pos=(455, 326));
  line(color=#2C3E50, line-type=solid, line-width=6px,  start=(200, 344), end=(450, 344));
  font(color=#7F8C8D, font-size=9px, text="6px",  pos=(455, 342));
  line(color=#2C3E50, line-type=solid, line-width=10px, start=(200, 362), end=(450, 362));
  font(color=#7F8C8D, font-size=9px, text="10px", pos=(455, 360));

  font(color=#7F8C8D, font-size=10px,
       text="line-type values: solid  |  dashed  |  dotted  |  dash-dot",
       pos=(15, 375));
end_frame
