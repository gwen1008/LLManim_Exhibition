# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示一個條件機率表達式，其中數值部分以黃色高亮顯示，並將其置於畫面底部。



from manim import *
class ExampleConditional(Scene):
    def construct(self):
        # 假設 get_probability_of_slot_group 是一個返回 Mobject 的函數
        # 由於原始代碼未提供其實現，這裡保留函數調用
        prob = get_probability_of_slot_group(
            [True, True], [True]
        )
        # 將 OldTex 替換為 MathTex
        rhs = MathTex("=", "0.925", ">", "0.8")
        # 將 set_color_by_tex 替換為 set_color
        # 注意：MathTex 的子物件是根據 LaTeX 字符串的部分來索引的
        # 這裡假設 "0.925" 是第二個元素（索引 1）
        rhs[1].set_color(YELLOW)
        rhs.next_to(prob, RIGHT)
        expression = VGroup(prob, rhs)
        expression.set_width(config.frame_width - 1)
        expression.center().to_edge(DOWN)

        self.play(Write(expression))
        self.wait()
