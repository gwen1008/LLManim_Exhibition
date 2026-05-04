# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示洛倫茲變換如何將坐標網格沿著光錐線進行剪切變形，同時顯示時空間隔公式。



from manim import *
class LorenzTransform(Scene):
    def construct(self):
        grid = NumberPlane()
        grid.scale(2)
        back_grid = grid.copy()
        back_grid.set_stroke(GREY, 0.5)

        c_lines = VGroup(Line(DL, UR), Line(DR, UL))
        c_lines.scale(config.frame_height)
        c_lines.set_stroke(YELLOW, 3)

        equation = MathTex("d\\tau^2 = dt^2 - dx^2")
        equation.scale(1.7)
        equation.to_corner(UL, buff=MED_SMALL_BUFF)
        equation.shift(2.75 * DOWN)
        equation.set_stroke(BLACK, 5, background=True)

        self.add(back_grid, grid, c_lines)
        self.add(equation)
        beta = 0.4
        self.play(
            grid.animate.apply_matrix(np.array([
                [1, beta],
                [beta, 1],
            ]) / (1 - beta**2)),
            run_time=2
        )
        self.wait()
