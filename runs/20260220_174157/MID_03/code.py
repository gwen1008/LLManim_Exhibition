from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        fulcrum = ORIGIN
        left_pan_center = 5 * LEFT
        right_pan_center = 5 * RIGHT
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Scale Beam
        scale_beam = Line(start=5*LEFT, end=5*RIGHT, color=WHITE, stroke_width=8)
        scale_beam.move_to(fulcrum)
        self.objects["scale_beam"] = scale_beam

        # Fulcrum Triangle
        fulcrum_triangle = Polygon(
            np.array([-0.5, 0, 0]),
            np.array([0.5, 0, 0]),
            np.array([0, -1, 0]),
            color=GRAY, fill_opacity=0.8
        )
        fulcrum_triangle.move_to(fulcrum + 0.5*DOWN)
        self.objects["fulcrum_triangle"] = fulcrum_triangle

        # Left Pan
        left_pan = Rectangle(width=2, height=0.5, color=GRAY_B, fill_opacity=0.3, stroke_color=WHITE)
        left_pan.move_to(left_pan_center)
        self.objects["left_pan"] = left_pan

        # Right Pan
        right_pan = Rectangle(width=2, height=0.5, color=GRAY_B, fill_opacity=0.3, stroke_color=WHITE)
        right_pan.move_to(right_pan_center)
        self.objects["right_pan"] = right_pan

        # Pan Strings
        left_pan_string = Line(start=5*LEFT, end=5*LEFT + 0.75*DOWN, color=WHITE, stroke_width=2)
        left_pan_string.move_to(fulcrum)
        self.objects["left_pan_string"] = left_pan_string

        right_pan_string = Line(start=5*RIGHT, end=5*RIGHT + 0.75*DOWN, color=WHITE, stroke_width=2)
        right_pan_string.move_to(fulcrum)
        self.objects["right_pan_string"] = right_pan_string

        # Boxes (left side)
        box1 = Square(side_length=1, color=BLUE, fill_opacity=0.5, stroke_color=WHITE)
        box1.move_to(left_pan_center + UP)
        self.objects["box1"] = box1

        box2 = Square(side_length=1, color=BLUE, fill_opacity=0.5, stroke_color=WHITE)
        box2.move_to(left_pan_center)
        self.objects["box2"] = box2

        # Box labels
        label_x1 = MathTex("x", color=WHITE)
        label_x1.move_to(box1.get_center())
        self.objects["label_x1"] = label_x1

        label_x2 = MathTex("x", color=WHITE)
        label_x2.move_to(box2.get_center())
        self.objects["label_x2"] = label_x2

        # Circles (right side) - initial 2x3 grid
        circle_positions = [
            right_pan_center + LEFT + 0.6*UP,
            right_pan_center + 0.6*UP,
            right_pan_center + RIGHT + 0.6*UP,
            right_pan_center + LEFT + 0.6*DOWN,
            right_pan_center + 0.6*DOWN,
            right_pan_center + RIGHT + 0.6*DOWN,
        ]
        circles = []
        for i, pos in enumerate(circle_positions):
            circ = Circle(radius=0.3, color=GREEN, fill_opacity=0.7, stroke_color=WHITE)
            circ.move_to(pos)
            self.objects[f"circle{i+1}"] = circ
            circles.append(circ)

        # Initial equation at bottom
        eq_initial = MathTex("2x = 6", color=YELLOW, font_size=40)
        eq_initial.move_to(footer_anchor)
        self.objects["eq_initial"] = eq_initial

        # Create VGroups for easier manipulation
        left_boxes = VGroup(box1, box2, label_x1, label_x2)
        all_circles = VGroup(*circles)
        scale_assembly = VGroup(scale_beam, left_pan_string, right_pan_string, left_pan, right_pan)
        # Note: fulcrum_triangle is separate, behind

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(FadeIn(title))
        self.wait(max(0.1, max(0.1, 13.248 - 1)))  # FadeIn run_time ~1

        # Step 2
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Create scale base
        self.play(
            Create(scale_beam),
            Create(fulcrum_triangle),
            Create(left_pan_string),
            Create(right_pan_string),
            Create(left_pan),
            Create(right_pan),
        )
        # Create left and right objects simultaneously
        self.play(
            Create(box1), Create(box2),
            Write(label_x1), Write(label_x2),
            *[Create(circ) for circ in circles]
        )
        self.wait(max(0.1, max(0.1, 7.2 - 6)))  # Approx animation time

        # Step 3
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate equation
        self.play(Indicate(eq_initial, color=YELLOW))
        # Visual action: Write equation
        self.play(Write(eq_initial))
        self.wait(max(0.1, max(0.1, 11.472 - 2)))  # Indicate+Write ~2

        # Step 4: Divide circles into two groups
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe all circles
        self.play(Circumscribe(all_circles, color=GREEN, run_time=1))
        # Visual action: Transform grid into two columns
        # Create target positions for two columns
        left_col_pos = right_pan_center + LEFT * 1.5
        right_col_pos = right_pan_center + RIGHT * 1.5
        # We'll create new VGroups for the columns
        circle_group_left = VGroup()
        circle_group_right = VGroup()
        # Assign circles 1,3,5 to left column; 2,4,6 to right column (maintain vertical order)
        for i, circ in enumerate(circles):
            if i % 2 == 0:  # even index: 0,2,4 -> circles 1,3,5
                target_pos = left_col_pos + (i//2) * 0.6 * DOWN
                circle_group_left.add(circ.copy().move_to(target_pos))
            else:  # odd index: 1,3,5 -> circles 2,4,6
                target_pos = right_col_pos + (i//2) * 0.6 * DOWN
                circle_group_right.add(circ.copy().move_to(target_pos))
        # Animate transformation
        self.play(
            Transform(all_circles[0], circle_group_left[0]),
            Transform(all_circles[2], circle_group_left[1]),
            Transform(all_circles[4], circle_group_left[2]),
            Transform(all_circles[1], circle_group_right[0]),
            Transform(all_circles[3], circle_group_right[1]),
            Transform(all_circles[5], circle_group_right[2]),
        )
        # Update the stored groups
        self.objects["circle_group_left"] = circle_group_left
        self.objects["circle_group_right"] = circle_group_right
        self.wait(max(0.1, max(0.1, 4.488 - 3)))  # Circumscribe+Transform ~3

        # Step 5: Remove one box and one group of circles
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate box2 and right circle group
        self.play(
            Indicate(box2, color=RED),
            Indicate(circle_group_right, color=RED)
        )
        # Visual action: Fade out box2, label_x2, and right circle group
        # Also move remaining box and circles to center of pans
        box1_target_pos = left_pan_center
        circle_left_target_pos = right_pan_center
        self.play(
            FadeOut(box2),
            FadeOut(label_x2),
            FadeOut(circle_group_right),
            box1.animate.move_to(box1_target_pos),
            label_x1.animate.move_to(box1_target_pos),
            circle_group_left.animate.move_to(circle_left_target_pos),
        )
        self.wait(max(0.1, max(0.1, 9.192 - 4)))  # Indicate+FadeOut+Move ~4

        # Step 6: Balance the scale
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Initially tilt the scale slightly (left down) to show imbalance
        scale_assembly.rotate(angle=10*DEGREES, about_point=fulcrum)
        # Now rotate back to horizontal (balanced)
        self.play(
            Rotate(scale_assembly, angle=-10*DEGREES, about_point=fulcrum, run_time=2)
        )
        self.wait(max(0.1, max(0.1, 9.072 - 2)))

        # Step 7: Final equation and highlight
        audio_file = "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe remaining objects
        remaining_objects = VGroup(box1, circle_group_left)
        self.play(Circumscribe(remaining_objects, color=YELLOW, run_time=1))
        # Visual action: Transform equation
        eq_final = MathTex("x = 3", color=YELLOW, font_size=40)
        eq_final.move_to(eq_initial.get_center())
        self.play(TransformMatchingTex(eq_initial, eq_final))
        self.wait(max(0.1, max(0.1, 4.92 - 2)))