# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示如何將一個關於質數與螺旋的問題分解成兩個子問題，並用顏色和動畫強調對應關係。



from manim import *
class SeparateIntoTwoQuestions(Scene):
    def construct(self):
        top_q = MathTex(r"\text{Why do}", r"\text{ primes}", r"\text{ cause}", r"\text{ spirals}", r"?")
        top_q.scale(2)
        top_q.to_edge(UP)

        q1 = MathTex(r"\text{Where do the}\\\\", r"\text{spirals}", r"\text{ come from?}")
        q2 = MathTex(r"\text{What happens when}\\\\", r"\text{filtering to}", r"\text{ primes}", r"?")
        for q in [q1, q2]:
            q.scale(1.3)
            q.next_to(top_q, DOWN, buff=LARGE_BUFF)
        q1.to_edge(LEFT)
        q1.set_color(YELLOW)
        q2.to_edge(RIGHT)
        q2.set_color(TEAL)

        v_line = DashedLine(
            top_q.get_bottom() + MED_SMALL_BUFF * DOWN,
            config.frame_height * DOWN / 2,
        )

        self.add(top_q)
        self.wait()

        for q, text in [(q1, r"\text{spirals}"), (q2, r"\text{ primes}")]:
            # 先設置顏色
            top_part = top_q.get_part_by_tex(text)
            q_part = q.get_part_by_tex(text)
            top_part.set_color(q.get_color())
            q_part.set_color(q.get_color())
            
            # 創建動畫
            self.play(
                TransformFromCopy(top_part, q_part),
                LaggedStartMap(
                    FadeIn,
                    VGroup(*[m for m in q if m is not q_part])
                )
            )
        self.wait()
        self.play(Create(v_line))
        self.wait()
