# Source: 3b1b/_2018/eop/chapter1/various_intro_visuals.py
# Description: [3b1b translated] 展示三組二元選擇（硬幣正反面、男女符號、勾叉符號）從上到下依次淡入的視覺效果。



from manim import *
class BinaryChoices(Scene):
    def construct(self):
        # 假設這些是自定義的 Mobject 類別，保留原名稱
        example1 = BinaryOption(UprightHeads(), UprightTails())
        example2 = BinaryOption(Male(), Female())
        example3 = BinaryOption(Checkmark(), Xmark())

        example2.next_to(example1, DOWN, buff=MED_LARGE_BUFF)
        example3.next_to(example2, DOWN, buff=MED_LARGE_BUFF)

        all_group = VGroup(example1, example2, example3)
        all_group.scale(2)

        self.play(
            LaggedStartMap(FadeIn, all_group)
        )
