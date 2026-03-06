'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual proof of the Corresponding Angles Theorem: corresponding interior angles formed by a transversal cutting two parallel lines are congruent.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Corresponding Angles Theorem"
#    - Main Content: [Center y=0] for the geometric diagram (parallel lines, transversal, angle arcs)
#    - Footer Region: [Bottom y=-3.5] for the principle statement text.
# 3. Anti-Overlap Check:
#    - Strategy: Keep diagram centered at origin. Title and footer are in separate zones. Angle arcs are small (radius=0.4) and placed at intersection points.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/corresponding_angles_theorem/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-3: Draw parallel lines and transversal.
#    - Step 4-5: Mark and label intersection points A and B.
#    - Step 6-7: Draw the two corresponding interior angle arcs.
#    - Step 8: Core demonstration: Animate a copy of angle A moving to superimpose on angle B.
#    - Step 9: Display the concluding principle.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Corresponding Angles Theorem", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Parallel lines
        line_l1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(diagram_center + UP)
        self.objects["line_l1"] = line_l1

        line_l2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(diagram_center + DOWN)
        self.objects["line_l2"] = line_l2

        # Transversal line
        line_t = Line(start=[-3, -2, 0], end=[3, 2, 0], color=YELLOW, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t

        # Intersection points and labels
        point_A = Dot(point=[1.5, 1, 0], color=WHITE, radius=0.06)
        self.objects["point_A"] = point_A

        point_B = Dot(point=[-1.5, -1, 0], color=WHITE, radius=0.06)
        self.objects["point_B"] = point_B

        label_A = MathTex("A", color=WHITE, font_size=24)
        label_A.next_to(point_A, UR, buff=0.1)
        self.objects["label_A"] = label_A

        label_B = MathTex("B", color=WHITE, font_size=24)
        label_B.next_to(point_B, DL, buff=0.1)
        self.objects["label_B"] = label_B

        # Rays for angle construction
        ray_l1_left = Line(start=[1.5, 1, 0], end=[0.5, 1, 0], color=BLUE, stroke_width=4)
        self.objects["ray_l1_left"] = ray_l1_left

        ray_t_down_A = Line(start=[1.5, 1, 0], end=[0.5, 0.333, 0], color=YELLOW, stroke_width=4)
        self.objects["ray_t_down_A"] = ray_t_down_A

        ray_l2_left = Line(start=[-1.5, -1, 0], end=[-2.5, -1, 0], color=BLUE, stroke_width=4)
        self.objects["ray_l2_left"] = ray_l2_left

        ray_t_down_B = Line(start=[-1.5, -1, 0], end=[-2.5, -1.667, 0], color=YELLOW, stroke_width=4)
        self.objects["ray_t_down_B"] = ray_t_down_B

        # Angle arcs (will be created after rays are defined)
        # We'll create them later when needed, but define placeholders now.
        self.objects["angle_arc_A"] = None
        self.objects["angle_arc_B"] = None

        # Principle text
        principle_text = Text(
            "Corresponding angles formed by a transversal of parallel lines are congruent.",
            color=WHITE,
            font_size=28
        )
        principle_text.move_to(footer_anchor)
        self.objects["principle_text"] = principle_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1: Draw top parallel line
        audio_step1 = "media/audio/corresponding_angles_theorem/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["line_l1"]), run_time=1.0)
        remaining_1 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2: Draw bottom parallel line
        audio_step2 = "media/audio/corresponding_angles_theorem/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["line_l2"]), run_time=1.0)
        remaining_2 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3: Draw transversal line
        audio_step3 = "media/audio/corresponding_angles_theorem/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Create(self.objects["line_t"]), run_time=1.5)
        remaining_3 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4: Mark and label point A
        audio_step4 = "media/audio/corresponding_angles_theorem/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Signal action: Indicate point_A
        self.play(Indicate(self.objects["point_A"], color=RED, run_time=1))
        # Visual action: Grow dot and write label
        self.play(GrowFromCenter(self.objects["point_A"]), run_time=0.75)
        self.play(Write(self.objects["label_A"]), run_time=0.75)
        remaining_4 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5: Mark and label point B
        audio_step5 = "media/audio/corresponding_angles_theorem/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action: Indicate point_B
        self.play(Indicate(self.objects["point_B"], color=RED, run_time=1))
        # Visual action: Grow dot and write label
        self.play(GrowFromCenter(self.objects["point_B"]), run_time=0.75)
        self.play(Write(self.objects["label_B"]), run_time=0.75)
        remaining_5 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6: Draw angle arc at A (first create the rays if not already shown, but they are for angle construction only)
        # Actually, the rays are just for constructing the Angle mobject. We don't need to show them.
        # Create angle_arc_A
        angle_arc_A = Angle(
            self.objects["ray_l1_left"],
            self.objects["ray_t_down_A"],
            radius=0.4,
            other_angle=False,
            color=GREEN,
            stroke_width=6
        )
        self.objects["angle_arc_A"] = angle_arc_A

        audio_step6 = "media/audio/corresponding_angles_theorem/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Create(self.objects["angle_arc_A"]), run_time=2.5)
        remaining_6 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7: Draw angle arc at B
        # Create angle_arc_B
        angle_arc_B = Angle(
            self.objects["ray_l2_left"],
            self.objects["ray_t_down_B"],
            radius=0.4,
            other_angle=False,
            color=GREEN,
            stroke_width=6
        )
        self.objects["angle_arc_B"] = angle_arc_B

        audio_step7 = "media/audio/corresponding_angles_theorem/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # Signal action: Indicate point_B (again)
        self.play(Indicate(self.objects["point_B"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["angle_arc_B"]), run_time=2.0)
        remaining_7 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8: Core demonstration - animate angle A moving to angle B
        audio_step8 = "media/audio/corresponding_angles_theorem/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Signal action: Circumscribe angle_arc_A
        self.play(Circumscribe(self.objects["angle_arc_A"], color=YELLOW, run_time=1))
        # Create a copy of angle_arc_A for the transformation
        angle_copy = self.objects["angle_arc_A"].copy()
        self.add(angle_copy)
        # Animate the copy moving and rotating to match angle_arc_B
        # We'll use Transform which will handle position and rotation.
        self.play(Transform(angle_copy, self.objects["angle_arc_B"]), run_time=3.0)
        remaining_8 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        # Remove the copy after transformation
        self.remove(angle_copy)

        # Step 9: Display principle text
        audio_step9 = "media/audio/corresponding_angles_theorem/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Write(self.objects["principle_text"]), run_time=3.0)
        remaining_9 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))