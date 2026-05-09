begin_obj card
  width: 220px;
  height: 220px;
  square(color=@card_border, fill=@card_fill, pos=(0,0), width=width, height=height, line-width=2px);
  font(color=@title, font-size=18px, weight=bold, text=title, pos=title_pos);
  font(color=@value, font-size=34px, text=value, pos=value_pos);
end_obj

# Example of object reuse with palette-defined style values
# The main script passes title and value via object parameters.
