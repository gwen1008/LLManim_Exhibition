from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on zones
        title_anchor = 3.0 * UP
        main_stage_center = ORIGIN
        zoom_stage_center = 1.5 * UP
        footer_anchor = 2.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Rounding 3.7 to the Nearest Whole Number", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # num_line_main
        num_line_main = NumberLine(
            x_range=[2.5, 4.5, 0.5],
            length=6,
            include_numbers=True,
            numbers_to_include=[3, 4]
        )
        num_line_main.move_to(main_stage_center)
        self.objects["num_line_main"] = num_line_main
        
        # point_3
        point_3 = Dot(radius=0.08, color=WHITE)
        point_3.move_to(num_line_main.n2p(3))
        self.objects["point_3"] = point_3
        
        # label_3
        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(point_3, DOWN, buff=0.2)
        self.objects["label_3"] = label_3
        
        # point_4
        point_4 = Dot(radius=0.08, color=WHITE)
        point_4.move_to(num_line_main.n2p(4))
        self.objects["point_4"] = point_4
        
        # label_4
        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(point_4, DOWN, buff=0.2)
        self.objects["label_4"] = label_4
        
        # point_3_7
        point_3_7 = Dot(radius=0.1, color=YELLOW, fill_opacity=1.0)
        point_3_7.move_to(num_line_main.n2p(3.7))
        self.objects["point_3_7"] = point_3_7
        
        # label_3_7
        label_3_7 = MathTex("3.7", color=YELLOW)
        label_3_7.next_to(point_3_7, UP, buff=0.2).shift(DOWN * 0.5)
        self.objects["label_3_7"] = label_3_7
        
        # num_line_zoom
        num_line_zoom = NumberLine(
            x_range=[3, 4, 0.1],
            length=4,
            include_numbers=True,
            numbers_with_elongated_ticks=[3, 4],
            tick_size=0.1,
            color=GRAY
        )
        num_line_zoom.move_to(zoom_stage_center)
        self.objects["num_line_zoom"] = num_line_zoom
        
        # zoom_highlight_rect
        zoom_highlight_rect = Rectangle(width=4.2, height=0.8, color=YELLOW, fill_opacity=0.2, stroke_width=2)
        zoom_highlight_rect.move_to(zoom_stage_center)
        self.objects["zoom_highlight_rect"] = zoom_highlight_rect
        
        # explanation_text_1
        explanation_text_1 = Text("Is 3.7 closer to 3 or to 4?", color=WHITE, font_size=28)
        explanation_text_1.move_to(footer_anchor)
        self.objects["explanation_text_1"] = explanation_text_1
        
        # dist_bar_3 (initial small width)
        dist_bar_3 = Rectangle(width=0.1, height=0.5, color=BLUE, fill_opacity=0.7, stroke_width=0)
        dist_bar_3.move_to(footer_anchor + UP*0.5 + LEFT*2.0)
        self.objects["dist_bar_3"] = dist_bar_3
        
        # dist_label_3
        dist_label_3 = MathTex("0.7", color=BLUE)
        dist_label_3.next_to(dist_bar_3, UP, buff=0.1)
        self.objects["dist_label_3"] = dist_label_3
        
        # dist_bar_4 (initial small width)
        dist_bar_4 = Rectangle(width=0.1, height=0.5, color=RED, fill_opacity=0.7, stroke_width=0)
        dist_bar_4.move_to(footer_anchor + UP*0.5 + RIGHT*2.0)
        self.objects["dist_bar_4"] = dist_bar_4
        
        # dist_label_4
        dist_label_4 = MathTex("0.3", color=RED)
        dist_label_4.next_to(dist_bar_4, UP, buff=0.1)
        self.objects["dist_label_4"] = dist_label_4
        
        # comparison_symbol
        comparison_symbol = MathTex("<", color=WHITE, font_size=48)
        comparison_symbol.move_to(footer_anchor + UP*0.5 + DOWN*0.5)
        self.objects["comparison_symbol"] = comparison_symbol
        
        # conclusion_text
        conclusion_text = Text("3.7 is closer to 4, so it rounds up to 4.", color=GREEN, font_size=28)
        conclusion_text.move_to(footer_anchor + DOWN*1.0)
        self.objects["conclusion_text"] = conclusion_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 9.168 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2
        audio_step2 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["num_line_main"]), run_time=1.5)
        self.play(
            Create(self.objects["point_3"]),
            Create(self.objects["point_4"]),
            Write(self.objects["label_3"]),
            Write(self.objects["label_4"]),
            run_time=1.5
        )
        remaining_2 = max(0.1, 5.376 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3
        audio_step3 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["point_3_7"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["point_3_7"]),
            Write(self.objects["label_3_7"]),
            run_time=1.5
        )
        remaining_3 = max(0.1, 6.96 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4
        audio_step4 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["num_line_main"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["zoom_highlight_rect"]), run_time=1)
        self.play(Create(self.objects["num_line_zoom"]), run_time=1.5)
        remaining_4 = max(0.1, 7.584 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5
        audio_step5 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["explanation_text_1"], color=WHITE, run_time=1))
        self.play(Write(self.objects["explanation_text_1"]), run_time=1.5)
        remaining_5 = max(0.1, 7.32 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Step 6
        audio_step6 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["dist_bar_3"], color=BLUE, run_time=1))
        self.play(
            Create(self.objects["dist_bar_3"]),
            Write(self.objects["dist_label_3"]),
            run_time=1
        )
        # Stretch bar to width proportional to 0.7 (scale_factor=2.0 -> width=1.4)
        self.play(
            self.objects["dist_bar_3"].animate.stretch_to_fit_width(1.4),
            run_time=1.5
        )
        remaining_6 = max(0.1, 5.352 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Step 7
        audio_step7 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["dist_bar_4"], color=RED, run_time=1))
        self.play(
            Create(self.objects["dist_bar_4"]),
            Write(self.objects["dist_label_4"]),
            run_time=1
        )
        # Stretch bar to width proportional to 0.3 (scale_factor=2.0 -> width=0.6)
        self.play(
            self.objects["dist_bar_4"].animate.stretch_to_fit_width(0.6),
            run_time=1.5
        )
        remaining_7 = max(0.1, 5.688 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # Step 8
        audio_step8 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Create(self.objects["comparison_symbol"]), run_time=1)
        self.play(Write(self.objects["comparison_symbol"]), run_time=1)
        remaining_8 = max(0.1, 8.52 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # Step 9
        audio_step9 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["conclusion_text"], color=GREEN, run_time=1))
        self.play(Write(self.objects["conclusion_text"]), run_time=1.5)
        remaining_9 = max(0.1, 6.888 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Step 10
        audio_step10 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # Create a green dot at position of point_4 for transformation
        point_4_green = Dot(radius=0.1, color=GREEN, fill_opacity=1.0)
        point_4_green.move_to(self.objects["point_4"].get_center())
        label_4_green = MathTex("4", color=GREEN)
        label_4_green.next_to(point_4_green, UP, buff=0.2)
        
        self.play(
            ReplacementTransform(self.objects["point_3_7"], point_4_green),
            ReplacementTransform(self.objects["label_3_7"], label_4_green),
            run_time=2.0
        )
        # Update registry for final highlight
        self.objects["point_3_7"] = point_4_green
        self.objects["label_3_7"] = label_4_green
        remaining_10 = max(0.1, 6.504 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # Step 11
        audio_step11 = "media/audio/Create_a_Manim_anima_1ec73a4fa3/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        self.play(Circumscribe(self.objects["point_4"], color=GREEN, run_time=1))
        # Fade out auxiliary elements
        fade_outs = [
            self.objects["zoom_highlight_rect"],
            self.objects["num_line_zoom"],
            self.objects["dist_bar_3"],
            self.objects["dist_label_3"],
            self.objects["dist_bar_4"],
            self.objects["dist_label_4"],
            self.objects["comparison_symbol"],
            self.objects["explanation_text_1"]
        ]
        self.play(*[FadeOut(obj) for obj in fade_outs], run_time=1.5)
        remaining_11 = max(0.1, 3.888 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_11))