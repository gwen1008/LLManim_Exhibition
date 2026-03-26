'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the head-to-tail method on a coordinate plane.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for coordinate plane and vectors
#    - Footer Region: [Bottom y=-3.5] for step narration
# 3. Anti-Overlap Check:
#    - Strategy: Use relative positioning (next_to, move_to) based on anchors and object centers.
#    - Vectors and labels are placed near their respective points.
#    - The equation is placed below the main content (DOWN*2).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_animate_the_vecto_9f10bfcfb8/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Create vector A, its label, and endpoint dot (with Indicate signal).
#    - Step 3: Create vector B, its label, and endpoint dot (with Circumscribe signal).
#    - Step 4: Create dashed resultant line.
#    - Step 5: Create resultant vector C and its label (with Indicate signal).
#    - Step 6: Write the final vector equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Vector Addition: Head-to-Tail Method", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Axes (NumberPlane)
        axes = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            axis_config={"stroke_opacity": 0.7},
            background_line_style={"stroke_opacity": 0.3},
            color=GRAY,
            stroke_width=2
        )
        axes.move_to(content_center).scale(0.8)
        self.objects["axes"] = axes

        # Vector A and its components
        vec_A = Arrow(start=[0,0,0], end=[3,1,0], color=BLUE, stroke_width=6, buff=0)
        vec_A.move_to(content_center)
        self.objects["vec_A"] = vec_A

        label_A = MathTex(r"\vec{A}", color=BLUE, font_size=30)
        # Position will be set after vec_A is created (in animation step)
        self.objects["label_A"] = label_A

        point_A_end = Dot(point=[3,1,0], color=BLUE, radius=0.07)
        point_A_end.move_to(content_center + 3*RIGHT + UP)
        self.objects["point_A_end"] = point_A_end

        coord_label_A = MathTex(r"(3, 1)", color=BLUE, font_size=24)
        # Position will be set relative to point_A_end
        self.objects["coord_label_A"] = coord_label_A

        # Vector B and its components
        vec_B = Arrow(start=[3,1,0], end=[4,3,0], color=GREEN, stroke_width=6, buff=0)
        vec_B.move_to(content_center + 3*RIGHT + UP)
        self.objects["vec_B"] = vec_B

        label_B = MathTex(r"\vec{B}", color=GREEN, font_size=30)
        self.objects["label_B"] = label_B

        point_B_end = Dot(point=[4,3,0], color=GREEN, radius=0.07)
        point_B_end.move_to(content_center + 4*RIGHT + 3*UP)
        self.objects["point_B_end"] = point_B_end

        coord_label_B = MathTex(r"(4, 3)", color=GREEN, font_size=24)
        self.objects["coord_label_B"] = coord_label_B

        # Dashed resultant line
        dashed_resultant_line = DashedLine(
            start=[0,0,0],
            end=[4,3,0],
            color=YELLOW,
            stroke_width=3,
            dash_length=0.1
        )
        dashed_resultant_line.move_to(content_center)
        self.objects["dashed_resultant_line"] = dashed_resultant_line

        # Resultant vector C and its label
        vec_C = Arrow(start=[0,0,0], end=[4,3,0], color=RED, stroke_width=8, buff=0)
        vec_C.move_to(content_center)
        self.objects["vec_C"] = vec_C

        label_C = MathTex(r"\vec{C}", color=RED, font_size=36)
        self.objects["label_C"] = label_C

        # Vector equation
        vector_equation = MathTex(r"\vec{A} + \vec{B} = \vec{C}", color=WHITE, font_size=40)
        vector_equation.move_to(content_center + 2*DOWN)
        self.objects["vector_equation"] = vector_equation

        # Step narration (initial)
        step_narration_1 = Text(
            "Step 1: Draw vector A from the origin (0,0) to point (3,1).",
            color=LIGHT_GRAY,
            font_size=28
        )
        step_narration_1.move_to(explanation_anchor)
        self.objects["step_narration_1"] = step_narration_1

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/To_animate_the_vecto_9f10bfcfb8/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = max(0.1, 5.736 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/To_animate_the_vecto_9f10bfcfb8/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Indicate point_A_end
        self.play(Indicate(self.objects["point_A_end"], color=YELLOW, run_time=1))

        # Visual action: Create vec_A, then its label and endpoint dot
        self.play(Create(self.objects["vec_A"]), run_time=1.5)

        # Position and create label_A
        label_A = self.objects["label_A"]
        label_A.next_to(self.objects["vec_A"].get_center(), UP+LEFT, buff=0.2)
        self.play(Write(label_A), run_time=0.8)

        # Create point_A_end and its coordinate label
        self.play(FadeIn(self.objects["point_A_end"]), run_time=0.5)
        coord_label_A = self.objects["coord_label_A"]
        coord_label_A.next_to(self.objects["point_A_end"], RIGHT, buff=0.15)
        self.play(Write(coord_label_A), run_time=0.7)

        total_anim_time_2 = 1.5 + 0.8 + 0.5 + 0.7
        remaining_2 = max(0.1, 3.504 - total_anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/To_animate_the_vecto_9f10bfcfb8/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Circumscribe point_A_end
        self.play(Circumscribe(self.objects["point_A_end"], color=YELLOW, run_time=1))

        # Visual action: Create vec_B, then its label and endpoint dot
        self.play(Create(self.objects["vec_B"]), run_time=1.5)

        # Position and create label_B
        label_B = self.objects["label_B"]
        label_B.next_to(self.objects["vec_B"].get_center(), UP+RIGHT, buff=0.2)
        self.play(Write(label_B), run_time=0.8)

        # Create point_B_end and its coordinate label
        self.play(FadeIn(self.objects["point_B_end"]), run_time=0.5)
        coord_label_B = self.objects["coord_label_B"]
        coord_label_B.next_to(self.objects["point_B_end"], UP, buff=0.15)
        self.play(Write(coord_label_B), run_time=0.7)

        total_anim_time_3 = 1.5 + 0.8 + 0.5 + 0.7
        remaining_3 = max(0.1, 8.952 - total_anim_time_3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/To_animate_the_vecto_9f10bfcfb8/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Create dashed_resultant_line (already handled as visual action)
        # Visual action: Create dashed_resultant_line
        self.play(Create(self.objects["dashed_resultant_line"]), run_time=2.0)
        remaining_4 = max(0.1, 6.192 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/To_animate_the_vecto_9f10bfcfb8/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate vec_C
        self.play(Indicate(self.objects["vec_C"], color=RED, run_time=1))

        # Visual action: Create vec_C and its label
        self.play(Create(self.objects["vec_C"]), run_time=1.5)

        # Position and create label_C
        label_C = self.objects["label_C"]
        label_C.next_to(self.objects["vec_C"].get_center(), DOWN+LEFT, buff=0.2)
        self.play(Write(label_C), run_time=0.8)

        total_anim_time_5 = 1.5 + 0.8
        remaining_5 = max(0.1, 7.344 - total_anim_time_5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/To_animate_the_vecto_9f10bfcfb8/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: Write vector_equation
        # Visual action: Write vector_equation
        self.play(Write(self.objects["vector_equation"]), run_time=2.0)
        remaining_6 = max(0.1, 7.128 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final pause
        self.wait(max(0.1, 2))