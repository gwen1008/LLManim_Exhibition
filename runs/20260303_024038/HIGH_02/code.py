'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the transformation of the parent parabola y=x^2 into y=(x-2)^2-3, showing horizontal and vertical shifts to explain vertex form.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "y = (x-2)^2 - 3"
#    - Main Content: [Center y=0] for coordinate axes and parabola graphs
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for parent parabola and its label. Keep vertex and axis labels close to their objects with buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/parabola_transform/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes, signal parent label.
#    - Step 2: Create parent parabola, indicate it.
#    - Step 3: Transform parent parabola horizontally (right shift), signal title.
#    - Step 4: Draw axis of symmetry line.
#    - Step 5: Shift parabola vertically (down), signal title again.
#    - Step 6: Fade in vertex dot.
#    - Step 7: Write vertex and axis labels.
#    - Step 8: Fade in final parabola, circumscribe it.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_the_parabola_re_ed7ec41789/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = MathTex(r"y = (x-2)^2 - 3", color=BLUE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # axes
        axes = Axes(
            x_range=[-3, 7, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(global_center)
        self.objects["axes"] = axes
        
        # parent_label
        parent_label = MathTex(r"y = x^2", color=GRAY, font_size=36)
        parent_label.move_to(axes.c2p(-2, 4))
        self.objects["parent_label"] = parent_label
        
        # parent_parabola
        parent_parabola = axes.plot(
            lambda x: x**2,
            x_range=[-3, 5],
            color=GRAY,
            stroke_width=3
        )
        self.objects["parent_parabola"] = parent_parabola
        
        # target_parabola
        target_parabola = axes.plot(
            lambda x: (x-2)**2 - 3,
            x_range=[-1, 5],
            color=BLUE,
            stroke_width=5
        )
        target_parabola.set_opacity(0.0)
        self.objects["target_parabola"] = target_parabola
        
        # axis_line
        axis_line = DashedLine(
            start=axes.c2p(2, -5),
            end=axes.c2p(2, 5),
            color=YELLOW,
            stroke_width=4
        )
        axis_line.set_opacity(0.0)
        self.objects["axis_line"] = axis_line
        
        # axis_label
        axis_label = MathTex(r"x = 2", color=YELLOW, font_size=36)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)
        axis_label.set_opacity(0.0)
        self.objects["axis_label"] = axis_label
        
        # vertex_dot
        vertex_dot = Dot(axes.c2p(2, -3), color=RED, radius=0.08)
        vertex_dot.set_opacity(0.0)
        self.objects["vertex_dot"] = vertex_dot
        
        # vertex_label
        vertex_label = MathTex(r"(2,\,-3)", color=RED, font_size=36)
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.15)
        vertex_label.set_opacity(0.0)
        self.objects["vertex_label"] = vertex_label
        
        # step_explanation
        step_explanation = Text("We start with the basic parabola y = x^2.", color=WHITE, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/parabola_transform/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["parent_label"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["axes"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/parabola_transform/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["parent_parabola"], color=GRAY, run_time=1))
        self.play(Create(self.objects["parent_parabola"]), Write(self.objects["parent_label"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/parabola_transform/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["title"], color=GREEN, run_time=1))
        # Create horizontally shifted parabola for transformation
        parabola_shifted_right = axes.plot(
            lambda x: (x-2)**2,
            x_range=[-1, 5],
            color=BLUE,
            stroke_width=5
        )
        # Update explanation text
        new_explanation_1 = Text("Horizontal shift: (x-2)² moves graph right 2 units.", color=WHITE, font_size=28)
        new_explanation_1.move_to(explanation_anchor)
        self.play(
            ReplacementTransform(self.objects["parent_parabola"], parabola_shifted_right),
            ReplacementTransform(self.objects["step_explanation"], new_explanation_1)
        )
        self.objects["parent_parabola"] = parabola_shifted_right  # Update reference
        self.objects["step_explanation"] = new_explanation_1
        remaining_3 = max(0.1, 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/parabola_transform/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(
            self.objects["axis_line"].animate.set_opacity(1.0),
            run_time=1.5
        )
        remaining_4 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/parabola_transform/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["title"], color=PINK, run_time=1))
        # Shift the parabola down by 3 units
        parabola_shifted_down = axes.plot(
            lambda x: (x-2)**2 - 3,
            x_range=[-1, 5],
            color=BLUE,
            stroke_width=5
        )
        # Update explanation text
        new_explanation_2 = Text("Vertical shift: -3 moves graph down 3 units.", color=WHITE, font_size=28)
        new_explanation_2.move_to(explanation_anchor)
        self.play(
            ReplacementTransform(self.objects["parent_parabola"], parabola_shifted_down),
            ReplacementTransform(self.objects["step_explanation"], new_explanation_2)
        )
        self.objects["parent_parabola"] = parabola_shifted_down  # Update reference
        self.objects["step_explanation"] = new_explanation_2
        remaining_5 = max(0.1, 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/parabola_transform/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(
            self.objects["vertex_dot"].animate.set_opacity(1.0),
            run_time=1.0
        )
        remaining_6 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/parabola_transform/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(
            self.objects["axis_label"].animate.set_opacity(1.0),
            self.objects["vertex_label"].animate.set_opacity(1.0),
            run_time=1.5
        )
        remaining_7 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/parabola_transform/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["target_parabola"], color=BLUE, run_time=1))
        # Update explanation text
        new_explanation_3 = Text("Final parabola: y = (x-2)² - 3 with vertex (2,-3) and axis x=2.", color=WHITE, font_size=28)
        new_explanation_3.move_to(explanation_anchor)
        self.play(
            self.objects["target_parabola"].animate.set_opacity(1.0),
            ReplacementTransform(self.objects["step_explanation"], new_explanation_3),
            run_time=1.5
        )
        self.objects["step_explanation"] = new_explanation_3
        remaining_8 = max(0.1, 4.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))