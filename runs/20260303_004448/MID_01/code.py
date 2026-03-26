'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing subtraction as finding the distance between two points on a number line (-2 to +3).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, points, arrow
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for ticks/labels to keep them together. Position labels below points to avoid collision with arrow.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/number_line_jump/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line and ticks.
#    - Step 2: Show start point (-2) with label.
#    - Step 3: Show end point (+3) with label.
#    - Step 4: Move start point to end point.
#    - Step 5: Grow arrow from start to end.
#    - Step 6: Write distance label '5'.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create title
        title = Text("Number Line Jump: From -2 to +3", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create number line (main horizontal line)
        number_line = Line(start=5*LEFT, end=5*RIGHT, color=GRAY_B, stroke_width=4)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line
        
        # Create ticks and labels from -5 to 5
        ticks_group = VGroup()
        for i in range(-5, 6):
            tick = Line(start=UP*0.15, end=DOWN*0.15, color=WHITE, stroke_width=2)
            tick.move_to(content_center + RIGHT * i)
            ticks_group.add(tick)
            
            label = MathTex(str(i), color=WHITE, font_size=24)
            label.next_to(tick, DOWN, buff=0.15)
            ticks_group.add(label)
        ticks_group.move_to(content_center)
        self.objects["ticks_group"] = ticks_group
        
        # Create start point and label
        point_start = Dot(radius=0.08, color=GREEN)
        point_start.move_to(content_center + LEFT * 2)
        self.objects["point_start"] = point_start
        
        label_start = MathTex("-2", color=GREEN, font_size=30)
        label_start.next_to(point_start, DOWN, buff=0.3)
        self.objects["label_start"] = label_start
        
        # Create end point and label
        point_end = Dot(radius=0.08, color=RED)
        point_end.move_to(content_center + RIGHT * 3)
        self.objects["point_end"] = point_end
        
        label_end = MathTex("+3", color=RED, font_size=30)
        label_end.next_to(point_end, DOWN, buff=0.3)
        self.objects["label_end"] = label_end
        
        # Create jump arrow
        jump_arrow = Arrow(
            start=point_start.get_center(),
            end=point_end.get_center(),
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["jump_arrow"] = jump_arrow
        
        # Create distance label
        distance_label = MathTex("5", color=YELLOW, font_size=36)
        distance_label.next_to(jump_arrow, UP, buff=0.2)
        self.objects["distance_label"] = distance_label
        
        # Create step explanation text
        step_explanation = Text("Let's set up our number line.", color=BLUE_C, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/number_line_jump/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Write(self.objects["step_explanation"]), run_time=1.0)
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        self.play(Create(self.objects["ticks_group"]), run_time=2.0)
        remaining_1 = max(0.1, 3.0 - (1.0 + 1.0 + 1.5 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/number_line_jump/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation text
        new_explanation_2 = Text("Our starting position is negative two.", color=BLUE_C, font_size=28)
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        
        self.play(Circumscribe(self.objects["label_start"], color=GREEN, run_time=1))
        self.play(FadeIn(self.objects["point_start"]), FadeIn(self.objects["label_start"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - (1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/number_line_jump/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        new_explanation_3 = Text("Our destination is positive three.", color=BLUE_C, font_size=28)
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        
        self.play(Circumscribe(self.objects["label_end"], color=RED, run_time=1))
        self.play(FadeIn(self.objects["point_end"]), FadeIn(self.objects["label_end"]), run_time=1.5)
        remaining_3 = max(0.1, 2.5 - (1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/number_line_jump/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        new_explanation_4 = Text("We make the jump from -2 to +3.", color=BLUE_C, font_size=28)
        new_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4
        
        self.play(Indicate(self.objects["point_start"], color=GREEN, run_time=1))
        
        # Create a copy of the start point to animate movement
        moving_dot = self.objects["point_start"].copy()
        self.add(moving_dot)
        self.play(
            moving_dot.animate.move_to(self.objects["point_end"].get_center()),
            run_time=2.0
        )
        self.remove(moving_dot)
        remaining_4 = max(0.1, 3.0 - (1.0 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/number_line_jump/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        new_explanation_5 = Text("The distance is represented by an arrow.", color=BLUE_C, font_size=28)
        new_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5
        
        self.play(Indicate(self.objects["jump_arrow"], color=YELLOW, run_time=1))
        self.play(GrowArrow(self.objects["jump_arrow"]), run_time=2.0)
        remaining_5 = max(0.1, 3.0 - (1.0 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/number_line_jump/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        new_explanation_6 = Text("The distance is 5 units.", color=BLUE_C, font_size=28)
        new_explanation_6.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_6))
        self.objects["step_explanation"] = new_explanation_6
        
        self.play(Circumscribe(self.objects["distance_label"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["distance_label"]), run_time=1.5)
        remaining_6 = max(0.1, 3.0 - (1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Final pause
        self.wait(max(0.1, 2))