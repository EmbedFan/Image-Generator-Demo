begin_obj info_panel
  width: 120px;
  height: 70px;
  background: lightyellow;
  border: solid 2px black;
  square(fill=background, color=black, pos=(0,0), width=width, height=height, line-width=2px);
  circle(color=black, fill=orange, center=(18,18), radius=8, line-width=1px);
  font(font-family="Arial", font-size=12px, color=black, weight=bold, text=label, pos=(34,14));
  font(font-family="Arial", font-size=10px, color=gray, text="Fixed icon size", pos=(34,34));
end_obj

begin_frame object_layout_resize_panel
  image width=940px; height=240px; colorspace=RGB; dpi=96; output-format=png;
  background(color=white);

  font(font-family="Arial", font-size=15px, color=black, weight=bold, text="Default resize scales the whole object", pos=(20,20));
  info_panel(pos=(20,50), width=240px, height=110px, label="Default scaled");

  font(font-family="Arial", font-size=15px, color=black, weight=bold, text="resize-mode=layout keeps the icon fixed", pos=(330,20));
  info_panel(pos=(330,50), width=240px, height=110px, resize-mode=layout, label="Layout resized");

  font(font-family="Arial", font-size=15px, color=black, weight=bold, text="layout resize plus explicit scale", pos=(650,20));
  info_panel(pos=(650,50), width=200px, height=90px, resize-mode=layout, scale=1.15, label="Layout + scale");
end_frame
