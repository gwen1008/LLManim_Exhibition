'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Distinguish area (space inside) from perimeter (distance around) for a 4x3 rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for rectangle and grid
#    - Footer Region: [Bottom y=-3.5] for area and perimeter formulas
# 3. Anti-Overlap Check:
#    - Title at top, formulas at bottom, main content centered. Use LEFT*3 and RIGHT*3 for formulas.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_a_4x3_rectangle_c127261c0e/step_XX.mp3"
# 5. Animation Flow:
#    - Draw rectangle outline.
#    - Fill with grid squares for area.
#    - Show area formula.
#    - Trace perimeter with a dot.
#    - Update perimeter formula stepwise.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        formula_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # rect_outline (Polygon with vertices)
        rect_vertices = [
            np.array([-2, -1.5, 0]),
            np.array([2, -1.5, 0]),
            np.array([2, 1.5, 0]),
            np.array([-2, 1.5, 0])
        ]
        rect_outline = Polygon(*rect_vertices, color=BLUE, stroke_width=6, fill_opacity=0)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline
        
        # area_grid (VGroup of 4x3 unit squares)
        grid = VGroup()
        square_side = 1.0
        for row in range(3):  # 3 rows
            for col in range(4):  # 4 columns
                sq = Square(side_length=square_side, color="#333333", fill_opacity=0.2, stroke_width=1)
                # Position relative to grid center
                sq.move_to(np.array([
                    (col - 1.5) * square_side,
                    (row - 1) * square_side,
                    0
                ]))
                grid.add(sq)
        grid.move_to(content_center)
        self.objects["area_grid"] = grid
        
        # perimeter_dot (will be positioned at start of rectangle path)
        perimeter_dot = Dot(radius=0.08, color=YELLOW)
        # Start at bottom-left corner of rectangle
        perimeter_dot.move_to(rect_outline.get_start())
        self.objects["perimeter_dot"] = perimeter_dot
        
        # perimeter_trace (TracedPath, will be added later with updater)
        # We create it but do not add yet, as it needs the dot to exist.
        perimeter_trace = TracedPath(perimeter_dot.get_center, stroke_color=YELLOW, stroke_width=4)
        self.objects["perimeter_trace"] = perimeter_trace
        
        # area_formula
        area_formula = MathTex(r"A = 4 \times 3 = 12", color=GREEN)
        area_formula.move_to(formula_anchor + 3 * LEFT)
        self.objects["area_formula"] = area_formula
        
        # perimeter_formula (initial "P = ?")
        perimeter_formula = MathTex(r"P = ?", color=YELLOW)
        perimeter_formula.move_to(formula_anchor + 3 * RIGHT)
        self.objects["perimeter_formula"] = perimeter_formula
        
        # We'll also create the updated formulas for later TransformMatchingTex
        perimeter_formula_step2 = MathTex(r"P = 2 \times (4 + 3)", color=YELLOW)
        perimeter_formula_step2.move_to(formula_anchor + 3 * RIGHT)
        self.objects["perimeter_formula_step2"] = perimeter_formula_step2
        
        perimeter_formula_step3 = MathTex(r"P = 14", color=YELLOW)
        perimeter_formula_step3.move_to(formula_anchor + 3 * RIGHT)
        self.objects["perimeter_formula_step3"] = perimeter_formula_step3
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_a_4x3_rectangle_c127261c0e/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["rect_outline"]), run_time=2.0)
        remaining_1 = max(0.1, 4.776 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Draw_a_4x3_rectangle_c127261c0e/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Indicate rect_outline
        self.play(Indicate(self.objects["rect_outline"], color=GREEN, run_time=1))
        # Visual action: Create area_grid
        self.play(Create(self.objects["area_grid"]), run_time=2.0)
        remaining_2 = max(0.1, 6.576 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Draw_a_4x3_rectangle_c127261c0e/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe area_grid
        self.play(Circumscribe(self.objects["area_grid"], color=GREEN, run_time=1))
        # Visual action: Write area_formula
        self.play(Write(self.objects["area_formula"]), run_time=1.5)
        remaining_3 = max(0.1, 10.056 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_a_4x3_rectangle_c127261c0e/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate rect_outline
        self.play(Indicate(self.objects["rect_outline"], color=YELLOW, run_time=1))
        # Visual action: Create perimeter_trace and dot, then move dot along perimeter
        # First, add the trace and dot to the scene
        self.add(self.objects["perimeter_trace"], self.objects["perimeter_dot"])
        # Now animate the dot moving around the rectangle
        # We'll use a ValueTracker to control the dot's position along the perimeter
        perimeter_length = 14.0  # 2*(4+3)
        # Define the path as a function of t from 0 to 1
        def perimeter_path(t):
            # t from 0 to 1, goes around rectangle clockwise starting at bottom-left
            # bottom edge (0 to 4), right edge (4 to 7), top edge (7 to 11), left edge (11 to 14)
            total = perimeter_length
            s = t * total
            if s < 4:  # bottom edge
                x = -2 + s
                y = -1.5
            elif s < 7:  # right edge
                x = 2
                y = -1.5 + (s - 4)
            elif s < 11:  # top edge
                x = 2 - (s - 7)
                y = 1.5
            else:  # left edge
                x = -2
                y = 1.5 - (s - 11)
            return np.array([x, y, 0])
        
        # Use a ValueTracker for the parameter t
        t_tracker = ValueTracker(0)
        # Updater for the dot
        self.objects["perimeter_dot"].add_updater(
            lambda d: d.move_to(perimeter_path(t_tracker.get_value()))
        )
        # Animate the dot moving around the rectangle
        self.play(t_tracker.animate.set_value(1), run_time=4.0, rate_func=linear)
        # Remove updater after animation
        self.objects["perimeter_dot"].clear_updaters()
        remaining_4 = max(0.1, 6.192 - 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Draw_a_4x3_rectangle_c127261c0e/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate perimeter_formula
        self.play(Indicate(self.objects["perimeter_formula"], color=YELLOW, run_time=1))
        # Visual action: TransformMatchingTex from "P = ?" to "P = 2 × (4 + 3)"
        self.play(TransformMatchingTex(
            self.objects["perimeter_formula"],
            self.objects["perimeter_formula_step2"]
        ), run_time=1.5)
        remaining_5 = max(0.1, 7.008 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/Draw_a_4x3_rectangle_c127261c0e/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe perimeter_trace
        self.play(Circumscribe(self.objects["perimeter_trace"], color=YELLOW, run_time=1))
        # Visual action: TransformMatchingTex from "P = 2 × (4 + 3)" to "P = 14"
        self.play(TransformMatchingTex(
            self.objects["perimeter_formula_step2"],
            self.objects["perimeter_formula_step3"]
        ), run_time=1.5)
        remaining_6 = max(0.1, 5.616 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Final hold
        self.wait(max(0.1, 2))