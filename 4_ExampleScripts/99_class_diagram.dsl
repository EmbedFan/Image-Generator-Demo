begin_frame number_python_class_diagram
  image width=1100px; height=900px; colorspace=RGB; dpi=96; output-format=png;
  background(color=#F5F7FA);

  square(color=black, line-width=2px, fill=white, pos=(180,70), width=740px, height=760px);

  font(font-family="Arial", font-size=32px, color=black, weight=bold, align=center,
       text="Number", pos=(550,125));

  line(color=black, line-width=2px, start=(180,160), end=(920,160));

  font(font-family="Consolas", font-size=18px, color=black,
       text="+ AllowedTypes : tuple = (\"integer\", \"float\", \"real\")\n- __value : int | float\n- __value_type : str",
       pos=(215,205));

  line(color=black, line-width=2px, start=(180,300), end=(920,300));

  font(font-family="Consolas", font-size=16px, color=black,
       text="+ __init__(value=0, value_type=\"integer\")\n+ Set(value, value_type) : void\n+ Get() : int | float\n+ GetType() : str\n+ ConvertTo(target_type) : Number\n+ Add(other) : Number\n+ Subtract(other) : Number\n+ Multiply(other) : Number\n+ Divide(other) : Number\n+ Compare(other) : int\n+ __add__(other) : Number\n+ __sub__(other) : Number\n+ __mul__(other) : Number\n+ __truediv__(other) : Number\n+ __eq__(other) : bool\n+ __lt__(other) : bool\n+ __le__(other) : bool\n+ __gt__(other) : bool\n+ __ge__(other) : bool\n+ __repr__() : str\n- __ConvertRaw(value, value_type) : int | float\n- __EnsureNumber(value) : Number\n- __ResultType(other) : str",
       pos=(215,345));

  font(font-family="Arial", font-size=18px, color=#333333, align=center,
       text="UML class diagram generated from the Python Number class",
       pos=(550,870));
end_frame