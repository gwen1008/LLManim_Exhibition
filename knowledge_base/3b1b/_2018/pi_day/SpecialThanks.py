# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一個感謝名單的標題和列表，包含標題、分隔線和四個人名。



from manim import *
class SpecialThanks(Scene):
    def construct(self):
        title = Text("Special thanks to:")
        title.to_edge(UP, buff=LARGE_BUFF)
        title.scale(1.5)
        title.set_color(BLUE)
        h_line = Line(LEFT, RIGHT).scale(4)
        h_line.next_to(title, DOWN)
        h_line.set_stroke(WHITE, 1)

        people = VGroup(*list(map(Text, [
            "Ben Hambrecht",
            "University Library Basel",
            "Martin Mattmüller",
            "Library of the Institut de France",
        ])))
        people.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        people.next_to(h_line, DOWN)

        self.add(title, h_line, people)
