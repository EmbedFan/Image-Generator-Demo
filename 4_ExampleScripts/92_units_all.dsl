# 92_units_all.dsl
# Category 17 — Colorspaces, Output Formats, and Units
# Demonstrates: all six unit suffixes in a single frame.
#   px  — pixels (default when no suffix given)
#   pt  — points (1pt = DPI/72 px; at 96dpi → 1.33 px)
#   cm  — centimeters (1cm = DPI/2.54 px; at 96dpi → 37.8 px)
#   mm  — millimeters (1mm = DPI/25.4 px; at 96dpi → 3.78 px)
#   em  — font-relative (inside font → current font-size; outside → 12px default)
#   %   — percentage (of parent container; scalar params → % of canvas width)

begin_frame units_all
  image width=680px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 17: All Six Unit Suffixes (dpi=96)",
       pos=(15, 18));
  font(color=#7F8C8D, font-size=11px,
       text="At 96 dpi: 1pt=1.33px  1cm=37.8px  1mm=3.78px  1em=12px (outside font)",
       pos=(15, 38));

  # ── px — pixels (explicit) ─────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="px — pixels (default)", pos=(15, 65));
  square(color=#2980B9, fill=#AED6F1,
         pos=(15, 82), width=150px, height=40px);
  font(color=#2C3E50, font-size=10px, align=center,
       text="width=150px, height=40px", pos=(90, 133));

  # ── pt — points ────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="pt — points (1pt=1.33px at 96dpi)", pos=(195, 65));
  # 100pt = 100 * (96/72) ≈ 133px
  square(color=#E74C3C, fill=#F1948A,
         pos=(195, 82), width=100pt, height=30pt);
  font(color=#2C3E50, font-size=10px,
       text="width=100pt (≈133px), height=30pt (≈40px)", pos=(195, 133));

  # ── cm — centimeters ───────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="cm — centimeters", pos=(15, 158));
  # 4cm = 4 * (96/2.54) ≈ 151px
  square(color=#27AE60, fill=#A9DFBF,
         pos=(15, 175), width=4cm, height=1cm);
  font(color=#2C3E50, font-size=10px,
       text="width=4cm (≈151px), height=1cm (≈38px)", pos=(15, 223));

  # ── mm — millimeters ───────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="mm — millimeters", pos=(350, 158));
  # 40mm = 40 * (96/25.4) ≈ 151px
  square(color=#8E44AD, fill=#D7BDE2,
         pos=(350, 175), width=40mm, height=10mm);
  font(color=#2C3E50, font-size=10px,
       text="width=40mm (≈151px), height=10mm (≈38px)", pos=(350, 223));

  # ── em — font-relative ─────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="em — font-relative (inside font=current size; outside=12px)", pos=(15, 248));

  # Inside font primitive: em = current font-size
  font(color=#E67E22, font-size=24px,
       text="font-size=24px (2em line-height context)",
       pos=(15, 272));
  # em outside font: line-width=2em resolves to 2*12=24px
  circle(color=#E67E22, fill=RGBA(230,126,34,0.2),
         center=(60, 320), radius=2em, line-width=0.5em);
  font(color=#2C3E50, font-size=10px, align=center,
       text="radius=2em=24px\nline-width=0.5em=6px", pos=(60, 352));

  # ── % — percentage ─────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="% — canvas-relative percentage", pos=(200, 248));

  # 50% of canvas width = 340px; 10% of canvas height = 42px
  square(color=#16A085, fill=#76D7C4,
         pos=(200, 272), width=50%, height=10%);
  font(color=#2C3E50, font-size=10px,
       text="width=50% (=340px of 680px canvas)", pos=(200, 317));

  # Scalar: radius=5% → 5% of canvas width = 34px
  circle(color=#2C3E50, fill=#AED6F1,
         center=(590, 300), radius=5%);
  font(color=#2C3E50, font-size=10px, align=center,
       text="radius=5%\n(=34px of 680px)", pos=(590, 345));

  # Border around the whole canvas using %
  square(color=#BDC3C7, fill=none,
         pos=(0, 0), width=100%, height=100%);

  font(color=#7F8C8D, font-size=11px,
       text="Omitting a unit defaults to px. Angles (rotate, start-angle, end-angle) never take a unit suffix.",
       pos=(15, 400));
end_frame
