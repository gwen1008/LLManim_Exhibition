# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示電場從均勻分佈到受圓柱影響的變化過程，包含電荷移動和電場線的動態視覺化。


from manim import *
import numpy as np
import random

class ElectricField(Scene):
    def construct(self):
        self.add_plane()
        self.add_title()
        self.setup_warped_grid()
        self.show_uniform_field()
        self.show_moving_charges()
        self.show_field_lines()

    def add_plane(self):
        # 假設的平面創建方法，根據實際需要調整
        self.plane = NumberPlane()
        self.add(self.plane)

    def add_title(self):
        self.title = Text("Electric Field", font_size=48)
        self.title.to_edge(UP)
        self.add(self.title)

    def get_func_label(self):
        # 假設的函數標籤創建方法
        self.func_label = MathTex("f(z) = z + \\frac{1}{z}")
        self.func_label.next_to(self.title, DOWN)
        return self.func_label

    def get_warpable_grid(self):
        # 創建可變形網格
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 2,
                "stroke_opacity": 0.5
            }
        )
        self.add(grid)
        return grid

    def inverse_joukowsky_map(self, point):
        # 逆茹科夫斯基變換的簡化實現
        x, y = point[:2]
        z = complex(x, y)
        w = z + 1/z if abs(z) > 0 else complex(0, 0)
        return np.array([w.real, w.imag, 0])

    def setup_warped_grid(self):
        warped_grid = self.warped_grid = self.get_warpable_grid()
        warped_grid.save_state()
        func_label = self.get_func_label()
        unit_circle = self.unit_circle = Circle(
            radius=self.plane.x_unit_size,  # 使用平面單位大小
            stroke_color=YELLOW,
            fill_color=BLACK,
            fill_opacity=1
        )

        self.add(self.title, func_label, unit_circle)
        self.remove(self.plane)
        
        # 應用複變函數變形
        self.play(
            warped_grid.animate.apply_complex_function(self.inverse_joukowsky_map),
            run_time=2
        )
        self.wait()

    def show_uniform_field(self):
        # 創建均勻向量場
        vector_field = self.vector_field = VectorField(
            lambda p: UP,
            colors=[BLUE_E, WHITE, RED_E],
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            length_func=lambda norm: 0.5
        )
        
        # 創建質子和電子群組
        def get_proton():
            return Circle(radius=0.2, color=RED, fill_opacity=1)
        
        def get_electron():
            return Circle(radius=0.2, color=BLUE, fill_opacity=1)
        
        protons, electrons = groups = [
            VGroup(*[method() for x in range(20)])
            for method in (get_proton, get_electron)
        ]
        
        for group in groups:
            group.arrange(RIGHT, buff=MED_SMALL_BUFF)
            random.shuffle(group.submobjects)
        
        protons.next_to(config.frame_height * DOWN / 2, DOWN)
        electrons.next_to(config.frame_height * UP / 2, UP)

        self.play(
            self.warped_grid.animate.restore(),
            FadeOut(self.unit_circle),
            FadeOut(self.title),
            FadeOut(self.func_label),
            LaggedStartMap(GrowArrow, vector_field, lag_ratio=0.1)
        )
        self.wait()
        
        for group, vect in [(protons, UP), (electrons, DOWN)]:
            self.play(LaggedStartMap(
                ApplyMethod, group,
                lambda m: (m.shift, (config.frame_height + 1) * vect),
                run_time=3,
                rate_func=rush_into
            ))

    def show_moving_charges(self):
        unit_circle = self.unit_circle

        # 創建質子環形排列
        protons = VGroup()
        for n in range(4):
            num_points = 6 * n if n > 0 else 1
            for angle in np.linspace(0, TAU, num_points, endpoint=False):
                point = 0.275 * n * np.array([np.cos(angle), np.sin(angle), 0])
                proton = Circle(radius=0.1, color=RED, fill_opacity=1)
                proton.move_to(point)
                protons.add(proton)

        # 創建電子（隨機位置）
        electrons = VGroup()
        for proton in protons:
            angle = np.random.random() * TAU
            offset = 0.2 * np.array([np.cos(angle), np.sin(angle), 0])
            electron = Circle(radius=0.1, color=BLUE, fill_opacity=1)
            electron.move_to(proton.get_center() + offset)
            electrons.add(electron)

        # 電子目標位置
        electrons.generate_target()
        for electron in electrons.target:
            y_part = electron.get_center()[1]
            if y_part > 0:
                electron.shift(2 * y_part * DOWN)

        # 新電場向量場
        def new_electric_field(point):
            x, y = point[:2]
            norm = np.sqrt(x**2 + y**2)
            if norm < 1:
                return ORIGIN
            # 簡化的圓柱流場
            angle = np.arctan2(y, x)
            vect = np.array([np.cos(angle), np.sin(angle), 0])
            # 旋轉90度
            return np.array([-vect[1], vect[0], 0])
        
        new_vector_field = VectorField(
            new_electric_field,
            colors=[BLUE_E, WHITE, RED_E],
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            length_func=lambda norm: 0.5
        )

        warped_grid = self.warped_grid

        self.play(GrowFromCenter(unit_circle))
        self.add(protons, electrons)
        self.play(
            LaggedStartMap(FadeIn, protons, lag_ratio=0.1),
            LaggedStartMap(FadeIn, electrons, lag_ratio=0.1),
        )
        
        # 縮放鏡頭
        self.play(
            self.camera.frame.animate.scale(0.7),
            run_time=3
        )
        
        self.play(
            MoveToTarget(electrons),
            warped_grid.animate.apply_complex_function(self.inverse_joukowsky_map),
            Transform(
                self.vector_field,
                new_vector_field
            ),
            run_time=3
        )
        self.wait(5)

    def show_field_lines(self):
        # 創建水平電場線
        h_lines = VGroup(*[
            Line(
                5 * LEFT, 5 * RIGHT,
                stroke_color=GREY_B,
                stroke_width=2,
            ).shift(y * UP)
            for y in np.arange(-3, 3.25, 0.25)
            if y != 0
        ])
        
        # 應用變形
        for h_line in h_lines:
            points = h_line.get_points()
            new_points = np.array([self.inverse_joukowsky_map(p) for p in points])
            h_line.set_points(new_points)
            h_line.save_state()

        # 電壓顯示
        voltage = DecimalNumber(
            10, num_decimal_places=1,
            unit="\\, V",
            color=YELLOW,
        )
        voltage.add_background_rectangle()
        
        vp_prop = 0.1
        voltage_point = Dot(point=h_lines[4].point_from_proportion(vp_prop), radius=0)

        def get_voltage():
            y = voltage_point.get_center()[1]
            return 10 - y

        voltage.add_updater(
            lambda d: d.set_value(get_voltage())
        )
        voltage.add_updater(
            lambda d: d.next_to(voltage_point, UP, SMALL_BUFF)
        )

        self.play(Create(
            h_lines,
            run_time=2,
            lag_ratio=0
        ))
        self.add(voltage)
        self.play(
            voltage.animate.set_fill(opacity=1),
            h_lines[4].animate.set_stroke(color=YELLOW, width=4),
        )
        
        for i in range(4, len(h_lines)-1):
            hl1 = h_lines[i]
            hl2 = h_lines[i+1]
            
            self.play(
                voltage_point.animate.move_to(hl2.point_from_proportion(vp_prop)),
                hl1.animate.restore(),
                hl2.animate.set_stroke(color=YELLOW, width=3),
                run_time=0.5
            )
            self.wait(0.5)
