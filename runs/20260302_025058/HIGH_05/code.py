'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the triangle method, showing that the resultant vector is the third side of the triangle formed by placing vectors head-to-tail.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for coordinate grid and vectors
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use relative positioning for labels (next_to arrows). Keep vectors in center, explanation at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_animate_the_vecto_fac1b3908d/step_XX.mp3"
# 5. Animation Flow:
#    - Step 0: Fade in grid.
#    - Step 1: Indicate origin, draw vector A, its label, and endpoint.
#    - Step 2: Indicate tip of A, draw vector B, its label, and endpoint.
#    - Step 3: Indicate final point, draw resultant vector C and its label.
#    - Step 4: Circumscribe triangle, fade in translucent triangle.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        grid_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Vector Addition: The Triangle Method", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Grid
        grid = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            axis_config={"stroke_opacity": 0.7},
            background_line_style={"stroke_opacity": 0.3}
        )
        grid.move_to(grid_center).scale(0.8)
        self.objects["grid"] = grid
        
        # Points
        point_O = Dot(radius=0.07, color=WHITE)
        point_O.move_to(grid_center)
        self.objects["point_O"] = point_O
        
        point_P = Dot(radius=0.07, color=YELLOW)
        point_P.move_to(grid_center + np.array([2.4, 0.8, 0]))
        self.objects["point_P"] = point_P
        
        point_Q = Dot(radius=0.07, color=YELLOW)
        point_Q.move_to(grid_center + np.array([3.2, 2.4, 0]))
        self.objects["point_Q"] = point_Q
        
        # Vectors (geometry defined using point centers)
        vec_A = Arrow(
            start=point_O.get_center(),
            end=point_P.get_center(),
            color="#1E90FF",
            buff=0,
            stroke_width=6
        )
        self.objects["vec_A"] = vec_A
        
        vec_B = Arrow(
            start=point_P.get_center(),
            end=point_Q.get_center(),
            color="#32CD32",
            buff=0,
            stroke_width=6
        )
        self.objects["vec_B"] = vec_B
        
        vec_C = Arrow(
            start=point_O.get_center(),
            end=point_Q.get_center(),
            color="#FF8C00",
            buff=0,
            stroke_width=8
        )
        self.objects["vec_C"] = vec_C
        
        # Labels
        label_A = MathTex(r"\vec{A} = (3, 1)", color="#1E90FF", font_size=28)
        label_A.next_to(vec_A.get_center(), UP+LEFT, buff=0.15)
        self.objects["label_A"] = label_A
        
        label_B = MathTex(r"\vec{B} = (1, 2)", color="#32CD32", font_size=28)
        label_B.next_to(vec_B.get_center(), UP+RIGHT, buff=0.15)
        self.objects["label_B"] = label_B
        
        label_C = MathTex(r"\vec{C} = \vec{A}+\vec{B} = (4, 3)", color="#FF8C00", font_size=32)
        label_C.next_to(vec_C.get_center(), DOWN+RIGHT, buff=0.2)
        self.objects["label_C"] = label_C
        
        # Triangle
        triangle = Polygon(
            point_O.get_center(),
            point_P.get_center(),
            point_Q.get_center(),
            color="#FFD700",
            fill_opacity=0.2,
            stroke_opacity=0.0
        )
        self.objects["triangle"] = triangle
        
        # Explanation text
        exp_text = Text("We begin with a coordinate grid.", color=GRAY_C, font_size=26)
        exp_text.move_to(explanation_anchor)
        self.objects["exp_text"] = exp_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 0
        audio_step0 = "media/audio/To_animate_the_vecto_fac1b3908d/step_00.mp3"
        if os.path.exists(audio_step0):
            self.add_sound(audio_step0)
        elif os.path.exists(audio_step0.replace(".mp3", ".wav")):
            self.add_sound(audio_step0.replace(".mp3", ".wav"))
        
        self.play(FadeIn(self.objects["grid"]), run_time=2.0)
        remaining_0 = max(0.1, 7.488 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_0))
        
        # Step 1
        audio_step1 = "media/audio/To_animate_the_vecto_fac1b3908d/step_01.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_O"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vec_A"]), run_time=1.5)
        self.play(Write(self.objects["label_A"]), Write(self.objects["point_P"]), run_time=1.0)
        remaining_1 = max(0.1, 4.296 - (1 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Update explanation text for step 2
        exp_text_step2 = Text("Now, draw vector B from the tip of A.", color=GRAY_C, font_size=26)
        exp_text_step2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["exp_text"], exp_text_step2))
        self.objects["exp_text"] = exp_text_step2
        
        # Step 2
        audio_step2 = "media/audio/To_animate_the_vecto_fac1b3908d/step_02.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_P"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vec_B"]), run_time=2.0)
        self.play(Write(self.objects["label_B"]), Write(self.objects["point_Q"]), run_time=1.0)
        remaining_2 = max(0.1, 10.872 - (1 + 2.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Update explanation text for step 3
        exp_text_step3 = Text("The resultant vector C completes the triangle.", color=GRAY_C, font_size=26)
        exp_text_step3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["exp_text"], exp_text_step3))
        self.objects["exp_text"] = exp_text_step3
        
        # Step 3
        audio_step3 = "media/audio/To_animate_the_vecto_fac1b3908d/step_03.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_Q"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vec_C"]), run_time=2.0)
        self.play(Write(self.objects["label_C"]), run_time=1.0)
        remaining_3 = max(0.1, 9.888 - (1 + 2.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Update explanation text for step 4
        exp_text_step4 = Text("The triangle shows the geometric relationship.", color=GRAY_C, font_size=26)
        exp_text_step4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["exp_text"], exp_text_step4))
        self.objects["exp_text"] = exp_text_step4
        
        # Step 4
        audio_step4 = "media/audio/To_animate_the_vecto_fac1b3908d/step_04.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["triangle"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["triangle"]), run_time=1.5)
        remaining_4 = max(0.1, 9.216 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Final hold
        self.wait(max(0.1, 2))