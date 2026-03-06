'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing how the parabola y=(x-2)²-3 is derived from the parent function y=x² through horizontal and vertical shifts, and identifying its vertex and axis of symmetry.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for equations and graph
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use distinct zones for title (top), equation (high-center), graph (center), and explanation (bottom).
#    - Keep vertex label close to vertex dot with small buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Step 1: Show axes and parent equation.
#    - Step 2: Draw parent parabola.
#    - Step 3: Shift parabola right (horizontal transformation).
#    - Step 4: Shift parabola down and transform equation.
#    - Step 5: Show vertex and axis of symmetry.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        equation_anchor = 2.5 * UP
        graph_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Graphing a Parabola: Transformations", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True},
            color=GRAY_B
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes
        
        # Parent equation
        parent_eq = MathTex("y = x^2", color=BLUE)
        parent_eq.move_to(equation_anchor)
        self.objects["parent_eq"] = parent_eq
        
        # Parent parabola (y=x²)
        parent_parabola = axes.plot(lambda x: x**2, x_range=[-2, 2], color=BLUE)
        self.objects["parent_parabola"] = parent_parabola
        
        # Target equation (initially invisible)
        target_eq = MathTex("y = (x-2)^2 - 3", color=GREEN)
        target_eq.move_to(equation_anchor)
        target_eq.set_opacity(0)
        self.objects["target_eq"] = target_eq
        
        # Target parabola (initially invisible)
        target_parabola = axes.plot(lambda x: (x-2)**2 - 3, x_range=[0, 4], color=GREEN)
        target_parabola.set_opacity(0)
        self.objects["target_parabola"] = target_parabola
        
        # Vertex dot
        vertex_dot = Dot(axes.c2p(2, -3), color=RED, radius=0.08)
        self.objects["vertex_dot"] = vertex_dot
        
        # Vertex label
        vertex_label = MathTex("V(2,-3)", color=RED, font_size=28)
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.1)
        self.objects["vertex_label"] = vertex_label
        
        # Axis of symmetry line
        axis_line = DashedLine(
            axes.c2p(2, -4),
            axes.c2p(2, 4),
            color=YELLOW,
            stroke_opacity=0.7,
            dash_length=0.2
        )
        self.objects["axis_line"] = axis_line
        
        # Step explanation
        step_explanation = Text("We start with the parent parabola y = x².", 
                               font_size=24, color=GRAY_B)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_file = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Write(self.objects["axes"], lag_ratio=0.01, run_time=1))
        self.play(Write(self.objects["parent_eq"]))
        self.play(Circumscribe(self.objects["parent_eq"], color=YELLOW, run_time=1))
        
        animation_time = 1 + 1 + 1  # Write axes + Write eq + Circumscribe
        remaining = 9.096 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        audio_file = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Create(self.objects["parent_parabola"], run_time=2))
        
        # Update explanation
        new_explanation = Text("The parent parabola y = x² is centered at the origin.", 
                              font_size=24, color=GRAY_B)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        animation_time = 2 + 1  # Create parabola + Transform text
        remaining = 5.832 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        audio_file = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(self.objects["parent_parabola"], color=BLUE))
        
        # Create intermediate parabola (shifted right only)
        intermediate_parabola = axes.plot(lambda x: (x-2)**2, x_range=[0, 4], color=BLUE)
        
        # Update explanation
        new_explanation = Text("Horizontal shift: (x-2)² moves the graph 2 units right.", 
                              font_size=24, color=GRAY_B)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        self.play(Transform(self.objects["parent_parabola"], intermediate_parabola, run_time=2))
        
        animation_time = 1 + 1 + 2  # Indicate + Transform text + Transform parabola
        remaining = 7.416 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        audio_file = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(self.objects["parent_parabola"], color=BLUE))
        
        # Update explanation
        new_explanation = Text("Vertical shift: -3 moves the graph 3 units down.", 
                              font_size=24, color=GRAY_B)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Transform parabola to final position and color
        self.play(
            Transform(self.objects["parent_parabola"], self.objects["target_parabola"]),
            TransformMatchingTex(self.objects["parent_eq"], self.objects["target_eq"]),
            run_time=2
        )
        
        # Make target parabola visible and parent_eq invisible
        self.objects["target_parabola"].set_opacity(1)
        self.objects["parent_eq"].set_opacity(0)
        
        animation_time = 1 + 1 + 2  # Indicate + Transform text + Transform parabola & equation
        remaining = 6.648 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        audio_file = "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(self.objects["vertex_dot"], color=RED))
        
        # Update explanation
        new_explanation = Text("Vertex at (2,-3) and axis of symmetry at x=2.", 
                              font_size=24, color=GRAY_B)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Create vertex dot, label, and axis line
        self.play(
            FadeIn(self.objects["vertex_dot"], scale=0.5),
            Write(self.objects["vertex_label"]),
            Create(self.objects["axis_line"]),
            run_time=2
        )
        
        animation_time = 1 + 1 + 2  # Indicate + Transform text + Create objects
        remaining = 10.656 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final pause
        self.wait(max(0.1, 2))