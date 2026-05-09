# 76_vars_complex_auto_layout.dsl
# Category 14 — Variables and Layout Chaining
# Demonstrates: full auto-layout using bbox chaining.
# Columns are built by reading each block's bbox and advancing horizontally.
# Connectors are anchored to computed bbox edges.
# A summary circle is centred on the entire row using bbox arithmetic.

begin_frame vars_complex_auto_layout
  image width=700px; height=280px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#1E1E2E);

  font(color=#CDD6F4, font-size=15px, weight=bold,
       text="Category 14: Complex Auto-Layout via .bbox Chaining",
       pos=(20, 18));

  var gap, row_y, row_h;
  gap   = 14;
  row_y = 60;
  row_h = 65;

  # ── Column 1: Input ───────────────────────────────────────────────────
  col1 = square(pos=(20, row_y), width=120, height=row_h,
                fill=#313244, color=#89B4FA);
  font(color=#89B4FA, font-size=11px, weight=bold, align=center,
       text="Input",
       pos=(20 + 60, row_y + 25));
  font(color=#6C7086, font-size=10px, align=center,
       text="source data",
       pos=(20 + 60, row_y + 42));

  var cx1, cy1, cw1;
  cx1 = col1.bbox.x;
  cy1 = col1.bbox.y;
  cw1 = col1.bbox.width;

  # Arrow to Column 2
  connector(color=#89B4FA, line-width=2px,
            start=(cx1 + cw1, row_y + row_h / 2),
            end=(cx1 + cw1 + gap, row_y + row_h / 2),
            end-cap=triangle, cap-size=small);

  # ── Column 2: Transform ───────────────────────────────────────────────
  col2 = square(pos=(cx1 + cw1 + gap, row_y), width=130, height=row_h,
                fill=#313244, color=#A6E3A1);
  font(color=#A6E3A1, font-size=11px, weight=bold, align=center,
       text="Transform",
       pos=(cx1 + cw1 + gap + 65, row_y + 25));
  font(color=#6C7086, font-size=10px, align=center,
       text="process / map",
       pos=(cx1 + cw1 + gap + 65, row_y + 42));

  var cx2, cw2;
  cx2 = col2.bbox.x;
  cw2 = col2.bbox.width;

  connector(color=#A6E3A1, line-width=2px,
            start=(cx2 + cw2, row_y + row_h / 2),
            end=(cx2 + cw2 + gap, row_y + row_h / 2),
            end-cap=triangle, cap-size=small);

  # ── Column 3: Validate ────────────────────────────────────────────────
  col3 = square(pos=(cx2 + cw2 + gap, row_y), width=115, height=row_h,
                fill=#313244, color=#FAB387);
  font(color=#FAB387, font-size=11px, weight=bold, align=center,
       text="Validate",
       pos=(cx2 + cw2 + gap + 57, row_y + 25));
  font(color=#6C7086, font-size=10px, align=center,
       text="check / verify",
       pos=(cx2 + cw2 + gap + 57, row_y + 42));

  var cx3, cw3;
  cx3 = col3.bbox.x;
  cw3 = col3.bbox.width;

  connector(color=#FAB387, line-width=2px,
            start=(cx3 + cw3, row_y + row_h / 2),
            end=(cx3 + cw3 + gap, row_y + row_h / 2),
            end-cap=triangle, cap-size=small);

  # ── Column 4: Output ──────────────────────────────────────────────────
  col4 = square(pos=(cx3 + cw3 + gap, row_y), width=110, height=row_h,
                fill=#313244, color=#F38BA8);
  font(color=#F38BA8, font-size=11px, weight=bold, align=center,
       text="Output",
       pos=(cx3 + cw3 + gap + 55, row_y + 25));
  font(color=#6C7086, font-size=10px, align=center,
       text="result / emit",
       pos=(cx3 + cw3 + gap + 55, row_y + 42));

  var cx4, cw4;
  cx4 = col4.bbox.x;
  cw4 = col4.bbox.width;

  # ── Summary circle centred on the full pipeline row ───────────────────
  # Centre x = midpoint between left edge of col1 and right edge of col4
  var pipeline_cx, pipeline_cy;
  pipeline_cx = (cx1 + cx4 + cw4) / 2;
  pipeline_cy = row_y + row_h + 45;

  circle(color=#CDD6F4, fill=none, line-width=2px, line-type=dashed,
         center=(pipeline_cx, pipeline_cy), radius=28);
  font(color=#CDD6F4, font-size=12px, align=center,
       text="pipeline", pos=(pipeline_cx, pipeline_cy + 5));

  # Dashed bracket lines from summary circle to first and last columns
  line(color=#6C7086, line-type=dashed, line-width=1px,
       start=(cx1, row_y + row_h), end=(pipeline_cx - 20, pipeline_cy - 28));
  line(color=#6C7086, line-type=dashed, line-width=1px,
       start=(cx4 + cw4, row_y + row_h), end=(pipeline_cx + 20, pipeline_cy - 28));

  font(color=#6C7086, font-size=10px,
       text="pipeline_cx = (cx1 + cx4 + cw4) / 2",
       pos=(20, 245));
  font(color=#6C7086, font-size=10px,
       text="All positions computed from .bbox — no hard-coded X coordinates",
       pos=(20, 260));
end_frame
