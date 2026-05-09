# 86_connector_label_advanced.dsl
# Category 16 — Advanced Connector Features
# Demonstrates: full connector label typography parameters.
#   label        — text shown along the connector
#   label-pos    — anchor: start | center | end
#   label-offset — pixel offset from the anchor point
#   label-font-family, label-font-size, label-font-color
#   label-font-style (normal | italic), label-font-weight (normal | bold)

begin_frame connector_label_advanced
  image width=640px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 16: Advanced Connector Labels",
       pos=(15, 18));

  # ── label-pos: start / center / end ───────────────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="label-pos=start", pos=(15, 55));
  connector(color=#3498DB, line-width=2px,
            start=(15, 78), end=(300, 78),
            end-cap=triangle,
            label="label-pos=start",
            label-pos=start,
            label-font-size=11px,
            label-font-color=#3498DB);

  font(color=#7F8C8D, font-size=11px,
       text="label-pos=center (default)", pos=(15, 110));
  connector(color=#27AE60, line-width=2px,
            start=(15, 133), end=(300, 133),
            end-cap=triangle,
            label="label-pos=center",
            label-pos=center,
            label-font-size=11px,
            label-font-color=#27AE60);

  font(color=#7F8C8D, font-size=11px,
       text="label-pos=end", pos=(15, 165));
  connector(color=#E74C3C, line-width=2px,
            start=(15, 188), end=(300, 188),
            end-cap=triangle,
            label="label-pos=end",
            label-pos=end,
            label-font-size=11px,
            label-font-color=#E74C3C);

  # ── label-offset: shift label away from anchor ─────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="label-offset=(0,-18) — raised above line", pos=(15, 218));
  connector(color=#8E44AD, line-width=2px,
            start=(15, 245), end=(300, 245),
            end-cap=triangle,
            label="raised label",
            label-pos=center,
            label-offset=(0, 18 - 36),
            label-font-size=11px,
            label-font-color=#8E44AD);

  font(color=#7F8C8D, font-size=11px,
       text="label-offset=(0,+16) — lowered below line", pos=(15, 270));
  connector(color=#E67E22, line-width=2px,
            start=(15, 293), end=(300, 293),
            end-cap=triangle,
            label="lowered label",
            label-pos=center,
            label-offset=(0, 16),
            label-font-size=11px,
            label-font-color=#E67E22);

  # ── Font style and weight ──────────────────────────────────────────────
  font(color=#7F8C8D, font-size=11px,
       text="label-font-style=italic, label-font-weight=bold, custom font-family",
       pos=(15, 323));
  connector(color=#2C3E50, line-width=2px,
            start=(15, 350), end=(580, 350),
            end-cap=filled-diamond,
            start-cap=circle,
            label="italic bold label — custom font",
            label-pos=center,
            label-font-family="Arial, Helvetica, sans-serif",
            label-font-size=13px,
            label-font-color=#C0392B,
            label-font-style=italic,
            label-font-weight=bold);

  # ── Full demo combining all label params on a diagram connector ─────────
  square(color=#2C3E50, fill=#D5E8D4, pos=(15, 375), width=80px, height=35px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Source", pos=(55, 397));
  square(color=#2C3E50, fill=#DAE8FC, pos=(500, 375), width=80px, height=35px);
  font(color=#2C3E50, font-size=11px, weight=bold, align=center,
       text="Target", pos=(540, 397));
  connector(color=#3498DB, line-width=2px,
            start=(95, 392), end=(500, 392),
            end-cap=triangle,
            label="data flow",
            label-pos=center,
            label-offset=(0, 14 - 28),
            label-font-size=12px,
            label-font-color=#2980B9,
            label-font-style=italic);
end_frame
