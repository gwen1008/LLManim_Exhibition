from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan description
        title_anchor = 3.5 * UP
        left_region_center = np.array([-3.5, 0, 0])
        right_region_center = np.array([3.5, 0, 0])
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Circumference: Unrolling a Circle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # circle_main
        circle_main = Circle(radius=2, color=BLUE, stroke_width=4)
        circle_main.move_to(left_region_center)
        self.objects["circle_main"] = circle_main
        
        # diameter_line (depends on circle_main)
        diameter_line = Line(
            circle_main.get_left(),
            circle_main.get_right(),
            color=YELLOW,
            stroke_width=6
        )
        self.objects["diameter_line"] = diameter_line
        
        # label_d (depends on diameter_line)
        label_d = MathTex("D", color=YELLOW)
        label_d.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_d"] = label_d
        
        # circumference_line
        circumference_line = Line(
            start=RIGHT * 0,
            end=RIGHT * 12.566,
            color=GREEN,
            stroke_width=6
        )
        circumference_line.scale(0.7)
        circumference_line.move_to(right_region_center)
        self.objects["circumference_line"] = circumference_line
        
        # label_c (depends on circumference_line)
        label_c = MathTex("C", color=GREEN)
        label_c.next_to(circumference_line, UP, buff=0.2)
        self.objects["label_c"] = label_c
        
        # diameter_copy (depends on circumference_line)
        diameter_copy = Line(
            start=RIGHT * 0,
            end=RIGHT * 4,
            color=YELLOW,
            stroke_width=4
        )
        diameter_copy.scale(0.7)
        diameter_copy.next_to(circumference_line, DOWN, buff=1.0)
        self.objects["diameter_copy"] = diameter_copy
        
        # triple_d_bar (three copies of diameter_copy)
        d1 = Line(RIGHT*0, RIGHT*4, color=RED, stroke_width=4)
        d2 = Line(RIGHT*0, RIGHT*4, color=RED, stroke_width=4)
        d3 = Line(RIGHT*0, RIGHT*4, color=RED, stroke_width=4)
        triple_d_bar = VGroup(d1, d2, d3)
        triple_d_bar.arrange(RIGHT, buff=0)
        triple_d_bar.scale(0.7)
        triple_d_bar.move_to(diameter_copy.get_center())
        self.objects["triple_d_bar"] = triple_d_bar
        
        # label_3d (depends on triple_d_bar)
        label_3d = MathTex("3D", color=RED)
        label_3d.next_to(triple_d_bar, DOWN, buff=0.2)
        self.objects["label_3d"] = label_3d
        
        # formula_pi_d
        formula_pi_d = MathTex(r"C = \pi D", color=WHITE, font_size=48)
        formula_pi_d.move_to(footer_anchor)
        self.objects["formula_pi_d"] = formula_pi_d
        
        # formula_pi_value (initially invisible)
        formula_pi_value = MathTex(r"C \approx 3.1416 \, D", color=WHITE, font_size=48)
        formula_pi_value.move_to(footer_anchor)
        formula_pi_value.set_opacity(0)
        self.objects["formula_pi_value"] = formula_pi_value
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/circumference_unrolling/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["circle_main"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/circumference_unrolling/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["diameter_line"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/circumference_unrolling/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_d"]), run_time=1.0)
        remaining_3 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/circumference_unrolling/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate circle_main
        self.play(Indicate(self.objects["circle_main"], color=GREEN, run_time=1))
        # Visual action: Transform circle_main into circumference_line
        # We'll create a copy of the circle's boundary for the transformation
        circle_arc = self.objects["circle_main"].copy()
        circle_arc.set_color(GREEN)
        self.play(Transform(circle_arc, self.objects["circumference_line"]), run_time=2.0)
        self.remove(circle_arc)
        self.add(self.objects["circumference_line"])
        remaining_4 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/circumference_unrolling/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe circumference_line
        self.play(Circumscribe(self.objects["circumference_line"], color=GREEN, run_time=1))
        # Visual action: Write label_c
        self.play(Write(self.objects["label_c"]), run_time=1.5)
        remaining_5 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/circumference_unrolling/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Indicate diameter_line
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        # Visual action: Create diameter_copy
        self.play(Create(self.objects["diameter_copy"]), run_time=1.0)
        remaining_6 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/circumference_unrolling/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Create triple_d_bar piece by piece
        d1, d2, d3 = self.objects["triple_d_bar"]
        self.play(Create(d1), run_time=0.8)
        self.play(Create(d2), run_time=0.8)
        self.play(Create(d3), run_time=0.8)
        remaining_7 = max(0.1, 2.5 - 2.4 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/circumference_unrolling/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_3d"]), run_time=1.0)
        remaining_8 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_08.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/circumference_unrolling/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        # Signal action: Indicate circumference_line and triple_d_bar
        self.play(
            Indicate(self.objects["circumference_line"], color=GREEN, run_time=1.5),
            Indicate(self.objects["triple_d_bar"], color=RED, run_time=1.5)
        )
        remaining_9 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_09.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/circumference_unrolling/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["formula_pi_d"]), run_time=3.0)
        remaining_10 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        self.add_sound("media/audio/Create_an_animation__30ae0f4fef/step_10.mp3")  # [auto-injected]
        # Step 11
        audio_step11 = "media/audio/circumference_unrolling/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe formula_pi_d
        self.play(Circumscribe(self.objects["formula_pi_d"], color=YELLOW, run_time=1))
        # Visual action: TransformMatchingTex formula_pi_d into formula_pi_value
        self.play(
            TransformMatchingTex(
                self.objects["formula_pi_d"],
                self.objects["formula_pi_value"],
                path_arc=90
            ),
            run_time=3.0
        )
        remaining_11 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_11))
        # Add extra wait time to ensure the final formula is clearly visible
        self.wait(2.0)