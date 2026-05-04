# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示小角度近似公式及其對單擺週期公式的推導過程，包含文字標註和動畫效果。



from manim import *
class SmallAngleApproximationTex(Scene):
    def construct(self):
        approx = MathTex(
            "\\sin", "(", "\\theta", ") \\approx \\theta",
            tex_to_color_map={"\\theta": RED},
        )

        implies = MathTex("\\Downarrow")
        period = MathTex(
            "\\text{Period}", "\\approx",
            "2\\pi \\sqrt{\\,{L} / {g}}",
        )
        group = VGroup(approx, implies, period)
        group.arrange(DOWN)

        approx_brace = Brace(approx, UP, buff=SMALL_BUFF)
        approx_words = Tex(
            "\\text{For small }\\theta",
            tex_to_color_map={"\\theta": RED},
        )
        approx_words.scale(0.75)
        approx_words.next_to(approx_brace, UP, SMALL_BUFF)

        self.add(approx, approx_brace, approx_words)
        self.play(
            Write(implies),
            FadeIn(period, shift=LEFT)
        )
        self.wait()
