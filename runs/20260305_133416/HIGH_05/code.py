'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually explain vector addition using the head-to-tail (triangle) method, showing the equivalence of the two-step path (A then B) and the direct resultant vector C.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for NumberPlane and vectors
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for vector lines and labels. Position labels relative to arrow ends with buff. Keep main content centered.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Create axes, origin dot, and label.
#    - Step 2: Draw vector A, its label, and endpoint dot.
#    - Step 3: Highlight connection point, draw vector B, its label, and final dot.
#    - Step 4: Draw resultant vector C, its label, and circumscribe triangle vertices.
#    - Step 5: Trace dashed path O->A->C, morph it into solid vector C, then fade out the trace.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/To_animate_the_vecto_b5998201b6/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan description (High-Low Split)
        title_anchor = 3.5 * UP
        step_label_anchor = 3.0 * UP  # Just below title
        main_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Vector Addition: Triangle (Head-to-Tail) Method", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Step Label
        step_label = Text("Step 1: Setup", color=GRAY, font_size=24)
        step_label.next_to(title, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # Axes (NumberPlane)
        axes = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=10,
            color="#333333"
        )
        axes.move_to(main_anchor)
        self.objects["axes"] = axes

        # Origin Dot
        origin_dot = Dot(radius=0.08, color=WHITE)
        origin_dot.move_to(main_anchor)
        self.objects["origin_dot"] = origin_dot

        # Origin Label
        origin_label = MathTex("O", color=WHITE, font_size=24)
        origin_label.next_to(origin_dot, DOWN + LEFT, buff=0.1)
        self.objects["origin_label"] = origin_label

        # Vector A Line (Arrow)
        vec_A_line = Arrow(start=[0, 0, 0], end=[3, 1, 0], color="#1E88E5", stroke_width=6, buff=0)
        vec_A_line.move_to(main_anchor)  # Position relative to main_anchor
        self.objects["vec_A_line"] = vec_A_line

        # Vector A Label
        vec_A_label = MathTex(r"\vec{A} = (3, 1)", color="#1E88E5", font_size=28)
        # Position will be set relative to vec_A_line.get_end() later, after creation
        self.objects["vec_A_label"] = vec_A_label

        # Point A Dot
        point_A_dot = Dot(radius=0.08, color="#1E88E5")
        point_A_dot.move_to([3, 1, 0])
        self.objects["point_A_dot"] = point_A_dot

        # Vector B Line
        vec_B_line = Arrow(start=[3, 1, 0], end=[4, 3, 0], color="#4CAF50", stroke_width=6, buff=0)
        vec_B_line.move_to(main_anchor)
        self.objects["vec_B_line"] = vec_B_line

        # Vector B Label
        vec_B_label = MathTex(r"\vec{B} = (1, 2)", color="#4CAF50", font_size=28)
        self.objects["vec_B_label"] = vec_B_label

        # Point C Dot
        point_C_dot = Dot(radius=0.08, color="#FFD600")
        point_C_dot.move_to([4, 3, 0])
        self.objects["point_C_dot"] = point_C_dot

        # Vector C Line (Resultant)
        vec_C_line = Arrow(start=[0, 0, 0], end=[4, 3, 0], color="#FFD600", stroke_width=8, buff=0)
        vec_C_line.move_to(main_anchor)
        self.objects["vec_C_line"] = vec_C_line

        # Vector C Label
        vec_C_label = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color="#FFD600", font_size=28)
        self.objects["vec_C_label"] = vec_C_label

        # Path Trace (DashedLine) - Start as O->A, will be transformed
        path_trace = DashedLine(start=[0, 0, 0], end=[3, 1, 0], color="#AAAAAA", stroke_width=4, dash_length=0.1)
        path_trace.move_to(main_anchor)
        self.objects["path_trace"] = path_trace

        # Explanation Text
        explanation_text = Text("Drawing the coordinate axes and the origin.", color=GRAY_C, font_size=22)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # Narrative: "We begin with a coordinate system and mark the origin, point O."
        # signal_action: null
        # visual_action: Create axes
        self.play(Create(self.objects["axes"]), run_time=1.5)
        self.play(Create(self.objects["origin_dot"]), Write(self.objects["origin_label"]), run_time=0.5)
        # Write title and step label
        self.play(Write(self.objects["title"]), Write(self.objects["step_label"]), Write(self.objects["explanation_text"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - (1.5 + 0.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # Narrative: "Now, draw vector A from the origin to the point (3, 1)."
        # signal_action: UpdateText step_label
        self.objects["step_label"].become(Text("Step 2: Draw Vector A", color=GRAY, font_size=24).next_to(self.objects["title"], DOWN, buff=0.3))
        self.objects["explanation_text"].become(Text("Now, draw vector A from the origin to the point (3, 1).", color=GRAY_C, font_size=22).move_to(explanation_anchor))
        # Position vec_A_label relative to vec_A_line's end (which exists now)
        self.objects["vec_A_label"].next_to(self.objects["vec_A_line"].get_end(), UP + RIGHT, buff=0.2)
        # visual_action: Create vec_A_line, Write vec_A_label, Create point_A_dot
        self.play(Create(self.objects["vec_A_line"]), run_time=1.0)
        self.play(Write(self.objects["vec_A_label"]), Create(self.objects["point_A_dot"]), run_time=1.0)
        remaining_2 = max(0.1, 3.0 - (1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # Narrative: "Next, we add vector B using the head-to-tail method..."
        # signal_action: UpdateText step_label
        self.objects["step_label"].become(Text("Step 3: Add Vector B (Head-to-Tail)", color=GRAY, font_size=24).next_to(self.objects["title"], DOWN, buff=0.3))
        self.objects["explanation_text"].become(Text("Next, we add vector B using the head-to-tail method. Place its tail at the head of vector A, and draw it to the point (4, 3).", color=GRAY_C, font_size=22).move_to(explanation_anchor))
        # signal_action: Indicate point_A_dot
        self.play(Indicate(self.objects["point_A_dot"], color=YELLOW, run_time=1))
        # Position vec_B_label
        self.objects["vec_B_label"].next_to(self.objects["vec_B_line"].get_end(), UP + LEFT, buff=0.2)
        # visual_action: Create vec_B_line, Write vec_B_label, Create point_C_dot
        self.play(Create(self.objects["vec_B_line"]), run_time=1.5)
        self.play(Write(self.objects["vec_B_label"]), Create(self.objects["point_C_dot"]), run_time=1.0)
        remaining_3 = max(0.1, 4.0 - (1.0 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # Narrative: "The resultant vector, C, is the vector from the start of the journey..."
        # signal_action: UpdateText step_label
        self.objects["step_label"].become(Text("Step 4: The Resultant Vector C", color=GRAY, font_size=24).next_to(self.objects["title"], DOWN, buff=0.3))
        self.objects["explanation_text"].become(Text("The resultant vector, C, is the vector from the start of the journey, the origin, to the end point. This is the sum of vectors A and B.", color=GRAY_C, font_size=22).move_to(explanation_anchor))
        # Position vec_C_label
        self.objects["vec_C_label"].next_to(self.objects["vec_C_line"].get_end(), DOWN + RIGHT, buff=0.3)
        # visual_action: Create vec_C_line, Write vec_C_label, Circumscribe vertices
        self.play(Create(self.objects["vec_C_line"]), run_time=1.5)
        self.play(Write(self.objects["vec_C_label"]), run_time=1.0)
        # Circumscribe the three dots
        circum_group = VGroup(self.objects["origin_dot"], self.objects["point_A_dot"], self.objects["point_C_dot"])
        self.play(Circumscribe(circum_group, color=PINK, run_time=1.5))
        remaining_4 = max(0.1, 4.0 - (1.5 + 1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # Narrative: "Observe how the two-step path along A and then B is equivalent..."
        # signal_action: UpdateText step_label
        self.objects["step_label"].become(Text("Step 5: Equivalence of Paths", color=GRAY, font_size=24).next_to(self.objects["title"], DOWN, buff=0.3))
        self.objects["explanation_text"].become(Text("Observe how the two-step path along A and then B is equivalent to the single direct step along the resultant vector C. This is the essence of vector addition.", color=GRAY_C, font_size=22).move_to(explanation_anchor))
        # visual_action: Create path_trace (O->A), Transform to O->A->C, Transform to solid C, FadeOut
        # Create initial dashed line O->A
        self.play(Create(self.objects["path_trace"]), run_time=1.0)
        # Transform to extend to point C (O->A->C)
        path_trace_extended = DashedLine(start=[0, 0, 0], end=[4, 3, 0], color="#AAAAAA", stroke_width=4, dash_length=0.1)
        path_trace_extended.move_to(main_anchor)
        self.play(Transform(self.objects["path_trace"], path_trace_extended), run_time=1.5)
        # Morph dashed line into solid yellow resultant vector C
        self.play(Transform(self.objects["path_trace"], self.objects["vec_C_line"].copy().set_color("#FFD600")), run_time=1.5)
        # Fade out the trace
        self.play(FadeOut(self.objects["path_trace"]), run_time=0.5)
        remaining_5 = max(0.1, 5.0 - (1.0 + 1.5 + 1.5 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_5))