# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示捕食者-被捕食者模型的相空間，包含坐標軸、向量場、相流線和微分方程。



from manim import *
class PhaseSpaceOfPopulationModel(Scene):
    def __init__(
        self,
        origin=5 * LEFT + 2.5 * DOWN,
        vector_field_config=None,
        pi_creatures_start_on_screen=False,
        default_pi_creature_kwargs=None,
        flow_time=10,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.origin = origin
        self.vector_field_config = vector_field_config or {"max_magnitude": 50}
        self.pi_creatures_start_on_screen = pi_creatures_start_on_screen
        self.default_pi_creature_kwargs = default_pi_creature_kwargs or {"height": 1.8}
        self.flow_time = flow_time
        self.start_num_rabbits = 10
        self.start_num_foxes = 10

    def construct(self):
        self.add_axes()
        self.add_example_point()
        self.write_differential_equations()
        self.add_vectors()
        self.show_phase_flow()

    def add_axes(self):
        axes = self.axes = Axes(
            x_range=[0, 55, 10],
            y_range=[0, 55, 10],
            x_length=55 * 0.15,
            y_length=55 * 0.09,
            axis_config={
                "include_numbers": True,
                "numbers_to_exclude": [0],
            },
        )
        axes.shift(self.origin)
        
        # 添加數字標籤
        for axis in [axes.x_axis, axes.y_axis]:
            numbers = VGroup(*[
                Integer(num).next_to(axis.number_to_point(num), DOWN if axis is axes.x_axis else LEFT)
                for num in range(10, 60, 10)
            ])
            axis.add(numbers)

        axes_labels = self.axes_labels = VGroup(*[
            VGroup(
                self.get_rabbit() if i == 0 else self.get_fox(),
                Text("Population"),
            ).arrange(RIGHT, buff=MED_SMALL_BUFF)
            for i in range(2)
        ])
        
        axes_labels[0].next_to(axes.x_axis, RIGHT, aligned_edge=axes_labels[0][0].get_bottom())
        axes_labels[1].next_to(axes.y_axis, UP, aligned_edge=axes_labels[1][0].get_left())

        self.add(axes, axes_labels)

    def add_example_point(self):
        axes = self.axes
        origin = self.origin
        x = self.start_num_rabbits
        y = self.start_num_foxes
        point = axes.c2p(x, y)
        x_point = axes.c2p(x, 0)
        y_point = axes.c2p(0, y)
        v_line = DashedLine(x_point, point)
        h_line = DashedLine(y_point, point)
        v_line.set_color(FOX_COLOR)
        h_line.set_color(GREY_B)
        dot = Dot(point)

        coord_pair = MathTex("(10, 10)")
        pop_sizes = VGroup(Integer(10), Integer(10))
        pop_sizes[0].set_color(GREY_B)
        pop_sizes[1].set_color(FOX_COLOR)
        
        # 將數字替換為pop_sizes
        coord_pair[0][1:3].set_opacity(0)  # 第一個10
        coord_pair[0][4:6].set_opacity(0)  # 第二個10
        pop_sizes[0].move_to(coord_pair[0][1:3])
        pop_sizes[1].move_to(coord_pair[0][4:6])
        coord_pair.add(pop_sizes)

        def get_pop_size_update(i):
            return always_redraw(lambda: pop_sizes[i].set_value(
                int(np.round(axes.p2c(dot.get_center())[i]))
            ).move_to(coord_pair[0][1:3] if i == 0 else coord_pair[0][4:6]))
        
        coord_pair.add_background_rectangle()
        coord_pair_update = always_redraw(lambda: coord_pair.next_to(dot, UR, SMALL_BUFF))
        pop_sizes_updates = [get_pop_size_update(i) for i in (0, 1)]

        phase_space = Text("``Phase space''", color=YELLOW, font_size=36)
        phase_space.to_edge(UP)
        phase_space.shift(2 * RIGHT)

        self.play(Create(v_line))
        self.play(Create(h_line))
        dot.save_state()
        dot.move_to(origin)
        self.add(coord_pair_update)
        for update in pop_sizes_updates:
            self.add(update)
        self.play(
            dot.animate.restore(),
            FadeIn(coord_pair),
            UpdateFromAlphaFunc(pop_sizes, lambda m, a: m.set_opacity(a)),
        )
        self.wait()
        self.play(Write(phase_space))
        self.wait(2)
        self.play(FadeOut(VGroup(h_line, v_line, phase_space)))
        self.play(Rotate(
            dot,
            angle=2 * PI,
            about_point=axes.c2p(30, 30),
            rate_func=smooth,
        ))

        self.dot = dot
        self.coord_pair = coord_pair
        self.coord_pair_update = coord_pair_update
        self.pop_sizes = pop_sizes
        self.pop_sizes_updates = pop_sizes_updates

    def write_differential_equations(self):
        equations = self.get_equations()
        equations.shift(2 * DOWN)
        rect = SurroundingRectangle(equations, color=YELLOW)
        rect.set_fill(BLACK, 0.8)
        title = Text("Differential equations", color=YELLOW)
        title.next_to(rect, UP)
        self.differential_equation_group = VGroup(
            rect, equations, title
        )
        self.differential_equation_group.to_corner(UR)

        # 由於PiCreatureScene在CE中不可用，我們用一個簡單的圖標代替
        randy = SVGMobject("pi_creatures/thinking")
        randy.set_height(1.8)
        randy.next_to(rect, DL)

        self.play(
            Write(title, run_time=1),
            Create(rect)
        )
        self.play(
            LaggedStart(*[FadeIn(eq) for eq in equations]),
            FadeIn(randy),
        )
        self.wait(3)

    def add_vectors(self):
        origin = self.axes.c2p(0, 0)
        dot = self.dot

        def rescaled_field(point):
            x, y = self.axes.p2c(point)
            result = self.predator_prey_vector_field(np.array([x, y, 0]))
            return self.axes.c2p(*result[:2]) - origin

        self.vector_field_config.update({
            "x_min": origin[0] + 0.5,
            "x_max": self.axes.get_right()[0] + 1,
            "y_min": origin[1] + 0.5,
            "y_max": self.axes.get_top()[1],
        })
        vector_field = VectorField(
            rescaled_field, **self.vector_field_config
        )

        def get_dot_vector():
            vector = vector_field.get_vector(dot.get_center())
            vector.scale(1, about_point=vector.get_start())
            return vector

        dot_vector = get_dot_vector()

        self.play(
            LaggedStart(*[GrowArrow(v) for v in vector_field]),
            Animation(self.differential_equation_group)
        )
        self.wait(3)
        self.play(
            vector_field.animate.set_opacity(0.2),
            Animation(self.differential_equation_group),
            GrowArrow(dot_vector),
        )
        self.wait()
        self.play(
            dot.animate.move_to(dot_vector.get_end()).align_to(dot, RIGHT),
            run_time=3,
        )
        self.wait(2)
        self.play(
            dot.animate.move_to(dot_vector.get_end()),
            run_time=3,
        )
        self.wait(2)
        for x in range(6):
            new_dot_vector = get_dot_vector()
            fade_anims = [
                FadeOut(dot_vector),
                FadeIn(new_dot_vector),
            ]
            if x == 4:
                fade_anims += [
                    vector_field.animate.set_opacity(0.5),
                    FadeOut(self.differential_equation_group),
                ]
            self.play(*fade_anims)
            dot_vector = new_dot_vector
            self.play(dot.animate.move_to(dot_vector.get_end()))

        # 簡化：沿向量場移動點
        dot_movement = self.move_along_vector_field(dot, vector_field)
        self.add(dot_movement)
        self.play(FadeOut(dot_vector))
        self.wait(10)
        self.play(
            vector_field.animate.set_opacity(1.0),
            FadeOut(dot),
            FadeOut(self.coord_pair),
            UpdateFromAlphaFunc(self.pop_sizes, lambda m, a: m.set_opacity(1 - a)),
        )
        self.remove(
            self.coord_pair_update,
            *self.pop_sizes_updates
        )
        self.wait()

        self.vector_field = vector_field

    def show_phase_flow(self):
        vector_field = self.vector_field
        # 在ManimCE中，StreamLines需要自定義實現
        # 這裡我們用一個簡化版本：創建一些沿向量場移動的點
        stream_lines = self.create_stream_lines(vector_field)
        self.add(stream_lines)
        self.add(vector_field)
        self.wait(self.flow_time)
        self.play(
            self.camera.frame.animate.scale(1.5).move_to(self.origin),
            run_time=self.flow_time,
        )
        self.wait(self.flow_time)

    def get_equations(self):
        equations = MathTex(
            r"""
                {dX \over dt} =
                X \cdot (\alpha - \beta Y) \\
                \quad \\
                {dY \over dt} =
                Y \cdot (\delta X - \gamma)
            """
        )
        # 用動物圖標替換變量
        rabbit = self.get_rabbit()
        fox = self.get_fox().flip()
        
        rabbit_target = equations[0][0]  # X
        fox_target = equations[0][15]   # Y
        
        rabbit_copy = rabbit.copy()
        rabbit_copy.set_height(0.5)
        rabbit_copy.move_to(rabbit_target, DL)
        
        fox_copy = fox.copy()
        fox_copy.set_height(0.5)
        fox_copy.move_to(fox_target, DL)
        
        equations[0][0].become(rabbit_copy)
        equations[0][15].become(fox_copy)
        
        return equations

    # 輔助方法
    def get_rabbit(self):
        # 簡化：用一個圓形代表兔子
        rabbit = Circle(color=GREY_B, fill_opacity=1)
        rabbit.set_height(0.5)
        return rabbit

    def get_fox(self):
        # 簡化：用一個三角形代表狐狸
        fox = Triangle(color=FOX_COLOR, fill_opacity=1)
        fox.set_height(0.5)
        return fox

    def predator_prey_vector_field(self, point):
        # 捕食者-被捕食者模型的向量場
        x, y, z = point
        alpha, beta, delta, gamma = 0.1, 0.02, 0.01, 0.5
        dx = x * (alpha - beta * y)
        dy = y * (delta * x - gamma)
        return np.array([dx, dy, 0])

    def move_along_vector_field(self, mobject, vector_field, speed=0.3):
        # 簡化：沿向量場移動物體
        def update(mob, dt):
            point = mob.get_center()
            vector = vector_field.func(point)
            mob.shift(speed * dt * vector)
        mobject.add_updater(update)
        return mobject

    def create_stream_lines(self, vector_field, num_lines=20):
        # 創建簡化的流線
        lines = VGroup()
        for i in range(num_lines):
            start_x = np.random.uniform(vector_field.x_min, vector_field.x_max)
            start_y = np.random.uniform(vector_field.y_min, vector_field.y_max)
            start_point = np.array([start_x, start_y, 0])
            
            line = VMobject()
            points = [start_point]
            for _ in range(50):
                vector = vector_field.func(points[-1])
                if np.linalg.norm(vector) < 0.1:
                    break
                new_point = points[-1] + 0.1 * vector / np.linalg.norm(vector)
                points.append(new_point)
            
            line.set_points_smoothly(points)
            line.set_stroke(width=1, opacity=0.7)
            lines.add(line)
        
        # 添加動畫：流線逐漸出現
        animation = Succession(
            *[Create(line, run_time=0.5) for line in lines],
            lag_ratio=0.1
        )
        return lines
