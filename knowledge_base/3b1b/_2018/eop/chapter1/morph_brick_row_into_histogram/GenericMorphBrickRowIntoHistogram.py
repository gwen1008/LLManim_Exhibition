# Source: 3b1b/_2018/eop/chapter1/morph_brick_row_into_histogram.py
# Description: [3b1b translated] 將一排磚塊轉換成直方圖，展示磚塊旋轉、移動並形成帶輪廓的長條圖的過程。



from manim import *
class GenericMorphBrickRowIntoHistogram(Scene):
    def __init__(
        self,
        level=3,
        bar_width=2.0,
        bar_anchor_height=-3.0,
        show_tallies=False,
        show_nb_flips=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.level = level
        self.bar_width = bar_width
        self.bar_anchor_height = bar_anchor_height
        self.show_tallies = show_tallies
        self.show_nb_flips = show_nb_flips

    def construct(self):
        # 創建磚塊行
        self.row = BrickRow(self.level, height=self.bar_width, width=10)
        # 創建可輪廓化的長條
        self.bars = OutlineableBars(*[self.row.rects[i] for i in range(self.level + 1)])
        # 計算長條錨點位置
        self.bar_anchors = [
            self.bar_anchor_height * UP + self.row.height * (i - 0.5 * self.level) * RIGHT
            for i in range(self.level + 1)
        ]

        self.add(self.row)

        tallies = None
        if self.show_tallies:
            tallies = VGroup()
            for i, brick in enumerate(self.row.rects):
                tally = TallyStack(self.level - i, i)
                tally.move_to(brick)
                self.add(tally)
                tallies.add(tally)
                brick.set_stroke(width=3)

        if self.show_nb_flips:
            nb_flips_text = MathTex(r"\# \text{ of flips: }" + str(self.level))
            nb_flips_text.to_corner(UR)
            self.add(nb_flips_text)

        # 移除細分和邊框
        self.remove(self.row.subdivs, self.row.border)

        for rect in self.row.rects:
            rect.set_stroke(color=WHITE, width=3)

        self.wait()
        
        # 磚塊間隔開
        self.play(
            self.row.rects.animate.space_out_submobjects(factor=1.3),
            FadeOut(tallies) if tallies else AnimationGroup()
        )
        self.wait()
        
        # 旋轉磚塊
        anims = []
        for brick in self.row.rects:
            anims.append(brick.animate.rotate(TAU/4))
        self.play(*anims)
        self.wait()

        # 移動磚塊到錨點位置
        anims = []
        for i, brick in enumerate(self.row.rects):
            anims.append(brick.animate.next_to(self.bar_anchors[i], UP, buff=0))
        self.play(*anims)
        self.wait()

        # 創建長條輪廓
        self.bars.create_outline()
        anims = [
            rect.animate.set_stroke(width=0)
            for rect in self.bars
        ]
        anims.append(FadeIn(self.bars.outline))
        self.play(*anims)

        self.wait()
