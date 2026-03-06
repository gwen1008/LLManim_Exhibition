from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        grid_center = ORIGIN
        title_anchor = 3.5 * UP
        table_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # title_text
        title_text = Text("Vector Addition: Head-to-Tail Method", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # step_label
        step_label = Text("Step 1: Draw Vector A", color=YELLOW, font_size=24)
        step_label.next_to(title_text, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # grid
        grid = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            stroke_opacity=0.5,
            axis_config={"stroke_opacity": 0.7}
        )
        grid.move_to(grid_center)
        self.objects["grid"] = grid

        # vector_a
        vector_a = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        vector_a.move_to(grid_center)
        self.objects["vector_a"] = vector_a

        # label_a
        label_a = MathTex(r"\vec{A} = (3, 1)", color=BLUE, font_size=28)
        label_a.next_to(vector_a.get_end(), RIGHT, buff=0.2)
        self.objects["label_a"] = label_a

        # vector_b_initial (invisible initially)
        vector_b_initial = Arrow(
            start=[0, 0, 0],
            end=[1, 2, 0],
            color=GREEN,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        vector_b_initial.move_to(grid_center + 2 * LEFT)
        vector_b_initial.set_opacity(0)
        self.objects["vector_b_initial"] = vector_b_initial

        # vector_b_final (invisible initially)
        vector_b_final = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color=GREEN,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        vector_b_final.move_to([3, 1, 0])
        vector_b_final.set_opacity(0)
        self.objects["vector_b_final"] = vector_b_final

        # label_b
        label_b = MathTex(r"\vec{B} = (1, 2)", color=GREEN, font_size=28)
        label_b.next_to(vector_b_final.get_end(), UP, buff=0.2)
        self.objects["label_b"] = label_b

        # vector_c (invisible initially)
        vector_c = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color=RED,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        vector_c.move_to(grid_center)
        vector_c.set_opacity(0)
        self.objects["vector_c"] = vector_c

        # label_c
        label_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color=RED, font_size=32)
        label_c.next_to(vector_c.get_end(), RIGHT + UP, buff=0.3).shift(0.5 * UP)
        self.objects["label_c"] = label_c

        # component_table (VGroup of MathTex objects)
        # Create a 3x3 grid: rows for A, B, C; columns for x and y.
        table_row_a = MathTex(r"\vec{A}", r"(3,", r"1)").scale(0.8)
        table_row_b = MathTex(r"\vec{B}", r"(1,", r"2)").scale(0.8)
        table_row_c = MathTex(r"\vec{C} = \vec{A} + \vec{B}", r"(4,", r"3)").scale(0.8)

        # Align rows vertically
        table_row_b.next_to(table_row_a, DOWN, aligned_edge=LEFT, buff=0.4)
        table_row_c.next_to(table_row_b, DOWN, aligned_edge=LEFT, buff=0.4)

        # Group them
        component_table = VGroup(table_row_a, table_row_b, table_row_c)
        component_table.move_to([0, -3, 0])
        self.objects["component_table"] = component_table

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_vectors_A__3__1_fdc103dec8/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title_text"]), Write(self.objects["step_label"]), run_time=1.5)
        self.play(Create(self.objects["grid"]), run_time=2.0)
        remaining_1 = max(0.1, 9.024 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/Draw_vectors_A__3__1_fdc103dec8/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Create vector_a
        self.play(Create(self.objects["vector_a"]), run_time=1.5)
        self.play(Write(self.objects["label_a"]), run_time=1.0)
        remaining_2 = max(0.1, 9.552 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Draw_vectors_A__3__1_fdc103dec8/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: UpdateText step_label
        new_step_label_3 = Text("Step 2: Attach Vector B Head-to-Tail", color=YELLOW, font_size=24)
        new_step_label_3.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(Transform(self.objects["step_label"], new_step_label_3), run_time=0.5)

        # Visual action: Transform vector_b_initial (fade in, move, then fade out, while vector_b_final fades in)
        # First, make vector_b_initial visible
        self.play(self.objects["vector_b_initial"].animate.set_opacity(1), run_time=0.5)
        # Animate it moving to the final position (tail at head of A)
        self.play(
            self.objects["vector_b_initial"].animate.move_to(self.objects["vector_b_final"].get_center()),
            run_time=2.0
        )
        # Fade out the moving copy and fade in the final static vector
        self.play(
            self.objects["vector_b_initial"].animate.set_opacity(0),
            self.objects["vector_b_final"].animate.set_opacity(1),
            run_time=0.5
        )
        # Write label_b
        self.play(Write(self.objects["label_b"]), run_time=1.0)
        remaining_3 = max(0.1, 9.672 - 0.5 - 0.5 - 2.0 - 0.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_vectors_A__3__1_fdc103dec8/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: UpdateText step_label
        new_step_label_4 = Text("Step 3: Find the Resultant Vector C", color=YELLOW, font_size=24)
        new_step_label_4.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(Transform(self.objects["step_label"], new_step_label_4), run_time=0.5)

        # Visual action: Create vector_c (change opacity to 1 and draw)
        self.play(self.objects["vector_c"].animate.set_opacity(1), run_time=0.5)
        # Actually draw the arrow (Create on the already visible arrow)
        self.play(Create(self.objects["vector_c"]), run_time=1.5)
        self.play(Write(self.objects["label_c"]), run_time=1.0)
        remaining_4 = max(0.1, 8.688 - 0.5 - 0.5 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Draw_vectors_A__3__1_fdc103dec8/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: UpdateText step_label
        new_step_label_5 = Text("Step 4: Verify with Components", color=YELLOW, font_size=24)
        new_step_label_5.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(Transform(self.objects["step_label"], new_step_label_5), run_time=0.5)

        # Visual action: Write component_table
        self.play(Write(self.objects["component_table"]), run_time=2.0)
        remaining_5 = max(0.1, 13.848 - 0.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/Draw_vectors_A__3__1_fdc103dec8/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: Indicate label_c
        self.play(Indicate(self.objects["label_c"], color=YELLOW, run_time=1.0))

        # Visual action: UpdateText step_label
        new_step_label_6 = Text("Result: A + B = C", color=YELLOW, font_size=24)
        new_step_label_6.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(Transform(self.objects["step_label"], new_step_label_6), run_time=0.5)

        remaining_6 = max(0.1, 7.032 - 1.0 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_6))