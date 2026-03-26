'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize area as count of unit squares and perimeter as boundary length for a 4x3 rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and dimension label.
#    - Main Content: [Center y=0] for rectangle, grid, dot, and perimeter counter.
#    - Footer Region: [Bottom y=-3.5] for step explanation text.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for grid squares. Position counter above rectangle with buff.
#    - Keep explanation text at bottom, title at top, main content centered.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/area_perimeter_rectangle/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw rectangle outline.
#    - Step 2: Indicate dimension label, then fill rectangle with 12 blue squares row by row.
#    - Step 3: Circumscribe outline, show perimeter counter.
#    - Step 4: Indicate dot, create it, animate it moving around perimeter while updating counter.
#    - Step 5: Indicate counter, morph dimension label into perimeter formula.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor).shift(UP * 0.2)
        self.objects["title"] = title
        
        # dim_label
        dim_label = MathTex("4 \\times 3", color=YELLOW)
        dim_label.next_to(title, DOWN, buff=0.3)
        self.objects["dim_label"] = dim_label
        
        # rect_outline
        rect_outline = Rectangle(width=3.2, height=2.4, color=WHITE, stroke_width=4, fill_opacity=0)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline
        
        # area_grid (empty VGroup, will be populated later)
        area_grid = VGroup()
        area_grid.move_to(content_center)
        self.objects["area_grid"] = area_grid
        
        # perimeter_dot (position set later)
        perimeter_dot = Dot(radius=0.08, color="#FF5555")
        # Initial position set in step 4
        self.objects["perimeter_dot"] = perimeter_dot
        
        # perimeter_counter
        perimeter_counter = DecimalNumber(0, color="#FFAA00", num_decimal_places=0)
        perimeter_counter.next_to(rect_outline, UP, buff=0.7)
        self.objects["perimeter_counter"] = perimeter_counter
        
        # counter_label
        counter_label = Text("Perimeter:", color="#FFAA00", font_size=24)
        counter_label.next_to(perimeter_counter, LEFT, buff=0.3)
        self.objects["counter_label"] = counter_label
        
        # step_explanation
        step_explanation = Text("Step 1: Draw a 4-unit by 3-unit rectangle.", color="#CCCCCC", font_size=26)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/area_perimeter_rectangle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), Write(self.objects["dim_label"]), Write(self.objects["step_explanation"]), run_time=0.5)
        self.play(Create(self.objects["rect_outline"]), run_time=2.0)
        remaining_1 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/area_perimeter_rectangle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Indicate dim_label
        self.play(Indicate(self.objects["dim_label"], color=YELLOW, run_time=1))
        
        # Visual action: Create 12 filled squares inside rectangle
        # Rectangle dimensions: width=3.2, height=2.4 → unit square side = 0.8
        side = 0.8
        cols, rows = 4, 3
        squares = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(side_length=side, color=BLUE_D, fill_opacity=0.7, stroke_width=2)
                # Position relative to rectangle center
                x_offset = (c - (cols-1)/2) * side
                y_offset = (r - (rows-1)/2) * side
                sq.move_to(self.objects["rect_outline"].get_center() + np.array([x_offset, y_offset, 0]))
                squares.add(sq)
        # Add squares to area_grid VGroup
        self.objects["area_grid"].add(*squares)
        
        # Animate creation row by row
        anims = []
        for i, sq in enumerate(squares):
            anims.append(Create(sq))
        self.play(LaggedStart(*anims, lag_ratio=0.1), run_time=3.0)
        remaining_2 = max(0.1, 5.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/area_perimeter_rectangle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe rect_outline
        self.play(Circumscribe(self.objects["rect_outline"], color=GREEN, run_time=1))
        
        # Update step explanation
        new_explanation = Text("Step 3: The perimeter is the distance around the outside.", color="#CCCCCC", font_size=26)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Visual action: FadeIn perimeter_counter and label
        self.play(FadeIn(self.objects["counter_label"]), FadeIn(self.objects["perimeter_counter"]), run_time=1.5)
        remaining_3 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/area_perimeter_rectangle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate perimeter_dot
        # First position the dot
        self.objects["perimeter_dot"].move_to(self.objects["rect_outline"].get_corner(DL))
        self.play(Indicate(self.objects["perimeter_dot"], color=RED, run_time=1))
        
        # Update step explanation
        new_explanation2 = Text("Step 4: Travel around the boundary to measure it.", color="#CCCCCC", font_size=26)
        new_explanation2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation2))
        self.objects["step_explanation"] = new_explanation2
        
        # Visual action: Create dot and animate along perimeter
        self.play(Create(self.objects["perimeter_dot"]), run_time=0.5)
        
        # Create perimeter path (rectangle vertices)
        rect = self.objects["rect_outline"]
        corners = [
            rect.get_corner(DL),
            rect.get_corner(DR),
            rect.get_corner(UR),
            rect.get_corner(UL),
            rect.get_corner(DL)
        ]
        # Use ValueTracker for animation
        t = ValueTracker(0)
        total_perimeter = 14.0  # 2*(4+3) units
        # Updater for dot position
        def update_dot(m):
            # t from 0 to 1
            progress = t.get_value()
            # Map progress to distance along perimeter (0 to total_perimeter)
            dist = progress * total_perimeter
            # Determine which edge and position
            side_lengths = [4, 3, 4, 3]  # unit lengths
            cumulative = 0
            for i, length in enumerate(side_lengths):
                if dist <= cumulative + length:
                    # On this edge
                    local = dist - cumulative
                    alpha = local / length
                    start = corners[i]
                    end = corners[i+1]
                    pos = start + alpha * (end - start)
                    m.move_to(pos)
                    break
                cumulative += length
        self.objects["perimeter_dot"].add_updater(update_dot)
        # Updater for counter
        def update_counter(m):
            m.set_value(t.get_value() * total_perimeter)
        self.objects["perimeter_counter"].add_updater(update_counter)
        
        # Animate dot moving around
        self.add(self.objects["perimeter_dot"], self.objects["perimeter_counter"])
        self.play(t.animate.set_value(1), run_time=7.0, rate_func=linear)
        
        # Remove updaters
        self.objects["perimeter_dot"].clear_updaters()
        self.objects["perimeter_counter"].clear_updaters()
        
        remaining_4 = max(0.1, 8.0 - 7.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/area_perimeter_rectangle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate perimeter_counter
        self.play(Indicate(self.objects["perimeter_counter"], color=YELLOW, run_time=1))
        
        # Update step explanation
        new_explanation3 = Text("Step 5: Perimeter formula: P = 2 × (length + width).", color="#CCCCCC", font_size=26)
        new_explanation3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation3))
        self.objects["step_explanation"] = new_explanation3
        
        # Visual action: Transform dim_label into perimeter formula
        formula = MathTex("P = 2 \\times (4 + 3) = 14", color=YELLOW)
        formula.move_to(self.objects["dim_label"].get_center())
        self.play(TransformMatchingTex(self.objects["dim_label"], formula, path_arc=90), run_time=2.0)
        self.objects["dim_label"] = formula
        
        remaining_5 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))