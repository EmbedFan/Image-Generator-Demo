# ------------------------------------------------------------
# File: 36_animation_position_sequence.dsl
# Purpose:
#   Demonstrates an object moving across frames by changing position.
# ------------------------------------------------------------

begin_obj marker
  width: 80px;
  height: 40px;
  square(color=#1F618D, line-width=2px, fill=#AED6F1, pos=(0,0), width=80px, height=40px)
  font(color=#154360, font-size=12px, text="MOVE", pos=(20,12))
end_obj

begin_frame seq_0
  hold-time=160; frame-mode=cyclic-run;
  image width=500px; height=180px; colorspace=RGB; dpi=96;
  background(color=white)
  line(color=#AAB7B8, line-width=2px, start=(40,110), end=(460,110))
  marker(pos=(50,70))
end_frame

begin_frame seq_1
  hold-time=160; frame-mode=cyclic-run;
  image width=500px; height=180px; colorspace=RGB; dpi=96;
  background(color=white)
  line(color=#AAB7B8, line-width=2px, start=(40,110), end=(460,110))
  marker(pos=(160,70))
end_frame

begin_frame seq_2
  hold-time=160; frame-mode=cyclic-run;
  image width=500px; height=180px; colorspace=RGB; dpi=96;
  background(color=white)
  line(color=#AAB7B8, line-width=2px, start=(40,110), end=(460,110))
  marker(pos=(270,70))
end_frame

begin_frame seq_3
  hold-time=160; frame-mode=cyclic-run;
  image width=500px; height=180px; colorspace=RGB; dpi=96;
  background(color=white)
  line(color=#AAB7B8, line-width=2px, start=(40,110), end=(460,110))
  marker(pos=(380,70))
end_frame
