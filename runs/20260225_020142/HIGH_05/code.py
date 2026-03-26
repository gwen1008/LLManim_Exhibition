from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create Anchors (from layout_plan.anchors)
        title_anchor = 3.5 * UP
        global_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Helper to parse position strings (simplified for this specific JSON)
        def parse_position(pos_str, ref_dict):
            if pos_str == "move_to(title_anchor)":
                return title_anchor
            elif pos_str == "move_to(global_center)":
                return global_center
            elif pos_str == "move_to(explanation_anchor)":
                return explanation_anchor
            elif pos_str == "next_to(title_text, DOWN, buff=0.5)":
                # title_text not created yet, will handle after creation
                return None  # Placeholder, will set later
            elif "next_to" in pos_str and "get_end" in pos_str:
                # These depend on other objects, will set after creation
                return None
            elif pos_str == "move_to([3,1,0])":
                return np.array([3, 1, 0])
            else:
                return ORIGIN

        # Create objects from layout_plan.objects
        # Object: title_text
        title_text = Text("Vector Addition: The Triangle Rule", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # Object: axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            axis_config={"include_numbers": True, "stroke_color": GREY},
            x_length=8,
            y_length=8,
        ).scale(0.8).move_to(global_center)
        self.objects["axes"] = axes

        # Object: vec_a
        vec_a = Arrow(start=[0,0,0], end=[3,1,0], buff=0, color=BLUE, stroke_width=6)
        vec_a.move_to(global_center)
        self.objects["vec_a"] = vec_a

        # Object: label_a
        label_a = MathTex(r"\vec{A} = (3,1)", color=BLUE).scale(0.8)
        self.objects["label_a"] = label_a

        # Object: vec_b
        vec_b = Arrow(start=[0,0,0], end=[1,2,0], buff=0, color=GREEN, stroke_width=6)
        vec_b.move_to(global_center)
        self.objects["vec_b"] = vec_b

        # Object: label_b
        label_b = MathTex(r"\vec{B} = (1,2)", color=GREEN).scale(0.8)
        self.objects["label_b"] = label_b

        # Object: vec_b_translated
        vec_b_translated = Arrow(start=[3,1,0], end=[4,3,0], buff=0, color=GREEN, stroke_width=6)
        vec_b_translated.set_opacity(0.0)
        vec_b_translated.move_to(vec_a.get_end())
        self.objects["vec_b_translated"] = vec_b_translated

        # Object: label_b_translated
        label_b_translated = MathTex(r"\vec{B}", color=GREEN).scale(0.8)
        label_b_translated.set_opacity(0.0)
        self.objects["label_b_translated"] = label_b_translated

        # Object: vec_c
        vec_c = Arrow(start=[0,0,0], end=[4,3,0], buff=0, color=RED, stroke_width=8)
        vec_c.set_opacity(0.0)
        vec_c.move_to(global_center)
        self.objects["vec_c"] = vec_c

        # Object: label_c
        label_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4,3)", color=RED).scale(0.8)
        label_c.set_opacity(0.0)
        self.objects["label_c"] = label_c

        # Object: triangle
        triangle = Polygon([0,0,0], [3,1,0], [4,3,0], color=YELLOW, fill_opacity=0.2)
        triangle.set_stroke(opacity=0.0)
        triangle.move_to(global_center)
        self.objects["triangle"] = triangle

        # Object: step_label
        step_label = Text("Step 1: Setup", color=GRAY, font_size=24)
        self.objects["step_label"] = step_label

        # Object: explanation_text
        explanation_text = Text("We begin with two vectors, A and B, drawn from the origin.", color=GREY, font_size=22)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # Now set positions that depend on other objects
        label_a.next_to(vec_a.get_end(), RIGHT, buff=0.15)
        label_b.next_to(vec_b.get_end(), UP, buff=0)
        label_b_translated.next_to(vec_b_translated.get_end(), LEFT+UP, buff=0.15)
        label_c.next_to(vec_c.get_end(), UP, buff=0.5)
        step_label.next_to(title_text, DOWN, buff=0.5)

        # Create VGroups for vector+label pairs for transformation
        vec_b_group = VGroup(vec_b, label_b)
        vec_b_translated_group = VGroup(vec_b_translated, label_b_translated)
        self.objects["vec_b_group"] = vec_b_group
        self.objects["vec_b_translated_group"] = vec_b_translated_group

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(title_text), Write(step_label), Write(explanation_text), run_time=1.5)
        self.play(Create(axes), run_time=2.0)
        remaining_1 = max(0.1, 8.952 - 1.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(vec_a, color=BLUE, run_time=1))
        self.play(Create(vec_a), Write(label_a), run_time=1.5)
        remaining_2 = max(0.1, 5.52 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(vec_b, color=GREEN, run_time=1))
        self.play(Create(vec_b), Write(label_b), run_time=1.5)
        remaining_3 = max(0.1, 3.696 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(label_a, color=YELLOW, run_time=1))
        step_label_new = Text("Step 2: Triangle Rule", color=GRAY, font_size=24)
        step_label_new.next_to(title_text, DOWN, buff=0.5)
        self.play(ReplacementTransform(step_label, step_label_new))
        step_label = step_label_new
        self.objects["step_label"] = step_label
        explanation_new = Text("Translate vector B to start at the head of A.", color=GREY, font_size=22)
        explanation_new.move_to(explanation_anchor)
        self.play(ReplacementTransform(explanation_text, explanation_new))
        explanation_text = explanation_new
        self.objects["explanation_text"] = explanation_text
        remaining_4 = max(0.1, 6.432 - 1.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        vec_b_translated_group.set_opacity(1)
        self.play(Transform(vec_b_group, vec_b_translated_group), run_time=2.0)
        self.objects["vec_b_group"] = vec_b_translated_group
        remaining_5 = max(0.1, 7.392 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Create(triangle, run_time=1))
        self.play(triangle.animate.set_stroke(opacity=1.0), run_time=0.5)
        explanation_new2 = Text("The triangle shows the path: A, then B. The sum is the direct path.", color=GREY, font_size=22)
        explanation_new2.move_to(explanation_anchor)
        self.play(ReplacementTransform(explanation_text, explanation_new2))
        explanation_text = explanation_new2
        self.objects["explanation_text"] = explanation_text
        remaining_6 = max(0.1, 9.168 - 1.0 - 0.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Indicate(triangle, color=YELLOW, run_time=1))
        self.play(vec_c.animate.set_opacity(1.0), run_time=1.5)
        explanation_new3 = Text("The resultant vector C goes from start to finish.", color=GREY, font_size=22)
        explanation_new3.move_to(explanation_anchor)
        self.play(ReplacementTransform(explanation_text, explanation_new3))
        explanation_text = explanation_new3
        self.objects["explanation_text"] = explanation_text
        remaining_7 = max(0.1, 8.256 - 1.0 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        self.play(Circumscribe(label_c, color=RED, run_time=1))
        self.play(label_c.animate.set_opacity(1.0), run_time=1.0)
        explanation_new4 = Text("C = A + B: (3+1, 1+2) = (4,3).", color=GREY, font_size=22)
        explanation_new4.move_to(explanation_anchor)
        self.play(ReplacementTransform(explanation_text, explanation_new4), run_time=1.0)
        remaining_8 = max(0.1, 11.472 - 1.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Final pause
        self.wait(max(0.1, 2))