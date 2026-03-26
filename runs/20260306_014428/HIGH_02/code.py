from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Graphing the Parabola: y = (x-2)² - 3", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": True},
            color=GRAY_C
        )
        axes.move_to(global_center).scale(0.8)
        self.objects["axes"] = axes

        # Parent function label
        parent_func_label = MathTex(r"y = x^2", color=BLUE)
        parent_func_label.next_to(axes.c2p(0, 0), UP + LEFT, buff=0.5)
        self.objects["parent_func_label"] = parent_func_label

        # Shifted right label (will be created later for transformation)
        shifted_right_label = MathTex(r"y = (x-2)^2", color=GREEN)
        shifted_right_label.next_to(axes.c2p(2, 0), UP, buff=0.5)
        self.objects["shifted_right_label"] = shifted_right_label

        # Final function label (will be created later for transformation)
        final_func_label = MathTex(r"y = (x-2)^2 - 3", color=YELLOW)
        final_func_label.next_to(axes.c2p(2, -3), UP + RIGHT, buff=0.5)
        self.objects["final_func_label"] = final_func_label

        # Vertex dot
        vertex_dot = Dot(radius=0.08, color=RED, fill_opacity=1.0)
        vertex_dot.move_to(axes.c2p(2, -3))
        self.objects["vertex_dot"] = vertex_dot

        # Vertex label
        vertex_label = MathTex(r"(2,\,-3)", color=RED)
        vertex_label.next_to(vertex_dot, RIGHT, buff=0.2)
        self.objects["vertex_label"] = vertex_label

        # Axis line
        axis_line = DashedLine(
            start=axes.c2p(2, axes.y_range[0]),
            end=axes.c2p(2, axes.y_range[1]),
            color=PURPLE,
            stroke_width=3,
            dash_length=0.1
        )
        self.objects["axis_line"] = axis_line

        # Axis label
        axis_label = MathTex(r"x = 2", color=PURPLE)
        axis_label.next_to(axes.c2p(2, axes.y_range[1]), UP, buff=0.1)
        self.objects["axis_label"] = axis_label

        # Step explanation
        step_explanation = Text("Step 1: Start with the parent function y = x².", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Create graphs (these are not in objects registry but will be animated)
        parent_graph = axes.plot(lambda x: x**2, color=BLUE)
        shifted_right_graph = axes.plot(lambda x: (x-2)**2, color=GREEN)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, color=YELLOW)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # [missing audio] self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_00.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_0 = 2.00  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(axes), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_01.mp3")  # [auto-injected] duration=7.37s
        _audio_dur_1 = 7.37  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Write(parent_func_label), run_time=2.0)
        self.play(Create(parent_graph), run_time=2.0)
        total_anim_time_2 = 2.0 + 2.0
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        # [missing audio] self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_02.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Indicate(parent_func_label, color=YELLOW, run_time=1))
        self.play(
            ReplacementTransform(parent_func_label, shifted_right_label),
            ReplacementTransform(parent_graph, shifted_right_graph),
            run_time=3.0
        )
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        # Update explanation for step 4
        step_explanation_4 = Text("Step 4: Apply vertical shift down by 3 units.", color=GRAY_C, font_size=24)
        step_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_4))
        self.objects["step_explanation"] = step_explanation_4

        # [missing audio] self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Indicate(shifted_right_label, color=YELLOW, run_time=1))
        self.play(
            ReplacementTransform(shifted_right_label, final_func_label),
            ReplacementTransform(shifted_right_graph, final_graph),
            run_time=3.0
        )
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        # Update explanation for step 5
        step_explanation_5 = Text("Step 5: Identify the vertex and axis of symmetry.", color=GRAY_C, font_size=24)
        step_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_5))
        self.objects["step_explanation"] = step_explanation_5

        # [missing audio] self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        self.play(FadeIn(vertex_dot), run_time=1.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        # [missing audio] self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_05.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_5 = 2.00  # [audio-sync] actual TTS duration
        # Step 6
        self.play(Circumscribe(vertex_dot, color=RED, run_time=1))
        self.play(Write(vertex_label), run_time=2.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        # [missing audio] self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_06.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_6 = 2.00  # [audio-sync] actual TTS duration
        # Step 7
        self.play(Create(axis_line), run_time=1.5)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        # Update explanation for final step
        step_explanation_final = Text("The graph of y = (x-2)² - 3 is complete.", color=GRAY_C, font_size=24)
        step_explanation_final.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_final))
        self.objects["step_explanation"] = step_explanation_final

        # [missing audio] self.add_sound("media/audio/Create_a_graph_of_th_3a3aa6e94c/step_07.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_7 = 2.00  # [audio-sync] actual TTS duration
        # Step 8
        self.play(Circumscribe(axis_line, color=PURPLE, run_time=1))
        self.play(Write(axis_label), run_time=3.0)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        # Final hold
        self.wait(max(0.1, 2))