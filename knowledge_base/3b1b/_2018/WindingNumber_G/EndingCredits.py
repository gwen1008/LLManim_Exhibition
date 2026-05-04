# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示結尾字幕動畫，包含文字淡入和 PiCreature 角色互動。



from manim import *
class EndingCredits(Scene):
    def construct(self):
        text = Tex(
            "Written and animated by: \\\\",
            "Sridhar Ramesh \\\\",
            "Grant Sanderson"
        )
        text[0].shift(MED_SMALL_BUFF * UP)
        text.to_edge(UP)

        pi = PiCreature(color=YELLOW_E, height=2)
        pi.to_edge(DOWN)
        pi.change_mode("happy")
        self.add(pi)

        self.play(LaggedStartMap(FadeIn, text), pi.animate.look_at(text))
        self.play(pi.animate.change("wave_1"), text)
        self.play(Blink(pi))
        self.play(pi.animate.change("happy"))
        self.wait()
