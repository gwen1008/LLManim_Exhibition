'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate the Consecutive Interior Angles Theorem (when a transversal crosses parallel lines, interior angles on the same side are equal) using a geometric proof.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Consecutive Interior Angles Theorem"
#    - Main Content: [Center y=0] for the parallel lines, transversal, points, and angle arcs.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Strategy: Keep diagram centered, labels placed close to points with small buff. Use VGroups for lines and angles for easy management.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/consecutive_interior_angles/step_XX.mp3"
# 5. Animation Flow:
#    - Draw parallel lines and transversal.
#    - Add intersection points and labels.
#    - Highlight the two interior angles (green).
#    - Introduce auxiliary point E and corresponding angle (yellow).
#    - Show vertical angle (pink) at B.
#    - Transform pink arc to overlap green arc, demonstrating equality.
#    - Pulse green angles together to conclude the theorem.
#    - Fade out auxiliary angles.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Consecutive Interior Angles Theorem", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Lines
        line_l1 = Line(start=[-3, 1, 0], end=[3, 1, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(diagram_center + UP)
        self.objects["line_l1"] = line_l1
        
        line_l2 = Line(start=[-3, -1, 0], end=[3, -1, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(diagram_center + DOWN)
        self.objects["line_l2"] = line_l2
        
        line_t = Line(start=[-2.5, 1.5, 0], end=[2.5, -1.5, 0], color=RED, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t
        
        # Points (Dots)
        point_A = Dot(point=[0, 1, 0], color=WHITE, radius=0.06)
        self.objects["point_A"] = point_A
        
        point_B = Dot(point=[0, -1, 0], color=WHITE, radius=0.06)
        self.objects["point_B"] = point_B
        
        point_C = Dot(point=[1.5, 1, 0], color=WHITE, radius=0.06)
        self.objects["point_C"] = point_C
        
        point_D = Dot(point=[1.5, -1, 0], color=WHITE, radius=0.06)
        self.objects["point_D"] = point_D
        
        point_E = Dot(point=[-1.5, 1, 0], color=WHITE, radius=0.06)
        self.objects["point_E"] = point_E
        
        # Labels (MathTex)
        label_A = MathTex("A", color=WHITE, font_size=24)
        label_A.next_to(point_A, UP+LEFT, buff=0.15)
        self.objects["label_A"] = label_A
        
        label_B = MathTex("B", color=WHITE, font_size=24)
        label_B.next_to(point_B, DOWN+RIGHT, buff=0.15)
        self.objects["label_B"] = label_B
        
        label_C = MathTex("C", color=WHITE, font_size=24)
        label_C.next_to(point_C, UP, buff=0.15)
        self.objects["label_C"] = label_C
        
        label_D = MathTex("D", color=WHITE, font_size=24)
        label_D.next_to(point_D, DOWN, buff=0.15)
        self.objects["label_D"] = label_D
        
        label_E = MathTex("E", color=WHITE, font_size=24)
        label_E.next_to(point_E, UP, buff=0.15)
        self.objects["label_E"] = label_E
        
        # Angles (will be created later when lines exist)
        # angle_CAB: between line_t and right segment of line_l1 (from A to C)
        # We need a line segment from A to C for the angle
        line_AC = Line(start=[0, 1, 0], end=[1.5, 1, 0], color=BLUE, stroke_width=4)
        self.objects["line_AC"] = line_AC  # store for angle creation
        
        # angle_ABD: between right segment of line_l2 (B to D) and line_t
        line_BD = Line(start=[0, -1, 0], end=[1.5, -1, 0], color=BLUE, stroke_width=4)
        self.objects["line_BD"] = line_BD
        
        # angle_EBA: between left segment of line_l1 (E to A) and line_t (other_angle=True)
        line_EA = Line(start=[-1.5, 1, 0], end=[0, 1, 0], color=BLUE, stroke_width=4)
        self.objects["line_EA"] = line_EA
        
        # angle_ABD_vertical: vertical angle to ∠EBA at B (other_angle=True)
        # We'll create a line segment from B leftwards for the vertical angle
        line_B_left = Line(start=[0, -1, 0], end=[-1.5, -1, 0], color=BLUE, stroke_width=4)
        self.objects["line_B_left"] = line_B_left
        
        # Footer explanation placeholder
        footer_explanation = Text(" ", color=GRAY_C, font_size=24)
        footer_explanation.move_to(explanation_anchor)
        self.objects["footer_explanation"] = footer_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/consecutive_interior_angles/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 1.0 - 1.0 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_03.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/consecutive_interior_angles/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_l1"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 1.0 - 1.0 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_05.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/consecutive_interior_angles/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_l2"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 1.0 - 1.0 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_06.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/consecutive_interior_angles/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_t"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_08.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/consecutive_interior_angles/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_A"], color=ORANGE, run_time=1))
        self.play(GrowFromCenter(self.objects["point_A"]), Write(self.objects["label_A"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_10.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/consecutive_interior_angles/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_B"], color=ORANGE, run_time=1))
        self.play(GrowFromCenter(self.objects["point_B"]), Write(self.objects["label_B"]), run_time=1.5)
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_11.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/consecutive_interior_angles/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(GrowFromCenter(self.objects["point_C"]), Write(self.objects["label_C"]),
                  GrowFromCenter(self.objects["point_D"]), Write(self.objects["label_D"]), run_time=2.0)
        self.wait(max(0.1, max(0.1, 2.0 - 2.0 + 0.5)))
        
        # Create line_AC and line_BD for angles (they're already in objects, just add to scene)
        self.add(self.objects["line_AC"], self.objects["line_BD"])
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_12.mp3")  # [auto-injected]
        # Step 8: Create angle_CAB
        audio_step8 = "media/audio/consecutive_interior_angles/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        angle_CAB = Angle(line1=self.objects["line_t"], line2=self.objects["line_AC"], 
                          radius=0.4, other_angle=False, color=GREEN)
        angle_CAB.set_fill(color=GREEN, opacity=0.3)
        self.objects["angle_CAB"] = angle_CAB
        self.play(Create(angle_CAB), run_time=1.5)
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_13.mp3")  # [auto-injected]
        # Step 9: Create angle_ABD
        audio_step9 = "media/audio/consecutive_interior_angles/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        angle_ABD = Angle(line1=self.objects["line_BD"], line2=self.objects["line_t"], 
                          radius=0.4, other_angle=False, color=GREEN)
        angle_ABD.set_fill(color=GREEN, opacity=0.3)
        self.objects["angle_ABD"] = angle_ABD
        self.play(Create(angle_ABD), run_time=1.5)
        self.wait(max(0.1, max(0.1, 1.5 - 1.5 + 0.5)))
        
        self.add_sound("media/audio/Draw_parallel_lines__a66d55fe46/step_14.mp3")  # [auto-injected]
        # Step 10: Introduce point E
        audio_step10 = "media/audio/consecutive_interior_angles/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_E"], color=YELLOW, run_time=1))
        self.play(GrowFromCenter(self.objects["point_E"]), Write(self.objects["label_E"]), run_time=2.0)
        self.wait(max(0.1, max(0.1, 2.0 - 2.0 + 0.5)))
        
        # Add line_EA for angle creation
        self.add(self.objects["line_EA"])
        
        # Step 11: Create angle_EBA (corresponding angle)
        audio_step11 = "media/audio/consecutive_interior_angles/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_CAB"], color=YELLOW, run_time=1))
        angle_EBA = Angle(line1=self.objects["line_EA"], line2=self.objects["line_t"], 
                          radius=0.35, other_angle=True, color=YELLOW)
        angle_EBA.set_fill(color=YELLOW, opacity=0.3)
        self.objects["angle_EBA"] = angle_EBA
        self.play(Create(angle_EBA), run_time=2.5)
        self.wait(max(0.1, max(0.1, 2.5 - 2.5 + 0.5)))
        
        # Add line_B_left for vertical angle
        self.add(self.objects["line_B_left"])
        
        # Step 12: Create angle_ABD_vertical (vertical angle)
        audio_step12 = "media/audio/consecutive_interior_angles/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_EBA"], color=PINK, run_time=1))
        angle_ABD_vertical = Angle(line1=self.objects["line_t"], line2=self.objects["line_B_left"], 
                                   radius=0.35, other_angle=True, color=PINK)
        angle_ABD_vertical.set_fill(color=PINK, opacity=0.3)
        self.objects["angle_ABD_vertical"] = angle_ABD_vertical
        self.play(Create(angle_ABD_vertical), run_time=2.5)
        self.wait(max(0.1, max(0.1, 2.5 - 2.5 + 0.5)))
        
        # Step 13: Transform pink arc to overlap green arc
        audio_step13 = "media/audio/consecutive_interior_angles/step_12.mp3"
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["angle_ABD_vertical"], color=PINK, run_time=1))
        # Create a copy of angle_ABD but with pink color for transformation
        angle_ABD_pink = Angle(line1=self.objects["line_BD"], line2=self.objects["line_t"], 
                               radius=0.4, other_angle=False, color=PINK)
        angle_ABD_pink.set_fill(color=PINK, opacity=0.3)
        angle_ABD_pink.move_to(self.objects["angle_ABD"].get_center())
        self.play(Transform(self.objects["angle_ABD_vertical"], angle_ABD_pink), run_time=1.5)
        self.play(FadeOut(self.objects["angle_ABD_vertical"]), run_time=1.0)
        self.wait(max(0.1, max(0.1, 2.5 - 2.5 + 0.5)))
        
        # Step 14: Show transitive relationship
        audio_step14 = "media/audio/consecutive_interior_angles/step_13.mp3"
        if os.path.exists(audio_step14):
            self.add_sound(audio_step14)
        elif os.path.exists(audio_step14.replace(".mp3", ".wav")):
            self.add_sound(audio_step14.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_CAB"], color=YELLOW, run_time=1),
                  Indicate(self.objects["angle_EBA"], color=YELLOW, run_time=1))
        self.wait(max(0.1, max(0.1, 3.0 - 2.0 + 0.5)))
        
        # Step 15: Pulse both green angles
        audio_step15 = "media/audio/consecutive_interior_angles/step_14.mp3"
        if os.path.exists(audio_step15):
            self.add_sound(audio_step15)
        elif os.path.exists(audio_step15.replace(".mp3", ".wav")):
            self.add_sound(audio_step15.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_ABD"], color=GREEN, run_time=1))
        # Pulse both green angles
        self.play(
            self.objects["angle_CAB"].animate.scale(1.2).set_opacity(0.6),
            self.objects["angle_ABD"].animate.scale(1.2).set_opacity(0.6),
            run_time=0.5
        )
        self.play(
            self.objects["angle_CAB"].animate.scale(1/1.2).set_opacity(0.3),
            self.objects["angle_ABD"].animate.scale(1/1.2).set_opacity(0.3),
            run_time=0.5
        )
        self.wait(max(0.1, max(0.1, 3.0 - 1.0 + 0.5)))
        
        # Step 16: Fade out auxiliary angles
        audio_step16 = "media/audio/consecutive_interior_angles/step_15.mp3"
        if os.path.exists(audio_step16):
            self.add_sound(audio_step16)
        elif os.path.exists(audio_step16.replace(".mp3", ".wav")):
            self.add_sound(audio_step16.replace(".mp3", ".wav"))
        
        self.play(FadeOut(self.objects["angle_EBA"]), run_time=2.5)
        self.wait(max(0.1, max(0.1, 2.5 - 2.5 + 0.5)))
        
        # Final hold
        self.wait(max(0.1, 2))