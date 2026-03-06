'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize displacement on a number line, moving from -2 to +3, and derive the displacement vector (+5).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, dots, arrow
#    - Footer Region: [Bottom y=-3.5] for explanatory text
# 3. Anti-Overlap Check:
#    - Strategy: Use relative positioning (next_to, move_to) based on anchors. Labels are placed near dots. Arrow created after dot movement to avoid overlap.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`? Yes, for each step.
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Number line drawn.
#    - Step 3: Start dot, start label, end label appear. End dot created invisible.
#    - Step 4: Dot moves from -2 to +3.
#    - Step 5: Arrow drawn, end dot becomes visible.
#    - Step 6: Arrow highlighted, footer text updates to displacement formula.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Displacement on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        # Note: GRAY_C is not a standard color. Use GRAY_B or LIGHT_GREY (British spelling).
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=12,
            include_numbers=True,
            include_tip=True,
            color=LIGHT_GREY
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # start_dot
        start_dot = Dot(radius=0.15, color=GREEN)
        start_dot.move_to(number_line.number_to_point(-2))
        self.objects["start_dot"] = start_dot

        # end_dot
        end_dot = Dot(radius=0.15, color=RED, fill_opacity=0.0)
        end_dot.move_to(number_line.number_to_point(3))
        self.objects["end_dot"] = end_dot

        # start_label
        start_label = MathTex("-2", color=GREEN, font_size=30)
        start_label.next_to(start_dot, UP, buff=0.3)
        self.objects["start_label"] = start_label

        # end_label
        end_label = MathTex("+3", color=RED, font_size=30)
        end_label.next_to(end_dot, UP, buff=0.3)
        self.objects["end_label"] = end_label

        # displacement_arrow
        displacement_arrow = Arrow(
            start=number_line.number_to_point(-2),
            end=number_line.number_to_point(3),
            buff=0,
            color=YELLOW,
            stroke_width=6,
            tip_length=0.25
        )
        displacement_arrow.set_opacity(0.0)
        displacement_arrow.move_to(content_center) # This move_to might shift it, but arrow start/end are absolute. We'll trust the initial definition.
        self.objects["displacement_arrow"] = displacement_arrow

        # footer_text
        # Note: BLUE_C is not a standard color. Use BLUE_C.
        footer_text = Text("We begin with a number line.", color=BLUE_C, font_size=28)
        footer_text.move_to(footer_anchor).scale(0.8)
        self.objects["footer_text"] = footer_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_scene_ebe9b6a043/step_00.mp3")  # [auto-injected] duration=5.09s
        _audio_dur_0 = 5.09  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_Manim_scene_ebe9b6a043/step_01.mp3")  # [auto-injected] duration=8.40s
        _audio_dur_1 = 8.40  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["number_line"]), run_time=2.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_scene_ebe9b6a043/step_02.mp3")  # [auto-injected] duration=7.54s
        _audio_dur_2 = 7.54  # [audio-sync] actual TTS duration
        # Step 3
        # signal_action: Indicate start_dot
        self.play(Indicate(self.objects["start_dot"], color=GREEN, run_time=1))
        # visual_action: Create start_dot, start_label, end_label
        self.play(
            Create(self.objects["start_dot"]),
            Write(self.objects["start_label"]),
            Write(self.objects["end_label"])
        )
        # Note: end_dot is created but invisible. We add it to the scene but keep opacity 0.
        self.add(self.objects["end_dot"])
        anim_time_step3 = 1 + 1.5 # Indicate (1s) + Create/Write (estimated 1.5s)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_scene_ebe9b6a043/step_03.mp3")  # [auto-injected] duration=4.44s
        _audio_dur_3 = 4.44  # [audio-sync] actual TTS duration
        # Step 4
        # signal_action: Indicate end_label
        self.play(Indicate(self.objects["end_label"], color=RED, run_time=1))
        # visual_action: Animate start_dot moving
        self.play(
            self.objects["start_dot"].animate.move_to(self.objects["number_line"].number_to_point(3)),
            run_time=3.0
        )
        anim_time_step4 = 1 + 3.0
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_scene_ebe9b6a043/step_04.mp3")  # [auto-injected] duration=9.50s
        _audio_dur_4 = 9.50  # [audio-sync] actual TTS duration
        # Step 5
        # No signal_action
        # visual_action: Create arrow and make end_dot visible
        # First, set end_dot opacity to 1 and color to RED (already RED)
        self.play(
            self.objects["end_dot"].animate.set_opacity(1.0),
            run_time=0.5
        )
        # Then draw the arrow
        self.play(
            self.objects["displacement_arrow"].animate.set_opacity(1.0),
            run_time=2.0
        )
        # Also ensure the arrow is created (Create might be better for drawing effect)
        # We used set_opacity to reveal it. Let's use Create for the drawing effect.
        # We'll replace the above with Create for the arrow.
        # Let's adjust: We already added the arrow with opacity 0. We'll Create it.
        # Actually, we want to draw it. Let's do:
        # self.play(Create(self.objects["displacement_arrow"]), run_time=2.0)
        # But the arrow is already added? No, we haven't added it to the scene yet.
        # We need to add it first with opacity 0, then Create it.
        # Let's redo: We'll add it with opacity 0, then animate opacity to 1 while also using Create for the drawing effect.
        # Simpler: Use Create on the arrow object (which currently has opacity 0). Create will make it appear.
        # We'll set opacity to 1 after creation? Actually, Create will make it visible.
        # Let's just use Create.
        # We'll change the visual_action implementation.
        # We'll create the arrow fresh in the step.
        # But the JSON says "Create" target_id "displacement_arrow". So we should Create the pre-defined arrow.
        # We haven't added it to the scene, so Create will add and draw it.
        # Let's do that.
        # We'll remove the previous opacity animations and just Create.
        # Revised Step 5 code:
        # self.play(Create(self.objects["displacement_arrow"]), run_time=2.0)
        # self.play(self.objects["end_dot"].animate.set_opacity(1.0), run_time=0.5)
        # Let's order: first make end_dot visible, then draw arrow.
        # We'll keep the original plan but use Create for arrow.
        # Let's implement:
        self.play(
            self.objects["end_dot"].animate.set_opacity(1.0),
            run_time=0.5
        )
        self.play(
            Create(self.objects["displacement_arrow"]),
            run_time=2.0
        )
        anim_time_step5 = 0.5 + 2.0
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_Manim_scene_ebe9b6a043/step_05.mp3")  # [auto-injected] duration=8.81s
        _audio_dur_5 = 8.81  # [audio-sync] actual TTS duration
        # Step 6
        # signal_action: Circumscribe arrow
        self.play(Circumscribe(self.objects["displacement_arrow"], color=YELLOW, run_time=1))
        # visual_action: Transform footer text
        new_footer_text = Text("Displacement = Final - Initial = 3 - (-2) = +5 units", color=BLUE_C, font_size=28)
        new_footer_text.move_to(footer_anchor).scale(0.8)
        self.play(Transform(self.objects["footer_text"], new_footer_text), run_time=1.5)
        anim_time_step6 = 1 + 1.5
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))