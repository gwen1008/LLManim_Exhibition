# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示一個角色思考貝葉斯規則，然後轉向一個螢幕矩形的動畫過程。



from manim import *
class BayesRuleInMemory(Scene):
    def construct(self):
        randy = Randolph()
        randy.to_corner(DOWN + LEFT)
        bubble = ThoughtBubble(height=4)
        bubble.pin_to(randy)
        B = "\\text{Belief}"
        D = "\\text{Data}"
        rule = MathTex(
            "P(", B, "|", D, ")", "=",
            "P(", "B", ")",
            "{P(", D, "|", B, ")", "\\over", "P(", D, ")}"
        )
        rule.set_color_by_tex(B, RED)
        rule.set_color_by_tex(D, GREEN)
        rule.next_to(randy, RIGHT, buff=LARGE_BUFF).shift(UP)
        rule.generate_target()
        bubble.add_content(rule.target)
        screen_rect = ScreenRectangle()
        screen_rect.next_to(randy, UP + RIGHT)

        self.add(randy)
        self.play(
            LaggedStartMap(FadeIn, rule),
            randy.animate.change("erm", rule)
        )
        self.play(Blink(randy))
        self.play(
            Create(bubble),
            MoveToTarget(rule),
            randy.animate.change("pondering"),
        )
        self.wait()
        self.play(rule.animate.set_opacity(0.3), run_time=2)
        self.play(randy.animate.change("confused", rule))
        self.play(Blink(randy))
        self.wait(2)
        self.play(
            FadeOut(VGroup(bubble, rule)),
            randy.animate.change("pondering", screen_rect),
        )
        self.play(
            randy.animate.look_at(screen_rect.get_right()),
            Create(screen_rect),
        )
        self.wait(4)
