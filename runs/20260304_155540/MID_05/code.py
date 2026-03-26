'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between a circle's circumference and its diameter (C = πD) by "unfolding" the circumference into a straight line and comparing it to three diameters placed end-to-end.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Circumference vs. Diameter"
#    - Main Content: [Center y=0] for circle, traced arc, unfolded line, and three diameters.
#    - Footer Region: [Bottom y=-3.5] for concluding formula "C = πD > 3D (since π > 3)".
# 3. Anti-Overlap Check:
#    - Strategy: Place circle and unfolded line in upper half (y ~ 0.5 to 2.5). Place three diameters in lower half (y = -1.0). Use vertical spacing to prevent overlap.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step?
# 5. Animation Flow:
#    - Step 1: Create circle.
#    - Step 2: Indicate circle, then create diameter line and label D.
#    - Step 3: Animate a dot tracing the circle's boundary, leaving a green trail (traced_arc).
#    - Step 4: Indicate traced arc, then morph it into a straight line (circumference_line) and show label C = πD.
#    - Step 5: Create three diameter segments below and label 3D.
#    - Step 6: Indicate circumference line, add brace and label, then animate a vertical line highlighting the excess length.
#    - Step 7: Circumscribe footer text, then write the concluding relationship.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create layout engine
        layout = LayoutEngine()

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        self.objects = {}

        # title
        title = Text("Circumference vs. Diameter", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_constraint(layout.get("title").center_x == 0)

        # circle
        circle = Circle(radius=2.0, color=BLUE, stroke_width=4)
        circle.move_to(content_center + UP*0.5)
        self.objects["circle"] = circle
        layout.add(LayoutObject(circle, "circle"))

        # diameter_line
        diameter_line = Line(LEFT*2, RIGHT*2, color=YELLOW, stroke_width=6)
        diameter_line.move_to(circle.get_center())
        self.objects["diameter_line"] = diameter_line
        layout.add(LayoutObject(diameter_line, "diameter_line"))

        # label_d
        label_d = MathTex("D", color=YELLOW)
        label_d.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_d"] = label_d
        layout.add(LayoutObject(label_d, "label_d"))

        # traced_arc (initially invisible)
        traced_arc = Arc(radius=2.0, angle=2*PI, color=GREEN, stroke_width=6, stroke_opacity=0.0)
        traced_arc.move_to(circle.get_center())
        self.objects["traced_arc"] = traced_arc
        layout.add(LayoutObject(traced_arc, "traced_arc"))

        # circumference_line (initially invisible)
        circumference_line = Line(LEFT*PI*2, RIGHT*PI*2, color=GREEN, stroke_width=6, stroke_opacity=0.0)
        circumference_line.move_to(circle.get_center() + UP*2.0)
        self.objects["circumference_line"] = circumference_line
        layout.add(LayoutObject(circumference_line, "circumference_line"))

        # label_c
        label_c = MathTex(r"C = \pi D", color=GREEN)
        label_c.next_to(circumference_line, UP, buff=0.3)
        self.objects["label_c"] = label_c
        layout.add(LayoutObject(label_c, "label_c"))

        # diameter_seg_1
        diameter_seg_1 = Line(LEFT*6.0, LEFT*2.0, color=YELLOW, stroke_width=6)
        diameter_seg_1.move_to([-6.0, -1.0, 0])
        self.objects["diameter_seg_1"] = diameter_seg_1
        layout.add(LayoutObject(diameter_seg_1, "diameter_seg_1"))

        # diameter_seg_2
        diameter_seg_2 = Line(LEFT*2.0, RIGHT*2.0, color=YELLOW, stroke_width=6)
        diameter_seg_2.move_to([-2.0, -1.0, 0])
        self.objects["diameter_seg_2"] = diameter_seg_2
        layout.add(LayoutObject(diameter_seg_2, "diameter_seg_2"))

        # diameter_seg_3
        diameter_seg_3 = Line(RIGHT*2.0, RIGHT*6.0, color=YELLOW, stroke_width=6)
        diameter_seg_3.move_to([2.0, -1.0, 0])
        self.objects["diameter_seg_3"] = diameter_seg_3
        layout.add(LayoutObject(diameter_seg_3, "diameter_seg_3"))

        # label_3d
        label_3d = MathTex("3D", color=YELLOW)
        label_3d.next_to(diameter_seg_2, DOWN, buff=0.3)
        self.objects["label_3d"] = label_3d
        layout.add(LayoutObject(label_3d, "label_3d"))

        # comparison_bracket
        comparison_bracket = Brace(circumference_line, DOWN, color=WHITE, stroke_width=3)
        comparison_bracket.move_to(circumference_line.get_center() + UP*0.0)
        self.objects["comparison_bracket"] = comparison_bracket
        layout.add(LayoutObject(comparison_bracket, "comparison_bracket"))

        # brace_label
        brace_label = MathTex(r"\pi D \approx 12.57", color=WHITE)
        brace_label.next_to(comparison_bracket, DOWN, buff=0.2)
        self.objects["brace_label"] = brace_label
        layout.add(LayoutObject(brace_label, "brace_label"))

        # footer_text
        footer_text = Tex(r"$C = \pi D > 3D$ \quad (since $\pi > 3$)", color=ORANGE, font_size=30)
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text
        layout.add(LayoutObject(footer_text, "footer_text"))
        layout.add_to_zone(layout.get("footer_text"), "FOOTER")
        layout.add_constraint(layout.get("footer_text").center_x == 0)

        # Solve layout constraints
        layout.solve()

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_an_animation__f87fabe115/step_00.mp3")  # [auto-injected] duration=5.40s
        _audio_dur_0 = 5.40  # [audio-sync] actual TTS duration
        # Step 1: Create circle
        self.play(Create(self.objects["circle"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_an_animation__f87fabe115/step_01.mp3")  # [auto-injected] duration=4.82s
        _audio_dur_1 = 4.82  # [audio-sync] actual TTS duration
        # Step 2: Indicate circle, then create diameter line and label D
        self.play(Indicate(self.objects["circle"], color=GREEN, run_time=1))
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["label_d"]), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_an_animation__f87fabe115/step_02.mp3")  # [auto-injected] duration=3.48s
        _audio_dur_2 = 3.48  # [audio-sync] actual TTS duration
        # Step 3: Animate tracing the circumference
        # We'll use a dot to trace and update the traced_arc's stroke_opacity
        dot = Dot(color=GREEN, radius=0.08)
        dot.move_to(self.objects["circle"].point_at_angle(0))
        self.add(dot)

        # ValueTracker for angle
        angle_tracker = ValueTracker(0)
        def update_dot(mob):
            mob.move_to(self.objects["circle"].point_at_angle(angle_tracker.get_value()))
        dot.add_updater(update_dot)

        # Update traced_arc opacity based on fraction traced
        def update_arc(mob):
            fraction = angle_tracker.get_value() / (2 * PI)
            mob.set_stroke(opacity=fraction)
        self.objects["traced_arc"].add_updater(update_arc)

        self.add(self.objects["traced_arc"])
        self.play(angle_tracker.animate.set_value(2 * PI), run_time=4.0, rate_func=linear)
        dot.remove_updater(update_dot)
        self.objects["traced_arc"].remove_updater(update_arc)
        self.remove(dot)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_an_animation__f87fabe115/step_03.mp3")  # [auto-injected] duration=9.14s
        _audio_dur_3 = 9.14  # [audio-sync] actual TTS duration
        # Step 4: Indicate traced arc, then morph it into circumference_line and show label
        self.play(Indicate(self.objects["traced_arc"], color=GREEN, run_time=1))
        # Prepare the circumference_line to be visible and at the same position as traced_arc for transform
        self.objects["circumference_line"].move_to(self.objects["traced_arc"].get_center())
        self.objects["circumference_line"].set_stroke(opacity=1.0)
        self.play(Transform(self.objects["traced_arc"], self.objects["circumference_line"]),
                  Write(self.objects["label_c"]), run_time=3.0)
        # After transform, update reference
        self.objects["traced_arc"] = self.objects["circumference_line"]
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_an_animation__f87fabe115/step_04.mp3")  # [auto-injected] duration=6.91s
        _audio_dur_4 = 6.91  # [audio-sync] actual TTS duration
        # Step 5: Create three diameter segments and label 3D
        self.play(Create(self.objects["diameter_seg_1"]),
                  Create(self.objects["diameter_seg_2"]),
                  Create(self.objects["diameter_seg_3"]),
                  Write(self.objects["label_3d"]), run_time=3.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_an_animation__f87fabe115/step_05.mp3")  # [auto-injected] duration=8.40s
        _audio_dur_5 = 8.40  # [audio-sync] actual TTS duration
        # Step 6: Indicate circumference line, add brace and label, then highlight excess
        self.play(Indicate(self.objects["circumference_line"], color=GREEN, run_time=1))
        self.play(GrowFromCenter(self.objects["comparison_bracket"]),
                  Write(self.objects["brace_label"]), run_time=2.0)
        # Create a vertical line to highlight the excess length
        excess_start = self.objects["diameter_seg_3"].get_end()
        excess_end = self.objects["circumference_line"].get_end()
        excess_line = DashedLine(excess_start, excess_end, color=RED, stroke_width=4)
        self.play(Create(excess_line), run_time=1.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_an_animation__f87fabe115/step_06.mp3")  # [auto-injected] duration=10.06s
        _audio_dur_6 = 10.06  # [audio-sync] actual TTS duration
        # Step 7: Circumscribe footer text, then write it
        self.play(Circumscribe(self.objects["footer_text"], color=ORANGE, run_time=1))
        self.play(Write(self.objects["footer_text"]), run_time=4.0)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))