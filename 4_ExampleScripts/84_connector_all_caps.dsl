# 84_connector_all_caps.dsl
# Category 16 — Advanced Connector Features
# Demonstrates: all nine cap shape values for start-cap and end-cap,
# per-end cap size overrides (start-cap-size / end-cap-size),
# and the three cap-size values: small, medium, large.

begin_frame connector_all_caps
  image width=660px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#FAFAFA);

  font(color=#2C3E50, font-size=15px, weight=bold,
       text="Category 16: All Connector Cap Shapes",
       pos=(15, 18));

  # Column headers
  font(color=#7F8C8D, font-size=11px, text="Cap type", pos=(15, 52));
  font(color=#7F8C8D, font-size=11px, text="Connector", pos=(120, 52));
  font(color=#7F8C8D, font-size=11px, text="Description", pos=(420, 52));

  # ── All nine cap types (on end-cap) ──────────────────────────────────

  # none (default)
  font(color=#2C3E50, font-size=11px, text="none", pos=(15, 75));
  connector(color=#2C3E50, line-width=2px,
            start=(120, 75), end=(400, 75),
            end-cap=none);
  font(color=#7F8C8D, font-size=10px,
       text="No cap at either end (default)", pos=(420, 72));

  # triangle
  font(color=#2C3E50, font-size=11px, text="triangle", pos=(15, 108));
  connector(color=#3498DB, line-width=2px,
            start=(120, 108), end=(400, 108),
            start-cap=none, end-cap=triangle);
  font(color=#7F8C8D, font-size=10px,
       text="Filled arrowhead", pos=(420, 105));

  # open-triangle
  font(color=#2C3E50, font-size=11px, text="open-triangle", pos=(15, 141));
  connector(color=#3498DB, line-width=2px,
            start=(120, 141), end=(400, 141),
            end-cap=open-triangle);
  font(color=#7F8C8D, font-size=10px,
       text="Outlined arrowhead", pos=(420, 138));

  # circle
  font(color=#2C3E50, font-size=11px, text="circle", pos=(15, 174));
  connector(color=#E74C3C, line-width=2px,
            start=(120, 174), end=(400, 174),
            end-cap=circle);
  font(color=#7F8C8D, font-size=10px,
       text="Hollow circle", pos=(420, 171));

  # filled-circle
  font(color=#2C3E50, font-size=11px, text="filled-circle", pos=(15, 207));
  connector(color=#E74C3C, line-width=2px,
            start=(120, 207), end=(400, 207),
            end-cap=filled-circle);
  font(color=#7F8C8D, font-size=10px,
       text="Filled circle", pos=(420, 204));

  # diamond
  font(color=#2C3E50, font-size=11px, text="diamond", pos=(15, 240));
  connector(color=#27AE60, line-width=2px,
            start=(120, 240), end=(400, 240),
            end-cap=diamond);
  font(color=#7F8C8D, font-size=10px,
       text="Hollow diamond", pos=(420, 237));

  # filled-diamond
  font(color=#2C3E50, font-size=11px, text="filled-diamond", pos=(15, 273));
  connector(color=#27AE60, line-width=2px,
            start=(120, 273), end=(400, 273),
            end-cap=filled-diamond);
  font(color=#7F8C8D, font-size=10px,
       text="Filled diamond", pos=(420, 270));

  # square
  font(color=#2C3E50, font-size=11px, text="square", pos=(15, 306));
  connector(color=#8E44AD, line-width=2px,
            start=(120, 306), end=(400, 306),
            end-cap=square);
  font(color=#7F8C8D, font-size=10px,
       text="Hollow square", pos=(420, 303));

  # filled-square
  font(color=#2C3E50, font-size=11px, text="filled-square", pos=(15, 339));
  connector(color=#8E44AD, line-width=2px,
            start=(120, 339), end=(400, 339),
            end-cap=filled-square);
  font(color=#7F8C8D, font-size=10px,
       text="Filled square", pos=(420, 336));

  # ── Per-end cap size overrides ─────────────────────────────────────────
  font(color=#2C3E50, font-size=12px, weight=bold,
       text="Per-end cap size: start-cap-size / end-cap-size",
       pos=(15, 370));

  connector(color=#E67E22, line-width=2px,
            start=(120, 395), end=(400, 395),
            start-cap=triangle, start-cap-size=small,
            end-cap=triangle, end-cap-size=large);
  font(color=#E67E22, font-size=10px, text="small", pos=(100, 408));
  font(color=#E67E22, font-size=10px, text="large", pos=(402, 408));
end_frame
