begin_frame uml_number_class
  image width=900px; height=650px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F5F7FA);

  square(color=black, line-width=2px, fill=white, pos=(220,90), width=460px, height=460px);

  font(font-family="Arial", font-size=30px, color=black, weight=bold, align=center,
       text="Number", pos=(450,135));

  line(color=black, line-width=2px, start=(220,165), end=(680,165));

  font(font-family="Consolas", font-size=18px, color=black,
       text="- value : float | real | integer\n- value_type : NumberType",
       pos=(250,205));

  line(color=black, line-width=2px, start=(220,275), end=(680,275));

  font(font-family="Consolas", font-size=17px, color=black,
       text="+ set(value, type) : void\n+ get() : value\n+ get_type() : NumberType\n+ convert_to(type) : Number\n+ add(other) : Number\n+ subtract(other) : Number\n+ multiply(other) : Number\n+ divide(other) : Number\n+ compare(other) : ComparisonResult",
       pos=(250,315));

  font(font-family="Arial", font-size=18px, color=#333333, align=center,
       text="UML-style class entity: private storage + public interfaces/operators",
       pos=(450,600));
end_frame