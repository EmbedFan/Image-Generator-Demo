# ------------------------------------------------------------
# File: 35_animation_color_transition.dsl
# Purpose:
#   Demonstrates color transition by changing fill colors across frames.
# ------------------------------------------------------------

begin_frame color_0
  hold-time=180; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#FBFCFC)
  square(color=#2C3E50, line-width=3px, fill=#85C1E9, pos=(110,50), width=200px, height=120px)
end_frame

begin_frame color_1
  hold-time=180; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#FBFCFC)
  square(color=#2C3E50, line-width=3px, fill=#82E0AA, pos=(110,50), width=200px, height=120px)
end_frame

begin_frame color_2
  hold-time=180; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#FBFCFC)
  square(color=#2C3E50, line-width=3px, fill=#F9E79F, pos=(110,50), width=200px, height=120px)
end_frame

begin_frame color_3
  hold-time=180; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#FBFCFC)
  square(color=#2C3E50, line-width=3px, fill=#F5B7B1, pos=(110,50), width=200px, height=120px)
end_frame
