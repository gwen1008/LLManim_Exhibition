# Source: 3b1b/_2019/diffyq/part3/pi_creature_scenes.py
# Description: [3b1b translated] 展示一個角色與傅立葉畫像並列，時間軸從1822年移動到2019年，同時顯示熱方程公式的動畫過程。



from manim import *
class InFouriersShoes(Scene):
    def construct(self):
        # 創建 PiCreature 角色
        randy = self.pi_creature
        
        # 載入傅立葉畫像
        fourier = ImageMobject("Joseph Fourier")
        fourier.set_height(4)
        fourier.next_to(randy, RIGHT, buff=LARGE_BUFF)
        fourier.align_to(randy, DOWN)

        # 創建熱方程公式
        equation = MathTex(
            r"\frac{\partial T}{\partial t} = \alpha \nabla^2 T"
        )
        equation.next_to(fourier, UP, buff=MED_LARGE_BUFF)

        # 創建時間軸
        decades = list(range(1740, 2040, 20))
        time_line = NumberLine(
            x_range=[decades[0], decades[-1], 1],
            length=10,
            include_numbers=True,
            numbers_with_elongated_ticks=decades,
            stroke_width=2,
        )
        time_line.add_numbers(
            values=decades,
            font_size=24,
            group_with_commas=False
        )
        time_line.move_to(ORIGIN, RIGHT)
        time_line.to_edge(UP)
        
        # 創建三角形指示器
        triangle = Triangle()
        triangle.set_height(0.25)
        triangle.rotate(-90 * DEGREES)
        triangle.move_to(time_line.n2p(2019), DOWN)
        triangle.set_color(WHITE)

        # 動畫序列
        self.play(FadeIn(fourier, shift=2*LEFT))
        self.play(randy.animate.change("thinking"))
        self.wait()
        
        self.play(
            Create(triangle, run_time=1),
            FadeIn(equation, shift=DOWN),
            FadeIn(time_line),
        )
        
        # 移動時間軸
        shift_distance = time_line.n2p(2019) - time_line.n2p(1822)
        self.play(
            triangle.animate,
            time_line.animate.shift(shift_distance),
            run_time=5
        )
        self.wait()
