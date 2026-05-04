# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示一個包含二項式係數符號和堆疊排列的縮圖場景。



from manim import *
class Thumbnail(Scene):
    def construct(self):
        n_choose_k = MathTex("n \\choose k")
        n_choose_k[1].set_color(YELLOW)
        n_choose_k[2].set_color(YELLOW)
        n_choose_k.scale(2)
        n_choose_k.to_edge(UP)
        
        # 假設 get_stacks 是一個自定義函數，這裡保留其調用
        # 注意：由於原代碼未提供 get_stacks 的實現，我們假設它返回一個 VGroup
        stacks = get_stacks(
            MathTex("1").set_color(PINK),
            MathTex("0").set_color(BLUE),
            n=5, vertical_buff=SMALL_BUFF,
        )
        stacks.to_edge(DOWN)
        stacks.shift(MED_SMALL_BUFF * LEFT)

        self.add(n_choose_k, stacks)
