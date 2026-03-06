from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = MathTex(r"y = (x-2)^2 - 3", color="#FFFF8D", font_size=48)
        self.objects["title"] = title

        # Axes (NumberPlane)
        axes = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-5, 5, 1],
            x_length=14,
            y_length=10,
            stroke_opacity=0.5,
            axis_config={"stroke_opacity": 1}
        )
        self.objects["axes"] = axes

        # Vertex dot
        vertex_dot = Dot(radius=0.08, color="#FF5252", fill_opacity=1.0)
        vertex_dot.move_to([2, -3, 0])
        self.objects["vertex_dot"] = vertex_dot

        # Vertex label
        vertex_label = MathTex(r"(2,\,-3)", color="#FF5252", font_size=36)
        # Position will be set relative to vertex_dot after creation
        self.objects["vertex_label"] = vertex_label

        # Axis of symmetry line
        axis_line = Line(start=[2, -5, 0], end=[2, 5, 0], color="#80DEEA", stroke_width=4, stroke_opacity=0.8)
        self.objects["axis_line"] = axis_line

        # Parabola curve
        parabola_curve = ParametricFunction(
            lambda t: np.array([t, (t-2)**2 - 3, 0]),
            t_range=[-1, 5],
            color="#69F0AE",
            stroke_width=6
        )
        self.objects["parabola_curve"] = parabola_curve

        # Step explanation text
        step_explanation = Text("We begin by setting up the coordinate plane.", color=WHITE, font_size=28)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Position title at top, axes at center, explanation at bottom
        title.move_to(3.5 * UP)
        axes.move_to(ORIGIN)
        step_explanation.move_to(3.5 * DOWN)

        # Signal action: Indicate title
        self.play(Indicate(self.objects["title"], color=YELLOW, run_time=1))
        # Visual action: Create axes
        self.play(Create(self.objects["axes"]), run_time=2.5)
        remaining_1 = max(0.1, 7.488 - 2.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Update explanation text
        new_explanation = Text("The vertex form of a parabola reveals its turning point.", color=WHITE, font_size=28)
        new_explanation.move_to(3.5 * DOWN)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation

        # Position vertex label relative to dot - FIXED: Move to UP instead of UP+RIGHT to avoid overlap
        self.objects["vertex_label"].next_to(self.objects["vertex_dot"], UP, buff=0.15)

        # Visual actions: Create vertex dot and write label
        self.play(Create(self.objects["vertex_dot"]), run_time=1.5)
        self.play(Write(self.objects["vertex_label"]), run_time=1.5)
        remaining_2 = max(0.1, 8.688 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Update explanation text
        new_explanation2 = Text("Parabolas are symmetric. The vertical line through the vertex is the axis of symmetry.", color=WHITE, font_size=28)
        new_explanation2.move_to(3.5 * DOWN)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation2))
        self.objects["step_explanation"] = new_explanation2

        # Signal action: Circumscribe vertex label
        self.play(Circumscribe(self.objects["vertex_label"], color=YELLOW, run_time=1))
        # Visual action: Create axis line (make it dashed)
        axis_line_dashed = DashedVMobject(self.objects["axis_line"], num_dashes=20)
        self.objects["axis_line"] = axis_line_dashed
        self.play(Create(axis_line_dashed), run_time=2.0)
        remaining_3 = max(0.1, 8.088 - 2.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Update explanation text
        new_explanation3 = Text("Now, we draw the parabola itself. It opens upwards and is symmetric.", color=WHITE, font_size=28)
        new_explanation3.move_to(3.5 * DOWN)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation3))
        self.objects["step_explanation"] = new_explanation3

        # Signal action: Indicate axis line
        self.play(Indicate(self.objects["axis_line"], color=YELLOW, run_time=1))
        # Visual action: Create parabola curve
        self.play(Create(self.objects["parabola_curve"]), run_time=3.0)
        remaining_4 = max(0.1, 8.712 - 3.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Update explanation text
        new_explanation4 = Text("The graph of y = (x-2)^2 - 3, with vertex and axis of symmetry.", color=WHITE, font_size=28)
        new_explanation4.move_to(3.5 * DOWN)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation4))
        self.objects["step_explanation"] = new_explanation4

        # Signal actions: Indicate parabola, vertex, axis line
        self.play(
            Indicate(self.objects["parabola_curve"], color=GREEN, run_time=1.5),
            Indicate(self.objects["vertex_dot"], color=RED, run_time=1.5),
            Indicate(self.objects["axis_line"], color=BLUE, run_time=1.5)
        )
        remaining_5 = max(0.1, 9.6 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))