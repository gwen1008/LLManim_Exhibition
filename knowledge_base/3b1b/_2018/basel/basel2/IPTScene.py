# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示逆畢氏定理的視覺證明，使用三個光源和兩個聚光燈三角形來說明 1/a² + 1/b² = 1/h² 的關係。


from manim import *
import numpy as np

class IPTScene(Scene):
    def __init__(self, max_opacity_ambient=0.2, num_levels=200, **kwargs):
        super().__init__(**kwargs)
        self.max_opacity_ambient = max_opacity_ambient
        self.num_levels = num_levels
        self.a = 8
        self.b = 6
        self.radius = 0.5
        self.origin_point = ORIGIN
    
    def construct(self):
        origin_point = self.origin_point
        
        # Axes
        axes = Axes(
            x_range=[-1, 10.5, 1],
            y_range=[-1, 6.5, 1],
        )
        axes.shift(origin_point)
        
        # Important reference points
        A = axes.c2p(self.a, 0)
        B = axes.c2p(0, self.b)
        C = axes.c2p(0, 0)
        xA, yA = A[0], A[1]
        xB, yB = B[0], B[1]
        xC, yC = C[0], C[1]
        
        # Find the coords of the altitude point H
        prelim_matrix = np.array([
            [yA - yB, xB - xA], 
            [xA - xB, yA - yB]
        ])
        prelim_vector = np.array(
            [xB * yA - xA * yB, xC * (xA - xB) + yC * (yA - yB)]
        )
        H2 = np.linalg.solve(prelim_matrix, prelim_vector)
        H = np.append(H2, 0.)
        
        # Lightsources (simplified as dots since LightSource doesn't exist in CE)
        lsA = Dot(point=A, color=YELLOW, radius=0.1)
        lsB = Dot(point=B, color=YELLOW, radius=0.1)
        lsC = Dot(point=H, color=YELLOW, radius=0.1)
        
        # Lighthouse labels
        A_label = Text("A")
        A_label.next_to(lsA, RIGHT)
        B_label = Text("B")
        B_label.next_to(lsB, LEFT)
        
        # Lines
        line_a = Line(C, A, color=BLUE)
        line_b = Line(C, B, color=RED)
        line_c = Line(A, B)
        line_h = Line(H, C, color=GREEN)
        
        label_a = MathTex("a").set_color(BLUE)
        label_a.next_to(line_a, DOWN, buff=SMALL_BUFF)
        label_b = MathTex("b").set_color(RED)
        label_b.next_to(line_b, LEFT, buff=SMALL_BUFF)
        label_h = MathTex("h").set_color(GREEN)
        label_h.next_to(line_h.get_center(), RIGHT, buff=SMALL_BUFF)
        
        perp_mark = VMobject().set_points_as_corners([
            RIGHT, RIGHT+DOWN, DOWN
        ])
        perp_mark.scale(0.25, about_point=ORIGIN)
        perp_mark.rotate(line_c.get_angle() + TAU/4, about_point=ORIGIN)
        perp_mark.shift(H)
        
        # Mini triangle
        m_hyp_a = Line(H, A)
        m_a = line_a.copy()
        m_hyp_b = Line(H, B)
        m_b = line_b.copy()
        mini_triangle = VGroup(m_a, m_hyp_a, m_b, m_hyp_b)
        mini_triangle.set_stroke(width=5)
        
        mini_triangle.generate_target()
        mini_triangle.target.scale(0.1, about_point=origin_point)
        
        # Screen label
        screen_word = Text("Screen")
        screen_word.next_to(mini_triangle.target, UP+RIGHT, buff=LARGE_BUFF)
        screen_arrow = Arrow(
            screen_word.get_bottom(),
            mini_triangle.target.get_center(),
            color=WHITE,
        )
        
        # IPT Theorem
        theorem = MathTex(
            "{1 \over ", "a^2}", "+", 
            "{1 \over", "b^2}", "=", "{1 \over","h^2}"
        )
        theorem.set_color_by_tex("a", BLUE)
        theorem.set_color_by_tex("b", RED)
        theorem.set_color_by_tex("h", GREEN)
        
        theorem_name = Text("Inverse Pythagorean Theorem")
        theorem_name.to_corner(UP+RIGHT)
        theorem.next_to(theorem_name, DOWN, buff=MED_LARGE_BUFF)
        theorem_box = SurroundingRectangle(theorem, color=WHITE)
        
        # Setup spotlights (simplified as triangles)
        spotlight_a = Polygon(H, A, H, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        spotlight_b = Polygon(H, B, H, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        
        # Add components
        self.add(
            axes,
            line_c,
        )
        self.add(
            lsA, A_label,
            lsB, B_label,
            lsC, line_h,
            theorem, theorem_name, theorem_box,
        )
        
        # Show miniature triangle
        self.play(Create(mini_triangle, lag_ratio=0))
        self.play(
            mini_triangle.animate.move_to(mini_triangle.target.get_center()).scale(0.1),
            run_time=2,
        )
        
        # Show beams of light
        self.play(
            Write(screen_word),
            GrowArrow(screen_arrow),
        )
        self.wait()
        
        self.play(
            FadeIn(spotlight_a),
            FadeIn(spotlight_b),
        )
        self.play(*[FadeOut(mob) for mob in [screen_word, screen_arrow]])
        self.wait()
        
        # Reshape screen
        m_hyps = [m_hyp_a, m_hyp_b]
        for hyp, line in (m_hyp_a, m_a), (m_hyp_b, m_b):
            hyp.save_state()
            hyp.alt_version = line.copy()
            hyp.alt_version.set_color(WHITE)
        
        for x in range(2):
            self.play(*[
                Transform(m, m.alt_version)
                for m in m_hyps
            ])
            self.wait()
            self.play(*[Restore(m) for m in m_hyps])
            self.wait()
        
        # Show spotlight at key points (simplified)
        def show_key_point(spotlight, new_point):
            # Simplified version - just move the spotlight
            self.play(
                spotlight.animate.move_to(new_point),
                run_time=2
            )
            self.wait()
            self.play(
                spotlight.animate.move_to(H),
                run_time=2
            )
            self.wait()
        
        self.play(FadeOut(spotlight_a))
        show_key_point(spotlight_b, A)
        self.play(
            FadeOut(spotlight_b),
            FadeIn(spotlight_a),
        )
        show_key_point(spotlight_a, B)
        self.wait()
