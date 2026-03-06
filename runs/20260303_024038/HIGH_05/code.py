'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the head-to-tail method, showing the geometric interpretation of (3,1)+(1,2)=(4,3).
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title "Vector Addition: Head-to-Tail Method"
#    - Main Content: [Center y=0] for coordinate grid and vectors
#    - Footer Region: [Bottom y=-2.8] for step-by-step narration text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each vector with its label. Position labels relative to arrow tips using next_to with small buff.
#    - Keep equation at y=-1.8 (below main vectors) to avoid overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/vector_addition_head_to_tail/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show grid.
#    - Step 2: Draw vector A.
#    - Step 3: Label vector A.
#    - Step 4: Draw vector B from tip of A.
#    - Step 5: Label vector B.
#    - Step 6: Draw resultant vector C from origin to tip of B.
#    - Step 7: Label C and show initial equation.
#    - Step 8: Transform equation to final form, emphasizing result.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_vectors_A____3__90b6737b64/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors
        global_center = ORIGIN
        title_anchor = 3.0 * UP
        explanation_anchor = -2.8 * UP
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Vector Addition: Head-to-Tail Method", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # grid
        grid = NumberPlane(
            x_range=[-2, 7, 1],
            y_range=[-2, 5, 1],
            x_length=12,
            y_length=10,
            stroke_opacity=0.2,
            axis_config={"stroke_opacity": 0.5}
        )
        grid.move_to(global_center)
        self.objects["grid"] = grid
        
        # vec_A
        vec_A = Arrow(start=[0,0,0], end=[3,1,0], color=BLUE, stroke_width=6, buff=0)
        vec_A.move_to(global_center)
        self.objects["vec_A"] = vec_A
        
        # label_A
        label_A = MathTex(r"\vec{A} = (3,1)", color=BLUE, font_size=28)
        label_A.next_to(vec_A.get_end(), UP+RIGHT, buff=0.1)
        self.objects["label_A"] = label_A
        
        # vec_B
        vec_B = Arrow(start=[3,1,0], end=[4,3,0], color=GREEN, stroke_width=6, buff=0)
        vec_B.move_to([3,1,0])
        self.objects["vec_B"] = vec_B
        
        # label_B
        label_B = MathTex(r"\vec{B} = (1,2)", color=GREEN, font_size=28)
        label_B.next_to(vec_B.get_end(), UP+RIGHT, buff=0.1)
        self.objects["label_B"] = label_B
        
        # vec_C
        vec_C = Arrow(start=[0,0,0], end=[4,3,0], color=YELLOW, stroke_width=8, buff=0)
        vec_C.move_to(global_center)
        self.objects["vec_C"] = vec_C
        
        # label_C
        label_C = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4,3)", color=YELLOW, font_size=32)
        label_C.next_to(vec_C.get_end(), DOWN+LEFT, buff=0.2)
        self.objects["label_C"] = label_C
        
        # step_explanation
        step_explanation = Text("Placeholder for step narration.", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # equation_initial
        equation_initial = MathTex(r"\vec{A} + \vec{B} = (3,1) + (1,2)", color=WHITE, font_size=32)
        equation_initial.move_to(global_center + DOWN*1.8)
        self.objects["equation_initial"] = equation_initial
        
        # equation_final
        equation_final = MathTex(r"\vec{A} + \vec{B} = (4,3) = \vec{C}", color=YELLOW, font_size=32)
        equation_final.move_to(global_center + DOWN*1.8)
        self.objects["equation_final"] = equation_final
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/vector_addition_head_to_tail/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # signal_action: Indicate grid
        self.play(Indicate(self.objects["grid"], color=WHITE, run_time=1))
        # visual_action: Create grid
        self.play(Create(self.objects["grid"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/vector_addition_head_to_tail/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # signal_action: null (skip)
        # visual_action: Create vec_A
        self.play(Create(self.objects["vec_A"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/vector_addition_head_to_tail/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # signal_action: Write label_A
        self.play(Write(self.objects["label_A"]), run_time=1.0)
        # visual_action: Write label_A (already done in signal)
        remaining_3 = max(0.1, 2.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/vector_addition_head_to_tail/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # signal_action: Indicate vec_A.get_end()
        tip_A = Dot(self.objects["vec_A"].get_end(), color=BLUE, radius=0.08)
        self.add(tip_A)
        self.play(Indicate(tip_A, color=BLUE, run_time=1))
        self.remove(tip_A)
        # visual_action: Create vec_B
        self.play(Create(self.objects["vec_B"]), run_time=2.0)
        remaining_4 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/vector_addition_head_to_tail/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # signal_action: Write label_B
        self.play(Write(self.objects["label_B"]), run_time=1.0)
        # visual_action: Write label_B (already done in signal)
        remaining_5 = max(0.1, 2.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/vector_addition_head_to_tail/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # signal_action: Indicate global_center
        origin_dot = Dot(global_center, color=YELLOW, radius=0.08)
        self.add(origin_dot)
        self.play(Indicate(origin_dot, color=YELLOW, run_time=1))
        self.remove(origin_dot)
        # visual_action: Create vec_C
        self.play(Create(self.objects["vec_C"]), run_time=2.5)
        remaining_6 = max(0.1, 3.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/vector_addition_head_to_tail/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # signal_action: Circumscribe label_C
        self.play(Circumscribe(self.objects["label_C"], color=YELLOW, run_time=1))
        # visual_action: Write label_C and Create equation_initial
        self.play(Write(self.objects["label_C"]), run_time=1.5)
        self.play(Create(self.objects["equation_initial"]), run_time=1.5)
        remaining_7 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/vector_addition_head_to_tail/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # signal_action: Indicate vec_C
        self.play(Indicate(self.objects["vec_C"], color=YELLOW, run_time=1))
        # visual_action: TransformMatchingTex equation_initial into equation_final
        self.play(TransformMatchingTex(self.objects["equation_initial"], self.objects["equation_final"]), run_time=2.0)
        remaining_8 = max(0.1, 3.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # Final hold
        self.wait(max(0.1, 2))