# ------------------------------------------------------------
# File: 48_example_dashboard.dsl
# Purpose:
#   Complete dashboard-like composition using objects, functions,
#   variables, palette, connectors, and charts.
# ------------------------------------------------------------

begin_palette dashboard_colors
  page_bg = #F4F6F7;
  panel_bg = white;
  panel_border = #D5DBDB;
  heading = #1F2D3A;
  muted = #5D6D7E;
  accent_blue = #3498DB;
  accent_green = #27AE60;
  accent_orange = #F39C12;
  accent_red = #E74C3C;
end_palette

begin_obj metric_card
  width: 160px;
  height: 92px;
  background: white;
  border: solid 1px #D5DBDB;
  square(color=#D5DBDB, fill=white, pos=(0,0), width=width, height=height, line-width=1px);
  font(color=@muted, font-size=12px, text=title, pos=(16,16));
  font(color=@heading, font-size=22px, weight=bold, text=value, pos=(16,40));
  circle(color=none, fill=accent, center=(132,46), radius=18);
end_obj

begin_func bar(x, y, label_text, value_h)
  square(color=@accent_blue, fill=@accent_blue, pos=(x, y - value_h), width=34px, height=value_h)
  font(color=@muted, font-size=11px, text=label_text, pos=(x + 6, y + 12))
end_func

begin_frame example_dashboard
  image width=980px; height=620px; colorspace=RGB; dpi=96; output-format=png
  background(color=@page_bg)

  square(color=#2C3E50, fill=#2C3E50, pos=(0,0), width=980px, height=72px)
  font(color=white, font-size=24px, weight=bold,
       text="Operations Dashboard", pos=(28,24))
  font(color=#D6EAF8, font-size=12px,
       text="Complete example: cards, chart, diagram, variables, connectors", pos=(30,48))

  metric_card(pos=(28,96), title="Orders", value="1,248", accent=@accent_blue)
  metric_card(pos=(210,96), title="Revenue", value="$84k", accent=@accent_green)
  metric_card(pos=(392,96), title="Alerts", value="12", accent=@accent_orange)
  metric_card(pos=(574,96), title="Incidents", value="3", accent=@accent_red)

  square(color=@panel_border, fill=@panel_bg, pos=(28,214), width=430px, height=330px)
  font(color=@heading, font-size=18px, weight=bold, text="Weekly Throughput", pos=(48,240))
  font(color=@muted, font-size=12px, text="Bar chart generated with a reusable function.", pos=(48,264))

  line(color=#AEB6BF, points=[(62,486),(426,486)], line-width=1px)
  line(color=#AEB6BF, points=[(62,316),(62,486)], line-width=1px)

  bar(92, 486, "Mon", 76)
  bar(146, 486, "Tue", 108)
  bar(200, 486, "Wed", 92)
  bar(254, 486, "Thu", 132)
  bar(308, 486, "Fri", 118)
  bar(362, 486, "Sat", 64)

  square(color=@panel_border, fill=@panel_bg, pos=(486,214), width=466px, height=330px)
  font(color=@heading, font-size=18px, weight=bold, text="Fulfillment Pipeline", pos=(506,240))
  font(color=@muted, font-size=12px, text="Named blocks plus connectors create a process overview.", pos=(506,264))

  ingest = square(color=#5DADE2, fill=#D6EAF8, pos=(522,320), width=110px, height=58px)
  pack = square(color=#58D68D, fill=#D5F5E3, pos=(694,320), width=110px, height=58px)
  ship = square(color=#F5B041, fill=#FCF3CF, pos=(694,432), width=110px, height=58px)
  audit = square(color=#AF7AC5, fill=#EBDEF0, pos=(522,432), width=110px, height=58px)

  font(color=@heading, font-size=14px, weight=bold, text="Ingest", pos=(552,340))
  font(color=@heading, font-size=14px, weight=bold, text="Pack", pos=(730,340))
  font(color=@heading, font-size=14px, weight=bold, text="Ship", pos=(730,452))
  font(color=@heading, font-size=14px, weight=bold, text="Audit", pos=(554,452))

  var start_x;
  var start_y;
  var end_x;
  var end_y;

  start_x = ingest.bbox.x + ingest.bbox.width;
  start_y = ingest.bbox.y + ingest.bbox.height / 2;
  end_x = pack.bbox.x;
  end_y = pack.bbox.y + pack.bbox.height / 2;
  connector(color=@accent_blue, start=(start_x, start_y), end=(end_x, end_y),
            connector-type=step, corner=rounded, corner-radius=10px,
            end-cap=filled-triangle, line-width=3px)

  start_x = pack.bbox.x + pack.bbox.width / 2;
  start_y = pack.bbox.y + pack.bbox.height;
  end_x = ship.bbox.x + ship.bbox.width / 2;
  end_y = ship.bbox.y;
  connector(color=@accent_green, start=(start_x, start_y), end=(end_x, end_y),
            connector-type=step, corner=rounded, corner-radius=10px,
            end-cap=filled-triangle, line-width=3px)

  start_x = ship.bbox.x;
  start_y = ship.bbox.y + ship.bbox.height / 2;
  end_x = audit.bbox.x + audit.bbox.width;
  end_y = audit.bbox.y + audit.bbox.height / 2;
  connector(color=@accent_orange, start=(start_x, start_y), end=(end_x, end_y),
            connector-type=step, corner=rounded, corner-radius=10px,
            end-cap=filled-triangle, line-width=3px)
end_frame
