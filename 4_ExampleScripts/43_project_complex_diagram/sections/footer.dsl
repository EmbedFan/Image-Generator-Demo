begin_func draw_footer(x, y)
  line(color=#AAB7B8, line-width=1px, start=(x, y), end=(x + 840, y))
  font(color=#7B7D7D, font-size=11px,
       text="Footer section imported from sections/footer.dsl", pos=(x, y + 12))
end_func
