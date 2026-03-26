from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors (adjusted for overflow)
        title_anchor = 3.0 * UP  # Changed from 3.5 to 3.0 to prevent overflow
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create Objects from layout_plan.objects
        # title
        title = MathTex(r"y = 2x - 1", color=BLUE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"color": LIGHT_GRAY}
        ).move_to(content_center).scale(0.8)
        self.objects["axes"] = axes

        # y_intercept_point
        y_intercept_point = Dot(radius=0.08, color=YELLOW)
        y_intercept_point.move_to(axes.c2p(0, -1))
        self.objects["y_intercept_point"] = y_intercept_point

        # y_intercept_label
        y_intercept_label = MathTex(r"(0, -1)", color=YELLOW, font_size=30)
        y_intercept_label.next_to(y_intercept_point, LEFT + DOWN, buff=0.3)
        self.objects["y_intercept_label"] = y_intercept_label

        # point_second
        point_second = Dot(radius=0.08, color=GREEN)
        point_second.move_to(axes.c2p(1, 1))
        self.objects["point_second"] = point_second

        # slope_triangle vertices using axes.c2p
        tri_v1 = axes.c2p(0, -1)
        tri_v2 = axes.c2p(1, -1)
        tri_v3 = axes.c2p(1, 1)
        slope_triangle = Polygon(tri_v1, tri_v2, tri_v3, color=TEAL, fill_opacity=0.3, stroke_width=2)
        self.objects["slope_triangle"] = slope_triangle

        # run_arrow
        run_arrow = Arrow(start=axes.c2p(0, -1), end=axes.c2p(1, -1), color=RED, stroke_width=4)
        self.objects["run_arrow"] = run_arrow

        # rise_arrow
        rise_arrow = Arrow(start=axes.c2p(1, -1), end=axes.c2p(1, 1), color=GREEN, stroke_width=4)
        self.objects["rise_arrow"] = rise_arrow

        # line_segment
        line_segment = Line(start=axes.c2p(0, -1), end=axes.c2p(1, 1), color=BLUE, stroke_width=5)
        self.objects["line_segment"] = line_segment

        # line_infinite
        line_infinite = Line(start=axes.c2p(-5, -11), end=axes.c2p(5, 9), color=BLUE, stroke_width=5)
        self.objects["line_infinite"] = line_infinite

        # step_explanation
        step_explanation = Text("Step 1: Introduce the linear function and its graph.", color=WHITE, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["title"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 6.72 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["y_intercept_point"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_2 = max(0.1, 7.704 - 2.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["run_arrow"], color=RED, run_time=1))
        self.play(Create(self.objects["y_intercept_point"]), Write(self.objects["y_intercept_label"]), run_time=2.0)
        remaining_3 = max(0.1, 8.688 - 2.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["rise_arrow"], color=GREEN, run_time=1))
        self.play(Create(self.objects["run_arrow"]), run_time=1.5)
        remaining_4 = max(0.1, 8.52 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["line_segment"], color=BLUE, run_time=1))
        self.play(Create(self.objects["rise_arrow"]), Create(self.objects["point_second"]), run_time=2.0)
        remaining_5 = max(0.1, 7.392 - 2.0 - 1 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # No signal_action for step 6
        self.play(Create(self.objects["slope_triangle"]), run_time=2.0)
        remaining_6 = max(0.1, 9.144 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["slope_triangle"], color=TEAL, run_time=1))
        self.play(Create(self.objects["line_segment"]), run_time=1.5)
        remaining_7 = max(0.1, 9.912 - 1.5 - 1 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        # No signal_action for step 8
        self.play(ReplacementTransform(self.objects["line_segment"], self.objects["line_infinite"]), run_time=3.0)
        remaining_8 = max(0.1, 13.896 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        # No audio for step 9 (duration 2.0, narrative empty)
        # ApplyMethod: slide triangle along the line by (2,4,0)
        shift_vector = axes.c2p(2, 4) - axes.c2p(0, 0)
        self.play(self.objects["slope_triangle"].animate.shift(shift_vector), run_time=2.0)
        self.wait(max(0.1, 0.5))