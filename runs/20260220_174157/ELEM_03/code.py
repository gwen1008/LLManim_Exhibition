from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Area vs. Perimeter: A 4x3 Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Rectangle outline (Polygon)
        rect_vertices = [(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0)]
        rect_outline = Polygon(*rect_vertices, color=WHITE, stroke_width=6)
        rect_outline.move_to(content_center)
        self.objects["rect_outline"] = rect_outline
        
        # Width label (4)
        dim_label_w = MathTex("4", color=YELLOW, font_size=28)
        # Position: next_to rectangle bottom, DOWN, buff=0.2, align to content_center LEFT, shift RIGHT*1.0
        dim_label_w.next_to(rect_outline.get_bottom(), DOWN, buff=0.2)
        dim_label_w.align_to(content_center, LEFT)
        dim_label_w.shift(RIGHT * 1.0)
        self.objects["dim_label_w"] = dim_label_w
        
        # Height label (3)
        dim_label_h = MathTex("3", color=YELLOW, font_size=28)
        # Position: next_to rectangle left, LEFT, buff=0.2, align to content_center DOWN, shift UP*0.75
        dim_label_h.next_to(rect_outline.get_left(), LEFT, buff=0.2)
        dim_label_h.align_to(content_center, DOWN)
        dim_label_h.shift(UP * 0.75)
        self.objects["dim_label_h"] = dim_label_h
        
        # Fill squares VGroup (initially empty, populated in step 3)
        fill_squares_vgroup = VGroup()
        fill_squares_vgroup.move_to(content_center)
        self.objects["fill_squares_vgroup"] = fill_squares_vgroup
        
        # Perimeter tracer dot
        perimeter_tracer = Dot(radius=0.08, color=RED, fill_opacity=1.0)
        # Start at rectangle's start vertex (bottom-left). Polygon start is first vertex given.
        perimeter_tracer.move_to(rect_outline.get_start())
        self.objects["perimeter_tracer"] = perimeter_tracer
        
        # Perimeter path (invisible, same as rectangle outline)
        # FIX: Use WHITE with 0 opacity instead of undefined TRANSPARENT
        perimeter_path = Polygon(*rect_vertices, color=WHITE, stroke_width=0, stroke_opacity=0, fill_opacity=0)
        perimeter_path.move_to(content_center)
        self.objects["perimeter_path"] = perimeter_path
        
        # Step explanation text
        step_explanation = Text(
            "Step 1: Draw the rectangle. Its dimensions are 4 units wide and 3 units tall.",
            color="#D3D3D3",  # LIGHT_GRAY equivalent
            font_size=24
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["rect_outline"]))
        self.play(Write(self.objects["step_explanation"]))
        
        animation_time = 2.0 + 1.5 + 1.0  # Estimate: Write title, Create rect, Write explanation
        remaining = 4.848 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Update explanation text
        new_explanation = Text(
            "Step 2: Label the width (4) and height (3).",
            color="#D3D3D3",
            font_size=24
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Signal action: Write dim_label_w (though JSON says signal_action type "Write", we use Write animation)
        self.play(Write(self.objects["dim_label_w"]))
        # Visual action: Write dim_label_h
        self.play(Write(self.objects["dim_label_h"]))
        
        animation_time = 1.0 + 0.5 + 0.5  # ReplacementTransform, Write, Write
        remaining = 3.408 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        new_explanation = Text(
            "Step 3: Area is the space covered. Fill with unit squares.",
            color="#D3D3D3",
            font_size=24
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Signal action: Indicate rectangle in BLUE
        self.play(Indicate(self.objects["rect_outline"], color=BLUE))
        
        # Create grid of small squares inside rectangle
        # Rectangle is 4 units wide, 3 units tall. We'll create 4x3 grid of unit squares.
        # Square side length = rectangle width / 4 = 1.0
        sq_side = 1.0
        squares = VGroup()
        for row in range(3):  # height = 3
            for col in range(4):  # width = 4
                # Calculate position relative to rectangle center
                # Rectangle vertices: bottom-left (-2, -1.5), top-right (2, 1.5)
                # Square center: start at bottom-left corner of rectangle + offset
                x = -2 + col * sq_side + sq_side / 2
                y = -1.5 + row * sq_side + sq_side / 2
                sq = Square(side_length=sq_side, color="#1E90FF", fill_opacity=0.3, stroke_width=1)
                sq.move_to([x, y, 0])
                squares.add(sq)
        
        # Add squares to the VGroup stored in objects
        self.objects["fill_squares_vgroup"].add(*squares)
        
        # Animate creation of squares with LaggedStart for row-by-row effect
        self.play(LaggedStart(*[Create(sq) for sq in squares], lag_ratio=0.1, run_time=3))
        
        animation_time = 1.0 + 1.0 + 3.0  # ReplacementTransform, Indicate, LaggedStart
        remaining = 6.576 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        new_explanation = Text(
            "Step 4: Perimeter is the boundary length. Introduce a tracer dot.",
            color="#D3D3D3",
            font_size=24
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Signal action: Circumscribe rectangle in RED
        self.play(Circumscribe(self.objects["rect_outline"], color=RED, run_time=1))
        
        # Visual action: Create (FadeIn) the red tracer dot
        self.play(FadeIn(self.objects["perimeter_tracer"]))
        
        animation_time = 1.0 + 1.0 + 0.5  # ReplacementTransform, Circumscribe, FadeIn
        remaining = 6.624 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        audio_file = "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        new_explanation = Text(
            "Step 5: Perimeter = 4+3+4+3 = 14 units. Tracer moves around.",
            color="#D3D3D3",
            font_size=24
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Visual action: Move tracer dot along perimeter path, highlighting side lengths
        # We'll create temporary labels for each side as the dot passes.
        path = self.objects["perimeter_path"]
        tracer = self.objects["perimeter_tracer"]
        
        # Define side lengths and their midpoints for labels
        # Bottom side from (-2,-1.5) to (2,-1.5)
        bottom_mid = np.array([0, -1.5, 0])
        # Right side from (2,-1.5) to (2,1.5)
        right_mid = np.array([2, 0, 0])
        # Top side from (2,1.5) to (-2,1.5)
        top_mid = np.array([0, 1.5, 0])
        # Left side from (-2,1.5) to (-2,-1.5)
        left_mid = np.array([-2, 0, 0])
        
        # Create temporary labels (will be faded in/out)
        label_bottom = MathTex("4", color=YELLOW, font_size=28).move_to(bottom_mid + 0.4 * DOWN)
        label_right = MathTex("3", color=YELLOW, font_size=28).move_to(right_mid + 0.4 * RIGHT)
        label_top = MathTex("4", color=YELLOW, font_size=28).move_to(top_mid + 0.4 * UP)
        label_left = MathTex("3", color=YELLOW, font_size=28).move_to(left_mid + 0.4 * LEFT)
        
        # Animate tracer moving along path with pauses at vertices
        # We'll break the path into four segments.
        # Segment 1: bottom side (left to right)
        self.play(tracer.animate.move_to(path.get_start()), run_time=0.1)  # Ensure start
        self.play(FadeIn(label_bottom))
        self.play(MoveAlongPath(tracer, path, run_time=2, rate_func=linear))
        self.play(FadeOut(label_bottom))
        
        # Segment 2: right side (bottom to top)
        self.play(FadeIn(label_right))
        self.play(MoveAlongPath(tracer, path, run_time=1.5, rate_func=linear))
        self.play(FadeOut(label_right))
        
        # Segment 3: top side (right to left)
        self.play(FadeIn(label_top))
        self.play(MoveAlongPath(tracer, path, run_time=2, rate_func=linear))
        self.play(FadeOut(label_top))
        
        # Segment 4: left side (top to bottom)
        self.play(FadeIn(label_left))
        self.play(MoveAlongPath(tracer, path, run_time=1.5, rate_func=linear))
        self.play(FadeOut(label_left))
        
        # Bring tracer back to start for completeness
        self.play(tracer.animate.move_to(path.get_start()), run_time=0.5)
        
        animation_time = 1.0 + 0.1 + 0.5 + 2 + 0.5 + 0.5 + 1.5 + 0.5 + 0.5 + 2 + 0.5 + 0.5 + 1.5 + 0.5 + 0.5 + 0.5
        # Rough estimate: ReplacementTransform, initial move, FadeIn label, Move, FadeOut, etc.
        remaining = 8.4 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final wait
        self.wait(max(0.1, 2))