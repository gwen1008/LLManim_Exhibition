# Source: 3b1b/_2018/eop/chapter2/permutation_grid.py
# Description: [3b1b translated] 展示一個遞迴生成的排列網格，從內到外逐層擴展，最終形成一個5階排列的視覺化結構。



from manim import *
class PermutationGrid(Scene):
    def text_box(self, str):
        box = Text(str, font_size=24)  # 使用 Text 替代 OldTexText，並調整字體大小
        box.add(SurroundingRectangle(box, stroke_color=GREY_D))
        return box

    def construct(self):
        N = 5
        index_list = []
        perm5_box = VGroup()
        for i in range(1, N + 1):
            index_list.append(i)
            perm4_box = VGroup()
            for j in range(1, N):
                index_list.append(j)
                perm3_box = VGroup()
                for k in range(1, N - 1):
                    index_list.append(k)
                    perm2_box = VGroup()
                    for l in range(1, N - 2):
                        index_list.append(l)
                        index_list.append(1)
                        # 假設 print_permutation 函數已定義，這裡保持原樣
                        perm_box = self.text_box(print_permutation(index_list))
                        if l > 1:
                            perm_box.next_to(perm2_box[-1], DOWN, buff=0)
                        perm2_box.add(perm_box)
                        index_list.pop()
                        index_list.pop()
                    if k > 1:
                        perm2_box.next_to(perm3_box[-1], RIGHT, buff=0.08)
                    perm3_box.add(perm2_box)
                    index_list.pop()
                perm3_box.add(SurroundingRectangle(perm3_box, buff=0.12, stroke_color=GREY_B))
                if j > 1:
                    perm3_box.next_to(perm4_box[-1], DOWN, buff=0)
                perm4_box.add(perm3_box)
                index_list.pop()
            if i > 1:
                perm4_box.next_to(perm5_box[-1], RIGHT, buff=0.16)
            perm5_box.add(perm4_box)
            index_list.pop()

        perm5_box.move_to(ORIGIN)
        self.add(perm5_box)
