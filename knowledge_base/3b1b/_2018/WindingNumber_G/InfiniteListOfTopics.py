# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個包含無限主題列表的矩形框，主題項目從上到下漸入顯示。



from manim import *
class InfiniteListOfTopics(Scene):
    def construct(self):
        rect = Rectangle(width=5, height=7)
        rect.to_edge(RIGHT)
        title = Text("Infinite list\nof topics")  # OldTexText -> Text
        title.next_to(rect.get_top(), DOWN)
        
        # 建立主題列表，OldTexText -> Text，Tex -> MathTex
        lines = VGroup(*[
            Text(words, font_size=24)  # scale(0.5) 改用 font_size
            for words in [
                "Winding number",
                "Laplace transform",
                "Wallis product",
                "Quantum information",
                "Elliptic curve cryptography",
                "Strange attractors",
                "Convolutional neural networks",
                "Fixed points",
            ]
        ] + [MathTex("\\vdots")])  # Tex -> MathTex
        
        lines.arrange(DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        lines.next_to(title, DOWN, buff=MED_LARGE_BUFF)
        lines[-1].next_to(lines[-2], DOWN)

        self.add(rect, title)
        self.play(LaggedStartMap(FadeIn, lines, run_time=5))
        self.wait()
