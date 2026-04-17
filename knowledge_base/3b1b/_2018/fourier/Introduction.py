# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示傅立葉變換的概念，從一個藍色函數圖形轉換成紅色傅立葉變換圖形，並有教師和學生角色互動。


from manim import *
import numpy as np

class Introduction(TeacherStudentsScene):
    def construct(self):
        title = Tex("Fourier Transform")
        title.scale(1.2)
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        func = lambda t: np.cos(2 * TAU * t) + np.cos(3 * TAU * t)
        
        # 創建藍色函數圖形
        graph = FunctionGraph(
            func,
            x_range=[0, 5],
            color=BLUE
        )
        graph.stretch(0.25, 1)
        graph.next_to(title, DOWN)
        graph.to_edge(LEFT)
        
        # 創建紅色傅立葉變換圖形
        # 注意：get_fourier_transform 函數需要自行定義或從原代碼中移植
        fourier_graph = FunctionGraph(
            lambda x: get_fourier_transform(func, 0, 5)(x),  # 假設 get_fourier_transform 已定義
            x_range=[0, 5],
            color=RED
        )
        fourier_graph.move_to(graph)
        fourier_graph.to_edge(RIGHT)
        
        arrow = Arrow(graph.get_right(), fourier_graph.get_left(), color=WHITE)
        
        self.add(title, graph)

        # 學生思考動畫
        self.student_thinks(
            "What's that?",
            look_at=title,
            target_mode="confused",
            student_index=1,
        )
        
        # 播放轉換動畫
        self.play(
            GrowArrow(arrow),
            TransformFromCopy(graph, fourier_graph)
        )
        self.wait(2)
        
        # 另一個學生思考
        self.student_thinks(
            "Pssht, I got this",
            target_mode="tease",
            student_index=2,
            added_anims=[FadeOut(self.students[1].bubble)]
        )
        
        # 教師表情變化
        self.play(self.teacher.animate.change("hesitant"))
        self.wait(2)

# 注意：需要定義 get_fourier_transform 函數或從原代碼移植
def get_fourier_transform(func, t_min, t_max):
    # 這裡是占位符，實際需要實現傅立葉變換計算
    # 原代碼中應該有這個函數的定義
    return lambda x: 0
