# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示橢圓的定義性質：從兩個焦點到橢圓上任意一點的距離之和保持不變。


from manim import *
import numpy as np

class ShowEllipseDefiningProperty(Scene):
    def __init__(
        self,
        camera_config={"background_opacity": 1},
        ellipse_color=BLUE,
        a=4.0,
        b=3.0,
        distance_labels_scale_factor=1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.camera.background_opacity = camera_config["background_opacity"]
        self.ellipse_color = ellipse_color
        self.a = a
        self.b = b
        self.distance_labels_scale_factor = distance_labels_scale_factor

    def construct(self):
        self.add_ellipse()
        self.add_focal_lines()
        self.add_distance_labels()
        self.label_foci()
        self.label_focal_sum()

    def add_ellipse(self):
        a = self.a
        b = self.b
        ellipse = Circle(radius=a, color=self.ellipse_color)
        ellipse.stretch(b / a, dim=1)
        ellipse.to_edge(LEFT, buff=LARGE_BUFF)
        self.ellipse = ellipse
        self.add(ellipse)

    def add_focal_lines(self):
        push_pins = VGroup(*[
            SVGMobject(
                file_name="push_pin.svg",
                color=GREY_B,
                fill_opacity=0.8,
                height=0.5,
            ).move_to(point, DR).shift(0.05 * RIGHT)
            for point in self.get_foci()
        ])

        dot = Dot()
        dot.scale(0.5)
        position_tracker = ValueTracker(0.125)
        dot_update = dot.add_updater(
            lambda d: d.move_to(
                self.ellipse.point_from_proportion(
                    position_tracker.get_value() % 1
                )
            )
        )
        
        # 替代 always_shift
        def update_position_tracker(tracker, dt):
            tracker.set_value(tracker.get_value() + 0.05 * dt)
        position_tracker.add_updater(update_position_tracker)

        lines, lines_update_animation = self.get_focal_lines_and_update(
            self.get_foci, dot
        )

        self.add(push_pins, dot)
        self.add(dot_update)
        self.play(LaggedStart(
            *[FadeIn(pin, shift=2*UP+LEFT) for pin in push_pins],
            run_time=1,
            lag_ratio=0.75
        ))
        self.play(Create(lines))
        self.add(lines_update_animation)
        self.add(position_tracker)
        self.wait(2)

        self.position_tracker = position_tracker
        self.focal_lines = lines

    def add_distance_labels(self):
        lines = self.focal_lines
        colors = [YELLOW, PINK]

        distance_labels, distance_labels_animation = \
            self.get_distance_labels_and_update(lines, colors)

        sum_expression, numbers, number_updates = \
            self.get_sum_expression_and_update(
                lines, colors, lambda mob: mob.to_corner(UR)
            )

        sum_expression_fading_rect = Rectangle(
            width=sum_expression.width + 0.2,
            height=sum_expression.height + 0.2,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0
        )
        sum_expression_fading_rect.move_to(sum_expression)

        sum_rect = SurroundingRectangle(numbers[-1])
        constant_words = Text("Stays constant")
        constant_words.next_to(sum_rect, DOWN, aligned_edge=RIGHT)
        VGroup(sum_rect, constant_words).set_color(BLUE)

        self.add(distance_labels_animation)
        for update in number_updates:
            self.add(update)
        self.add(sum_expression)
        self.add(sum_expression_fading_rect)
        self.play(
            FadeIn(distance_labels),
            FadeOut(sum_expression_fading_rect),
        )
        self.remove(sum_expression_fading_rect)
        self.wait(7)
        self.play(
            Create(sum_rect),
            Write(constant_words)
        )
        self.wait(7)
        self.play(FadeOut(sum_rect), FadeOut(constant_words))

        self.sum_expression = sum_expression
        self.sum_rect = sum_rect

    def label_foci(self):
        foci = self.get_foci()
        focus_words = VGroup(*[
            Text("Focus").next_to(focus, DOWN)
            for focus in foci
        ])
        foci_word = Text("Foci")
        foci_word.move_to(focus_words)
        foci_word.shift(MED_SMALL_BUFF * UP)
        connecting_lines = VGroup(*[
            Arrow(
                foci_word.get_edge_center(-edge),
                focus_word.get_edge_center(edge),
                buff=MED_SMALL_BUFF,
                stroke_width=2,
            )
            for focus_word, edge in zip(focus_words, [LEFT, RIGHT])
        ])

        translation = Text(
            "``Foco'' → Fireplace"
        )
        translation.to_edge(RIGHT)
        translation.shift(UP)
        
        # 替代 ImageMobject
        sun = Circle(radius=0.25, color=YELLOW, fill_opacity=1)
        sun.move_to(foci[0])
        
        # 簡化太陽動畫
        def sun_animation_update(mob, dt):
            mob.rotate(dt * 30 * DEGREES)
        sun.add_updater(sun_animation_update)

        self.play(FadeIn(focus_words, shift=DOWN))
        self.wait(2)
        self.play(
            ReplacementTransform(focus_words.copy(), foci_word),
        )
        self.play(*[Create(line) for line in connecting_lines])
        for word in list(focus_words) + [foci_word]:
            word.add_background_rectangle()
            self.add(word)
        self.wait(4)
        self.play(Write(translation))
        self.wait(2)
        self.play(GrowFromCenter(sun))
        self.add(sun)
        self.wait(8)
        
        # 移除更新器
        sun.remove_updater(sun_animation_update)

    def label_focal_sum(self):
        sum_rect = self.sum_rect

        focal_sum = Text("``Focal sum''")
        focal_sum.scale(1.5)
        focal_sum.next_to(sum_rect, DOWN, aligned_edge=RIGHT)
        VGroup(sum_rect, focal_sum).set_color(RED)

        footnote = Text(
            "*This happens to equal the longest distance\n"
            "across the ellipse, so perhaps the more standard\n"
            "terminology would be ``major axis'', but I want\n"
            "some terminology that conveys the idea of adding\n"
            "two distances to the foci.",
            font_size=24,
        )
        footnote.set_width(5)
        footnote.to_corner(DR)
        footnote.set_stroke(WHITE, 0.5)

        self.play(FadeIn(focal_sum, shift=DOWN))
        self.play(Create(sum_rect))
        self.wait()
        self.play(FadeIn(footnote))
        self.wait(2)
        self.play(FadeOut(footnote))
        self.wait(8)

    # Helpers
    def get_foci(self):
        ellipse = self.ellipse
        a = ellipse.get_width() / 2
        b = ellipse.get_height() / 2
        c = np.sqrt(a**2 - b**2)
        center = ellipse.get_center()
        return [
            center + c * RIGHT,
            center + c * LEFT,
        ]

    def get_focal_lines_and_update(self, get_foci, focal_sum_point):
        lines = VGroup(Line(LEFT, RIGHT), Line(LEFT, RIGHT))
        lines.set_stroke(width=2)

        def update_lines(lines):
            foci = get_foci()
            for line, focus in zip(lines, foci):
                line.put_start_and_end_on(
                    focus, focal_sum_point.get_center()
                )
            lines[1].rotate(np.pi)
        lines_update_animation = lines.add_updater(update_lines)
        return lines, lines_update_animation

    def get_distance_labels_and_update(self, lines, colors):
        distance_labels = VGroup(
            DecimalNumber(0), DecimalNumber(0),
        )
        for label in distance_labels:
            label.scale(self.distance_labels_scale_factor)

        def update_distance_labels(labels):
            for label, line, color in zip(labels, lines, colors):
                angle = -line.get_angle()
                if np.abs(angle) > 90 * DEGREES:
                    angle = 180 * DEGREES + angle
                line.rotate(angle, about_point=ORIGIN)
                new_decimal = DecimalNumber(line.get_length())
                new_decimal.scale(
                    self.distance_labels_scale_factor
                )
                max_width = 0.6 * line.get_width()
                if new_decimal.get_width() > max_width:
                    new_decimal.set_width(max_width)
                new_decimal.next_to(line, UP, buff=SMALL_BUFF)
                new_decimal.set_color(color)
                new_decimal.add_to_back(
                    new_decimal.copy().set_stroke(BLACK, 5)
                )
                VGroup(new_decimal, line).rotate(
                    -angle, about_point=ORIGIN
                )
                label.submobjects = list(new_decimal.submobjects)

        distance_labels_animation = distance_labels.add_updater(update_distance_labels)

        return distance_labels, distance_labels_animation

    def get_sum_expression_and_update(self, lines, colors, sum_position_func):
        sum_expression = MathTex("0.00", "+", "0.00", "=", "0.00")
        sum_position_func(sum_expression)
        
        # 獲取數字部分
        number_refs = VGroup(*[sum_expression[i] for i in [0, 2, 4]])
        number_refs.set_fill(opacity=0)
        
        numbers = VGroup(*[DecimalNumber(0) for _ in range(3)])
        for number, color in zip(numbers, colors + [WHITE]):
            number.set_color(color)

        # 創建持續更新的數字
        number_updates = []
        
        # 第一個數字（對應第二個距離）
        def update_num1(mob):
            mob.set_value(lines[1].get_length())
            mob.move_to(number_refs[0], LEFT)
        numbers[0].add_updater(update_num1)
        number_updates.append(numbers[0])
        
        # 第二個數字（對應第一個距離）
        def update_num2(mob):
            mob.set_value(lines[0].get_length())
            mob.move_to(number_refs[1], LEFT)
        numbers[1].add_updater(update_num2)
        number_updates.append(numbers[1])
        
        # 總和
        def update_sum(mob):
            mob.set_value(lines[0].get_length() + lines[1].get_length())
            mob.move_to(number_refs[2], LEFT)
        numbers[2].add_updater(update_sum)
        number_updates.append(numbers[2])

        return sum_expression, numbers, number_updates
