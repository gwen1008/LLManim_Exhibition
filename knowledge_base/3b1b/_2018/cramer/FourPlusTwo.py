# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示兩個帶有括號和標籤的數學表達式，並用動畫方式呈現大括號和標籤的出現。



from manim import *
class FourPlusTwo(Scene):
    def construct(self):
        p1 = MathTex("(4)(1)")
        p2 = MathTex("-(-1)(2)")
        p2.next_to(p1, RIGHT, buff=SMALL_BUFF)
        b1 = Brace(p1, UP)
        b2 = Brace(p2, UP)
        t1 = b1.get_tex("4", buff=SMALL_BUFF)
        t2 = b2.get_tex("+2", buff=SMALL_BUFF)

        for b, t in (b1, t1), (b2, t2):
            t.set_stroke(BLACK, width=3, background=True)
            self.play(
                GrowFromCenter(b),
                Write(t)
            )
        self.wait()
