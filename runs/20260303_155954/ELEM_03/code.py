'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Distinguish area (2D fill) from perimeter (1D boundary) of a rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title and Step Label.
#    - Main Content: [Center y=0] for rectangle, grid, perimeter trace.
#    - Footer Region: [Bottom y=-3.0] for area and perimeter formulas.
# 3. Anti-Overlap Check:
#    - Use VGroup for grid to keep it together.
#    - Position formulas vertically in footer with buff.
#    - Step label updates via ReplacementTransform to avoid clutter.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/area_perimeter_rectangle/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw rectangle.
#    - Step 2: Label dimensions.
#    - Step 3: Update step label, indicate rectangle for area.
#    - Step 4: Create grid of unit squares.
#    - Step 5: Show area formula.
#    - Step 6: Update step label, indicate rectangle for perimeter.
#    - Step 7: Create perimeter dot.
#    - Step 8: Animate dot tracing boundary, growing path.
#    - Step 9: Show perimeter formula.
#    - Step 10: Highlight both formulas.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3 * UP
        content_center = ORIGIN
        footer_anchor = 3 * DOWN
        
        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text
        
        # step_label
        step_label = Text("Step 1: The Rectangle", color=YELLOW, font_size=24)
        step_label.next_to(title_text, DOWN, buff=0.3)
        self.objects["step_label"] = step_label
        
        # rect_outline (Polygon with vertices)
        rect_vertices = [(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0)]
        rect_outline = Polygon(*rect_vertices, color=BLUE, stroke_width=4)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline
        
        # dim_label_w
        dim_label_w = MathTex("4", color=GREEN)
        # Position: next_to bottom side, aligned to center_x offset
        dim_label_w.next_to(rect_outline.get_bottom(), DOWN, buff=0.2)
        dim_label_w.align_to(content_center + 0.5*LEFT, LEFT) # align_to LEFT of a point left of center
        self.objects["dim_label_w"] = dim_label_w
        
        # dim_label_h
        dim_label_h = MathTex("3", color=GREEN)
        dim_label_h.next_to(rect_outline.get_right(), RIGHT, buff=0.2)
        dim_label_h.align_to(content_center + 0.5*UP, UP) # align_to UP of a point above center
        self.objects["dim_label_h"] = dim_label_h
        
        # unit_square_template (will be used to create grid)
        unit_square_template = Square(side_length=1, color=WHITE, fill_opacity=0.0, stroke_width=1, stroke_opacity=0.5)
        unit_square_template.move_to(ORIGIN)
        self.objects["unit_square_template"] = unit_square_template
        
        # area_formula
        area_formula = MathTex(r"\mathrm{Area} = 4 \times 3 = 12\ \mathrm{square units}", color=TEAL, font_size=32)
        area_formula.move_to(footer_anchor + UP*0.5)
        self.objects["area_formula"] = area_formula
        
        # perimeter_formula
        perimeter_formula = MathTex(r"\mathrm{Perimeter} = 2 \times (4 + 3) = 14\ \mathrm{units}", color=ORANGE, font_size=32)
        perimeter_formula.next_to(area_formula, DOWN, buff=0.5)
        self.objects["perimeter_formula"] = perimeter_formula
        
        # perimeter_dot
        perimeter_dot = Dot(radius=0.08, color=RED)
        perimeter_dot.move_to((-2, -1.5, 0))
        self.objects["perimeter_dot"] = perimeter_dot
        
        # perimeter_path (empty VMobject)
        perimeter_path = VMobject(color=ORANGE, stroke_width=6)
        self.objects["perimeter_path"] = perimeter_path
        
        # Create grid VGroup (but not added yet)
        grid = VGroup()
        for row in range(3):  # 3 rows
            for col in range(4):  # 4 columns
                sq = Square(side_length=0.98, color=WHITE, fill_opacity=0.0, stroke_width=1, stroke_opacity=0.5)
                # Position relative to rectangle's bottom-left corner
                sq.move_to((-2 + col + 0.5, -1.5 + row + 0.5, 0))
                grid.add(sq)
        self.objects["grid"] = grid
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/area_perimeter_rectangle/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["rect_outline"]), run_time=2.0)
        remaining_1 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/area_perimeter_rectangle/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Write dim_label_w
        self.play(Write(self.objects["dim_label_w"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/area_perimeter_rectangle/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate rect_outline
        self.play(Indicate(self.objects["rect_outline"], color=YELLOW, run_time=1))
        # Visual action: Update step_label
        step_label_new = Text("Step 2: Area as Unit Squares", color=YELLOW, font_size=24)
        step_label_new.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new))
        self.objects["step_label"] = step_label_new
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)  # Indicate (1) + Transform (~1) = ~2
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/area_perimeter_rectangle/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Animate grid appearance row by row
        grid_animations = []
        for i, square in enumerate(self.objects["grid"]):
            grid_animations.append(Create(square))
        self.play(LaggedStart(*grid_animations, lag_ratio=0.1), run_time=4.0)
        remaining_4 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/area_perimeter_rectangle/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe area_formula
        self.play(Circumscribe(self.objects["area_formula"], color=TEAL, run_time=1))
        # Visual action: Write area_formula
        self.play(Write(self.objects["area_formula"]), run_time=2.0)
        remaining_5 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/area_perimeter_rectangle/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Update step_label
        step_label_new2 = Text("Step 3: The Perimeter", color=YELLOW, font_size=24)
        step_label_new2.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new2))
        self.objects["step_label"] = step_label_new2
        # Visual action: Indicate rect_outline (pulse in orange)
        original_color = self.objects["rect_outline"].get_color()
        self.play(
            self.objects["rect_outline"].animate.set_color(ORANGE).set_stroke(width=6),
            run_time=0.5
        )
        self.play(
            self.objects["rect_outline"].animate.set_color(original_color).set_stroke(width=4),
            run_time=0.5
        )
        remaining_6 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/area_perimeter_rectangle/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["perimeter_dot"]), run_time=1.5)
        remaining_7 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/area_perimeter_rectangle/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Define path vertices (rectangle perimeter)
        path_vertices = [
            (-2, -1.5, 0),  # A (bottom-left)
            (2, -1.5, 0),   # B (bottom-right)
            (2, 1.5, 0),    # C (top-right)
            (-2, 1.5, 0),   # D (top-left)
            (-2, -1.5, 0)   # back to A
        ]
        
        # Animate dot moving along path and path growing
        self.objects["perimeter_path"].set_points_as_corners([path_vertices[0], path_vertices[0]])
        self.add(self.objects["perimeter_path"])
        
        # Create animation for dot and path
        run_time_step8 = 6.0
        self.play(
            MoveAlongPath(self.objects["perimeter_dot"], 
                         Polygon(*path_vertices[:4]),  # Use polygon for path
                         rate_func=linear,
                         run_time=run_time_step8),
            # Animate path growing
            self.objects["perimeter_path"].animate.set_points_as_corners(path_vertices),
            run_time=run_time_step8
        )
        remaining_8 = max(0.1, 6.0 - 6.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/area_perimeter_rectangle/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe perimeter_formula
        self.play(Circumscribe(self.objects["perimeter_formula"], color=ORANGE, run_time=1))
        # Visual action: Write perimeter_formula
        self.play(Write(self.objects["perimeter_formula"]), run_time=3.0)
        remaining_9 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        self.add_sound("media/audio/Draw_a_4x3_rectangle_906c247e22/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/area_perimeter_rectangle/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        # Signal action: Indicate area_formula
        self.play(Indicate(self.objects["area_formula"], color=TEAL, run_time=1))
        # Visual action: Indicate perimeter_formula
        self.play(Indicate(self.objects["perimeter_formula"], color=ORANGE, run_time=1))
        remaining_10 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_10))