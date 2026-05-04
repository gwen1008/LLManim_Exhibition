# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示「層流」標題及其拉丁文詞源解釋的動畫。



from manim import *
class LaminarFlowLabel(Scene):
    def construct(self):
        words = Text("Laminar flow", font_size=48)
        words.to_edge(UP)
        subwords = Text(
            "`Lamina', in Latin, means\n"
            "``a thin sheet of material''",
            font_size=36,
            t2c={"Lamina": YELLOW}
        )
        subwords.next_to(words, DOWN, buff=MED_LARGE_BUFF)
        VGroup(words, subwords).set_stroke(width=4, color=BLACK, background=True)
        self.play(Write(words))
        self.wait()
        self.play(FadeIn(subwords, shift=DOWN))
        self.wait()
