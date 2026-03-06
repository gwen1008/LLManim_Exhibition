'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Solve the linear equation 2x = 6 using a concrete balance scale model.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Equation
#    - Main Content: [Center y=0] for the balance scale, boxes, and circles
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - The scale, pans, boxes, and circles are positioned relative to each other using VGroups and get_center/get_left.
#    - Removed items are animated off-screen to LEFT*5 and RIGHT*5 to avoid clutter.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_visualize_the_equ_265869bce5/step_XX.mp3"
# 5. Animation Flow:
#    - Build the scale.
#    - Load boxes (left) and circles (right).
#    - Show equation.
#    - Divide both sides: remove one box, split circles, remove one group.
#    - Transform equation to final answer.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors from layout_plan
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        explanation_anchor = 3.5 * DOWN
        left_side_anchor = 5 * LEFT
        right_side_anchor = 5 * RIGHT
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # scale_fulcrum (Triangle)
        scale_fulcrum = Triangle(color=GRAY_C, fill_opacity=0.5)
        scale_fulcrum.scale(0.5)
        scale_fulcrum.move_to(global_center)
        self.objects["scale_fulcrum"] = scale_fulcrum
        
        # scale_beam
        scale_beam = Line(start=LEFT*3, end=RIGHT*3, color=WHITE, stroke_width=6)
        scale_beam.move_to(global_center + UP*0.7)
        self.objects["scale_beam"] = scale_beam
        
        # left_pan
        left_pan = Circle(radius=0.8, color=GRAY, fill_opacity=0.2, stroke_width=2)
        left_pan.move_to(scale_beam.get_left() + DOWN*0.8)
        self.objects["left_pan"] = left_pan
        
        # right_pan
        right_pan = Circle(radius=0.8, color=GRAY, fill_opacity=0.2, stroke_width=2)
        right_pan.move_to(scale_beam.get_right() + DOWN*0.8)
        self.objects["right_pan"] = right_pan
        
        # box1
        box1 = Square(side_length=0.7, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box1.move_to(left_pan.get_center() + UP*0.4)
        self.objects["box1"] = box1
        
        # box2
        box2 = Square(side_length=0.7, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box2.move_to(left_pan.get_center() + DOWN*0.4)
        self.objects["box2"] = box2
        
        # box_label (will be created later after box1 exists)
        box_label = MathTex("x", color=WHITE).scale(0.8)
        box_label.move_to(box1.get_center())
        self.objects["box_label"] = box_label
        
        # circle_group: six circles in a 2x3 grid
        circles = VGroup()
        for i in range(2):  # rows
            for j in range(3):  # columns
                circ = Circle(radius=0.25, color=GREEN, fill_opacity=0.7)
                circ.move_to(RIGHT * (j - 1) * 0.6 + DOWN * (i - 0.5) * 0.6)
                circles.add(circ)
        circles.move_to(right_pan.get_center())
        self.objects["circle_group"] = circles
        
        # step_explanation
        step_explanation = Text("We start with the equation 2x = 6.", color=YELLOW, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # equation_start
        equation_start = MathTex("2x = 6", color=WHITE, font_size=40)
        equation_start.move_to(global_center + UP*2.0)
        self.objects["equation_start"] = equation_start
        
        # equation_end
        equation_end = MathTex("x = 3", color=WHITE, font_size=40)
        equation_end.move_to(global_center + UP*2.0)
        self.objects["equation_end"] = equation_end
        
        # Additional objects needed for steps
        # For step 7: updated explanation text
        step_explanation_divide = Text("Divide both sides by 2: Perform the same action on both pans.", color=YELLOW, font_size=28)
        step_explanation_divide.move_to(explanation_anchor)
        self.objects["step_explanation_divide"] = step_explanation_divide
        
        # For step 9: two groups of circles
        # We'll split the existing circle_group into two VGroups
        circle_group_top = VGroup(*circles[:3])  # first three circles (top row)
        circle_group_bottom = VGroup(*circles[3:])  # last three circles (bottom row)
        self.objects["circle_group_top"] = circle_group_top
        self.objects["circle_group_bottom"] = circle_group_bottom
        
        # For step 10: we'll animate the top group off
        # For step 13: final explanation text
        step_explanation_final = Text("Solution: One x balances three units, so x = 3.", color=YELLOW, font_size=28)
        step_explanation_final.move_to(explanation_anchor)
        self.objects["step_explanation_final"] = step_explanation_final
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/To_visualize_the_equ_265869bce5/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 9.264 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/To_visualize_the_equ_265869bce5/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["scale_fulcrum"]), run_time=1.5)
        remaining_2 = max(0.1, 2.928 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/To_visualize_the_equ_265869bce5/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(
            Create(self.objects["scale_beam"]),
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            run_time=1.5
        )
        remaining_3 = max(0.1, 2.592 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/To_visualize_the_equ_265869bce5/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate box1
        self.play(Indicate(self.objects["box1"], color=YELLOW, run_time=1))
        # Visual action: Create boxes and labels
        self.play(
            Create(self.objects["box1"]),
            Create(self.objects["box2"]),
            run_time=2.0
        )
        # Add label to box1 and copy to box2
        label1 = self.objects["box_label"].copy()
        label2 = self.objects["box_label"].copy()
        label2.move_to(self.objects["box2"].get_center())
        self.play(Write(label1), Write(label2), run_time=1.5)
        # Store labels for later reference (though not used again)
        self.objects["label1"] = label1
        self.objects["label2"] = label2
        
        remaining_4 = max(0.1, 7.968 - (1 + 2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/To_visualize_the_equ_265869bce5/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate circle_group
        self.play(Indicate(self.objects["circle_group"], color=YELLOW, run_time=1))
        # Visual action: Create circles
        self.play(Create(self.objects["circle_group"]), run_time=2.0)
        remaining_5 = max(0.1, 5.352 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/To_visualize_the_equ_265869bce5/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # No signal action
        self.play(Write(self.objects["equation_start"]), run_time=1.5)
        remaining_6 = max(0.1, 6.936 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/To_visualize_the_equ_265869bce5/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe equation_start
        self.play(Circumscribe(self.objects["equation_start"], color=ORANGE, run_time=1))
        # Visual action: Update explanation text
        self.play(
            ReplacementTransform(
                self.objects["step_explanation"],
                self.objects["step_explanation_divide"]
            ),
            run_time=1.5
        )
        remaining_7 = max(0.1, 11.064 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/To_visualize_the_equ_265869bce5/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Signal action: Indicate box2
        self.play(Indicate(self.objects["box2"], color=RED, run_time=1))
        # Visual action: Animate box2 moving off-screen left
        self.play(
            self.objects["box2"].animate.move_to(left_side_anchor),
            self.objects["label2"].animate.move_to(left_side_anchor),
            run_time=2.0
        )
        remaining_8 = max(0.1, 8.952 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        audio_step9 = "media/audio/To_visualize_the_equ_265869bce5/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe circle_group
        self.play(Circumscribe(self.objects["circle_group"], color=GREEN, run_time=1))
        # Visual action: Temporarily separate circles into two groups
        # We'll shift the top group up and bottom group down slightly
        circle_group_top_target = self.objects["circle_group_top"].copy()
        circle_group_bottom_target = self.objects["circle_group_bottom"].copy()
        circle_group_top_target.shift(UP * 0.3)
        circle_group_bottom_target.shift(DOWN * 0.3)
        
        self.play(
            Transform(self.objects["circle_group_top"], circle_group_top_target),
            Transform(self.objects["circle_group_bottom"], circle_group_bottom_target),
            run_time=1.5
        )
        remaining_9 = max(0.1, 7.176 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # ========== Step 10 ==========
        audio_step10 = "media/audio/To_visualize_the_equ_265869bce5/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        # Signal action: Indicate the top group of circles
        self.play(Indicate(self.objects["circle_group_top"], color=RED, run_time=1))
        # Visual action: Animate top group off-screen right
        self.play(
            self.objects["circle_group_top"].animate.move_to(right_side_anchor),
            run_time=2.0
        )
        remaining_10 = max(0.1, 5.904 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # ========== Step 11 ==========
        audio_step11 = "media/audio/To_visualize_the_equ_265869bce5/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        # No signal action
        # Visual action: Indicate box1
        self.play(Indicate(self.objects["box1"], color=BLUE, run_time=1.5))
        remaining_11 = max(0.1, 8.472 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # ========== Step 12 ==========
        audio_step12 = "media/audio/To_visualize_the_equ_265869bce5/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        
        # Signal action: Indicate the remaining circles (bottom group)
        self.play(Indicate(self.objects["circle_group_bottom"], color=GREEN, run_time=1))
        # Visual action: Transform equation
        self.play(
            TransformMatchingTex(
                self.objects["equation_start"],
                self.objects["equation_end"]
            ),
            run_time=1.5
        )
        remaining_12 = max(0.1, 5.928 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_12))
        
        # ========== Step 13 ==========
        audio_step13 = "media/audio/To_visualize_the_equ_265869bce5/step_12.mp3"
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))
        
        # No signal action
        # Visual action: Update explanation text to final
        self.play(
            ReplacementTransform(
                self.objects["step_explanation_divide"],
                self.objects["step_explanation_final"]
            ),
            run_time=1.5
        )
        remaining_13 = max(0.1, 5.208 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_13))
        
        # Final pause
        self.wait(max(0.1, 2))