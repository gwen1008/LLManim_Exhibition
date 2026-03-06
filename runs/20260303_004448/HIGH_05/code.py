'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate the head-to-tail (triangle) method of vector addition, connecting geometric construction to algebraic component-wise addition.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for coordinate grid and vectors
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for vector arrows and their labels. Position labels relative to arrow tips. Keep component equation above grid (y=1.5) and explanation at bottom (y=-3.0).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/vector_addition_triangle_method/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create coordinate grid.
#    - Step 2: Grow vector A and label.
#    - Step 3: Indicate tip of A, grow vector B and label.
#    - Step 4: Circumscribe triangle, fill triangle, grow resultant vector C and label.
#    - Step 5: Indicate component sum, write equation, morph to final result.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan
        # Title
        title = Text("Vector Addition: The Triangle (Head-to-Tail) Method", color=WHITE, font_size=36)
        title.move_to(3.5 * UP)
        self.objects["title"] = title
        
        # Grid
        grid = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            stroke_opacity=0.5,
            axis_config={"stroke_opacity": 0.7}
        )
        grid.move_to(ORIGIN)
        self.objects["grid"] = grid
        
        # Vector A Arrow
        vec_A_arrow = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color="#1f77b4",
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15,
            buff=0
        )
        self.objects["vec_A_arrow"] = vec_A_arrow
        
        # Vector A Label
        vec_A_label = MathTex(r"\vec{A} = (3, 1)", color="#1f77b4", font_size=30)
        vec_A_label.next_to(vec_A_arrow.get_end(), UP+RIGHT, buff=0.15)
        self.objects["vec_A_label"] = vec_A_label
        
        # Vector B Arrow
        vec_B_arrow = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color="#2ca02c",
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15,
            buff=0
        )
        self.objects["vec_B_arrow"] = vec_B_arrow
        
        # Vector B Label
        vec_B_label = MathTex(r"\vec{B} = (1, 2)", color="#2ca02c", font_size=30)
        vec_B_label.next_to(vec_B_arrow.get_end(), UP+RIGHT, buff=0.15)
        self.objects["vec_B_label"] = vec_B_label
        
        # Vector C Arrow
        vec_C_arrow = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color="#d62728",
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15,
            buff=0
        )
        self.objects["vec_C_arrow"] = vec_C_arrow
        
        # Vector C Label
        vec_C_label = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color="#d62728", font_size=32)
        vec_C_label.next_to(vec_C_arrow.get_end(), LEFT+UP, buff=0.3)
        self.objects["vec_C_label"] = vec_C_label
        
        # Triangle Fill
        triangle_fill = Polygon(
            [0, 0, 0],
            [3, 1, 0],
            [4, 3, 0],
            color="#9467bd",
            fill_opacity=0.2,
            stroke_width=0
        )
        self.objects["triangle_fill"] = triangle_fill
        
        # Component Sum Equation (initial state)
        component_sum = MathTex(r"(3, 1) + (1, 2) = (3+1,\ 1+2)", font_size=36)
        component_sum.move_to(UP * 1.5)
        self.objects["component_sum"] = component_sum
        
        # Step Explanation (initial state)
        step_explanation = Text(
            "Step 1: Draw the coordinate axes and vector A from the origin.",
            color=GRAY_C,
            font_size=24
        )
        step_explanation.move_to(3.0 * DOWN)
        self.objects["step_explanation"] = step_explanation
        
        # Create the transformed versions of step_explanation for later steps
        step2_text = Text(
            "Step 2: Draw vector A from the origin.",
            color=GRAY_C,
            font_size=24
        )
        step2_text.move_to(3.0 * DOWN)
        self.objects["step2_text"] = step2_text
        
        step3_text = Text(
            "Step 3: Place vector B tail-to-head with A.",
            color=GRAY_C,
            font_size=24
        )
        step3_text.move_to(3.0 * DOWN)
        self.objects["step3_text"] = step3_text
        
        step4_text = Text(
            "Step 4: The resultant C closes the triangle from start to finish.",
            color=GRAY_C,
            font_size=24
        )
        step4_text.move_to(3.0 * DOWN)
        self.objects["step4_text"] = step4_text
        
        step5_text = Text(
            "Step 5: Component-wise addition gives the resultant: (3+1, 1+2) = (4, 3).",
            color=GRAY_C,
            font_size=24
        )
        step5_text.move_to(3.0 * DOWN)
        self.objects["step5_text"] = step5_text
        
        # Create the final component sum equation for transformation
        component_sum_final = MathTex(r"(3, 1) + (1, 2) = (4, 3)", font_size=36)
        component_sum_final.move_to(UP * 1.5)
        self.objects["component_sum_final"] = component_sum_final
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/vector_addition_triangle_method/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["grid"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/vector_addition_triangle_method/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(
            GrowArrow(self.objects["vec_A_arrow"]),
            Write(self.objects["vec_A_label"]),
            ReplacementTransform(self.objects["step_explanation"], self.objects["step2_text"]),
            run_time=2.5
        )
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/vector_addition_triangle_method/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate tip of vector A
        dot_at_tip = Dot(self.objects["vec_A_arrow"].get_end(), color=YELLOW, radius=0.1)
        self.add(dot_at_tip)
        self.play(
            Indicate(dot_at_tip, color=YELLOW, run_time=1.0)
        )
        
        self.play(
            GrowArrow(self.objects["vec_B_arrow"]),
            Write(self.objects["vec_B_label"]),
            ReplacementTransform(self.objects["step2_text"], self.objects["step3_text"]),
            run_time=3.0
        )
        remaining_3 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/vector_addition_triangle_method/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe triangle
        self.play(
            Circumscribe(self.objects["triangle_fill"], color=PURPLE, run_time=1.0)
        )
        
        self.play(
            Create(self.objects["triangle_fill"]),
            GrowArrow(self.objects["vec_C_arrow"]),
            Write(self.objects["vec_C_label"]),
            ReplacementTransform(self.objects["step3_text"], self.objects["step4_text"]),
            run_time=4.0
        )
        remaining_4 = max(0.1, 5.0 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/vector_addition_triangle_method/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate component sum
        self.play(
            Indicate(self.objects["component_sum"], color=YELLOW, run_time=1.0)
        )
        
        self.play(
            Write(self.objects["component_sum"]),
            ReplacementTransform(self.objects["step4_text"], self.objects["step5_text"]),
            run_time=2.0
        )
        self.play(
            TransformMatchingTex(
                self.objects["component_sum"],
                self.objects["component_sum_final"],
                path_arc=90 * DEGREES
            ),
            run_time=3.0
        )
        remaining_5 = max(0.1, 6.0 - 5.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final pause
        self.wait(max(0.1, 2.0))