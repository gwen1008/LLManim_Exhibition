'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Graph the parabola y = (x-2)^2 - 3 by transforming the parent function y = x^2 step-by-step, showing horizontal and vertical shifts, and identifying the vertex and axis of symmetry.
# 2. Layout Strategy: Use three zones.
#    - Header Region: [y=3.5] for Title and equation display.
#    - Main Content: [Center y=0] for axes and parabola graph.
#    - Footer Region: [Bottom y=-3.5] for step explanation text.
# 3. Anti-Overlap Check: Use VGroup for title and equation to keep them together. Position axes at center. Keep explanation text at bottom. Ensure vertex label and axis label do not overlap with graph.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/graphing_parabola/step_XX.mp3"
# 5. Animation Flow: Show axes -> parent parabola -> horizontal shift -> vertical shift -> highlight vertex and axis.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": True}
        )
        axes.move_to(graph_anchor)
        axes.set_color(GRAY_C)
        self.objects["axes"] = axes
        
        # title_text
        title_text = Text("Graphing a Parabola", font_size=36)
        title_text.move_to(title_anchor + UP*0.5)
        title_text.set_color(WHITE)
        self.objects["title_text"] = title_text
        
        # eq_display_parent
        eq_display_parent = MathTex(r"y = x^2")
        eq_display_parent.next_to(title_text, DOWN, buff=0.5)
        eq_display_parent.set_color(BLUE)
        self.objects["eq_display_parent"] = eq_display_parent
        
        # parent_parabola
        parent_parabola = axes.plot(lambda x: x**2, color=BLUE, stroke_width=3)
        parent_parabola.move_to(graph_anchor)
        self.objects["parent_parabola"] = parent_parabola
        
        # eq_display_hshifted
        eq_display_hshifted = MathTex(r"y = (x-2)^2")
        eq_display_hshifted.next_to(title_text, DOWN, buff=0.5)
        eq_display_hshifted.set_color(GREEN)
        self.objects["eq_display_hshifted"] = eq_display_hshifted
        
        # hshifted_parabola
        hshifted_parabola = axes.plot(lambda x: (x-2)**2, color=GREEN, stroke_width=3)
        hshifted_parabola.move_to(graph_anchor)
        self.objects["hshifted_parabola"] = hshifted_parabola
        
        # eq_display_final
        eq_display_final = MathTex(r"y = (x-2)^2 - 3")
        eq_display_final.next_to(title_text, DOWN, buff=0.5)
        eq_display_final.set_color(YELLOW)
        self.objects["eq_display_final"] = eq_display_final
        
        # final_parabola
        final_parabola = axes.plot(lambda x: (x-2)**2 - 3, color=YELLOW, stroke_width=4)
        final_parabola.move_to(graph_anchor)
        self.objects["final_parabola"] = final_parabola
        
        # vertex_dot
        vertex_dot = Dot(radius=0.08, color=RED, fill_opacity=1.0)
        vertex_dot.move_to(axes.c2p(2, -3))
        self.objects["vertex_dot"] = vertex_dot
        
        # vertex_label
        vertex_label = MathTex(r"(2,\,-3)", font_size=24)
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.1)
        vertex_label.set_color(RED)
        self.objects["vertex_label"] = vertex_label
        
        # axis_line
        axis_line = Line(UP*5, DOWN*5, color=PURPLE, stroke_width=2, stroke_opacity=0.7)
        axis_line.move_to(axes.c2p(2, 0))
        self.objects["axis_line"] = axis_line
        
        # axis_label
        axis_label = MathTex(r"x = 2", font_size=24)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)
        axis_label.set_color(PURPLE)
        self.objects["axis_label"] = axis_label
        
        # step_explanation
        step_explanation = Text("Start with the parent function.", font_size=24)
        step_explanation.move_to(explanation_anchor)
        step_explanation.set_color(GRAY_C)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/graphing_parabola/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2
        audio_step2 = "media/audio/graphing_parabola/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["eq_display_parent"], color=BLUE, run_time=1))
        self.play(Create(self.objects["parent_parabola"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3
        audio_step3 = "media/audio/graphing_parabola/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["eq_display_hshifted"], color=GREEN, run_time=1))
        self.play(
            ReplacementTransform(self.objects["eq_display_parent"], self.objects["eq_display_hshifted"]),
            ReplacementTransform(self.objects["parent_parabola"], self.objects["hshifted_parabola"]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4
        audio_step4 = "media/audio/graphing_parabola/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["eq_display_final"], color=YELLOW, run_time=1))
        self.play(
            ReplacementTransform(self.objects["eq_display_hshifted"], self.objects["eq_display_final"]),
            ReplacementTransform(self.objects["hshifted_parabola"], self.objects["final_parabola"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5
        audio_step5 = "media/audio/graphing_parabola/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["vertex_dot"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["vertex_dot"]),
            Create(self.objects["vertex_label"]),
            Create(self.objects["axis_line"]),
            Create(self.objects["axis_label"]),
            run_time=3.0
        )
        remaining_5 = max(0.1, 5.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))