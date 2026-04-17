# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示兩個角色之間出現納維-斯托克斯方程，隨後在一個角色旁顯示能量分佈公式並添加註解，最後淡出角色和方程並放大分佈公式。



from manim import *
class SomeTurbulenceEquations(PiCreatureScene):
    def construct(self):
        randy, morty = self.pi_creatures
        navier_stokes = NavierStokesEquations()
        line = Line(randy.get_right(), morty.get_left())
        navier_stokes.replace(line, dim_to_match=0)
        navier_stokes.scale(1.2)

        distribution = MathTex(
            "E(k) \\propto k^{-5/3}",
            tex_to_color_map={
                "k": GREEN,
                "-5/3": YELLOW,
            }
        )
        distribution.next_to(morty, UL)
        brace = Brace(distribution, DOWN, buff=SMALL_BUFF)
        brace_words = brace.get_text("Explained soon...")
        brace_group = VGroup(brace, brace_words)

        self.play(
            Write(navier_stokes),
            randy.animate.change("confused", navier_stokes),
            morty.animate.change("confused", navier_stokes),
        )
        self.wait(3)
        self.play(
            morty.animate.change("raise_right_hand", distribution),
            randy.animate.look_at(distribution),
            FadeIn(distribution, shift=DOWN),
            navier_stokes.animate.set_opacity(0.5),
        )
        self.play(GrowFromCenter(brace_group))
        self.play(randy.animate.change("pondering", distribution))
        self.wait(3)
        dist_group = VGroup(distribution, brace_group)
        self.play(
            LaggedStartMap(FadeOut, VGroup(randy, morty, navier_stokes)),
            dist_group.animate.scale(1.5),
            dist_group.animate.center(),
            dist_group.animate.to_edge(UP),
        )
        self.wait()

    def create_pi_creatures(self):
        randy, morty = Randolph(), Mortimer()
        randy.to_corner(DL)
        morty.to_corner(DR)
        return (randy, morty)
