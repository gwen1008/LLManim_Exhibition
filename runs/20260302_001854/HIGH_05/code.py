'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate vector addition via the triangle (head-to-tail) method.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Step Indicator
#    - Main Content: [Center y=0] for coordinate grid and vectors
#    - Footer Region: [Bottom y=-3.5] for explanation and component display
# 3. Anti-Overlap Check:
#    - Use VGroups for vector+label pairs to keep them together.
#    - Position grid at ORIGIN, title at top, explanation at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Draw_vectors_A____3__92a8fc66ac/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Fade in grid.
#    - Step 2: Draw vector A, indicate it.
#    - Step 3: Draw vector B, indicate it.
#    - Step 4: Translate B to head of A, update step indicator.
#    - Step 5: Fill in triangle.
#    - Step 6: Draw resultant vector C.
#    - Step 7: Update component display, show resultant label, update step indicator.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout plan zones
        title_anchor = 3.5 * UP
        grid_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Vector Addition: The Triangle (Head-to-Tail) Method", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text
        
        # step_indicator
        step_indicator = Text("Step 1: Define Vectors A and B", color=YELLOW, font_size=28)
        step_indicator.next_to(title_text, DOWN, buff=0.3)
        self.objects["step_indicator"] = step_indicator
        
        # grid
        grid = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            stroke_opacity=0.5,
            color=GRAY
        )
        grid.move_to(grid_center)
        self.objects["grid"] = grid
        
        # vec_A
        vec_A = Arrow(start=[0,0,0], end=[3,1,0], color=BLUE, stroke_width=6, buff=0)
        vec_A.move_to(grid_center)
        self.objects["vec_A"] = vec_A
        
        # label_A
        label_A = MathTex(r"\vec{A}", color=BLUE, font_size=36)
        # Position will be set after vec_A is created, but we need to create it now.
        # We'll position it later when vec_A is added to scene.
        self.objects["label_A"] = label_A
        
        # vec_B_original
        vec_B_original = Arrow(start=[0,0,0], end=[1,2,0], color=RED, stroke_width=6, buff=0)
        vec_B_original.move_to(grid_center)
        self.objects["vec_B_original"] = vec_B_original
        
        # label_B_original
        label_B_original = MathTex(r"\vec{B}", color=RED, font_size=36)
        self.objects["label_B_original"] = label_B_original
        
        # vec_B_translated
        vec_B_translated = Arrow(start=[3,1,0], end=[4,3,0], color=RED, stroke_width=6, buff=0)
        vec_B_translated.move_to(grid_center + [3,1,0])
        vec_B_translated.set_opacity(0.0)
        self.objects["vec_B_translated"] = vec_B_translated
        
        # label_B_translated
        label_B_translated = MathTex(r"\vec{B}", color=RED, font_size=36)
        label_B_translated.set_opacity(0.0)
        self.objects["label_B_translated"] = label_B_translated
        
        # vec_C
        vec_C = Arrow(start=[0,0,0], end=[4,3,0], color=GREEN, stroke_width=8, buff=0)
        vec_C.move_to(grid_center)
        vec_C.set_opacity(0.0)
        self.objects["vec_C"] = vec_C
        
        # label_C
        label_C = MathTex(r"\vec{C} = \vec{A} + \vec{B}", color=GREEN, font_size=36)
        label_C.set_opacity(0.0)
        self.objects["label_C"] = label_C
        
        # triangle
        triangle = Polygon([0,0,0], [3,1,0], [4,3,0], color=WHITE, fill_opacity=0.2, stroke_opacity=0.0)
        triangle.move_to(grid_center)
        self.objects["triangle"] = triangle
        
        # explanation_text
        explanation_text = Text("Graphical Vector Addition:", color=GRAY_C, font_size=28)
        explanation_text.move_to(explanation_anchor + UP*0.5)
        self.objects["explanation_text"] = explanation_text
        
        # components_display
        components_display = MathTex(r"\vec{A} = (3,1),\quad \vec{B} = (1,2)", color=WHITE, font_size=32)
        components_display.next_to(explanation_text, DOWN, buff=0.3)
        self.objects["components_display"] = components_display
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_vectors_A____3__92a8fc66ac/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(FadeIn(self.objects["grid"]), run_time=1.5)
        remaining_1 = max(0.1, 5.52 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Draw_vectors_A____3__92a8fc66ac/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Signal action: Indicate vec_A
        self.play(Indicate(self.objects["vec_A"], color=YELLOW, run_time=1))
        # Visual action: Create vec_A
        self.play(Create(self.objects["vec_A"]), run_time=1.5)
        # Position and write label_A
        self.objects["label_A"].next_to(self.objects["vec_A"].get_end(), RIGHT, buff=0.15)
        self.play(Write(self.objects["label_A"]), run_time=0.8)
        # Also add title and step indicator (they should appear at the beginning)
        self.play(Write(self.objects["title_text"]), Write(self.objects["step_indicator"]), run_time=1.5)
        remaining_2 = max(0.1, 4.104 - (1 + 1.5 + 0.8 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Draw_vectors_A____3__92a8fc66ac/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate vec_B_original
        self.play(Indicate(self.objects["vec_B_original"], color=YELLOW, run_time=1))
        # Visual action: Create vec_B_original
        self.play(Create(self.objects["vec_B_original"]), run_time=1.5)
        # Position and write label_B_original
        self.objects["label_B_original"].next_to(self.objects["vec_B_original"].get_end(), UP, buff=0.15)
        self.play(Write(self.objects["label_B_original"]), run_time=0.8)
        remaining_3 = max(0.1, 4.056 - (1 + 1.5 + 0.8) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_vectors_A____3__92a8fc66ac/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe vec_A.get_end()
        # Create a temporary dot at the end of vec_A for circumscribing
        end_dot = Dot(self.objects["vec_A"].get_end(), radius=0.1, color=YELLOW)
        end_dot.set_opacity(0.0)  # Make it invisible
        self.add(end_dot)
        self.play(Circumscribe(end_dot, color=YELLOW, run_time=1))
        self.remove(end_dot)
        
        # Visual action: Transform vec_B_original to translated position
        # We'll create a copy for transformation, and simultaneously fade in the translated version
        vec_B_translated_copy = self.objects["vec_B_translated"].copy()
        vec_B_translated_copy.set_opacity(1.0)
        label_B_translated_copy = self.objects["label_B_translated"].copy()
        label_B_translated_copy.set_opacity(1.0)
        label_B_translated_copy.next_to(vec_B_translated_copy.get_end(), UP+RIGHT, buff=0.15)
        
        # Update step indicator
        step_indicator_2 = Text("Step 2: Translate B to head of A", color=YELLOW, font_size=28)
        step_indicator_2.next_to(self.objects["title_text"], DOWN, buff=0.3)
        
        self.play(
            Transform(self.objects["vec_B_original"], vec_B_translated_copy),
            FadeOut(self.objects["label_B_original"]),
            FadeIn(self.objects["vec_B_translated"]),
            FadeIn(self.objects["label_B_translated"]),
            ReplacementTransform(self.objects["step_indicator"], step_indicator_2),
            run_time=2.5
        )
        self.objects["step_indicator"] = step_indicator_2
        self.objects["label_B_translated"].next_to(self.objects["vec_B_translated"].get_end(), UP+RIGHT, buff=0.15)
        remaining_4 = max(0.1, 6.48 - (1 + 2.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Draw_vectors_A____3__92a8fc66ac/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate triangle
        self.play(Indicate(self.objects["triangle"], color=WHITE, run_time=1))
        # Visual action: Create triangle (fill)
        self.objects["triangle"].set_stroke(opacity=0.5)
        self.play(self.objects["triangle"].animate.set_fill(opacity=0.2), run_time=2.0)
        remaining_5 = max(0.1, 8.232 - (1 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/Draw_vectors_A____3__92a8fc66ac/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Indicate vec_C
        self.play(Indicate(self.objects["vec_C"], color=YELLOW, run_time=1))
        # Visual action: Create vec_C
        self.objects["vec_C"].set_opacity(1.0)
        self.play(Create(self.objects["vec_C"]), run_time=1.5)
        # Position and write label_C
        self.objects["label_C"].set_opacity(1.0)
        self.objects["label_C"].next_to(self.objects["vec_C"].get_end(), UP+LEFT, buff=0.2)
        self.play(Write(self.objects["label_C"]), run_time=1.0)
        remaining_6 = max(0.1, 5.088 - (1 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/Draw_vectors_A____3__92a8fc66ac/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe components_display
        self.play(Circumscribe(self.objects["components_display"], color=YELLOW, run_time=1))
        
        # Visual action: TransformMatchingTex components_display
        new_components = MathTex(r"\vec{A} = (3,1),\quad \vec{B} = (1,2),\quad \vec{C} = \vec{A}+\vec{B} = (4,3)", color=WHITE, font_size=32)
        new_components.next_to(self.objects["explanation_text"], DOWN, buff=0.3)
        
        # Update step indicator
        step_indicator_3 = Text("Step 3: The Resultant C = A + B", color=YELLOW, font_size=28)
        step_indicator_3.next_to(self.objects["title_text"], DOWN, buff=0.3)
        
        self.play(
            TransformMatchingTex(self.objects["components_display"], new_components),
            ReplacementTransform(self.objects["step_indicator"], step_indicator_3),
            run_time=3.0
        )
        self.objects["components_display"] = new_components
        self.objects["step_indicator"] = step_indicator_3
        
        # Also write explanation_text if not already shown
        self.play(Write(self.objects["explanation_text"]), run_time=1.0)
        
        remaining_7 = max(0.1, 14.064 - (1 + 3.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_7))