from manim import *

class LayoutZoneVisualizer(Scene):
    def construct(self):
        # 1. Define Zones
        # HEADER: y in [3.0, 3.5], width 14 (full screen)
        # CONTENT: y in [-2.5, 3.0], width 13 (padding 0.5)
        # FOOTER: y in [-3.5, -2.5], width 14
        
        # Draw Header Zone (Top Banner)
        header_rect = Rectangle(width=14.2, height=1.0) # slightly larger than camera frame
        header_rect.set_fill(YELLOW, opacity=0.3)
        header_rect.set_stroke(YELLOW, width=2)
        header_rect.move_to([0, 3.5, 0]) # Center at y=3.5 (Top edge is y=4.0, bottom y=3.0)
        # Correction: Frame top is y=4.0. So range [3.0, 4.0] height is 1.0.
        # Ideally header is thin? User requested [3.0, 3.5].
        # Let's visualize EXACTLY what I proposed: y in [3.0, 3.5]
        
        # PROPOSAL 1 REVISION:
        # User prompt said: HEADER [3.0, 3.5]
        # Let's assume standard full width (-7.1 to 7.1)
        
        # Header: y [3.0, 3.5]
        h_rect = Rectangle(width=14.0, height=0.5)
        h_rect.move_to([0, 3.25, 0])
        h_rect.set_fill(YELLOW, opacity=0.4)
        h_rect.set_stroke(YELLOW, width=4)
        h_label = Text("HEADER Zone", color=BLACK).scale(0.8).move_to(h_rect)
        h_range = MathTex(r"y \in [3.0, 3.5]", color=BLACK).scale(0.6).next_to(h_label, RIGHT)
        
        # Content: y [-2.5, 3.0]
        # Height = 3.0 - (-2.5) = 5.5
        c_rect = Rectangle(width=13.0, height=5.5) # slightly narrower for safety
        c_rect.move_to([0, 0.25, 0]) # Center is (3.0 + -2.5)/2 = 0.25
        c_rect.set_fill(BLUE, opacity=0.2)
        c_rect.set_stroke(BLUE, width=4)
        c_label = Text("CONTENT Zone (Main Math)", color=WHITE).scale(1.0).move_to(c_rect)
        c_range = MathTex(r"y \in [-2.5, 3.0]", color=WHITE).scale(0.8).next_to(c_label, DOWN)
        
        # Footer: y [-3.5, -2.5]
        # Height = 1.0
        f_rect = Rectangle(width=14.0, height=1.0)
        f_rect.move_to([0, -3.0, 0]) # Center is (-2.5 + -3.5)/2 = -3.0
        f_rect.set_fill(GREEN, opacity=0.4)
        f_rect.set_stroke(GREEN, width=4)
        f_label = Text("FOOTER Zone (Explanation)", color=BLACK).scale(0.8).move_to(f_rect)
        f_range = MathTex(r"y \in [-3.5, -2.5]", color=BLACK).scale(0.6).next_to(f_label, RIGHT)
        
        # Add everything
        self.add(h_rect, h_label, h_range)
        self.add(c_rect, c_label, c_range)
        self.add(f_rect, f_label, f_range)
        
        # Add Reference Lines / Axes
        axes = Axes(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True, "font_size": 20},
        ).set_opacity(0.3)
        self.add(axes)
        
        self.wait(2)
