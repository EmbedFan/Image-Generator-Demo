# 73_vars_chained_layout.dsl
# Category 14 — Variables and Layout Chaining
# Demonstrates: sequential chained layout — each block is placed by reading
# the previous block's .bbox, building a horizontal flow automatically.
# This replicates the complete example from DSL user guide §20.

begin_frame vars_chained_layout
  image width=640px; height=210px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#1E1E2E);

  var gap;
  gap = 16;

  # ── Block 1 ──────────────────────────────────────────────────────────────
  b1 = square(pos=(22, 70), width=130, height=65, fill=#89B4FA, color=none);
  font(color=#1E1E2E, font-size=12px, weight=bold, align=center,
       text="Block 1",
       pos=(22 + 65, 70 + 38));

  var bx1, by1, bw1, bh1;
  bx1 = b1.bbox.x;
  by1 = b1.bbox.y;
  bw1 = b1.bbox.width;
  bh1 = b1.bbox.height;

  # Arrow → Block 2
  connector(color=#CDD6F4, line-width=2px,
            start=(bx1 + bw1, by1 + bh1 / 2),
            end=(bx1 + bw1 + gap, by1 + bh1 / 2),
            end-cap=triangle, cap-size=small);

  # ── Block 2 — anchored via b1 bbox ───────────────────────────────────────
  b2 = square(pos=(bx1 + bw1 + gap, by1), width=110, height=bh1,
              fill=#A6E3A1, color=none);
  font(color=#1E1E2E, font-size=12px, weight=bold, align=center,
       text="Block 2",
       pos=(bx1 + bw1 + gap + 55, by1 + bh1 / 2 + 5));

  var bx2, bw2;
  bx2 = b2.bbox.x;
  bw2 = b2.bbox.width;

  # Arrow → Block 3
  connector(color=#CDD6F4, line-width=2px,
            start=(bx2 + bw2, by1 + bh1 / 2),
            end=(bx2 + bw2 + gap, by1 + bh1 / 2),
            end-cap=triangle, cap-size=small);

  # ── Block 3 — anchored via b2 bbox ───────────────────────────────────────
  b3 = square(pos=(bx2 + bw2 + gap, by1), width=90, height=bh1,
              fill=#FAB387, color=none);
  font(color=#1E1E2E, font-size=12px, weight=bold, align=center,
       text="Block 3",
       pos=(bx2 + bw2 + gap + 45, by1 + bh1 / 2 + 5));

  var bx3, bw3;
  bx3 = b3.bbox.x;
  bw3 = b3.bbox.width;

  # Arrow → Block 4
  connector(color=#CDD6F4, line-width=2px,
            start=(bx3 + bw3, by1 + bh1 / 2),
            end=(bx3 + bw3 + gap, by1 + bh1 / 2),
            end-cap=triangle, cap-size=small);

  # ── Block 4 — anchored via b3 bbox ───────────────────────────────────────
  b4 = square(pos=(bx3 + bw3 + gap, by1), width=75, height=bh1,
              fill=#F38BA8, color=none);
  font(color=#1E1E2E, font-size=11px, weight=bold, align=center,
       text="Block 4",
       pos=(bx3 + bw3 + gap + 37, by1 + bh1 / 2 + 5));

  # Circle overlay on Block 1 using its center
  var cx1, cy1;
  cx1 = bx1 + bw1 / 2;
  cy1 = by1 + bh1 / 2;
  circle(center=(cx1, cy1), radius=22, color=#CDD6F4, line-width=2, fill=none);

  font(color=#CDD6F4, font-size=13px, weight=bold,
       text="Category 14: Chained Layout via .bbox",
       pos=(22, 178));
  font(color=#6C7086, font-size=10px,
       text="Each block's pos computed from previous block's .bbox.x + .bbox.width + gap",
       pos=(22, 195));
end_frame
