# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示向量場在一個點附近的微小變化，通過旋轉步長向量觀察差異向量的點積和叉積，對應散度和旋度的概念。


from manim import *
import numpy as np
import random

class DivergenceTinyNudgesView(MovingCameraScene):
    def __init__(self, scale_factor=0.25, point=ORIGIN, **kwargs):
        super().__init__(**kwargs)
        self.scale_factor = scale_factor
        self.point = point

    def construct(self):
        self.add_vector_field()
        self.zoom_in()
        self.take_tiny_step()
        self.show_dot_product()
        self.show_circle_of_values()
        self.switch_to_curl_words()
        self.rotate_difference_vectors()

    def add_vector_field(self):
        plane = self.plane = NumberPlane()

        def func(p):
            x, y = p[:2]
            result = np.array([
                np.sin(x + 0.1),
                np.cos(2 * y),
                0
            ])
            result /= (np.linalg.norm(result)**0.5 + 1)
            return result

        vector_field = self.vector_field = VectorField(
            func,
            length_func=lambda n: 0.5 * (1 / (1 + np.exp(-n))),  # sigmoid替代
        )
        self.add(plane)
        self.add(vector_field)

    def zoom_in(self):
        point = self.point
        vector_field = self.vector_field
        sf = self.scale_factor

        vector_field.vector_config.update({
            "rectangular_stem_width": 0.02,
            "tip_length": 0.1,
        })
        vector_field.length_func = lambda n: n
        vector = vector_field.get_vector(point)

        input_dot = Dot(point).scale(sf)
        input_words = Text("$(x_0, y_0)$").scale(sf)
        input_words.next_to(input_dot, DL, SMALL_BUFF * sf)
        output_words = Text("Output").scale(sf)
        output_words.add_background_rectangle()
        output_words.next_to(vector.get_end(), UP, sf * SMALL_BUFF)
        output_words.set_color(vector.get_color())

        self.play(
            self.camera.frame.animate.scale(sf).move_to(point),
            FadeOut(vector_field),
            FadeIn(vector),
            run_time=2
        )
        self.add_foreground_mobjects(input_dot)
        self.play(
            FadeIn(input_dot, shift=DL*SMALL_BUFF),
            Write(input_words),
        )
        self.play(
            Indicate(vector),
            Write(output_words),
        )
        self.wait()

        self.point = point
        self.vector = vector
        self.input_dot = input_dot
        self.input_words = input_words
        self.output_words = output_words

    def take_tiny_step(self):
        sf = self.scale_factor
        vector_field = self.vector_field
        point = self.point
        vector = self.vector
        output_words = self.output_words
        input_dot = self.input_dot

        nudge = 0.5 * RIGHT
        nudged_point = point + nudge

        new_vector = vector_field.get_vector(nudged_point)
        new_vector.set_color(YELLOW)
        new_dot = Dot(nudged_point).scale(sf)
        step_vector = Arrow(
            point, nudged_point,
            buff=0,
            color=TEAL,
            **vector_field.vector_config
        )
        step_vector.set_stroke(BLACK, 0.5)

        new_output_words = Text("New output").scale(sf)
        new_output_words.add_background_rectangle()
        new_output_words.next_to(new_vector.get_end(), UP, sf * SMALL_BUFF)
        new_output_words.set_color(new_vector.get_color())
        step_words = Text("Step").scale(sf)
        step_words.next_to(step_vector, UP, buff=0)
        step_words.set_color(step_vector.get_color())
        step_words.add_background_rectangle()
        small_step_words = Text("(think tiny step)").scale(sf)
        small_step_words.next_to(
            step_words, RIGHT,
            buff=sf * MED_SMALL_BUFF,
        )
        small_step_words.add_background_rectangle()
        small_step_words.set_color(step_words.get_color())

        shifted_vector = vector.copy().shift(nudge)
        diff_vector = Arrow(
            shifted_vector.get_end(),
            new_vector.get_end(),
            buff=0,
            color=RED,
            **vector_field.vector_config
        )
        diff_words = Text("Difference").scale(sf)
        diff_words.add_background_rectangle()
        diff_words.next_to(diff_vector.get_start(), UR, buff=2 * sf * SMALL_BUFF)
        diff_words.set_color(diff_vector.get_color())
        diff_words.rotate(
            diff_vector.get_angle(),
            about_point=diff_vector.get_start()
        )

        self.play(
            GrowArrow(step_vector),
            Write(step_words),
            ReplacementTransform(input_dot.copy(), new_dot)
        )
        self.add_foreground_mobjects(new_dot)
        self.play(FadeIn(small_step_words))
        self.play(FadeOut(small_step_words))
        self.play(
            ReplacementTransform(vector.copy(), new_vector),
            ReplacementTransform(output_words.copy(), new_output_words),
        )
        self.wait()
        self.play(ReplacementTransform(
            vector.copy(), shifted_vector,
            path_arc=-TAU / 4
        ))
        self.wait()
        self.play(
            FadeOut(output_words),
            FadeOut(new_output_words),
            GrowArrow(diff_vector),
            Write(diff_words)
        )
        self.wait()
        self.play(
            vector.animate.scale(0, about_point=vector.get_start()),
            shifted_vector.animate.scale(0, about_point=shifted_vector.get_start()),
            ReplacementTransform(
                new_vector,
                diff_vector.copy().shift(-vector.get_vector()),
                remover=True
            ),
            diff_vector.animate.shift(-vector.get_vector()),
            MaintainPositionRelativeTo(diff_words, diff_vector),
            run_time=2
        )
        self.wait()

        self.step_vector = step_vector
        self.step_words = step_words
        self.diff_vector = diff_vector
        self.diff_words = diff_words

    def show_dot_product(self):
        sf = self.scale_factor
        point = self.point
        step_vector = self.step_vector
        step_words = self.step_words
        diff_vector = self.diff_vector
        diff_words = self.diff_words
        vects = VGroup(step_vector, diff_vector)

        moving_step_vector = step_vector.copy()
        moving_diff_vector = diff_vector.copy()

        def update_moving_diff_vector(dv):
            step = moving_step_vector.get_vector()
            o1 = self.vector_field.get_vector(point).get_vector()
            o2 = self.vector_field.get_vector(point + step).get_vector()
            diff = o2 - o1
            dv.put_start_and_end_on(
                moving_step_vector.get_end(),
                moving_step_vector.get_end() + diff,
            )
        moving_diff_vector.add_updater(update_moving_diff_vector)
        self.add(moving_diff_vector)

        div_text = self.get_operator_text("div")

        step_words_copy = step_words.copy()
        diff_words_copy = diff_words.copy()
        copies = VGroup(step_words_copy, diff_words_copy)

        substrings = ["Step", "Difference"]
        dot_product = Text(
            "(Step) $\\cdot$ (Difference)",
            isolate=substrings,
        ).scale(sf)
        group = VGroup(div_text, dot_product)
        group.arrange(RIGHT, buff=sf * MED_SMALL_BUFF)
        group.next_to(
            self.camera.frame.get_top(), DOWN,
            buff=sf * MED_SMALL_BUFF
        )

        for substring, mob, vect in zip(substrings, copies, vects):
            part = dot_product.get_part_by_text(substring)
            mob.generate_target()
            mob.target.rotate(-vect.get_angle())
            mob.target.replace(part)
            part.set_color(mob.get_color())
        dot_product.add_background_rectangle()

        brace = Brace(
            dot_product.copy().scale(1 / sf, about_point=ORIGIN), DOWN,
            buff=SMALL_BUFF
        ).scale(sf, about_point=ORIGIN)
        dp_kwargs = {
            "include_sign": True,
        }
        dot_product_value = DecimalNumber(1.0, **dp_kwargs)
        dot_product_value.scale(sf)
        dot_product_value.next_to(brace, DOWN, sf * SMALL_BUFF)
        
        def update_dot_product_value():
            return np.dot(
                moving_step_vector.get_vector(),
                moving_diff_vector.get_vector(),
            )
        dot_product_value.add_updater(lambda d: d.set_value(update_dot_product_value()))

        self.play(
            Write(dot_product),
            LaggedStartMap(MoveToTarget, copies)
        )
        self.remove(copies)
        self.play(FadeIn(div_text))
        self.play(ShowPassingFlashAround(
            div_text[1:3],
            surrounding_rectangle_config={"buff": sf * SMALL_BUFF}
        ))
        self.add(BackgroundRectangle(dot_product_value))
        self.play(
            GrowFromCenter(brace),
            Write(dot_product_value),
        )
        self.add(dot_product_value)
        self.wait()

        self.div_text = div_text
        self.dot_product = dot_product
        self.moving_step_vector = moving_step_vector
        self.moving_diff_vector = moving_diff_vector
        self.dot_product_value = dot_product_value
        self.brace = brace

    def show_circle_of_values(self):
        point = self.point
        moving_step_vector = self.moving_step_vector
        moving_diff_vector = self.moving_diff_vector

        all_diff_vectors = VGroup()
        all_step_vectors = VGroup()
        n_samples = 12
        angle = TAU / n_samples
        self.add_foreground_mobjects(self.step_words)
        for n in range(n_samples):
            self.play(
                Rotating(
                    moving_step_vector,
                    radians=angle,
                    about_point=point,
                    run_time=15.0 / n_samples,
                    rate_func=linear,
                )
            )
            step_vector_copy = moving_step_vector.copy()
            diff_vector_copy = moving_diff_vector.copy()
            diff_vector_copy.set_stroke(BLACK, 0.5)
            self.add(step_vector_copy, diff_vector_copy)
            all_step_vectors.add(step_vector_copy)
            all_diff_vectors.add(diff_vector_copy)
        self.remove(
            self.step_vector, self.diff_vector,
            self.moving_step_vector, self.moving_diff_vector,
        )
        self.moving_diff_vector.clear_updaters()
        self.dot_product_value.clear_updaters()
        self.remove_foreground_mobjects(self.step_words)
        self.play(
            FadeOut(self.brace),
            FadeOut(self.dot_product_value),
            FadeOut(self.step_words),
            FadeOut(self.diff_words),
        )
        self.wait()

        for s in 0.6, -0.6:
            for step, diff in zip(all_step_vectors, all_diff_vectors):
                diff.generate_target()
                diff.target.put_start_and_end_on(
                    step.get_end(),
                    step.get_end() + s * step.get_vector()
                )
            self.play(
                all_step_vectors.animate.set_fill(opacity=0.5),
                LaggedStartMap(
                    MoveToTarget, all_diff_vectors,
                    run_time=3
                ),
            )
            self.wait()
            self.show_stream_lines(lambda p: s * (p - point))
            self.wait()

        self.all_step_vectors = all_step_vectors
        self.all_diff_vectors = all_diff_vectors

    def switch_to_curl_words(self):
        sf = self.scale_factor
        div_text = self.div_text
        dot_product = self.dot_product

        curl_text = self.get_operator_text("curl")
        cross_product = Text(
            "(Step) $\\times$ (Difference)",
            color_map={
                "Step": TEAL,
                "Difference": RED
            },
        ).scale(sf)
        cross_product.add_background_rectangle(opacity=1)

        group = VGroup(curl_text, cross_product)
        group.arrange(RIGHT, buff=sf * MED_SMALL_BUFF)
        group.next_to(self.camera.frame.get_top(), sf * DOWN)

        self.play(
            dot_product.animate.shift(sf * DOWN).set_opacity(0),
            remover=True
        )
        self.play(FadeIn(cross_product, shift=sf * DOWN))
        self.play(
            div_text.animate.shift(sf * DOWN).set_opacity(0),
            remover=True
        )
        self.play(FadeIn(curl_text, shift=sf * DOWN))
        self.wait()

    def rotate_difference_vectors(self):
        point = self.point
        all_step_vectors = self.all_step_vectors
        all_diff_vectors = self.all_diff_vectors

        for s in 0.6, -0.6:
            for step, diff in zip(all_step_vectors, all_diff_vectors):
                diff.generate_target()
                diff.target.put_start_and_end_on(
                    step.get_end(),
                    step.get_end() + s * rotate_vector(
                        step.get_vector(),
                        90 * DEGREES
                    )
                )
            self.play(
                LaggedStartMap(
                    MoveToTarget, all_diff_vectors,
                    run_time=2
                ),
            )
            self.wait()
            self.show_stream_lines(
                lambda p: s * rotate_vector((p - point), 90 * DEGREES)
            )
            self.wait()

        self.all_step_vectors = all_step_vectors
        self.all_diff_vectors = all_diff_vectors

    def get_operator_text(self, operator):
        text = Text(
            operator + "\\,",
            "$\\textbf{F}(x_0, y_0)\\,$",
            "corresponds to average of",
        ).scale(self.scale_factor)
        text.set_color_by_tex(operator, YELLOW)
        text.add_background_rectangle()
        return text

    def show_stream_lines(self, func):
        point = self.point
        # 簡化流線顯示，使用簡單的線條動畫
        lines = VGroup()
        for x in np.arange(point[0] - 2, point[0] + 2, 0.1):
            for y in np.arange(point[1] - 1, point[1] + 1, 0.1):
                start = np.array([x, y, 0])
                end = start + func(start)
                line = Arrow(start, end, buff=0, stroke_width=1)
                lines.add(line)
        random.shuffle(lines.submobjects)
        self.play(LaggedStartMap(
            Create, lines,
            run_time=2,
            lag_ratio=0.01
        ))
        self.play(FadeOut(lines))
