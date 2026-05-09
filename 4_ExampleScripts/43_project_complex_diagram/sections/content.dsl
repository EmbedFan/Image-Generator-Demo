begin_func draw_content(x, y)
  input_box = square(color=#2E86C1, line-width=2px, fill=#D6EAF8, pos=(x + 20, y + 40), width=180px, height=90px)
  transform_box = square(color=#28B463, line-width=2px, fill=#D5F5E3, pos=(x + 280, y + 40), width=180px, height=90px)
  output_box = square(color=#AF7AC5, line-width=2px, fill=#EBDEF0, pos=(x + 540, y + 40), width=180px, height=90px)

  font(color=#1B4F72, font-size=15px, weight=bold, align=center,
       text="Input",
       pos=(input_box.bbox.x + input_box.bbox.width / 2,
            input_box.bbox.y + input_box.bbox.height / 2 - 8))
  font(color=#145A32, font-size=15px, weight=bold, align=center,
       text="Transform",
       pos=(transform_box.bbox.x + transform_box.bbox.width / 2,
            transform_box.bbox.y + transform_box.bbox.height / 2 - 8))
  font(color=#512E5F, font-size=15px, weight=bold, align=center,
       text="Output",
       pos=(output_box.bbox.x + output_box.bbox.width / 2,
            output_box.bbox.y + output_box.bbox.height / 2 - 8))

  connector(color=#34495E, line-width=3px,
            start=(input_box.bbox.x + input_box.bbox.width,
                   input_box.bbox.y + input_box.bbox.height / 2),
            end=(transform_box.bbox.x,
                 transform_box.bbox.y + transform_box.bbox.height / 2),
            end-cap=triangle)
  connector(color=#34495E, line-width=3px,
            start=(transform_box.bbox.x + transform_box.bbox.width,
                   transform_box.bbox.y + transform_box.bbox.height / 2),
            end=(output_box.bbox.x,
                 output_box.bbox.y + output_box.bbox.height / 2),
            end-cap=triangle)

  note_panel = square(color=#D5D8DC, line-width=2px, fill=white, pos=(x + 170, y + 190), width=400px, height=120px)

  var note_center_x;
  var note_line_1_y;
  var note_line_2_y;
  var note_line_3_y;

  note_center_x = note_panel.bbox.x + note_panel.bbox.width / 2;
  note_line_1_y = note_panel.bbox.y + 34;
  note_line_2_y = note_panel.bbox.y + 56;
  note_line_3_y = note_panel.bbox.y + 78;

  font(color=#566573, font-size=13px, align=center,
       text="The central annotation panel explains the data path",
       pos=(note_center_x, note_line_1_y))
  font(color=#566573, font-size=13px, align=center,
       text="and keeps the supporting notes inside the content pane",
       pos=(note_center_x, note_line_2_y))
  font(color=#566573, font-size=13px, align=center,
       text="with balanced padding on both the left and right.",
       pos=(note_center_x, note_line_3_y))
end_func
