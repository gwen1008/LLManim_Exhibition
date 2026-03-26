from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Distance on a Number Line", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # number_line
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=12,
            include_numbers=True,
            color=GRAY_B
        )
        number_line.move_to(global_center)
        self.objects["number_line"] = number_line
        
        # start_dot
        start_dot = Dot(radius=0.1, color=BLUE, fill_opacity=1.0)
        start_dot.move_to(number_line.n2p(-2))
        self.objects["start_dot"] = start_dot
        
        # start_label
        start_label = MathTex("-2", color=BLUE, font_size=36)
        start_label.next_to(start_dot, DOWN, buff=0.2)
        self.objects["start_label"] = start_label
        
        # end_dot (initially invisible)
        end_dot = Dot(radius=0.1, color=GREEN, fill_opacity=0.0)
        end_dot.move_to(number_line.n2p(3))
        self.objects["end_dot"] = end_dot
        
        # end_label (initially invisible)
        end_label = MathTex("3", color=GREEN, font_size=36)
        end_label.next_to(number_line.n2p(3), DOWN, buff=0.2)
        end_label.set_opacity(0.0)
        self.objects["end_label"] = end_label
        
        # distance_arrow (initially invisible)
        distance_arrow = Arrow(
            start=number_line.n2p(-2),
            end=number_line.n2p(3),
            color=YELLOW,
            stroke_width=6,
            buff=0
        )
        distance_arrow.set_opacity(0.0)
        self.objects["distance_arrow"] = distance_arrow
        
        # distance_label (initially invisible)
        distance_label = MathTex("5", color=YELLOW, font_size=36)
        distance_label.next_to(distance_arrow, UP, buff=0.2)
        distance_label.set_opacity(0.0)
        self.objects["distance_label"] = distance_label
        
        # calculation (initially invisible)
        calculation = MathTex(r"|\,3 - (-2)\,| = 5", color=WHITE, font_size=42)
        calculation.move_to(global_center + UP * 1.8)
        calculation.set_opacity(0.0)
        self.objects["calculation"] = calculation
        
        # step_explanation
        step_explanation = Text(
            "We begin with a number line and our starting point.",
            color=GRAY_B,
            font_size=30
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # Additional objects needed for step 4 (moving dot and trail)
        # These are not in layout_plan but required by visual_action details.
        moving_dot = Dot(radius=0.1, color=ORANGE, fill_opacity=1.0)
        moving_dot.move_to(number_line.n2p(-2))
        self.objects["moving_dot"] = moving_dot
        
        # ValueTracker for moving dot animation
        move_tracker = ValueTracker(-2.0)
        self.objects["move_tracker"] = move_tracker
        
        # Trail line using always_redraw (FIXED: replaced add_updater with always_redraw)
        trail = always_redraw(lambda: Line(
            start=number_line.n2p(-2),
            end=number_line.n2p(move_tracker.get_value()),
            color=ORANGE,
            stroke_width=4
        ))
        self.objects["trail"] = trail
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/On_a_number_line_fro_150932c6d6/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["start_dot"], color=BLUE, run_time=1))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 7.176 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Update explanation text for step 1 (implicitly from narrative)
        new_explanation_1 = Text(
            "Let's examine a number line from negative five to positive five. Our journey begins at the point negative two.",
            color=GRAY_B, font_size=30
        )
        new_explanation_1.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_1))
        self.objects["step_explanation"] = new_explanation_1
        
        # Step 2
        audio_step2 = "media/audio/On_a_number_line_fro_150932c6d6/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_2 = max(0.1, 4.464 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        new_explanation_2 = Text(
            "First, we draw the number line and mark our starting position.",
            color=GRAY_B, font_size=30
        )
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        
        # Step 3
        audio_step3 = "media/audio/On_a_number_line_fro_150932c6d6/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(
            Create(self.objects["start_dot"]),
            Write(self.objects["start_label"]),
            run_time=1.5
        )
        remaining_3 = max(0.1, 3.432 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        new_explanation_3 = Text(
            "We place a dot at negative two and label it.",
            color=GRAY_B, font_size=30
        )
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        
        # Step 4
        audio_step4 = "media/audio/On_a_number_line_fro_150932c6d6/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["start_dot"], color=BLUE, run_time=1))
        
        # Add moving dot and trail to scene
        self.add(self.objects["trail"], self.objects["moving_dot"])
        self.play(
            move_tracker.animate.set_value(3.0),
            run_time=3.0,
            rate_func=linear
        )
        remaining_4 = max(0.1, 4.344 - 1.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        new_explanation_4 = Text(
            "Now, we animate the jump from negative two to positive three.",
            color=GRAY_B, font_size=30
        )
        new_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4
        
        # Step 5
        audio_step5 = "media/audio/On_a_number_line_fro_150932c6d6/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Fade out moving dot and trail
        self.play(
            FadeOut(self.objects["moving_dot"]),
            FadeOut(self.objects["trail"]),
            run_time=0.5
        )
        
        # Fade in end dot and label
        self.play(
            self.objects["end_dot"].animate.set_opacity(1.0),
            self.objects["end_label"].animate.set_opacity(1.0),
            run_time=1.0
        )
        remaining_5 = max(0.1, 4.824 - 0.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        new_explanation_5 = Text(
            "The moving dot arrives at positive three. Let's mark this destination.",
            color=GRAY_B, font_size=30
        )
        new_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5
        
        # Step 6
        audio_step6 = "media/audio/On_a_number_line_fro_150932c6d6/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        start_end_group = VGroup(self.objects["start_dot"], self.objects["end_dot"])
        self.play(Circumscribe(start_end_group, color=YELLOW, run_time=1))
        
        self.play(
            self.objects["distance_arrow"].animate.set_opacity(1.0),
            self.objects["distance_label"].animate.set_opacity(1.0),
            run_time=1.5
        )
        remaining_6 = max(0.1, 6.984 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        new_explanation_6 = Text(
            "The path taken is this segment. We can represent it as an arrow, and its length is the distance traveled.",
            color=GRAY_B, font_size=30
        )
        new_explanation_6.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_6))
        self.objects["step_explanation"] = new_explanation_6
        
        # Step 7
        audio_step7 = "media/audio/On_a_number_line_fro_150932c6d6/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["distance_label"], color=YELLOW, run_time=1))
        self.play(self.objects["calculation"].animate.set_opacity(1.0), run_time=1.5)
        remaining_7 = max(0.1, 7.848 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        new_explanation_7 = Text(
            "We can calculate this distance. It is the absolute difference between the end and start points: three minus negative two.",
            color=GRAY_B, font_size=30
        )
        new_explanation_7.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_7))
        self.objects["step_explanation"] = new_explanation_7
        
        # Step 8
        audio_step8 = "media/audio/On_a_number_line_fro_150932c6d6/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["calculation"], color=GREEN, run_time=1))
        
        # Create transformed equation
        calculation_final = MathTex(r"|\,5\,| = 5", color=WHITE, font_size=42)
        calculation_final.move_to(self.objects["calculation"].get_center())
        calculation_final.set_opacity(1.0)
        
        self.play(
            TransformMatchingTex(
                self.objects["calculation"],
                calculation_final,
                path_arc=90
            ),
            run_time=2.0
        )
        self.objects["calculation"] = calculation_final  # Update registry
        
        remaining_8 = max(0.1, 8.472 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        new_explanation_8 = Text(
            "Three minus negative two equals five. Taking the absolute value gives us the positive distance: five units.",
            color=GRAY_B, font_size=30
        )
        new_explanation_8.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_8))
        self.objects["step_explanation"] = new_explanation_8
        
        # Step 9
        audio_step9 = "media/audio/On_a_number_line_fro_150932c6d6/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        final_group = VGroup(
            self.objects["distance_arrow"],
            self.objects["distance_label"],
            self.objects["calculation"]
        )
        self.play(Indicate(final_group, color=YELLOW, run_time=1))
        
        new_explanation_9 = Text(
            "Thus, a jump from negative two to positive three covers a distance of five units on the number line.",
            color=GRAY_B, font_size=30
        )
        new_explanation_9.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_9))
        self.objects["step_explanation"] = new_explanation_9
        
        remaining_9 = max(0.1, 6.624 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))