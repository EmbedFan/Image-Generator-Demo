begin_obj panel
  width: 180px;
  height: 100px;
  background: white;
  border: solid 1px gray;
  shadow: 4px 4px 6px RGBA(0,0,0,0.25);
  square(fill=background, color=black, pos=(0,0), width=width, height=height, line-width=2px, shadow=shadow);
  font(font-family="Arial", font-size=12px, color=black, weight=bold,
       text=label, pos=(10,15));
  line(color=gray, line-width=1px, start=(0,30), end=(180,30));
end_obj

begin_frame object_ui_panel
  image width=400px; height=300px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  # Place panel instances
  panel(pos=(50,10), label="Panel 1");
  panel(pos=(50,130), background=lightyellow, height=120px, label="Yes / No panel", rotate=350);

  # Add label
  font(font-family="Arial", font-size=16px, color=black, text="UI Panel Objects", pos=(120,270));
end_frame