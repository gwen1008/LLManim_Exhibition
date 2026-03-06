from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan description
        title_anchor = 3.5 * UP
        eq_anchor = 1.5 * UP
        fulcrum_anchor = ORIGIN
        left_pan_anchor = 3 * LEFT + 2.0 * DOWN
        right_pan_anchor = 3 * RIGHT + 2.0 * DOWN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # scale_fulcrum (Triangle)
        fulcrum_verts = [np.array([0, 0, 0]), np.array([-0.5, -0.8, 0]), np.array([0.5, -0.8, 0])]
        scale_fulcrum = Polygon(*fulcrum_verts, color=GRAY, fill_opacity=1.0)
        scale_fulcrum.move_to(fulcrum_anchor + DOWN*0.1)
        self.objects["scale_fulcrum"] = scale_fulcrum

        # scale_beam
        scale_beam = Line(start=3*LEFT, end=3*RIGHT, color=LIGHT_GRAY, stroke_width=8)
        scale_beam.move_to(fulcrum_anchor)
        self.objects["scale_beam"] = scale_beam

        # left_string and right_string depend on scale_beam endpoints, created later after scale_beam is defined
        left_string = Line(start=scale_beam.get_start(), end=scale_beam.get_start() + DOWN*2, color=LIGHT_GRAY, stroke_width=4)
        self.objects["left_string"] = left_string
        right_string = Line(start=scale_beam.get_end(), end=scale_beam.get_end() + DOWN*2, color=LIGHT_GRAY, stroke_width=4)
        self.objects["right_string"] = right_string

        # left_pan
        left_pan = Rectangle(width=2.0, height=0.3, color=GRAY, fill_opacity=0.7)
        left_pan.move_to(3*LEFT + DOWN*2.0)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Rectangle(width=2.0, height=0.3, color=GRAY, fill_opacity=0.7)
        right_pan.move_to(3*RIGHT + DOWN*2.0)
        self.objects["right_pan"] = right_pan

        # box1 and box2
        box1 = Rectangle(width=1.0, height=1.0, color=BLUE, fill_opacity=0.8, stroke_color=WHITE)
        box1.move_to(left_pan.get_center() + UP*0.6)
        self.objects["box1"] = box1
        box2 = Rectangle(width=1.0, height=1.0, color=BLUE, fill_opacity=0.8, stroke_color=WHITE)
        box2.next_to(box1, DOWN, buff=0)
        self.objects["box2"] = box2

        # label_x1 and label_x2
        label_x1 = MathTex("x", color=WHITE, font_size=30)
        label_x1.move_to(box1.get_center())
        self.objects["label_x1"] = label_x1
        label_x2 = MathTex("x", color=WHITE, font_size=30)
        label_x2.move_to(box2.get_center())
        self.objects["label_x2"] = label_x2

        # circle_group: create 6 green circles arranged in 2x3 grid
        circle_radius = 0.3
        circles = []
        for row in range(2):
            for col in range(3):
                circle = Circle(radius=circle_radius, color=GREEN, fill_opacity=0.8, stroke_color=WHITE)
                # Position relative to right_pan_anchor
                circle.move_to(right_pan.get_center() + UP*(0.6 - row*1.2) + LEFT*(1.0 - col*1.0))
                circles.append(circle)
        circle_group = VGroup(*circles)
        circle_group.move_to(right_pan.get_center())  # Center the group
        self.objects["circle_group"] = circle_group
        # Also store individual circles for potential removal animation (we'll use slicing)
        for i, circ in enumerate(circles):
            self.objects[f"circle_{i}"] = circ

        # eq_initial
        eq_initial = MathTex("2x = 6", color=WHITE, font_size=48)
        eq_initial.move_to(eq_anchor + DOWN*0.5)
        self.objects["eq_initial"] = eq_initial

        # step_explanation
        step_explanation = Text("We start with the equation 2x = 6.", color=YELLOW, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["scale_fulcrum"]), run_time=1.5)
        remaining_1 = max(0.1, 4.776 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(
            AnimationGroup(
                Create(self.objects["scale_beam"]),
                Create(self.objects["left_string"]),
                Create(self.objects["right_string"]),
                Create(self.objects["left_pan"]),
                Create(self.objects["right_pan"]),
                lag_ratio=0.1
            ),
            run_time=2.0
        )
        remaining_2 = max(0.1, 4.2 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # Signal action: Indicate left_pan
        self.play(Indicate(self.objects["left_pan"], color=YELLOW, run_time=1))
        # Visual action: Create boxes and labels
        self.play(
            AnimationGroup(
                Create(self.objects["box1"]),
                Create(self.objects["box2"]),
                Write(self.objects["label_x1"]),
                Write(self.objects["label_x2"]),
                lag_ratio=0.1
            ),
            run_time=2.5
        )
        remaining_3 = max(0.1, 8.856 - 1 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Signal action: Indicate right_pan
        self.play(Indicate(self.objects["right_pan"], color=YELLOW, run_time=1))
        # Visual action: Create circle_group
        self.play(Create(self.objects["circle_group"]), run_time=2.0)
        remaining_4 = max(0.1, 5.184 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action: Circumscribe eq_initial
        self.play(Circumscribe(self.objects["eq_initial"], color=GREEN, run_time=1))
        # Visual action: Write eq_initial
        self.play(Write(self.objects["eq_initial"]), run_time=1.5)
        remaining_5 = max(0.1, 6.936 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # Signal action: Circumscribe eq_initial[0] (the "2x" part)
        # Note: Hardcoded index might be risky, but JSON specifies it.
        self.play(Circumscribe(self.objects["eq_initial"][0], color=RED, run_time=1))
        # Visual action: Transform equation to fraction form
        eq_fraction = MathTex(r"\frac{2x}{2} = \frac{6}{2}", color=WHITE, font_size=48)
        eq_fraction.move_to(self.objects["eq_initial"].get_center())
        self.play(TransformMatchingTex(self.objects["eq_initial"], eq_fraction), run_time=2.0)
        self.objects["eq_initial"] = eq_fraction  # Update registry
        remaining_6 = max(0.1, 5.832 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # No signal action
        # Visual action: Remove box2 and three circles (bottom row: circles 3,4,5)
        circles_to_remove = VGroup(self.objects["circle_3"], self.objects["circle_4"], self.objects["circle_5"])
        self.play(
            AnimationGroup(
                Uncreate(self.objects["box2"]),
                Uncreate(circles_to_remove),
                lag_ratio=0.1
            ),
            run_time=2.5
        )
        # Update circle_group to only contain remaining circles
        remaining_circles = [self.objects[f"circle_{i}"] for i in [0,1,2]]
        new_circle_group = VGroup(*remaining_circles)
        new_circle_group.move_to(self.objects["circle_group"].get_center())
        self.objects["circle_group"] = new_circle_group
        remaining_7 = max(0.1, 6.648 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Signal action: Indicate box1
        self.play(Indicate(self.objects["box1"], color=BLUE, run_time=1))
        # Visual action: Indicate circle_group (remaining three circles)
        self.play(Indicate(self.objects["circle_group"], color=GREEN, run_time=1))
        remaining_8 = max(0.1, 6.024 - 1 - 1 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/To_visualize_the_equ_a022dcbc4a/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # Signal action: Circumscribe eq_initial (current fraction equation)
        self.play(Circumscribe(self.objects["eq_initial"], color=YELLOW, run_time=1))
        # Visual action: Transform to final solution
        eq_final = MathTex("x = 3", color=WHITE, font_size=48)
        eq_final.move_to(self.objects["eq_initial"].get_center())
        self.play(TransformMatchingTex(self.objects["eq_initial"], eq_final), run_time=2.0)
        self.objects["eq_initial"] = eq_final  # Update registry
        remaining_9 = max(0.1, 7.32 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))