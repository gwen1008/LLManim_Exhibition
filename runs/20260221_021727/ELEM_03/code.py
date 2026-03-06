'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the difference between area (space inside) and perimeter (distance around) for a 4x3 rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for rectangle and grid
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Place labels (area, perimeter) below the rectangle in a vertical stack using `next_to` with buff.
#    - The grid and rectangle share the same center.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw rectangle outline (perimeter).
#    - Step 2: Indicate rectangle, then fill with unit squares (area).
#    - Step 3: Write area label.
#    - Step 4: Write perimeter label.
#    - Step 5: Indicate rectangle, then trace perimeter with a yellow flash.
#    - Step 6: Show bottom explanation.
'''

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
        title = Text("Area and Perimeter of a 4x3 Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create rectangle outline (perimeter boundary)
        rect_outline = Rectangle(width=4, height=3, color=BLUE, stroke_width=6, fill_opacity=0.0)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline

        # Create grid of 12 unit squares
        grid_squares = VGroup()
        for h in range(3):  # 3 rows
            for w in range(4):  # 4 columns
                sq = Square(side_length=1.0, color=GREEN, fill_opacity=0.3, stroke_width=2)
                # Position relative to grid center
                sq.move_to([w - 1.5, h - 1.0, 0])  # Centers the 4x3 grid at origin
                grid_squares.add(sq)
        grid_squares.move_to(content_center)
        self.objects["grid_squares"] = grid_squares

        # Create area label
        area_label = MathTex(r"\text{Area} = 12 \text{ square units}", color=GREEN, font_size=30)
        area_label.next_to(rect_outline, DOWN, buff=0.8)
        self.objects["area_label"] = area_label

        # Create perimeter label
        perimeter_label = MathTex(r"\text{Perimeter} = 14 \text{ units}", color=BLUE, font_size=30)
        perimeter_label.next_to(area_label, DOWN, buff=0.5)
        self.objects["perimeter_label"] = perimeter_label

        # Create explanation text
        explanation_text = Text("Perimeter is the distance around. Area is the space inside.", color=GRAY_B, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # Create tracer line (a copy of rectangle for ShowPassingFlash)
        tracer_line = Rectangle(width=4, height=3, color=YELLOW, stroke_width=8, fill_opacity=0.0)
        tracer_line.move_to(content_center)
        self.objects["tracer_line"] = tracer_line

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["rect_outline"]))
        self.wait(max(0.1, max(0.1, 7.488 - 1.0)))  # Create run_time default ~1.0

        # Step 2
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate rectangle
        self.play(Indicate(self.objects["rect_outline"], color=GREEN))
        # Visual action: Create grid squares (with slight stagger)
        self.play(LaggedStart(*[FadeIn(sq) for sq in self.objects["grid_squares"]], lag_ratio=0.05))
        self.wait(max(0.1, max(0.1, 8.448 - 1.0 - 1.0)))  # Indicate ~1.0, LaggedStart ~1.0

        # Step 3
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Write area_label (already part of visual action)
        # Visual action: Write area label
        self.play(Write(self.objects["area_label"]))
        self.wait(max(0.1, max(0.1, 10.752 - 1.0)))  # Write run_time default ~1.0

        # Step 4
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Write perimeter_label (already part of visual action)
        # Visual action: Write perimeter label
        self.play(Write(self.objects["perimeter_label"]))
        self.wait(max(0.1, max(0.1, 4.128 - 1.0)))  # Write run_time default ~1.0

        # Step 5
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate rectangle
        self.play(Indicate(self.objects["rect_outline"], color=YELLOW))
        # Visual action: ShowPassingFlash on tracer line
        self.play(ShowPassingFlash(self.objects["tracer_line"].copy().set_stroke(width=10), time_width=0.5))
        self.wait(max(0.1, max(0.1, 6.264 - 1.0 - 1.0)))  # Indicate ~1.0, ShowPassingFlash ~1.0

        # Step 6
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Visual action: FadeIn explanation text
        self.play(FadeIn(self.objects["explanation_text"]))
        self.wait(max(0.1, max(0.1, 6.792 - 1.0)))  # FadeIn run_time default ~1.0

        # Final hold
        self.wait(max(0.1, 2))