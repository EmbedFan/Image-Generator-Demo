begin_obj warning_icon
  width: 64px; height: 64px;

  # triangle background
  polygon(color=black, line-width=2px, fill=yellow,
          points=[(32,4),(60,56),(4,56)]);

  # exclamation mark
  square(color=black, fill=black,
         pos=(30,20), width=4px, height=22px);

  square(color=black, fill=black,
         pos=(30,46), width=4px, height=4px);
end_obj


begin_frame warning_test
  image width=200px; height=200px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # rotated instance
  warning_icon(pos=(70,70), rotate=35);

end_frame