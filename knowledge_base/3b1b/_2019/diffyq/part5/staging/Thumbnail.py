# Source: 3b1b/_2019/diffyq/part5/staging.py
# Description: [3b1b translated] 展示歐拉公式 e^(iπ) = -1 的視覺化，包含複數平面、單位圓、向量和公式文字。



from manim import *
class Thumbnail(Scene):
    def construct(self):
        epii = MathTex(
            "e^{ {i} \\pi} = -1",
            tex_to_color_map={
                "{i}": YELLOW,
                "\\pi": BLUE,
                "-1": GREY_A,
            }
        )
        epii.set_width(8)
        epii.to_edge(UP)
        epii.set_stroke(BLACK, 50, background=True)

        words = VGroup(
            Text("in"),
            MathTex(
                "in",
                "3.14", " minutes"
            ),
        )
        words.set_stroke(BLACK, 6, background=True)
        words.set_width(config.frame_width - 2)
        words.arrange(DOWN, buff=LARGE_BUFF)
        words.next_to(epii, DOWN, LARGE_BUFF)
        words[1].set_color_by_tex("3.14", YELLOW)
        words.shift(-words[0].get_center())
        words[0].set_opacity(0)

        unit_size = 2.0
        plane = ComplexPlane()
        plane.scale(unit_size)
        plane.shift(1.0 * DOWN)
        plane.add_coordinates([*range(-3, 4), complex(0, -1), complex(0, 1)])

        circle = Circle(
            radius=unit_size,
            color=YELLOW,
        )
        circle.set_stroke(GREY_B, 3)
        arc = Arc(0, PI, radius=unit_size)
        arc.set_stroke(BLUE, 10)
        circle = VGroup(arc.copy().set_stroke(BLACK, 20, background=True), circle, arc)

        circle.move_to(plane.get_origin())
        p_vect = Arrow(
            plane.n2p(0),
            plane.n2p(1),
            buff=0,
            color=GREY_A,
            stroke_width=0.1
        )
        v_vect = Arrow(
            plane.n2p(1),
            plane.n2p(complex(1, 1)),
            buff=0,
            color=YELLOW,
            stroke_width=0.1
        )
        vects = VGroup(p_vect, v_vect)

        self.add(plane)
        self.add(circle)
        self.add(vects)
        self.add(epii)
        # self.add(words)
