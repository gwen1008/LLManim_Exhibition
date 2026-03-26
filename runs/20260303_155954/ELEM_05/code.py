'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize rounding 3.7 to the nearest whole number using a number line, distance arcs, and the rounding rule.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title and Step Label
#    - Main Content: [Center y=0] for Number Line, Dots, Arcs
#    - Footer Region: [Bottom y=-2.5] for Rule and Final Answer
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for number line components. Position arcs and labels carefully using midpoints.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/rounding_to_nearest_whole/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line.
#    - Step 2: Create point and label for 3.7.
#    - Step 3: Update step label, prompt question.
#    - Step 4: Create distance arc to 3 with label.
#    - Step 5: Write rounding rule in footer.
#    - Step 6: Morph 3.7 label to 4, show final answer.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/To_illustrate_the_ro_80096aeea2/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create Anchors
        header_anchor = 3.0 * UP
        content_center = ORIGIN
        footer_anchor = 2.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Rounding to the Nearest Whole Number", color=WHITE, font_size=36)
        title.move_to(header_anchor)
        self.objects["title"] = title

        # step_label
        step_label = Text("Step 1: The Number Line", color=YELLOW, font_size=24)
        step_label.next_to(title, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # number_line
        number_line = NumberLine(
            x_range=[2.5, 4.5, 0.5],
            length=8,
            include_numbers=True,
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # point_3
        point_3 = Dot(radius=0.08, color=BLUE)
        point_3.move_to(number_line.n2p(3))
        self.objects["point_3"] = point_3

        # label_3
        label_3 = MathTex("3", color=BLUE)
        label_3.next_to(point_3, DOWN, buff=0.2)
        self.objects["label_3"] = label_3

        # point_4
        point_4 = Dot(radius=0.08, color=BLUE)
        point_4.move_to(number_line.n2p(4))
        self.objects["point_4"] = point_4

        # label_4
        label_4 = MathTex("4", color=BLUE)
        label_4.next_to(point_4, DOWN, buff=0.2)
        self.objects["label_4"] = label_4

        # point_37
        point_37 = Dot(radius=0.1, color=RED)
        point_37.move_to(number_line.n2p(3.7))
        self.objects["point_37"] = point_37

        # label_37
        label_37 = MathTex("3.7", color=RED)
        label_37.next_to(point_37, UP, buff=0.2)
        self.objects["label_37"] = label_37

        # distance_arc_to_3
        # Will be created dynamically in step 4
        distance_arc_to_3 = ArcBetweenPoints(
            start=point_37.get_center(),
            end=point_3.get_center(),
            angle=-PI/2,
            color=GREEN,
            stroke_width=3
        )
        self.objects["distance_arc_to_3"] = distance_arc_to_3

        # distance_label_to_3
        midpoint_37_3 = (point_37.get_center() + point_3.get_center()) / 2
        distance_label_to_3 = MathTex("0.3", color=GREEN, font_size=24)
        distance_label_to_3.move_to(midpoint_37_3 + UP * 0.3)
        self.objects["distance_label_to_3"] = distance_label_to_3

        # distance_arc_to_4
        distance_arc_to_4 = ArcBetweenPoints(
            start=point_37.get_center(),
            end=point_4.get_center(),
            angle=PI/2,
            color=PURPLE,
            stroke_width=3
        )
        self.objects["distance_arc_to_4"] = distance_arc_to_4

        # distance_label_to_4
        midpoint_37_4 = (point_37.get_center() + point_4.get_center()) / 2
        distance_label_to_4 = MathTex("0.3", color=PURPLE, font_size=24)
        distance_label_to_4.move_to(midpoint_37_4 + DOWN * 0.3)
        self.objects["distance_label_to_4"] = distance_label_to_4

        # rule_text
        rule_text = MathTex(r"\mathrm{Rounding Rule: }", color=GRAY, font_size=28)
        rule_text.move_to(footer_anchor + LEFT * 2)
        self.objects["rule_text"] = rule_text

        # rule_condition
        rule_condition = MathTex(r"\mathrm{If decimal } \geq 0.5, \mathrm{ round up.}", color=YELLOW, font_size=28)
        rule_condition.next_to(rule_text, RIGHT, buff=0.2)
        self.objects["rule_condition"] = rule_condition

        # final_answer
        final_answer = MathTex(r"3.7 \rightarrow 4", color=GREEN, font_size=36)
        final_answer.move_to(footer_anchor + RIGHT * 3)
        self.objects["final_answer"] = final_answer

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/rounding_to_nearest_whole/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), Write(self.objects["step_label"]), run_time=1.0)
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/rounding_to_nearest_whole/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["label_37"], color=RED, run_time=1))
        self.play(Create(self.objects["point_37"]), Write(self.objects["label_37"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/rounding_to_nearest_whole/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["label_37"], color=YELLOW, run_time=1))
        step_label_new = Text("Step 3: Which is Closer?", color=YELLOW, font_size=24)
        step_label_new.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new), run_time=1.5)
        self.objects["step_label"] = step_label_new
        remaining_3 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/rounding_to_nearest_whole/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["distance_arc_to_3"], color=GREEN, run_time=1))
        self.play(Create(self.objects["distance_arc_to_3"]), run_time=1.5)
        self.play(Write(self.objects["distance_label_to_3"]), run_time=1.0)
        remaining_4 = max(0.1, 4.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/rounding_to_nearest_whole/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["rule_condition"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["rule_text"]), Write(self.objects["rule_condition"]), run_time=2.0)
        remaining_5 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/rounding_to_nearest_whole/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["final_answer"], color=GREEN, run_time=1))
        label_4_new = MathTex("4", color=GREEN)
        label_4_new.move_to(self.objects["label_37"].get_center())
        self.play(TransformMatchingTex(self.objects["label_37"], label_4_new), run_time=1.5)
        self.objects["label_37"] = label_4_new
        self.play(Write(self.objects["final_answer"]), run_time=1.0)
        remaining_6 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))