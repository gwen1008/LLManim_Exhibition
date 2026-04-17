# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示從二維輸入輸出空間的函數映射過渡到三維空間中旋轉的筆記型電腦模型。



from manim import *
class TwoDScreenInOurThreeDWorld(AltTeacherStudentsScene, ThreeDScene):
    def construct(self):
        self.ask_about_2d_functions()
        self.show_3d()

    def ask_about_2d_functions(self):
        in_plane = NumberPlane(x_range=[-2.5, 2.5], y_range=[-2.5, 2.5], x_length=5, y_length=5)
        in_plane.add_coordinates()
        in_plane.set_height(3)
        out_plane = in_plane.copy()

        in_text = Text("Input space", font_size=24)
        out_text = Text("Output space", font_size=24)
        in_text.next_to(in_plane, UP, buff=SMALL_BUFF)
        out_text.next_to(out_plane, UP, buff=SMALL_BUFF)
        in_plane.add(in_text)
        out_plane.add(out_text)

        arrow = Arrow(
            LEFT, RIGHT,
            path_arc=-TAU/4,
            color=WHITE
        )
        arrow.pointwise_become_partial(arrow, 0.0, 0.97)
        group = VGroup(in_plane, arrow, out_plane)
        group.arrange(RIGHT)
        arrow.shift(UP)
        group.move_to(self.students)
        group.to_edge(UP)

        dots = VGroup()
        dots_target = VGroup()
        for x in np.arange(-2.5, 3.0, 0.5):
            for y in np.arange(-2.5, 3.0, 0.5):
                dot = Dot(radius=0.05)
                dot.move_to(in_plane.c2p(x, y))
                dot.generate_target()
                dot.target.move_to(out_plane.c2p(
                    x + 0.25*np.cos(5*y), y + 0.25*np.sin(3*x)
                ))
                dots.add(dot)
                dots_target.add(dot.target)
        dots.set_color_by_gradient(YELLOW, RED)
        dots_target.set_color_by_gradient(YELLOW, RED)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            Write(in_plane, run_time=1)
        )
        self.play(
            Create(arrow),
            ReplacementTransform(
                in_plane.copy(), out_plane,
                path_arc=-TAU/4,
            )
        )
        self.play(
            LaggedStartMap(GrowFromCenter, dots, run_time=1),
            self.change_students(*3*["erm"]),
        )
        self.play(LaggedStartMap(MoveToTarget, dots, path_arc=-TAU/4))
        self.wait(3)

    def show_3d(self):
        # 注意：Laptop 類別在 ManimCE 中不存在，這裡用一個簡單的立方體替代
        # 如果需要更精確的筆記型電腦模型，需要自定義或使用其他方法
        laptop = Cube(side_length=2).set_fill(BLUE_E, opacity=0.8).set_stroke(WHITE, width=1)
        laptop.rotate(-TAU/12, DOWN)
        laptop.rotate(-5*TAU/24, LEFT)
        laptop.rotate(TAU/8, LEFT)
        laptop.scale(2.3*config.frame_width/(2))
        laptop.shift(-laptop.get_center() + 0.1*IN)
        
        # 簡單的 3D 陰影效果
        laptop.set_shade_in_3d(True)

        everything = VGroup(laptop, *self.mobjects)
        everything.generate_target()
        everything.target.rotate(TAU/12, LEFT)
        everything.target.rotate(TAU/16, UP)
        everything.target.shift(4*UP)

        self.move_camera(
            phi=75 * DEGREES,
            theta=30 * DEGREES,
            distance=12,
            run_time=4,
        )
        self.play(
            MoveToTarget(everything, run_time=4),
        )
        
        # 持續旋轉
        self.begin_ambient_camera_rotation(rate=3 * DEGREES)
        self.wait(10)
        self.stop_ambient_camera_rotation()
