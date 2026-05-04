# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示計算圓周率 π 的各種演算法在「效率-優雅度」坐標平面上的分布位置，每個演算法以文字或公式標示並搭配紅色叉號。



from manim import *
class PiComputingAlgorithmsAxes(Scene):
    def construct(self):
        self.setup_axes()
        self.add_methods()

    def setup_axes(self):
        axes = Axes(
            x_range=[0, 9, 1],
            y_range=[0, 5, 1],
            axis_config={
                "tick_frequency": 100,
                "include_numbers": False,
            }
        )

        y_label = Text("Efficiency")
        y_label.rotate(90 * DEGREES)
        y_label.next_to(axes.y_axis, LEFT, SMALL_BUFF)
        x_label = Text("Elegance")
        x_label.next_to(axes.x_axis, DOWN, SMALL_BUFF)
        axes.add(y_label, x_label)
        axes.center().to_edge(DOWN)
        self.axes = axes

        title = Text("Algorithms for computing $\\pi$")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        self.add(title, axes)

    def add_methods(self):
        method_location_list = [
            (self.get_machin_like_formula(), (1, 4.5)),
            (self.get_viete(), (3, 3.5)),
            (self.get_measuring_tape(), (0.5, 1)),
            (self.get_monte_carlo(), (2, 0.2)),
            (self.get_basel(), (6, 1)),
            (self.get_blocks_image(), (8, 0.1)),
        ]

        algorithms = VGroup()
        for method, location in method_location_list:
            cross = MathTex("\\times")
            cross.set_color(RED)
            cross.move_to(self.axes.c2p(*location))
            method.next_to(cross, UP, SMALL_BUFF)
            method.align_to(cross, LEFT)
            method.shift_onto_screen()
            algorithms.add(VGroup(method, cross))

        self.play(LaggedStart(
            *[FadeIn(mob, shift=DOWN) for mob in algorithms],
            run_time=4,
            lag_ratio=0.4,
        ))
        self.wait()
        self.play(CreateThenFadeAround(algorithms[-1][0]))

    def get_machin_like_formula(self):
        formula = MathTex(
            "\\frac{\\pi}{4} = "
            "12\\arctan\\left(\\frac{1}{49}\\right) + "
            "32\\arctan\\left(\\frac{1}{57}\\right) - "
            "5\\arctan\\left(\\frac{1}{239}\\right) + "
            "12\\arctan\\left(\\frac{1}{110{,}443}\\right)"
        )
        formula.scale(0.5)
        return formula

    def get_viete(self):
        formula = MathTex(
            "\\frac{2}{\\pi} = "
            "\\frac{\\sqrt{2}}{2} \\cdot"
            "\\frac{\\sqrt{2 + \\sqrt{2}}}{2} \\cdot"
            "\\frac{\\sqrt{2 + \\sqrt{2 + \\sqrt{2}}}}{2} \\cdots"
        )
        formula.scale(0.5)
        return formula

    def get_measuring_tape(self):
        return Text("Measuring tape").scale(0.75)

    def get_monte_carlo(self):
        return Text("Monte Carlo").scale(0.75)

    def get_basel(self):
        formula = MathTex(
            "\\frac{\\pi^2}{6} = "
            "\\sum_{n=1}^\\infty \\frac{1}{n^2}"
        )
        formula.scale(0.5)
        return formula

    def get_blocks_image(self):
        # 由於 BlocksAndWallScene 是自定義類別，這裡保留原樣
        # 如果實際執行時不存在，可以替換為一個簡單的示意圖形
        scene = BlocksAndWallScene(
            write_to_movie=False,
            skip_animations=True,
            count_clacks=False,
            floor_y=1,
            wall_x=0,
            n_wall_ticks=6,
            sliding_blocks_config={
                "block1_config": {
                    "mass": 1e2,
                    "velocity": -0.01,
                    "distance": 3.5
                },
                "block2_config": {
                    "distance": 1,
                    "velocity": 0,
                },
            }
        )
        group = VGroup(
            scene.wall, scene.floor,
            scene.blocks.block1,
            scene.blocks.block2,
        )
        group.set_width(3)
        return group
