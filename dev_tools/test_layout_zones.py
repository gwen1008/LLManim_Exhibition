from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import sys

class TestLayoutZones(Scene):
    def construct(self):
        print("\n--- Testing Layout Zones ---")
        layout = LayoutEngine()
        
        # 1. Create Objects
        header_text = Text("Header Title")
        content_math = MathTex("a^2 + b^2 = c^2")
        footer_text = Text("Footer Explanation")
        
        # 2. Add to Layout Engine
        obj_h = LayoutObject(header_text, "header")
        obj_c = LayoutObject(content_math, "content")
        obj_f = LayoutObject(footer_text, "footer")
        
        layout.add(obj_h)
        layout.add(obj_c)
        layout.add(obj_f)
        
        # 3. Add to Zones
        layout.add_to_zone(obj_h, "HEADER")
        layout.add_to_zone(obj_c, "CONTENT")
        layout.add_to_zone(obj_f, "FOOTER")
        
        # 4. Add Layout Constraints (Center them roughly or relative to each other)
        # Without other constraints, kiwisolver might pick any valid position in zone.
        # Let's say we want them centered horizontally.
        
        # Use a dummy anchor for centering
        # Simply align to 0? No, kiwisolver variables are abstract.
        # We can add explicit constraints: center_x == 0
        layout.add_constraint(obj_h.center_x == 0)
        layout.add_constraint(obj_c.center_x == 0)
        layout.add_constraint(obj_f.center_x == 0)
        
        # Also constraint them vertically to be in the distinct regions
        # Kiwisolver will try to satisfy zone constraints.
        
        # 5. Solve
        layout.solve()
        
        # 6. Verify Positions
        print(f"Header Y: {header_text.get_y()} (Expected: 3.0 ~ 3.5)")
        print(f"Content Y: {content_math.get_y()} (Expected: -2.5 ~ 3.0)")
        print(f"Footer Y: {footer_text.get_y()} (Expected: -3.5 ~ -2.5)")
        
        # Assertions
        h_y = header_text.get_y()
        c_y = content_math.get_y()
        f_y = footer_text.get_y()
        
        # Check if centers are roughly correct (considering height)
        # Header Top <= 3.5, Bottom >= 3.0
        # Actually constraints are: top <= 3.5, bottom >= 3.0 (Wait, zone is [3.0, 3.5])
        # So the object must be INSIDE.
        # Header height is small (~0.5), so it fits.
        
        if 3.0 <= h_y - header_text.height/2 and h_y + header_text.height/2 <= 3.5:
             print("✅ Header is strictly within defined zone.")
        else:
             print("⚠️ Header might be sticking out (or just centered within large zone).")
             # Kiwisolver satisfies weak or required? Required.
        
        # Visual visuality
        self.add(header_text, content_math, footer_text)
        
        # Draw zones for reference
        for zone_name, zone_obj in layout.zones.items():
            rect = Rectangle(
                width=zone_obj.max_x - zone_obj.min_x,
                height=zone_obj.max_y - zone_obj.min_y
            )
            rect.move_to([
                (zone_obj.max_x + zone_obj.min_x)/2,
                (zone_obj.max_y + zone_obj.min_y)/2,
                0
            ])
            rect.set_stroke(color=GRAY, width=2)
            self.add(rect)
            self.add(Text(zone_name, color=GRAY, font_size=24).move_to(rect.get_corner(UL) + DR*0.2))

        print("--- End Test ---")
