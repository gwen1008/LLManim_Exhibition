'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize that a circle's circumference (πD) is slightly longer than three diameters (3D), illustrating π > 3.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] Left side for circle, right side for comparison lines.
#    - Footer Region: [Bottom y=-3.5] for final comparison text.
# 3. Anti-Overlap Check:
#    - Strategy: Place circle on left (x ~ -4), lines on right (x ~ 4). Use VGroup for 3D segments.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_an_animation__14e8550228/step_XX.mp3"
# 5. Animation Flow:
#    - Show circle and diameter.
#    - Unfold circumference into a line (πD) on the right.
#    - Construct 3D line below it.
#    - Compare lengths, conclude πD > 3D.
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
        circle_anchor = 4 * LEFT  # Left side
        lines_anchor = 4 * RIGHT   # Right side
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Unfolding a Circle: Circumference = πD", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # diameter_line
        diameter_line = Line(
            start=circle_anchor + LEFT*2,
            end=circle_anchor + RIGHT*2,
            color=YELLOW,
            stroke_width=6
        )
        self.objects["diameter_line"] = diameter_line

        # diameter_label
        diameter_label = MathTex("D", color=YELLOW)
        diameter_label.next_to(diameter_line, UP, buff=0.2)
        self.objects["diameter_label"] = diameter_label

        # unfold_guide
        # Guide from circle's rightmost point to start of πD line
        guide_start = circle_anchor + RIGHT*2  # Rightmost point of circle
        guide_end = lines_anchor + LEFT*6.283  # Start of πD line (π*2 ≈ 6.283)
        unfold_guide = DashedLine(
            start=guide_start,
            end=guide_end,
            color=GREY,
            stroke_width=2,
            dash_length=0.1
        )
        self.objects["unfold_guide"] = unfold_guide

        # line_piD
        line_piD = Line(
            start=lines_anchor + LEFT*6.283,
            end=lines_anchor + RIGHT*6.283,
            color=GREEN,
            stroke_width=8
        )
        line_piD.set_opacity(0)
        self.objects["line_piD"] = line_piD

        # label_piD
        label_piD = MathTex("\\pi D", color=GREEN)
        label_piD.next_to(line_piD, UP, buff=0.3)
        self.objects["label_piD"] = label_piD

        # line_3d (VGroup of three segments)
        segment_d1 = Line(
            start=LEFT*6,
            end=LEFT*2,
            color=RED,
            stroke_width=6
        )
        segment_d2 = Line(
            start=LEFT*2,
            end=RIGHT*2,
            color=RED,
            stroke_width=6
        )
        segment_d3 = Line(
            start=RIGHT*2,
            end=RIGHT*6,
            color=RED,
            stroke_width=6
        )
        line_3d = VGroup(segment_d1, segment_d2, segment_d3)
        line_3d.move_to(lines_anchor + DOWN*1.5)
        line_3d.set_opacity(0)
        self.objects["line_3d"] = line_3d
        self.objects["segment_d1"] = segment_d1
        self.objects["segment_d2"] = segment_d2
        self.objects["segment_d3"] = segment_d3

        # label_3d
        label_3d = MathTex("3D", color=RED)
        label_3d.next_to(line_3d, UP, buff=0.3)
        self.objects["label_3d"] = label_3d

        # footer_text
        footer_text = MathTex("\\pi D > 3D", color=WHITE, font_size=30)
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Create_an_animation__14e8550228/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        # signal_action: Create circle
        self.play(Create(self.objects["circle"]), run_time=1.5)
        remaining_1 = max(0.1, 6.912 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_an_animation__14e8550228/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        # signal_action: Indicate circle
        self.play(Indicate(self.objects["circle"], color=WHITE, run_time=1))
        # visual_action: Create diameter_line
        self.play(Create(self.objects["diameter_line"]), run_time=1.5)
        remaining_2 = max(0.1, 6.624 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_an_animation__14e8550228/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # signal_action: Write diameter_label
        self.play(Write(self.objects["diameter_label"]), run_time=1)
        remaining_3 = max(0.1, 5.808 - 1 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_an_animation__14e8550228/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # signal_action: Create unfold_guide
        self.play(Create(self.objects["unfold_guide"]), run_time=1.5)
        remaining_4 = max(0.1, 4.224 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_an_animation__14e8550228/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # signal_action: GrowFromPoint line_piD
        line_piD = self.objects["line_piD"]
        line_piD.set_opacity(1)
        self.play(
            GrowFromPoint(line_piD, point=line_piD.get_start()),
            FadeOut(self.objects["unfold_guide"]),
            run_time=2.0
        )
        remaining_5 = max(0.1, 3.456 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Create_an_animation__14e8550228/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # signal_action: Write label_piD
        self.play(Write(self.objects["label_piD"]), run_time=1)
        remaining_6 = max(0.1, 5.496 - 1 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/Create_an_animation__14e8550228/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # signal_action: Indicate diameter_line
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        # visual_action: Create segment_d1
        segment_d1 = self.objects["segment_d1"]
        segment_d1.set_opacity(1)
        self.play(Create(segment_d1), run_time=1.0)
        remaining_7 = max(0.1, 3.72 - 1 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/Create_an_animation__14e8550228/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # signal_action: null
        # visual_action: Create segment_d2
        segment_d2 = self.objects["segment_d2"]
        segment_d2.set_opacity(1)
        self.play(Create(segment_d2), run_time=1.0)
        remaining_8 = max(0.1, 2.808 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/Create_an_animation__14e8550228/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # signal_action: null
        # visual_action: Create segment_d3
        segment_d3 = self.objects["segment_d3"]
        segment_d3.set_opacity(1)
        self.play(Create(segment_d3), run_time=1.0)
        remaining_9 = max(0.1, 2.52 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        audio_step10 = "media/audio/Create_an_animation__14e8550228/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # signal_action: Write label_3d
        self.play(Write(self.objects["label_3d"]), run_time=1)
        remaining_10 = max(0.1, 5.448 - 1 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Step 11
        audio_step11 = "media/audio/Create_an_animation__14e8550228/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        # signal_action: Indicate line_piD
        self.play(Indicate(self.objects["line_piD"], color=GREEN, run_time=1))
        # visual_action: Create footer_text
        self.play(Write(self.objects["footer_text"]), run_time=1.5)
        remaining_11 = max(0.1, 10.008 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_11))

        # Final hold
        self.wait(max(0.1, 2))