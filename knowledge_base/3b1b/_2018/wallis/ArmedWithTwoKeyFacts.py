# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示兩個圓形燈塔陣列，分別計算距離乘積為 2 和 N，並引入 Wallis 乘積公式。


from manim import *
import itertools as it

class ArmedWithTwoKeyFacts(Scene):
    def __init__(
        self,
        num_lighthouses=6,
        ambient_light_config={
            "opacity_function": lambda r: 1 / (1 + r**6),  # 近似 inverse_power_law
            "radius": 1,
            "num_levels": 100,
            "max_opacity": 1,
        },
        **kwargs
    ):
        super().__init__(**kwargs)
        self.num_lighthouses = num_lighthouses
        self.ambient_light_config = ambient_light_config
        
        # 初始化教師和學生場景元素（簡化版）
        self.teacher = Dot(color=BLUE)
        self.students = VGroup(*[Dot(color=GREEN) for _ in range(3)])
        self.teacher.to_edge(UP)
        self.students.arrange(DOWN, buff=0.5).to_edge(DOWN)
        
        # 初始化圓形
        self.circle = Circle()
        
    def get_lights(self):
        # 簡化燈光生成
        lights = VGroup()
        for i in range(self.num_lighthouses):
            angle = i * 2 * PI / self.num_lighthouses
            point = self.circle.point_at_angle(angle)
            light = Dot(point, color=YELLOW, radius=0.1)
            lights.add(light)
        return lights
    
    def get_circle_point_at_proportion(self, proportion):
        angle = proportion * 2 * PI
        return self.circle.point_at_angle(angle)
    
    def get_distance_lines(self, point, line_class=DashedLine):
        lines = VGroup()
        for light in self.get_lights():
            line = line_class(point, light.get_center(), color=WHITE, stroke_width=2)
            lines.add(line)
        return lines
    
    def change_students(self, *modes, look_at=None):
        # 簡化學生狀態變化
        return AnimationGroup(*[
            student.animate.set_color(color)
            for student, color in zip(self.students, [GREEN, GREEN, GREEN])
        ])
    
    def construct(self):
        # 添加教師和學生
        self.add(self.teacher, self.students)
        
        circle1 = Circle()
        circle1.set_height(1.5)
        circle1.to_corner(UL)
        circle2 = circle1.copy()
        circle2.next_to(circle1, DOWN, buff=MED_LARGE_BUFF)

        # 簡化 Wallis 乘積顯示
        wallis_product = MathTex(r"\frac{2}{1} \cdot \frac{2}{3} \cdot \frac{4}{3} \cdot \frac{4}{5} \cdots")
        wallis_product.scale(0.7)

        N = self.num_lighthouses
        labels = VGroup()
        
        for circle, f, dp in [(circle1, 0.5, "2"), (circle2, 0, "N")]:
            self.circle = circle
            lights = self.get_lights()
            if f == 0:
                lights.submobjects.pop(0)  # 移除第一個燈塔
            
            observer = Dot(color=MAROON_B)
            frac = f / N
            point = self.get_circle_point_at_proportion(frac)
            observer.move_to(point)
            lines = self.get_distance_lines(point, line_class=DashedLine)

            label = Text(f"Distance product = {dp}", font_size=24)
            label.next_to(circle, RIGHT)
            labels.add(label)

            group = VGroup(lines, observer, label)
            
            # 創建動畫序列
            self.play(
                Create(circle),
                LaggedStart(*[FadeIn(light) for light in lights]),
                LaggedStart(*[FadeIn(mob) for mob in group]),
                self.teacher.animate.set_color(BLUE),
                self.change_students("pondering", "pondering", "pondering")
            )
            
        wallis_product.move_to(labels).to_edge(RIGHT)
        self.play(
            LaggedStart(*[FadeIn(term) for term in wallis_product]),
            self.teacher.animate.set_color(GREEN),
            self.change_students("thinking", "thinking", "thinking", look_at=wallis_product)
        )
        self.wait(2)
