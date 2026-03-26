'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the head-to-tail method and compute vector magnitudes via the Pythagorean Theorem, connecting geometric and algebraic representations.
# 2. Layout Strategy: Use High-Low Split.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for coordinate axes, vectors, and triangles.
#    - Footer Region: [Bottom y=-3.5] for step explanations and magnitude equations.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for composite objects (e.g., vector + label). Position magnitude equations at the bottom, centered, using ReplacementTransform to avoid stacking.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-2: Draw axes and vector A.
#    - Step 3-4: Show triangle for A and its magnitude.
#    - Step 5-6: Draw vector B, show its triangle and magnitude.
#    - Step 7: Slide vector B to origin.
#    - Step 8-10: Show resultant vector C, its triangle, label, and magnitude.
#    - Step 11: Fade out explanation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors (zones)
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Helper to parse position strings (simplified for this blueprint)
        def parse_pos(pos_str, ref_obj=None):
            if pos_str == "move_to(title_anchor)":
                return title_anchor
            elif pos_str == "move_to(content_center)":
                return content_center
            elif pos_str == "move_to(explanation_anchor)":
                return explanation_anchor
            elif pos_str.startswith("next_to"):
                # Simplified parsing for the given strings
                if "vector_a.get_center()" in pos_str:
                    base = self.objects["vector_a"].get_center()
                    dir = UP
                    buff = 0.2
                    if "LEFT*0.5" in pos_str:
                        return base + dir * buff + LEFT * 0.5
                    return base + dir * buff
                elif "vector_b.get_center()" in pos_str:
                    base = self.objects["vector_b"].get_center()
                    dir = UP
                    buff = 0.2
                    return base + dir * buff
                elif "vector_c.get_center()" in pos_str:
                    base = self.objects["vector_c"].get_center()
                    dir = LEFT
                    buff = 0.3
                    return base + dir * buff
                elif "content_center + DOWN*2.5" in pos_str:
                    return content_center + 2.5 * DOWN
            return ORIGIN

        # Create objects from layout_plan.objects
        # title
        title = Text("Vector Addition: Head-to-Tail Method & Magnitudes", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": LIGHT_GRAY}
        ).move_to(content_center)
        self.objects["axes"] = axes

        # vector_a
        vector_a = Arrow(start=[0,0,0], end=[3,1,0], color=BLUE, stroke_width=6, buff=0).move_to(content_center)
        self.objects["vector_a"] = vector_a

        # vector_b (initial position)
        vector_b = Arrow(start=[3,1,0], end=[4,3,0], color=GREEN, stroke_width=6, buff=0).move_to(content_center)
        self.objects["vector_b"] = vector_b

        # vector_c (initially invisible)
        vector_c = Arrow(start=[0,0,0], end=[4,3,0], color=RED, stroke_width=8, buff=0).move_to(content_center)
        vector_c.set_opacity(0)
        self.objects["vector_c"] = vector_c

        # triangle_a
        tri_a_verts = [[0,0,0], [3,0,0], [3,1,0]]
        triangle_a = Polygon(*tri_a_verts, color=BLUE, fill_opacity=0.2, stroke_width=3).move_to(content_center)
        triangle_a.set_opacity(0)
        self.objects["triangle_a"] = triangle_a

        # triangle_b
        tri_b_verts = [[3,1,0], [4,1,0], [4,3,0]]
        triangle_b = Polygon(*tri_b_verts, color=GREEN, fill_opacity=0.2, stroke_width=3).move_to(content_center)
        triangle_b.set_opacity(0)
        self.objects["triangle_b"] = triangle_b

        # triangle_c
        tri_c_verts = [[0,0,0], [4,0,0], [4,3,0]]
        triangle_c = Polygon(*tri_c_verts, color=RED, fill_opacity=0.2, stroke_width=3).move_to(content_center)
        triangle_c.set_opacity(0)
        self.objects["triangle_c"] = triangle_c

        # label_a
        label_a = MathTex(r"\vec{A} = (3,1)", color=BLUE)
        label_a.next_to(vector_a.get_center(), UP, buff=0.2).shift(LEFT*0.5)
        self.objects["label_a"] = label_a

        # label_b
        label_b = MathTex(r"\vec{B} = (1,2)", color=GREEN)
        label_b.next_to(vector_b.get_center(), UP, buff=0.2)
        self.objects["label_b"] = label_b

        # label_c
        label_c = MathTex(r"\vec{C} = (4,3)", color=RED)
        label_c.next_to(vector_c.get_center(), LEFT, buff=0.3)
        label_c.set_opacity(0)
        self.objects["label_c"] = label_c

        # magnitude_eq_a
        magnitude_eq_a = MathTex(r"|\vec{A}| = \sqrt{3^2 + 1^2} = \sqrt{10}", color=BLUE)
        magnitude_eq_a.move_to(vector_a.get_center() + UP*0.3)
        magnitude_eq_a.set_opacity(0)
        self.objects["magnitude_eq_a"] = magnitude_eq_a

        # magnitude_eq_b
        magnitude_eq_b = MathTex(r"|\vec{B}| = \sqrt{1^2 + 2^2} = \sqrt{5}", color=GREEN)
        magnitude_eq_b.move_to(content_center + 2.5 * DOWN)
        magnitude_eq_b.set_opacity(0)
        self.objects["magnitude_eq_b"] = magnitude_eq_b

        # magnitude_eq_c
        magnitude_eq_c = MathTex(r"|\vec{C}| = \sqrt{4^2 + 3^2} = 5", color=RED)
        magnitude_eq_c.move_to(content_center + 2.5 * DOWN)
        magnitude_eq_c.set_opacity(0)
        self.objects["magnitude_eq_c"] = magnitude_eq_c

        # step_explanation
        step_explanation = Text("Step 1: Draw coordinate system and vector A.", color=WHITE, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["axes"]))
        self.play(Write(self.objects["step_explanation"]))
        animation_time = 2.0 + 2.0 + 1.0  # Estimate for Write+Create+Write
        remaining = 7.512 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["vector_a"]))
        self.play(Write(self.objects["label_a"]))
        # Update explanation (simplified: create new text)
        new_explanation = Text("Step 2: Vector A has components (3,1).", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.5 + 1.0 + 1.0
        remaining = 6.888 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["vector_a"], color=YELLOW))
        self.play(self.objects["triangle_a"].animate.set_opacity(1))
        new_explanation = Text("Step 3: Visualize the right triangle for A's components.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.0 + 1.0 + 1.0
        remaining = 8.184 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["triangle_a"], color=YELLOW, run_time=1))
        self.play(self.objects["magnitude_eq_a"].animate.set_opacity(1))
        new_explanation = Text("Step 4: Calculate magnitude of A using Pythagorean Theorem.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.0 + 1.0 + 1.0
        remaining = 8.064 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["vector_b"]))
        self.play(Write(self.objects["label_b"]))
        new_explanation = Text("Step 5: Draw vector B from the tip of A.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.5 + 1.0 + 1.0
        remaining = 7.512 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["vector_b"], color=YELLOW))
        self.play(self.objects["triangle_b"].animate.set_opacity(1))
        # Transform magnitude equation
        self.play(ReplacementTransform(self.objects["magnitude_eq_a"], self.objects["magnitude_eq_b"]))
        new_explanation = Text("Step 6: Triangle and magnitude for B.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.0 + 1.0 + 1.0 + 1.0
        remaining = 6.6 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 7
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["vector_b"], color=YELLOW))
        # Create a copy of vector_b at origin for transformation
        vector_b_at_origin = Arrow(start=[0,0,0], end=[1,2,0], color=GREEN, stroke_width=6, buff=0).move_to(content_center)
        self.play(Transform(self.objects["vector_b"], vector_b_at_origin))
        # Update label_b position (simplified: create new label)
        label_b_new = MathTex(r"\vec{B} = (1,2)", color=GREEN)
        label_b_new.next_to(vector_b_at_origin.get_center(), UP, buff=0.2)
        self.play(Transform(self.objects["label_b"], label_b_new))
        new_explanation = Text("Step 7: Slide vector B to start at origin.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.0 + 2.0 + 1.0 + 1.0
        remaining = 7.176 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 8
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(self.objects["vector_c"].animate.set_opacity(1))
        new_explanation = Text("Step 8: The resultant vector C is the sum.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.5 + 1.0
        remaining = 5.664 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 9
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["vector_c"], color=YELLOW, run_time=1))
        self.play(self.objects["triangle_c"].animate.set_opacity(1))
        self.play(self.objects["label_c"].animate.set_opacity(1))
        new_explanation = Text("Step 9: Components of C are (4,3) = (3,1)+(1,2).", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.0 + 1.0 + 1.0 + 1.0
        remaining = 7.368 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 10
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_09.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["triangle_c"], color=YELLOW))
        self.play(ReplacementTransform(self.objects["magnitude_eq_b"], self.objects["magnitude_eq_c"]))
        new_explanation = Text("Step 10: Calculate magnitude of C: sqrt(4^2+3^2)=5.", color=WHITE, font_size=24).move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        animation_time = 1.0 + 1.0 + 1.0
        remaining = 9.168 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 11
        audio_file = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_10.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(FadeOut(self.objects["step_explanation"]))
        animation_time = 1.0
        remaining = 7.176 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))