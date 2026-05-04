# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個 PiCreature 角色旁出現 div/curl 和 Jacobian 文字，並用箭頭連接到上方的「基於流的直覺」文字，角色手勢隨之變化。



from manim import *
class ToolsBeyondDivAndCurlForODEs(PiCreatureScene):
    def __init__(self, **kwargs):
        super().__init__(
            default_pi_creature_kwargs={"color": GREY_BROWN},
            default_pi_creature_start_corner=DOWN,
            **kwargs
        )

    def construct(self):
        morty = self.pi_creature
        div_curl = MathTex("\\text{div} \\\\", "\\text{curl}")
        div_curl.set_color_by_tex("div", BLUE)
        div_curl.set_color_by_tex("curl", YELLOW)
        div_curl.next_to(morty.get_corner(UL), UP, buff=MED_LARGE_BUFF)

        jacobian = Text("Analyze the\nJacobian")
        jacobian.set_color(GREEN)
        jacobian.next_to(morty.get_corner(UR), UP, buff=MED_LARGE_BUFF)

        flow_intuitions = Text("Flow-based intuitions")
        flow_intuitions.next_to(
            VGroup(div_curl, jacobian),
            UP, buff=1.5
        )
        arrow1 = Arrow(div_curl.get_top(), flow_intuitions.get_bottom())
        arrow2 = Arrow(flow_intuitions.get_bottom(), jacobian.get_top())

        self.play(
            FadeIn(div_curl, shift=DOWN),
            morty.animate.change("raise_left_hand"),
        )
        self.wait()
        self.play(
            FadeIn(jacobian, shift=DOWN),
            morty.animate.change("raise_right_hand")
        )
        self.wait()
        self.play(
            ReplacementTransform(
                flow_intuitions.copy().set_opacity(0).move_to(div_curl),
                flow_intuitions,
            ),
            GrowArrow(arrow1),
            morty.animate.change("pondering")
        )
        self.wait(0.5)
        self.play(GrowArrow(arrow2))
        self.wait()
