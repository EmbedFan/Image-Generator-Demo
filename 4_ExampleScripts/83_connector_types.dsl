# 83_connector_types.dsl
# Category 16 — Advanced Connector Features
# Demonstrates: all three connector-type values.
#   straight — direct line segments between points (default)
#   curved   — smooth Catmull-Rom spline (needs ≥ 3 points for visible curve)
#   step     — H-V-H right-angle routing between each pair of points

begin_frame connector_types
  image width=640px; height=380px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 16: connector-type Values",
       pos=(15, 18));

  # ── Endpoint boxes (shared across all three demos) ─────────────────────
  # Left column
  square(color=#2C3E50, fill=#D5E8D4, pos=(20,  75), width=70px, height=40px);
  square(color=#2C3E50, fill=#D5E8D4, pos=(20, 155), width=70px, height=40px);
  square(color=#2C3E50, fill=#D5E8D4, pos=(20, 235), width=70px, height=40px);

  # Right column
  square(color=#2C3E50, fill=#DAE8FC, pos=(200,  95), width=70px, height=40px);
  square(color=#2C3E50, fill=#DAE8FC, pos=(200, 175), width=70px, height=40px);
  square(color=#2C3E50, fill=#DAE8FC, pos=(200, 255), width=70px, height=40px);

  font(color=#2C3E50, font-size=11px, weight=bold,
       text="connector-type=straight (default)", pos=(300, 95));
  font(color=#2C3E50, font-size=11px, weight=bold,
       text="connector-type=step", pos=(300, 175));
  font(color=#2C3E50, font-size=11px, weight=bold,
       text="connector-type=curved (3-point spline)", pos=(300, 255));

  # ── straight: default line segments ───────────────────────────────────
  connector(color=#27AE60, line-width=2px,
            connector-type=straight,
            start=(90, 95), end=(200, 115),
            end-cap=triangle);
  font(color=#27AE60, font-size=10px, text="straight", pos=(115, 88));

  # ── step: H-V-H right-angle routing ───────────────────────────────────
  # Two waypoints → engine inserts horizontal-vertical-horizontal legs
  connector(color=#E74C3C, line-width=2px,
            connector-type=step,
            points=[(90, 175), (150, 175), (200, 195)],
            end-cap=triangle);
  font(color=#E74C3C, font-size=10px, text="step (H-V-H)", pos=(115, 165));

  # ── curved: Catmull-Rom spline through 4 control points ───────────────
  # With 2 points curved renders as straight; 3+ gives visible curve
  connector(color=#3498DB, line-width=2px,
            connector-type=curved,
            points=[(90, 255), (140, 220), (160, 290), (200, 275)],
            end-cap=triangle);
  font(color=#3498DB, font-size=10px, text="curved (spline)", pos=(115, 248));

  # ── Detailed step demo (right half) ────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="Step routing detail", pos=(430, 55));
  font(color=#7F8C8D, font-size=10px,
       text="Each segment pair → H-V-H", pos=(430, 70));

  square(color=#2C3E50, fill=#E8D5F5, pos=(400, 95), width=60px, height=35px);
  square(color=#2C3E50, fill=#E8D5F5, pos=(580, 170), width=60px, height=35px);

  connector(color=#8E44AD, line-width=2px,
            connector-type=step,
            points=[(460, 112), (520, 112), (580, 187)],
            end-cap=filled-triangle,
            start-cap=circle, cap-size=small);
  font(color=#8E44AD, font-size=10px,
       text="points: 3 vertices", pos=(460, 145));

  # Curved demo with visible curve (right)
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="Curved spline detail", pos=(430, 225));
  square(color=#2C3E50, fill=#FFF2CC, pos=(400, 250), width=60px, height=35px);
  square(color=#2C3E50, fill=#FFF2CC, pos=(565, 310), width=60px, height=35px);

  connector(color=#F39C12, line-width=2px,
            connector-type=curved,
            points=[(460, 267), (490, 230), (540, 340), (565, 327)],
            end-cap=triangle);
  font(color=#F39C12, font-size=10px,
       text="4 control points", pos=(460, 350));

  font(color=#7F8C8D, font-size=11px,
       text="curved with exactly 2 points renders as straight (no curvature without 3+ points).",
       pos=(15, 355));
end_frame
