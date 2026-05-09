# ------------------------------------------------------------
# File: 49_example_technical_diagram.dsl
# Purpose:
#   Complete technical illustration combining objects, functions,
#   connectors, transforms, and layout annotations.
# ------------------------------------------------------------

begin_obj module_box
  width: 170px;
  height: 82px;
  background: white;
  border: solid 2px #5D6D7E;
  shadow: 3px 3px 5px RGBA(0,0,0,0.18);
  square(color=#5D6D7E, fill=white, pos=(0,0), width=width, height=height, line-width=2px);
  square(color=none, fill=band_color, pos=(0,0), width=width, height=18px);
  font(color=#1F2D3A, font-size=14px, weight=bold, text=title, pos=(14,30));
  font(color=#566573, font-size=11px, text=subtitle, pos=(14,52));
end_obj

begin_func port(x, y, label_text, fill_color)
  circle(color=#2C3E50, fill=fill_color, center=(x, y), radius=10)
  font(color=#2C3E50, font-size=11px, text=label_text, pos=(x + 14, y - 5))
end_func

begin_frame example_technical_diagram
  image width=1040px; height=640px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F8F9F9)

  font(color=#1F2D3A, font-size=24px, weight=bold,
       text="Technical Illustration: Sensor Gateway Topology", pos=(28,28))
  font(color=#5D6D7E, font-size=12px,
       text="Complete example combining modules, ports, transformed callouts, and connector styles.",
       pos=(30,56))

  module_box(pos=(90,140), title="Sensor Bank A", subtitle="Temperature / Pressure", band_color=#AED6F1)
  module_box(pos=(90,330), title="Sensor Bank B", subtitle="Flow / Vibration", band_color=#D5F5E3)
  module_box(pos=(420,236), title="Edge Gateway", subtitle="Protocol normalization", band_color=#FCF3CF)
  module_box(pos=(760,236), title="Cloud Ingest", subtitle="Message validation", band_color=#FADBD8)

  port(282, 181, "A-Out", blue)
  port(282, 371, "B-Out", green)
  port(410, 277, "In-1", orange)
  port(410, 315, "In-2", orange)
  port(602, 277, "Upstream", gold)
  port(750, 277, "API", red)

  connector(color=#3498DB, points=[(282,181),(410,277)],
            connector-type=curved, end-cap=filled-triangle, line-width=3px,
            label="Sensor stream A", label-pos=center, label-font-size=11px,
            label-font-color=#1F618D)

  connector(color=#27AE60, points=[(282,371),(410,315)],
            connector-type=curved, end-cap=filled-triangle, line-width=3px,
            label="Sensor stream B", label-pos=center, label-font-size=11px,
            label-font-color=#117864)

  connector(color=#E67E22, points=[(602,277),(750,277)],
            connector-type=straight, start-cap=filled-circle, end-cap=filled-triangle,
            line-width=4px, pattern=dash, pattern-color=#E67E22, pattern-length=12px, pattern-gap=8px,
            label="Normalized event bus", label-pos=center, label-font-size=11px,
            label-font-color=#AF601A)

  polygon(color=#7D3C98, fill=RGBA(155,89,182,0.18),
          points=[(642,118),(712,118),(734,164),(620,164)], rotate=352)
  font(color=#7D3C98, font-size=12px, weight=bold,
       text="Encrypted channel", pos=(632,132), rotate=352)

  square(color=#D5DBDB, fill=white, pos=(760,384), width=210px, height=150px)
  font(color=#1F2D3A, font-size=16px, weight=bold, text="Legend", pos=(784,410))
  line(color=#3498DB, points=[(784,446),(838,446)], line-width=3px)
  font(color=#566573, font-size=11px, text="Curved sensor feed", pos=(852,439))
  line(color=#E67E22, points=[(784,478),(838,478)], line-width=4px, line-type=dashed)
  font(color=#566573, font-size=11px, text="Dashed event bus", pos=(852,471))
  square(color=#5D6D7E, fill=white, pos=(784,500), width=24px, height=16px, line-width=2px)
  font(color=#566573, font-size=11px, text="Module component", pos=(852,499))
end_frame
