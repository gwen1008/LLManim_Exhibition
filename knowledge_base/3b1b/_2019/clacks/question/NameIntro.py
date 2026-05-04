# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示 "3Blue1Brown" 文字標誌的動畫，其中 "3Blue" 和 "1Brown" 兩個部分分別閃爍並移動到畫面邊緣後返回原位。



from manim import *
class NameIntro(Scene):
    def construct(self):
        name = MathTex("3Blue", "1Brown", arg_separator="")
        blue, brown = name
        name.scale(2.5)
        for part in name:
            part.save_state()
        brown.to_edge(RIGHT, buff=0)
        flash_time = 0.75

        self.add(blue, brown)
        self.play(
            VFadeIn(blue),
            VFadeIn(brown),
            Restore(brown, rate_func=linear),
        )
        self.play(
            Flash(blue.get_right(), run_time=flash_time),
            blue.animate.to_edge(LEFT, buff=0),
            rate_func=linear,
        )
        self.play(
            Flash(blue.get_left(), run_time=flash_time),
            Restore(blue, rate_func=linear),
        )
        self.play(
            Flash(blue.get_right(), run_time=flash_time),
            brown.animate.to_edge(RIGHT, buff=0),
            rate_func=linear,
        )
        self.play(
            Flash(brown.get_right(), run_time=flash_time),
            Restore(brown, rate_func=linear)
        )
