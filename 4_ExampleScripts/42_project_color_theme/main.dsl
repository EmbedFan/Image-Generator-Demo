include "lib/colors.dsl"
include "lib/styles.dsl"

begin_frame color_theme_project
  image width=760px; height=420px; colorspace=RGB; dpi=96; output-format=png
  background(color=@canvas)

  themed_panel(pos=(40,70), title="Theme Panel")
  themed_panel(pos=(410,70), title="Theme Chart")

  square(color=@accent, line-width=2px, fill=@accent-soft, pos=(80,150), width=260px, height=34px)
  square(color=@accent, line-width=2px, fill=@accent-soft, pos=(80,200), width=180px, height=34px)
  square(color=@accent, line-width=2px, fill=@accent-soft, pos=(80,250), width=220px, height=34px)

  font(color=@text-main, font-size=18px, weight=bold, text="Color Theme Project", pos=(40,30))
  font(color=@text-main, font-size=14px, text="Shared colors and shared object styles via include files.", pos=(40,340))
end_frame
