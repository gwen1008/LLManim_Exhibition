'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize solving the linear equation 2x = 6 using a concrete balance scale model.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Equation
#    - Main Content: [Center y=0] for the balance scale and items
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for pan contents to manage positioning. Keep equation and explanation text separate.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)`?
# 5. Animation Flow:
#    - Introduce title and equation.
#    - Build the balance scale.
#    - Add items (boxes and circles) to the pans.
#    - Show explanation text.
#    - Animate removal of half the items (division).
#    - Transform equation to final solution.
#    - Final emphasis on the balanced pans.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/To_visualize_the_equ_8471c9c9e4/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        scale_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title_text.move_to(title_anchor).shift(UP * 0.2)
        self.objects["title_text"] = title_text

        # equation_initial
        equation_initial = MathTex("2x = 6", color=YELLOW, font_size=40)
        equation_initial.next_to(title_text, DOWN, buff=0.5)
        self.objects["equation_initial"] = equation_initial

        # scale_beam
        scale_beam = Line(start=LEFT * 4, end=RIGHT * 4, color=GRAY_B, stroke_width=6)
        scale_beam.move_to(scale_anchor).shift(UP * 1.0)
        self.objects["scale_beam"] = scale_beam

        # scale_fulcrum (Triangle)
        fulcrum_points = [ORIGIN, LEFT * 0.3 + DOWN * 0.5, RIGHT * 0.3 + DOWN * 0.5]
        scale_fulcrum = Polygon(*fulcrum_points, color=GRAY, fill_opacity=1.0)
        scale_fulcrum.move_to(scale_anchor).shift(UP * 0.5)
        self.objects["scale_fulcrum"] = scale_fulcrum

        # left_pan
        left_pan = Rectangle(width=2.0, height=0.3, color=GRAY, fill_opacity=0.3, stroke_color=WHITE)
        left_pan.move_to(scale_anchor + LEFT * 2.5 + DOWN * 0.5)
        self.objects["left_pan"] = left_pan

        # right_pan
        right_pan = Rectangle(width=2.0, height=0.3, color=GRAY, fill_opacity=0.3, stroke_color=WHITE)
        right_pan.move_to(scale_anchor + RIGHT * 2.5 + DOWN * 0.5)
        self.objects["right_pan"] = right_pan

        # left_connector (depends on scale_beam and left_pan)
        left_connector = Line(
            start=scale_beam.get_start(),
            end=left_pan.get_top(),
            color=GRAY_B,
            stroke_width=4
        )
        self.objects["left_connector"] = left_connector

        # right_connector (depends on scale_beam and right_pan)
        right_connector = Line(
            start=scale_beam.get_end(),
            end=right_pan.get_top(),
            color=GRAY_B,
            stroke_width=4
        )
        self.objects["right_connector"] = right_connector

        # box1
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
        box1.move_to(left_pan.get_center() + UP * 0.3)
        self.objects["box1"] = box1

        # box2
        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
        box2.move_to(left_pan.get_center() + DOWN * 0.3)
        self.objects["box2"] = box2

        # label_x1
        label_x1 = MathTex("x", color=WHITE, font_size=24)
        label_x1.move_to(box1.get_center())
        self.objects["label_x1"] = label_x1

        # label_x2
        label_x2 = MathTex("x", color=WHITE, font_size=24)
        label_x2.move_to(box2.get_center())
        self.objects["label_x2"] = label_x2

        # circle1 to circle6
        circle_radius = 0.3
        circle_props = {"color": GREEN, "fill_opacity": 0.7, "stroke_color": WHITE}
        circle1 = Circle(radius=circle_radius, **circle_props)
        circle1.move_to(right_pan.get_center() + LEFT * 0.5 + UP * 0.4)
        self.objects["circle1"] = circle1

        circle2 = Circle(radius=circle_radius, **circle_props)
        circle2.move_to(right_pan.get_center() + RIGHT * 0.5 + UP * 0.4)
        self.objects["circle2"] = circle2

        circle3 = Circle(radius=circle_radius, **circle_props)
        circle3.move_to(right_pan.get_center() + LEFT * 0.5)
        self.objects["circle3"] = circle3

        circle4 = Circle(radius=circle_radius, **circle_props)
        circle4.move_to(right_pan.get_center() + RIGHT * 0.5)
        self.objects["circle4"] = circle4

        circle5 = Circle(radius=circle_radius, **circle_props)
        circle5.move_to(right_pan.get_center() + LEFT * 0.5 + DOWN * 0.4)
        self.objects["circle5"] = circle5

        circle6 = Circle(radius=circle_radius, **circle_props)
        circle6.move_to(right_pan.get_center() + RIGHT * 0.5 + DOWN * 0.4)
        self.objects["circle6"] = circle6

        # VGroups for pan contents
        left_items_initial = VGroup(box1, box2, label_x1, label_x2)
        self.objects["left_items_initial"] = left_items_initial

        right_items_initial = VGroup(circle1, circle2, circle3, circle4, circle5, circle6)
        self.objects["right_items_initial"] = right_items_initial

        # explanation_text
        explanation_text = Text(
            "The scale is balanced: two 'x' boxes equal six unit circles.",
            color=GRAY_B,
            font_size=28
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # signal_action: Circumscribe equation_initial
        self.play(Circumscribe(self.objects["equation_initial"], color=YELLOW, run_time=1))
        # visual_action: Create title_text
        self.play(FadeIn(self.objects["title_text"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # signal_action: null
        # visual_action: Create equation_initial
        self.play(Write(self.objects["equation_initial"]), run_time=1.5)
        remaining_2 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # signal_action: null
        # visual_action: Create scale components
        scale_parts = [
            self.objects["scale_fulcrum"],
            self.objects["scale_beam"],
            self.objects["left_connector"],
            self.objects["right_connector"],
            self.objects["left_pan"],
            self.objects["right_pan"]
        ]
        self.play(*[Create(part) for part in scale_parts], run_time=2.5)
        remaining_3 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # signal_action: null
        # visual_action: Create left boxes and labels
        left_items = [
            self.objects["box1"],
            self.objects["box2"],
            self.objects["label_x1"],
            self.objects["label_x2"]
        ]
        self.play(*[Create(item) for item in left_items], run_time=2.0)
        remaining_4 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # signal_action: null
        # visual_action: Create right circles
        right_circles = [
            self.objects["circle1"],
            self.objects["circle2"],
            self.objects["circle3"],
            self.objects["circle4"],
            self.objects["circle5"],
            self.objects["circle6"]
        ]
        self.play(*[Create(circle) for circle in right_circles], run_time=2.5)
        remaining_5 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        # signal_action: Indicate left_items_initial
        self.play(Indicate(self.objects["left_items_initial"], color=RED, run_time=1))
        # visual_action: Write explanation_text
        self.play(Write(self.objects["explanation_text"]), run_time=1.5)
        remaining_6 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        # signal_action: Indicate right_items_initial
        self.play(Indicate(self.objects["right_items_initial"], color=RED, run_time=1))
        # visual_action: Transform explanation_text
        new_explanation_1 = Text(
            "Dividing both sides by 2 means removing half from each side.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_1.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_1), run_time=1.5)
        self.objects["explanation_text"] = new_explanation_1
        remaining_7 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        # signal_action: null
        # visual_action: GroupAnimation - remove half items
        # Items to remove: box2, label_x2, circle1, circle3, circle5
        items_to_remove = VGroup(
            self.objects["box2"],
            self.objects["label_x2"],
            self.objects["circle1"],
            self.objects["circle3"],
            self.objects["circle5"]
        )
        # Animate removal downwards
        self.play(
            items_to_remove.animate.shift(DOWN * 2).set_opacity(0),
            run_time=2.0
        )
        # Remove them from the scene
        self.remove(*items_to_remove)
        # Update VGroups (optional, but good practice)
        self.objects["left_items_initial"] = VGroup(self.objects["box1"], self.objects["label_x1"])
        remaining_circles = [self.objects["circle2"], self.objects["circle4"], self.objects["circle6"]]
        self.objects["right_items_initial"] = VGroup(*remaining_circles)
        remaining_8 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        # signal_action: Circumscribe box1
        self.play(Circumscribe(self.objects["box1"], color=YELLOW, run_time=1))
        # visual_action: ReplacementTransform equation_initial to final equation
        final_equation = MathTex("x = 3", color=YELLOW, font_size=40)
        final_equation.move_to(self.objects["equation_initial"].get_center())
        # Also update explanation text
        final_explanation = Text(
            "One x equals three. So, x = 3.",
            color=GRAY_B,
            font_size=28
        )
        final_explanation.move_to(explanation_anchor)
        self.play(
            TransformMatchingTex(self.objects["equation_initial"], final_equation),
            ReplacementTransform(self.objects["explanation_text"], final_explanation),
            run_time=2.0
        )
        self.objects["equation_initial"] = final_equation
        self.objects["explanation_text"] = final_explanation
        remaining_9 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # ========== Step 10 ==========
        # signal_action: Indicate left_pan and right_pan (visual_action also Indicate)
        self.play(
            Indicate(self.objects["left_pan"], color=BLUE, run_time=1),
            Indicate(self.objects["right_pan"], color=GREEN, run_time=1)
        )
        remaining_10 = max(0.1, 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_10))