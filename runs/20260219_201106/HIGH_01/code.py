from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Layout anchors
        title_anchor = UP * 3.2
        plane_center = ORIGIN
        explanation_anchor = DOWN * 3.2
        
        # Create objects according to specification
        title = MathTex("y = 2x - 1", color=BLUE, font_size=48)
        title.move_to(title_anchor)
        
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=9,
            y_length=9,
            stroke_opacity=0.5
        )
        plane.move_to(plane_center)
        
        y_intercept_dot = Dot(point=[0, -1, 0], radius=0.08, color=YELLOW)
        y_intercept_label = MathTex("(0, -1)", font_size=36, color=YELLOW)
        y_intercept_label.next_to(y_intercept_dot, LEFT+UP, buff=0.2)
        
        # Initial zero-length segments
        run_segment = Line(
            start=[0, -1, 0],
            end=[0, -1, 0],
            color=GREEN,
            stroke_width=6
        )
        
        rise_segment = Line(
            start=[1, -1, 0],
            end=[1, -1, 0],
            color=RED,
            stroke_width=6
        )
        
        # Slope triangle (initially invisible)
        slope_triangle = Polygon(
            [0, -1, 0],
            [1, -1, 0],
            [1, 1, 0],
            color=WHITE,
            fill_opacity=0.3,
            stroke_width=3
        )
        slope_triangle.move_to(plane_center)
        
        run_label = MathTex("\\text{run}=1", font_size=32, color=GREEN)
        run_label.next_to(run_segment, DOWN, buff=0.1)
        
        rise_label = MathTex("\\text{rise}=2", font_size=32, color=RED)
        rise_label.next_to(rise_segment, RIGHT, buff=0.1)
        
        slope_label = MathTex("m = \\frac{\\text{rise}}{\\text{run}} = \\frac{2}{1} = 2", 
                             font_size=36, color=ORANGE)
        slope_label.next_to(slope_triangle, UP+RIGHT, buff=0.5)
        
        # Line graph (initially zero-length at leftmost point)
        line_graph = Line(
            start=[-2, -5, 0],
            end=[-2, -5, 0],
            color=BLUE,
            stroke_width=5
        )
        
        # Step explanation text
        step_explanation = Text(
            "Step 1: Identify the y-intercept at (0, -1).",
            font_size=28,
            color=WHITE
        )
        step_explanation.move_to(explanation_anchor)
        
        # Step 1: Begin with function and show coordinate grid
        self.play(Write(title))
        self.play(Circumscribe(title, color=YELLOW))
        self.play(Create(plane))
        self.wait(2)
        
        # Step 2: Show y-intercept
        self.play(Create(y_intercept_dot), Write(y_intercept_label))
        self.play(Indicate(y_intercept_dot, color=YELLOW))
        self.wait(1)
        
        # Update explanation text for step 3
        step_explanation_new = Text(
            "Step 3: Run 1 unit to the right.",
            font_size=28,
            color=WHITE
        )
        step_explanation_new.move_to(explanation_anchor)
        self.play(Transform(step_explanation, step_explanation_new))
        
        # Step 3: Show run segment
        run_segment_target = Line(
            start=[0, -1, 0],
            end=[1, -1, 0],
            color=GREEN,
            stroke_width=6
        )
        self.play(Transform(run_segment, run_segment_target))
        self.wait(1)
        
        # Update explanation text for step 4
        step_explanation_new2 = Text(
            "Step 4: Rise 2 units up.",
            font_size=28,
            color=WHITE
        )
        step_explanation_new2.move_to(explanation_anchor)
        self.play(Transform(step_explanation, step_explanation_new2))
        
        # Step 4: Show rise segment
        rise_segment_target = Line(
            start=[1, -1, 0],
            end=[1, 1, 0],
            color=RED,
            stroke_width=6
        )
        self.play(Transform(rise_segment, rise_segment_target))
        self.play(Indicate(rise_segment, color=RED))
        self.wait(1)
        
        # Update explanation text for step 5
        step_explanation_new3 = Text(
            "Step 5: Slope = rise/run = 2/1 = 2.",
            font_size=28,
            color=WHITE
        )
        step_explanation_new3.move_to(explanation_anchor)
        self.play(Transform(step_explanation, step_explanation_new3))
        
        # Step 5: Show slope triangle and labels
        self.play(Create(slope_triangle))
        self.play(Write(run_label), Write(rise_label))
        self.play(Write(slope_label))
        self.wait(1)
        
        # Step 6: Draw the complete line
        line_graph_target = Line(
            start=[-2, -5, 0],
            end=[2, 3, 0],
            color=BLUE,
            stroke_width=5
        )
        self.play(Transform(line_graph, line_graph_target))
        self.play(Indicate(line_graph, color=BLUE))
        self.wait(2)