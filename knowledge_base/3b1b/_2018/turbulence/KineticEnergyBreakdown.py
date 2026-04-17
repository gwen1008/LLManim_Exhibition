# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示動能分解的標題與左右兩欄對比，左欄列出較簡單的物理現象，右欄預留給湍流物理。



from manim import *
class KineticEnergyBreakdown(Scene):
    def construct(self):
        title = Text("Kinetic energy breakdown")
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).set_width(config.frame_width)
        h_line.next_to(title, DOWN)
        v_line = Line(h_line.get_center(), config.frame_height * DOWN / 2)
        lc_title = Text("Simpler physics")
        lc_title.set_color(YELLOW)
        rc_title = Text("Turbulence physics")
        rc_title.set_color(GREEN)
        for word, vect in (lc_title, LEFT), (rc_title, RIGHT):
            word.next_to(h_line, DOWN)
            word.shift(config.frame_width * vect / 4)

        left_items = VGroup(
            Text("- Big moving things"),
            Text("- Heat"),
        )
        left_items.arrange(DOWN, aligned_edge=LEFT)
        left_items.next_to(lc_title, DOWN, buff=MED_LARGE_BUFF)
        left_items.to_edge(LEFT)

        self.play(
            Write(VGroup(
                title, h_line, v_line, lc_title, rc_title
            ))
        )
        self.wait()
        for item in left_items:
            self.play(FadeIn(item))
            self.wait()
