# Source: 3b1b/_2018/eop/chapter1/show_proportion.py
# Description: [3b1b translated] 展示一個概率矩形從初始值動態變化到不同概率值的過程。



from manim import *
class ShowProbAsProportion(Scene):
    def construct(self):
        p0 = 0.3
        p1 = 1
        p2 = 0.18
        p3 = 0.64

        # 注意：ProbabilityRect 和 ChangeProbability 不是 ManimCE 內建類別
        # 假設它們是自定義的 Mobject 和動畫
        # 這裡保持原樣，但實際使用時需要確保這些類別已定義
        prob_mob = ProbabilityRect(p0,
            unit_width=4,
            unit_height=2,
            use_percent=False,
            num_decimal_places=2
        )

        self.add(prob_mob)
        self.wait()
        self.play(
            ChangeProbability(prob_mob, p1,
                run_time=3)
        )
        self.wait(0.5)
        self.play(
            ChangeProbability(prob_mob, p2,
                run_time=3)
        )
        self.wait(0.5)
        self.play(
            ChangeProbability(prob_mob, p3,
                run_time=3)
        )
