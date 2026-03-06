'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition via the head-to-tail (triangle) method using a concrete journey metaphor.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and vector definitions.
#    - Main Content: [Center y=0] for coordinate plane and vectors.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Use VGroups for composite objects (e.g., vector + label + dot).
#    - Position labels relative to their vectors using next_to with buff.
#    - Keep explanation text at bottom, updating via ReplacementTransform to prevent overflow.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/vector_addition_head_to_tail/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show title and vector definitions.
#    - Step 2: Show coordinate axes.
#    - Step 3: Draw vector A, its label, and point P.
#    - Step 4: Draw vector B from P, its label, and point Q.
#    - Step 5: Draw resultant vector C and its label.
#    - Step 6: Final hold, highlight numerical result.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_vectors_A____3__ede6b36e97/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Vector Addition: The Head-to-Tail (Triangle) Method", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Vector definitions
        vec_defs = MathTex(r"\vec{A} = (3,1),\quad \vec{B} = (1,2),\quad \vec{C} = \vec{A}+\vec{B} = (4,3)", color=YELLOW, font_size=28)
        vec_defs.next_to(title, DOWN, buff=0.3)
        self.objects["vec_defs"] = vec_defs
        
        # Axes (NumberPlane)
        axes = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=7,
            stroke_opacity=0.7
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes
        
        # Origin label
        origin_label = MathTex("O", color=WHITE, font_size=24)
        origin_label.move_to(content_center + LEFT*0.2 + DOWN*0.2)
        self.objects["origin_label"] = origin_label
        
        # Points P and Q (Dots) - positions relative to content_center
        point_P = Dot(point=content_center + RIGHT*3 + UP*1, color=BLUE, radius=0.06)
        self.objects["point_P"] = point_P
        
        point_Q = Dot(point=content_center + RIGHT*4 + UP*3, color=GREEN, radius=0.06)
        self.objects["point_Q"] = point_Q
        
        # Vector A (Arrow from O to P)
        vector_A = Arrow(
            start=content_center,
            end=content_center + RIGHT*3 + UP*1,
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["vector_A"] = vector_A
        
        # Label for vector A
        label_A = MathTex(r"\vec{A}", color=BLUE, font_size=28)
        label_A.move_to(content_center + RIGHT*1.5 + UP*0.5 + LEFT*0.2)
        self.objects["label_A"] = label_A
        
        # Vector B (Arrow from P to Q)
        vector_B = Arrow(
            start=content_center + RIGHT*3 + UP*1,
            end=content_center + RIGHT*4 + UP*3,
            color=GREEN,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["vector_B"] = vector_B
        
        # Label for vector B
        label_B = MathTex(r"\vec{B}", color=GREEN, font_size=28)
        label_B.move_to(content_center + RIGHT*3.5 + UP*2.0 + RIGHT*0.2)
        self.objects["label_B"] = label_B
        
        # Vector C (Resultant Arrow from O to Q)
        vector_C = Arrow(
            start=content_center,
            end=content_center + RIGHT*4 + UP*3,
            color=RED,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["vector_C"] = vector_C
        
        # Label for vector C
        label_C = MathTex(r"\vec{C} = \vec{A}+\vec{B}", color=RED, font_size=28)
        label_C.move_to(content_center + RIGHT*2.0 + UP*1.5 + DOWN*0.3)
        self.objects["label_C"] = label_C
        
        # Step explanation text (initial content)
        step_explanation = Text("Step 1: We begin at the origin O.", color=GRAY_C, font_size=26)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/vector_addition_head_to_tail/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe vec_defs
        self.play(Circumscribe(self.objects["vec_defs"], color=YELLOW, run_time=1))
        # Visual action: Create title
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/vector_addition_head_to_tail/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Indicate origin_label
        self.play(Indicate(self.objects["origin_label"], color=WHITE, run_time=1))
        # Visual action: Create axes
        self.play(Create(self.objects["axes"]), run_time=2.0)
        # Also write the origin label and vector definitions
        self.play(Write(self.objects["origin_label"]), Write(self.objects["vec_defs"]), run_time=1.0)
        # Update step explanation (create initial text)
        self.play(Write(self.objects["step_explanation"]), run_time=1.0)
        remaining_2 = max(0.1, 3.0 - (2.0 + 1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/vector_addition_head_to_tail/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate vector_A
        self.play(Indicate(self.objects["vector_A"], color=BLUE, run_time=1))
        # Visual action: Create vector_A, then its label and point_P
        self.play(Create(self.objects["vector_A"]), run_time=2.0)
        self.play(Write(self.objects["label_A"]), Create(self.objects["point_P"]), run_time=1.0)
        # Update step explanation
        step_explanation_3 = Text("Step 2: Draw vector A from O to point P.", color=GRAY_C, font_size=26)
        step_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_3), run_time=0.5)
        self.objects["step_explanation"] = step_explanation_3
        remaining_3 = max(0.1, 4.0 - (1.0 + 2.0 + 1.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/vector_addition_head_to_tail/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate point_P
        self.play(Indicate(self.objects["point_P"], color=BLUE, run_time=1))
        # Visual action: Create vector_B, then its label and point_Q
        self.play(Create(self.objects["vector_B"]), run_time=2.0)
        self.play(Write(self.objects["label_B"]), Create(self.objects["point_Q"]), run_time=1.0)
        # Update step explanation
        step_explanation_4 = Text("Step 3: Place vector B's tail at P and draw it to Q.", color=GRAY_C, font_size=26)
        step_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_4), run_time=0.5)
        self.objects["step_explanation"] = step_explanation_4
        remaining_4 = max(0.1, 4.0 - (1.0 + 2.0 + 1.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/vector_addition_head_to_tail/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate vector_C
        self.play(Indicate(self.objects["vector_C"], color=RED, run_time=1))
        # Visual action: Create vector_C and its label
        self.play(Create(self.objects["vector_C"]), run_time=2.0)
        self.play(Write(self.objects["label_C"]), run_time=1.0)
        # Update step explanation
        step_explanation_5 = Text("Step 4: The resultant vector C completes the triangle.", color=GRAY_C, font_size=26)
        step_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_5), run_time=0.5)
        self.objects["step_explanation"] = step_explanation_5
        remaining_5 = max(0.1, 4.0 - (1.0 + 2.0 + 1.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/vector_addition_head_to_tail/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe vec_defs
        self.play(Circumscribe(self.objects["vec_defs"], color=YELLOW, run_time=1))
        # Visual action: Wait (hold final frame)
        # Update step explanation
        step_explanation_6 = Text("Step 5: C = A + B. The components add: (4,3) = (3,1)+(1,2).", color=GRAY_C, font_size=26)
        step_explanation_6.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_6), run_time=0.5)
        self.objects["step_explanation"] = step_explanation_6
        remaining_6 = max(0.1, 4.0 - (1.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Final hold
        self.wait(max(0.1, 2))