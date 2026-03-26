'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative of y=0.5x² as the slope of the tangent line, showing the derivative function y'=x.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for axes, curve, tangent line, moving point
#    - Footer Region: [Bottom y=-3.5] for derivative formula and slope display
# 3. Anti-Overlap Check:
#    - Strategy: Keep title at top, main visualization centered, slope display at bottom. Use relative positioning.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/derivative_as_slope/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Create curve, indicate it.
#    - Step 3: Create moving point, circumscribe it.
#    - Step 4: Write derivative formula, indicate it.
#    - Step 5: Create tangent line, indicate it, then animate point movement with always_redraw for tangent and slope value.
'''

from manim import *
import os
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Derivative as Slope: y = 0.5x²", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes
        
        # curve
        curve = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=4)
        self.objects["curve"] = curve
        
        # moving_point (initial position at x=-3, y=4.5)
        moving_point = Dot(radius=0.08, color=YELLOW, fill_opacity=1.0)
        moving_point.move_to(axes.c2p(-3, 4.5))
        self.objects["moving_point"] = moving_point
        
        # tangent_line (initial dummy line, will be updated via always_redraw)
        tangent_line = Line(start=LEFT*2, end=RIGHT*2, color=RED, stroke_width=3)
        tangent_line.move_to(content_center)
        self.objects["tangent_line"] = tangent_line
        
        # slope_formula
        slope_formula = MathTex(r"y' = x", color=GREEN, font_size=32)
        slope_formula.move_to(footer_anchor + LEFT*2.5)
        self.objects["slope_formula"] = slope_formula
        
        # slope_label
        slope_label = Text("Slope =", color=WHITE, font_size=28)
        slope_label.next_to(slope_formula, RIGHT, buff=1.0)
        self.objects["slope_label"] = slope_label
        
        # slope_value
        slope_value = DecimalNumber(0.00, num_decimal_places=2, color=YELLOW, font_size=32)
        slope_value.next_to(slope_label, RIGHT, buff=0.3)
        self.objects["slope_value"] = slope_value
        
        # ValueTracker for x-coordinate of moving point
        x_tracker = ValueTracker(-3.0)
        self.objects["x_tracker"] = x_tracker
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/derivative_as_slope/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/derivative_as_slope/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["curve"], color=BLUE, run_time=1))
        self.play(Create(self.objects["curve"]), run_time=2.0)
        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/derivative_as_slope/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["moving_point"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["moving_point"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/derivative_as_slope/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["slope_formula"], color=GREEN, run_time=1))
        self.play(Write(self.objects["slope_formula"]), run_time=1.5)
        remaining_4 = max(0.1, 4.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/derivative_as_slope/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["tangent_line"], color=RED, run_time=1))
        self.play(Create(self.objects["tangent_line"]), run_time=1.5)
        
        # Now set up always_redraw for moving_point, tangent_line, and slope_value
        x_tracker = self.objects["x_tracker"]
        axes = self.objects["axes"]
        curve = self.objects["curve"]
        
        # Update moving_point position based on x_tracker
        moving_point_updater = always_redraw(
            lambda: self.objects["moving_point"].move_to(
                axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2)
            )
        )
        self.add(moving_point_updater)
        
        # Update tangent_line: line segment of fixed length (2 units) centered at the point
        tangent_line_updater = always_redraw(
            lambda: self.objects["tangent_line"].become(
                Line(
                    start=axes.c2p(x_tracker.get_value() - 1, x_tracker.get_value() - 1 * x_tracker.get_value()),
                    end=axes.c2p(x_tracker.get_value() + 1, x_tracker.get_value() + 1 * x_tracker.get_value()),
                    color=RED,
                    stroke_width=3
                )
            )
        )
        self.add(tangent_line_updater)
        
        # Update slope_value (derivative is x)
        slope_value_updater = always_redraw(
            lambda: self.objects["slope_value"].set_value(x_tracker.get_value())
        )
        self.add(slope_value_updater)
        
        # Also add slope_label and slope_value to scene (they were created but not added)
        self.add(self.objects["slope_label"], self.objects["slope_value"])
        
        # Animate x_tracker from -3 to 3
        self.play(x_tracker.animate.set_value(3.0), run_time=6.0, rate_func=linear)
        remaining_5 = max(0.1, 8.0 - 6.0 + 0.5)
        self.wait(max(0.1, remaining_5))