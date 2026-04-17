# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示條件機率符號中，條件部分被不同布林值組合替換，強調條件不影響結果的視覺概念。



from manim import *
class ShowIndependenceSymbolically(Scene):
    def construct(self):
        filler_tex = "Filler"
        rhs = MathTex("=", "0.8")
        rhs.set_color_by_tex("0.8", YELLOW)
        rhs.next_to(ORIGIN, RIGHT, LARGE_BUFF)
        lhs = MathTex("P(", filler_tex, "|", filler_tex, ")")
        lhs.next_to(rhs, LEFT)
        VGroup(lhs, rhs).scale(1.5)
        
        # 替換 filler_tex 為 slot_group
        for part in lhs.get_parts_by_tex(filler_tex):
            slot_group = get_slot_group(
                [True, True, True],
                buff=SMALL_BUFF,
                include_qs=False,
            )
            slot_group.replace(part, dim_to_match=0)
            # 在 ManimCE 中，直接替換 submobjects 的方式不同
            # 我們先找到索引，然後用新的物件替換
            idx = lhs.submobjects.index(part)
            lhs.submobjects[idx] = slot_group
        
        # 設置部分內容為透明
        VGroup(*lhs[1].content[:2]).set_opacity(0)
        condition = lhs[3]
        condition.content[2].set_opacity(0)
        
        bool_lists = [
            [False], [True, False], [False, True], [True],
        ]
        arrow = Arrow(UP, DOWN)
        arrow.next_to(condition, UP)
        arrow.set_color(RED)
        words = Text("Doesn't matter")
        words.set_color(RED)
        words.next_to(arrow, UP)

        self.add(rhs, lhs, arrow, words)
        self.wait()
        for bool_list in bool_lists:
            slot_group = get_slot_group(bool_list, SMALL_BUFF, False)
            slot_group.replace(condition)
            slot_group.move_to(condition, DOWN)
            self.play(Transform(condition, slot_group))
            self.wait()

# 需要定義 get_slot_group 函數（從原始代碼推斷）
def get_slot_group(bool_list, buff, include_qs):
    # 這是一個佔位函數，實際實現應根據原始代碼邏輯
    # 創建一個簡單的矩形組來表示布林值
    group = VGroup()
    for val in bool_list:
        if val:
            rect = Square(side_length=0.3, fill_color=BLUE, fill_opacity=1, stroke_width=2)
        else:
            rect = Square(side_length=0.3, fill_color=RED, fill_opacity=1, stroke_width=2)
        group.add(rect)
    group.arrange(RIGHT, buff=buff)
    return group
