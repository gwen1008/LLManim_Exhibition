# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示數線上正負數的箭頭表示，並在箭頭上方顯示對應的正負號。



from manim import *
class SignsExplanation(Scene):
    def construct(self):
        num_line = NumberLine()
        largest_num = 10
        num_line.add_numbers(*list(range(-largest_num, largest_num + 1)))
        self.add(num_line)
        self.wait()

        pos_num = 3
        neg_num = -pos_num

        pos_arrow = Arrow(
                num_line.number_to_point(0), 
                num_line.number_to_point(pos_num),
                buff = 0,
                color = BLUE)  # positive_color 替換為 BLUE
        neg_arrow = Arrow(
                num_line.number_to_point(0), 
                num_line.number_to_point(neg_num),
                buff = 0,
                color = RED)   # negative_color 替換為 RED

        plus_sign = MathTex("+", color = BLUE)  # OldTex 改為 MathTex
        minus_sign = MathTex("-", color = RED)  # OldTex 改為 MathTex

        plus_sign.next_to(pos_arrow, UP)
        minus_sign.next_to(neg_arrow, UP)
        
        #num_line.add_numbers(pos_num)
        self.play(Create(pos_arrow), FadeIn(plus_sign))  # ShowCreation 改為 Create

        #num_line.add_numbers(neg_num)
        self.play(Create(neg_arrow), FadeIn(minus_sign))  # ShowCreation 改為 Create
