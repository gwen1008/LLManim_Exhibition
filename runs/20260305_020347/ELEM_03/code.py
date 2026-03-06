'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Distinguish area (covering) from perimeter (boundary length) for a rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for rectangle, grid, and perimeter trace
#    - Footer Region: [Bottom y=-3.5] for area and perimeter formulas
# 3. Anti-Overlap Check:
#    - The rectangle and its grid will be centered at ORIGIN.
#    - Footer formulas will be placed at y=-2.5 and y=-3.0, well below the main visual.
#    - Labels for length/width will be placed just outside the rectangle.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Draw rectangle.
#    - Step 2: Label dimensions.
#    - Step 3: Fill with grid of unit squares.
#    - Step 4: Show area formula.
#    - Step 5: Create trace dot.
#    - Step 6: Animate dot tracing perimeter, drawing line.
#    - Step 7: Show perimeter formula.
#    - Step 8: Final emphasis.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # rect_main
        rect_main = Rectangle(width=4, height=3, color=BLUE, stroke_width=4, fill_opacity=0.0)
        rect_main.move_to(content_center)
        self.objects["rect_main"] = rect_main

        # label_length
        label_length = MathTex("4", color=GREEN)
        label_length.next_to(rect_main.get_right(), RIGHT, buff=0.2)
        self.objects["label_length"] = label_length

        # label_width
        label_width = MathTex("3", color=GREEN)
        label_width.next_to(rect_main.get_top(), UP, buff=0.2)
        self.objects["label_width"] = label_width

        # grid_unit_square (template, will be duplicated)
        grid_unit_square = Square(side_length=1, color="#333333", stroke_width=1, fill_opacity=0.0, stroke_opacity=0.5)
        # Initial position as per JSON, but grid will be built relative to rectangle later
        grid_unit_square.move_to(content_center + LEFT*1.5 + DOWN*1.0)
        self.objects["grid_unit_square"] = grid_unit_square

        # trace_dot
        trace_dot = Dot(radius=0.05, color=YELLOW)
        trace_dot.move_to(rect_main.get_corner(DL))
        self.objects["trace_dot"] = trace_dot

        # perimeter_line (initialize as empty VMobject)
        perimeter_line = VMobject(color=YELLOW, stroke_width=3)
        perimeter_line.move_to(trace_dot.get_center())
        self.objects["perimeter_line"] = perimeter_line

        # footer_area_formula
        footer_area_formula = Tex(r"Area $= \mathrm{Length} \times \mathrm{Width} = 4 \times 3 = 12$", color=BLUE, font_size=30)
        footer_area_formula.move_to(footer_anchor + UP*0.5)
        self.objects["footer_area_formula"] = footer_area_formula

        # footer_perimeter_formula
        footer_perimeter_formula = Tex(r"Perimeter $= 4 + 3 + 4 + 3 = 14$", color=YELLOW, font_size=30)
        footer_perimeter_formula.next_to(footer_area_formula, DOWN, buff=0.5)
        self.objects["footer_perimeter_formula"] = footer_perimeter_formula

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_00.mp3")  # [auto-injected] duration=5.04s
        _audio_dur_0 = 5.04  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(self.objects["rect_main"]), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_01.mp3")  # [auto-injected] duration=5.95s
        _audio_dur_1 = 5.95  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Indicate(self.objects["rect_main"], color=GREEN, run_time=1))
        self.play(Write(self.objects["label_length"]), Write(self.objects["label_width"]), run_time=1.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_02.mp3")  # [auto-injected] duration=10.01s
        _audio_dur_2 = 10.01  # [audio-sync] actual TTS duration
        # Step 3: Create Grid
        # Build 4x3 grid of unit squares inside the rectangle
        grid_group = VGroup()
        rect_corner = rect_main.get_corner(DL)  # Bottom-left corner of rectangle
        for row in range(3):  # height = 3
            for col in range(4):  # length = 4
                sq = Square(side_length=1, color="#333333", stroke_width=1, fill_opacity=0.0, stroke_opacity=0.5)
                # Position each square relative to the rectangle's bottom-left corner
                sq.move_to(rect_corner + RIGHT * (col + 0.5) + UP * (row + 0.5))
                grid_group.add(sq)
        # Animate all squares appearing at once (fade in)
        self.play(FadeIn(grid_group), run_time=2.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_03.mp3")  # [auto-injected] duration=9.70s
        _audio_dur_3 = 9.70  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Circumscribe(self.objects["rect_main"], color=BLUE, run_time=1))
        self.play(Write(self.objects["footer_area_formula"]), run_time=2.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_04.mp3")  # [auto-injected] duration=7.10s
        _audio_dur_4 = 7.10  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Create(self.objects["trace_dot"]), run_time=1.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_05.mp3")  # [auto-injected] duration=8.16s
        _audio_dur_5 = 8.16  # [audio-sync] actual TTS duration
        # Step 6: Animate Perimeter Trace
        # Get rectangle corners
        corners = [
            rect_main.get_corner(DL),
            rect_main.get_corner(DR),
            rect_main.get_corner(UR),
            rect_main.get_corner(UL),
            rect_main.get_corner(DL)  # return to start to close the path
        ]
        # Create the perimeter line by animating the dot and building the line segment by segment
        self.play(Indicate(self.objects["rect_main"], color=YELLOW, run_time=1))
        # We'll animate the dot moving and simultaneously draw the line
        # First, add the perimeter_line to the scene (it's empty initially)
        self.add(self.objects["perimeter_line"])
        # Define the line's points
        line_points = []
        # Animate dot moving along each side
        run_time_per_side = 1.0  # Total 6 sec for trace, 4 sides -> ~1.5 sec per side
        for i in range(4):
            start_point = corners[i]
            end_point = corners[i+1]
            # Animate dot moving
            self.play(
                self.objects["trace_dot"].animate.move_to(end_point),
                run_time=run_time_per_side,
                rate_func=linear
            )
            # Update the perimeter_line to include the new segment
            line_points.append(start_point)
            line_points.append(end_point)
            new_line = VMobject(color=YELLOW, stroke_width=3)
            new_line.set_points_as_corners(line_points)
            self.play(Transform(self.objects["perimeter_line"], new_line), run_time=0.1)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_06.mp3")  # [auto-injected] duration=4.22s
        _audio_dur_6 = 4.22  # [audio-sync] actual TTS duration
        # Step 7
        self.play(Circumscribe(self.objects["perimeter_line"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["footer_perimeter_formula"]), run_time=1.5)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c6b256a552/step_07.mp3")  # [auto-injected] duration=8.18s
        _audio_dur_7 = 8.18  # [audio-sync] actual TTS duration
        # Step 8
        self.play(Indicate(self.objects["footer_area_formula"], color=BLUE, run_time=1))
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))