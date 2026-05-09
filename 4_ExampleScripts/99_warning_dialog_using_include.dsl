include "..\\5_Includes\\objectslib_001.dsl"

begin_frame warning_dialog
  image width=640px; height=390px; colorspace=RGB; dpi=600; output-format=png;
  # background(color=RGB(245,245,245));
  
  # Gradient background (left → right)
  background(
    color1=lightblue,
    color2=navy,
    start=(0,0),
    end=(640,0)
  );

  #square(color=gray, line-width=2px, fill=blue,
  #       pos=(70,90), width=500px, height=288px);

  square(color=gray, line-width=1px, fill=RGB(230,230,230),
         pos=(70,55), width=500px, height=62px);

  font(font-family="DejaVu Sans", font-size=20px, color=black,
       weight=bold, text="Figyelmeztetés", pos=(90,83));

  square(color=gray, line-width=1px, fill=white,
         pos=(70,110), width=500px, height=236px);

  warning_icon(pos=(90,138), width=85px, height=85px);
  # error_icon(pos=(90,138));
  # info_icon(pos=(90,138));

  font(font-family="DejaVu Sans", font-size=22px, color=black,
       weight=bold, text="Hiányzó távoli-gép definíció!", pos=(190,170));

  # Button Ok
  square(color=gray, line-width=2px, fill=RGB(240,240,240),
         pos=(130,285), width=120px, height=36px);
  font(font-family="DejaVu Sans", font-size=15px, color=black,
       weight=bold, align=center, text="Rendben", pos=(160,295));

  # Button Cancel
  square(color=gray, line-width=2px, fill=RGB(240,240,240),
         pos=(260,285), width=120px, height=36px);
  font(font-family="DejaVu Sans", font-size=15px, color=black,
       weight=bold, align=center, text="Mégsem", pos=(290,295));
	
  # Button Help
  square(color=gray, line-width=2px, fill=RGB(240,240,240),
         pos=(390,285), width=120px, height=36px);
  font(font-family="DejaVu Sans", font-size=15px, color=black,
       weight=bold, align=center, text="Súgó", pos=(430,295));

end_frame