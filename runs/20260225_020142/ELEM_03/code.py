from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors (zones)
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create title
        title = Text("Area and Perimeter of a 4×3 Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create rectangle (4x3) centered at origin
        rect = Rectangle(width=4, height=3, color=BLUE, stroke_width=4, fill_opacity=0.0)
        rect.move_to(global_center)
        self.objects["rect"] = rect

        # Create grid of unit squares (8 columns, 6 rows, side=0.5)
        grid = VGroup()
        side_length = 0.5
        for row in range(6):  # 3 units tall / 0.5 = 6 rows
            for col in range(8):  # 4 units wide / 0.5 = 8 columns
                # Calculate position relative to rectangle's bottom-left corner
                # Rectangle spans x: -2 to 2, y: -1.5 to 1.5
                # Bottom-left corner of rectangle is at (-2, -1.5, 0)
                x = -2 + col * side_length + side_length / 2
                y = -1.5 + row * side_length + side_length / 2
                sq = Square(side_length=side_length, color=BLUE, fill_opacity=0.0, stroke_width=1, stroke_opacity=0.5)
                sq.move_to(np.array([x, y, 0]))
                grid.add(sq)
        grid.move_to(ORIGIN)  # Ensure center alignment
        self.objects["grid"] = grid

        # Create tracer dot (will be positioned at rectangle start later)
        tracer_dot = Dot(radius=0.05, color=YELLOW)
        # Initial position: bottom-left vertex of rectangle
        tracer_dot.move_to(rect.get_corner(DL))
        self.objects["tracer_dot"] = tracer_dot

        # TracedPath will be created as an updater in Step 2
        self.objects["traced_path"] = None  # Placeholder

        # Create dimension labels
        dim_label_length = MathTex("4", color=GREEN)
        dim_label_length.next_to(rect, DOWN, buff=0.3)
        self.objects["dim_label_length"] = dim_label_length

        dim_label_height = MathTex("3", color=GREEN)
        dim_label_height.next_to(rect, LEFT, buff=0.3)
        self.objects["dim_label_height"] = dim_label_height

        # Create footer text
        footer_text = Text("Perimeter = 2×(4+3) = 14 units | Area = 4×3 = 12 square units", color=GRAY_B, font_size=24)
        footer_text.move_to(footer_anchor + DOWN * 0.5)
        self.objects["footer_text"] = footer_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # signal_action: null
        self.play(Create(self.objects["rect"]), run_time=2.0)
        remaining_1 = max(0.1, 4.776 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # signal_action: Indicate rect with YELLOW
        self.play(Indicate(self.objects["rect"], color=YELLOW, run_time=1))

        # Create TracedPath and add updater
        traced_path = TracedPath(self.objects["tracer_dot"].get_center, stroke_color=YELLOW, stroke_width=6)
        self.objects["traced_path"] = traced_path
        self.add(traced_path)

        # Add tracer dot to scene
        self.play(FadeIn(self.objects["tracer_dot"]))

        # Animate dot moving along rectangle perimeter (closed loop)
        # Use MoveAlongPath with the rectangle itself as the path
        perimeter_path = self.objects["rect"]
        self.play(MoveAlongPath(self.objects["tracer_dot"], perimeter_path, run_time=4.0, rate_func=linear))

        remaining_2 = max(0.1, 7.152 - (1 + 4.0) + 0.5)  # Indicate (1s) + MoveAlongPath (4s)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # signal_action: Circumscribe rect with GREEN
        self.play(Circumscribe(self.objects["rect"], color=GREEN, run_time=1))

        # visual_action: FadeIn grid by increasing fill_opacity
        self.play(
            self.objects["grid"].animate.set_fill(opacity=0.2),
            run_time=3.0
        )
        remaining_3 = max(0.1, 8.184 - (1 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # signal_action: Indicate dim_label_length with GREEN
        self.play(Indicate(self.objects["dim_label_length"], color=GREEN, run_time=1))

        # visual_action: Write dim_label_length
        self.play(Write(self.objects["dim_label_length"]), run_time=1.0)
        # Also write the height label for completeness (implied by narrative)
        self.play(Write(self.objects["dim_label_height"]), run_time=1.0)

        remaining_4 = max(0.1, 4.224 - (1 + 2.0) + 0.5)  # Indicate (1s) + Write both labels (2s)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # signal_action: Indicate footer_text with WHITE
        self.play(Indicate(self.objects["footer_text"], color=WHITE, run_time=1))

        # visual_action: Write footer_text
        self.play(Write(self.objects["footer_text"]), run_time=3.0)

        remaining_5 = max(0.1, 11.184 - (1 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))