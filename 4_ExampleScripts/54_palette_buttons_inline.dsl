begin_palette palette
  button_bg    = #34495E
  button_fill  = #156e22
  button_text  = #FDFEFE
  border_color = #2C3E50
  panel_bg     = #ECF0F1
end_palette

begin_obj button
  width: 220px;
  height: 60px;
  square(color=@border_color, fill=@button_fill, pos=(0,0), width=220px, height=60px, line-width=3px);
  font(color=@button_text, font-size=16px, text=label, pos=label_pos);
end_obj

begin_frame buttons_inline
  image width=720px; height=420px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@panel_bg);
  button(pos=(80,80), label="Primary Action", label_pos=(20,18));
  button(pos=(80,170), label="Secondary Action", label_pos=(20,18));
  button(pos=(80,260), label="Cancel", label_pos=(20,18));
  font(color=@border_color, font-size=18px, text="Palette Buttons Inline", pos=(80,40));
end_frame
