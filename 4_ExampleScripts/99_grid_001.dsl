begin_frame grid_demo

image width=600px; height=400px; colorspace=RGB; dpi=96; output-format=png;

background(color=white);

# --- Section A: 50px coarse grid, global align=true, default align-origin
# Squares use left-top origin (default), circles use center origin (default)
grid(
  step-x=50px,
  step-y=50px,
  render=true,
  color=lightgray,
  line-width=1px,
  align=true
);

# align-origin=left-top (default for squares): pos (63,48) → snaps to (50,50)
square(
  color=black,
  fill=red,
  pos=(63,48),
  width=40px,
  height=40px
);

# align-origin=center (default for circles): center (112,52) → snaps to (100,50)
circle(
  color=black,
  fill=blue,
  center=(112,52),
  radius=20px
);

# align=false overrides global align — text stays at raw position
font(
  color=black,
  font-family="DejaVu Sans",
  font-size=18px,
  text="no snap",
  pos=(162,36),
  align=false
);

# --- Section B: per-element align=true with explicit align-origin
# (global align is still true from first grid, but we show explicit origin)

# Snap right-bottom corner of this square to the grid
# right-bottom = (52+80, 97+40) = (132,137) → snaps to (150,150)
# new pos = (150-80, 150-40) = (70, 110)
square(
  color=darkblue,
  fill=lightblue,
  pos=(52,97),
  width=80px,
  height=40px,
  align=true,
  align-origin=right-bottom
);

# Snap left-top of bounding box of circle to grid
# left-top = center - radius = (295,178) - 20 = (275,158) → snaps to (300,150)
# new center = (300+20, 150+20) = (320, 170)
circle(
  color=black,
  fill=orange,
  center=(295,178),
  radius=20px,
  align=true,
  align-origin=left-top
);

# --- Section C: switch to finer 25px grid mid-frame
grid(
  step-x=25px,
  step-y=25px,
  render=true,
  color=silver,
  line-width=1px,
  line-type=dashed,
  align=true
);

# With 25px grid: pos (162,251) → snaps to (150,250)
square(
  color=black,
  fill=green,
  pos=(162,251),
  width=40px,
  height=40px
);

# Center (262,268) → snaps to (275,275)
circle(
  color=black,
  fill=red,
  center=(262,268),
  radius=15px
);

font(
  color=black,
  font-family="DejaVu Sans",
  font-size=14px,
  text="25px grid",
  pos=(320,260)
);

end_frame
