'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the concepts of area and perimeter for a rectangle, showing area as covering with unit squares and perimeter as the boundary length.
# 2. Layout Strategy:
#    - Header Region: [y=3.2] for Title and perimeter counter.
#    - Main Content: [Center y=0] for rectangle, grid, and tracing animation.
#    - Footer Region: [Bottom y=-3.0] for area and perimeter formulas.
# 3. Anti-Overlap Check:
#    - Strategy: Keep formulas at bottom left/right, separated by buff. Center main rectangle. Use VGroup for grid.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Draw rectangle and label dimensions.
#    - Fill with grid squares for area.
#    - Show area formula.
#    - Show perimeter formula.
#    - Animate tracing the perimeter with a live counter.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.2 * UP
        content_center = ORIGIN
        formula_anchor = 3.0 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # rect_outline (Polygon with 4 points)
        rect_points = [
            np.array([-2, -1.5, 0]),
            np.array([2, -1.5, 0]),
            np.array([2, 1.5, 0]),
            np.array([-2, 1.5, 0])
        ]
        rect_outline = Polygon(*rect_points, color=BLUE, stroke_width=4)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline

        # label_length
        label_length = MathTex("4", color=YELLOW)
        label_length.next_to(rect_outline.get_bottom(), DOWN, buff=0.2)
        label_length.set_x(0)
        self.objects["label_length"] = label_length

        # label_width
        label_width = MathTex("3", color=YELLOW)
        label_width.next_to(rect_outline.get_right(), RIGHT, buff=0.2)
        label_width.set_y(0)
        self.objects["label_width"] = label_width

        # grid_squares (VGroup of 12 squares, 4 columns, 3 rows)
        grid_squares = VGroup()
        side_len = 0.8
        start_x = -1.6
        start_y = -1.2
        for row in range(3):
            for col in range(4):
                sq = Square(side_length=side_len, color=GREEN, fill_opacity=0.5, stroke_width=1)
                sq.move_to([start_x + col * side_len, start_y + row * side_len, 0])
                grid_squares.add(sq)
        grid_squares.move_to(content_center)
        self.objects["grid_squares"] = grid_squares

        # perimeter_tracer (initial line of zero length)
        perimeter_tracer = Line(
            start=np.array([-2, -1.5, 0]),
            end=np.array([-2, -1.5, 0]),
            color=RED,
            stroke_width=6
        )
        perimeter_tracer.move_to(content_center)
        self.objects["perimeter_tracer"] = perimeter_tracer

        # tracer_dot
        tracer_dot = Dot(radius=0.08, color=RED)
        tracer_dot.move_to(perimeter_tracer.get_start())
        self.objects["tracer_dot"] = tracer_dot

        # area_formula
        area_formula = Tex(
            r"Area $= \mathrm{length} \times \mathrm{width} = 4 \times 3 = 12$",
            color=GREEN,
            font_size=30
        )
        area_formula.move_to(formula_anchor)
        area_formula.set_x(-3.0)
        self.objects["area_formula"] = area_formula

        # perimeter_formula
        perimeter_formula = Tex(
            r"Perimeter $= 2\times(\mathrm{length}+\mathrm{width}) = 2\times(4+3) = 14$",
            color=RED,
            font_size=30
        )
        perimeter_formula.next_to(area_formula, RIGHT, buff=1.5)
        self.objects["perimeter_formula"] = perimeter_formula

        # perimeter_counter
        perimeter_counter = Tex("P = 0", color=RED, font_size=28)
        perimeter_counter.next_to(title, DOWN, buff=0.5)
        self.objects["perimeter_counter"] = perimeter_counter

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_00.mp3")  # [auto-injected] duration=5.78s
        _audio_dur_0 = 5.78  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(self.objects["rect_outline"]), run_time=2.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_01.mp3")  # [auto-injected] duration=4.92s
        _audio_dur_1 = 4.92  # [audio-sync] actual TTS duration
        # Step 2
        # signal_action: Write label_length
        self.play(Write(self.objects["label_length"]), run_time=1.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_02.mp3")  # [auto-injected] duration=2.18s
        _audio_dur_2 = 2.18  # [audio-sync] actual TTS duration
        # Step 3
        # signal_action: Write label_width
        self.play(Write(self.objects["label_width"]), run_time=1.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_03.mp3")  # [auto-injected] duration=9.53s
        _audio_dur_3 = 9.53  # [audio-sync] actual TTS duration
        # Step 4
        # signal_action: Indicate rect_outline
        self.play(Indicate(self.objects["rect_outline"], color=YELLOW, run_time=1))
        # visual_action: Create grid_squares (row by row for clarity)
        # We'll create the grid row by row
        rows = []
        for i in range(3):
            row = VGroup(*[self.objects["grid_squares"][j] for j in range(i*4, (i+1)*4)])
            rows.append(row)
        anim_time_per_row = 4.0 / 3.0
        for row in rows:
            self.play(Create(row), run_time=anim_time_per_row)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_04.mp3")  # [auto-injected] duration=5.71s
        _audio_dur_4 = 5.71  # [audio-sync] actual TTS duration
        # Step 5
        # signal_action: Circumscribe grid_squares
        self.play(Circumscribe(self.objects["grid_squares"], color=GREEN, run_time=1))
        # visual_action: Write area_formula
        self.play(Write(self.objects["area_formula"]), run_time=3.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_05.mp3")  # [auto-injected] duration=8.57s
        _audio_dur_5 = 8.57  # [audio-sync] actual TTS duration
        # Step 6
        # signal_action: Indicate rect_outline
        self.play(Indicate(self.objects["rect_outline"], color=RED, run_time=1))
        # visual_action: Write perimeter_formula
        self.play(Write(self.objects["perimeter_formula"]), run_time=3.5)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_06.mp3")  # [auto-injected] duration=6.72s
        _audio_dur_6 = 6.72  # [audio-sync] actual TTS duration
        # Step 7
        # visual_action: Create perimeter_counter
        self.play(Write(self.objects["perimeter_counter"]), run_time=2.0)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Draw_a_4x3_rectangle_c127261c0e/step_07.mp3")  # [auto-injected] duration=7.75s
        _audio_dur_7 = 7.75  # [audio-sync] actual TTS duration
        # Step 8: AnimatePerimeterTrace
        # We'll animate the perimeter_tracer line and tracer_dot along the rectangle boundary.
        # Path: start at (-2,-1.5) -> up to (-2,1.5) -> across to (2,1.5) -> down to (2,-1.5) -> back to start.
        # Total perimeter = 14 units.
        # We'll use a ValueTracker for the progress and update the line and dot via always_redraw.
        progress = ValueTracker(0)
        total_perimeter = 14.0
        vertices = [
            np.array([-2, -1.5, 0]),  # bottom-left
            np.array([-2, 1.5, 0]),   # top-left
            np.array([2, 1.5, 0]),    # top-right
            np.array([2, -1.5, 0]),   # bottom-right
            np.array([-2, -1.5, 0])   # back to start
        ]
        side_lengths = [3, 4, 3, 4]  # up, right, down, left

        # Function to get current point along perimeter based on progress
        def get_point_on_perimeter(prog):
            remaining = prog
            for i in range(4):
                if remaining <= side_lengths[i]:
                    t = remaining / side_lengths[i]
                    return vertices[i] + t * (vertices[i+1] - vertices[i])
                remaining -= side_lengths[i]
            return vertices[-1]

        # Create always_redraw objects for tracer and dot
        perimeter_tracer_redraw = always_redraw(lambda: Line(
            vertices[0], 
            get_point_on_perimeter(progress.get_value()), 
            color=RED, 
            stroke_width=6
        ))
        
        tracer_dot_redraw = always_redraw(lambda: Dot(
            radius=0.08, 
            color=RED
        ).move_to(get_point_on_perimeter(progress.get_value())))
        
        # Update perimeter_counter text using always_redraw
        perimeter_counter_redraw = always_redraw(lambda: Tex(f"P = {int(progress.get_value())}", color=RED, font_size=28).next_to(self.objects["title"], DOWN, buff=0.5))
        
        # Remove old objects and add new redrawn ones
        self.remove(self.objects["perimeter_tracer"], self.objects["tracer_dot"], self.objects["perimeter_counter"])
        self.add(perimeter_tracer_redraw, tracer_dot_redraw, perimeter_counter_redraw)
        self.objects["perimeter_tracer"] = perimeter_tracer_redraw
        self.objects["tracer_dot"] = tracer_dot_redraw
        self.objects["perimeter_counter"] = perimeter_counter_redraw

        # Animate the progress from 0 to 14
        self.play(progress.animate.set_value(total_perimeter), run_time=8.0, rate_func=linear)

        # No need to remove updaters since we used always_redraw
        # The objects will continue to update, but we can leave them as is
        # No need to remove updater from perimeter_counter_redraw as always_redraw handles it

        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))