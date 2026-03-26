'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing transformations of quadratic functions from y=x² to y=(x-2)²-3, showing how parameters h and k shift the graph horizontally and vertically, and highlighting the vertex and axis of symmetry.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for equations and graph
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine zones to keep title, equations, graph, and explanations in separate vertical regions.
#    - Graph will be centered at origin, equations above it, title at top, explanations at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes and title.
#    - Step 2: Draw parent graph y=x².
#    - Step 3: Show vertex and axis of symmetry.
#    - Step 4: Transform equation and graph to y=(x-2)² (shift right).
#    - Step 5: Move vertex and axis to x=2.
#    - Step 6: Transform to y=(x-2)²-3 (shift down).
#    - Step 7: Show final vertex at (2,-3).
#    - Step 8: Highlight axis of symmetry with label.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Create Layout Engine
        from utils.layout_engine import LayoutEngine, LayoutObject
        layout = LayoutEngine()

        # Define anchors (zones)
        title_anchor = 3.5 * UP
        eq_anchor = 2.5 * UP
        graph_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Graphing Parabolas: Transformations", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_constraint(layout.get("title").center_x == 0)

        # Axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": True},
            color=GRAY_B
        )
        axes.move_to(graph_center)
        self.objects["axes"] = axes
        layout.add(LayoutObject(axes, "axes"))
        layout.add_to_zone(layout.get("axes"), "CONTENT")
        layout.add_constraint(layout.get("axes").center_x == 0)
        layout.add_constraint(layout.get("axes").center_y == 0)

        # Parent equation
        parent_eq = MathTex("y = x^2", color=BLUE)
        parent_eq.move_to(eq_anchor)
        self.objects["parent_eq"] = parent_eq
        layout.add(LayoutObject(parent_eq, "parent_eq"))
        layout.add_to_zone(layout.get("parent_eq"), "CONTENT")
        layout.add_constraint(layout.get("parent_eq").center_x == 0)

        # Parent graph (y=x²)
        parent_graph = axes.plot(lambda x: x**2, x_range=[-3, 3, 0.1], color=BLUE, stroke_width=3)
        self.objects["parent_graph"] = parent_graph

        # Parent vertex dot
        parent_vertex = Dot(axes.c2p(0, 0), color=BLUE, radius=0.08, fill_opacity=1)
        self.objects["parent_vertex"] = parent_vertex

        # Parent vertex label
        parent_vertex_label = MathTex("(0,0)", color=BLUE, font_size=24)
        parent_vertex_label.next_to(parent_vertex, UP, buff=0.1)
        self.objects["parent_vertex_label"] = parent_vertex_label

        # Parent axis of symmetry (x=0)
        parent_axis = Line(axes.c2p(0, 4), axes.c2p(0, -4), color=BLUE, stroke_width=2, stroke_opacity=0.5)
        self.objects["parent_axis"] = parent_axis

        # Step explanation label
        step_label = Text("Step 1: Start with parent function y=x²", color=YELLOW, font_size=24)
        step_label.move_to(explanation_anchor)
        self.objects["step_label"] = step_label
        layout.add(LayoutObject(step_label, "step_label"))
        layout.add_to_zone(layout.get("step_label"), "FOOTER")
        layout.add_constraint(layout.get("step_label").center_x == 0)

        # Additional objects that will be created later
        # Shifted graph (y=(x-2)²)
        shifted_graph = axes.plot(lambda x: (x-2)**2, x_range=[-1, 5, 0.1], color=GREEN, stroke_width=3)
        self.objects["shifted_graph"] = shifted_graph

        # Final graph (y=(x-2)²-3)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-1, 5, 0.1], color=RED, stroke_width=3)
        self.objects["final_graph"] = final_graph

        # Final vertex dot
        final_vertex = Dot(axes.c2p(2, -3), color=RED, radius=0.08, fill_opacity=1)
        self.objects["final_vertex"] = final_vertex

        # Final vertex label
        final_vertex_label = MathTex("(2,-3)", color=RED, font_size=24)
        final_vertex_label.next_to(final_vertex, UP, buff=0.1)
        self.objects["final_vertex_label"] = final_vertex_label

        # Final axis of symmetry (x=2) - same line as shifted axis but will be transformed
        final_axis = Line(axes.c2p(2, 4), axes.c2p(2, -4), color=RED, stroke_width=2, stroke_opacity=0.5)
        self.objects["final_axis"] = final_axis

        # Final axis label
        final_axis_label = MathTex("x = 2", color=RED, font_size=24)
        final_axis_label.next_to(final_axis.get_top(), RIGHT, buff=0.2)
        self.objects["final_axis_label"] = final_axis_label

        # Solve layout constraints
        layout.solve()

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = 1
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["axes"]))
        self.play(Circumscribe(self.objects["parent_eq"], color=YELLOW, run_time=1))
        self.wait(max(0.1, max(0.1, 5.328 - 3)))  # duration 5.328, animation ~3

        # Step 2
        step = 2
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        self.play(Create(self.objects["parent_graph"]))
        self.play(Indicate(self.objects["parent_vertex"], color=BLUE))
        self.wait(max(0.1, max(0.1, 4.872 - 2)))

        # Step 3
        step = 3
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        self.play(Create(self.objects["parent_vertex"]))
        self.play(Write(self.objects["parent_vertex_label"]))
        self.play(Create(self.objects["parent_axis"]))
        self.wait(max(0.1, max(0.1, 5.712 - 3)))

        # Step 4
        step = 4
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        # Update step label
        new_step_label = Text("Step 2: Horizontal shift right 2 units", color=YELLOW, font_size=24)
        new_step_label.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label

        # Transform equation
        new_eq = MathTex("y = (x-2)^2", color=GREEN)
        new_eq.move_to(self.objects["parent_eq"].get_center())
        self.play(TransformMatchingTex(self.objects["parent_eq"], new_eq))
        self.objects["parent_eq"] = new_eq

        # Transform graph
        self.play(Transform(self.objects["parent_graph"], self.objects["shifted_graph"]))
        self.wait(max(0.1, max(0.1, 8.448 - 4)))

        # Step 5
        step = 5
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        # Update step label
        new_step_label = Text("Step 3: Vertex moves to (2,0)", color=YELLOW, font_size=24)
        new_step_label.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label

        # Transform axis
        self.play(Transform(self.objects["parent_axis"], self.objects["final_axis"]))

        # Move vertex and update label
        self.play(self.objects["parent_vertex"].animate.move_to(axes.c2p(2, 0)))
        new_vertex_label = MathTex("(2,0)", color=GREEN, font_size=24)
        new_vertex_label.next_to(axes.c2p(2, 0), UP, buff=0.1)
        self.play(Transform(self.objects["parent_vertex_label"], new_vertex_label))
        self.objects["parent_vertex_label"] = new_vertex_label
        self.wait(max(0.1, max(0.1, 6.312 - 4)))

        # Step 6
        step = 6
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        # Update step label
        new_step_label = Text("Step 4: Vertical shift down 3 units", color=YELLOW, font_size=24)
        new_step_label.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label

        # Transform equation
        final_eq = MathTex("y = (x-2)^2 - 3", color=RED)
        final_eq.move_to(self.objects["parent_eq"].get_center())
        self.play(TransformMatchingTex(self.objects["parent_eq"], final_eq))
        self.objects["parent_eq"] = final_eq

        # Transform graph
        self.play(Transform(self.objects["parent_graph"], self.objects["final_graph"]))
        self.wait(max(0.1, max(0.1, 6.408 - 3)))

        # Step 7
        step = 7
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        # Update step label
        new_step_label = Text("Step 5: Final vertex at (2,-3)", color=YELLOW, font_size=24)
        new_step_label.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label

        # Create final vertex
        self.play(Create(self.objects["final_vertex"]))
        self.play(Write(self.objects["final_vertex_label"]))
        self.play(Indicate(self.objects["final_vertex"], color=YELLOW))
        self.wait(max(0.1, max(0.1, 7.92 - 4)))

        # Step 8
        step = 8
        audio_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/畫出_y____x_2__2___3_的_95119814cf/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)

        # Update step label
        new_step_label = Text("Step 6: Axis of symmetry at x=2", color=YELLOW, font_size=24)
        new_step_label.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label

        # Highlight axis
        self.play(self.objects["final_axis"].animate.set_stroke(width=4))
        self.play(Write(self.objects["final_axis_label"]))
        self.wait(max(0.1, max(0.1, 6.048 - 3)))

        # Final pause
        self.wait(max(0.1, 2))