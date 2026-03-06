'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the transformation of the parent parabola y=x^2 into y=(x-2)^2-3 through horizontal and vertical shifts.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.0] for Title and Step Label
#    - Main Content: [Center y=0] for Axes, Parabola, Vertex Dot, Labels
#    - Footer Region: [Bottom y=-3.0] for Explanation Text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for parabola and its vertex dot to keep them together during transformations.
#    - Keep equation label near the curve, vertex label near the dot, axis label near the line.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/graphing_parabola_transformational/step_XX.mp3"
# 5. Animation Flow:
#    - Setup axes, parent parabola, labels.
#    - Step 1: Show axes.
#    - Step 2: Show vertex dot and parabola.
#    - Step 3: Label parent equation.
#    - Step 4-6: Horizontal shift (update step label, explanation, equation, transform parabola).
#    - Step 7-9: Vertical shift (update step label, explanation, equation, transform parabola).
#    - Step 10-13: Label vertex and axis of symmetry.
#    - Step 14: Final summary.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        title_anchor = 3.0 * UP
        explanation_anchor = 3.0 * DOWN
        global_center = ORIGIN

        # Create objects from layout_plan
        # Title
        title = Text("Graphing a Parabola: Transformational Approach", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Step Label
        step_label = Text("Step 1: The Parent Function", color=YELLOW, font_size=28)
        step_label.next_to(title, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # Axes
        axes = Axes(
            x_range=[-4, 6, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=8,
            axis_config={"include_numbers": True, "color": GRAY_C}
        )
        axes.move_to(global_center)
        self.objects["axes"] = axes

        # Parent Parabola (FunctionGraph)
        parabola_parent = axes.plot(
            lambda x: x**2,
            x_range=[-4, 4, 0.01],
            color=BLUE,
            stroke_width=4
        )
        self.objects["parabola_parent"] = parabola_parent

        # Parent Equation Label
        eq_label_parent = MathTex(r"y = x^2", color=BLUE)
        # Position will be set relative to parabola after it's created
        self.objects["eq_label_parent"] = eq_label_parent

        # Vertex Dot for parent
        vertex_parent_dot = Dot(radius=0.08, color=BLUE, fill_opacity=1.0)
        vertex_parent_dot.move_to(axes.c2p(0, 0))
        self.objects["vertex_parent_dot"] = vertex_parent_dot

        # Explanation Text
        explanation_text = Text("We start with the basic parabola, vertex at the origin.", color=GRAY_C, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # Additional objects defined in visual_action details (steps 11,12,13)
        # Vertex Label (will be created at step 11)
        vertex_label = MathTex(r"V(2,-3)", color=GREEN)
        self.objects["vertex_label"] = vertex_label  # placeholder, position set later

        # Axis of Symmetry Line (dashed)
        axis_symmetry = DashedLine(
            start=axes.c2p(2, axes.y_range[0]),
            end=axes.c2p(2, axes.y_range[1]),
            color=RED,
            stroke_width=3,
            dash_length=0.2
        )
        self.objects["axis_symmetry"] = axis_symmetry

        # Axis Label
        axis_label = MathTex(r"x = 2", color=RED)
        self.objects["axis_label"] = axis_label  # placeholder, position set later

        # Group parabola and dot for synchronized transformation
        parabola_group = VGroup(parabola_parent, vertex_parent_dot)
        self.objects["parabola_group"] = parabola_group

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Audio base path
        audio_base = "media/audio/graphing_parabola_transformational"

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = os.path.join(audio_base, "step_00.mp3")
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(axes), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = os.path.join(audio_base, "step_01.mp3")
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(vertex_parent_dot), run_time=0.5)
        self.play(Create(parabola_parent), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = os.path.join(audio_base, "step_02.mp3")
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # Position equation label relative to parabola
        eq_label_parent.next_to(parabola_parent, UP, buff=0.2).shift(LEFT*2)
        self.play(Write(eq_label_parent), run_time=1.0)
        remaining_3 = max(0.1, 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = os.path.join(audio_base, "step_03.mp3")
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        step_label_new = Text("Step 2: Horizontal Shift", color=YELLOW, font_size=28)
        step_label_new.next_to(title, DOWN, buff=0.3)
        explanation_new = Text("The term (x-2) shifts the graph 2 units to the RIGHT.", color=GRAY_C, font_size=24)
        explanation_new.move_to(explanation_anchor)
        self.play(
            ReplacementTransform(step_label, step_label_new),
            ReplacementTransform(explanation_text, explanation_new)
        )
        step_label = step_label_new
        explanation_text = explanation_new
        self.objects["step_label"] = step_label
        self.objects["explanation_text"] = explanation_text
        remaining_4 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = os.path.join(audio_base, "step_04.mp3")
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(eq_label_parent, color=YELLOW, run_time=1))
        eq_label_new = MathTex(r"y = (x-2)^2", color=BLUE)
        eq_label_new.move_to(eq_label_parent.get_center())
        self.play(TransformMatchingTex(eq_label_parent, eq_label_new))
        eq_label_parent = eq_label_new
        self.objects["eq_label_parent"] = eq_label_parent
        remaining_5 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = os.path.join(audio_base, "step_05.mp3")
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Indicate(vertex_parent_dot, color=RED, run_time=1))
        # Create new parabola for horizontal shift
        parabola_horizontal = axes.plot(
            lambda x: (x-2)**2,
            x_range=[-2, 6, 0.01],
            color=BLUE,
            stroke_width=4
        )
        # Create new dot at (2,0)
        vertex_horizontal_dot = Dot(radius=0.08, color=BLUE, fill_opacity=1.0)
        vertex_horizontal_dot.move_to(axes.c2p(2, 0))
        parabola_group_horizontal = VGroup(parabola_horizontal, vertex_horizontal_dot)
        # Transform the group
        self.play(Transform(parabola_group, parabola_group_horizontal), run_time=2.0)
        # Update references
        parabola_parent = parabola_horizontal
        vertex_parent_dot = vertex_horizontal_dot
        parabola_group = parabola_group_horizontal
        self.objects["parabola_parent"] = parabola_parent
        self.objects["vertex_parent_dot"] = vertex_parent_dot
        self.objects["parabola_group"] = parabola_group
        remaining_6 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = os.path.join(audio_base, "step_06.mp3")
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        step_label_new = Text("Step 3: Vertical Shift", color=YELLOW, font_size=28)
        step_label_new.next_to(title, DOWN, buff=0.3)
        explanation_new = Text("The term -3 shifts the graph 3 units DOWN.", color=GRAY_C, font_size=24)
        explanation_new.move_to(explanation_anchor)
        self.play(
            ReplacementTransform(step_label, step_label_new),
            ReplacementTransform(explanation_text, explanation_new)
        )
        step_label = step_label_new
        explanation_text = explanation_new
        self.objects["step_label"] = step_label
        self.objects["explanation_text"] = explanation_text
        remaining_7 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = os.path.join(audio_base, "step_07.mp3")
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Indicate(eq_label_parent, color=YELLOW, run_time=1))
        eq_label_new = MathTex(r"y = (x-2)^2 - 3", color=BLUE)
        eq_label_new.move_to(eq_label_parent.get_center())
        self.play(TransformMatchingTex(eq_label_parent, eq_label_new))
        eq_label_parent = eq_label_new
        self.objects["eq_label_parent"] = eq_label_parent
        remaining_8 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = os.path.join(audio_base, "step_08.mp3")
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Indicate(vertex_parent_dot, color=RED, run_time=1))
        # Create final parabola
        parabola_final = axes.plot(
            lambda x: (x-2)**2 - 3,
            x_range=[-2, 6, 0.01],
            color=BLUE,
            stroke_width=4
        )
        # Create final dot at (2,-3)
        vertex_final_dot = Dot(radius=0.08, color=BLUE, fill_opacity=1.0)
        vertex_final_dot.move_to(axes.c2p(2, -3))
        parabola_group_final = VGroup(parabola_final, vertex_final_dot)
        self.play(Transform(parabola_group, parabola_group_final), run_time=2.0)
        # Update references
        parabola_parent = parabola_final
        vertex_parent_dot = vertex_final_dot
        parabola_group = parabola_group_final
        self.objects["parabola_parent"] = parabola_parent
        self.objects["vertex_parent_dot"] = vertex_parent_dot
        self.objects["parabola_group"] = parabola_group
        remaining_9 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = os.path.join(audio_base, "step_09.mp3")
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        step_label_new = Text("Step 4: Labeling Key Features", color=YELLOW, font_size=28)
        step_label_new.next_to(title, DOWN, buff=0.3)
        explanation_new = Text("The vertex is (h,k). The axis of symmetry is x = h.", color=GRAY_C, font_size=24)
        explanation_new.move_to(explanation_anchor)
        self.play(
            ReplacementTransform(step_label, step_label_new),
            ReplacementTransform(explanation_text, explanation_new)
        )
        step_label = step_label_new
        explanation_text = explanation_new
        self.objects["step_label"] = step_label
        self.objects["explanation_text"] = explanation_text
        remaining_10 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_10.mp3")  # [auto-injected]
        # Step 11
        audio_step11 = os.path.join(audio_base, "step_10.mp3")
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        self.play(Circumscribe(vertex_parent_dot, color=GREEN, run_time=1))
        # Position and create vertex label
        vertex_label.next_to(vertex_parent_dot, RIGHT, buff=0.2)
        self.play(Write(vertex_label), run_time=1.5)
        remaining_11 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_11))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_11.mp3")  # [auto-injected]
        # Step 12
        audio_step12 = os.path.join(audio_base, "step_11.mp3")
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        self.play(Create(axis_symmetry), run_time=1.5)
        remaining_12 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_12))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_12.mp3")  # [auto-injected]
        # Step 13
        audio_step13 = os.path.join(audio_base, "step_12.mp3")
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))
        # Position axis label
        axis_label.next_to(axis_symmetry.get_top(), UP, buff=0.1)
        self.play(Write(axis_label), run_time=1.0)
        remaining_13 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_13))

        self.add_sound("media/audio/Create_a_graph_of_th_17f57adaca/step_13.mp3")  # [auto-injected]
        # Step 14
        audio_step14 = os.path.join(audio_base, "step_13.mp3")
        if os.path.exists(audio_step14):
            self.add_sound(audio_step14)
        elif os.path.exists(audio_step14.replace(".mp3", ".wav")):
            self.add_sound(audio_step14.replace(".mp3", ".wav"))
        step_label_new = Text("Complete Graph", color=GREEN, font_size=28)
        step_label_new.next_to(title, DOWN, buff=0.3)
        explanation_new = Text("Final parabola: y = (x-2)² - 3. Vertex: (2,-3). Axis: x=2.", color=GRAY_C, font_size=24)
        explanation_new.move_to(explanation_anchor)
        self.play(
            ReplacementTransform(step_label, step_label_new),
            ReplacementTransform(explanation_text, explanation_new),
            run_time=2.0
        )
        remaining_14 = max(0.1, 5.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_14))

        # Final hold
        self.wait(max(0.1, 2))