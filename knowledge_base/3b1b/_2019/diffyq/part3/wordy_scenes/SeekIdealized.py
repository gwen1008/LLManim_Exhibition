# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示從「現實問題」到「理想化問題」的轉變過程，並引入解決方案和模型的概念。



from manim import *
class SeekIdealized(Scene):
    def construct(self):
        phrases = VGroup(*[
            MathTex(
                "\\text{Seek}", text, "\\text{problems}",
                tex_to_color_map={
                    "\\text{realistic}": GREEN,
                    "\\text{idealized}": YELLOW,
                    "\\text{over-idealized}": YELLOW,
                    "\\text{general}": BLUE,
                }
            )
            for text in [
                "\\text{realistic}",
                "\\text{idealized}",
                "\\text{over-idealized}",
                "\\text{general}",
            ]
        ])
        phrases.scale(2)
        words = VGroup()
        for phrase in phrases:
            phrase.center()
            word = phrase[1]
            words.add(word)
            phrase.remove(word)
        arrow = Arrow(start=UP, end=DOWN, stroke_width=6)
        arrow.set_color(WHITE)
        arrow.next_to(words[3], UP)
        low_arrow = arrow.copy()
        low_arrow.next_to(words[3], DOWN)

        solutions = Text("solutions")
        solutions.scale(2)
        solutions.move_to(phrases[3][1].get_center() + UL * 0.5)
        models = Text("models")
        models.scale(2)
        models.next_to(
            words[0], RIGHT, buff=0.35,
            aligned_edge=DOWN
        )

        phrases.center()
        phrase = phrases[0]

        self.add(phrase)
        self.add(words[0])
        self.wait()
        words[0].save_state()
        self.play(
            words[0].animate.to_edge(DOWN),
            words[0].animate.set_opacity(0.5),
            Transform(phrase, phrases[1]),
            FadeIn(words[1], shift=UP)
        )
        self.wait()
        self.play(
            words[1].animate.next_to(arrow, UP),
            Create(arrow),
            phrase.animate.next_to(words[1], LEFT),
            FadeIn(solutions, shift=LEFT),
            FadeIn(words[3]),
        )
        self.wait()

        words[0].generate_target()
        words[0].target.next_to(low_arrow, DOWN)
        words[0].target.set_opacity(1)
        models.shift(
            words[0].target.get_center() -
            words[0].saved_state.get_center()
        )
        self.play(
            MoveToTarget(words[0]),
            Create(low_arrow),
            FadeIn(models, shift=LEFT)
        )
        self.wait()
