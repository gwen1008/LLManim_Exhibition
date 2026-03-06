'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the transformation of the parent parabola y=x² into y=(x-2)²-3 to understand vertex form.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for Axes and Parabolas
#    - Footer Region: [Bottom y=-3.5] for Explanation Text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for related objects (e.g., vertex point and label). Keep step label below title, explanation at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_the_parabola_re_a55f895d06/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Indicate parent equation, create parent parabola.
#    - Step 3: Circumscribe final eq, update text, shift parabola right.
#    - Step 4: Circumscribe final eq, update text, shift parabola down, transform equation.
#    - Step 5: Update text, fade in vertex, axis line, and labels.
#    - Step 6: Indicate final eq, update text, hold final scene.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        step_label_anchor = None  # Will be positioned relative to title
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": True}
        )
        axes.move_to(content_center)
        axes.set_color(GRAY_B)  # GRAY_C -> GRAY_B
        self.objects["axes"] = axes

        # title
        title = Text("Graphing a Parabola from Vertex Form", font_size=36)
        title.move_to(title_anchor)
        title.set_color(WHITE)
        self.objects["title"] = title

        # step_label
        step_label = Text("Step 1: Start with the parent function y = x²", font_size=28)
        step_label.next_to(title, DOWN, buff=0.3)
        step_label.set_color(YELLOW)
        self.objects["step_label"] = step_label

        # parent_parabola
        # Use axes.plot as per implementation_hints
        parent_parabola = axes.plot(lambda x: x**2, x_range=[-2, 6])
        parent_parabola.set_color(BLUE)
        parent_parabola.set_stroke(width=4)
        self.objects["parent_parabola"] = parent_parabola

        # parent_eq
        parent_eq = MathTex(r"y = x^2", font_size=32)
        parent_eq.next_to(step_label, DOWN, buff=0.5)
        parent_eq.set_color(BLUE)
        self.objects["parent_eq"] = parent_eq

        # transformed_parabola
        transformed_parabola = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-2, 6])
        transformed_parabola.set_color(GREEN)
        transformed_parabola.set_stroke(width=4)
        transformed_parabola.set_opacity(0.0)
        self.objects["transformed_parabola"] = transformed_parabola

        # final_eq
        final_eq = MathTex(r"y = (x-2)^2 - 3", font_size=32)
        final_eq.move_to(parent_eq.get_center())
        final_eq.set_color(GREEN)
        final_eq.set_opacity(0.0)
        self.objects["final_eq"] = final_eq

        # axis_line
        axis_line = DashedLine(
            start=axes.c2p(2, axes.y_range[1]),
            end=axes.c2p(2, axes.y_range[0]),
            stroke_width=3,
            dash_length=0.1
        )
        axis_line.set_color(RED)
        axis_line.set_opacity(0.0)
        self.objects["axis_line"] = axis_line

        # vertex_point
        vertex_point = Dot(radius=0.08)
        vertex_point.move_to(axes.c2p(2, -3))
        vertex_point.set_color(YELLOW)
        vertex_point.set_opacity(0.0)
        self.objects["vertex_point"] = vertex_point

        # vertex_label
        vertex_label = MathTex(r"(2,\,-3)", font_size=24)
        vertex_label.next_to(vertex_point, UP+RIGHT, buff=0.1)
        vertex_label.set_color(YELLOW)
        vertex_label.set_opacity(0.0)
        self.objects["vertex_label"] = vertex_label

        # axis_label
        axis_label = MathTex(r"x = 2", font_size=24)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)
        axis_label.set_color(RED)
        axis_label.set_opacity(0.0)
        self.objects["axis_label"] = axis_label

        # explanation_text
        explanation_text = Text("The basic parabola, symmetric about the y-axis (x=0).", font_size=24)
        explanation_text.move_to(explanation_anchor)
        explanation_text.set_color(GRAY_B)  # GRAY_C -> GRAY_B
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Draw_the_parabola_re_a55f895d06/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(axes), run_time=2.0)
        remaining_1 = max(0.1, 9.408 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Draw_the_parabola_re_a55f895d06/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(parent_eq, color=BLUE, run_time=1))
        self.play(Create(parent_parabola), run_time=2.0)
        remaining_2 = max(0.1, 4.104 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Draw_the_parabola_re_a55f895d06/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(final_eq, color=YELLOW, run_time=1))

        step_label_new = Text("Step 2: Horizontal Shift (x → x-2)", font_size=28)
        step_label_new.next_to(title, DOWN, buff=0.3)
        step_label_new.set_color(YELLOW)

        explanation_new = Text("The (x-2) shifts every point on the parabola 2 units to the right.", font_size=24)
        explanation_new.move_to(explanation_anchor)
        explanation_new.set_color(GRAY_B)

        self.play(
            Transform(self.objects["step_label"], step_label_new),
            Transform(self.objects["explanation_text"], explanation_new),
            self.objects["parent_parabola"].animate.shift(RIGHT*2),
            run_time=3.0
        )
        self.objects["step_label"] = step_label_new
        self.objects["explanation_text"] = explanation_new
        remaining_3 = max(0.1, 11.904 - 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Draw_the_parabola_re_a55f895d06/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(final_eq, color=YELLOW, run_time=1))

        step_label_new2 = Text("Step 3: Vertical Shift (y → y-3)", font_size=28)
        step_label_new2.next_to(title, DOWN, buff=0.3)
        step_label_new2.set_color(YELLOW)

        explanation_new2 = Text("The -3 shifts the entire parabola down by 3 units.", font_size=24)
        explanation_new2.move_to(explanation_anchor)
        explanation_new2.set_color(GRAY_B)

        # Prepare for equation transform: set final_eq opacity to 1, parent_eq to 0 during transform
        final_eq.set_opacity(1.0)
        parent_eq.set_opacity(0.0)

        self.play(
            Transform(self.objects["step_label"], step_label_new2),
            Transform(self.objects["explanation_text"], explanation_new2),
            self.objects["parent_parabola"].animate.shift(DOWN*3),
            TransformMatchingTex(parent_eq, final_eq, path_arc=90),
            run_time=3.0
        )
        self.objects["step_label"] = step_label_new2
        self.objects["explanation_text"] = explanation_new2
        self.objects["parent_eq"] = final_eq  # Update registry
        remaining_4 = max(0.1, 6.912 - 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Draw_the_parabola_re_a55f895d06/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        step_label_new3 = Text("Step 4: Vertex & Axis of Symmetry", font_size=28)
        step_label_new3.next_to(title, DOWN, buff=0.3)
        step_label_new3.set_color(YELLOW)

        explanation_new3 = Text("The vertex (h,k) is at (2,-3). The axis of symmetry is the vertical line x = h.", font_size=24)
        explanation_new3.move_to(explanation_anchor)
        explanation_new3.set_color(GRAY_B)

        self.play(
            Transform(self.objects["step_label"], step_label_new3),
            Transform(self.objects["explanation_text"], explanation_new3),
            run_time=1.5
        )
        self.objects["step_label"] = step_label_new3
        self.objects["explanation_text"] = explanation_new3

        self.play(
            FadeIn(vertex_point),
            FadeIn(vertex_label),
            FadeIn(axis_line),
            FadeIn(axis_label),
            run_time=2.0
        )
        remaining_5 = max(0.1, 13.44 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Draw_the_parabola_re_a55f895d06/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(final_eq, color=GREEN, run_time=1))

        step_label_new4 = Text("Final Graph", font_size=28)
        step_label_new4.next_to(title, DOWN, buff=0.3)
        step_label_new4.set_color(YELLOW)

        explanation_new4 = Text("The graph of y = (x-2)² - 3 is a parabola with vertex (2,-3) and axis x=2.", font_size=24)
        explanation_new4.move_to(explanation_anchor)
        explanation_new4.set_color(GRAY_B)

        self.play(
            Transform(self.objects["step_label"], step_label_new4),
            Transform(self.objects["explanation_text"], explanation_new4),
            run_time=1.5
        )
        self.objects["step_label"] = step_label_new4
        self.objects["explanation_text"] = explanation_new4

        remaining_6 = max(0.1, 14.112 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))