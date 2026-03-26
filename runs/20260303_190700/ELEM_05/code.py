'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize why 3.7 rounds to 4 using a number line, distance comparison, and the midpoint decision rule.
# 2. Layout Strategy:
#    - Header Region: Title at y=3.5
#    - Main Content: Number line and visual elements centered at y=0
#    - Footer Region: Rule and conclusion text at y=-3.0
# 3. Anti-Overlap Check:
#    - Number line and distance segments are placed at different y-levels to avoid clutter.
#    - Labels are positioned with buff to prevent overlapping.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/rounding_number_line/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line and labels.
#    - Step 2: Show 3.7 point.
#    - Step 3: Show distance to 3 (0.7).
#    - Step 4: Show distance to 4 (0.3).
#    - Step 5: Show midpoint boundary and general rule.
#    - Step 6: Show final conclusion.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_number_line_308d536ac9/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.0 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Rounding on a Number Line: Why 3.7 Rounds to 4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # number_line - custom NumberLine with x_range [-2.5, 2.5] representing 3 to 4
        number_line = NumberLine(
            x_range=[-2.5, 2.5, 0.5],
            length=10,
            include_numbers=False,
            color=GRAY_C
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line
        
        # tick_label_3 (at x=-2 representing 3)
        tick_label_3 = MathTex("3", color=WHITE)
        tick_label_3.next_to(Dot().move_to([-2, 0, 0]), DOWN, buff=0.2)
        self.objects["tick_label_3"] = tick_label_3
        
        # tick_label_4 (at x=2 representing 4)
        tick_label_4 = MathTex("4", color=WHITE)
        tick_label_4.next_to(Dot().move_to([2, 0, 0]), DOWN, buff=0.2)
        self.objects["tick_label_4"] = tick_label_4
        
        # point_37_dot (at x=0.8 representing 3.7)
        point_37_dot = Dot(radius=0.08, color=YELLOW)
        point_37_dot.move_to([0.8, 0, 0])
        self.objects["point_37_dot"] = point_37_dot
        
        # point_37_label
        point_37_label = MathTex("3.7", color=YELLOW)
        point_37_label.next_to(point_37_dot, UP, buff=0.2)
        self.objects["point_37_label"] = point_37_label
        
        # dist_line_3 (from x=-2 to x=0.8, y=-0.5)
        dist_line_3 = Line(
            start=[-2, -0.5, 0],
            end=[0.8, -0.5, 0],
            color=RED,
            stroke_width=6
        )
        self.objects["dist_line_3"] = dist_line_3
        
        # dist_label_3
        dist_label_3 = MathTex("0.7", color=RED)
        dist_label_3.next_to(dist_line_3, DOWN, buff=0.1)
        self.objects["dist_label_3"] = dist_label_3
        
        # dist_line_4 (from x=0.8 to x=2, y=-0.5)
        dist_line_4 = Line(
            start=[0.8, -0.5, 0],
            end=[2, -0.5, 0],
            color=GREEN,
            stroke_width=6
        )
        self.objects["dist_line_4"] = dist_line_4
        
        # dist_label_4
        dist_label_4 = MathTex("0.3", color=GREEN)
        dist_label_4.next_to(dist_line_4, DOWN, buff=0.1)
        self.objects["dist_label_4"] = dist_label_4
        
        # midpoint_line (vertical dashed line at x=0)
        midpoint_line = DashedLine(
            start=[0, -1, 0],
            end=[0, 1, 0],
            color=PURE_BLUE,
            dash_length=0.1
        )
        self.objects["midpoint_line"] = midpoint_line
        
        # midpoint_label
        midpoint_label = MathTex("3.5", color=PURE_BLUE)
        midpoint_label.next_to(midpoint_line, UP, buff=0.2)
        self.objects["midpoint_label"] = midpoint_label
        
        # rule_text
        rule_text = MathTex(r"\mathrm{Rule: } \mathrm{decimal} \geq 0.5 \Rightarrow \mathrm{round up}", color=PURE_BLUE, font_size=30)
        rule_text.move_to(explanation_anchor)
        self.objects["rule_text"] = rule_text
        
        # conclusion_text
        conclusion_text = Text("Therefore, 3.7 rounds up to 4.", color=YELLOW, font_size=30)
        conclusion_text.next_to(rule_text, DOWN, buff=0.5)
        self.objects["conclusion_text"] = conclusion_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/rounding_number_line/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # Visual action: Create number line and labels
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        self.play(Write(self.objects["tick_label_3"]), Write(self.objects["tick_label_4"]), run_time=1.0)
        remaining_1 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/rounding_number_line/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Indicate point_37_dot
        self.play(Indicate(self.objects["point_37_dot"], color=YELLOW, run_time=1))
        
        # Visual action: Create the dot and label
        self.play(Create(self.objects["point_37_dot"]), run_time=1.0)
        self.play(Write(self.objects["point_37_label"]), run_time=0.5)
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/rounding_number_line/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate dist_line_3
        self.play(Indicate(self.objects["dist_line_3"], color=RED, run_time=1))
        
        # Visual action: Create distance line and label
        self.play(Create(self.objects["dist_line_3"]), run_time=1.5)
        self.play(Write(self.objects["dist_label_3"]), run_time=0.5)
        remaining_3 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/rounding_number_line/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate dist_line_4
        self.play(Indicate(self.objects["dist_line_4"], color=GREEN, run_time=1))
        
        # Visual action: Create distance line and label
        self.play(Create(self.objects["dist_line_4"]), run_time=1.5)
        self.play(Write(self.objects["dist_label_4"]), run_time=0.5)
        remaining_4 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/rounding_number_line/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Create midpoint_line (as per JSON, signal_action type is Create)
        self.play(Create(self.objects["midpoint_line"]), run_time=1.0)
        
        # Visual action: Create midpoint label and rule text
        self.play(Write(self.objects["midpoint_label"]), run_time=0.5)
        self.play(Write(self.objects["rule_text"]), run_time=1.0)
        remaining_5 = max(0.1, 5.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/rounding_number_line/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe point_37_dot
        self.play(Circumscribe(self.objects["point_37_dot"], color=YELLOW, run_time=1))
        
        # Visual action: Write conclusion text
        self.play(Write(self.objects["conclusion_text"]), run_time=1.5)
        remaining_6 = max(0.1, 5.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Final hold
        self.wait(max(0.1, 2))