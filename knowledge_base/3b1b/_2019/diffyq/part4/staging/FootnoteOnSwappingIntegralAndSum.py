# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示一段關於數學中無窮級數求和順序交換的注意事項文字。



from manim import *
class FootnoteOnSwappingIntegralAndSum(Scene):
    def construct(self):
        words = Text(
            """
            Typically in math, you have to be more
            careful swapping the order of sums like
            this when infinities are involved. Again,
            such questions are what real analysis
            is built for.
            """,
            alignment="left"
        )

        self.add(words)
        self.wait()
