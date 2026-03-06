'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the head-to-tail method on a coordinate plane.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for coordinate plane and vectors
#    - Footer Region: [Bottom y=-3.5] for algebraic verification text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for vector+label pairs. Position labels relative to arrow ends.
#    - Ensure algebraic text is at bottom, not overlapping main diagram.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/vector_addition_head_to_tail/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show grid.
#    - Step 2: Draw vector A.
#    - Step 3: Label A, show faint vector B at origin.
#    - Step 4: Translate B to head of A.
#    - Step 5: Draw resultant vector C.
#    - Step 6: Label C.
#    - Step 7: Show algebraic verification.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_vectors_A____3__3da18626d1/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Vector Addition: Head-to-Tail Method", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Coordinate Plane
        coordinate_plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=7,
            stroke_opacity=0.5
        )
        coordinate_plane.move_to(content_center)
        self.objects["coordinate_plane"] = coordinate_plane
        
        # Vector A Arrow
        vector_a_arrow = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color=BLUE,
            stroke_width=6,
            buff=0
        )
        vector_a_arrow.move_to(content_center)
        self.objects["vector_a_arrow"] = vector_a_arrow
        
        # Label A
        label_a = MathTex(r"\vec{A} = (3,1)", color=BLUE, font_size=30)
        label_a.next_to(vector_a_arrow.get_end(), UP+RIGHT, buff=0.1)
        self.objects["label_a"] = label_a
        
        # Vector B Original Arrow (faint)
        vector_b_original_arrow = Arrow(
            start=[0, 0, 0],
            end=[1, 2, 0],
            color=GREEN_D,
            stroke_width=6,
            buff=0
        )
        vector_b_original_arrow.move_to(content_center)
        vector_b_original_arrow.set_opacity(0.5)
        self.objects["vector_b_original_arrow"] = vector_b_original_arrow
        
        # Label B Original (faint)
        label_b_original = MathTex(r"\vec{B} = (1,2)", color=GREEN_D, font_size=30)
        label_b_original.next_to(vector_b_original_arrow.get_end(), UP+LEFT, buff=0.1)
        label_b_original.set_opacity(0.5)
        self.objects["label_b_original"] = label_b_original
        
        # Vector B Translated Arrow (initially invisible)
        vector_b_translated_arrow = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color=GREEN,
            stroke_width=6,
            buff=0
        )
        vector_b_translated_arrow.move_to(content_center + [3, 1, 0])
        vector_b_translated_arrow.set_opacity(0.0)
        self.objects["vector_b_translated_arrow"] = vector_b_translated_arrow
        
        # Label B Translated (initially invisible)
        label_b_translated = MathTex(r"\vec{B}", color=GREEN, font_size=30)
        label_b_translated.next_to(vector_b_translated_arrow.get_end(), UP+LEFT, buff=0.1)
        label_b_translated.set_opacity(0.0)
        self.objects["label_b_translated"] = label_b_translated
        
        # Vector C Arrow (initially invisible)
        vector_c_arrow = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color=RED,
            stroke_width=8,
            buff=0
        )
        vector_c_arrow.move_to(content_center)
        vector_c_arrow.set_opacity(0.0)
        self.objects["vector_c_arrow"] = vector_c_arrow
        
        # Label C (initially invisible)
        label_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4,3)", color=RED, font_size=30)
        label_c.next_to(vector_c_arrow.get_end(), RIGHT, buff=0.2)
        label_c.set_opacity(0.0)
        self.objects["label_c"] = label_c
        
        # Algebraic Text (initially invisible)
        algebraic_text = MathTex(r"(3,1) + (1,2) = (3+1, 1+2) = (4,3)", color=YELLOW, font_size=36)
        algebraic_text.move_to(explanation_anchor)
        algebraic_text.set_opacity(0.0)
        self.objects["algebraic_text"] = algebraic_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/vector_addition_head_to_tail/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["coordinate_plane"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/vector_addition_head_to_tail/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["vector_a_arrow"], color=BLUE, run_time=1))
        self.play(GrowArrow(self.objects["vector_a_arrow"]), run_time=1.0)
        remaining_2 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/vector_addition_head_to_tail/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_a"]), run_time=0.5)
        self.play(FadeIn(self.objects["vector_b_original_arrow"]), run_time=1.0)
        self.play(FadeIn(self.objects["label_b_original"]), run_time=1.0)
        remaining_3 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/vector_addition_head_to_tail/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["vector_b_original_arrow"], color=YELLOW, run_time=1))
        # Create the translated B arrow (visible) and transform original to it
        self.objects["vector_b_translated_arrow"].set_opacity(1.0)
        self.objects["label_b_translated"].set_opacity(1.0)
        self.play(
            Transform(self.objects["vector_b_original_arrow"], self.objects["vector_b_translated_arrow"]),
            Transform(self.objects["label_b_original"], self.objects["label_b_translated"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/vector_addition_head_to_tail/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["vector_b_translated_arrow"], color=GREEN, run_time=1))
        self.objects["vector_c_arrow"].set_opacity(1.0)
        self.play(GrowArrow(self.objects["vector_c_arrow"]), run_time=1.5)
        remaining_5 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/vector_addition_head_to_tail/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_c"].set_color(RED)), run_time=0.5)
        self.objects["label_c"].set_opacity(1.0)
        self.play(FadeIn(self.objects["label_c"]), run_time=1.5)
        remaining_6 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/vector_addition_head_to_tail/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["label_c"], color=RED, run_time=1))
        self.objects["algebraic_text"].set_opacity(1.0)
        self.play(FadeIn(self.objects["algebraic_text"]), run_time=2.0)
        remaining_7 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # Final hold
        self.wait(max(0.1, 2))