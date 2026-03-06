'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate vector addition using the head-to-tail (triangle) method.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for coordinate plane and vectors, slightly lowered to y=-0.5
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check:
#    - Use VGroups for component lines and labels to keep them together.
#    - Position labels with buff to avoid overlapping vectors.
#    - Fill triangle has low opacity and is behind vectors (z_index).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/vector_addition_triangle_method/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create coordinate plane.
#    - Step 2: Create vector A with Indicate signal.
#    - Step 3: Show label and dashed components for A.
#    - Step 4: Create vector B from head of A.
#    - Step 5: Create resultant vector C.
#    - Step 6: Fill triangle to solidify geometric interpretation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN + DOWN * 0.5
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Vector Addition: The Triangle Method", font_size=36, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Coordinate Plane
        coord_plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"stroke_opacity": 1},
            background_line_style={"stroke_opacity": 0.3}
        )
        coord_plane.move_to(content_center)
        self.objects["coord_plane"] = coord_plane
        
        # Vector A
        vec_a = Arrow(start=[0, 0, 0], end=[3, 1, 0], buff=0, color="#1E90FF", stroke_width=6)
        self.objects["vec_a"] = vec_a
        
        # Label for A
        label_a = MathTex(r"\vec{A} = (3, 1)", color="#1E90FF", font_size=28)
        # Position will be set after vec_a is created
        self.objects["label_a"] = label_a
        
        # Component lines for A (dashed)
        a_x_component = DashedLine(start=[0, 0, 0], end=[3, 0, 0], color="#1E90FF", stroke_width=3, stroke_opacity=0.7, dash_length=0.1)
        self.objects["a_x_component"] = a_x_component
        a_y_component = DashedLine(start=[3, 0, 0], end=[3, 1, 0], color="#1E90FF", stroke_width=3, stroke_opacity=0.7, dash_length=0.1)
        self.objects["a_y_component"] = a_y_component
        
        # Vector B
        vec_b = Arrow(start=[3, 1, 0], end=[4, 3, 0], buff=0, color="#32CD32", stroke_width=6)
        self.objects["vec_b"] = vec_b
        
        # Label for B
        label_b = MathTex(r"\vec{B} = (1, 2)", color="#32CD32", font_size=28)
        self.objects["label_b"] = label_b
        
        # Vector C (resultant)
        vec_c = Arrow(start=[0, 0, 0], end=[4, 3, 0], buff=0, color="#FF8C00", stroke_width=8)
        self.objects["vec_c"] = vec_c
        
        # Label for C
        label_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color="#FF8C00", font_size=32)
        self.objects["label_c"] = label_c
        
        # Triangle fill
        triangle_fill = Polygon([0, 0, 0], [3, 1, 0], [4, 3, 0], color="#FFD700", fill_opacity=0.3, stroke_width=0)
        triangle_fill.set_z_index(-1)  # Behind vectors
        self.objects["triangle_fill"] = triangle_fill
        
        # Step explanation text (will be updated)
        step_explanation = Text("Step 1: Establish the coordinate system.", font_size=24, color=GRAY_C)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # Group for A details (label and components)
        group_a_details = VGroup(label_a, a_x_component, a_y_component)
        self.objects["group_a_details"] = group_a_details
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Animate_the_vector_a_ece8e59c8d/step_00.mp3")  # [auto-injected]
        # Step 1: Create coordinate plane
        audio_step1 = "media/audio/vector_addition_triangle_method/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(coord_plane), Write(step_explanation), run_time=2.0)
        remaining_1 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Animate_the_vector_a_ece8e59c8d/step_01.mp3")  # [auto-injected]
        # Step 2: Introduce vector A
        audio_step2 = "media/audio/vector_addition_triangle_method/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Update explanation
        new_explanation_2 = Text("Step 2: Introduce vector A from origin to (3,1).", font_size=24, color=GRAY_C)
        new_explanation_2.move_to(explanation_anchor)
        self.play(Transform(step_explanation, new_explanation_2))
        
        # Signal action: Indicate vec_a
        self.play(Indicate(vec_a, color=YELLOW, run_time=1))
        # Visual action: Create vec_a
        self.play(Create(vec_a), run_time=1.5)
        remaining_2 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Animate_the_vector_a_ece8e59c8d/step_02.mp3")  # [auto-injected]
        # Step 3: Show label and components for A
        audio_step3 = "media/audio/vector_addition_triangle_method/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        new_explanation_3 = Text("Step 3: Label A and show its components (3,1).", font_size=24, color=GRAY_C)
        new_explanation_3.move_to(explanation_anchor)
        self.play(Transform(step_explanation, new_explanation_3))
        
        # Position label_a relative to vec_a
        label_a.next_to(vec_a.get_end(), UP+RIGHT, buff=0.2)
        
        # Signal action: Circumscribe label_a
        self.play(Circumscribe(label_a, color=YELLOW, run_time=1))
        # Visual action: Write label and create components simultaneously
        self.play(
            Write(label_a),
            Create(a_x_component),
            Create(a_y_component),
            run_time=2.0
        )
        remaining_3 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Animate_the_vector_a_ece8e59c8d/step_03.mp3")  # [auto-injected]
        # Step 4: Place vector B
        audio_step4 = "media/audio/vector_addition_triangle_method/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        new_explanation_4 = Text("Step 4: Place vector B from head of A to (4,3).", font_size=24, color=GRAY_C)
        new_explanation_4.move_to(explanation_anchor)
        self.play(Transform(step_explanation, new_explanation_4))
        
        # Signal action: Indicate start of vec_b (head of A)
        start_dot = Dot(vec_a.get_end(), color=RED)
        self.play(FadeIn(start_dot, run_time=0.5))
        self.play(FadeOut(start_dot, run_time=0.5))
        
        # Visual action: Create vec_b and its label
        self.play(Create(vec_b), run_time=1.5)
        # Position label_b
        label_b.next_to(vec_b.get_end(), UP+LEFT, buff=0.2)
        self.play(Write(label_b), run_time=1.0)
        remaining_4 = max(0.1, 3.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Animate_the_vector_a_ece8e59c8d/step_04.mp3")  # [auto-injected]
        # Step 5: Draw resultant vector C
        audio_step5 = "media/audio/vector_addition_triangle_method/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        new_explanation_5 = Text("Step 5: The resultant C is the direct path from start to finish.", font_size=24, color=GRAY_C)
        new_explanation_5.move_to(explanation_anchor)
        self.play(Transform(step_explanation, new_explanation_5))
        
        # Signal action: Indicate vec_c
        self.play(Indicate(vec_c, color=YELLOW, run_time=1))
        # Visual action: Create vec_c and its label
        self.play(Create(vec_c), run_time=1.5)
        # Position label_c
        label_c.next_to(vec_c.get_end(), DOWN+RIGHT, buff=0.3)
        self.play(Write(label_c), run_time=1.0)
        remaining_5 = max(0.1, 3.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Animate_the_vector_a_ece8e59c8d/step_05.mp3")  # [auto-injected]
        # Step 6: Fill triangle
        audio_step6 = "media/audio/vector_addition_triangle_method/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        new_explanation_6 = Text("Step 6: The triangle shows A + B = C geometrically.", font_size=24, color=GRAY_C)
        new_explanation_6.move_to(explanation_anchor)
        self.play(Transform(step_explanation, new_explanation_6))
        
        # Signal action: Indicate triangle_fill
        self.play(Indicate(triangle_fill, color=WHITE, run_time=1))
        # Visual action: Create triangle fill
        self.play(FadeIn(triangle_fill), run_time=2.0)
        remaining_6 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Final hold
        self.wait(max(0.1, 2))