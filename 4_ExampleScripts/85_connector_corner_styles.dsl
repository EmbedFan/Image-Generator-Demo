# 85_connector_corner_styles.dsl
# Category 16 — Advanced Connector Features
# Demonstrates: corner styles on step and straight multi-segment connectors.
#   corner=sharp    — hard right-angle turns (default)
#   corner=rounded  — arc-smoothed turns; corner-radius controls arc size
#   corner=beveled  — diagonal cut at each turn
# Note: corner is silently ignored for connector-type=curved.

begin_frame connector_corner_styles
  image width=640px; height=400px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 16: Corner Styles (sharp / rounded / beveled)",
       pos=(15, 18));

  # ── Step connectors in left column ────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="connector-type=step", pos=(20, 50));

  # sharp (default)
  font(color=#7F8C8D, font-size=11px, text="corner=sharp", pos=(20, 72));
  connector(color=#3498DB, line-width=3px,
            connector-type=step,
            points=[(20, 90), (90, 90), (90, 150), (180, 150)],
            corner=sharp,
            end-cap=triangle);

  # rounded with small radius
  font(color=#7F8C8D, font-size=11px, text="corner=rounded  radius=8px", pos=(20, 178));
  connector(color=#E74C3C, line-width=3px,
            connector-type=step,
            points=[(20, 195), (90, 195), (90, 255), (180, 255)],
            corner=rounded, corner-radius=8px,
            end-cap=triangle);

  # rounded with large radius
  font(color=#7F8C8D, font-size=11px, text="corner=rounded  radius=20px", pos=(20, 283));
  connector(color=#27AE60, line-width=3px,
            connector-type=step,
            points=[(20, 300), (90, 300), (90, 360), (180, 360)],
            corner=rounded, corner-radius=20px,
            end-cap=triangle);

  # beveled
  font(color=#7F8C8D, font-size=11px, text="corner=beveled", pos=(20, 375));

  # ── Straight multi-segment connectors in right column ─────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="connector-type=straight (multi-segment)", pos=(330, 50));

  # sharp
  font(color=#7F8C8D, font-size=11px, text="corner=sharp", pos=(330, 72));
  connector(color=#3498DB, line-width=3px,
            connector-type=straight,
            points=[(330, 90), (400, 140), (460, 100), (540, 150)],
            corner=sharp,
            end-cap=triangle);

  # rounded
  font(color=#7F8C8D, font-size=11px, text="corner=rounded  radius=12px", pos=(330, 178));
  connector(color=#E74C3C, line-width=3px,
            connector-type=straight,
            points=[(330, 195), (400, 245), (460, 205), (540, 255)],
            corner=rounded, corner-radius=12px,
            end-cap=triangle);

  # beveled
  font(color=#7F8C8D, font-size=11px, text="corner=beveled", pos=(330, 283));
  connector(color=#8E44AD, line-width=3px,
            connector-type=straight,
            points=[(330, 300), (400, 350), (460, 310), (540, 355)],
            corner=beveled,
            end-cap=triangle);

  font(color=#7F8C8D, font-size=11px,
       text="corner and corner-radius are silently ignored for connector-type=curved.",
       pos=(15, 385));
end_frame
