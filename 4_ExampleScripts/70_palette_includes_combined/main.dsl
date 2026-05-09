include "lib/color_palette.dsl"
include "lib/object_library.dsl"

begin_frame includes_combined
  image width=800px; height=450px; colorspace=RGB; dpi=96; output-format=png;
  background(color=@bg);
  card(pos=(60,80), width=220px, height=220px, title="Metrics", value="92%", title_pos=(20,40), value_pos=(20,100));
  card(pos=(300,80), width=220px, height=220px, title="Traffic", value="1.4M", title_pos=(20,40), value_pos=(20,100));
  card(pos=(540,80), width=220px, height=220px, title="Alerts", value="3", title_pos=(20,40), value_pos=(20,100));
  font(color=@text, font-size=24px, text="Combined Palette + Objects", pos=(60,40));
end_frame
