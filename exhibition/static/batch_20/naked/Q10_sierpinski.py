from manim import *

class GeneratedScene(Scene):
    def construct(self):
        title = Text("Sierpinski Triangle", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Initial big triangle vertices
        size = 5.5
        A = np.array([-size/2, -size*np.sqrt(3)/6, 0])
        B = np.array([size/2, -size*np.sqrt(3)/6, 0])
        C = np.array([0, size*np.sqrt(3)/3, 0])

        def make_triangle(p1, p2, p3, color=BLUE, opacity=0.7):
            t = Polygon(p1, p2, p3, color=color, fill_color=color, fill_opacity=opacity, stroke_width=1.5)
            return t

        triangles = [(A, B, C)]
        tri_group = VGroup(make_triangle(A, B, C))
        self.play(Create(tri_group), run_time=1.5)

        iter_label = Text("Iteration: 0", font_size=28).to_edge(DOWN)
        self.play(FadeIn(iter_label))

        colors = [BLUE, TEAL, GREEN, YELLOW, ORANGE]

        for i in range(1, 5):
            new_triangles = []
            new_group = VGroup()
            removed_group = VGroup()
            for (p1, p2, p3) in triangles:
                m12 = (p1 + p2) / 2
                m23 = (p2 + p3) / 2
                m31 = (p3 + p1) / 2
                # three corner triangles kept
                new_triangles.append((p1, m12, m31))
                new_triangles.append((m12, p2, m23))
                new_triangles.append((m31, m23, p3))
                new_group.add(make_triangle(p1, m12, m31, color=colors[i]))
                new_group.add(make_triangle(m12, p2, m23, color=colors[i]))
                new_group.add(make_triangle(m31, m23, p3, color=colors[i]))
                # middle removed
                removed_group.add(make_triangle(m12, m23, m31, color=RED, opacity=0.5))

            new_label = Text(f"Iteration: {i}", font_size=28).to_edge(DOWN)
            self.play(FadeIn(removed_group), run_time=0.8)
            self.play(FadeOut(removed_group), FadeOut(tri_group), FadeIn(new_group),
                      Transform(iter_label, new_label), run_time=1.2)
            tri_group = new_group
            triangles = new_triangles

        self.wait(2)