'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the transformation of the parent parabola y=x^2 into y=(x-2)^2-3, showing how horizontal and vertical shifts affect the graph and define the vertex and axis of symmetry.
# 2. Layout Strategy: Use High-Low Split.
#    - Header Region: [y=3.5] for Title equation.
#    - Main Content: [Center y=0] for coordinate axes and parabola.
#    - Footer Region: [Bottom y=-3.5] for step explanation text.
# 3. Anti-Overlap Check:
#    - Title, axes, and explanation are in separate zones.
#    - Vertex label and axis label are placed with buff to avoid overlap with the curve.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/quadratic_transformation/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes, signal title.
#    - Step 2: Create parent parabola.
#    - Step 3: Transform title, shift parabola right, update explanation.
#    - Step 4: Transform title to final form, shift parabola down, change color, update explanation.
#    - Step 5: Show vertex dot and label.
#    - Step 6: Show axis of symmetry line and label.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_an_animation__e6d21a0a81/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title_equation
        title_equation = MathTex(r"y = x^2", color=BLUE)
        title_equation.move_to(title_anchor)
        self.objects["title_equation"] = title_equation

        # axes
        axes = Axes(
            x_range=[-4, 6, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes

        # parent_parabola
        parent_parabola = axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE, stroke_width=3)
        parent_parabola.move_to(content_center)
        self.objects["parent_parabola"] = parent_parabola

        # target_parabola (initially invisible, for reference only)
        target_parabola = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-1, 5], color=GREEN, stroke_width=3)
        target_parabola.move_to(content_center + RIGHT*2 + DOWN*3)
        target_parabola.set_opacity(0.0)
        self.objects["target_parabola"] = target_parabola

        # vertex_dot
        vertex_dot = Dot(axes.c2p(2, -3), radius=0.08, color=RED)
        vertex_dot.set_opacity(0.0)
        self.objects["vertex_dot"] = vertex_dot

        # vertex_label
        vertex_label = MathTex(r"(2, -3)", color=RED, font_size=36)
        vertex_label.next_to(axes.c2p(2, -3), UP+RIGHT, buff=0.2)
        vertex_label.set_opacity(0.0)
        self.objects["vertex_label"] = vertex_label

        # axis_line
        axis_line = DashedLine(start=UP*5, end=DOWN*5, color=YELLOW, stroke_width=2)
        axis_line.move_to(content_center + RIGHT*2)
        axis_line.set_opacity(0.0)
        self.objects["axis_line"] = axis_line

        # axis_label
        axis_label = MathTex(r"x = 2", color=YELLOW, font_size=36)
        axis_label.next_to(axes.c2p(2, 4), RIGHT, buff=0.3)
        axis_label.set_opacity(0.0)
        self.objects["axis_label"] = axis_label

        # step_explanation
        step_explanation = Text("We start with the basic parabola, y = x^2.", color=WHITE, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/quadratic_transformation/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Signal action: Circumscribe title_equation
        self.play(Circumscribe(self.objects["title_equation"], color=YELLOW, run_time=1))
        # Visual action: Create axes
        self.play(Create(self.objects["axes"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/quadratic_transformation/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # No signal action
        # Visual action: Create parent_parabola
        self.play(Create(self.objects["parent_parabola"]), run_time=2.5)
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/quadratic_transformation/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate parent_parabola
        self.play(Indicate(self.objects["parent_parabola"], color=BLUE, run_time=1))
        # Visual actions:
        # 1. ReplacementTransform title_equation to y = (x-2)^2
        title_eq_step3 = MathTex(r"y = (x-2)^2", color=BLUE)
        title_eq_step3.move_to(title_anchor)
        self.play(ReplacementTransform(self.objects["title_equation"], title_eq_step3))
        self.objects["title_equation"] = title_eq_step3

        # 2. ApplyMethod shift parent_parabola RIGHT*2
        self.play(self.objects["parent_parabola"].animate.shift(RIGHT*2), run_time=1.5)

        # 3. ReplacementTransform step_explanation
        step_explanation_step3 = Text("The (x-2) shifts the graph 2 units to the right.", color=WHITE, font_size=28)
        step_explanation_step3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_step3))
        self.objects["step_explanation"] = step_explanation_step3

        remaining_3 = max(0.1, 4.0 - (1 + 1.5 + 1) + 0.5)  # signal 1s, title transform ~1s, shift 1.5s, text transform ~1s
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/quadratic_transformation/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate parent_parabola
        self.play(Indicate(self.objects["parent_parabola"], color=BLUE, run_time=1))
        # Visual actions:
        # 1. ReplacementTransform title_equation to final form
        title_eq_step4 = MathTex(r"y = (x-2)^2 - 3", color=BLUE)
        title_eq_step4.move_to(title_anchor)
        self.play(ReplacementTransform(self.objects["title_equation"], title_eq_step4))
        self.objects["title_equation"] = title_eq_step4

        # 2. ApplyMethod shift parent_parabola DOWN*3
        self.play(self.objects["parent_parabola"].animate.shift(DOWN*3), run_time=1.5)

        # 3. ChangeColor parent_parabola from BLUE to GREEN
        self.play(self.objects["parent_parabola"].animate.set_color(GREEN), run_time=1)

        # 4. ReplacementTransform step_explanation
        step_explanation_step4 = Text("The -3 shifts the graph down by 3 units, giving us the final function.", color=WHITE, font_size=28)
        step_explanation_step4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_step4))
        self.objects["step_explanation"] = step_explanation_step4

        remaining_4 = max(0.1, 4.0 - (1 + 1 + 1.5 + 1 + 1) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/quadratic_transformation/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # No signal action
        # Visual actions:
        # 1. FadeIn vertex_dot
        self.play(FadeIn(self.objects["vertex_dot"]), run_time=1)
        # 2. Write vertex_label
        self.play(Write(self.objects["vertex_label"]), run_time=1)
        # 3. ReplacementTransform step_explanation
        step_explanation_step5 = Text("The vertex is at (2, -3), the point where the parabola turns.", color=WHITE, font_size=28)
        step_explanation_step5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_step5))
        self.objects["step_explanation"] = step_explanation_step5

        remaining_5 = max(0.1, 3.5 - (1 + 1 + 1) + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/quadratic_transformation/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: Circumscribe vertex_dot
        self.play(Circumscribe(self.objects["vertex_dot"], color=YELLOW, run_time=1))
        # Visual actions:
        # 1. Create axis_line (make it visible)
        self.objects["axis_line"].set_opacity(1.0)
        self.play(Create(self.objects["axis_line"]), run_time=1.5)
        # 2. Write axis_label
        self.objects["axis_label"].set_opacity(1.0)
        self.play(Write(self.objects["axis_label"]), run_time=1)
        # 3. ReplacementTransform step_explanation
        step_explanation_step6 = Text("The axis of symmetry is the vertical line x = 2, passing through the vertex.", color=WHITE, font_size=28)
        step_explanation_step6.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_step6))
        self.objects["step_explanation"] = step_explanation_step6

        remaining_6 = max(0.1, 4.5 - (1 + 1.5 + 1 + 1) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))