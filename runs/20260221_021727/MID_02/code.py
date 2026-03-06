'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the ratio 2:5 (milk to water) using a tape diagram.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for milk segments and water segments to keep them together for bracing.
#    - All segments placed edge-to-edge (buff=0) within the tape outline.
#    - Labels positioned relative to braces.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Write title.
#    - Step 2: Indicate and create tape outline.
#    - Steps 3-5: Transform dots into segments (milk then water).
#    - Step 6: Circumscribe milk group, create brace and label.
#    - Step 7: Indicate and write ratio notation.
#    - Step 8: Indicate tape outline, write explanation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout zones
        title_anchor = 3.5 * UP
        diagram_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Visualizing the Ratio 2:5 (Milk to Water)", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Tape outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        tape_outline.move_to(diagram_anchor)
        self.objects["tape_outline"] = tape_outline
        
        # Create segments (initially as dots for transformation)
        # We'll create them at their final positions but store them for later transformation from dots
        segment_width = 1.0
        segment_height = 1.0
        milk_color = "#66B3FF"
        water_color = "#CCE5FF"
        
        # Segment 1 (Milk)
        segment_1 = Rectangle(width=segment_width, height=segment_height, color=milk_color, fill_opacity=0.7, stroke_width=2)
        segment_1.move_to(diagram_anchor + 3.0 * LEFT)
        self.objects["segment_1"] = segment_1
        
        # Segment 2 (Milk)
        segment_2 = Rectangle(width=segment_width, height=segment_height, color=milk_color, fill_opacity=0.7, stroke_width=2)
        segment_2.next_to(segment_1, RIGHT, buff=0.0)
        self.objects["segment_2"] = segment_2
        
        # Segment 3 (Water)
        segment_3 = Rectangle(width=segment_width, height=segment_height, color=water_color, fill_opacity=0.7, stroke_width=2)
        segment_3.next_to(segment_2, RIGHT, buff=0.0)
        self.objects["segment_3"] = segment_3
        
        # Segment 4 (Water)
        segment_4 = Rectangle(width=segment_width, height=segment_height, color=water_color, fill_opacity=0.7, stroke_width=2)
        segment_4.next_to(segment_3, RIGHT, buff=0.0)
        self.objects["segment_4"] = segment_4
        
        # Segment 5 (Water)
        segment_5 = Rectangle(width=segment_width, height=segment_height, color=water_color, fill_opacity=0.7, stroke_width=2)
        segment_5.next_to(segment_4, RIGHT, buff=0.0)
        self.objects["segment_5"] = segment_5
        
        # Segment 6 (Water)
        segment_6 = Rectangle(width=segment_width, height=segment_height, color=water_color, fill_opacity=0.7, stroke_width=2)
        segment_6.next_to(segment_5, RIGHT, buff=0.0)
        self.objects["segment_6"] = segment_6
        
        # Segment 7 (Water)
        segment_7 = Rectangle(width=segment_width, height=segment_height, color=water_color, fill_opacity=0.7, stroke_width=2)
        segment_7.next_to(segment_6, RIGHT, buff=0.0)
        self.objects["segment_7"] = segment_7
        
        # Create VGroups for milk and water segments
        milk_segments = VGroup(segment_1, segment_2)
        water_segments = VGroup(segment_3, segment_4, segment_5, segment_6, segment_7)
        
        # Milk brace and label
        milk_brace = Brace(milk_segments, UP, color=YELLOW)
        milk_brace.next_to(milk_segments, UP, buff=0.1)
        self.objects["milk_brace"] = milk_brace
        
        label_milk = Text("Milk", color=milk_color, font_size=28)
        label_milk.next_to(milk_brace, UP, buff=0.2)
        self.objects["label_milk"] = label_milk
        
        # Water brace and label
        water_brace = Brace(water_segments, UP, color=YELLOW)
        water_brace.next_to(water_segments, UP, buff=0.1)
        self.objects["water_brace"] = water_brace
        
        label_water = Text("Water", color=water_color, font_size=28)
        label_water.next_to(water_brace, UP, buff=0.2)
        self.objects["label_water"] = label_water
        
        # Ratio notation
        label_ratio = MathTex("2 : 5", color=YELLOW, font_size=40)
        label_ratio.next_to(tape_outline, DOWN, buff=0.8)
        self.objects["label_ratio"] = label_ratio
        
        # Parts labels
        label_parts_milk = MathTex("2\\text{ parts}", color=milk_color, font_size=24)
        label_parts_milk.next_to(milk_brace, DOWN, buff=0.2)
        self.objects["label_parts_milk"] = label_parts_milk
        
        label_parts_water = MathTex("5\\text{ parts}", color=water_color, font_size=24)
        label_parts_water.next_to(water_brace, DOWN, buff=0.2)
        self.objects["label_parts_water"] = label_parts_water
        
        # Explanation text
        explanation_text = Text(
            "The tape diagram shows 2 parts milk for every 5 parts water, a total of 7 equal parts.",
            color=GRAY_B, font_size=26
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        step = {
            "step": 1,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_00.mp3",
            "duration": 4.944
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Write(self.objects["title"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 1.0)))
        
        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "tape_outline", "color": "WHITE"},
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_01.mp3",
            "duration": 7.968
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action"):
            self.play(Indicate(self.objects["tape_outline"], color=WHITE))
        self.play(Create(self.objects["tape_outline"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Step 3: First milk segment (transform from dot)
        step = {
            "step": 3,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_02.mp3",
            "duration": 3.264
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Create starting dot at left edge of tape
        start_dot_1 = Dot(point=self.objects["tape_outline"].get_left(), color=milk_color, radius=0.05)
        self.play(Transform(start_dot_1, self.objects["segment_1"]))
        self.remove(start_dot_1)
        self.add(self.objects["segment_1"])
        self.wait(max(0.1, max(0.1, step["duration"] - 1.0)))
        
        # Step 4: Second milk segment
        step = {
            "step": 4,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_03.mp3",
            "duration": 2.328
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        start_dot_2 = Dot(point=self.objects["segment_1"].get_right(), color=milk_color, radius=0.05)
        self.play(Transform(start_dot_2, self.objects["segment_2"]))
        self.remove(start_dot_2)
        self.add(self.objects["segment_2"])
        self.wait(max(0.1, max(0.1, step["duration"] - 1.0)))
        
        # Step 5: Water segments (animate first one, then quickly the rest)
        step = {
            "step": 5,
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_04.mp3",
            "duration": 3.312
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # First water segment
        start_dot_3 = Dot(point=self.objects["segment_2"].get_right(), color=water_color, radius=0.05)
        self.play(Transform(start_dot_3, self.objects["segment_3"]))
        self.remove(start_dot_3)
        self.add(self.objects["segment_3"])
        
        # Quickly add remaining water segments
        water_segments_remaining = [self.objects["segment_4"], self.objects["segment_5"], 
                                   self.objects["segment_6"], self.objects["segment_7"]]
        for seg in water_segments_remaining:
            start_dot = Dot(point=seg.get_center(), color=water_color, radius=0.05)
            self.play(Transform(start_dot, seg), run_time=0.3)
            self.remove(start_dot)
            self.add(seg)
        
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Step 6: Milk group brace and label
        step = {
            "step": 6,
            "signal_action": {"type": "Circumscribe", "target": "VGroup(segment_1, segment_2)", "color": "YELLOW"},
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_05.mp3",
            "duration": 5.832
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action"):
            self.play(Circumscribe(milk_segments, color=YELLOW, run_time=1))
        self.play(Create(self.objects["milk_brace"]))
        self.play(Write(self.objects["label_milk"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 3.0)))
        
        # Also create water brace and label (implied by the narrative)
        self.play(Create(self.objects["water_brace"]))
        self.play(Write(self.objects["label_water"]))
        
        # Add parts labels
        self.play(Write(self.objects["label_parts_milk"]))
        self.play(Write(self.objects["label_parts_water"]))
        
        # Step 7: Ratio notation
        step = {
            "step": 7,
            "signal_action": {"type": "Indicate", "target": "label_ratio", "color": "YELLOW"},
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_06.mp3",
            "duration": 5.424
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action"):
            self.play(Indicate(self.objects["label_ratio"], color=YELLOW))
        self.play(Write(self.objects["label_ratio"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Step 8: Explanation
        step = {
            "step": 8,
            "signal_action": {"type": "Indicate", "target": "tape_outline", "color": "WHITE"},
            "audio_path": "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_07.mp3",
            "duration": 3.552
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action"):
            self.play(Indicate(self.objects["tape_outline"], color=WHITE))
        self.play(Write(self.objects["explanation_text"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Final pause
        self.wait(max(0.1, 2))