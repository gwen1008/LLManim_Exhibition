'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize solving the linear equation 2x = 6 using a concrete balance scale model and abstract symbolic transformation.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Solving 2x = 6 with a Balance Scale"
#    - Main Content: [Center y=0] for the balance scale, pans, boxes, and circles.
#    - Footer Region: [Bottom y=-2.5] for the evolving equation.
# 3. Anti-Overlap Check:
#    - Strategy: Keep scale components grouped. Equation is placed low (y=-2.5) to avoid collision with scale pans.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_visualize_the_equ_84cda10a8c/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Fade in title.
#    - Step 2: Create the entire scale structure, boxes, and circles simultaneously.
#    - Step 3: Write the equation "2x = 6" and Indicate it.
#    - Step 4: Circumscribe the equation, then FadeOut half the objects (box2, circles 3,4,5).
#    - Step 5: Indicate the remaining box, then ReplacementTransform the equation to "x = 3".
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        equation_anchor = 2.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # scale_pivot (Triangle)
        pivot_points = [np.array([0, 0, 0]), np.array([-0.5, -0.8, 0]), np.array([0.5, -0.8, 0])]
        scale_pivot = Polygon(*pivot_points, color=GRAY, fill_opacity=0.8)
        scale_pivot.move_to(content_center)
        self.objects["scale_pivot"] = scale_pivot

        # scale_beam
        scale_beam = Line(start=4*LEFT, end=4*RIGHT, color=GRAY_B, stroke_width=8)
        scale_beam.move_to(content_center + 0.1*UP)
        self.objects["scale_beam"] = scale_beam

        # left_pan
        left_pan = Square(side_length=1.5, color=GRAY, fill_opacity=0.2, stroke_width=2)
        left_pan.next_to(scale_beam.get_end(), DOWN, buff=0).shift(4*LEFT + 0.75*DOWN)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Square(side_length=1.5, color=GRAY, fill_opacity=0.2, stroke_width=2)
        right_pan.next_to(scale_beam.get_end(), DOWN, buff=0).shift(4*RIGHT + 0.75*DOWN)
        self.objects["right_pan"] = right_pan

        # box1
        box1 = Square(side_length=1.0, color=BLUE_C, fill_opacity=0.8)
        box1.move_to(left_pan.get_center() + 0.3*UP)
        self.objects["box1"] = box1

        # box2
        box2 = Square(side_length=1.0, color=BLUE_C, fill_opacity=0.8)
        box2.next_to(box1, DOWN, buff=0.2)
        self.objects["box2"] = box2

        # circle_group (6 circles in a 2x3 grid)
        circles = VGroup(*[Circle(radius=0.4, color=GREEN_C, fill_opacity=0.8) for _ in range(6)])
        circles.arrange_in_grid(rows=2, cols=3, buff=0.3)
        circles.move_to(right_pan.get_center())
        self.objects["circle_group"] = circles
        # Also store individual circles for easy access in step 4
        for i, circle in enumerate(circles):
            self.objects[f"circle_group[{i}]"] = circle

        # initial_eq
        initial_eq = MathTex("2x = 6", color=WHITE, font_size=48)
        initial_eq.move_to(equation_anchor)
        self.objects["initial_eq"] = initial_eq

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/To_visualize_the_equ_84cda10a8c/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 8.568 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/To_visualize_the_equ_84cda10a8c/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(
            Create(self.objects["scale_pivot"]),
            Create(self.objects["scale_beam"]),
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            Create(self.objects["box1"]),
            Create(self.objects["box2"]),
            Create(self.objects["circle_group"]),
            run_time=3.0
        )
        remaining_2 = max(0.1, 12.312 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/To_visualize_the_equ_84cda10a8c/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate initial_eq
        self.play(Indicate(self.objects["initial_eq"], color=YELLOW, run_time=1))
        # Visual action: Write initial_eq
        self.play(Write(self.objects["initial_eq"]), run_time=1.5)
        remaining_3 = max(0.1, 5.472 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/To_visualize_the_equ_84cda10a8c/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Circumscribe initial_eq
        self.play(Circumscribe(self.objects["initial_eq"], color=ORANGE, run_time=1))
        # Visual action: FadeOut box2 and circles 3,4,5 (indices 3,4,5)
        self.play(
            FadeOut(self.objects["box2"]),
            FadeOut(self.objects["circle_group[3]"]),
            FadeOut(self.objects["circle_group[4]"]),
            FadeOut(self.objects["circle_group[5]"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 8.616 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/To_visualize_the_equ_84cda10a8c/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate box1
        self.play(Indicate(self.objects["box1"], color=YELLOW, run_time=1))
        # Visual action: ReplacementTransform initial_eq to new equation "x = 3"
        final_eq = MathTex("x = 3", color=WHITE, font_size=48)
        final_eq.move_to(self.objects["initial_eq"].get_center())
        self.play(ReplacementTransform(self.objects["initial_eq"], final_eq), run_time=2.0)
        remaining_5 = max(0.1, 9.984 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))