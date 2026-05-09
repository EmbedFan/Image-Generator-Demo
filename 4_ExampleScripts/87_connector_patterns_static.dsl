# 87_connector_patterns_static.dsl
# Category 16 — Advanced Connector Features
# Demonstrates: static stroke patterns on connectors (animated=false, which is the default).
# When animated=false, the pattern tiles along the connector stroke without advancing.
# Pattern types: dash, dot, arrow, zigzag
# Parameters: pattern-length, pattern-gap, pattern-color

begin_frame connector_patterns_static
  image width=640px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#FAFAFA);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 16: Static Connector Patterns (animated=false)",
       pos=(15, 18));

  # Column labels
  font(color=#7F8C8D, font-size=11px, text="Pattern", pos=(15, 52));
  font(color=#7F8C8D, font-size=11px, text="Default spacing", pos=(160, 52));
  font(color=#7F8C8D, font-size=11px, text="Custom spacing", pos=(410, 52));

  # ── dash (default pattern) ─────────────────────────────────────────────
  font(color=#2C3E50, font-size=11px, text="dash", pos=(15, 78));

  # Default dash (pattern-length=8px, pattern-gap=4px)
  connector(color=#3498DB, line-width=3px,
            start=(160, 78), end=(380, 78),
            pattern=dash, end-cap=triangle);

  # Custom dash with wider units and gaps
  connector(color=#3498DB, line-width=3px,
            start=(410, 78), end=(620, 78),
            pattern=dash,
            pattern-length=18px, pattern-gap=8px,
            pattern-color=#85C1E9, end-cap=triangle);
  font(color=#7F8C8D, font-size=9px,
       text="length=18 gap=8", pos=(410, 90));

  # ── dot ───────────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=11px, text="dot", pos=(15, 130));

  connector(color=#E74C3C, line-width=3px,
            start=(160, 130), end=(380, 130),
            pattern=dot, end-cap=triangle);

  connector(color=#E74C3C, line-width=3px,
            start=(410, 130), end=(620, 130),
            pattern=dot,
            pattern-length=5px, pattern-gap=10px,
            pattern-color=#F1948A, end-cap=triangle);
  font(color=#7F8C8D, font-size=9px,
       text="length=5 gap=10", pos=(410, 142));

  # ── arrow ─────────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=11px, text="arrow", pos=(15, 182));

  connector(color=#27AE60, line-width=3px,
            start=(160, 182), end=(380, 182),
            pattern=arrow, end-cap=triangle);

  connector(color=#27AE60, line-width=3px,
            start=(410, 182), end=(620, 182),
            pattern=arrow,
            pattern-length=20px, pattern-gap=6px,
            pattern-color=#82E0AA, end-cap=triangle);
  font(color=#7F8C8D, font-size=9px,
       text="length=20 gap=6", pos=(410, 194));

  # ── zigzag ────────────────────────────────────────────────────────────
  font(color=#2C3E50, font-size=11px, text="zigzag", pos=(15, 234));

  connector(color=#8E44AD, line-width=3px,
            start=(160, 234), end=(380, 234),
            pattern=zigzag, end-cap=triangle);

  connector(color=#8E44AD, line-width=3px,
            start=(410, 234), end=(620, 234),
            pattern=zigzag,
            pattern-length=12px, pattern-gap=3px,
            pattern-color=#D7BDE2, end-cap=triangle);
  font(color=#7F8C8D, font-size=9px,
       text="length=12 gap=3", pos=(410, 246));

  # ── pattern-color: custom color independent of connector color ─────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="pattern-color differs from connector color", pos=(15, 278));

  connector(color=#BDC3C7, line-width=3px,
            start=(15, 305), end=(300, 305),
            pattern=arrow,
            pattern-color=#E74C3C,
            end-cap=triangle);
  font(color=#7F8C8D, font-size=10px,
       text="color=gray, pattern-color=red", pos=(15, 320));

  connector(color=#BDC3C7, line-width=3px,
            start=(15, 355), end=(300, 355),
            pattern=zigzag,
            pattern-length=10px, pattern-gap=4px,
            pattern-color=#3498DB,
            end-cap=none);
  font(color=#7F8C8D, font-size=10px,
       text="color=gray, pattern-color=blue, pattern-length=10, gap=4", pos=(15, 370));

  font(color=#7F8C8D, font-size=11px,
       text="animated=false (default): pattern tiles statically — no advancing between frames.",
       pos=(15, 400));
end_frame
