# ------------------------------------------------------------
# File: 37_diagram_architecture.dsl
# Purpose:
#   Demonstrates a system architecture diagram using panels, labels,
#   and directional connectors.
# ------------------------------------------------------------

begin_frame diagram_architecture
  image width=900px; height=420px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F8F9F9)

  font(color=#1F2D3A, font-size=18px, weight=bold,
       text="System Architecture Diagram", pos=(30,28))

  square(color=#2E86C1, line-width=3px, fill=#D6EAF8, pos=(40,100), width=170px, height=90px)
  font(color=#1B4F72, font-size=15px, weight=bold, text="Client App", pos=(88,138))

  square(color=#28B463, line-width=3px, fill=#D5F5E3, pos=(280,100), width=170px, height=90px)
  font(color=#145A32, font-size=15px, weight=bold, text="API Gateway", pos=(320,138))

  square(color=#AF7AC5, line-width=3px, fill=#EBDEF0, pos=(520,100), width=170px, height=90px)
  font(color=#512E5F, font-size=15px, weight=bold, text="Service Layer", pos=(554,138))

  square(color=#F39C12, line-width=3px, fill=#FCF3CF, pos=(740,100), width=120px, height=90px)
  font(color=#7E5109, font-size=15px, weight=bold, text="DB", pos=(785,138))

  square(color=#16A085, line-width=3px, fill=#D1F2EB, pos=(520,250), width=170px, height=90px)
  font(color=#0E6251, font-size=15px, weight=bold, text="Cache Layer", pos=(550,288))

  connector(color=#34495E, line-width=3px, start=(210,145), end=(280,145), end-cap=triangle)
  connector(color=#34495E, line-width=3px, start=(450,145), end=(520,145), end-cap=triangle)
  connector(color=#34495E, line-width=3px, start=(690,145), end=(740,145), end-cap=triangle)
  connector(color=#34495E, line-width=3px, start=(605,190), end=(605,250), end-cap=triangle)
end_frame
