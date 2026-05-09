begin_obj warning_icon
  polygon(color=black, line-width=3px, fill=yellow,
          points=[(48,6),(90,84),(6,84)]);

  square(color=black, line-width=1px, fill=black,
         pos=(45,32), width=8px, height=30px);

  square(color=black, line-width=1px, fill=black,
         pos=(45,68), width=8px, height=8px);
end_obj


begin_obj error_icon_1
  # Red octagon (stop sign)
  polygon(
    color=black,
    line-width=2px,
    fill=red,
    points=[
      (22,4),(42,4),(60,22),(60,42),
      (42,60),(22,60),(4,42),(4,22)
    ]
  );

  # White cross (X)

  # diagonal 1
  polygon(
    color=white,
    fill=white,
    points=[
      (20,16),(24,12),(44,32),(40,36)
    ]
  );

  # diagonal 2
  polygon(
    color=white,
    fill=white,
    points=[
      (40,16),(44,20),(24,40),(20,36)
    ]
  );
end_obj


begin_obj error_icon
  # Red octagon
  polygon(
    color=white,
    line-width=3px,
    fill=red,
    points=[
      (22,4),(42,4),(60,22),(60,42),
      (42,60),(22,60),(4,42),(4,22)
    ]
  );

  # STOP text (centered)
  font(
    font-family="DejaVu Sans",
    font-size=16px,
    color=white,
    weight=bold,
    align=center,
    text="STOP",
    pos=(8,23)
  );
end_obj


begin_obj info_icon
  # Blue circle
  circle(
    color=black,
    line-width=2px,
    fill=blue,
    center=(32,32),
    radius=28
  );

  # Yellow "I" using font (baseline-centered tuning)
  font(
    font-family="DejaVu Sans",
    font-size=48px,
    color=yellow,
    weight=bold,
    align=center,
    text="i",
    pos=(25,6)
  );
end_obj

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

  # warning_icon(pos=(90,138));
  # error_icon(pos=(90,138));
  info_icon(pos=(90,138));

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