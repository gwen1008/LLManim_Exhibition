'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the linear function y=2x-1, focusing on the y-intercept and the slope as a repeatable "rise over run" action to generate points and reveal the line.
# 2. Layout Strategy: Use three zones.
#    - Header Region: [y=3.5] for Title (y=2x-1)
#    - Main Content: [Center y=0] for Axes, points, slope vectors, and line.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Title is at top, axes centered and scaled, explanation at bottom. Points and labels are placed relative to axes coordinates using c2p. Slope label is placed to the right of the rise arrow.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_an_animation__0da061fb25/step_XX.mp3"
# 5. Animation Flow:
#    Step 1: Create axes.
#    Step 2: Show y-intercept point (0,-1) and label.
#    Step 3: Show horizontal "run" arrow from intercept.
#    Step 4: Show vertical "rise" arrow, then point (1,1) and slope label.
#    Step 5: Show second slope step to point (2,3).
#    Step 6: Draw the complete line.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title_tex
        title_tex = MathTex(r"y = 2x - 1", color=BLUE, font_size=48)
        title_tex.move_to(title_anchor)
        self.objects["title_tex"] = title_tex

        # axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True},
            color=GRAY_C
        ).scale(0.9).move_to(global_center)
        self.objects["axes"] = axes

        # step_text
        step_text = Text("Step 1: Draw the coordinate axes.", color=YELLOW, font_size=28)
        step_text.move_to(explanation_anchor)
        self.objects["step_text"] = step_text

        # dot_b
        dot_b = Dot(radius=0.08, color=GREEN, fill_opacity=1.0)
        dot_b.move_to(axes.c2p(0, -1))
        self.objects["dot_b"] = dot_b

        # label_b
        label_b = MathTex(r"(0, -1)", color=GREEN, font_size=28)
        label_b.next_to(dot_b, LEFT+UP, buff=0.2)
        self.objects["label_b"] = label_b

        # run_arrow
        run_arrow = Arrow(
            start=axes.c2p(0, -1),
            end=axes.c2p(1, -1),
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["run_arrow"] = run_arrow

        # rise_arrow
        rise_arrow = Arrow(
            start=axes.c2p(1, -1),
            end=axes.c2p(1, 1),
            buff=0,
            color=TEAL,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["rise_arrow"] = rise_arrow

        # slope_label
        slope_label = MathTex(r"m = 2 = \frac{Rise}{Run} = \frac{2}{1}", color=ORANGE, font_size=32)
        slope_label.next_to(rise_arrow, RIGHT, buff=0.5)
        self.objects["slope_label"] = slope_label

        # dot_p1
        dot_p1 = Dot(radius=0.08, color=YELLOW, fill_opacity=1.0)
        dot_p1.move_to(axes.c2p(1, 1))
        self.objects["dot_p1"] = dot_p1

        # label_p1
        label_p1 = MathTex(r"(1, 1)", color=YELLOW, font_size=28)
        label_p1.next_to(dot_p1, RIGHT+UP, buff=0.2)
        self.objects["label_p1"] = label_p1

        # dot_p2
        dot_p2 = Dot(radius=0.08, color=PINK, fill_opacity=1.0)
        dot_p2.move_to(axes.c2p(2, 3))
        self.objects["dot_p2"] = dot_p2

        # label_p2
        label_p2 = MathTex(r"(2, 3)", color=PINK, font_size=28)
        label_p2.next_to(dot_p2, RIGHT+UP, buff=0.2)
        self.objects["label_p2"] = label_p2

        # line
        line = Line(
            start=axes.c2p(-1, -3),
            end=axes.c2p(3, 5),
            color=BLUE,
            stroke_width=4
        )
        self.objects["line"] = line

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Create_an_animation__0da061fb25/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title_tex"]), run_time=1.0)
        self.play(Create(self.objects["axes"]), run_time=2.0)
        self.play(Write(self.objects["step_text"]), run_time=1.5)
        remaining_1 = max(0.1, 7.008 - (1.0 + 2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/Create_an_animation__0da061fb25/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Update step text
        step_text_2 = Text("Step 2: Identify the y-intercept (0, -1).", color=YELLOW, font_size=28)
        step_text_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_2), run_time=0.5)
        self.objects["step_text"] = step_text_2

        self.play(Indicate(self.objects["dot_b"], color=GREEN, run_time=1))
        self.play(FadeIn(self.objects["dot_b"]), FadeIn(self.objects["label_b"]), run_time=1.5)
        remaining_2 = max(0.1, 9.384 - (0.5 + 1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/Create_an_animation__0da061fb25/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        step_text_3 = Text("Step 3: Slope = rise/run. Run 1 unit right.", color=YELLOW, font_size=28)
        step_text_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_3), run_time=0.5)
        self.objects["step_text"] = step_text_3

        self.play(Circumscribe(self.objects["run_arrow"], color=RED, run_time=1))
        self.play(Create(self.objects["run_arrow"]), run_time=1.5)
        remaining_3 = max(0.1, 9.192 - (0.5 + 1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Create_an_animation__0da061fb25/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        step_text_4 = Text("Step 4: Rise 2 units up. Land at (1,1). Slope = 2/1 = 2.", color=YELLOW, font_size=28)
        step_text_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_4), run_time=0.5)
        self.objects["step_text"] = step_text_4

        self.play(Circumscribe(self.objects["rise_arrow"], color=TEAL, run_time=1))
        self.play(Create(self.objects["rise_arrow"]), run_time=1.5)
        self.play(FadeIn(self.objects["dot_p1"]), FadeIn(self.objects["label_p1"]), Write(self.objects["slope_label"]), run_time=2.0)
        remaining_4 = max(0.1, 11.28 - (0.5 + 1.0 + 1.5 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/Create_an_animation__0da061fb25/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        step_text_5 = Text("Step 5: Repeat slope from (1,1) to get (2,3).", color=YELLOW, font_size=28)
        step_text_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_5), run_time=0.5)
        self.objects["step_text"] = step_text_5

        self.play(Indicate(self.objects["dot_p1"], color=YELLOW, run_time=1))
        # Create a second slope vector group from (1,1) to (2,3)
        run_arrow2 = Arrow(
            start=axes.c2p(1, 1),
            end=axes.c2p(2, 1),
            buff=0,
            color=RED,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        rise_arrow2 = Arrow(
            start=axes.c2p(2, 1),
            end=axes.c2p(2, 3),
            buff=0,
            color=TEAL,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.play(Create(run_arrow2), run_time=1.0)
        self.play(Create(rise_arrow2), run_time=1.0)
        self.play(FadeIn(self.objects["dot_p2"]), FadeIn(self.objects["label_p2"]), run_time=1.5)
        remaining_5 = max(0.1, 8.976 - (0.5 + 1.0 + 1.0 + 1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/Create_an_animation__0da061fb25/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        step_text_6 = Text("Step 6: Connect points to reveal the line y=2x-1.", color=YELLOW, font_size=28)
        step_text_6.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], step_text_6), run_time=0.5)
        self.objects["step_text"] = step_text_6

        self.play(Indicate(self.objects["line"], color=BLUE, run_time=1))
        self.play(Create(self.objects["line"]), run_time=3.0)
        remaining_6 = max(0.1, 17.232 - (0.5 + 1.0 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))