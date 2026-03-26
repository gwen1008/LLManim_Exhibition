from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create title
        title = Text("Distance on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create number line
        number_line = Line(start=[-6, 0, 0], end=[6, 0, 0], color=GRAY_B, stroke_width=4)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Create ticks_group (11 ticks from x=-5 to 5)
        ticks = VGroup()
        for x in range(-5, 6):
            tick = Line(start=[x, -0.2, 0], end=[x, 0.2, 0], color=WHITE)
            ticks.add(tick)
        ticks.move_to(content_center)
        self.objects["ticks_group"] = ticks

        # Create labels_group (MathTex labels '-5' to '5')
        labels = VGroup()
        for x in range(-5, 6):
            label = MathTex(str(x), color=WHITE, font_size=24)
            label.move_to([x, -0.5, 0])
            labels.add(label)
        labels.move_to(content_center)
        self.objects["labels_group"] = labels

        # Create point_start (green dot at -2)
        point_start = Dot(radius=0.08, color=GREEN)
        point_start.move_to([-2, 0, 0])
        self.objects["point_start"] = point_start

        # Create label_start (MathTex '-2')
        label_start = MathTex("-2", color=GREEN, font_size=28)
        label_start.next_to(point_start, UP, buff=0.1)
        self.objects["label_start"] = label_start

        # Create point_end (red dot at 3)
        point_end = Dot(radius=0.08, color=RED)
        point_end.move_to([3, 0, 0])
        self.objects["point_end"] = point_end

        # Create label_end (MathTex '+3')
        label_end = MathTex("+3", color=RED, font_size=28)
        label_end.next_to(point_end, UP, buff=0.2)
        self.objects["label_end"] = label_end

        # Create moving_dot (yellow dot, initially at start)
        moving_dot = Dot(radius=0.1, color=YELLOW)
        moving_dot.move_to([-2, 0, 0])
        moving_dot.set_z_index(1)
        self.objects["moving_dot"] = moving_dot

        # Create spanning_arrow (blue arrow from start to end, y=0.5)
        spanning_arrow = Arrow(start=[-2, 0.5, 0], end=[3, 0.5, 0], color=BLUE, stroke_width=8, buff=0)
        self.objects["spanning_arrow"] = spanning_arrow

        # Create distance_label (MathTex '5')
        distance_label = MathTex("5", color=BLUE, font_size=36)
        distance_label.next_to(spanning_arrow, UP, buff=0.5)
        self.objects["distance_label"] = distance_label

        # Create initial step_explanation
        step_explanation = Text("We begin with a number line from -5 to 5.", color=GRAY_B, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_a_number_line_0e039892c1/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["number_line"]), run_time=1.5)
        remaining_1 = max(0.1, 3.648 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/Create_a_number_line_0e039892c1/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["ticks_group"]), run_time=1.5)
        remaining_2 = max(0.1, 3.408 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_a_number_line_0e039892c1/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Circumscribe labels_group[3] (which is '-2')
        self.play(Circumscribe(self.objects["labels_group"][3], color=YELLOW, run_time=1))
        # Visual action: Create point_start
        self.play(Create(self.objects["point_start"]), run_time=1.5)
        remaining_3 = max(0.1, 5.664 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_a_number_line_0e039892c1/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate point_start
        self.play(Indicate(self.objects["point_start"], color=GREEN, run_time=1))
        # Visual action: Write label_start
        self.play(Write(self.objects["label_start"]), run_time=1.0)
        remaining_4 = max(0.1, 2.592 - 1.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_a_number_line_0e039892c1/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate labels_group[8] (which is '3')
        self.play(Indicate(self.objects["labels_group"][8], color=RED, run_time=1))
        # Visual action: Create point_end
        self.play(Create(self.objects["point_end"]), run_time=1.5)
        remaining_5 = max(0.1, 2.928 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/Create_a_number_line_0e039892c1/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: Create moving_dot (but it's already created, so we FadeIn)
        self.play(FadeIn(self.objects["moving_dot"]), run_time=0.5)
        # Visual action: ApplyMethod to move moving_dot from start to end
        self.play(self.objects["moving_dot"].animate.move_to(self.objects["point_end"].get_center()), run_time=3.0)
        remaining_6 = max(0.1, 3.408 - 3.0 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/Create_a_number_line_0e039892c1/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # Signal action: Create spanning_arrow (but it's already created, so we GrowArrow)
        # Visual action: GrowArrow (Create with GrowArrow effect)
        self.play(GrowArrow(self.objects["spanning_arrow"]), run_time=2.0)
        remaining_7 = max(0.1, 5.472 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/Create_a_number_line_0e039892c1/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        # Signal action: Indicate spanning_arrow
        self.play(Indicate(self.objects["spanning_arrow"], color=BLUE, run_time=1))
        # Visual action: Write distance_label
        self.play(Write(self.objects["distance_label"]), run_time=1.5)
        remaining_8 = max(0.1, 9.072 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Final hold
        self.wait(max(0.1, 2))