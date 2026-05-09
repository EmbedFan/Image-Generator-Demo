# ------------------------------------------------------------
# File: 33_animation_bouncing_ball.dsl
# Purpose:
#   Demonstrates a multi-frame bouncing ball animation.
# ------------------------------------------------------------

begin_frame ball_0
  hold-time=160; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#F4F6F7)
  line(color=#7F8C8D, line-width=2px, start=(20,180), end=(400,180))
  circle(color=#1B4F72, line-width=2px, fill=#5DADE2, center=(70,80), radius=22)
end_frame

begin_frame ball_1
  hold-time=160; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#F4F6F7)
  line(color=#7F8C8D, line-width=2px, start=(20,180), end=(400,180))
  circle(color=#1B4F72, line-width=2px, fill=#5DADE2, center=(140,130), radius=22)
end_frame

begin_frame ball_2
  hold-time=160; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#F4F6F7)
  line(color=#7F8C8D, line-width=2px, start=(20,180), end=(400,180))
  circle(color=#1B4F72, line-width=2px, fill=#5DADE2, center=(210,158), radius=22)
end_frame

begin_frame ball_3
  hold-time=160; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#F4F6F7)
  line(color=#7F8C8D, line-width=2px, start=(20,180), end=(400,180))
  circle(color=#1B4F72, line-width=2px, fill=#5DADE2, center=(280,118), radius=22)
end_frame

begin_frame ball_4
  hold-time=160; frame-mode=cyclic-run;
  image width=420px; height=220px; colorspace=RGB; dpi=96;
  background(color=#F4F6F7)
  line(color=#7F8C8D, line-width=2px, start=(20,180), end=(400,180))
  circle(color=#1B4F72, line-width=2px, fill=#5DADE2, center=(350,78), radius=22)
end_frame
