# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個 PiCreature 角色輪流面向不同方向，表現出在幾何問題中沉思的狀態。



from manim import *
class ImmersedInGeometryProblems(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature
        randy.center().to_edge(DOWN)

        # 定義八個方向向量（從左上開始順時針）
        directions = [UL, UP, UR, RIGHT, DR, DOWN, DL, LEFT]
        
        for vect in directions:
            self.play(randy.animate.change("pondering", 4 * vect))
            self.wait(2)
