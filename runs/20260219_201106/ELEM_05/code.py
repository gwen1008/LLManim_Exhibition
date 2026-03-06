from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole", 
                    color=WHITE, font_size=36)
        self.objects["title"] = title
        title.to_edge(UP, buff=0.5)
        
        # number_line
        number_line = NumberLine(
            x_range=[3, 4, 0.1], 
            length=6, 
            include_ticks=True, 
            color=LIGHT_GRAY
        )
        self.objects["number_line"] = number_line
        number_line.move_to(ORIGIN)
        
        # endpoint_3
        endpoint_3 = MathTex("3", color=WHITE)
        self.objects["endpoint_3"] = endpoint_3
        endpoint_3.next_to(number_line.number_to_point(3), DOWN, buff=0.3)
        
        # endpoint_4
        endpoint_4 = MathTex("4", color=WHITE)
        self.objects["endpoint_4"] = endpoint_4
        endpoint_4.next_to(number_line.number_to_point(4), DOWN, buff=0.3)
        
        # point_3.7
        point_37 = Dot(radius=0.08, color=YELLOW)
        self.objects["point_3.7"] = point_37
        point_37.move_to(number_line.number_to_point(3.7))
        
        # label_3.7
        label_37 = MathTex("3.7", color=YELLOW)
        self.objects["label_3.7"] = label_37
        label_37.next_to(point_37, UP, buff=0.2)
        
        # segment_to_4
        segment_to_4 = Line(
            start=number_line.number_to_point(3.7),
            end=number_line.number_to_point(4),
            color=GREEN, 
            stroke_width=6
        )
        self.objects["segment_to_4"] = segment_to_4
        
        # label_0.3
        label_03 = MathTex("0.3", color=GREEN)
        self.objects["label_0.3"] = label_03
        label_03.next_to(segment_to_4, UP, buff=0.15)
        
        # segment_to_3
        segment_to_3 = Line(
            start=number_line.number_to_point(3.7),
            end=number_line.number_to_point(3),
            color=RED, 
            stroke_width=6
        )
        self.objects["segment_to_3"] = segment_to_3
        
        # label_0.7
        label_07 = MathTex("0.7", color=RED)
        self.objects["label_0.7"] = label_07
        label_07.next_to(segment_to_3, UP, buff=0.15)
        
        # halfway_mark
        halfway_mark = Dot(radius=0.05, color=BLUE, fill_opacity=0.8)
        self.objects["halfway_mark"] = halfway_mark
        halfway_mark.move_to(number_line.number_to_point(3.5))
        
        # label_half
        label_half = MathTex("0.5", color=BLUE)
        self.objects["label_half"] = label_half
        label_half.next_to(halfway_mark, UP, buff=0.15)
        
        # inequality
        inequality = MathTex("0.7 > 0.5", color=WHITE, font_size=36)
        self.objects["inequality"] = inequality
        inequality.to_edge(DOWN, buff=0.5)
        
        # rounding_statement
        rounding_statement = MathTex("3.7 \\rightarrow 4", color=YELLOW, font_size=36)
        self.objects["rounding_statement"] = rounding_statement
        rounding_statement.move_to(inequality.get_center())
        
        # rounding_arrow
        rounding_arrow = Arrow(
            start=point_37.get_center(),
            end=number_line.number_to_point(4),
            color=YELLOW,
            stroke_width=4
        )
        self.objects["rounding_arrow"] = rounding_arrow
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's consider a number line from 3 to 4.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "number_line",
                    "details": "Draw the number line. Then write the endpoint labels."
                },
                "duration": 3.36,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We want to plot the value 3.7 on this line.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "point_3.7",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "point_3.7",
                    "details": "Fade in the dot at 3.7, then write its label."
                },
                "duration": 3.576,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, let's measure the distances from 3.7 to the nearest whole numbers. The distance to 4 is 0.3.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "segment_to_4",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "segment_to_4",
                    "details": "Draw the green segment from 3.7 to 4, then write the label '0.3'."
                },
                "duration": 7.8,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "And the distance back to 3 is 0.7.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "segment_to_3",
                    "color": "RED"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "segment_to_3",
                    "details": "Draw the red segment from 3.7 to 3, then write the label '0.7'."
                },
                "duration": 3.168,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "The halfway point between 3 and 4 is 3.5, which is a distance of 0.5 from 3.7. The rule for rounding is: if the distance to the lower number is greater than 0.5, we round up.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "label_0.7",
                    "color": "RED"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "halfway_mark",
                    "details": "Show the blue dot at 3.5 and its label '0.5'."
                },
                "duration": 12.888,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "So we compare: is 0.7 greater than 0.5? Yes.",
                "signal_action": None,
                "visual_action": {
                    "type": "Write",
                    "target_id": "inequality",
                    "details": "Write the inequality '0.7 > 0.5' in the footer area."
                },
                "duration": 5.544,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Therefore, since 0.7 is greater than 0.5, the value 3.7 rounds up to 4.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "inequality",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "TransformMatchingTex",
                    "target_id": "inequality",
                    "details": "Morph the inequality '0.7 > 0.5' into the rounding statement '3.7 → 4'. Use TransformMatchingTex to animate the '0.7' becoming '3.7', the '>' becoming '→', and the '0.5' becoming '4'."
                },
                "duration": 6.48,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "Let's visualize this rounding: 3.7 rounds up to 4.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "rounding_statement",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "rounding_arrow",
                    "details": "Draw a yellow arrow from the point at 3.7 gliding to the tick at 4."
                },
                "duration": 4.536,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_07.mp3"
            }
        ]

        # Play title first (not in sequence)
        self.play(Write(title))

        for step in sequence:
            step_num = step["step"]
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects[signal["target"]]
                color = eval(signal["color"]) if signal["color"] in ["YELLOW", "RED", "GREEN", "BLUE"] else YELLOW
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))

            # Visual action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            obj = self.objects[target_id]

            if visual["type"] == "Create":
                if target_id == "number_line":
                    self.play(Create(obj))
                    self.play(Write(self.objects["endpoint_3"]), Write(self.objects["endpoint_4"]))
                    anim_time = 1.0 + 0.5  # Create + Write
                elif target_id == "point_3.7":
                    self.play(FadeIn(obj, scale=0.5))
                    self.play(Write(self.objects["label_3.7"]))
                    anim_time = 0.5 + 0.5
                elif target_id == "segment_to_4":
                    self.play(Create(obj))
                    self.play(Write(self.objects["label_0.3"]))
                    anim_time = 1.0 + 0.5
                elif target_id == "segment_to_3":
                    self.play(Create(obj))
                    self.play(Write(self.objects["label_0.7"]))
                    anim_time = 1.0 + 0.5
                elif target_id == "halfway_mark":
                    self.play(FadeIn(obj, scale=0.5))
                    self.play(Write(self.objects["label_half"]))
                    anim_time = 0.5 + 0.5
                elif target_id == "rounding_arrow":
                    self.play(Create(obj))
                    anim_time = 1.0
                else:
                    self.play(Create(obj))
                    anim_time = 1.0
            elif visual["type"] == "Write":
                self.play(Write(obj))
                anim_time = 1.0
            elif visual["type"] == "TransformMatchingTex":
                target = self.objects["rounding_statement"]
                self.play(TransformMatchingTex(obj, target, path_arc=90))
                # Update registry
                self.objects["inequality"] = target
                anim_time = 2.0

            # Wait for remaining audio
            remaining = step["duration"] - anim_time + 0.5
            if remaining > 0:
                self.wait(remaining)