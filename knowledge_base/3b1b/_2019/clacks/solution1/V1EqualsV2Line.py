# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示一條水平線和一個紅色等式 "v_1 = v_2" 同時出現的動畫。



from manim import *
class V1EqualsV2Line(Scene):
    def construct(self):
        line = Line(LEFT, 7 * RIGHT)
        eq = MathTex("v_1", "=", "v_2")
        eq.set_color_by_tex("v_", RED)
        eq.next_to(RIGHT, UR, buff=SMALL_BUFF)
        self.play(
            Write(eq, run_time=1),
            Create(line),
        )
        self.wait()
