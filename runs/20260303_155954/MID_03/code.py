'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the solution to the equation 2x = 6 using a balance scale metaphor.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title and Equation
#    - Main Content: [Center y=0] for Balance Scale
#    - Footer Region: [Bottom y=-3.5] for Step Explanation
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use VGroups for left boxes and right circles. Keep equation centered. Position circles in a grid within the pan.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/solving_2x_equals_6/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Step 1: Show title, equation, explanation.
#    - Step 2: Build balance scale and left-side boxes.
#    - Step 3: Add six circles to right pan.
#    - Step 4: Group circles into two sets of three.
#    - Step 5: Transform equation to x = 3.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/To_visualize_the_equ_6e842a64b8/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        scale_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title_text
        title_text = Text("Solving 2x = 6", font_size=36, color=WHITE)
        title_text.move_to(title_anchor + UP*0.3)
        self.objects["title_text"] = title_text

        # equation
        equation = MathTex("2x = 6", font_size=40, color=YELLOW)
        equation.move_to(title_anchor + DOWN*0.7)
        self.objects["equation"] = equation

        # scale_pivot
        scale_pivot = Circle(radius=0.1, color=GREY, fill_opacity=1.0)
        scale_pivot.move_to(scale_anchor)
        self.objects["scale_pivot"] = scale_pivot

        # scale_beam
        scale_beam = Line(start=[-3,0,0], end=[3,0,0], color=GREY, stroke_width=8)
        scale_beam.move_to(scale_anchor)
        self.objects["scale_beam"] = scale_beam

        # left_pan
        left_pan = Square(side_length=1.2, color=GRAY_C, fill_opacity=0.2, stroke_width=2)
        left_pan.move_to(scale_anchor + LEFT*2.5)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Square(side_length=1.8, color=GRAY_C, fill_opacity=0.2, stroke_width=2)
        right_pan.move_to(scale_anchor + RIGHT*2.5)
        self.objects["right_pan"] = right_pan

        # box1
        box1 = Square(side_length=0.6, color=BLUE, fill_opacity=0.7)
        box1.move_to(left_pan.get_center() + UP*0.4)
        self.objects["box1"] = box1

        # box2
        box2 = Square(side_length=0.6, color=BLUE, fill_opacity=0.7)
        box2.move_to(left_pan.get_center() + DOWN*0.4)
        self.objects["box2"] = box2

        # label_x1
        label_x1 = MathTex("x", font_size=24, color=WHITE)
        label_x1.move_to(box1.get_center())
        self.objects["label_x1"] = label_x1

        # label_x2
        label_x2 = MathTex("x", font_size=24, color=WHITE)
        label_x2.move_to(box2.get_center())
        self.objects["label_x2"] = label_x2

        # circle6 (will be created as part of a group in sequence)
        # We'll create six circles in step 3
        circle_radius = 0.25
        circle_props = {"color": GREEN, "fill_opacity": 0.7}
        # Positions for a 2x3 grid within right_pan
        right_center = right_pan.get_center()
        grid_positions = []
        for row in range(2):
            for col in range(3):
                x_offset = (col - 1) * 0.6  # 0.6 spacing
                y_offset = (0.5 - row) * 0.6
                pos = right_center + np.array([x_offset, y_offset, 0])
                grid_positions.append(pos)
        circles = []
        for i, pos in enumerate(grid_positions):
            circ = Circle(radius=circle_radius, **circle_props)
            circ.move_to(pos)
            circles.append(circ)
            self.objects[f"circle{i+1}"] = circ

        # step_explanation
        step_explanation = Text("We start with the equation 2x = 6.", font_size=24, color=GRAY_C)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # group1_highlight and group2_highlight (will be positioned in sequence)
        group1_highlight = Rectangle(width=1.8, height=0.7, color=BLUE, stroke_width=3, fill_opacity=0.0)
        group2_highlight = Rectangle(width=1.8, height=0.7, color=RED, stroke_width=3, fill_opacity=0.0)
        # Position them around the top and bottom rows of circles
        top_row_center = right_center + UP*0.3
        bottom_row_center = right_center + DOWN*0.3
        group1_highlight.move_to(top_row_center)
        group2_highlight.move_to(bottom_row_center)
        self.objects["group1_highlight"] = group1_highlight
        self.objects["group2_highlight"] = group2_highlight

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/solving_2x_equals_6/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Signal Action
        self.play(Circumscribe(self.objects["equation"], color=YELLOW, run_time=1))
        # Visual Action
        self.play(
            Write(self.objects["title_text"]),
            Write(self.objects["equation"]),
            Write(self.objects["step_explanation"]),
            run_time=1.5
        )
        remaining_1 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/solving_2x_equals_6/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal Action
        self.play(Indicate(VGroup(self.objects["box1"], self.objects["box2"], self.objects["label_x1"], self.objects["label_x2"]), color=BLUE, run_time=1))
        # Visual Action
        self.play(
            Create(self.objects["scale_pivot"]),
            Create(self.objects["scale_beam"]),
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            Create(self.objects["box1"]),
            Create(self.objects["box2"]),
            Write(self.objects["label_x1"]),
            Write(self.objects["label_x2"]),
            run_time=2.0
        )
        # Update explanation text
        new_explanation_2 = Text("On the left: two x boxes. On the right: six unit circles.", font_size=24, color=GRAY_C)
        new_explanation_2.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        remaining_2 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/solving_2x_equals_6/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal Action
        self.play(Indicate(self.objects["right_pan"], color=GREEN, run_time=1))
        # Visual Action
        circle_animations = [Create(circ) for circ in circles]
        self.play(*circle_animations, run_time=2.0)
        # Update explanation text
        new_explanation_3 = Text("The scale is balanced: 2x = 6.", font_size=24, color=GRAY_C)
        new_explanation_3.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        remaining_3 = max(0.1, 3.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/solving_2x_equals_6/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal Action
        self.play(Indicate(VGroup(self.objects["box1"], self.objects["box2"]), color=BLUE, run_time=1))
        # Visual Action
        self.play(
            Create(self.objects["group1_highlight"]),
            Create(self.objects["group2_highlight"]),
            run_time=1.5
        )
        # Update explanation text
        new_explanation_4 = Text("Divide 6 into 2 equal groups.", font_size=24, color=GRAY_C)
        new_explanation_4.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4
        remaining_4 = max(0.1, 4.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/solving_2x_equals_6/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal Action
        self.play(Indicate(VGroup(self.objects["group1_highlight"], self.objects["group2_highlight"]), color=YELLOW, run_time=1))
        # Visual Action
        new_equation = MathTex("x = 3", font_size=40, color=YELLOW)
        new_equation.move_to(self.objects["equation"].get_center())
        self.play(TransformMatchingTex(self.objects["equation"], new_equation, path_arc=90), run_time=2.0)
        self.objects["equation"] = new_equation
        # Update explanation text
        new_explanation_5 = Text("Each x equals 3. So, x = 3.", font_size=24, color=GRAY_C)
        new_explanation_5.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5
        remaining_5 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final pause
        self.wait(max(0.1, 2))