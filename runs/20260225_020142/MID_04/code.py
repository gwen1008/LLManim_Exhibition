from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create objects from layout_plan.objects
        # Title
        title = Text("Corresponding Interior Angles", color=WHITE, font_size=40)
        self.objects["title"] = title

        # Parallel Lines
        line1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=BLUE, stroke_width=4)
        self.objects["line1"] = line1
        line2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=BLUE, stroke_width=4)
        self.objects["line2"] = line2

        # Transversal
        transversal = Line(start=[-3, -1, 0], end=[3, 1, 0], color=RED, stroke_width=4)
        self.objects["transversal"] = transversal

        # Intersection Points and Labels
        point_P = Dot(point=[3, 1, 0], color=WHITE, radius=0.07)
        self.objects["point_P"] = point_P
        point_Q = Dot(point=[-3, -1, 0], color=WHITE, radius=0.07)
        self.objects["point_Q"] = point_Q

        label_P = MathTex("P", color=WHITE, font_size=24).next_to(point_P, UR, buff=0.15)
        self.objects["label_P"] = label_P
        label_Q = MathTex("Q", color=WHITE, font_size=24).next_to(point_Q, DL, buff=0.15)
        self.objects["label_Q"] = label_Q

        # Angle Arcs and Labels
        # Angle at P (between line1 and transversal, on the right side)
        angle1_arc = Angle(line1, transversal, radius=0.4, other_angle=False, color=GREEN_C, stroke_width=6)
        self.objects["angle1_arc"] = angle1_arc

        angle1_label = MathTex(r"\angle 1", color=GREEN_C, font_size=24)
        self.objects["angle1_label"] = angle1_label

        # Angle at Q (between transversal and line2, on the right side)
        angle2_arc = Angle(transversal, line2, radius=0.4, other_angle=False, color=GREEN_C, stroke_width=6)
        self.objects["angle2_arc"] = angle2_arc

        angle2_label = MathTex(r"\angle 2", color=GREEN_C, font_size=24)
        self.objects["angle2_label"] = angle2_label

        # Position angle labels relative to arc centers
        angle1_label.next_to(angle1_arc.point_from_proportion(0.5), UR, buff=0.15)
        angle2_label.next_to(angle2_arc.point_from_proportion(0.5), UR, buff=0.15).shift(LEFT*0.2)

        # VGroups for angles
        angle1_group = VGroup(angle1_arc, angle1_label)
        self.objects["angle1_group"] = angle1_group
        angle2_group = VGroup(angle2_arc, angle2_label)
        self.objects["angle2_group"] = angle2_group

        # Conclusion Text
        conclusion_text = Text("Corresponding interior angles on the same side of the transversal are equal.", color=YELLOW, font_size=30)
        self.objects["conclusion_text"] = conclusion_text

        # Manual positioning for title and conclusion
        title.to_edge(UP, buff=0.5)
        conclusion_text.to_edge(DOWN, buff=0.5).scale(0.8)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(line1), run_time=1.5)
        remaining_1 = max(0.1, 5.016 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(line2), run_time=1.5)
        remaining_2 = max(0.1, 3.672 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Create(transversal), run_time=1.5)
        self.play(Create(point_P), Write(label_P), run_time=1.0)
        self.play(Create(point_Q), Write(label_Q), run_time=1.0)
        total_anim_time_step3 = 1.5 + 1.0 + 1.0
        remaining_3 = max(0.1, 7.368 - total_anim_time_step3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Signal action: Indicate angle1_arc
        self.play(Indicate(angle1_arc, color=GREEN, run_time=1))
        self.play(Create(angle1_arc), Write(angle1_label), run_time=1.5)
        self.play(Create(angle2_arc), Write(angle2_label), run_time=1.5)
        total_anim_time_step4 = 1 + 1.5 + 1.5
        remaining_4 = max(0.1, 12.048 - total_anim_time_step4 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action: Circumscribe angle1_group
        self.play(Circumscribe(angle1_group, color=YELLOW, run_time=1))
        # Create a copy of angle1_group to transform into angle2_group's position/orientation
        angle1_group_target = angle2_group.copy()
        # Now transform angle1_group into that target
        self.play(Transform(angle1_group, angle1_group_target), run_time=3)
        total_anim_time_step5 = 1 + 3
        remaining_5 = max(0.1, 11.976 - total_anim_time_step5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        self.play(Write(conclusion_text), run_time=2.0)
        remaining_6 = max(0.1, 8.496 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))