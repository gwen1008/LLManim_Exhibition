from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Helper function to parse geometry_def strings (simplified for this specific case)
        def parse_geometry_def(def_str, obj_type):
            # For this specific JSON, geometry_def is a simple list of coordinates or parameters.
            # We'll handle the specific cases present.
            if def_str.startswith("start="):
                # Format: "start=[-3, 0, 0], end=[3, 0, 0]"
                parts = def_str.split(", ")
                start_str = parts[0].replace("start=", "").strip("[]")
                end_str = parts[1].replace("end=", "").strip("[]")
                start = np.array([float(x) for x in start_str.split(",")])
                end = np.array([float(x) for x in end_str.split(",")])
                return start, end
            elif def_str.startswith("radius="):
                # Format: "radius=0.08"
                radius = float(def_str.split("=")[1])
                return radius
            else:
                # Default/unknown, return None
                return None

        # Create objects from layout_plan.objects
        # Object: title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Integer", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Object: number_line
        start, end = parse_geometry_def("start=[-3, 0, 0], end=[3, 0, 0]", "Line")
        number_line = Line(start=start, end=end, color=WHITE, stroke_width=4)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Object: tick_3
        start_t3, end_t3 = parse_geometry_def("start=[-3, -0.2, 0], end=[-3, 0.2, 0]", "Line")
        tick_3 = Line(start=start_t3, end=end_t3, color=WHITE, stroke_width=3)
        # Position relative to number_line start
        tick_3.move_to(number_line.get_start() + np.array([0, 0, 0]))
        self.objects["tick_3"] = tick_3

        # Object: label_3
        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(self.objects["tick_3"], DOWN, buff=0.3)
        self.objects["label_3"] = label_3

        # Object: tick_4
        start_t4, end_t4 = parse_geometry_def("start=[3, -0.2, 0], end=[3, 0.2, 0]", "Line")
        tick_4 = Line(start=start_t4, end=end_t4, color=WHITE, stroke_width=3)
        tick_4.move_to(number_line.get_end() + np.array([0, 0, 0]))
        self.objects["tick_4"] = tick_4

        # Object: label_4
        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(self.objects["tick_4"], DOWN, buff=0.3)
        self.objects["label_4"] = label_4

        # Object: midpoint_line
        start_mid, end_mid = parse_geometry_def("start=[0, -0.8, 0], end=[0, 0.8, 0]", "Line")
        midpoint_line = DashedLine(start=start_mid, end=end_mid, color=YELLOW, stroke_width=3, dash_length=0.1)
        midpoint_line.move_to(content_center + np.array([0, 0, 0]))
        self.objects["midpoint_line"] = midpoint_line

        # Object: label_mid
        label_mid = MathTex("3.5", color=YELLOW)
        label_mid.next_to(midpoint_line.get_top(), UP, buff=0.2)
        self.objects["label_mid"] = label_mid

        # Object: point_37_dot
        radius = parse_geometry_def("radius=0.08", "Dot")
        point_37_dot = Dot(radius=radius, color=GREEN)
        # Position: x = -3 + 6*(3.7 - 3) = -3 + 6*0.7 = -3 + 4.2 = 1.2
        point_37_dot.move_to(np.array([1.2, 0, 0]))
        self.objects["point_37_dot"] = point_37_dot

        # Object: label_37
        label_37 = MathTex("3.7", color=GREEN)
        label_37.next_to(point_37_dot, UP, buff=0.3)
        self.objects["label_37"] = label_37

        # Object: pointer
        pointer = Triangle(color=RED, fill_opacity=1, stroke_width=2)
        pointer.rotate(-90 * DEGREES)
        pointer.scale(0.15)
        pointer.move_to([1.2, 0, 0])
        self.objects["pointer"] = pointer

        # Object: pointer_label
        pointer_label = MathTex("3.7", color=RED)
        pointer_label.next_to(pointer, UP, buff=0.8)
        self.objects["pointer_label"] = pointer_label

        # Object: explanation_text
        explanation_text = Text("Let's create a number line from 3 to 4.", color=GRAY_B, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 2.952 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        audio_step2 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        remaining_2 = max(0.1, 3.168 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        audio_step3 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # Signal action: Indicate label_3
        self.play(Indicate(self.objects["label_3"], color=BLUE, run_time=1))
        # Visual action: Create endpoint ticks and labels
        self.play(
            Create(self.objects["tick_3"]),
            Write(self.objects["label_3"]),
            Create(self.objects["tick_4"]),
            Write(self.objects["label_4"]),
            run_time=2.5
        )
        remaining_3 = max(0.1, 5.28 - 1 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Signal action: Create midpoint_line (but JSON says type: Create, target: midpoint_line, color: YELLOW)
        # This is essentially the same as the visual action, so we'll just do the visual action.
        # Visual action: Create midpoint_line and label_mid
        self.play(
            Create(self.objects["midpoint_line"]),
            Write(self.objects["label_mid"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 9.336 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        audio_step5 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action: Circumscribe label_mid
        self.play(Circumscribe(self.objects["label_mid"], color=YELLOW, run_time=1))
        # Visual action: Create point_37_dot and label_37
        self.play(
            Create(self.objects["point_37_dot"]),
            Write(self.objects["label_37"]),
            run_time=1.5
        )
        remaining_5 = max(0.1, 4.992 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        audio_step6 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # Signal action: Indicate point_37_dot
        self.play(Indicate(self.objects["point_37_dot"], color=GREEN, run_time=1))
        # Visual action: Create pointer
        self.play(Create(self.objects["pointer"]), run_time=1.5)
        remaining_6 = max(0.1, 4.944 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # Signal action: Create pointer_label (but JSON says type: Create, target: pointer_label, color: RED)
        # This is essentially the same as the visual action, so we'll just do the visual action.
        # Visual action: Write pointer_label
        self.play(Write(self.objects["pointer_label"]), run_time=1.5)
        remaining_7 = max(0.1, 3.096 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8
        audio_step8 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Signal action: Indicate label_4
        self.play(Indicate(self.objects["label_4"], color=BLUE, run_time=1))
        # Visual action: Transform pointer to position of tick_4
        # Create a target position for the pointer at the tick_4 location (same y, x at tick_4)
        target_pos = self.objects["tick_4"].get_center()
        self.play(
            self.objects["pointer"].animate.move_to(target_pos).set_color(RED),
            run_time=2.0,
            rate_func=smooth
        )
        remaining_8 = max(0.1, 4.92 - 1 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9
        audio_step9 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # Signal action: Indicate pointer
        self.play(Indicate(self.objects["pointer"], color=RED, run_time=1))
        # Visual action: ReplacementTransform pointer_label from '3.7' to '4'
        # Create new label '4' at the correct position relative to the moved pointer
        new_label = MathTex("4", color=RED)
        new_label.next_to(self.objects["pointer"], UP, buff=0.8)
        self.play(ReplacementTransform(self.objects["pointer_label"], new_label), run_time=1.5)
        self.objects["pointer_label"] = new_label  # Update registry
        remaining_9 = max(0.1, 4.008 - 1 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        audio_step10 = "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # Signal action: Circumscribe pointer_label
        self.play(Circumscribe(self.objects["pointer_label"], color=RED, run_time=1))
        # Visual action: Wait (hold final frame)
        remaining_10 = max(0.1, 4.632 - 1 + 0.5)
        self.wait(max(0.1, remaining_10))