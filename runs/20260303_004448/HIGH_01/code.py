'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the concept of slope as "rise over run" using a coordinate plane and a moving point on the line y=2x-1.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Slope: Rise over Run"
#    - Main Content: [Center y=0] for axes, line, points, and dynamic triangle.
#    - Footer Region: [Bottom y=-3.5] for step-by-step narrative text.
# 3. Anti-Overlap Check:
#    - Title at top, explanation at bottom, main graph centered.
#    - Dynamic triangle and labels will be positioned relative to the moving point.
#    - Use .scale(0.8) for footer text to prevent overflow.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/slope_rise_over_run/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Create line graph, indicate its label.
#    - Step 3: Show y-intercept point and label.
#    - Step 4: Introduce moving red dot.
#    - Step 5: Animate horizontal run, draw dashed line, label "run".
#    - Step 6: Animate vertical rise, draw dashed line, label "rise", complete triangle.
#    - Step 7: Show slope pattern repeats, move point further, circumscribe line.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Slope: Rise over Run", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True},
            color=GRAY_C
        ).scale(0.9).move_to(global_center)
        self.objects["axes"] = axes

        # line_graph
        line_graph = axes.plot(lambda x: 2*x - 1, x_range=[-1.5, 2.5], color=BLUE, stroke_width=4)
        # Note: initial_pos "move_to(axes.c2p(0,0))" is not needed for a FunctionGraph relative to axes.
        self.objects["line_graph"] = line_graph

        # line_label
        line_label = MathTex(r"y = 2x - 1", color=BLUE)
        # Position next to axes.c2p(2, 3). We'll compute that point.
        label_point = axes.c2p(2, 3)
        line_label.next_to(label_point, RIGHT, buff=0.2)
        self.objects["line_label"] = line_label

        # start_point
        start_point = Dot(radius=0.08, color=YELLOW)
        start_point.move_to(axes.c2p(0, -1))
        self.objects["start_point"] = start_point

        # start_label
        start_label = MathTex(r"(0, -1)", color=YELLOW, font_size=30)
        start_label.next_to(start_point, UP+LEFT, buff=0.1)
        self.objects["start_label"] = start_label

        # moving_point
        moving_point = Dot(radius=0.08, color=RED)
        moving_point.move_to(axes.c2p(0, -1))
        self.objects["moving_point"] = moving_point

        # step_explanation
        step_explanation = Text("We begin by drawing the axes and the line y = 2x - 1.", color=GRAY_C, font_size=28)
        step_explanation.move_to(explanation_anchor).scale(0.8)
        self.objects["step_explanation"] = step_explanation

        # Additional objects needed for steps 5,6,7 (dynamic triangle, labels)
        # We'll create them as needed during the sequence.

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/slope_rise_over_run/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["axes"]), run_time=2.5)
        remaining_1 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/slope_rise_over_run/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["line_label"], color=BLUE, run_time=1))
        self.play(Create(self.objects["line_graph"]), run_time=3.0)
        remaining_2 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/slope_rise_over_run/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["start_point"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["start_label"]), run_time=3.5)
        remaining_3 = max(0.1, 3.5 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/slope_rise_over_run/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["moving_point"], color=RED, run_time=1))
        self.play(Create(self.objects["moving_point"]), run_time=4.0)
        remaining_4 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5: Move horizontally, draw dashed line, label "run"
        audio_step5 = "media/audio/slope_rise_over_run/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Create horizontal dashed line from (0,-1) to (1,-1)
        h_start = axes.c2p(0, -1)
        h_end = axes.c2p(1, -1)
        h_line = DashedLine(h_start, h_end, color=WHITE, dash_length=0.1)
        self.objects["h_line"] = h_line
        # Create label "run = 1"
        run_label = MathTex(r"\mathrm{run} = 1", color=WHITE, font_size=24)
        run_label.next_to(h_line, DOWN, buff=0.1)
        self.objects["run_label"] = run_label

        self.play(
            self.objects["moving_point"].animate.move_to(h_end),
            Create(h_line),
            Write(run_label),
            run_time=3.0
        )
        remaining_5 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6: Move vertically, draw dashed line, label "rise", complete triangle
        audio_step6 = "media/audio/slope_rise_over_run/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Create vertical dashed line from (1,-1) to (1,1)
        v_start = axes.c2p(1, -1)
        v_end = axes.c2p(1, 1)
        v_line = DashedLine(v_start, v_end, color=WHITE, dash_length=0.1)
        self.objects["v_line"] = v_line
        # Create label "rise = 2"
        rise_label = MathTex(r"\mathrm{rise} = 2", color=WHITE, font_size=24)
        rise_label.next_to(v_line, RIGHT, buff=0.1)
        self.objects["rise_label"] = rise_label
        # Create hypotenuse (solid line from (0,-1) to (1,1))
        hyp_start = axes.c2p(0, -1)
        hyp_end = axes.c2p(1, 1)
        hyp_line = Line(hyp_start, hyp_end, color=GREEN, stroke_width=3)
        self.objects["hyp_line"] = hyp_line

        self.play(
            self.objects["moving_point"].animate.move_to(v_end),
            Create(v_line),
            Write(rise_label),
            Create(hyp_line),
            run_time=3.0
        )
        remaining_6 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7: Move point further, show pattern, circumscribe line, fade out first triangle
        audio_step7 = "media/audio/slope_rise_over_run/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # Create a second triangle at (1,1) to (2,3) to show repetition
        h2_start = axes.c2p(1, 1)
        h2_end = axes.c2p(2, 1)
        v2_start = axes.c2p(2, 1)
        v2_end = axes.c2p(2, 3)
        h2_line = DashedLine(h2_start, h2_end, color=WHITE, dash_length=0.1)
        v2_line = DashedLine(v2_start, v2_end, color=WHITE, dash_length=0.1)
        hyp2_start = axes.c2p(1, 1)
        hyp2_end = axes.c2p(2, 3)
        hyp2_line = Line(hyp2_start, hyp2_end, color=GREEN, stroke_width=3)
        self.objects["h2_line"] = h2_line
        self.objects["v2_line"] = v2_line
        self.objects["hyp2_line"] = hyp2_line

        # Animate moving point to (2,3) while drawing the second triangle
        self.play(
            self.objects["moving_point"].animate.move_to(v2_end),
            Create(h2_line),
            Create(v2_line),
            Create(hyp2_line),
            run_time=2.0
        )
        self.play(Circumscribe(self.objects["line_graph"], color=GREEN, run_time=1))
        # Fade out the first triangle and its labels
        self.play(
            FadeOut(self.objects["h_line"]),
            FadeOut(self.objects["v_line"]),
            FadeOut(self.objects["hyp_line"]),
            FadeOut(self.objects["run_label"]),
            FadeOut(self.objects["rise_label"]),
            run_time=1.0
        )
        total_anim_time_step7 = 2.0 + 1.0 + 1.0  # move+create + circumscribe + fadeout
        remaining_7 = max(0.1, 4.0 - total_anim_time_step7 + 0.5)
        self.wait(max(0.1, remaining_7))