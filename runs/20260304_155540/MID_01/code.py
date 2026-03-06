'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing subtraction as distance/direction on a number line, specifically 3 - (-2) = 5.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Jump on a Number Line"
#    - Main Content: [Center y=0] for the number line, dots, and arrow.
#    - Footer Region: [Bottom y=-3.5] for the final calculation "3 - (-2) = 5"
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for start (dot+label) and end (dot+label). Position labels above dots with buff. Anchor number line at ORIGIN.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`? Yes, for each step.
# 5. Animation Flow:
#    Step 1: Create number line.
#    Step 2: Indicate start dot, then create start/end dots and labels.
#    Step 3: Circumscribe arrow, then create full arrow.
#    Step 4: Indicate arrow, then animate it sliding (using Create from start to end).
#    Step 5: Indicate calculation, then write it at the bottom.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Jump on a Number Line", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        # Note: GRAY_C is not a standard color. Use GRAY_B or LIGHT_GREY (British spelling).
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=11,
            include_numbers=True,
            color=GRAY_B  # Using GRAY_B as a light gray
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # start_dot
        start_dot = Dot(radius=0.08, color=GREEN)
        start_dot.move_to(number_line.n2p(-2))
        self.objects["start_dot"] = start_dot

        # end_dot
        end_dot = Dot(radius=0.08, color=RED)
        end_dot.move_to(number_line.n2p(3))
        self.objects["end_dot"] = end_dot

        # start_label
        start_label = MathTex("-2", color=GREEN)
        start_label.next_to(start_dot, UP, buff=0.2)
        self.objects["start_label"] = start_label

        # end_label
        end_label = MathTex("+3", color=RED)
        end_label.next_to(end_dot, UP, buff=0.2)
        self.objects["end_label"] = end_label

        # jump_arrow
        # Arrow geometry: start and end from dot centers, buff=0.
        # We'll create it initially at the start point, but its full geometry is defined.
        jump_arrow = Arrow(
            start=start_dot.get_center(),
            end=end_dot.get_center(),
            buff=0,
            color=YELLOW,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        # The arrow is already positioned correctly by its start/end points.
        self.objects["jump_arrow"] = jump_arrow

        # jump_calculation
        jump_calculation = MathTex("3 - (-2) = 5", color=YELLOW, font_size=36)
        jump_calculation.move_to(explanation_anchor)
        self.objects["jump_calculation"] = jump_calculation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/On_a_number_line_ran_2492284b94/step_00.mp3")  # [auto-injected] duration=5.21s
        _audio_dur_0 = 5.21  # [audio-sync] actual TTS duration
        # Step 1: Create number_line
        # narrative: "Let's begin with our number line, ranging from negative five to positive five."
        # signal_action: null
        # visual_action: Create number_line
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/On_a_number_line_ran_2492284b94/step_01.mp3")  # [auto-injected] duration=4.25s
        _audio_dur_1 = 4.25  # [audio-sync] actual TTS duration
        # Step 2: Create start and end points with labels
        # narrative: "We start our jump at negative two, and we end at positive three."
        # signal_action: Indicate start_dot (GREEN)
        # visual_action: Create [start_dot, start_label, end_dot, end_label] simultaneously
        self.play(Indicate(self.objects["start_dot"], color=GREEN, run_time=1))
        self.play(
            Create(self.objects["start_dot"]),
            Create(self.objects["end_dot"]),
            Write(self.objects["start_label"]),
            Write(self.objects["end_label"]),
            run_time=1.5
        )
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/On_a_number_line_ran_2492284b94/step_02.mp3")  # [auto-injected] duration=3.86s
        _audio_dur_2 = 3.86  # [audio-sync] actual TTS duration
        # Step 3: Create the jump arrow
        # narrative: "The jump from start to end is represented by this arrow."
        # signal_action: Circumscribe jump_arrow (YELLOW)
        # visual_action: Create jump_arrow (draw full arrow)
        self.play(Circumscribe(self.objects["jump_arrow"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["jump_arrow"]), run_time=1.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/On_a_number_line_ran_2492284b94/step_03.mp3")  # [auto-injected] duration=6.94s
        _audio_dur_3 = 6.94  # [audio-sync] actual TTS duration
        # Step 4: Animate the arrow sliding
        # narrative: "Watch the arrow move, tracing the path of the jump. It travels five units in the positive direction."
        # signal_action: Indicate jump_arrow (ORANGE)
        # visual_action: Animate arrow sliding. We'll achieve this by creating a copy that grows from start to end.
        # Implementation: Create a new arrow with zero length at start, then transform it to the full arrow.
        self.play(Indicate(self.objects["jump_arrow"], color=ORANGE, run_time=1))

        # Create a zero-length arrow at the start point
        sliding_arrow = Arrow(
            start=start_dot.get_center(),
            end=start_dot.get_center(),  # Zero length
            buff=0,
            color=YELLOW,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        # Replace the static arrow with the sliding one for the animation
        self.remove(self.objects["jump_arrow"])
        self.add(sliding_arrow)
        # Animate it growing to the full length
        self.play(
            Transform(
                sliding_arrow,
                self.objects["jump_arrow"],
                run_time=3.0,
                rate_func=linear
            )
        )
        # Restore the original arrow
        self.remove(sliding_arrow)
        self.add(self.objects["jump_arrow"])

        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/On_a_number_line_ran_2492284b94/step_04.mp3")  # [auto-injected] duration=9.10s
        _audio_dur_4 = 9.10  # [audio-sync] actual TTS duration
        # Step 5: Write the calculation
        # narrative: "We can calculate this jump precisely. The distance is the end point minus the start point: three minus negative two equals five."
        # signal_action: Indicate jump_calculation (YELLOW)
        # visual_action: Write jump_calculation
        self.play(Indicate(self.objects["jump_calculation"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["jump_calculation"]), run_time=1.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))