begin_obj button
  width: 120px;
  height: 40px;
  background: lightblue;
  border: solid 2px black;
  square(fill=background, color=black, pos=(0,0), width=width, height=height, line-width=2px);
  font(font-family="Arial", font-size=14px, color=black, weight=bold, text=label, pos=(20,12));
end_obj

begin_frame object_simple_button
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Place multiple button instances
  button(pos=(50,50), label="Ok");
  button(pos=(200,50), background=lightgreen, label="Help");
  button(pos=(50,120), background=lightcoral, label="Cancel");

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="Reusable Button Objects", pos=(100,250));
end_frame