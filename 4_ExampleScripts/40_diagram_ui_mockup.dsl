# ------------------------------------------------------------
# File: 40_diagram_ui_mockup.dsl
# Purpose:
#   Demonstrates a UI mockup using multiple reusable panels and controls.
# ------------------------------------------------------------

begin_obj card
  width: 220px;
  height: 120px;
  square(color=#D5D8DC, line-width=2px, fill=white, pos=(0,0), width=220px, height=120px)
end_obj

begin_frame diagram_ui_mockup
  image width=920px; height=520px; colorspace=RGB; dpi=96; output-format=png
  background(color=#F4F6F7)

  square(color=#2C3E50, line-width=0px, fill=#2C3E50, pos=(0,0), width=920px, height=70px)
  font(color=white, font-size=24px, weight=bold, text="Analytics Dashboard", pos=(28,22))

  square(color=#D5DBDB, line-width=1px, fill=#EBF5FB, pos=(0,70), width=220px, height=450px)
  font(color=#1F2D3A, font-size=16px, weight=bold, text="Navigation", pos=(28,98))
  square(color=#85C1E9, line-width=0px, fill=#D6EAF8, pos=(20,130), width=180px, height=38px)
  square(color=#85C1E9, line-width=0px, fill=#D6EAF8, pos=(20,180), width=180px, height=38px)
  square(color=#85C1E9, line-width=0px, fill=#D6EAF8, pos=(20,230), width=180px, height=38px)
  font(color=#1B4F72, font-size=14px, text="Overview", pos=(38,142))
  font(color=#1B4F72, font-size=14px, text="Reports", pos=(38,192))
  font(color=#1B4F72, font-size=14px, text="Settings", pos=(38,242))

  card(pos=(270,110))
  card(pos=(520,110))
  card(pos=(270,260))
  card(pos=(520,260))

  font(color=#566573, font-size=13px, text="Revenue", pos=(294,136))
  font(color=#566573, font-size=13px, text="Users", pos=(544,136))
  font(color=#566573, font-size=13px, text="Conversion", pos=(294,286))
  font(color=#566573, font-size=13px, text="Health", pos=(544,286))

  font(color=#1F2D3A, font-size=28px, weight=bold, text="$182K", pos=(310,174))
  font(color=#1F2D3A, font-size=28px, weight=bold, text="14.2K", pos=(562,174))
  font(color=#1F2D3A, font-size=28px, weight=bold, text="6.4%", pos=(314,324))
  font(color=#1F2D3A, font-size=28px, weight=bold, text="98.7%", pos=(556,324))
end_frame
