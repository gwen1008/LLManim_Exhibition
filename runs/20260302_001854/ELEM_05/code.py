'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize rounding 3.7 to the nearest whole number using a number line, emphasizing the midpoint rule (3.5) and spatial reasoning.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, points, labels
#    - Footer Region: [Bottom y=-3.5] for explanatory text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for number line components. Keep labels close to their points. Footer text scaled to 0.8 and centered.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_a_Manim_anima_41db960e84/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Number line, ticks, labels for 3 and 4 appear.
#    - Step 3: Indicate number line, then show point 3.7 and its label.
#    - Step 4: Show midpoint 3.5 and its label.
#    - Step 5: Indicate and draw distance arc, update footer text.
#    - Step 6: Indicate label 4, animate dot moving from 3.7 to 4, show final text.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole Number", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        number_line = Line(start=LEFT*4, end=RIGHT*4, color=GRAY_C, stroke_width=4)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # tick_3
        tick_3 = Line(start=DOWN*0.2, end=UP*0.2, color=WHITE, stroke_width=3)
        tick_3.move_to(LEFT*4)
        self.objects["tick_3"] = tick_3

        # tick_4
        tick_4 = Line(start=DOWN*0.2, end=UP*0.2, color=WHITE, stroke_width=3)
        tick_4.move_to(RIGHT*4)
        self.objects["tick_4"] = tick_4

        # label_3
        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(self.objects["tick_3"], DOWN, buff=0.3)
        self.objects["label_3"] = label_3

        # label_4
        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(self.objects["tick_4"], DOWN, buff=0.3)
        self.objects["label_4"] = label_4

        # point_3_7
        point_3_7 = Dot(radius=0.08, color=YELLOW)
        point_3_7.move_to(RIGHT*1.6)
        self.objects["point_3_7"] = point_3_7

        # label_3_7
        label_3_7 = MathTex("3.7", color=YELLOW)
        label_3_7.next_to(self.objects["point_3_7"], UP, buff=0.3)
        self.objects["label_3_7"] = label_3_7

        # point_mid
        point_mid = Dot(radius=0.08, color=RED)
        point_mid.move_to(ORIGIN)
        self.objects["point_mid"] = point_mid

        # label_mid
        label_mid = MathTex("3.5", color=RED)
        label_mid.next_to(self.objects["point_mid"], UP, buff=0.3)
        self.objects["label_mid"] = label_mid

        # distance_arc
        distance_arc = Arc(radius=0.8, angle=PI/3, start_angle=PI/2, color=TEAL, stroke_width=3)
        distance_arc.move_to(RIGHT*0.8 + UP*0.2)
        self.objects["distance_arc"] = distance_arc

        # explanation_text_step1
        explanation_text_step1 = Text("We start with a number line from 3 to 4.", color=GRAY_C, font_size=28)
        explanation_text_step1.move_to(footer_anchor)
        self.objects["explanation_text_step1"] = explanation_text_step1

        # Additional objects needed for steps (created dynamically)
        # We'll create them when needed and store in self.objects

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_a_Manim_anima_41db960e84/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 3.024 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/Create_a_Manim_anima_41db960e84/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["number_line"]), run_time=1.0)
        self.play(Create(self.objects["tick_3"]), Create(self.objects["tick_4"]), run_time=0.8)
        self.play(Write(self.objects["label_3"]), Write(self.objects["label_4"]), run_time=0.8)
        total_anim_2 = 1.0 + 0.8 + 0.8
        remaining_2 = max(0.1, 2.976 - total_anim_2 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_a_Manim_anima_41db960e84/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # signal_action: Indicate number_line
        self.play(Indicate(self.objects["number_line"], color=YELLOW, run_time=1))
        # visual_action: Create point_3_7 and label_3_7
        self.play(Create(self.objects["point_3_7"]), run_time=0.8)
        self.play(Write(self.objects["label_3_7"]), run_time=0.8)
        total_anim_3 = 1.0 + 0.8 + 0.8
        remaining_3 = max(0.1, 4.128 - total_anim_3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_a_Manim_anima_41db960e84/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Create and update footer text for step 4
        explanation_text_step4 = Text("The midpoint 3.5 is the rounding boundary.", color=GRAY_C, font_size=28)
        explanation_text_step4.move_to(footer_anchor)
        self.objects["explanation_text_step4"] = explanation_text_step4
        self.play(ReplacementTransform(self.objects["explanation_text_step1"], explanation_text_step4), run_time=0.8)
        # Create midpoint and label
        self.play(Create(self.objects["point_mid"]), run_time=0.8)
        self.play(Write(self.objects["label_mid"]), run_time=0.8)
        total_anim_4 = 0.8 + 0.8 + 0.8
        remaining_4 = max(0.1, 10.44 - total_anim_4 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_a_Manim_anima_41db960e84/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # signal_action: Indicate distance_arc
        self.play(Indicate(self.objects["distance_arc"], color=TEAL, run_time=1))
        # visual_action: Create distance_arc and update footer text
        self.play(Create(self.objects["distance_arc"]), run_time=1.0)
        explanation_text_step5 = Text("3.7 > 3.5, so it is closer to 4.", color=GRAY_C, font_size=28)
        explanation_text_step5.move_to(footer_anchor)
        self.objects["explanation_text_step5"] = explanation_text_step5
        self.play(ReplacementTransform(self.objects["explanation_text_step4"], explanation_text_step5), run_time=0.8)
        total_anim_5 = 1.0 + 1.0 + 0.8
        remaining_5 = max(0.1, 9.936 - total_anim_5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/Create_a_Manim_anima_41db960e84/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # signal_action: Indicate label_4
        self.play(Indicate(self.objects["label_4"], color=GREEN, run_time=1))
        # visual_action: Animate dot moving, update footer text
        # Create a copy of the dot to animate
        moving_dot = self.objects["point_3_7"].copy()
        self.add(moving_dot)
        target_position = self.objects["tick_4"].get_center() + UP * 0.2  # Slightly above tick
        self.play(moving_dot.animate.move_to(target_position), run_time=1.5)
        self.remove(moving_dot)
        # Fade out original 3.7 label
        self.play(FadeOut(self.objects["label_3_7"]), run_time=0.5)
        # Create final label near footer
        final_label = MathTex(r"3.7 \rightarrow 4", color=YELLOW, font_size=36)
        final_label.move_to(footer_anchor + UP * 1.0)
        self.objects["final_label"] = final_label
        self.play(Write(final_label), run_time=1.0)
        # Update final explanation text
        explanation_text_final = Text("Therefore, 3.7 rounds up to 4.", color=GRAY_C, font_size=28)
        explanation_text_final.move_to(footer_anchor)
        self.objects["explanation_text_final"] = explanation_text_final
        self.play(ReplacementTransform(self.objects["explanation_text_step5"], explanation_text_final), run_time=0.8)
        total_anim_6 = 1.0 + 1.5 + 0.5 + 1.0 + 0.8
        remaining_6 = max(0.1, 5.928 - total_anim_6 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))