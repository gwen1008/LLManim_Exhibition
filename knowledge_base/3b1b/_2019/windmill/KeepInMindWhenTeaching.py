# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示老師對學生說「我不知道你們知道什麼」，然後學生回應「我們知道」的師生互動場景。



from manim import *
class KeepInMindWhenTeaching(Scene):
    def construct(self):
        # 創建老師和學生角色
        teacher = SVGMobject("teacher.svg")  # 假設有老師的SVG
        students = VGroup(*[SVGMobject(f"student{i}.svg") for i in range(3)])
        
        # 安排位置
        teacher.to_edge(UP)
        students.arrange(RIGHT, buff=1).to_edge(DOWN)
        
        self.add(teacher, students)
        
        # 老師說話
        teacher_bubble = SpeechBubble(
            "I don't know\nwhat you know!",
            direction=DOWN
        )
        teacher_bubble.next_to(teacher, DOWN)
        
        self.play(
            Write(teacher_bubble),
            teacher.animate.change("pleading")  # 假設有表情變化方法
        )
        self.wait(2)
        
        # 學生回應
        student_bubble = SpeechBubble(
            "We know",
            direction=UP
        )
        student_bubble.next_to(students[0], UP)
        
        self.play(
            Write(student_bubble),
            students[0].animate.change("hooray"),
            students[1].animate.change("happy"),
            students[2].animate.change("happy"),
        )
        self.wait(2)
