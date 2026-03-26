'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Graph the parabola y=(x-2)^2-3 by transforming the parent function y=x^2, showing horizontal and vertical shifts, and identifying vertex and axis of symmetry.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for equation labels (parent_label, shifted_h_label, final_label)
#    - Main Content: [Center y=0] for axes and parabola graphs
#    - Footer Region: [Bottom y=-3.5] for step_explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use title_anchor for equation labels, replacing them in place. Keep vertex_label and axis_label close to their graphical elements.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/graph_parabola_transform/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Create parent parabola (dashed gray).
#    - Step 3: Indicate parent label, transform to horizontally shifted parabola (blue).
#    - Step 4: Indicate shifted label, transform to final parabola (blue), add vertex dot.
#    - Step 5: Circumscribe vertex, label vertex, draw axis of symmetry and its label.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_the_parabola_de_2a92751f88/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # axes
        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-5, 3, 1],
            axis_config={"include_numbers": True}
        ).move_to(content_center)
        axes.set_color(GRAY_C)
        self.objects["axes"] = axes
        
        # parent_label
        parent_label = MathTex(r"y = x^2", color=GRAY).move_to(title_anchor)
        self.objects["parent_label"] = parent_label
        
        # parent_curve
        parent_curve = axes.plot(
            lambda x: x**2,
            x_range=[-3, 3],
            color=GRAY
        )
        parent_curve.set_stroke(opacity=0.7, width=3)
        parent_curve = DashedVMobject(parent_curve, num_dashes=20)
        self.objects["parent_curve"] = parent_curve
        
        # shifted_h_label
        shifted_h_label = MathTex(r"y = (x-2)^2", color=BLUE).move_to(title_anchor)
        self.objects["shifted_h_label"] = shifted_h_label
        
        # shifted_h_curve
        shifted_h_curve = axes.plot(
            lambda x: (x-2)**2,
            x_range=[-1, 5],
            color=BLUE
        )
        shifted_h_curve.set_stroke(opacity=0.7, width=4)
        self.objects["shifted_h_curve"] = shifted_h_curve
        
        # final_label
        final_label = MathTex(r"y = (x-2)^2 - 3", color=BLUE).move_to(title_anchor)
        self.objects["final_label"] = final_label
        
        # final_curve
        final_curve = axes.plot(
            lambda x: (x-2)**2 - 3,
            x_range=[-1, 5],
            color=BLUE
        )
        final_curve.set_stroke(opacity=1.0, width=5)
        self.objects["final_curve"] = final_curve
        
        # vertex_dot
        vertex_dot = Dot(axes.c2p(2, -3), radius=0.08, color=RED, fill_opacity=1.0)
        self.objects["vertex_dot"] = vertex_dot
        
        # vertex_label
        vertex_label = MathTex(r"(2,\,-3)", color=RED, font_size=30)
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.15)
        self.objects["vertex_label"] = vertex_label
        
        # axis_line
        axis_line = DashedLine(
            start=axes.c2p(2, axes.y_range[0]),
            end=axes.c2p(2, axes.y_range[1]),
            color=GREEN,
            stroke_opacity=0.8,
            dash_length=0.05
        )
        self.objects["axis_line"] = axis_line
        
        # axis_label
        axis_label = MathTex(r"x = 2", color=GREEN, font_size=28)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1).align_to(axis_line, LEFT)
        self.objects["axis_label"] = axis_label
        
        # step_explanation
        step_explanation = Text("We start with the basic parabola, y = x squared.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/graph_parabola_transform/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["axes"]), run_time=2.5)
        remaining_1 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/graph_parabola_transform/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["parent_curve"]), run_time=3.0)
        remaining_2 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/graph_parabola_transform/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate parent_label
        self.play(Indicate(self.objects["parent_label"], color=YELLOW, run_time=1))
        # Visual actions: ReplacementTransform for curve and label
        self.play(
            ReplacementTransform(self.objects["parent_curve"], self.objects["shifted_h_curve"]),
            ReplacementTransform(self.objects["parent_label"], self.objects["shifted_h_label"]),
            run_time=3.0
        )
        remaining_3 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/graph_parabola_transform/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate shifted_h_label
        self.play(Indicate(self.objects["shifted_h_label"], color=YELLOW, run_time=1))
        # Visual actions: ReplacementTransform for curve and label, Create vertex_dot
        self.play(
            ReplacementTransform(self.objects["shifted_h_curve"], self.objects["final_curve"]),
            ReplacementTransform(self.objects["shifted_h_label"], self.objects["final_label"]),
            Create(self.objects["vertex_dot"]),
            run_time=3.0
        )
        remaining_4 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/graph_parabola_transform/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe vertex_dot
        self.play(Circumscribe(self.objects["vertex_dot"], color=YELLOW, run_time=1))
        # Visual actions: Write vertex_label, Create axis_line, Write axis_label
        self.play(
            Write(self.objects["vertex_label"]),
            Create(self.objects["axis_line"]),
            Write(self.objects["axis_label"]),
            run_time=5.0
        )
        remaining_5 = max(0.1, 6.0 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_5))