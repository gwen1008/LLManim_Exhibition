'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the graph of a linear function y=2x-1 and deriving its slope using a slope triangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for coordinate plane, line, and slope triangle
#    - Footer Region: [Bottom y=-3.0] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use distinct zones. The slope formula is placed in the upper left of the graph area to avoid overlapping the main line and triangle.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create coordinate plane.
#    - Step 2: Show y-intercept dot and label.
#    - Step 3: Draw the line.
#    - Step 4: Draw horizontal run segment of slope triangle.
#    - Step 5: Draw vertical rise segment of slope triangle.
#    - Step 6: Label run and rise.
#    - Step 7: Transform labels into slope formula.
#    - Step 8: Hold final frame.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.0 * UP
        graph_anchor = ORIGIN
        explanation_anchor = 3.0 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Graphing the Line: y = 2x - 1", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # plane
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=9,
            y_length=6,
            stroke_opacity=0.5,
            axis_config={"stroke_opacity": 1}
        )
        plane.move_to(graph_anchor)
        self.objects["plane"] = plane

        # y_intercept_dot
        y_intercept_dot = Dot(radius=0.08, color=YELLOW, fill_opacity=1)
        y_intercept_dot.move_to(graph_anchor + np.array([0, -1, 0]))
        self.objects["y_intercept_dot"] = y_intercept_dot

        # y_intercept_label
        y_intercept_label = MathTex("(0, -1)", color=YELLOW, font_size=24)
        y_intercept_label.next_to(y_intercept_dot, RIGHT, buff=0.2)
        self.objects["y_intercept_label"] = y_intercept_label

        # line
        line = FunctionGraph(
            lambda x: 2*x - 1,
            x_range=[-4, 4],
            color=BLUE,
            stroke_width=4
        )
        line.move_to(graph_anchor)
        self.objects["line"] = line

        # slope_triangle_horizontal
        slope_triangle_horizontal = Line(
            start=[0, -1, 0],
            end=[1, -1, 0],
            color=GREEN,
            stroke_width=6
        )
        slope_triangle_horizontal.move_to(graph_anchor + np.array([0, -1, 0]))
        self.objects["slope_triangle_horizontal"] = slope_triangle_horizontal

        # slope_triangle_vertical
        slope_triangle_vertical = Line(
            start=[1, -1, 0],
            end=[1, 1, 0],
            color=RED,
            stroke_width=6
        )
        slope_triangle_vertical.move_to(graph_anchor + np.array([1, -1, 0]))
        self.objects["slope_triangle_vertical"] = slope_triangle_vertical

        # label_run
        label_run = MathTex(r"\text{run}=1", color=GREEN, font_size=24)
        label_run.next_to(slope_triangle_horizontal, DOWN, buff=0.1)
        self.objects["label_run"] = label_run

        # label_rise
        label_rise = MathTex(r"\text{rise}=2", color=RED, font_size=24)
        label_rise.next_to(slope_triangle_vertical, RIGHT, buff=0.1)
        self.objects["label_rise"] = label_rise

        # slope_formula
        slope_formula = MathTex(
            r"\text{slope} = \frac{\text{rise}}{\text{run}} = \frac{2}{1} = 2",
            color=ORANGE,
            font_size=30
        )
        slope_formula.move_to(graph_anchor + np.array([-3, 2, 0]))
        self.objects["slope_formula"] = slope_formula

        # step_explanation
        step_explanation = Text(
            "Step 1: Set up the coordinate plane and identify the y-intercept.",
            color=GRAY_B,
            font_size=24
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.play(Create(self.objects["plane"]))
        self.objects["step_explanation"].set_text("Step 1: Set up the coordinate plane and identify the y-intercept.")
        self.play(Write(self.objects["step_explanation"]))
        animation_time = 1.0 + 1.0  # Create plane + Write text
        remaining = 6.816 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.objects["step_explanation"].set_text("Step 2: The y-intercept is at (0, -1).")
        self.play(Transform(self.objects["step_explanation"], self.objects["step_explanation"].copy()))
        # Simulating check for signal_action - variable 'step' is not defined in this scope
        # Since we don't have a steps list, we'll remove the conditional or use a placeholder
        self.play(Indicate(self.objects["y_intercept_dot"], color=YELLOW))
        self.play(
            AnimationGroup(
                Create(self.objects["y_intercept_dot"]),
                Write(self.objects["y_intercept_label"])
            )
        )
        animation_time = 1.0 + 2.0  # Transform text + Indicate + Create dot and label
        remaining = 7.152 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.objects["step_explanation"].set_text("Step 3: Draw the line y = 2x - 1.")
        self.play(Transform(self.objects["step_explanation"], self.objects["step_explanation"].copy()))
        self.play(Create(self.objects["line"]))
        animation_time = 1.0 + 2.0  # Transform text + Create line
        remaining = 7.68 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.objects["step_explanation"].set_text("Step 4: The slope is 2. Move 1 unit right (run=1).")
        self.play(Transform(self.objects["step_explanation"], self.objects["step_explanation"].copy()))
        # Simulating check for signal_action - variable 'step' is not defined in this scope
        self.play(Indicate(self.objects["slope_triangle_horizontal"], color=GREEN))
        self.play(Create(self.objects["slope_triangle_horizontal"]))
        animation_time = 1.0 + 1.0 + 1.0  # Transform text + Indicate + Create horizontal
        remaining = 9.888 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.objects["step_explanation"].set_text("Step 5: For that run, the line rises by 2 units.")
        self.play(Transform(self.objects["step_explanation"], self.objects["step_explanation"].copy()))
        # Simulating check for signal_action - variable 'step' is not defined in this scope
        self.play(Indicate(self.objects["slope_triangle_vertical"], color=RED))
        self.play(Create(self.objects["slope_triangle_vertical"]))
        animation_time = 1.0 + 1.0 + 1.0  # Transform text + Indicate + Create vertical
        remaining = 6.528 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.objects["step_explanation"].set_text("Step 6: Label the run and rise.")
        self.play(Transform(self.objects["step_explanation"], self.objects["step_explanation"].copy()))
        self.play(
            AnimationGroup(
                Write(self.objects["label_run"]),
                Write(self.objects["label_rise"])
            )
        )
        animation_time = 1.0 + 1.0  # Transform text + Write labels
        remaining = 4.584 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 7
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.objects["step_explanation"].set_text("Step 7: Slope = rise / run = 2 / 1 = 2.")
        self.play(Transform(self.objects["step_explanation"], self.objects["step_explanation"].copy()))
        # Simulating check for signal_action - variable 'step' is not defined in this scope
        self.play(Circumscribe(self.objects["slope_triangle_horizontal"], color=YELLOW, run_time=1))
        # Prepare for transformation: create a temporary group of source labels
        source_group = VGroup(self.objects["label_run"], self.objects["label_rise"])
        # We'll transform them into the slope_formula. Ensure slope_formula is at the right place but invisible initially.
        self.objects["slope_formula"].set_opacity(0)
        self.add(self.objects["slope_formula"])
        self.play(
            TransformMatchingTex(
                source_group,
                self.objects["slope_formula"],
                path_arc=90
            )
        )
        self.objects["slope_formula"].set_opacity(1)
        animation_time = 1.0 + 1.0 + 2.0  # Transform text + Circumscribe + TransformMatchingTex
        remaining = 7.368 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 8
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)

        self.objects["step_explanation"].set_text("Step 8: The slope triangle confirms the slope is 2.")
        self.play(Transform(self.objects["step_explanation"], self.objects["step_explanation"].copy()))
        # Simulating check for signal_action - variable 'step' is not defined in this scope
        self.play(Indicate(self.objects["slope_formula"], color=ORANGE))
        animation_time = 1.0 + 1.0  # Transform text + Indicate
        remaining = 9.552 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))