from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = Text("Vector Addition: The Triangle Method", color=WHITE, font_size=40)
        self.objects["title"] = title

        # Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": GRAY_B}
        )
        self.objects["axes"] = axes

        # Vector A
        vec_a = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            buff=0,
            color=BLUE,
            stroke_width=6,
            tip_length=0.2
        )
        self.objects["vec_a"] = vec_a

        # Vector B
        vec_b = Arrow(
            start=[0, 0, 0],
            end=[1, 2, 0],
            buff=0,
            color=RED,
            stroke_width=6,
            tip_length=0.2
        )
        self.objects["vec_b"] = vec_b

        # Label A
        label_a = MathTex(r"\vec{A} = (3,1)", color=BLUE, font_size=30)
        self.objects["label_a"] = label_a

        # Label B
        label_b = MathTex(r"\vec{B} = (1,2)", color=RED, font_size=30)
        self.objects["label_b"] = label_b

        # Vector B copy (for translation)
        vec_b_copy = Arrow(
            start=[0, 0, 0],
            end=[1, 2, 0],
            buff=0,
            color=RED,
            stroke_width=6,
            tip_length=0.2
        )
        vec_b_copy.set_opacity(0)
        self.objects["vec_b_copy"] = vec_b_copy

        # Triangle
        triangle = Polygon(
            [0, 0, 0],
            [3, 1, 0],
            [4, 3, 0],
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=3
        )
        triangle.set_opacity(0)
        self.objects["triangle"] = triangle

        # Resultant Vector C
        vec_c = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            buff=0,
            color=YELLOW,
            stroke_width=8,
            tip_length=0.25
        )
        vec_c.set_opacity(0)
        self.objects["vec_c"] = vec_c

        # Label C
        label_c = MathTex(r"\vec{C} = (4,3)", color=YELLOW, font_size=30)
        label_c.set_opacity(0)
        self.objects["label_c"] = label_c

        # Step text
        step_text = Text("Step 1: Draw vectors A and B from the origin.", color=GRAY_B, font_size=28)
        self.objects["step_text"] = step_text

        # Component calculation
        calc_components = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (3+1,\; 1+2)", color=WHITE, font_size=32)
        calc_components.set_opacity(0)
        self.objects["calc_components"] = calc_components

        # Final result
        calc_result = MathTex(r"\vec{C} = (4,\; 3)", color=YELLOW, font_size=32)
        calc_result.set_opacity(0)
        self.objects["calc_result"] = calc_result

        # Initialize Layout Engine
        layout = LayoutEngine()

        # Register objects
        obj_title = LayoutObject(title, "title")
        obj_axes = LayoutObject(axes, "axes")
        obj_vec_a = LayoutObject(vec_a, "vec_a")
        obj_vec_b = LayoutObject(vec_b, "vec_b")
        obj_label_a = LayoutObject(label_a, "label_a")
        obj_label_b = LayoutObject(label_b, "label_b")
        obj_vec_b_copy = LayoutObject(vec_b_copy, "vec_b_copy")
        obj_triangle = LayoutObject(triangle, "triangle")
        obj_vec_c = LayoutObject(vec_c, "vec_c")
        obj_label_c = LayoutObject(label_c, "label_c")
        obj_step_text = LayoutObject(step_text, "step_text")
        obj_calc_components = LayoutObject(calc_components, "calc_components")
        obj_calc_result = LayoutObject(calc_result, "calc_result")

        layout.add(obj_title)
        layout.add(obj_axes)
        layout.add(obj_vec_a)
        layout.add(obj_vec_b)
        layout.add(obj_label_a)
        layout.add(obj_label_b)
        layout.add(obj_vec_b_copy)
        layout.add(obj_triangle)
        layout.add(obj_vec_c)
        layout.add(obj_label_c)
        layout.add(obj_step_text)
        layout.add(obj_calc_components)
        layout.add(obj_calc_result)

        # Assign to zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_axes, "CONTENT")
        layout.add_to_zone(obj_vec_a, "CONTENT")
        layout.add_to_zone(obj_vec_b, "CONTENT")
        layout.add_to_zone(obj_label_a, "CONTENT")
        layout.add_to_zone(obj_label_b, "CONTENT")
        layout.add_to_zone(obj_vec_b_copy, "CONTENT")
        layout.add_to_zone(obj_triangle, "CONTENT")
        layout.add_to_zone(obj_vec_c, "CONTENT")
        layout.add_to_zone(obj_label_c, "CONTENT")
        layout.add_to_zone(obj_step_text, "FOOTER")
        layout.add_to_zone(obj_calc_components, "FOOTER")
        layout.add_to_zone(obj_calc_result, "FOOTER")

        # Center title and step text horizontally
        layout.add_constraint(obj_title.center_x == 0)
        layout.add_constraint(obj_step_text.center_x == 0)
        layout.add_constraint(obj_calc_components.center_x == 0)
        layout.add_constraint(obj_calc_result.center_x == 0)

        # Align calc_components below step_text
        layout.add_constraint(obj_calc_components.top == obj_step_text.bottom + 0.5)

        # Solve layout
        layout.solve()

        # Apply relative positioning for labels (after layout solves main positions)
        label_a.move_to(vec_a.get_end() + 0.2 * RIGHT)
        label_b.move_to(vec_b.get_end() + 0.2 * UP)
        label_c.move_to(vec_c.get_end() + 0.2 * (UP + RIGHT))

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(axes), run_time=2.0)
        remaining_1 = max(0.1, 6.528 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(vec_a, color=BLUE, run_time=1), Indicate(vec_b, color=RED, run_time=1))
        self.play(
            Create(vec_a),
            Create(vec_b),
            Write(label_a),
            Write(label_b),
            run_time=2.5
        )
        remaining_2 = max(0.1, 7.512 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(vec_b, color=RED, run_time=1))
        self.play(FadeIn(vec_b_copy, run_time=0.5))
        self.play(
            vec_b_copy.animate.shift([3, 1, 0]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 6.912 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(triangle, color=GREEN, run_time=1))
        self.play(Create(triangle), run_time=2.0)
        remaining_4 = max(0.1, 6.432 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(vec_c, color=YELLOW, run_time=1))
        self.play(
            Create(vec_c),
            FadeOut(vec_b_copy),
            FadeIn(label_c),
            run_time=3.0
        )
        remaining_5 = max(0.1, 10.632 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(FadeIn(calc_components), run_time=1.5)
        remaining_6 = max(0.1, 8.904 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Circumscribe(calc_result, color=YELLOW, run_time=1))
        self.play(TransformMatchingTex(calc_components, calc_result), run_time=2.0)
        remaining_7 = max(0.1, 6.912 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Final hold
        self.wait(max(0.1, 2))