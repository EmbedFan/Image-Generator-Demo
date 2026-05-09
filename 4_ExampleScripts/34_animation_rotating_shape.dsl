# ------------------------------------------------------------
# File: 34_animation_rotating_shape.dsl
# Purpose:
#   Demonstrates a rotating polygon across multiple frames.
# ------------------------------------------------------------

begin_frame rotor_0
  hold-time=180; frame-mode=cyclic-run;
  image width=360px; height=260px; colorspace=RGB; dpi=96;
  background(color=white)
  polygon(color=#8E44AD, line-width=3px, fill=#D2B4DE,
          points=[(180,50),(230,125),(180,210),(130,125)],
          rotate=0)
end_frame

begin_frame rotor_1
  hold-time=180; frame-mode=cyclic-run;
  image width=360px; height=260px; colorspace=RGB; dpi=96;
  background(color=white)
  polygon(color=#8E44AD, line-width=3px, fill=#D2B4DE,
          points=[(180,50),(230,125),(180,210),(130,125)],
          rotate=22)
end_frame

begin_frame rotor_2
  hold-time=180; frame-mode=cyclic-run;
  image width=360px; height=260px; colorspace=RGB; dpi=96;
  background(color=white)
  polygon(color=#8E44AD, line-width=3px, fill=#D2B4DE,
          points=[(180,50),(230,125),(180,210),(130,125)],
          rotate=44)
end_frame

begin_frame rotor_3
  hold-time=180; frame-mode=cyclic-run;
  image width=360px; height=260px; colorspace=RGB; dpi=96;
  background(color=white)
  polygon(color=#8E44AD, line-width=3px, fill=#D2B4DE,
          points=[(180,50),(230,125),(180,210),(130,125)],
          rotate=66)
end_frame
