from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Left Pizza Circle
        pizza_left_circle = Circle(radius=1.5, color=WHITE, fill_opacity=0.1, stroke_width=2)
        pizza_left_circle.move_to(content_center + 3.5 * LEFT)
        self.objects["pizza_left_circle"] = pizza_left_circle

        # Right Pizza Circle
        pizza_right_circle = Circle(radius=1.5, color=WHITE, fill_opacity=0.1, stroke_width=2)
        pizza_right_circle.move_to(content_center + 3.5 * RIGHT)
        self.objects["pizza_right_circle"] = pizza_right_circle

        # Labels for pizzas
        label_left = MathTex(r"\text{Pizza 1}", color=GRAY_B)
        label_left.next_to(pizza_left_circle, UP, buff=0.5)
        self.objects["label_left"] = label_left

        label_right = MathTex(r"\text{Pizza 2}", color=GRAY_B)
        label_right.next_to(pizza_right_circle, UP, buff=0.5)
        self.objects["label_right"] = label_right

        # Left pizza sector (half)
        sector_left_half = Sector(radius=1.5, angle=PI, start_angle=0, color="#FF9900", fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
        sector_left_half.move_to(pizza_left_circle.get_center() + LEFT * 0.2)
        self.objects["sector_left_half"] = sector_left_half

        # Right pizza sectors (quarters)
        sector_right_q1 = Sector(radius=1.5, angle=PI/2, start_angle=0, color="#3399FF", fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
        sector_right_q1.move_to(pizza_right_circle.get_center() + DOWN * 0.1)
        self.objects["sector_right_q1"] = sector_right_q1

        sector_right_q2 = Sector(radius=1.5, angle=PI/2, start_angle=PI/2, color="#3399FF", fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
        sector_right_q2.move_to(pizza_right_circle.get_center() + DOWN * 0.1)
        self.objects["sector_right_q2"] = sector_right_q2

        # Fraction labels
        frac_left = MathTex(r"\frac{1}{2}", color="#FF9900", font_size=36)
        frac_left.next_to(pizza_left_circle, DOWN, buff=0.5)
        self.objects["frac_left"] = frac_left

        frac_right = MathTex(r"\frac{2}{4}", color="#3399FF", font_size=36)
        frac_right.next_to(pizza_right_circle, DOWN, buff=0.5)
        self.objects["frac_right"] = frac_right

        # Conclusion text
        conclusion_text = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=YELLOW, font_size=42)
        conclusion_text.move_to(footer_anchor + UP * 0.5)
        self.objects["conclusion_text"] = conclusion_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Create_two_identical_6b03ade3ce/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["pizza_left_circle"]), run_time=1.5)
        remaining_1 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_two_identical_6b03ade3ce/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["pizza_right_circle"]), run_time=1.5)
        remaining_2 = max(0.1, 2.256 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_two_identical_6b03ade3ce/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["pizza_left_circle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["sector_left_half"]), run_time=1.5)
        remaining_3 = max(0.1, 3.432 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_two_identical_6b03ade3ce/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["sector_left_half"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["frac_left"]), run_time=1.0)
        remaining_4 = max(0.1, 3.552 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_two_identical_6b03ade3ce/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["pizza_right_circle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["sector_right_q1"]), run_time=1.5)
        remaining_5 = max(0.1, 4.2 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Create_two_identical_6b03ade3ce/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Create(self.objects["sector_right_q2"]), run_time=1.5)
        remaining_6 = max(0.1, 3.408 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/Create_two_identical_6b03ade3ce/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        target_group = VGroup(self.objects["sector_right_q1"], self.objects["sector_right_q2"])
        self.play(Circumscribe(target_group, color=YELLOW, run_time=1))
        self.play(Write(self.objects["frac_right"]), run_time=1.0)
        remaining_7 = max(0.1, 4.584 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/Create_two_identical_6b03ade3ce/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        target_group2 = VGroup(self.objects["sector_left_half"], self.objects["sector_right_q1"], self.objects["sector_right_q2"])
        self.play(Indicate(target_group2, color=GREEN, run_time=1))
        self.play(Write(self.objects["conclusion_text"]), run_time=1.5)
        remaining_8 = max(0.1, 5.112 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/Create_two_identical_6b03ade3ce/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["conclusion_text"], color=YELLOW, run_time=1))
        remaining_9 = max(0.1, 3.504 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))