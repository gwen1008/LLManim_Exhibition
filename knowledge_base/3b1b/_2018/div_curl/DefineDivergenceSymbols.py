# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示散度符號的定義，包含向量場函數、點座標和散度值的動態標籤說明。



from manim import *
class DefineDivergenceSymbols(Scene):
    def construct(self):
        tex_mob = MathTex(
            "\\text{div}",
            "\\textbf{F}",
            "(x, y)",
            "=",
        )
        div, F, xy, eq = tex_mob
        output = DecimalNumber(0, include_sign=True)
        output.next_to(tex_mob, RIGHT)
        time_tracker = ValueTracker()
        always(time_tracker.increment_value, 1)  # 替代 always_shift
        self.add(time_tracker)
        output_animation = always_redraw(
            lambda: output.set_value(3 * np.cos(int(time_tracker.get_value())))
        )

        F.set_color(BLUE)
        xy.set_color(YELLOW)

        F_brace = Brace(F, UP, buff=SMALL_BUFF)
        F_label = F_brace.get_text("Vector field function")
        F_label.set_color(F.get_color())
        xy_brace = Brace(xy, DOWN, buff=SMALL_BUFF)
        xy_label = xy_brace.get_text("Some point")
        xy_label.set_color(xy.get_color())
        output_brace = Brace(output, UP, buff=SMALL_BUFF)
        output_label = output_brace.get_text(
            "Measure of how much \\\\ $(x, y)$ ``generates'' fluid"
        )
        brace_label_pairs = [
            (F_brace, F_label),
            (xy_brace, xy_label),
            (output_brace, output_label),
        ]

        self.add(tex_mob, output_animation)
        fade_anims = []
        for brace, label in brace_label_pairs:
            self.play(
                GrowFromCenter(brace),
                FadeIn(label, shift=DOWN),  # 替代 FadeInFromDown
                *fade_anims
            )
            self.wait(2)
            fade_anims = [FadeOut(brace), FadeOut(label)]
        self.wait()
