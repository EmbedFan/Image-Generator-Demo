# ------------------------------------------------------------
# File: 39_diagram_network_topology.dsl
# Purpose:
#   Demonstrates a network topology diagram with core, edge, and clients.
# ------------------------------------------------------------

begin_frame diagram_network_topology
  image width=860px; height=440px; colorspace=RGB; dpi=96; output-format=png
  background(color=#FDFEFE)

  font(color=#212F3C, font-size=18px, weight=bold,
       text="Network Topology", pos=(28,28))

  circle(color=#1F618D, line-width=3px, fill=#D6EAF8, center=(430,90), radius=42)
  font(color=#1B4F72, font-size=14px, weight=bold, text="Core", pos=(411,88))

  square(color=#117A65, line-width=3px, fill=#D1F2EB, pos=(160,190), width=120px, height=70px)
  square(color=#117A65, line-width=3px, fill=#D1F2EB, pos=(370,190), width=120px, height=70px)
  square(color=#117A65, line-width=3px, fill=#D1F2EB, pos=(580,190), width=120px, height=70px)
  font(color=#0B5345, font-size=14px, text="Edge A", pos=(193,218))
  font(color=#0B5345, font-size=14px, text="Edge B", pos=(403,218))
  font(color=#0B5345, font-size=14px, text="Edge C", pos=(613,218))

  circle(color=#884EA0, line-width=2px, fill=#F5EEF8, center=(110,350), radius=24)
  circle(color=#884EA0, line-width=2px, fill=#F5EEF8, center=(250,350), radius=24)
  circle(color=#884EA0, line-width=2px, fill=#F5EEF8, center=(390,350), radius=24)
  circle(color=#884EA0, line-width=2px, fill=#F5EEF8, center=(530,350), radius=24)
  circle(color=#884EA0, line-width=2px, fill=#F5EEF8, center=(670,350), radius=24)
  circle(color=#884EA0, line-width=2px, fill=#F5EEF8, center=(810,350), radius=24)

  connector(color=#34495E, line-width=3px, start=(430,132), end=(220,190), end-cap=triangle)
  connector(color=#34495E, line-width=3px, start=(430,132), end=(430,190), end-cap=triangle)
  connector(color=#34495E, line-width=3px, start=(430,132), end=(640,190), end-cap=triangle)

  connector(color=#7D3C98, line-width=2px, start=(220,260), end=(110,326), end-cap=triangle)
  connector(color=#7D3C98, line-width=2px, start=(220,260), end=(250,326), end-cap=triangle)
  connector(color=#7D3C98, line-width=2px, start=(430,260), end=(390,326), end-cap=triangle)
  connector(color=#7D3C98, line-width=2px, start=(430,260), end=(530,326), end-cap=triangle)
  connector(color=#7D3C98, line-width=2px, start=(640,260), end=(670,326), end-cap=triangle)
  connector(color=#7D3C98, line-width=2px, start=(640,260), end=(810,326), end-cap=triangle)
end_frame
