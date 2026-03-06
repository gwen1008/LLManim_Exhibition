from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        left_pizza_anchor = 3.5 * LEFT
        right_pizza_anchor = 3.5 * RIGHT
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Circle outline
        circle_outline = Circle(radius=2.5, color=WHITE, stroke_width=3)
        circle_outline.move_to(content_center)
        self.objects["circle_outline"] = circle_outline
        
        # Half shaded sector
        half_shaded = Sector(
            radius=2.5,
            angle=PI,
            start_angle=-PI/2,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        half_shaded.move_to(content_center)
        self.objects["half_shaded"] = half_shaded
        
        # Label for half
        label_half = MathTex(r"\frac{1}{2}", color="#1E90FF", font_size=36)
        # Position will be set relative to half_shaded when it exists
        self.objects["label_half"] = label_half
        
        # Vertical line
        line_vertical = Line(
            start=[0, -2.5, 0],
            end=[0, 2.5, 0],
            color=GRAY_B,
            stroke_width=2
        )
        line_vertical.move_to(content_center)
        self.objects["line_vertical"] = line_vertical
        
        # Horizontal line
        line_horizontal = Line(
            start=[-2.5, 0, 0],
            end=[2.5, 0, 0],
            color=GRAY_B,
            stroke_width=2
        )
        line_horizontal.move_to(content_center)
        self.objects["line_horizontal"] = line_horizontal
        
        # Quarter sectors
        quarter_shaded_top = Sector(
            radius=2.5,
            angle=PI/2,
            start_angle=0,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        quarter_shaded_top.move_to(content_center)
        self.objects["quarter_shaded_top"] = quarter_shaded_top
        
        quarter_shaded_bottom = Sector(
            radius=2.5,
            angle=-PI/2,
            start_angle=0,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        quarter_shaded_bottom.move_to(content_center)
        self.objects["quarter_shaded_bottom"] = quarter_shaded_bottom
        
        # Label for quarters
        label_quarters = MathTex(r"\frac{2}{4}", color="#1E90FF", font_size=36)
        # Position will be set relative to circle_outline when needed
        self.objects["label_quarters"] = label_quarters
        
        # Explanation text
        explanation_text = Text("Start with one whole pizza.", color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # Pizza groups (empty VGroups for now, will be populated in sequence)
        pizza_left_group = VGroup()
        self.objects["pizza_left_group"] = pizza_left_group
        
        pizza_right_group = VGroup()
        self.objects["pizza_right_group"] = pizza_right_group
        
        # Equals sign
        equals_sign = MathTex("=", color=WHITE, font_size=48)
        # Position will be set between pizza groups in step 8
        self.objects["equals_sign"] = equals_sign
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.5)
        self.play(Create(self.objects["circle_outline"]), run_time=1.5)
        remaining_1 = max(0.1, 4.224 - 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation = Text("Divide into two equal halves.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        
        # Signal action: Create line_vertical
        self.play(Create(self.objects["line_vertical"]), run_time=1.5)
        remaining_2 = max(0.1, 7.536 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation = Text("Shade the right half: one-half.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        
        # Signal action: Create half_shaded
        self.play(Create(self.objects["half_shaded"]), run_time=1.5)
        remaining_3 = max(0.1, 6.648 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Position label_half
        self.objects["label_half"].next_to(self.objects["half_shaded"], RIGHT, buff=0.3)
        
        # Signal action: Write label_half
        self.play(Write(self.objects["label_half"]), run_time=1.0)
        remaining_4 = max(0.1, 2.568 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation = Text("Cut each half again: four equal quarters.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        
        # Signal action: Create line_horizontal
        self.play(Create(self.objects["line_horizontal"]), run_time=1.5)
        remaining_5 = max(0.1, 8.52 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation = Text("Shaded area is now two out of four pieces.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        
        # Signal action: Transform half_shaded into two quarters
        # Create a VGroup of the two quarter sectors
        quarters_group = VGroup(
            self.objects["quarter_shaded_top"],
            self.objects["quarter_shaded_bottom"]
        )
        
        # Fade out the half sector and fade in the two quarters
        self.play(
            FadeOut(self.objects["half_shaded"]),
            FadeIn(self.objects["quarter_shaded_top"]),
            FadeIn(self.objects["quarter_shaded_bottom"]),
            run_time=2.0
        )
        remaining_6 = max(0.1, 10.296 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation = Text("One-half equals two-quarters.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        
        # Position label_quarters at same position as label_half
        self.objects["label_quarters"].move_to(self.objects["label_half"].get_center())
        
        # Signal action: ReplacementTransform label_half to label_quarters
        self.play(
            ReplacementTransform(self.objects["label_half"], self.objects["label_quarters"]),
            run_time=1.5
        )
        remaining_7 = max(0.1, 6.072 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation = Text("Compare two separate pizzas.", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        
        # Fade out central objects
        objects_to_fade = VGroup(
            self.objects["circle_outline"],
            self.objects["line_vertical"],
            self.objects["line_horizontal"],
            self.objects["quarter_shaded_top"],
            self.objects["quarter_shaded_bottom"],
            self.objects["label_quarters"],
            self.objects["title"]
        )
        self.play(FadeOut(objects_to_fade), run_time=1.0)
        
        # Create left pizza (half-shaded state)
        left_circle = Circle(radius=2.0, color=WHITE, stroke_width=3)
        left_circle.move_to(left_pizza_anchor)
        
        left_line = Line(
            start=left_pizza_anchor + [0, -2.0, 0],
            end=left_pizza_anchor + [0, 2.0, 0],
            color=GRAY_B,
            stroke_width=2
        )
        
        left_half = Sector(
            radius=2.0,
            angle=PI,
            start_angle=-PI/2,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        left_half.move_to(left_pizza_anchor)
        
        left_label = MathTex(r"\frac{1}{2}", color="#1E90FF", font_size=36)
        left_label.next_to(left_circle, RIGHT, buff=0.3)
        
        # Group left pizza
        self.objects["pizza_left_group"] = VGroup(left_circle, left_line, left_half, left_label)
        self.objects["pizza_left_group"].move_to(left_pizza_anchor)
        
        # Create right pizza (quarter-shaded state)
        right_circle = Circle(radius=2.0, color=WHITE, stroke_width=3)
        right_circle.move_to(right_pizza_anchor)
        
        right_line_v = Line(
            start=right_pizza_anchor + [0, -2.0, 0],
            end=right_pizza_anchor + [0, 2.0, 0],
            color=GRAY_B,
            stroke_width=2
        )
        
        right_line_h = Line(
            start=right_pizza_anchor + [-2.0, 0, 0],
            end=right_pizza_anchor + [2.0, 0, 0],
            color=GRAY_B,
            stroke_width=2
        )
        
        right_quarter_top = Sector(
            radius=2.0,
            angle=PI/2,
            start_angle=0,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        right_quarter_top.move_to(right_pizza_anchor)
        
        right_quarter_bottom = Sector(
            radius=2.0,
            angle=-PI/2,
            start_angle=0,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        right_quarter_bottom.move_to(right_pizza_anchor)
        
        right_label = MathTex(r"\frac{2}{4}", color="#1E90FF", font_size=36)
        right_label.next_to(right_circle, RIGHT, buff=0.3)
        
        # Group right pizza
        self.objects["pizza_right_group"] = VGroup(
            right_circle, right_line_v, right_line_h,
            right_quarter_top, right_quarter_bottom, right_label
        )
        self.objects["pizza_right_group"].move_to(right_pizza_anchor)
        
        # Position equals sign between them
        self.objects["equals_sign"].move_to(ORIGIN)
        
        # Animate creation of side-by-side pizzas
        self.play(
            Create(left_circle),
            Create(left_line),
            Create(left_half),
            Write(left_label),
            run_time=1.5
        )
        
        self.play(
            Create(right_circle),
            Create(right_line_v),
            Create(right_line_h),
            Create(right_quarter_top),
            Create(right_quarter_bottom),
            Write(right_label),
            run_time=1.5
        )
        
        self.play(Write(self.objects["equals_sign"]), run_time=0.8)
        
        remaining_8 = max(0.1, 7.488 - 1.0 - 1.5 - 1.5 - 0.8 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        audio_step9 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation = Text("Shaded area is identical: 1/2 = 2/4", color=GRAY_B, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        
        # Signal action: Indicate both pizza groups with yellow
        self.play(
            Indicate(self.objects["pizza_left_group"], color=YELLOW, run_time=1.5),
            Indicate(self.objects["pizza_right_group"], color=YELLOW, run_time=1.5)
        )
        
        remaining_9 = max(0.1, 9.24 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Final hold
        self.wait(max(0.1, 2))