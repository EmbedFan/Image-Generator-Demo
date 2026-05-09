# ------------------------------------------------------------
# File: 38_diagram_flowchart.dsl
# Purpose:
#   Demonstrates a process flowchart with decisions and routed connectors.
# ------------------------------------------------------------

begin_frame diagram_flowchart
  image width=760px; height=520px; colorspace=RGB; dpi=96; output-format=png
  background(color=white)

  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="Process Flowchart", pos=(25,25))

  square(color=#2C3E50, line-width=2px, fill=#D6EAF8, pos=(290,70), width=180px, height=60px)
  font(color=#1B4F72, font-size=15px, text="Start Request", pos=(336,92))

  polygon(color=#2C3E50, line-width=2px, fill=#FCF3CF,
          points=[(360,170),(450,230),(360,290),(270,230)])
  font(color=#7D6608, font-size=15px, text="Valid?", pos=(336,223))

  square(color=#2C3E50, line-width=2px, fill=#D5F5E3, pos=(80,360), width=180px, height=60px)
  font(color=#196F3D, font-size=15px, text="Reject Request", pos=(116,382))

  square(color=#2C3E50, line-width=2px, fill=#EBDEF0, pos=(500,360), width=180px, height=60px)
  font(color=#633974, font-size=15px, text="Process Request", pos=(532,382))

  connector(color=#34495E, line-width=3px, start=(380,130), end=(380,170), end-cap=triangle)
  connector(color=#34495E, line-width=3px, connector-type=step,
            start=(292,230), end=(260,390), corner=rounded, corner-radius=14px,
            end-cap=triangle)
  connector(color=#34495E, line-width=3px, connector-type=step,
            start=(448,230), end=(500,390), corner=rounded, corner-radius=14px,
            end-cap=triangle)

  font(color=#566573, font-size=12px, text="No", pos=(215,255))
  font(color=#566573, font-size=12px, text="Yes", pos=(458,255))
end_frame
