begin_obj button
  width: 80px;
  height: 30px;
  background: lightblue;
  border: solid 1px blue;
  square(fill=background, color=black, pos=(0,0), width=width, height=height, line-width=2px, shadow=shadow);
  font(font-family="Arial", font-size=10px, color=black, text="OK", pos=(30,8));
end_obj

begin_obj dialog
  width: 200px;
  height: 120px;
  background: white;
  border: solid 2px black;
  shadow: 4px 4px 8px RGBA(0,0,0,0.4);
  square(fill=background, color=black, pos=(0,0), width=width, height=height, line-width=2px, shadow=shadow);
  font(font-family="Arial", font-size=14px, color=black, weight=bold,
       text="Confirm Action", pos=(20,20));
  line(color=black, line-width=1px, start=(0,40), end=(200,40));
  # Nest the button inside the dialog
  button(pos=(60,60));
end_obj

begin_frame object_nested
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Place the nested dialog
  dialog(pos=(100,80));

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Nested Objects", pos=(140,270));
end_frame