# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示 Linus 思考數線伸縮的過程，數線會根據不同縮放因子進行拉伸或壓縮，同時 Linus 的目光跟隨數線上的數字移動。



from manim import *
class LinusThinksAboutStretching(Scene):
    def construct(self):
        linus = Linus()
        top_line = NumberLine(color=GREY)
        top_line.to_edge(UP)
        top_line.add_numbers()

        linus.move_to(3 * LEFT + DOWN)

        self.add(linus, top_line)

        scalars = [3, 0.5, 2]

        for scalar in scalars:
            lower_line = NumberLine(
                x_range=[-14, 14, 1],
                color=BLUE
            )
            lower_line.next_to(top_line, DOWN, buff=MED_LARGE_BUFF)
            lower_line.numbers = lower_line.get_number_mobjects()
            for number in lower_line.numbers:
                number.add_updater(lambda m: m.next_to(
                    lower_line.number_to_point(m.get_value()),
                    DOWN, buff=MED_SMALL_BUFF,
                ))
            lower_line.save_state()
            lower_line.numbers.save_state()
            self.add(lower_line, *lower_line.numbers)

            words = Text(f"Multiply by {scalar}")
            words.next_to(lower_line.numbers, DOWN)

            self.play(
                lower_line.animate.stretch(scalar, 0, about_point=lower_line.get_center()),
                run_time=2
            )
            self.play(
                FadeIn(words, scale=1.0 / scalar),
                linus.animate.look_at(top_line.number_to_point(scalar))
            )
            self.play(Blink(linus))
            self.play(
                FadeOut(lower_line),
                FadeOut(lower_line.numbers),
                FadeOut(words),
                FadeIn(lower_line.saved_state, remover=True),
                FadeIn(lower_line.numbers.saved_state, remover=True),
                linus.animate.look_at(top_line.number_to_point(0))
            )
        self.play(linus.animate.change("confused", DOWN + RIGHT))
        self.wait(2)
        self.play(Blink(linus))
        self.wait(2)
