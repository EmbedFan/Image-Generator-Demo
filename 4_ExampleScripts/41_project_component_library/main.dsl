include "lib/components.dsl"

begin_frame component_library_demo
  image width=760px; height=360px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F8F9F9)

  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="Project 41: Component Library", pos=(24,26))

  panel_card(pos=(40,80), title="Server A", subtitle="Healthy")
  panel_card(pos=(280,80), title="Server B", subtitle="Warning")
  panel_card(pos=(520,80), title="Server C", subtitle="Healthy")

  action_button(pos=(280,250), label="Deploy")
end_frame
