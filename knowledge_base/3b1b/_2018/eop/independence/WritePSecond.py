# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 將一個帶有概率表達式和等號右側數值的組合物件置中並寫入場景底部。



from manim import *
class WritePSecond(Scene):
    def construct(self):
        prob = get_probability_of_slot_group([None, True, None])
        rhs = MathTex("= 0.8")
        rhs.next_to(prob, RIGHT)
        prob.add(rhs)
        prob.set_width(config.frame_width - 1)
        prob.center().to_edge(DOWN)
        self.play(Write(prob))
