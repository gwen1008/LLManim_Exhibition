from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Create Layout Engine
        layout = LayoutEngine()

        # 1. Create Anchors (as per layout_plan.anchors)
        # We'll create dummy invisible mobjects for anchors and add them to layout
        title_anchor_mob = Dot(ORIGIN, radius=0).set_opacity(0)
        content_center_mob = Dot(ORIGIN, radius=0).set_opacity(0)
        footer_anchor_mob = Dot(ORIGIN, radius=0).set_opacity(0)

        obj_title_anchor = LayoutObject(title_anchor_mob, "title_anchor")
        obj_content_center = LayoutObject(content_center_mob, "content_center")
        obj_footer_anchor = LayoutObject(footer_anchor_mob, "footer_anchor")

        layout.add(obj_title_anchor)
        layout.add(obj_content_center)
        layout.add(obj_footer_anchor)

        # Place anchors in their zones
        layout.add_to_zone(obj_title_anchor, "HEADER")
        layout.add_to_zone(obj_content_center, "CONTENT")
        layout.add_to_zone(obj_footer_anchor, "FOOTER")
        # Anchor them to center horizontally
        layout.add_constraint(obj_title_anchor.center_x == 0)
        layout.add_constraint(obj_content_center.center_x == 0)
        layout.add_constraint(obj_footer_anchor.center_x == 0)

        # 2. Create Objects from layout_plan.objects
        # Title
        title = Text("Tape Diagram: Ratio of Milk to Water", font_size=40, color=WHITE)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.align_to(obj_title, obj_title_anchor, 'CENTER')

        # Milk Rectangle
        milk_rect = Rectangle(width=2.0, height=1.5, color="#F0F0F0", fill_color="#F0F0F0", fill_opacity=0.8, stroke_width=3)
        self.objects["milk_rect"] = milk_rect

        # Water Rectangle
        water_rect = Rectangle(width=5.0, height=1.5, color="#87CEEB", fill_color="#87CEEB", fill_opacity=0.8, stroke_width=3)
        self.objects["water_rect"] = water_rect

        # Tape Group (VGroup)
        tape_group = VGroup(milk_rect, water_rect)
        self.objects["tape_group"] = tape_group
        obj_tape_group = LayoutObject(tape_group, "tape_group")
        layout.add(obj_tape_group)
        layout.add_to_zone(obj_tape_group, "CONTENT")
        # Position tape group relative to content center anchor (left edge at center)
        # We'll align the left edge of milk_rect to the content center anchor's center
        # This requires a custom constraint: milk_rect.get_left() == content_center.get_center()
        # Since LayoutObject doesn't have get_left() as a variable, we'll position after solve.
        # We'll instead align the center of the tape group to the content center, then shift left later.
        layout.align_to(obj_tape_group, obj_content_center, 'CENTER')

        # Labels
        label_milk = Text("Milk (2x)", font_size=28, color="#F0F0F0")
        self.objects["label_milk"] = label_milk
        obj_label_milk = LayoutObject(label_milk, "label_milk")
        layout.add(obj_label_milk)
        # Position will be set relative to milk_rect after layout solve

        label_water = Text("Water (5x)", font_size=28, color="#87CEEB")
        self.objects["label_water"] = label_water
        obj_label_water = LayoutObject(label_water, "label_water")
        layout.add(obj_label_water)

        label_ratio = Text("Ratio: 2 : 5", font_size=36, color=YELLOW, weight=BOLD)
        self.objects["label_ratio"] = label_ratio
        obj_label_ratio = LayoutObject(label_ratio, "label_ratio")
        layout.add(obj_label_ratio)
        layout.add_to_zone(obj_label_ratio, "CONTENT")
        # Position above tape group, we'll set after solve

        explanation = Text("The scaling factor 'x' makes the ratio applicable to any quantity.", font_size=24, color=GRAY_B)
        self.objects["explanation"] = explanation
        obj_explanation = LayoutObject(explanation, "explanation")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.align_to(obj_explanation, obj_footer_anchor, 'CENTER')

        # Solve the layout to get initial positions
        layout.solve()

        # Now apply relative positioning that couldn't be expressed with constraints
        # Position milk_rect left edge at content center (which is at ORIGIN after solve)
        tape_group.move_to(obj_content_center.get_center())
        # Align milk_rect left edge to origin
        milk_rect.align_to(ORIGIN, LEFT)
        # Place water_rect next to milk_rect with no gap
        water_rect.next_to(milk_rect, RIGHT, buff=0)
        water_rect.align_to(milk_rect, DOWN)

        # Position labels relative to their rectangles
        label_milk.next_to(milk_rect, UP, buff=0.3)
        label_water.next_to(water_rect, UP, buff=0.3)
        label_ratio.next_to(tape_group, UP, buff=0.8)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        # Audio
        audio_file = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_00.mp3"
        self.add_sound(audio_file)
        # Signal Action: Write title
        self.play(Write(title))
        # Visual Action: Create tape_group
        self.play(Create(tape_group))
        # Wait for remaining audio
        animation_time = 1.0 + 1.0  # Approximate run_time for Write and Create
        remaining = 4.8 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        audio_file = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_01.mp3"
        self.add_sound(audio_file)
        # Signal Action: Indicate milk_rect
        self.play(Indicate(milk_rect, color=WHITE))
        # Visual Action: Write label_milk
        self.play(Write(label_milk))
        animation_time = 1.0 + 1.0
        remaining = 4.272 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        audio_file = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_02.mp3"
        self.add_sound(audio_file)
        # Signal Action: Indicate water_rect
        self.play(Indicate(water_rect, color=BLUE))
        # Visual Action: Write label_water
        self.play(Write(label_water))
        animation_time = 1.0 + 1.0
        remaining = 4.536 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        audio_file = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_03.mp3"
        self.add_sound(audio_file)
        # Signal Action: Circumscribe tape_group
        self.play(Circumscribe(tape_group, color=YELLOW, run_time=1))
        # Visual Action: Write label_ratio
        self.play(Write(label_ratio))
        animation_time = 1.0 + 1.0
        remaining = 8.112 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        audio_file = "media/audio/一種混合物含有_2_份牛奶與_5_份水__af84ced948/step_04.mp3"
        self.add_sound(audio_file)
        # Signal Action: Indicate label_milk
        self.play(Indicate(label_milk, color=YELLOW))
        # Visual Action: FadeIn explanation
        self.play(FadeIn(explanation))
        animation_time = 1.0 + 1.0
        remaining = 9.576 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))