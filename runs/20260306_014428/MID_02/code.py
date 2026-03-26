'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the part-to-part ratio 2:5 using a tape diagram constructed step-by-step.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for ratio statement
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for partition lines to manage them together. Position labels using next_to relative to fills.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Draw tape outline.
#    - Step 2: Indicate outline, then draw partition lines.
#    - Step 3: Circumscribe milk area, then fill it.
#    - Step 4: Circumscribe water area, then fill it.
#    - Step 5: Indicate milk label, write both labels.
#    - Step 6: Circumscribe ratio text, write it.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        diagram_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Tape Diagram: Milk to Water Ratio", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Tape Outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, stroke_width=3, fill_opacity=0.0)
        tape_outline.move_to(diagram_anchor)
        self.objects["tape_outline"] = tape_outline
        
        # Partition Lines (create them at origin first, will be positioned later)
        # We'll create them and store in a list, then position relative to tape_outline
        partition_lines = []
        for i in range(1, 7):  # lines 1 through 6
            line = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
            partition_lines.append(line)
            self.objects[f"partition_line_{i}"] = line
        
        # Position partition lines relative to tape_outline's left edge
        tape_left = tape_outline.get_left()
        for i, line in enumerate(partition_lines, start=1):
            line.move_to(tape_left + RIGHT * i)
        
        # Milk Fill
        milk_fill = Rectangle(width=2.0, height=1.0, color="#ADD8E6", fill_opacity=0.5, stroke_opacity=0.0)
        milk_fill.align_to(tape_outline, LEFT).align_to(tape_outline, DOWN)
        self.objects["milk_fill"] = milk_fill
        
        # Water Fill
        water_fill = Rectangle(width=5.0, height=1.0, color="#87CEEB", fill_opacity=0.5, stroke_opacity=0.0)
        water_fill.next_to(milk_fill, RIGHT, buff=0.0)
        self.objects["water_fill"] = water_fill
        
        # Labels
        label_milk = Text("milk", color="#ADD8E6", font_size=28)
        label_milk.next_to(milk_fill, UP, buff=0.3)
        self.objects["label_milk"] = label_milk
        
        label_water = Text("water", color="#87CEEB", font_size=28)
        label_water.next_to(water_fill, UP, buff=0.3)
        self.objects["label_water"] = label_water
        
        # Ratio Text
        ratio_text = Tex(r"Milk : Water $= 2 : 5$", color=YELLOW, font_size=36)
        ratio_text.move_to(explanation_anchor)
        self.objects["ratio_text"] = ratio_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # [missing audio] self.add_sound("media/audio/Create_a_tape_diagra_037339ca3f/step_00.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_0 = 2.00  # [audio-sync] actual TTS duration
        # Step 1: Draw tape outline
        self.play(Create(self.objects["tape_outline"]), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))
        
        # [missing audio] self.add_sound("media/audio/Create_a_tape_diagra_037339ca3f/step_01.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2: Indicate outline, then draw partition lines
        self.play(Indicate(self.objects["tape_outline"], color=YELLOW, run_time=1))
        # Create partition lines sequentially
        for i in range(1, 7):
            self.play(Create(self.objects[f"partition_line_{i}"]), run_time=0.3)
        anim_time_2 = 1 + 6*0.3  # Indicate + 6 lines
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))
        
        # [missing audio] self.add_sound("media/audio/Create_a_tape_diagra_037339ca3f/step_02.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3: Circumscribe milk area, then fill it
        self.play(Circumscribe(self.objects["milk_fill"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["milk_fill"]), run_time=1.5)
        anim_time_3 = 1 + 1.5
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))
        
        # [missing audio] self.add_sound("media/audio/Create_a_tape_diagra_037339ca3f/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4: Circumscribe water area, then fill it
        self.play(Circumscribe(self.objects["water_fill"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["water_fill"]), run_time=1.5)
        anim_time_4 = 1 + 1.5
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))
        
        # [missing audio] self.add_sound("media/audio/Create_a_tape_diagra_037339ca3f/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5: Indicate milk label, write both labels
        self.play(Indicate(self.objects["label_milk"], color=WHITE, run_time=1))
        self.play(Write(self.objects["label_milk"]), Write(self.objects["label_water"]), run_time=2.0)
        anim_time_5 = 1 + 2.0
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Create_a_tape_diagra_037339ca3f/step_05.mp3")  # [auto-injected] duration=6.62s
        _audio_dur_5 = 6.62  # [audio-sync] actual TTS duration
        # Step 6: Circumscribe ratio text, write it
        self.play(Circumscribe(self.objects["ratio_text"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["ratio_text"]), run_time=2.0)
        anim_time_6 = 1 + 2.0
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))