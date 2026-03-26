from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        title_anchor = 3.5 * UP
        main_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN + 0.5 * UP  # Shift up by 0.5 units

        # Create title
        title = Text("Area vs. Perimeter: A 4x3 Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create rectangle (4x3, centered at origin)
        rect_vertices = [
            np.array([-2, -1.5, 0]),
            np.array([2, -1.5, 0]),
            np.array([2, 1.5, 0]),
            np.array([-2, 1.5, 0])
        ]
        rect = Polygon(*rect_vertices, color=BLUE, stroke_width=4, fill_opacity=0.0)
        rect.move_to(main_anchor)
        self.objects["rect"] = rect

        # Create grid of unit squares (4 columns, 3 rows)
        grid = VGroup()
        square_side = 1.0
        bottom_left = np.array([-2, -1.5, 0])
        for row in range(3):
            for col in range(4):
                sq = Square(side_length=square_side, color=GREEN, fill_opacity=0.3, stroke_width=1)
                sq.move_to(bottom_left + np.array([col * square_side + square_side/2, row * square_side + square_side/2, 0]))
                grid.add(sq)
        grid.move_to(main_anchor)
        self.objects["grid"] = grid

        # Create static perimeter line (initially invisible)
        perimeter_line_static = Polygon(*rect_vertices, color=YELLOW, stroke_width=6, fill_opacity=0.0)
        perimeter_line_static.move_to(main_anchor)
        perimeter_line_static.set_opacity(0)
        self.objects["perimeter_line_static"] = perimeter_line_static

        # Create tracing dot
        tracing_dot = Dot(radius=0.08, color=RED)
        tracing_dot.move_to(rect_vertices[0])
        tracing_dot.set_opacity(0)
        self.objects["tracing_dot"] = tracing_dot

        # Create perimeter label
        perimeter_label = MathTex(r"P = 2(4+3) = 14", color=YELLOW, font_size=36)
        perimeter_label.next_to(rect, RIGHT, buff=1.0)
        self.objects["perimeter_label"] = perimeter_label

        # Create area label
        area_label = MathTex(r"A = 4 \times 3 = 12", color=GREEN, font_size=36)
        area_label.next_to(rect, LEFT, buff=1.0)
        self.objects["area_label"] = area_label

        # Create explanation text
        explanation_text = Text("Let's visualize a 4 by 3 rectangle.", color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence ==========

        # Step 1
        audio_step1 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(title), Write(explanation_text), run_time=1.5)
        self.play(Create(rect), run_time=2.0)
        remaining_1 = max(0.1, 5.568 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Circumscribe(rect, color=GREEN, run_time=1))
        self.play(FadeIn(grid), run_time=2.0)
        remaining_2 = max(0.1, 9.816 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(rect, color=YELLOW, run_time=1))
        self.play(perimeter_line_static.animate.set_opacity(1), run_time=1.5)
        remaining_3 = max(0.1, 7.968 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        perimeter_path = rect_vertices + [rect_vertices[0]]
        total_length = 0
        segment_lengths = []
        for i in range(len(perimeter_path)-1):
            seg_len = np.linalg.norm(perimeter_path[i+1] - perimeter_path[i])
            segment_lengths.append(seg_len)
            total_length += seg_len

        progress_tracker = ValueTracker(0)
        tracing_dot.set_opacity(1)

        def get_dot_position():
            prog = progress_tracker.get_value()
            accumulated = 0
            for i in range(len(segment_lengths)):
                if prog <= accumulated + segment_lengths[i]:
                    t = (prog - accumulated) / segment_lengths[i]
                    start = perimeter_path[i]
                    end = perimeter_path[i+1]
                    return start + t * (end - start)
                accumulated += segment_lengths[i]
            return perimeter_path[-1]

        def get_perimeter_line():
            prog = progress_tracker.get_value()
            points = [perimeter_path[0]]
            accumulated = 0
            for i in range(len(segment_lengths)):
                if prog < accumulated:
                    break
                elif prog <= accumulated + segment_lengths[i]:
                    t = (prog - accumulated) / segment_lengths[i]
                    start = perimeter_path[i]
                    end = perimeter_path[i+1]
                    points.append(start + t * (end - start))
                    break
                else:
                    points.append(perimeter_path[i+1])
                accumulated += segment_lengths[i]
            return Polygon(*points, color=YELLOW, stroke_width=6, fill_opacity=0.0)

        dynamic_perimeter_line = always_redraw(get_perimeter_line)
        tracing_dot.add_updater(lambda d: d.move_to(get_dot_position()))

        self.add(dynamic_perimeter_line, tracing_dot)
        self.play(ReplacementTransform(perimeter_line_static, dynamic_perimeter_line), run_time=0.5)

        trace_time = 6.0
        self.play(progress_tracker.animate.set_value(total_length), run_time=trace_time, rate_func=linear)
        remaining_4 = max(0.1, 8.208 - 0.5 - trace_time + 0.5)
        self.wait(max(0.1, remaining_4))

        tracing_dot.clear_updaters()

        # Step 5
        audio_step5 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        new_explanation = Text("Perimeter is distance around. Area is space inside.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(explanation_text, new_explanation), run_time=1.0)
        self.play(Write(perimeter_label), Write(area_label), run_time=2.5)
        remaining_5 = max(0.1, 11.04 - 1.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.wait(max(0.1, 2))