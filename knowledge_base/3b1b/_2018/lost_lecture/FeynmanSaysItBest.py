# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 老師對學生說「費曼說得最好」，同時學生們呈現不同的表情反應。



from manim import *
class FeynmanSaysItBest(Scene):
    def construct(self):
        # 由於 TeacherStudentsScene 在 ManimCE 中不是內建類別，
        # 我們用最接近的方式實現：創建老師和學生角色並模擬對話場景
        # 這裡假設有預先定義的 teacher 和 students 角色
        
        # 創建老師角色
        teacher = Text("老師").scale(0.8).to_edge(UP)
        
        # 創建學生角色
        student1 = Text("學生1").scale(0.6).shift(LEFT*3 + DOWN)
        student2 = Text("學生2").scale(0.6).shift(DOWN)
        student3 = Text("學生3").scale(0.6).shift(RIGHT*3 + DOWN)
        
        # 添加所有角色到場景
        self.add(teacher, student1, student2, student3)
        
        # 老師說的話
        speech = Text("Feynman says\nit best", font_size=36).next_to(teacher, DOWN)
        
        # 學生表情變化（用顏色和文字變化模擬）
        student1_new = Text("學生1\n(歡呼)", color=GREEN, font_size=24).move_to(student1)
        student2_new = Text("學生2\n(開心)", color=YELLOW, font_size=24).move_to(student2)
        student3_new = Text("學生3\n(呃...)", color=RED, font_size=24).move_to(student3)
        
        # 播放動畫
        self.play(
            Write(speech),
            Transform(student1, student1_new),
            Transform(student2, student2_new),
            Transform(student3, student3_new),
            run_time=2
        )
        self.wait(3)
