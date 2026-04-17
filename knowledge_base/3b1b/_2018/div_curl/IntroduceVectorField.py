# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示向量場從點轉換為箭頭，並模擬流體流動、重力場和磁場的動態視覺化過程。


from manim import *
import numpy as np

# 定義輔助函數（根據原始代碼推斷）
def four_swirls_function(point):
    x, y = point[:2]
    result = np.array([
        np.sin(y),
        np.sin(x),
        0
    ])
    norm = np.linalg.norm(result)
    if norm == 0:
        return result
    return result / norm

def get_force_field_func(*sources):
    def func(point):
        result = np.zeros(3)
        for center, strength in sources:
            diff = center - point[:3]
            norm = np.linalg.norm(diff)
            if norm < 0.1:
                norm = 0.1
            result += strength * diff / norm**3
        return result
    return func

class IntroduceVectorField(Scene):
    def __init__(
        self,
        vector_field_config=None,
        stream_line_config=None,
        stream_line_animation_config=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # 設置默認配置
        self.vector_field_config = vector_field_config or {
            "delta_x": 0.5,
            "delta_y": 0.5,
        }
        self.stream_line_config = stream_line_config or {
            "start_points_generator_config": {
                "delta_x": 0.25,
                "delta_y": 0.25,
            },
            "virtual_time": 3,
        }
        self.stream_line_animation_config = stream_line_animation_config or {
            # 注意：ShowPassingFlashWithThinningStrokeWidth 不是 ManimCE 標準類
            # 這裡使用 ShowPassingFlash 替代
            "line_anim_class": ShowPassingFlash,
        }

    def construct(self):
        self.add_plane()
        self.add_title()
        self.points_to_vectors()
        self.show_fluid_flow()
        self.show_gravitational_force()
        self.show_magnetic_force()
        self.show_fluid_flow()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        # 移除最後一個坐標標籤（通常是原點標籤）
        if plane.coordinate_labels:
            plane.remove(plane.coordinate_labels[-1])
        self.add(plane)

    def add_title(self):
        title = Text("Vector field")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.add_background_rectangle(opacity=1, buff=SMALL_BUFF)
        self.add(title)

    def points_to_vectors(self):
        vector_field = self.vector_field = VectorField(
            four_swirls_function,
            **self.vector_field_config
        )
        dots = VGroup()
        for vector in vector_field:
            dot = Dot(radius=0.05)
            dot.move_to(vector.get_start())
            dot.target = vector
            dots.add(dot)

        self.play(LaggedStart(GrowFromCenter, dots))
        self.wait()
        self.play(LaggedStart(MoveToTarget, dots, remover=True))
        self.add(vector_field)
        self.wait()

    def show_fluid_flow(self):
        vector_field = self.vector_field
        # 注意：ManimCE 沒有 StreamLines 和 AnimatedStreamLines
        # 這裡使用替代方案展示流線
        stream_lines = VGroup()
        for x in np.arange(-7, 7, 0.5):
            for y in np.arange(-4, 4, 0.5):
                line = Line(
                    start=[x, y, 0],
                    end=[x + 0.3 * np.sin(y), y + 0.3 * np.sin(x), 0],
                    stroke_width=2,
                    color=BLUE
                )
                stream_lines.add(line)
        
        self.play(
            vector_field.animate.set_opacity(0.5),
            Create(stream_lines, run_time=2)
        )
        self.wait(3)
        self.play(
            vector_field.animate.set_opacity(1),
            FadeOut(stream_lines)
        )

    def show_gravitational_force(self):
        # 注意：ImageMobject 在 ManimCE 中是 Image
        # 這裡使用替代圖形
        earth = self.earth = Circle(radius=0.5, color=BLUE, fill_opacity=1)
        moon = self.moon = Circle(radius=0.25, color=GRAY, fill_opacity=1)
        earth_center = 3 * RIGHT + 2 * UP
        moon_center = 3 * LEFT + DOWN
        earth.move_to(earth_center)
        moon.move_to(moon_center)

        gravity_func = get_force_field_func((earth_center, -6), (moon_center, -1))
        gravity_field = VectorField(
            gravity_func,
            **self.vector_field_config
        )

        self.add(earth, moon)
        self.play(
            GrowFromCenter(earth),
            GrowFromCenter(moon),
            Transform(self.vector_field, gravity_field),
            run_time=2
        )
        self.vector_field.func = gravity_field.func
        self.wait()

    def show_magnetic_force(self):
        magnetic_func = get_force_field_func(
            (3 * LEFT, -1), (3 * RIGHT, +1)
        )
        magnetic_field = VectorField(
            magnetic_func,
            **self.vector_field_config
        )
        magnet = VGroup(*[
            Rectangle(
                width=3.5,
                height=1,
                stroke_width=0,
                fill_opacity=1,
                fill_color=color
            )
            for color in (BLUE, RED)
        ])
        magnet.arrange(RIGHT, buff=0)
        for char, vect in ("S", LEFT), ("N", RIGHT):
            letter = Text(char)
            edge = magnet.get_edge_center(vect)
            letter.next_to(edge, -vect, buff=MED_LARGE_BUFF)
            magnet.add(letter)

        self.add(magnet)
        self.play(
            self.earth.animate.scale(0),
            self.moon.animate.scale(0),
            DrawBorderThenFill(magnet),
            Transform(self.vector_field, magnetic_field),
            run_time=2
        )
        self.vector_field.func = magnetic_field.func
        self.remove(self.earth, self.moon)
