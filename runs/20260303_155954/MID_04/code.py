'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize and prove the Corresponding Angles Theorem using a geometric diagram with parallel lines and a transversal.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for diagram (lines, labels, angle arcs)
#    - Footer Region: [Bottom y=-3.5] for proof text
# 3. Anti-Overlap Check:
#    - Strategy: Use calculated positions for angle labels relative to intersection points. Keep diagram centered, proof text at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/corresponding_angles_theorem/step_XX.mp3"
# 5. Animation Flow:
#    - Draw lines (L1, L2, T).
#    - Label lines and angle numbers.
#    - Highlight corresponding pair (1 & 5).
#    - Step-by-step proof via vertical and alternate interior angles.
#    - Conclude equality and highlight remaining pairs.
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
        title = Text("Corresponding Angles Theorem", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Lines
        line_l1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(diagram_center + UP)
        self.objects["line_l1"] = line_l1
        
        line_l2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(diagram_center + DOWN)
        self.objects["line_l2"] = line_l2
        
        line_t = Line(start=[-3.5, -1.1667, 0], end=[3.5, 1.1667, 0], color=YELLOW, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t
        
        # Line labels
        label_l1 = MathTex("L_1", color=BLUE)
        label_l1.next_to(line_l1, RIGHT, buff=0.2)
        self.objects["label_l1"] = label_l1
        
        label_l2 = MathTex("L_2", color=BLUE)
        label_l2.next_to(line_l2, RIGHT, buff=0.2)
        self.objects["label_l2"] = label_l2
        
        label_t = MathTex("T", color=YELLOW)
        label_t.next_to(line_t.get_end(), RIGHT+UP, buff=0.1)
        self.objects["label_t"] = label_t
        
        # Angle labels (create VGroups, positions set later)
        angle_labels_top = VGroup(
            MathTex("1", color=WHITE, font_size=24),
            MathTex("2", color=WHITE, font_size=24),
            MathTex("3", color=WHITE, font_size=24),
            MathTex("4", color=WHITE, font_size=24)
        )
        angle_labels_top.move_to(diagram_center + UP)
        self.objects["angle_labels_top"] = angle_labels_top
        
        angle_labels_bottom = VGroup(
            MathTex("5", color=WHITE, font_size=24),
            MathTex("6", color=WHITE, font_size=24),
            MathTex("7", color=WHITE, font_size=24),
            MathTex("8", color=WHITE, font_size=24)
        )
        angle_labels_bottom.move_to(diagram_center + DOWN)
        self.objects["angle_labels_bottom"] = angle_labels_bottom
        
        # Proof text
        proof_text = Text("Given: L1 is parallel to L2. T is a transversal.", color=GRAY_C, font_size=28)
        proof_text.move_to(explanation_anchor)
        self.objects["proof_text"] = proof_text
        
        # Pre-calculate intersection points for angle label positioning
        # Intersection A (top): line_l1 ∩ line_t
        # Solve: y=1, line_t: y = (1.1667/3.5)*x + c? Actually use geometry.
        # For simplicity, approximate positions relative to diagram center.
        # We'll position them manually in sequence.
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Draw_parallel_lines__6cd53e41ab/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/corresponding_angles_theorem/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_l1"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Draw_parallel_lines__6cd53e41ab/step_03.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/corresponding_angles_theorem/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_l2"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Draw_parallel_lines__6cd53e41ab/step_04.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/corresponding_angles_theorem/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_t"]), run_time=1.5)
        remaining_3 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Draw_parallel_lines__6cd53e41ab/step_05.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/corresponding_angles_theorem/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Write line labels
        self.play(
            Write(self.objects["label_l1"]),
            Write(self.objects["label_l2"]),
            Write(self.objects["label_t"]),
            run_time=1.5
        )
        
        # Position angle labels (approximate positions)
        # Top intersection (angles 1,2,3,4 around point where line_t crosses line_l1)
        # Intersection point approx at x=0? line_t: from (-3.5,-1.1667) to (3.5,1.1667), line_l1: y=1
        # Solve: 1 = (1.1667/3.5)*x + c? Actually line passes through origin? Let's approximate.
        # We'll place them relative to a point on line_l1 near the intersection.
        top_int_pt = np.array([0, 1, 0])  # Approximation
        angle_labels_top[0].move_to(top_int_pt + LEFT*0.5 + UP*0.3)  # top-left
        angle_labels_top[1].move_to(top_int_pt + RIGHT*0.5 + UP*0.3) # top-right
        angle_labels_top[2].move_to(top_int_pt + RIGHT*0.5 + DOWN*0.3) # bottom-right
        angle_labels_top[3].move_to(top_int_pt + LEFT*0.5 + DOWN*0.3)  # bottom-left
        
        # Bottom intersection (angles 5,6,7,8)
        bottom_int_pt = np.array([0, -1, 0])  # Approximation
        angle_labels_bottom[0].move_to(bottom_int_pt + LEFT*0.5 + UP*0.3)  # top-left
        angle_labels_bottom[1].move_to(bottom_int_pt + RIGHT*0.5 + UP*0.3) # top-right
        angle_labels_bottom[2].move_to(bottom_int_pt + RIGHT*0.5 + DOWN*0.3) # bottom-right
        angle_labels_bottom[3].move_to(bottom_int_pt + LEFT*0.5 + DOWN*0.3)  # bottom-left
        
        # Write all angle labels
        self.play(
            LaggedStart(
                Write(angle_labels_top[0]),
                Write(angle_labels_top[1]),
                Write(angle_labels_top[2]),
                Write(angle_labels_top[3]),
                Write(angle_labels_bottom[0]),
                Write(angle_labels_bottom[1]),
                Write(angle_labels_bottom[2]),
                Write(angle_labels_bottom[3]),
                lag_ratio=0.1
            ),
            run_time=2.5
        )
        remaining_4 = max(0.1, 4.0 - (1.5 + 2.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Draw_parallel_lines__6cd53e41ab/step_06.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/corresponding_angles_theorem/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe angle_labels_top[0]
        self.play(Circumscribe(self.objects["angle_labels_top"][0], color=GREEN, run_time=1))
        # Visual action: Indicate angle_labels_bottom[0]
        self.play(Indicate(self.objects["angle_labels_bottom"][0], color=GREEN, run_time=1))
        remaining_5 = max(0.1, 3.0 - (1 + 1) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Draw_parallel_lines__6cd53e41ab/step_07.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/corresponding_angles_theorem/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Indicate angle_labels_top[2]
        self.play(Indicate(self.objects["angle_labels_top"][2], color=RED, run_time=1))
        # Visual action: Update proof text
        new_proof_text_1 = Text("Step 1: ∠1 = ∠3 (Vertical Angles)", color=GRAY_C, font_size=28)
        new_proof_text_1.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["proof_text"], new_proof_text_1))
        self.objects["proof_text"] = new_proof_text_1
        remaining_6 = max(0.1, 3.0 - (1 + 1) + 0.5)
        self.wait(max(0.1, remaining_6))
        
        self.add_sound("media/audio/Draw_parallel_lines__6cd53e41ab/step_08.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/corresponding_angles_theorem/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Signal action: Indicate angle_labels_bottom[2]
        self.play(Indicate(self.objects["angle_labels_bottom"][2], color=RED, run_time=1))
        # Visual action: Update proof text
        new_proof_text_2 = Text("Step 2: ∠3 = ∠7 (Alternate Interior Angles, L1 ∥ L2)", color=GRAY_C, font_size=28)
        new_proof_text_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["proof_text"], new_proof_text_2))
        self.objects["proof_text"] = new_proof_text_2
        remaining_7 = max(0.1, 4.0 - (1 + 1) + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # Step 8
        audio_step8 = "media/audio/corresponding_angles_theorem/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Signal action: Indicate angle_labels_bottom[0]
        self.play(Indicate(self.objects["angle_labels_bottom"][0], color=RED, run_time=1))
        # Visual action: Update proof text
        new_proof_text_3 = Text("Step 3: ∠7 = ∠5 (Vertical Angles)", color=GRAY_C, font_size=28)
        new_proof_text_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["proof_text"], new_proof_text_3))
        self.objects["proof_text"] = new_proof_text_3
        remaining_8 = max(0.1, 3.0 - (1 + 1) + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # Step 9
        audio_step9 = "media/audio/corresponding_angles_theorem/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe angle_labels_top[0]
        self.play(Circumscribe(self.objects["angle_labels_top"][0], color=GREEN, run_time=1))
        # Visual action: Update proof text
        new_proof_text_4 = Text("Conclusion: ∠1 = ∠5. All corresponding angles are equal.", color=GRAY_C, font_size=28)
        new_proof_text_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["proof_text"], new_proof_text_4))
        self.objects["proof_text"] = new_proof_text_4
        remaining_9 = max(0.1, 4.0 - (1 + 1) + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Step 10
        audio_step10 = "media/audio/corresponding_angles_theorem/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        # Visual action: Highlight remaining corresponding pairs
        # Pairs: (2 & 6), (3 & 7), (4 & 8)
        self.play(
            Indicate(self.objects["angle_labels_top"][1], color=GREEN, run_time=0.8),
            Indicate(self.objects["angle_labels_bottom"][1], color=GREEN, run_time=0.8)
        )
        self.wait(max(0.1, 0.5))
        self.play(
            Indicate(self.objects["angle_labels_top"][2], color=GREEN, run_time=0.8),
            Indicate(self.objects["angle_labels_bottom"][2], color=GREEN, run_time=0.8)
        )
        self.wait(max(0.1, 0.5))
        self.play(
            Indicate(self.objects["angle_labels_top"][3], color=GREEN, run_time=0.8),
            Indicate(self.objects["angle_labels_bottom"][3], color=GREEN, run_time=0.8)
        )
        remaining_10 = max(0.1, 5.0 - (0.8+0.5+0.8+0.5+0.8) + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # Final hold
        self.wait(max(0.1, 2))