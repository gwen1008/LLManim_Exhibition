'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the transformation of the parent parabola y=x² into y=(x-2)²-3, showing horizontal and vertical shifts, and identifying the vertex and axis of symmetry.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title/Equation
#    - Main Content: [Center y=0] for coordinate axes and parabolas
#    - Footer Region: [Bottom y=-3.5] for explanatory text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for labels (vertex, axis) to keep them with their graphical elements. Keep equation updates in-place using ReplacementTransform.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/parabola_transform/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes and header equation.
#    - Step 2: Draw parent parabola (green).
#    - Step 3: Shift parabola right, update equation to y=(x-2)².
#    - Step 4: Shift parabola down, update equation to final form.
#    - Step 5: Reveal vertex (red dot) and label.
#    - Step 6: Draw axis of symmetry (dashed line) and label.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_the_parabola_re_c101454754/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        axes_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-4, 3, 1],
            axis_config={'include_numbers': True}
        )
        axes.move_to(axes_anchor)
        axes.set_color(GRAY_C)
        self.objects["axes"] = axes
        
        # Equation header - parent
        eq_header_parent = MathTex(r"y = x^2")
        eq_header_parent.move_to(title_anchor)
        eq_header_parent.set_color(YELLOW)
        self.objects["eq_header_parent"] = eq_header_parent
        
        # Parent graph
        def parent_func(t):
            return axes.c2p(t, t**2)
        graph_parent = ParametricFunction(
            parent_func,
            t_range=[-2, 4],
            color=GREEN
        )
        graph_parent.align_to(axes, ORIGIN)
        self.objects["graph_parent"] = graph_parent
        
        # Target graph (initially invisible)
        def target_func(t):
            return axes.c2p(t, (t-2)**2 - 3)
        graph_target = ParametricFunction(
            target_func,
            t_range=[-1, 5],
            color=BLUE
        )
        graph_target.align_to(axes, ORIGIN)
        graph_target.set_stroke(opacity=0.0)
        self.objects["graph_target"] = graph_target
        
        # Vertex dot
        vertex_dot = Dot(radius=0.08)
        vertex_dot.move_to(axes.c2p(2, -3))
        vertex_dot.set_color(RED)
        vertex_dot.set_opacity(0.0)
        self.objects["vertex_dot"] = vertex_dot
        
        # Vertex label
        vertex_label = MathTex(r"(2,\,-3)")
        vertex_label.next_to(vertex_dot, RIGHT, buff=0.2)
        vertex_label.set_color(RED)
        vertex_label.scale(0.8)
        self.objects["vertex_label"] = vertex_label
        
        # Axis of symmetry line
        axis_line = DashedLine(
            start=3 * UP,
            end=3 * DOWN,
            dash_length=0.1
        )
        axis_line.move_to(axes.c2p(2, 0))
        axis_line.set_color(PINK)
        axis_line.set_opacity(0.0)
        self.objects["axis_line"] = axis_line
        
        # Axis label
        axis_label = MathTex(r"x = 2")
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)
        axis_label.set_color(PINK)
        axis_label.scale(0.8)
        self.objects["axis_label"] = axis_label
        
        # Footer text
        footer_text = Text("Start with the basic parabola, y equals x squared.")
        footer_text.move_to(footer_anchor)
        footer_text.set_color(GRAY_C)
        footer_text.scale(0.7)
        self.objects["footer_text"] = footer_text
        
        # Additional equations needed for transformation steps
        eq_header_shifted = MathTex(r"y = (x-2)^2")
        eq_header_shifted.move_to(title_anchor)
        eq_header_shifted.set_color(YELLOW)
        self.objects["eq_header_shifted"] = eq_header_shifted
        
        eq_header_final = MathTex(r"y = (x-2)^2 - 3")
        eq_header_final.move_to(title_anchor)
        eq_header_final.set_color(YELLOW)
        self.objects["eq_header_final"] = eq_header_final
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/parabola_transform/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["eq_header_parent"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["axes"]), Write(self.objects["eq_header_parent"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/parabola_transform/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["graph_parent"]), run_time=2.5)
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/parabola_transform/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["eq_header_parent"], color=ORANGE, run_time=1))
        # Create a copy of parent graph that will transform
        graph_parent_copy = self.objects["graph_parent"].copy()
        self.add(graph_parent_copy)
        
        # Animate horizontal shift
        shift_animation = graph_parent_copy.animate.align_to(self.objects["graph_target"], ORIGIN)
        self.play(shift_animation, run_time=2.0)
        
        # Update equation
        self.play(ReplacementTransform(
            self.objects["eq_header_parent"],
            self.objects["eq_header_shifted"]
        ), run_time=1.0)
        
        # Replace the transformed copy with the actual target graph (now visible)
        self.remove(graph_parent_copy)
        self.objects["graph_target"].set_stroke(opacity=1.0)
        self.add(self.objects["graph_target"])
        
        remaining_3 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/parabola_transform/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # The graph is already at the horizontally shifted position
        # Update equation to final form
        self.play(ReplacementTransform(
            self.objects["eq_header_shifted"],
            self.objects["eq_header_final"]
        ), run_time=1.5)
        
        remaining_4 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/parabola_transform/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["graph_target"], color=RED, run_time=1))
        self.play(self.objects["vertex_dot"].animate.set_opacity(1.0), run_time=1.0)
        self.play(Write(self.objects["vertex_label"]), run_time=1.0)
        
        remaining_5 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/parabola_transform/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["vertex_dot"], color=PINK, run_time=1))
        self.play(self.objects["axis_line"].animate.set_opacity(1.0), run_time=1.0)
        self.play(Write(self.objects["axis_label"]), run_time=1.0)
        
        remaining_6 = max(0.1, 3.5 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))