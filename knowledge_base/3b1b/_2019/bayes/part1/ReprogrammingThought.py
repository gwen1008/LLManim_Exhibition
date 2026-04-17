# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示一個大腦圖像、問號、貝葉斯公式和思想泡泡的動畫，用於視覺化貝葉斯推理的思維過程。



from manim import *
class ReprogrammingThought(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        # 大腦SVG
        brain = SVGMobject("brain")
        brain.set_fill(GREY, opacity=1)
        brain.set_sheen(1, UL)
        brain.set_stroke(width=0)

        # 雙向箭頭
        arrow = DoubleArrow(ORIGIN, 3 * RIGHT)

        # 貝葉斯公式（假設 get_bayes_formula 返回一個 MathTex）
        formula = MathTex(r"P(H|D) = \frac{P(D|H) P(H)}{P(D)}")
        # 注意：如果原來的 get_bayes_formula 返回的是 TexMobject/OldTex，這裡用 MathTex 替代

        # 將三個物件水平排列並置中
        group = VGroup(brain, arrow, formula)
        group.arrange(RIGHT)
        group.center()

        # 問號
        q_marks = MathTex("???")
        q_marks.scale(1.5)
        q_marks.next_to(arrow, UP, buff=SMALL_BUFF)

        # Kahneman 和 Tversky 的圖片（假設圖片檔案存在）
        # 注意：ImageMobject 在 ManimCE 中改為 Image
        kahneman = ImageMobject("kahneman")  # 應改為 Image("kahneman.png")
        tversky = ImageMobject("tversky")    # 應改為 Image("tversky.png")
        kt = Group(kahneman, tversky)
        kt.arrange(RIGHT)
        kt.set_height(2)
        kt.to_corner(UR)

        # 大腦輪廓（用於高亮）
        brain_outline = brain.copy()
        brain_outline.set_fill(opacity=0)
        brain_outline.set_stroke(TEAL, 4)

        # 動畫序列
        self.play(FadeIn(brain, shift=RIGHT))
        self.play(
            GrowFromCenter(arrow),
            LaggedStart(*[FadeIn(mark, shift=DOWN) for mark in q_marks], lag_ratio=0.1),
            run_time=1
        )
        self.play(FadeIn(formula, shift=LEFT))
        self.wait()

        kw = {"run_time": 1, "lag_ratio": 0.3}
        self.play(LaggedStart(*[FadeIn(img, shift=DOWN) for img in kt], **kw))
        self.play(LaggedStart(*[FadeOut(img) for img in kt], **kw))
        self.wait()

        self.add(brain)
        self.play(Create(brain_outline), run_time=1.5)
        self.play(FadeOut(brain_outline), run_time=0.5)

        # 思想泡泡
        bubble = ThoughtBubble()
        bubble.next_to(brain, UR, buff=SMALL_BUFF)
        bubble.shift(2 * DOWN)

        # 貝葉斯圖表（假設 BayesDiagram 是一個自定義的 Mobject）
        diagram = BayesDiagram(0.25, 0.8, 0.5)
        diagram.set_height(2.5)
        diagram.move_to(bubble.get_bubble_center())

        group = VGroup(brain, arrow, q_marks, formula)

        self.play(
            DrawBorderThenFill(VGroup(*reversed(bubble.get_family()))),
            group.animate.shift(2 * DOWN),
        )
        self.play(FadeIn(diagram))
        self.wait()
        self.play(
            q_marks.animate.scale(1.5),
            q_marks.animate.space_out_submobjects(1.5),
            q_marks.animate.set_opacity(0),
        )
        self.remove(q_marks)
        self.wait()

        # 移動部分（高亮先驗和似然）
        # 假設 formula[7:12] 對應先驗部分，formula[12:18] 對應似然部分
        prior_outline = formula[7:12].copy()
        prior_outline.set_stroke(YELLOW, 5, background=True)
        like_outline = formula[12:18].copy()
        like_outline.set_stroke(BLUE, 5, background=True)

        self.play(
            FadeIn(prior_outline),
            diagram.animate.set_prior(0.5),  # 假設 diagram 有 set_prior 方法
            run_time=2
        )
        self.play(FadeOut(prior_outline))
        self.play(
            FadeIn(like_outline),
            diagram.animate.set_likelihood(0.2),  # 假設 diagram 有 set_likelihood 方法
            run_time=2,
        )
        self.play(FadeOut(like_outline))
        self.wait()
