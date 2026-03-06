from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        left_pizza_anchor = content_center + 3.5 * LEFT
        right_pizza_anchor = content_center + 3.5 * RIGHT
        explanation_anchor = 3.0 * DOWN
        
        # Create title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create pizza bases
        pizza_left_base = Circle(radius=2.0, color="#8B4513", fill_opacity=0.3, stroke_width=3)
        pizza_left_base.move_to(left_pizza_anchor)
        self.objects["pizza_left_base"] = pizza_left_base
        
        pizza_right_base = Circle(radius=2.0, color="#8B4513", fill_opacity=0.3, stroke_width=3)
        pizza_right_base.move_to(right_pizza_anchor)
        self.objects["pizza_right_base"] = pizza_right_base
        
        # Create colored slices (initially invisible)
        slice_left_colored = Sector(radius=2.0, angle=PI, start_angle=0, color=YELLOW, fill_opacity=0.7, stroke_width=0)
        slice_left_colored.move_to(pizza_left_base.get_center())
        slice_left_colored.set_opacity(0)
        self.objects["slice_left_colored"] = slice_left_colored
        
        slice_right_colored_1 = Sector(radius=2.0, angle=PI/2, start_angle=0, color=YELLOW, fill_opacity=0.7, stroke_width=0)
        slice_right_colored_1.move_to(right_pizza_anchor)
        slice_right_colored_1.set_opacity(0)
        self.objects["slice_right_colored_1"] = slice_right_colored_1
        
        slice_right_colored_2 = Sector(radius=2.0, angle=PI/2, start_angle=PI/2, color=YELLOW, fill_opacity=0.7, stroke_width=0)
        slice_right_colored_2.move_to(right_pizza_anchor)
        slice_right_colored_2.set_opacity(0)
        self.objects["slice_right_colored_2"] = slice_right_colored_2
        
        # Create divider lines (initially invisible)
        divider_line_left = Line(start=[0,0,0], end=[2,0,0], color=RED, stroke_width=4)
        divider_line_left.move_to(left_pizza_anchor)
        divider_line_left.set_opacity(0)
        self.objects["divider_line_left"] = divider_line_left
        
        divider_line_right_1 = Line(start=[0,0,0], end=[2,0,0], color=RED, stroke_width=4)
        divider_line_right_1.move_to(right_pizza_anchor)
        divider_line_right_1.set_opacity(0)
        self.objects["divider_line_right_1"] = divider_line_right_1
        
        divider_line_right_2 = Line(start=[0,0,0], end=[0,2,0], color=RED, stroke_width=4)
        divider_line_right_2.move_to(right_pizza_anchor)
        divider_line_right_2.set_opacity(0)
        self.objects["divider_line_right_2"] = divider_line_right_2
        
        # Create labels with increased font size and spacing
        label_left = MathTex(r"\frac{1}{2}", color=WHITE, font_size=48)
        label_left.next_to(pizza_left_base, DOWN, buff=1.0)
        self.objects["label_left"] = label_left
        
        label_right = MathTex(r"\frac{2}{4}", color=WHITE, font_size=48)
        label_right.next_to(pizza_right_base, DOWN, buff=1.0)
        self.objects["label_right"] = label_right
        
        # Create explanation text
        explanation_text = Text("We start with two identical whole pizzas.", color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # Create equality sign (initially invisible) - moved up to avoid overlap
        equality_sign = MathTex("=", color=GREEN, font_size=72)
        equality_sign.move_to(content_center + UP*1)
        equality_sign.set_opacity(0)
        self.objects["equality_sign"] = equality_sign
        
        # Group objects for easier transformation
        left_pizza_group = VGroup(
            pizza_left_base,
            slice_left_colored,
            divider_line_left,
            label_left
        )
        self.objects["left_pizza_group"] = left_pizza_group
        
        right_pizza_group = VGroup(
            pizza_right_base,
            slice_right_colored_1,
            slice_right_colored_2,
            divider_line_right_1,
            divider_line_right_2,
            label_right
        )
        self.objects["right_pizza_group"] = right_pizza_group
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["pizza_left_base"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["pizza_left_base"]),
            Create(self.objects["pizza_right_base"]),
            Write(self.objects["title"]),
            Write(self.objects["explanation_text"]),
            run_time=2.0
        )
        remaining_1 = max(0.1, 3.12 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation_2 = Text("The first pizza is cut into two equal halves.", color=GRAY_B, font_size=28)
        new_explanation_2.move_to(explanation_anchor)
        
        self.play(
            self.objects["divider_line_left"].animate.set_opacity(1),
            Write(self.objects["label_left"]),
            ReplacementTransform(self.objects["explanation_text"], new_explanation_2),
            run_time=2.5
        )
        self.objects["explanation_text"] = new_explanation_2
        remaining_2 = max(0.1, 5.184 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation_3 = Text("The second pizza is cut into four equal quarters.", color=GRAY_B, font_size=28)
        new_explanation_3.move_to(explanation_anchor)
        
        self.play(
            self.objects["divider_line_right_1"].animate.set_opacity(1),
            self.objects["divider_line_right_2"].animate.set_opacity(1),
            Write(self.objects["label_right"]),
            ReplacementTransform(self.objects["explanation_text"], new_explanation_3),
            run_time=2.0
        )
        self.objects["explanation_text"] = new_explanation_3
        remaining_3 = max(0.1, 3.624 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["label_left"], color=YELLOW, run_time=1))
        
        # Update explanation text
        new_explanation_4 = Text("Color one half and two quarters to show the fractions.", color=GRAY_B, font_size=28)
        new_explanation_4.move_to(explanation_anchor)
        
        self.play(
            self.objects["slice_left_colored"].animate.set_opacity(0.7),
            self.objects["slice_right_colored_1"].animate.set_opacity(0.7),
            self.objects["slice_right_colored_2"].animate.set_opacity(0.7),
            ReplacementTransform(self.objects["explanation_text"], new_explanation_4),
            run_time=3.0
        )
        self.objects["explanation_text"] = new_explanation_4
        remaining_4 = max(0.1, 9.768 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["slice_left_colored"], color=ORANGE, run_time=1))
        
        # Update explanation text
        new_explanation_5 = Text("Bring pizzas together to compare colored areas directly.", color=GRAY_B, font_size=28)
        new_explanation_5.move_to(explanation_anchor)
        
        # Move pizzas to center positions
        left_target_pos = content_center + 1.5 * LEFT
        right_target_pos = content_center + 1.5 * RIGHT
        
        self.play(
            self.objects["left_pizza_group"].animate.move_to(left_target_pos),
            self.objects["right_pizza_group"].animate.move_to(right_target_pos),
            ReplacementTransform(self.objects["explanation_text"], new_explanation_5),
            run_time=3.0
        )
        self.objects["explanation_text"] = new_explanation_5
        remaining_5 = max(0.1, 11.208 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Show equality sign
        self.play(
            self.objects["equality_sign"].animate.set_opacity(1),
            run_time=1.0
        )
        
        self.play(Circumscribe(self.objects["equality_sign"], color=GREEN, run_time=1))
        
        # Update to final explanation
        final_explanation = Text("One-half equals two-fourths. The colored areas match exactly!", color=GRAY_B, font_size=28)
        final_explanation.move_to(explanation_anchor)
        
        self.play(
            ReplacementTransform(self.objects["explanation_text"], final_explanation),
            run_time=2.0
        )
        self.objects["explanation_text"] = final_explanation
        remaining_6 = max(0.1, 9.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Final hold
        self.wait(max(0.1, 2.0))