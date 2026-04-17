# Source: 3b1b/_2018/eop/chapter1/various_intro_visuals.py
# Description: [3b1b translated] 展示一個包含兩個骰子所有可能組合的表格，並將其置中於畫面。



from manim import *
class TwoDiceTableScene(Scene):
    def construct(self):
        # 假設 TwoDiceTable 是一個自定義的 Mobject，用於繪製兩個骰子的組合表格
        # 由於原始代碼未提供 TwoDiceTable 的定義，我們假設它是一個可用的類
        # 並保持其初始化參數不變
        table = TwoDiceTable(cell_size=1)
        table.move_to(ORIGIN)  # 將表格置中，相當於 .center()
        self.add(table)
