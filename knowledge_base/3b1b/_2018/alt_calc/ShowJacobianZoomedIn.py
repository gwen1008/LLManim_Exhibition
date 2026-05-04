# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示在非線性變換下，局部放大區域的雅可比矩陣視覺化效果。



from manim import *
class ShowJacobianZoomedIn(Scene):
    def __init__(
        self,
        show_basis_vectors=False,
        show_coordinates=True,
        zoom_factor=0.05,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.show_basis_vectors = show_basis_vectors
        self.show_coordinates = show_coordinates
        self.zoom_factor = zoom_factor

    def construct(self):
        def example_function(point):
            x, y, z = point
            return np.array([
                x + np.sin(y),
                y + np.sin(x),
                0
            ])

        # 創建主坐標平面
        main_plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4.5, 4.5, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        )
        self.add(main_plane)

        # 創建放大相機和顯示區域
        zoomed_camera = self.camera.frame
        zoomed_display = Rectangle(
            height=3, width=4,
            stroke_color=YELLOW,
            stroke_width=3
        )
        zoomed_display.move_to(3 * LEFT + 1 * UP)
        
        # 創建放大顯示的背景
        zd_rect = BackgroundRectangle(
            zoomed_display,
            fill_opacity=0.8,
            buff=0.2,
            color=BLACK
        )
        self.add(zd_rect)
        
        # 創建放大區域的小網格
        tiny_grid = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.8
            },
            faded_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 0.5,
                "stroke_opacity": 0.5
            },
            faded_line_ratio=2
        )
        tiny_grid.move_to(zoomed_display.get_center())
        
        # 創建雅可比文字標籤
        jacobian_words = Text("Jacobian", color=WHITE)
        jacobian_words.scale(1.5)
        jacobian_background = SurroundingRectangle(
            jacobian_words,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2
        )
        jacobian_group = VGroup(jacobian_background, jacobian_words)
        jacobian_group.move_to(zoomed_display.get_top() + UP * 0.5)
        
        # 動畫序列
        self.play(
            Create(zoomed_display),
            run_time=1.5
        )
        self.play(
            Create(tiny_grid),
            Write(jacobian_group),
            run_time=2
        )
        self.wait()
        
        # 應用非線性變換
        def apply_nonlinear_transform(mob, alpha):
            mob.become(tiny_grid.copy())
            for point in mob.get_points():
                transformed = example_function(point)
                mob.apply_points_function_about_point(
                    lambda p: example_function(p),
                    point
                )
            return mob
        
        self.play(
            UpdateFromAlphaFunc(tiny_grid, apply_nonlinear_transform),
            run_time=5
        )
        self.wait()
