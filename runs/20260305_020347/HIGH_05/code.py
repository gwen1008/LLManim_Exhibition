'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate vector addition using the head-to-tail (triangle) method.
# 2. Layout Strategy: Three-zone layout.
#    - Header Region: [y=3.5] for Title and Step Label.
#    - Main Content: [Center y=0] for NumberPlane and Vectors.
#    - Footer Region: [Bottom y=-3.5] for Explanation Text.
# 3. Anti-Overlap Check: Use VGroups for vector+label pairs. Position labels relative to arrow ends.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow: Show plane, draw Vector A, label it, update step, draw Vector B from A's head, label it, update step, draw resultant Vector C, label it, final summary.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_vectors_A____3__3dde9b6b82/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        plane_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title_text
        title_text = Text("Vector Addition: The Triangle (Head-to-Tail) Method", color=WHITE, font_size=36)
        title_text.move_to(title_anchor + UP*0.3)
        self.objects["title_text"] = title_text

        # step_label
        step_label = Text("Step 1: Draw Vector A", color=YELLOW, font_size=28)
        step_label.next_to(title_text, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # plane
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            stroke_opacity=0.5
        )
        plane.move_to(plane_center)
        self.objects["plane"] = plane

        # vec_a_arrow
        vec_a_arrow = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color=BLUE,
            stroke_width=8,
            buff=0
        )
        vec_a_arrow.move_to(plane_center)
        self.objects["vec_a_arrow"] = vec_a_arrow

        # label_a
        label_a = MathTex(r"\vec{A} = (3,1)", color=BLUE, font_size=30)
        # Position will be set after arrow is created/positioned
        self.objects["label_a"] = label_a

        # vec_b_arrow
        vec_b_arrow = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color=GREEN,
            stroke_width=8,
            buff=0
        )
        vec_b_arrow.move_to([3, 1, 0])
        self.objects["vec_b_arrow"] = vec_b_arrow

        # label_b
        label_b = MathTex(r"\vec{B} = (1,2)", color=GREEN, font_size=30)
        self.objects["label_b"] = label_b

        # vec_c_arrow
        vec_c_arrow = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color=RED,
            stroke_width=10,
            buff=0
        )
        vec_c_arrow.move_to(plane_center)
        self.objects["vec_c_arrow"] = vec_c_arrow

        # label_c
        label_c = MathTex(r"\vec{C} = \vec{A}+\vec{B} = (4,3)", color=RED, font_size=32)
        self.objects["label_c"] = label_c

        # explanation_line
        explanation_line = Text("Placeholder explanation text.", color=GRAY_B, font_size=24)
        explanation_line.move_to(explanation_anchor)
        self.objects["explanation_line"] = explanation_line

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # Narrative: We begin with a coordinate plane.
        # signal_action: null
        # visual_action: Create plane
        self.play(Create(self.objects["plane"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # Narrative: Let's draw vector A from the origin to the point (3,1).
        # signal_action: Indicate plane_center
        center_dot = Dot(self.objects["plane"].get_center(), color=YELLOW, radius=0.1)
        self.add(center_dot)
        self.play(Indicate(center_dot, color=YELLOW, run_time=1))
        # visual_action: Create vec_a_arrow
        self.play(Create(self.objects["vec_a_arrow"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # Narrative: We label it as vector A, with its components three and one.
        # signal_action: Circumscribe vec_a_arrow
        self.play(Circumscribe(self.objects["vec_a_arrow"], color=BLUE, run_time=1))
        # Position label_a relative to vec_a_arrow's end
        self.objects["label_a"].next_to(self.objects["vec_a_arrow"].get_end(), RIGHT, buff=0.2)
        # visual_action: Write label_a
        self.play(Write(self.objects["label_a"]), run_time=1.0)
        remaining_3 = max(0.1, 2.5 - (1 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # Narrative: Now, for vector B. We place its tail at the head of vector A...
        # signal_action: Indicate vec_a_arrow.get_end()
        end_dot = Dot(self.objects["vec_a_arrow"].get_end(), color=YELLOW, radius=0.1)
        self.add(end_dot)
        self.play(Indicate(end_dot, color=YELLOW, run_time=1))
        # visual_action: ReplacementTransform step_label
        step_label_new = Text("Step 2: Place Vector B head-to-tail", color=YELLOW, font_size=28)
        step_label_new.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new))
        self.objects["step_label"] = step_label_new
        remaining_4 = max(0.1, 3.0 - (1 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # Narrative: Vector B has components one and two...
        # signal_action: null
        # visual_action: Create vec_b_arrow
        self.play(Create(self.objects["vec_b_arrow"]), run_time=1.5)
        remaining_5 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        # Narrative: We label this as vector B.
        # signal_action: Circumscribe vec_b_arrow
        self.play(Circumscribe(self.objects["vec_b_arrow"], color=GREEN, run_time=1))
        # Position label_b relative to vec_b_arrow's end
        self.objects["label_b"].next_to(self.objects["vec_b_arrow"].get_end(), UP+RIGHT, buff=0.2)
        # visual_action: Write label_b
        self.play(Write(self.objects["label_b"]), run_time=1.0)
        remaining_6 = max(0.1, 2.0 - (1 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        # Narrative: The graphical sum, or resultant vector C...
        # signal_action: Indicate vec_a_arrow.get_start()
        start_dot = Dot(self.objects["vec_a_arrow"].get_start(), color=YELLOW, radius=0.1)
        self.add(start_dot)
        self.play(Indicate(start_dot, color=YELLOW, run_time=1))
        # visual_action: ReplacementTransform step_label
        step_label_new2 = Text("Step 3: Draw the Resultant Vector C", color=YELLOW, font_size=28)
        step_label_new2.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new2))
        self.objects["step_label"] = step_label_new2
        remaining_7 = max(0.1, 3.5 - (1 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        # Narrative: Let's draw that vector now, from the origin directly to the head of vector B.
        # signal_action: Indicate vec_b_arrow.get_end()
        end_dot2 = Dot(self.objects["vec_b_arrow"].get_end(), color=YELLOW, radius=0.1)
        self.add(end_dot2)
        self.play(Indicate(end_dot2, color=YELLOW, run_time=1))
        # visual_action: Create vec_c_arrow
        self.play(Create(self.objects["vec_c_arrow"]), run_time=1.5)
        remaining_8 = max(0.1, 2.5 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        # Narrative: This is our resultant vector C...
        # signal_action: Circumscribe label_c
        # Position label_c relative to vec_c_arrow's end
        self.objects["label_c"].next_to(self.objects["vec_c_arrow"].get_end(), LEFT+UP, buff=0.3)
        self.play(Circumscribe(self.objects["label_c"], color=RED, run_time=1))
        # visual_action: Write label_c
        self.play(Write(self.objects["label_c"]), run_time=1.5)
        remaining_9 = max(0.1, 4.0 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_9))

        # ========== Step 10 ==========
        # Narrative: Graphically, we have constructed a triangle...
        # signal_action: Indicate vec_a_arrow
        self.play(Indicate(self.objects["vec_a_arrow"], color=BLUE, run_time=1))
        # visual_action: ReplacementTransform step_label
        step_label_new3 = Text("Summary: A + B = C", color=YELLOW, font_size=28)
        step_label_new3.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_new3))
        self.objects["step_label"] = step_label_new3
        remaining_10 = max(0.1, 4.0 - (1 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_10))

        # Final hold
        self.wait(max(0.1, 2))