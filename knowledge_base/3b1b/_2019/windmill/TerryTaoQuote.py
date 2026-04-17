# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示陶哲軒的圖片和名字，然後淡入引文並高亮其中的故事部分。



from manim import *
class TerryTaoQuote(Scene):
    def construct(self):
        image = ImageMobject("TerryTao")
        image.set_height(4)
        name = Text("Terence Tao")
        name.scale(1.5)
        name.next_to(image, DOWN, buff=0.2)
        tao = Group(image, name)
        tao.to_corner(DL, buff=MED_SMALL_BUFF)

        tiny_tao = ImageMobject("TerryTaoIMO")
        tiny_tao.match_height(image)
        tiny_tao.next_to(image, RIGHT, LARGE_BUFF)

        quote = self.get_quote()

        self.play(
            FadeIn(image, shift=DOWN),
            Write(name),
        )
        self.wait()
        self.play(
            FadeIn(tiny_tao, shift=LEFT)
        )
        self.wait()
        self.play(FadeOut(tiny_tao))

        #
        self.play(
            FadeIn(
                quote,
                lag_ratio=0.05,
                run_time=5,
                rate_func=bezier([0, 0, 1, 1])
            )
        )
        self.wait()
        story_line = Line()
        story_line.match_width(quote.story_part)
        story_line.next_to(quote.story_part, DOWN, buff=0)
        story_line.set_color(TEAL)
        self.play(
            quote.story_part.animate.set_color(TEAL),
            Create(story_line),
            lag_ratio=0.2,
        )
        self.wait()

    def get_quote(self):
        story_words = "fables, stories, and anecdotes"
        quote = Tex(
            r"""
            \Large
            ``Mathematical problems, or puzzles, are important to real mathematics
            (like solving real-life problems), just as fables, stories, and anecdotes
            are important to the young in understanding real life.''\\
            """,
            alignment="",
            isolate=[story_words]
        )
        quote.story_part = quote.get_part_by_tex(story_words)
        quote.set_width(config.frame_width - 2.5)
        quote.to_edge(UP)

        return quote
