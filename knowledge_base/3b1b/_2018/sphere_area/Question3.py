# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個數學問題的標題和方程式，並用括號和文字標註方程式的特定部分。



from manim import *
class Question3(Scene):
    def construct(self):
        question = Text("Question #3:")
        question.to_edge(LEFT)
        equation = MathTex(
            r"\text{(Shadow area)}", "=", r"\frac{1}{2}",
            r"\text{(Area of one of the rings)}"
        )
        # 注意：MathTex 中的文字需要用 \text{} 包裹
        # 設定顏色需要根據新的索引結構
        equation[0][1:-1].set_color(YELLOW)  # "Shadow area" 部分
        equation[3][1:-1].set_color(PINK)    # "Area of one of the rings" 部分
        equation.next_to(question, RIGHT)
        
        which_one = Text("Which one?")
        # which_one.set_color(YELLOW)  # 原代碼註解掉了
        
        brace = Brace(equation[-1], DOWN, buff=SMALL_BUFF)
        which_one.next_to(brace, DOWN, SMALL_BUFF)

        self.add(question)
        self.play(FadeIn(equation))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(which_one)
        )
        self.wait()
