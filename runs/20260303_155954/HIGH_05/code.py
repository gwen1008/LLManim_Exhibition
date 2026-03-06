'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition via the triangle method, showing that placing vectors head-to-tail and drawing the resultant from the tail of the first to the head of the last yields the sum.
# 2. Layout Strategy: Use High-Low Split.
#    - Header Region: [y=3.0] for Title "Vector Addition: The Triangle Method"
#    - Main Content: [Center y=0] for coordinate grid and vectors.
#    - Footer Region: [Bottom y=-2.8] for final equation.
# 3. Anti-Overlap Check:
#    - Strategy: Use relative positioning for labels (next_to arrow tips). The grid is centered, vectors are placed relative to grid center. Title and equation are in separate zones.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/vector_addition_triangle_method/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create grid.
#    - Step 2: Create vector A (blue) with Indicate signal.
#    - Step 3: Write label A.
#    - Step 4: Create vector B (green) with Indicate signal.
#    - Step 5: Write label B.
#    - Step 6: Create dashed triangle with Circumscribe signal.
#    - Step 7: Create resultant vector C (red) with Indicate signal.
#    - Step 8: Write label C.
#    - Step 9: Write final equation with Indicate signal.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        title_anchor = 3.0 * UP
        grid_center = ORIGIN
        explanation_anchor = -2.8 * UP

        # Create objects from layout_plan
        # Title
        title = Text("Vector Addition: The Triangle Method", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Grid
        grid = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=10,
            stroke_opacity=0.5,
            axis_config={"stroke_opacity": 0.7}
        )
        grid.move_to(grid_center)
        self.objects["grid"] = grid

        # Vector A
        vector_a = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color="#1E88E5",
            stroke_width=6,
            tip_length=0.2,
            buff=0
        )
        vector_a.move_to(grid_center)
        self.objects["vector_a"] = vector_a

        # Label A
        label_a = MathTex(r"\vec{A} = (3,1)", color="#1E88E5", font_size=28)
        label_a.next_to(vector_a.get_end(), RIGHT, buff=0.1)
        self.objects["label_a"] = label_a

        # Vector B
        vector_b = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color="#43A047",
            stroke_width=6,
            tip_length=0.2,
            buff=0
        )
        vector_b.move_to(grid_center + [3, 1, 0])
        self.objects["vector_b"] = vector_b

        # Label B
        label_b = MathTex(r"\vec{B} = (1,2)", color="#43A047", font_size=28)
        label_b.next_to(vector_b.get_end(), UP + RIGHT, buff=0.1)
        self.objects["label_b"] = label_b

        # Vector C (Resultant)
        vector_c = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color="#E53935",
            stroke_width=8,
            tip_length=0.25,
            buff=0
        )
        vector_c.move_to(grid_center)
        self.objects["vector_c"] = vector_c

        # Label C
        label_c = MathTex(r"\vec{C}", color="#E53935", font_size=32)
        label_c.next_to(vector_c.get_end(), LEFT + UP, buff=0.1)
        self.objects["label_c"] = label_c

        # Triangle (dashed)
        triangle = Polygon(
            [0, 0, 0],
            [3, 1, 0],
            [4, 3, 0],
            color=YELLOW,
            stroke_width=3,
            stroke_opacity=0.7,
            fill_opacity=0.0
        )
        triangle.move_to(grid_center)
        triangle = DashedVMobject(triangle, num_dashes=15)
        self.objects["triangle"] = triangle

        # Equation C
        equation_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4,3)", color=WHITE, font_size=32)
        equation_c.move_to(explanation_anchor)
        self.objects["equation_c"] = equation_c

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_00.mp3")  # [auto-injected]
        # Step 1: Create grid
        audio_step1 = "media/audio/vector_addition_triangle_method/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["grid"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_01.mp3")  # [auto-injected]
        # Step 2: Create vector A with Indicate signal
        audio_step2 = "media/audio/vector_addition_triangle_method/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["vector_a"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vector_a"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_02.mp3")  # [auto-injected]
        # Step 3: Write label A
        audio_step3 = "media/audio/vector_addition_triangle_method/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Write(self.objects["label_a"]), run_time=1.5)
        remaining_3 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_03.mp3")  # [auto-injected]
        # Step 4: Create vector B with Indicate signal
        audio_step4 = "media/audio/vector_addition_triangle_method/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["vector_b"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vector_b"]), run_time=1.5)
        remaining_4 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_04.mp3")  # [auto-injected]
        # Step 5: Write label B
        audio_step5 = "media/audio/vector_addition_triangle_method/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Write(self.objects["label_b"]), run_time=1.5)
        remaining_5 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_05.mp3")  # [auto-injected]
        # Step 6: Create triangle with Circumscribe signal
        audio_step6 = "media/audio/vector_addition_triangle_method/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["triangle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["triangle"]), run_time=2.0)
        remaining_6 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_06.mp3")  # [auto-injected]
        # Step 7: Create vector C with Indicate signal
        audio_step7 = "media/audio/vector_addition_triangle_method/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["vector_c"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["vector_c"]), run_time=1.5)
        remaining_7 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_07.mp3")  # [auto-injected]
        # Step 8: Write label C
        audio_step8 = "media/audio/vector_addition_triangle_method/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Write(self.objects["label_c"]), run_time=1.5)
        remaining_8 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/To_animate_the_vecto_1464932052/step_08.mp3")  # [auto-injected]
        # Step 9: Write equation with Indicate signal
        audio_step9 = "media/audio/vector_addition_triangle_method/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["equation_c"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["equation_c"]), run_time=2.0)
        remaining_9 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))