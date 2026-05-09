# 72_vars_bbox_access.dsl
# Category 14 — Variables and Layout Chaining
# Demonstrates: naming a primitive with 'name = primitive(...)' and reading
# .bbox.x, .bbox.y, .bbox.width, .bbox.height to position subsequent elements.

begin_frame vars_bbox_access
  image width=620px; height=270px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#FAFAFA);

  # Draw and name a rectangle — renders immediately; bbox is now readable
  mainbox = square(color=#2C3E50, fill=#3498DB,
                   pos=(50, 80), width=160px, height=70px);

  # Read all four bbox properties into variables
  var bx, by, bw, bh;
  bx = mainbox.bbox.x;
  by = mainbox.bbox.y;
  bw = mainbox.bbox.width;
  bh = mainbox.bbox.height;

  # Label centred inside the box using computed bbox values
  font(color=white, font-size=14px, weight=bold, align=center,
       text="mainbox",
       pos=(bx + bw / 2, by + bh / 2 + 5));

  # Red dot at top-left corner (bbox origin)
  circle(color=#E74C3C, fill=#E74C3C, center=(bx, by), radius=5);
  font(color=#E74C3C, font-size=10px,
       text="(bx, by)",
       pos=(bx + 8, by - 6));

  # Green dot at bottom-right corner
  circle(color=#27AE60, fill=#27AE60, center=(bx + bw, by + bh), radius=5);
  font(color=#27AE60, font-size=10px,
       text="(bx+bw, by+bh)",
       pos=(bx + bw - 88, by + bh + 13));

  # Dashed line showing width dimension below the box
  line(color=#E67E22, line-type=dashed, line-width=1px,
       start=(bx, by + bh + 28), end=(bx + bw, by + bh + 28));
  font(color=#E67E22, font-size=11px, align=center,
       text="bw = 160 px",
       pos=(bx + bw / 2, by + bh + 42));

  # Dashed line showing height on the left
  line(color=#8E44AD, line-type=dashed, line-width=1px,
       start=(bx - 28, by), end=(bx - 28, by + bh));
  font(color=#8E44AD, font-size=11px,
       text="bh=70",
       pos=(bx - 56, by + bh / 2));

  # Second box placed immediately after the first using bbox data
  nextbox = square(color=#8E44AD, fill=#9B59B6,
                   pos=(bx + bw + 25, by), width=bw, height=bh);
  font(color=white, font-size=13px, weight=bold, align=center,
       text="nextbox",
       pos=(bx + bw + 25 + bw / 2, by + bh / 2 + 5));
  font(color=#9B59B6, font-size=10px,
       text="pos.x = bx + bw + 25",
       pos=(bx + bw + 25, by + bh + 13));

  font(color=#2C3E50, font-size=14px, weight=bold,
       text="Category 14: Variables — .bbox Property Access",
       pos=(30, 240));
end_frame
