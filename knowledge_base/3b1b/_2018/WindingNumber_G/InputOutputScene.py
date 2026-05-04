# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個複數函數的輸入平面與輸出平面，並用彩色映射和點陣列表示函數映射關係。


from manim import *
import numpy as np

class InputOutputScene(Scene):
    def __init__(
        self,
        plane_width=6,
        plane_height=6,
        x_shift=FRAME_WIDTH/4,  # FRAME_X_RADIUS/2 在 CE 中等於 FRAME_WIDTH/4
        y_shift=MED_LARGE_BUFF,
        output_scalar=10,
        non_renormalized_func=None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.plane_width = plane_width
        self.plane_height = plane_height
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.output_scalar = output_scalar
        
        # 定義預設的 non_renormalized_func
        if non_renormalized_func is None:
            # 模擬原來的 plane_func_by_wind_spec 函數
            # 這裡用一個簡單的複數函數替代：f(z) = z^3 - 2z + 1
            def default_func(coord_pair):
                x, y = coord_pair
                z = complex(x, y)
                w = z**3 - 2*z + 1
                return (w.real, w.imag)
            self.non_rennormalized_func = default_func
        else:
            self.non_rennormalized_func = non_renormalized_func

    ###

    def func(self, coord_pair):
        out_coords = np.array(self.non_rennormalized_func(coord_pair))
        out_norm = np.linalg.norm(out_coords)
        if out_norm > 1:
            angle = np.arctan2(out_coords[1], out_coords[0])
            factor = 0.5 - 0.1 * np.cos(4 * angle)
            target_norm = factor * np.log(out_norm)
            out_coords *= target_norm / out_norm
        else:
            out_coords = (0, 0)
        return tuple(out_coords)

    def point_function(self, point):
        in_coords = self.input_plane.point_to_coords(point)
        out_coords = self.func(in_coords)
        return self.output_plane.coords_to_point(*out_coords)

    def get_colorings(self):
        # 在 CE 中沒有 ColorMappedObjectsScene，用漸變色矩形替代
        input_coloring = Rectangle(
            height=self.plane_height,
            width=self.plane_width,
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=1,
        )
        output_coloring = input_coloring.copy()
        colorings = VGroup(input_coloring, output_coloring)
        
        # 創建漸變色效果
        colors = [BLUE, GREEN, YELLOW, RED]
        for coloring, vect in zip(colorings, [LEFT, RIGHT]):
            coloring.move_to(self.x_shift * vect + self.y_shift * DOWN)
            # 使用漸變色填充
            coloring.set_fill(
                color=color_gradient(colors, 10),
                opacity=1
            )
        
        return colorings

    def get_planes(self):
        input_plane = self.input_plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=self.plane_width,
            y_length=self.plane_height,
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        output_plane = self.output_plane = input_plane.copy()
        planes = VGroup(input_plane, output_plane)
        
        vects = [LEFT, RIGHT]
        label_texts = ["Input", "Output"]
        label_colors = [GREEN, RED]
        
        for plane, vect, text, color in zip(planes, vects, label_texts, label_colors):
            plane.move_to(vect * FRAME_WIDTH/4 + self.y_shift * DOWN)
            
            # 添加坐標標籤
            labels = VGroup()
            for i in range(-2, 3):
                if i != 0:
                    x_label = MathTex(str(i)).scale(0.5)
                    y_label = MathTex(str(i)).scale(0.5)
                    x_label.next_to(plane.c2p(i, 0), DOWN, buff=0.1)
                    y_label.next_to(plane.c2p(0, i), LEFT, buff=0.1)
                    labels.add(x_label, y_label)
            plane.add(labels)
            
            # 添加標題
            label = Text(text, font_size=36)
            label.set_color(color)
            label.add_background_rectangle(buff=0.1, color=BLACK, opacity=0.7)
            label.move_to(plane)
            label.to_edge(UP, buff=MED_SMALL_BUFF)
            plane.add(label)
            plane.label = label
        
        return planes

    def get_v_line(self):
        v_line = Line(UP, DOWN).scale(FRAME_HEIGHT/2)
        v_line.set_stroke(WHITE, 5)
        return v_line

    def get_dots(self, input_plane, output_plane, dot_density=0.2, dot_radius=0.03):
        step = dot_density
        x_min = -3.0
        x_max = 3.0
        y_min = -3.0
        y_max = 3.0
        dots = VGroup()
        
        for x in np.arange(x_min, x_max + step, step):
            for y in np.arange(y_max, y_min - step, -step):
                out_coords = self.func((x, y))
                dot = Dot(radius=dot_radius)
                dot.set_stroke(BLACK, 1)
                dot.move_to(input_plane.c2p(x, y))
                dot.original_position = dot.get_center()
                
                dot.generate_target()
                dot.target.move_to(output_plane.c2p(*out_coords))
                
                # 根據輸出坐標計算顏色
                scaled_coords = tuple(self.output_scalar * np.array(out_coords))
                # 簡單的顏色映射：根據坐標大小映射到色譜
                hue = (np.arctan2(scaled_coords[1], scaled_coords[0]) + np.pi) / (2 * np.pi)
                sat = min(1.0, np.linalg.norm(scaled_coords) / 10)
                dot.target_color = color_gradient([RED, YELLOW, GREEN, BLUE, PURPLE], 100)[
                    int(hue * 99)
                ]
                dots.add(dot)
        
        return dots

    def construct(self):
        # 獲取平面
        planes = self.get_planes()
        input_plane, output_plane = planes
        
        # 獲取彩色背景
        colorings = self.get_colorings()
        
        # 獲取垂直分隔線
        v_line = self.get_v_line()
        
        # 獲取點陣列
        dots = self.get_dots(input_plane, output_plane)
        
        # 添加所有元素到場景
        self.add(colorings[0], input_plane)
        self.add(colorings[1], output_plane)
        self.add(v_line)
        self.add(dots)
        
        # 動畫：點從輸入平面移動到輸出平面
        self.play(
            *[dot.animate.move_to(dot.target).set_color(dot.target_color) for dot in dots],
            run_time=3
        )
        self.wait(2)
