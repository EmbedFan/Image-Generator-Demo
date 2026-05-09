# 06_simple_pie.dsl
# Category 1 - Basic Primitives
# Demonstrates: pie primitive (filled sector) and arc primitive (curve only)
# Angles: 0 = rightward (3 o'clock), increasing clockwise.
# IMPORTANT: fill is NOT allowed on arc — not even fill=none.

begin_frame simple_pie
  image width=680px; height=440px; colorspace=RGB; dpi=600; output-format=png;
  background(color=white);

  # ============================================================
  # Section 1: Pie slices — filled sector (arc + two radii)
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Pie slices (filled sectors)", pos=(20, 22));

  # Quarter slice (0-90 deg, top-right quadrant)
  pie(color=black, fill=red,    center=(80,  100), radius=60, start-angle=0,   end-angle=90);
  font(font-family="Arial", font-size=11px, color=darkgray, text="0-90", pos=(55, 175));

  # Half slice (0-180 deg, right half)
  pie(color=black, fill=orange, center=(220, 100), radius=60, start-angle=0,   end-angle=180);
  font(font-family="Arial", font-size=11px, color=darkgray, text="0-180", pos=(192, 175));

  # Three-quarter slice (0-270 deg)
  pie(color=black, fill=gold,   center=(360, 100), radius=60, start-angle=0,   end-angle=270);
  font(font-family="Arial", font-size=11px, color=darkgray, text="0-270", pos=(332, 175));

  # Full circle as pie (0-360 deg)
  pie(color=black, fill=lime,   center=(500, 100), radius=60, start-angle=0,   end-angle=360);
  font(font-family="Arial", font-size=11px, color=darkgray, text="0-360", pos=(472, 175));

  # ============================================================
  # Section 2: A pie chart built from slices
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Pie chart (composed slices)", pos=(20, 210));

  # Slice 1: 30% = 108 deg
  pie(color=white, fill=tomato,       center=(130, 320), radius=90, start-angle=0,   end-angle=108);
  # Slice 2: 25% = 90 deg
  pie(color=white, fill=cornflowerblue, center=(130, 320), radius=90, start-angle=108, end-angle=198);
  # Slice 3: 20% = 72 deg
  pie(color=white, fill=gold,         center=(130, 320), radius=90, start-angle=198, end-angle=270);
  # Slice 4: 15% = 54 deg
  pie(color=white, fill=lime,         center=(130, 320), radius=90, start-angle=270, end-angle=324);
  # Slice 5: 10% = 36 deg
  pie(color=white, fill=plum,         center=(130, 320), radius=90, start-angle=324, end-angle=360);

  # Legend
  square(color=transparent, fill=tomato,        pos=(250, 250), width=14px, height=14px);
  font(font-family="Arial", font-size=12px, color=black, text="30%", pos=(270, 263));
  square(color=transparent, fill=cornflowerblue, pos=(250, 272), width=14px, height=14px);
  font(font-family="Arial", font-size=12px, color=black, text="25%", pos=(270, 285));
  square(color=transparent, fill=gold,           pos=(250, 294), width=14px, height=14px);
  font(font-family="Arial", font-size=12px, color=black, text="20%", pos=(270, 307));
  square(color=transparent, fill=lime,           pos=(250, 316), width=14px, height=14px);
  font(font-family="Arial", font-size=12px, color=black, text="15%", pos=(270, 329));
  square(color=transparent, fill=plum,           pos=(250, 338), width=14px, height=14px);
  font(font-family="Arial", font-size=12px, color=black, text="10%", pos=(270, 351));

  # ============================================================
  # Section 3: Arcs — curve segment only, no fill allowed
  # ============================================================
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Arcs (curve only, no fill)", pos=(370, 210));

  # Solid arc, upper half
  arc(color=black, line-width=2px,
      center=(450, 320), radius=60, start-angle=180, end-angle=360);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="solid 180-360", pos=(400, 395));

  # Dashed arc, lower half
  arc(color=blue, line-width=2px, line-type=dashed,
      center=(580, 320), radius=60, start-angle=0, end-angle=180);
  font(font-family="Arial", font-size=11px, color=darkgray,
       text="dashed 0-180", pos=(530, 395));

end_frame
