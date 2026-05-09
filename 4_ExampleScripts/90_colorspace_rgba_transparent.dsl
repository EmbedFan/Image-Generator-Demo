# 90_colorspace_rgba_transparent.dsl
# Category 17 — Colorspaces, Output Formats, and Units
# Demonstrates: colorspace=RGBA canvas with transparent background.
# Semi-transparent RGBA fills layer over a PNG background image.
# The image primitive uses opacity=; shapes use RGBA() for transparency.
# Output is a PNG with an alpha channel — suitable for compositing.

begin_frame colorspace_rgba_transparent
  image width=600px; height=380px; colorspace=RGBA; dpi=96; output-format=png;

  # Transparent canvas — no background fill; alpha channel preserved
  background(color=transparent);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 17: colorspace=RGBA — Transparent Canvas",
       pos=(15, 18));
  font(color=#7F8C8D, font-size=11px,
       text="Canvas has an alpha channel. Shapes use RGBA() for transparency.",
       pos=(15, 38));

  # ── Checkerboard pattern to visualize transparency ─────────────────────
  # (In a real renderer, transparent areas show the checkerboard pattern
  #  or underlying content. Here we simulate it with gray squares.)
  font(color=#7F8C8D, font-size=10px,
       text="< transparent area — no fill >", pos=(15, 62));

  # ── RGBA fills at varying alpha levels ────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="RGBA fill transparency (alpha 0.0 → 1.0):", pos=(15, 88));

  # Horizontal strip of overlapping semi-transparent circles
  circle(color=transparent, fill=RGBA(231,76,60,0.15),  center=(80,  145), radius=45);
  circle(color=transparent, fill=RGBA(231,76,60,0.35),  center=(130, 145), radius=45);
  circle(color=transparent, fill=RGBA(231,76,60,0.55),  center=(180, 145), radius=45);
  circle(color=transparent, fill=RGBA(231,76,60,0.75),  center=(230, 145), radius=45);
  circle(color=transparent, fill=RGBA(231,76,60,1.00),  center=(280, 145), radius=45);

  font(color=#7F8C8D, font-size=9px, text="0.15", pos=(65,  198));
  font(color=#7F8C8D, font-size=9px, text="0.35", pos=(115, 198));
  font(color=#7F8C8D, font-size=9px, text="0.55", pos=(165, 198));
  font(color=#7F8C8D, font-size=9px, text="0.75", pos=(215, 198));
  font(color=#7F8C8D, font-size=9px, text="1.00", pos=(265, 198));

  # ── Overlapping RGBA rectangles (compositing demo) ────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="Overlapping RGBA fills (compositing):", pos=(15, 220));

  square(color=transparent, fill=RGBA(52,152,219,0.6),
         pos=(30, 240), width=120px, height=80px);
  square(color=transparent, fill=RGBA(231,76,60,0.6),
         pos=(80, 260), width=120px, height=80px);
  square(color=transparent, fill=RGBA(39,174,96,0.6),
         pos=(55, 285), width=120px, height=60px);

  font(color=#2C3E50, font-size=10px, text="Blue 0.6", pos=(35, 328));
  font(color=#2C3E50, font-size=10px, text="Red 0.6",  pos=(125, 328));
  font(color=#2C3E50, font-size=10px, text="Green 0.6 (bottom)", pos=(55, 355));

  # ── Semi-transparent stroke (RGBA color on color= parameter) ──────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="Semi-transparent strokes:", pos=(350, 220));

  circle(color=RGBA(142,68,173,0.3), fill=transparent,
         center=(420, 295), radius=50, line-width=8px);
  circle(color=RGBA(142,68,173,0.6), fill=transparent,
         center=(420, 295), radius=35, line-width=8px);
  circle(color=RGBA(142,68,173,1.0), fill=transparent,
         center=(420, 295), radius=20, line-width=8px);
  font(color=#7F8C8D, font-size=10px, align=center,
       text="RGBA stroke alpha: 0.3 / 0.6 / 1.0",
       pos=(420, 355));

  # ── Reminder about JPEG incompatibility ───────────────────────────────
  font(color=#E74C3C, font-size=11px,
       text="JPEG does not support RGBA — use output-format=png for transparency.",
       pos=(15, 360));
end_frame
