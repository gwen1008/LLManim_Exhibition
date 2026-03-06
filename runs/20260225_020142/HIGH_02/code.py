from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = Text("Graphing y = (x-2)² - 3", color=WHITE, font_size=36)
        self.objects["title"] = title

        # Axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=8,
            axis_config={"include_numbers": True}
        )
        self.objects["axes"] = axes

        # Parent Graph (y = x^2)
        parent_graph = axes.plot(lambda x: x**2, x_range=[-2.5, 4.5, 0.1])
        parent_graph.set_color(GRAY).set_stroke(width=3)
        self.objects["parent_graph"] = parent_graph

        # Final Graph (y = (x-2)^2 - 3)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-0.5, 4.5, 0.1])
        final_graph.set_color(BLUE).set_stroke(width=4)
        self.objects["final_graph"] = final_graph

        # Vertex Point
        vertex_point = Dot(axes.c2p(2, -3), radius=0.08, color=RED, fill_opacity=1.0)
        self.objects["vertex_point"] = vertex_point

        # Vertex Label
        vertex_label = MathTex("(2,-3)", color=RED, font_size=24)
        self.objects["vertex_label"] = vertex_label

        # Axis Line (x=2)
        axis_line = DashedLine(
            start=axes.c2p(2, axes.y_range[0]),
            end=axes.c2p(2, axes.y_range[1]),
            color=GREEN,
            stroke_width=3,
            dashed_ratio=0.5
        )
        self.objects["axis_line"] = axis_line

        # Axis Label
        axis_label = MathTex("x=2", color=GREEN, font_size=24)
        self.objects["axis_label"] = axis_label

        # Step Label
        step_label = Text("Step 1: Start with y = x²", color=YELLOW, font_size=28)
        self.objects["step_label"] = step_label

        # Explanation Text
        explanation_text = Text(
            "The basic parabola, vertex at (0,0), axis at x=0.",
            color=LIGHT_GRAY, font_size=24
        )
        self.objects["explanation_text"] = explanation_text

        # Temporary graph for step 3 transformation (y = (x-2)^2)
        shifted_graph = axes.plot(lambda x: (x-2)**2, x_range=[-0.5, 4.5, 0.1])
        shifted_graph.set_color(GRAY).set_stroke(width=3)
        self.objects["shifted_graph"] = shifted_graph

        # ========== Manual Layout (without LayoutEngine) ==========
        # Position title at top
        title.move_to(UP * 3.0)
        # Position axes at center
        axes.move_to(ORIGIN)
        # Position step label below title
        step_label.next_to(title, DOWN, buff=0.5)
        # Position explanation text at bottom
        explanation_text.move_to(DOWN * 3.5)

        # Position dependent objects after axes are placed
        vertex_point.move_to(axes.c2p(2, -3))
        vertex_label.next_to(vertex_point, UP + LEFT, buff=0.25)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)

        # Initially hide objects that appear later
        final_graph.set_opacity(0)
        vertex_point.set_opacity(0)
        vertex_label.set_opacity(0)
        axis_line.set_opacity(0)
        axis_label.set_opacity(0)
        shifted_graph.set_opacity(0)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(title), run_time=1.0)
        self.play(Create(axes), run_time=2.0)
        self.play(Write(step_label), Write(explanation_text), run_time=1.5)
        remaining_1 = max(0.1, 5.928 - (1.0 + 2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(parent_graph), run_time=2.0)
        self.play(Indicate(parent_graph, color=YELLOW, run_time=1.0))
        remaining_2 = max(0.1, 5.424 - (2.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal Action
        self.play(Circumscribe(step_label, color=ORANGE, run_time=1.0))

        # Update labels
        step_label_new = Text("Step 2: Shift right → (x-2)²", color=YELLOW, font_size=28)
        step_label_new.move_to(step_label.get_center())
        explanation_new = Text(
            "Horizontal shift right by 2 units. Vertex: (2,0). Axis: x=2.",
            color=LIGHT_GRAY, font_size=24
        )
        explanation_new.move_to(explanation_text.get_center())

        self.play(
            ReplacementTransform(step_label, step_label_new),
            ReplacementTransform(explanation_text, explanation_new),
            run_time=1.5
        )
        self.objects["step_label"] = step_label_new
        self.objects["explanation_text"] = explanation_new

        # Transform parent graph to shifted graph (horizontal shift)
        self.play(Transform(parent_graph, shifted_graph), run_time=2.0)
        # Create axis line and label
        self.play(Create(axis_line), Write(axis_label), run_time=1.5)

        remaining_3 = max(0.1, 16.152 - (1.0 + 1.5 + 2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal Action
        self.play(Indicate(vertex_point, color=RED, run_time=1.0))

        # Update labels
        step_label_new2 = Text("Step 3: Shift down → -3", color=YELLOW, font_size=28)
        step_label_new2.move_to(step_label_new.get_center())
        explanation_new2 = Text(
            "Vertical shift down by 3 units. Final vertex: (2, -3).",
            color=LIGHT_GRAY, font_size=24
        )
        explanation_new2.move_to(explanation_new.get_center())

        self.play(
            ReplacementTransform(step_label_new, step_label_new2),
            ReplacementTransform(explanation_new, explanation_new2),
            run_time=1.5
        )
        self.objects["step_label"] = step_label_new2
        self.objects["explanation_text"] = explanation_new2

        # Transform shifted graph to final graph (vertical shift)
        self.play(Transform(shifted_graph, final_graph), run_time=2.0)
        # Create vertex and label
        self.play(FadeIn(vertex_point), Write(vertex_label), run_time=1.5)

        remaining_4 = max(0.1, 16.032 - (1.0 + 1.5 + 2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal Actions
        self.play(
            Circumscribe(final_graph, color=BLUE, run_time=1.5),
            Indicate(vertex_point, color=RED, run_time=1.5),
            Indicate(axis_line, color=GREEN, run_time=1.5)
        )

        remaining_5 = max(0.1, 14.04 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))