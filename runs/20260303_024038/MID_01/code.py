from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_number_line_51b7bfc453/final_narrative.mp3")
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Number Line Jump: From -2 to +3", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # number_line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=12,
            include_numbers=False,
            color=BLUE
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line
        
        # tick_marks_group
        tick_marks = VGroup()
        for x in range(-5, 6):
            tick = Line(UP * 0.15, DOWN * 0.15, color=BLUE)
            tick.move_to(number_line.n2p(x))
            tick_marks.add(tick)
        tick_marks.move_to(content_center)
        self.objects["tick_marks_group"] = tick_marks
        
        # number_labels_group
        number_labels = VGroup()
        for x in range(-5, 6):
            if x == 0:
                label = MathTex("0", color=GRAY_C, font_size=24)
            else:
                label = MathTex(str(x), color=GRAY_C, font_size=24)
            label.move_to(number_line.n2p(x) + DOWN * 0.4)
            number_labels.add(label)
        self.objects["number_labels_group"] = number_labels
        
        # point_start
        point_start = Dot(radius=0.08, color=RED)
        point_start.move_to(number_line.n2p(-2))
        self.objects["point_start"] = point_start
        
        # label_start
        label_start = MathTex(r"\mathrm{Start: } -2", color=RED, font_size=28)
        label_start.next_to(point_start, UP, buff=0.3)
        self.objects["label_start"] = label_start
        
        # point_end
        point_end = Dot(radius=0.08, color=GREEN)
        point_end.move_to(number_line.n2p(3))
        self.objects["point_end"] = point_end
        
        # label_end
        label_end = MathTex(r"\mathrm{End: } +3", color=GREEN, font_size=28)
        label_end.next_to(point_end, UP, buff=0.3)
        self.objects["label_end"] = label_end
        
        # Create a ValueTracker for arrow progress
        arrow_progress = ValueTracker(0)
        self.objects["arrow_progress"] = arrow_progress
        
        # Define a function to create the arrow based on progress
        def create_arrow():
            start = point_start.get_center()
            end = point_start.get_center() + (point_end.get_center() - point_start.get_center()) * arrow_progress.get_value()
            return Arrow(
                start=start,
                end=end,
                color=YELLOW,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.15,
                buff=0
            )
        
        # Create the arrow using always_redraw
        jump_arrow = always_redraw(create_arrow)
        self.objects["jump_arrow"] = jump_arrow
        
        # distance_bracket
        # Create a line between the points for the brace
        brace_line = Line(
            start=point_start.get_center(),
            end=point_end.get_center(),
            color=TEAL
        )
        distance_bracket = Brace(
            brace_line,
            direction=UP,
            color=TEAL
        )
        self.objects["distance_bracket"] = distance_bracket
        
        # distance_label
        distance_label = MathTex(r"5\mathrm{ units}", color=TEAL, font_size=28)
        distance_label.next_to(distance_bracket, UP, buff=0.2)
        self.objects["distance_label"] = distance_label
        
        # step_explanation (placeholder, will be updated each step)
        step_explanation = Text("Placeholder for step explanation.", color=GRAY_C, font_size=26)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # Set z_index for layering
        jump_arrow.set_z_index(1)
        distance_bracket.set_z_index(1)
        distance_label.set_z_index(1)
        point_start.set_z_index(1)
        point_end.set_z_index(1)
        label_start.set_z_index(1)
        label_end.set_z_index(1)
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/number_line_jump/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation1 = Text("Let's begin by drawing a number line from negative five to positive five.", color=GRAY_C, font_size=26)
        new_explanation1.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation1))
        self.objects["step_explanation"] = new_explanation1
        
        # Create number line, ticks, and labels
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        self.play(Create(self.objects["tick_marks_group"]), run_time=1.0)
        self.play(Write(self.objects["number_labels_group"]), run_time=1.5)
        remaining_1 = max(0.1, 4.0 - (1.5 + 1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/number_line_jump/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation2 = Text("We are interested in a jump starting at negative two and ending at positive three. Let's mark these points.", color=GRAY_C, font_size=26)
        new_explanation2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation2))
        self.objects["step_explanation"] = new_explanation2
        
        # Signal action: Indicate point_start
        self.play(Indicate(self.objects["point_start"], color=RED, run_time=1))
        
        # Visual action: Create start point and label
        self.play(FadeIn(self.objects["point_start"]), run_time=0.5)
        self.play(Write(self.objects["label_start"]), run_time=0.5)
        remaining_2 = max(0.1, 3.0 - (1.0 + 0.5 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/number_line_jump/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation3 = Text("Now, let's visualize the jump itself. An arrow will grow from the start point to the end point.", color=GRAY_C, font_size=26)
        new_explanation3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation3))
        self.objects["step_explanation"] = new_explanation3
        
        # Signal action: Indicate point_end
        self.play(Indicate(self.objects["point_end"], color=GREEN, run_time=1))
        
        # Create end point and label
        self.play(FadeIn(self.objects["point_end"]), run_time=0.5)
        self.play(Write(self.objects["label_end"]), run_time=0.5)
        
        # Add the arrow to the scene before animating it
        self.add(self.objects["jump_arrow"])
        
        # Animate arrow growing from start to end using ValueTracker
        self.play(
            arrow_progress.animate.set_value(1),
            run_time=2.0
        )
        remaining_3 = max(0.1, 4.0 - (1.0 + 0.5 + 0.5 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/number_line_jump/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation4 = Text("How far did we jump? The distance from negative two to positive three is five units. Let's measure and label this distance.", color=GRAY_C, font_size=26)
        new_explanation4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation4))
        self.objects["step_explanation"] = new_explanation4
        
        # Create the distance bracket and label
        self.play(Create(self.objects["distance_bracket"]), run_time=1.0)
        self.play(Write(self.objects["distance_label"]), run_time=0.5)
        self.play(Circumscribe(self.objects["distance_label"], color=TEAL, run_time=1))
        remaining_4 = max(0.1, 4.0 - (1.0 + 0.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/number_line_jump/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation5 = Text("We have successfully demonstrated that a jump from negative two to positive three on the number line covers a distance of five units.", color=GRAY_C, font_size=26)
        new_explanation5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation5))
        self.objects["step_explanation"] = new_explanation5
        
        # Signal action: Indicate jump_arrow
        self.play(Indicate(self.objects["jump_arrow"], color=YELLOW, run_time=1))
        # Also highlight distance label
        self.play(Indicate(self.objects["distance_label"], color=TEAL, run_time=1))
        remaining_5 = max(0.1, 3.0 - (1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final pause
        self.wait(max(0.1, 2))