'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between a circle's circumference (C) and its diameter (D), demonstrating that C = πD > 3D.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle (left) and length comparison (right)
#    - Footer Region: [Bottom y=-2.5] for step-by-step text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use left-right split. Circle on left (x=-4), comparison lines on right (x=2). Footer text centered at bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow: [Brief sequence of events]
#    - Step 1: Show circle and diameter D.
#    - Step 2: Build 3D length on the right.
#    - Step 3: Unroll circumference from circle into a line.
#    - Step 4: Compare C line with 3D line.
#    - Step 5: Show conclusion and π value.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/The_animation_begins_1cfb54a569/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        circle_anchor = np.array([-4, 0, 0])  # Left side
        comparison_anchor = np.array([2, 0, 0])  # Right side
        footer_anchor = 2.5 * DOWN
        
        # Create objects from layout_plan
        # title
        title = Text("Circumference: Unrolling a Circle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # circle
        circle = Circle(radius=1.5, color=BLUE, stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle
        
        # diameter_line
        diameter_line = Line(LEFT*1.5, RIGHT*1.5, color=YELLOW, stroke_width=6)
        diameter_line.move_to(circle_anchor)
        self.objects["diameter_line"] = diameter_line
        
        # label_D
        label_D = MathTex("D", color=YELLOW)
        label_D.next_to(diameter_line, UP, buff=0.1)
        self.objects["label_D"] = label_D
        
        # circumference_arc (full circle arc)
        circumference_arc = Arc(radius=1.5, angle=2*PI, color=GREEN, stroke_width=4)
        circumference_arc.move_to(circle_anchor)
        self.objects["circumference_arc"] = circumference_arc
        
        # segment_D_template (invisible template)
        segment_D_template = Line(start=[0,0,0], end=[3.0,0,0], color=YELLOW, stroke_width=6).set_opacity(0.0)
        segment_D_template.move_to(comparison_anchor + LEFT*1.5)
        self.objects["segment_D_template"] = segment_D_template
        
        # segment_3D (VGroup of three segments)
        seg1 = Line(start=[0,0,0], end=[3.0,0,0], color=YELLOW, stroke_width=6)
        seg2 = Line(start=[3.0,0,0], end=[6.0,0,0], color=YELLOW, stroke_width=6)
        seg3 = Line(start=[6.0,0,0], end=[9.0,0,0], color=YELLOW, stroke_width=6)
        segment_3D = VGroup(seg1, seg2, seg3)
        segment_3D.move_to(comparison_anchor).align_to(comparison_anchor, LEFT)
        # Set overall color to RED as per properties
        segment_3D.set_color(RED)
        self.objects["segment_3D"] = segment_3D
        
        # label_3D
        label_3D = MathTex("3D", color=RED)
        label_3D.next_to(segment_3D, UP, buff=0.2)
        self.objects["label_3D"] = label_3D
        
        # circumference_line (unrolled length = πD ≈ 9.4248)
        circumference_line = Line(start=[0,0,0], end=[3.0*PI, 0, 0], color=GREEN, stroke_width=6)
        # Position will be set during animation; initial position as per plan
        circumference_line.move_to(circle_anchor + RIGHT*0.5 + UP*1.5)
        self.objects["circumference_line"] = circumference_line
        
        # label_C
        label_C = MathTex("C = \\pi D", color=GREEN)
        label_C.next_to(circumference_line, UP, buff=0.2)
        self.objects["label_C"] = label_C
        
        # footer_text_anchor (invisible dot)
        footer_text_anchor = Dot(point=[0, -2.5, 0]).set_opacity(0.0)
        self.objects["footer_text_anchor"] = footer_text_anchor
        
        # step_text (dynamic footer text)
        step_text = Text("Step 1: A circle with diameter D.", color=WHITE, font_size=24)
        step_text.move_to(footer_anchor)
        self.objects["step_text"] = step_text
        
        # Additional objects needed for animations
        # For step 4: vertical dashed line
        vertical_dash = DashedLine(
            start=[0,0,0],
            end=[0,1,0],
            color=WHITE,
            stroke_width=2,
            dash_length=0.1
        )
        self.objects["vertical_dash"] = vertical_dash
        
        # For step 5: pi value label
        pi_label = MathTex("\\pi \\approx 3.14159", color=YELLOW, font_size=32)
        pi_label.next_to(segment_3D, DOWN, buff=0.5)
        self.objects["pi_label"] = pi_label
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        # Signal action: Indicate diameter_line
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        # Visual action: Create circle
        self.play(Create(self.objects["circle"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Also create diameter line and label (they are part of the initial view)
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["label_D"]), run_time=1.0)
        # Write step text
        self.play(Write(self.objects["step_text"]), run_time=1.0)
        self.wait(max(0.1, 0.5))
        
        # ========== Step 2 ==========
        # Update footer text
        new_step_text_2 = Text("Step 2: Three diameters (3D) placed end to end.", color=WHITE, font_size=24)
        new_step_text_2.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], new_step_text_2))
        self.objects["step_text"] = new_step_text_2
        
        # Signal action: Circumscribe label_D
        self.play(Circumscribe(self.objects["label_D"], color=YELLOW, run_time=1))
        # Visual action: Create segment_3D and label_3D
        # Animate three segments appearing one after another
        seg1, seg2, seg3 = self.objects["segment_3D"]
        self.play(Create(seg1), run_time=0.8)
        self.play(Create(seg2), run_time=0.8)
        self.play(Create(seg3), run_time=0.8)
        # Write label
        self.play(Write(self.objects["label_3D"]), run_time=1.0)
        remaining_2 = max(0.1, 4.0 - (0.8*3 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        # Update footer text
        new_step_text_3 = Text("Step 3: Unroll the circumference C from the circle.", color=WHITE, font_size=24)
        new_step_text_3.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], new_step_text_3))
        self.objects["step_text"] = new_step_text_3
        
        # Signal action: Indicate circumference_arc
        self.play(Indicate(self.objects["circumference_arc"], color=GREEN, run_time=1))
        # Visual action: Transform circumference_arc into circumference_line
        # First, create the arc (it's overlaid on circle)
        self.play(Create(self.objects["circumference_arc"]), run_time=1.0)
        
        # Animate unrolling: we'll morph the arc into a line
        # We'll use a custom animation: rotate and stretch the arc
        arc = self.objects["circumference_arc"]
        line = self.objects["circumference_line"]
        # Position line to start at same left point as segment_3D
        line_start = self.objects["segment_3D"].get_left()
        line_end = line_start + RIGHT * (3.0 * PI)
        line.put_start_and_end_on(line_start, line_end)
        
        # Create a copy of the arc for transformation
        arc_copy = arc.copy()
        self.add(arc_copy)
        # Animate the copy moving and straightening
        # We'll use a combination of rotation and scaling
        self.play(
            arc_copy.animate.rotate(-PI/2, about_point=arc_copy.get_center()).shift(RIGHT*1.5),
            run_time=2.0
        )
        # Then transform into the line
        self.play(Transform(arc_copy, line), run_time=2.0)
        self.remove(arc_copy)
        self.add(line)
        # Also fade out the original arc on the circle
        self.play(FadeOut(self.objects["circumference_arc"]), run_time=0.5)
        
        remaining_3 = max(0.1, 5.0 - (1.0 + 2.0 + 2.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        # Update footer text
        new_step_text_4 = Text("Step 4: Compare C (green) with 3D (red).", color=WHITE, font_size=24)
        new_step_text_4.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], new_step_text_4))
        self.objects["step_text"] = new_step_text_4
        
        # Signal action: Indicate circumference_line.get_end
        end_dot = Dot(self.objects["circumference_line"].get_end(), color=GREEN, radius=0.08)
        self.add(end_dot)
        self.play(Indicate(end_dot, color=GREEN, run_time=1))
        self.remove(end_dot)
        
        # Visual action: Write label_C and add vertical dashed line
        self.play(Write(self.objects["label_C"]), run_time=1.0)
        
        # Create vertical dashed line from end of 3D to end of C
        dash_start = self.objects["segment_3D"].get_right()
        dash_end = self.objects["circumference_line"].get_end()
        vertical_dash = DashedLine(dash_start, dash_end, color=WHITE, stroke_width=2, dash_length=0.1)
        self.objects["vertical_dash"] = vertical_dash
        self.play(Create(vertical_dash), run_time=1.0)
        
        remaining_4 = max(0.1, 4.0 - (1.0 + 1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        # Update footer text
        new_step_text_5 = Text("Conclusion: C = πD ≈ 3.14159 D, which is > 3D", color=WHITE, font_size=24)
        new_step_text_5.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["step_text"], new_step_text_5))
        self.objects["step_text"] = new_step_text_5
        
        # Signal action: Circumscribe label_C
        self.play(Circumscribe(self.objects["label_C"], color=GREEN, run_time=1))
        
        # Visual action: Show pi value
        self.play(Write(self.objects["pi_label"]), run_time=1.5)
        
        remaining_5 = max(0.1, 5.0 - (1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))