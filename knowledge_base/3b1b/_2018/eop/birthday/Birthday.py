# Source: 3b1b/_2018/eop/birthday.py
# Description: [3b1b translated] 展示一個正方形隨著天數減少而逐漸縮小，直到其面積佔比低於50%的過程。



from manim import *
class Birthday(Scene):
    def construct(self):
        sidelength = 6.0
        corner = np.array([-sidelength/2, -sidelength/2, 0])
        nb_days_left = 365.0
        toggle = False

        def probability():
            width = rect.get_width()
            height = rect.get_height()
            return width * height / sidelength**2

        rect = Square().scale(sidelength/2)

        while probability() > 0.5:
            self.add(rect.copy())
            nb_days_left -= 1

            if toggle:
                dim = 0
            else:
                dim = 1

            rect.stretch_about_point(nb_days_left / 365, dim, corner)

            toggle = not toggle
