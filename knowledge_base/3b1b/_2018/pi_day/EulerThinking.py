# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示歐拉畫像旁出現思考泡泡，先顯示π與τ的選擇問題，再轉換為無窮級數求和問題。



from manim import *
class EulerThinking(Scene):
    def construct(self):
        # 載入歐拉畫像
        image = ImageMobject("Leonhard_Euler_by_Handmann")
        image.set_height(4)
        image.to_edge(DOWN)
        image.shift(4*LEFT)
        
        # 思考泡泡
        bubble = ThoughtBubble(height=4.5)
        bubble.next_to(image, RIGHT)
        bubble.to_edge(UP, buff=SMALL_BUFF)
        bubble.shift(0.8*LEFT)
        bubble.set_fill(BLACK, 0.3)
        
        # π vs τ 文字
        pi_vs_tau = MathTex(
            "\\text{Should }\\pi\\text{ represent }\\\\", 
            "3.1415...",
            "\\text{ or }", 
            "6.2831...", 
            "\\text{?}"
        )
        # 設定顏色
        pi_vs_tau[1].set_color(GREEN)
        pi_vs_tau[3].set_color(RED)
        pi_vs_tau.move_to(bubble.get_bubble_center())
        
        # 數學問題
        question = MathTex(
            "\\frac{1}{1} + \\frac{1}{4} + \\frac{1}{9} + \\frac{1}{16} + \\cdots = ",
            "\\;???"
        )
        question[0].set_color_by_gradient(BLUE_C, BLUE_B)
        question.move_to(bubble.get_bubble_center())
        question.shift(2*SMALL_BUFF*UP)
        
        # 叉叉
        cross = Cross(pi_vs_tau)
        cross.set_stroke(RED, 8)
        
        # 動畫
        self.add(image)
        self.play(
            Create(bubble),
            Write(pi_vs_tau)
        )
        self.play(Create(cross))
        self.wait()
        self.play(
            FadeOut(VGroup(pi_vs_tau, cross)),
            FadeIn(question),
        )
        self.wait()
