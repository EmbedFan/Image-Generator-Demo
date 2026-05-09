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
  image width=300px; height=200px; colorspace=RGB; dpi=600; output-format=png;
  background(color=white);

  # first icon
  warning_icon(pos=(40,70), rotate=35);

  # second icon (rotated + scaled)
  warning_icon(pos=(150,60), rotate=50, scale=2.25);

end_frame