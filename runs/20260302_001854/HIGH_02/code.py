'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the transformation from parent parabola y=x^2 to vertex form y=(x-2)^2-3, showing how horizontal and vertical shifts affect the graph and locate the vertex and axis of symmetry.
# 2. Layout Strategy: Use three-zone layout.
#    - Header Region: [y=3.5] for Title and equation display.
#    - Main Content: [Center y=0] for coordinate axes and graphs.
#    - Footer Region: [Bottom y=-3.5] for step explanations.
# 3. Anti-Overlap Check: Keep title and footer text scaled appropriately. Ensure vertex label and axis label do not overlap with graph. Use VGroups for positioning.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_the_parabola_re_6cb658d604/step_XX.mp3"
# 5. Animation Flow: Show axes, parent graph, transform equation and graph horizontally, then vertically, reveal vertex, reveal axis of symmetry.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title_text
        title_text = Text("Graphing a Parabola in Vertex Form", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=8,
            axis_config={"include_numbers": True}
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes

        # parent_graph - Note: Using axes.plot as per hint, not ParametricFunction
        parent_graph = axes.plot(lambda x: x**2, x_range=[-2, 4], color="#666666", stroke_width=3)
        parent_graph.set_stroke(opacity=0.5)
        self.objects["parent_graph"] = parent_graph

        # final_graph
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-1, 5], color=BLUE, stroke_width=5)
        self.objects["final_graph"] = final_graph

        # vertex_dot
        vertex_dot = Dot(radius=0.08, color=RED, fill_opacity=1.0)
        vertex_dot.move_to(axes.c2p(2, -3))
        self.objects["vertex_dot"] = vertex_dot

        # vertex_label
        vertex_label = MathTex(r"(2,\,-3)", color=RED, font_size=30)
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.15)
        self.objects["vertex_label"] = vertex_label

        # axis_line - DashedLine
        axis_line = DashedLine(
            start=axes.c2p(2, -5),
            end=axes.c2p(2, 5),
            color=GREEN,
            stroke_width=4,
            stroke_opacity=0.7,
            dash_length=0.2
        )
        self.objects["axis_line"] = axis_line

        # axis_label
        axis_label = MathTex(r"x=2", color=GREEN, font_size=30)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.2)
        self.objects["axis_label"] = axis_label

        # eq_display
        eq_display = MathTex(r"y = x^2", color=YELLOW, font_size=32)
        eq_display.next_to(title_text, DOWN, buff=0.5)
        self.objects["eq_display"] = eq_display

        # footer_text
        footer_text = Text("We start with the basic parabola, y = x^2.", color=GRAY_C, font_size=24)
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # Create intermediate equation states for transformations
        eq_horizontal = MathTex(r"y = (x-2)^2", color=YELLOW, font_size=32)
        eq_horizontal.move_to(eq_display.get_center())
        self.objects["eq_horizontal"] = eq_horizontal

        eq_final = MathTex(r"y = (x-2)^2 - 3", color=YELLOW, font_size=32)
        eq_final.move_to(eq_display.get_center())
        self.objects["eq_final"] = eq_final

        # Create intermediate graph for horizontal shift
        graph_horizontal = axes.plot(lambda x: (x-2)**2, x_range=[0, 4], color=BLUE, stroke_width=5)
        graph_horizontal.set_stroke(opacity=0.7)
        self.objects["graph_horizontal"] = graph_horizontal

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_the_parabola_re_6cb658d604/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title_text"]), run_time=1.5)
        self.play(Write(self.objects["eq_display"]), run_time=1.5)
        self.play(Create(self.objects["axes"]), run_time=2.0)
        self.play(Write(self.objects["footer_text"]), run_time=1.5)
        remaining_1 = max(0.1, 6.696 - (1.5+1.5+2.0+1.5) + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/Draw_the_parabola_re_6cb658d604/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Update footer text
        new_footer = Text("The most basic parabola is y = x^2. Vertex at origin, symmetric about y-axis.", color=GRAY_C, font_size=24)
        new_footer.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer), run_time=1.0)
        self.objects["footer_text"] = new_footer

        self.play(Create(self.objects["parent_graph"]), run_time=3.0)
        self.play(Indicate(self.objects["parent_graph"], color=WHITE, run_time=1.0))
        remaining_2 = max(0.1, 9.36 - (1.0+3.0+1.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Draw_the_parabola_re_6cb658d604/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Update footer text
        new_footer2 = Text("The term (x-2) inside the square causes a horizontal shift right by 2.", color=GRAY_C, font_size=24)
        new_footer2.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer2), run_time=1.0)
        self.objects["footer_text"] = new_footer2

        self.play(Circumscribe(self.objects["eq_display"], color=YELLOW, run_time=1.0))
        self.play(TransformMatchingTex(self.objects["eq_display"], self.objects["eq_horizontal"]), run_time=2.0)
        self.objects["eq_display"] = self.objects["eq_horizontal"]

        # Transform parent graph to horizontally shifted graph
        self.play(Transform(self.objects["parent_graph"], self.objects["graph_horizontal"]), run_time=3.0)
        remaining_3 = max(0.1, 12.144 - (1.0+1.0+2.0+3.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_the_parabola_re_6cb658d604/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Update footer text
        new_footer3 = Text("The -3 outside shifts the graph vertically down by 3 units.", color=GRAY_C, font_size=24)
        new_footer3.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer3), run_time=1.0)
        self.objects["footer_text"] = new_footer3

        self.play(Circumscribe(self.objects["eq_display"], color=YELLOW, run_time=1.0))
        self.play(TransformMatchingTex(self.objects["eq_display"], self.objects["eq_final"]), run_time=2.0)
        self.objects["eq_display"] = self.objects["eq_final"]

        # Replace horizontally shifted graph with final graph
        self.play(ReplacementTransform(self.objects["parent_graph"], self.objects["final_graph"]), run_time=2.0)
        remaining_4 = max(0.1, 9.072 - (1.0+1.0+2.0+2.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Draw_the_parabola_re_6cb658d604/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Update footer text
        new_footer4 = Text("The vertex is the lowest point at (2, -3), from the equation's structure.", color=GRAY_C, font_size=24)
        new_footer4.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer4), run_time=1.0)
        self.objects["footer_text"] = new_footer4

        self.play(Indicate(self.objects["vertex_dot"], color=RED, run_time=1.0))
        self.play(FadeIn(self.objects["vertex_dot"], scale=0.5), run_time=1.5)
        self.play(Write(self.objects["vertex_label"]), run_time=1.5)
        remaining_5 = max(0.1, 10.104 - (1.0+1.0+1.5+1.5) + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/Draw_the_parabola_re_6cb658d604/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Update footer text
        new_footer5 = Text("The axis of symmetry is the vertical line x=2 through the vertex.", color=GRAY_C, font_size=24)
        new_footer5.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer5), run_time=1.0)
        self.objects["footer_text"] = new_footer5

        self.play(Indicate(self.objects["axis_line"], color=GREEN, run_time=1.0))
        self.play(Create(self.objects["axis_line"]), run_time=2.0)
        self.play(Write(self.objects["axis_label"]), run_time=1.5)
        remaining_6 = max(0.1, 13.104 - (1.0+1.0+2.0+1.5) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))