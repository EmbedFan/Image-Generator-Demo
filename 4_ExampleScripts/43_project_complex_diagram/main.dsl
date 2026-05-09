include "sections/header.dsl"
include "sections/content.dsl"
include "sections/footer.dsl"

begin_frame complex_diagram_project
  image width=920px; height=520px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F8F9F9)

  draw_header(30, 24)
  draw_content(30, 90)
  draw_footer(30, 470)
end_frame
