'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the solution to the equation 2x = 6 using a balance scale model to demonstrate the concept of division/balancing.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and initial equation.
#    - Main Content: [Center y=0] for the balance scale, boxes, and circles.
#    - Footer Region: [Bottom y=-3.5] for step explanations.
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine zones to keep Title, Scale, and Explanation in separate vertical bands.
#    - Group boxes and circles into VGroups for collective positioning and animation.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using provided audio_path.
#    - [x] Files: "media/audio/用天平模型視覺化_2x_=_6。一邊放兩個箱子，另一邊放_6_個圓圈。最後演示除法得出_x_的過程。/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show equation.
#    - Step 2: Build scale, add boxes and circles.
#    - Step 3: Indicate circles, lift and split them.
#    - Step 4: Remove one box, keep one group of circles.
#    - Step 5: Transform equation to final solution.
'''

from manim import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Initialize layout engine
        layout = LayoutEngine()

        # Create a dictionary to store all objects for easy reference
        self.objects = {}

        # --- Create objects from layout_plan.objects ---
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        self.objects["title"] = title

        # Initial Equation
        equation_initial = MathTex("2x = 6", color=YELLOW, font_size=40)
        obj_eq = LayoutObject(equation_initial, "equation_initial")
        layout.add(obj_eq)
        layout.align_to(obj_eq, obj_title, "BOTTOM", buff=0.5)
        self.objects["equation_initial"] = equation_initial

        # Beam
        beam = Line(start=LEFT*4, end=RIGHT*4, color=LIGHT_GRAY, stroke_width=8)
        obj_beam = LayoutObject(beam, "beam")
        layout.add(obj_beam)
        layout.add_to_zone(obj_beam, "CONTENT")
        self.objects["beam"] = beam

        # Fulcrum (Triangle)
        fulcrum_vertices = [(0, 0.5, 0), (-0.3, 0, 0), (0.3, 0, 0)]
        fulcrum = Polygon(*fulcrum_vertices, color=GRAY, fill_opacity=0.7)
        obj_fulcrum = LayoutObject(fulcrum, "fulcrum")
        layout.add(obj_fulcrum)
        layout.align_to(obj_fulcrum, obj_beam, "CENTER")
        self.objects["fulcrum"] = fulcrum

        # Pans
        pan_left = Square(side_length=1.5, color=GRAY, fill_opacity=0.2)
        obj_pan_left = LayoutObject(pan_left, "pan_left")
        layout.add(obj_pan_left)
        layout.align_to(obj_pan_left, obj_beam, "LEFT", buff=-3)
        layout.align_to(obj_pan_left, obj_beam, "BOTTOM", buff=-0.5)
        self.objects["pan_left"] = pan_left

        pan_right = Square(side_length=1.5, color=GRAY, fill_opacity=0.2)
        obj_pan_right = LayoutObject(pan_right, "pan_right")
        layout.add(obj_pan_right)
        layout.align_to(obj_pan_right, obj_beam, "RIGHT", buff=-3)
        layout.align_to(obj_pan_right, obj_beam, "BOTTOM", buff=-0.5)
        self.objects["pan_right"] = pan_right

        # Boxes (representing x)
        box1 = Square(side_length=1.0, color=BLUE, fill_opacity=0.5)
        # Position relative to pan_left after layout solves
        self.objects["box1"] = box1

        box2 = Square(side_length=1.0, color=BLUE, fill_opacity=0.5)
        self.objects["box2"] = box2

        # Label for boxes
        label_2x_group = MathTex("2x", color=BLUE, font_size=30)
        obj_label_2x = LayoutObject(label_2x_group, "label_2x_group")
        layout.add(obj_label_2x)
        layout.align_to(obj_label_2x, obj_pan_left, "TOP", buff=0.2)
        self.objects["label_2x_group"] = label_2x_group

        # Circles (six unit circles)
        circle_radius = 0.3
        circle_positions = []
        # Arrange in 2 rows, 3 columns grid centered at origin
        for row in range(2):
            for col in range(3):
                x_offset = (col - 1) * (circle_radius * 2.5)
                y_offset = (row - 0.5) * (circle_radius * 2.5)
                circle_positions.append([x_offset, y_offset, 0])
        circles = VGroup(*[Circle(radius=circle_radius, color=GREEN, fill_opacity=0.5) for _ in range(6)])
        for i, circle in enumerate(circles):
            circle.move_to(circle_positions[i])
        self.objects["circle_group"] = circles
        obj_circles = LayoutObject(circles, "circle_group")
        layout.add(obj_circles)
        layout.align_to(obj_circles, obj_pan_right, "CENTER")
        # We'll also store individual circles for splitting later
        self.circles_list = list(circles)

        # Label for circles
        label_6 = MathTex("6", color=GREEN, font_size=30)
        obj_label_6 = LayoutObject(label_6, "label_6")
        layout.add(obj_label_6)
        layout.align_to(obj_label_6, obj_pan_right, "TOP", buff=0.2)
        self.objects["label_6"] = label_6

        # Explanation Text
        explanation_text = Text("The scale is balanced: 2x equals 6.", color=LIGHT_GRAY, font_size=28)
        obj_expl = LayoutObject(explanation_text, "explanation_text")
        layout.add(obj_expl)
        layout.add_to_zone(obj_expl, "FOOTER")
        self.objects["explanation_text"] = explanation_text

        # Solve layout constraints
        layout.solve()

        # Now position boxes relative to solved pan positions
        box1.move_to(self.objects["pan_left"].get_center() + LEFT*0.6)
        box2.move_to(self.objects["pan_left"].get_center() + RIGHT*0.6)

        # Group boxes for easier handling
        box_group = VGroup(box1, box2)
        self.objects["box_group"] = box_group

        # Initially hide all objects except title and equation (they will be created in sequence)
        # Objects will be introduced via animations in Phase 2

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start with the equation 2x equals 6. Imagine a balance scale where equality means balance.",
                "signal_action": {"type": "Circumscribe", "target": "equation_initial", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "equation_initial", "details": "Write the equation"},
                "duration": 7.08,
                "audio_path": "media/audio/用天平模型視覺化_2x_=_6。一邊放兩個箱子，另一邊放_6_個圓圈。最後演示除法得出_x_的過程。/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "On the left side, we place two boxes, each representing the unknown x. Together they are 2x. On the right, six unit circles represent the number 6.",
                "signal_action": None,
                "visual_action": {"type": "AnimationGroup", "target_ids": ["beam", "fulcrum", "pan_left", "pan_right", "box1", "box2", "label_2x_group", "circle_group", "label_6"], "details": "Create scale, then create boxes and circles in their pans with labels"},
                "duration": 10.8,
                "audio_path": "media/audio/用天平模型視覺化_2x_=_6。一邊放兩個箱子，另一邊放_6_個圓圈。最後演示除法得出_x_的過程。/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "The scale is balanced, showing 2x equals 6. To find x, we divide both sides by 2. Visually, we split the six circles into two equal groups.",
                "signal_action": {"type": "Indicate", "target": "circle_group", "color": "GREEN"},
                "visual_action": {"type": "Custom", "details": "Lift circle_group up to a temporary position above scale, then animate a vertical line dividing them into two columns of three circles each."},
                "duration": 11.784,
                "audio_path": "media/audio/用天平模型視覺化_2x_=_6。一邊放兩個箱子，另一邊放_6_個圓圈。最後演示除法得出_x_的過程。/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "If two boxes balance six circles, then one box must balance three circles. So we remove one box and keep one group of three circles.",
                "signal_action": {"type": "Indicate", "target": "box1", "color": "BLUE"},
                "visual_action": {"type": "Transform", "target_id": "box2", "details": "Fade out box2 and label_2x_group. Transform box1 into a new 'x' box at pan_left center. Move one group of three circles back to pan_right."},
                "duration": 9.648,
                "audio_path": "media/audio/用天平模型視覺化_2x_=_6。一邊放兩個箱子，另一邊放_6_個圓圈。最後演示除法得出_x_的過程。/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Now we have x equals 3. The scale remains balanced, showing the solution to our equation.",
                "signal_action": {"type": "Circumscribe", "target": "equation_final", "color": "YELLOW"},
                "visual_action": {"type": "TransformMatchingTex", "target_id": "equation_initial", "details": "Transform '2x = 6' into 'x = 3'"},
                "duration": 6.768,
                "audio_path": "media/audio/用天平模型視覺化_2x_=_6。一邊放兩個箱子，另一邊放_6_個圓圈。最後演示除法得出_x_的過程。/step_04.mp3"
            }
        ]

        # Step 1
        step1 = sequence[0]
        # Audio
        if "audio_path" in step1 and step1["audio_path"] and os.path.exists(step1["audio_path"]):
            self.add_sound(step1["audio_path"])
        # Signal Action
        if step1.get("signal_action") is not None:
            signal = step1["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Visual Action
        self.play(Write(self.objects["title"]), Write(self.objects["equation_initial"]), run_time=2)
        # Wait
        animation_time = 1 + 2  # signal + visual
        remaining = step1["duration"] - animation_time
        if remaining > 0:
            self.wait(remaining)

        # Step 2
        step2 = sequence[1]
        if "audio_path" in step2 and step2["audio_path"] and os.path.exists(step2["audio_path"]):
            self.add_sound(step2["audio_path"])
        # Create scale parts
        scale_parts = [self.objects["beam"], self.objects["fulcrum"], self.objects["pan_left"], self.objects["pan_right"]]
        self.play(*[Create(part) for part in scale_parts], run_time=2)
        # Create boxes, circles, and labels
        other_parts = [self.objects["box1"], self.objects["box2"], self.objects["label_2x_group"], self.objects["circle_group"], self.objects["label_6"]]
        self.play(*[FadeIn(part) for part in other_parts], run_time=2)
        # Update explanation text (make it visible)
        self.play(FadeIn(self.objects["explanation_text"]), run_time=1)
        # Wait
        animation_time = 2 + 2 + 1
        remaining = step2["duration"] - animation_time
        if remaining > 0:
            self.wait(remaining)

        # Step 3: Visual Grouping (Prep for Division)
        step3 = sequence[2]
        if "audio_path" in step3 and step3["audio_path"] and os.path.exists(step3["audio_path"]):
            self.add_sound(step3["audio_path"])
        
        # Audio Sync: Check signal
        if step3.get("signal_action") is not None:
            # Indicate the concept of "splitting"
            pass 

        # Regroup circles into two explicit groups for visual clarity
        # Group 1 (correspond to Box 1)
        circles_group_1 = VGroup(*self.circles_list[0:3]) 
        # Group 2 (correspond to Box 2)
        circles_group_2 = VGroup(*self.circles_list[3:6])
        
        # Animate them separating slightly to show "2 groups"
        self.play(
            circles_group_1.animate.shift(UP * 0.3),
            circles_group_2.animate.shift(DOWN * 0.3),
            run_time=2
        )
        
        # Draw braces to show the grouping
        brace_1 = Brace(circles_group_1, LEFT, buff=0.1).set_color(BLUE)
        brace_2 = Brace(circles_group_2, LEFT, buff=0.1).set_color(BLUE)
        
        self.play(Create(brace_1), Create(brace_2), run_time=1)
        
        animation_time = 2 + 1
        remaining = step3["duration"] - animation_time
        if remaining > 0:
            self.wait(remaining)

        # Step 4: The Actual Division (Removing Parts)
        step4 = sequence[3]
        if "audio_path" in step4 and step4["audio_path"] and os.path.exists(step4["audio_path"]):
            self.add_sound(step4["audio_path"])
            
        # Highlight what we are about to remove
        self.play(
            Indicate(self.objects["box2"], color=RED),
            Indicate(circles_group_2, color=RED),
            run_time=2
        )
        
        # Execution: Fade out half of both sides simultaneously
        # This visually proves "Divide by 2"
        self.play(
            FadeOut(self.objects["box2"]),
            FadeOut(self.objects["label_2x_group"]),
            FadeOut(circles_group_2),
            FadeOut(brace_2),
            FadeOut(brace_1), # No longer needed
            run_time=2
        )
        
        # Center the remaining items
        self.play(
            self.objects["box1"].animate.move_to(self.objects["pan_left"].get_center()),
            circles_group_1.animate.move_to(self.objects["pan_right"].get_center()),
            run_time=1.5
        )
        # Update label_6 to "3"
        label_3 = MathTex("3", color=GREEN, font_size=30)
        label_3.move_to(self.objects["label_6"].get_center())
        self.play(ReplacementTransform(self.objects["label_6"], label_3), run_time=1)
        self.objects["label_6"] = label_3  # Update reference
        # Update explanation text
        new_explanation = Text("One box balances three circles: x equals 3.", color=LIGHT_GRAY, font_size=28)
        new_explanation.move_to(self.objects["explanation_text"].get_center())
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation), run_time=1)
        self.objects["explanation_text"] = new_explanation
        # Wait
        animation_time = 1 + 1 + 1 + 1.5 + 1 + 1
        remaining = step4["duration"] - animation_time
        if remaining > 0:
            self.wait(remaining)

        # Step 5
        step5 = sequence[4]
        if "audio_path" in step5 and step5["audio_path"] and os.path.exists(step5["audio_path"]):
            self.add_sound(step5["audio_path"])
        # Create final equation
        equation_final = MathTex("x = 3", color=YELLOW, font_size=40)
        equation_final.move_to(self.objects["equation_initial"].get_center())
        self.objects["equation_final"] = equation_final
        # Transform equation
        self.play(TransformMatchingTex(self.objects["equation_initial"], equation_final, path_arc=90), run_time=2)
        # Signal Action
        if step5.get("signal_action") is not None:
            signal = step5["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Wait
        animation_time = 2 + 1
        remaining = step5["duration"] - animation_time
        if remaining > 0:
            self.wait(remaining)

        # Final hold
        self.wait(2)