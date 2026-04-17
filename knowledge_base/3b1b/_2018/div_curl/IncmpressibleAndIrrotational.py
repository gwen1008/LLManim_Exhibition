# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示不可壓縮與無旋向量場的數學定義，並用動畫將散度與旋度公式與其物理意義配對，最後提出疑問。



from manim import *
class IncmpressibleAndIrrotational(Scene):
    def construct(self):
        div_0 = MathTex(r"\text{div }\mathbf{F} = 0")
        curl_0 = MathTex(r"\text{curl }\mathbf{F} = 0")
        incompressible = Text("Incompressible")
        irrotational = Text("Irrotational")

        for text in [div_0, curl_0, incompressible, irrotational]:
            self.stylize_word_for_background(text)

        div_0.to_edge(UP)
        curl_0.next_to(div_0, DOWN, buff=MED_LARGE_BUFF)

        # 為 div_0 和 curl_0 創建移動目標
        div_0.generate_target()
        curl_0.generate_target()

        # 為每個運算符和對應的單詞創建分組並排列
        div_group = VGroup(div_0.target, incompressible)
        div_group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        div_group.move_to(div_0)

        curl_group = VGroup(curl_0.target, irrotational)
        curl_group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        curl_group.move_to(curl_0)

        self.play(FadeIn(div_0, shift=DOWN))
        self.play(FadeIn(curl_0, shift=DOWN))
        self.wait()
        self.play(
            MoveToTarget(div_0),
            FadeIn(incompressible, shift=DOWN),
        )
        self.wait()
        self.play(
            MoveToTarget(curl_0),
            FadeIn(irrotational, shift=DOWN),
        )
        self.wait()

        rect = SurroundingRectangle(VGroup(curl_0, irrotational))
        question = Text("Does this actually happen?")
        question.next_to(rect, DOWN)
        question.set_color(rect.get_color())
        self.stylize_word_for_background(question)

        self.play(Create(rect))
        self.play(Write(question))
        self.wait()

    def stylize_word_for_background(self, mobject):
        mobject.add_background_rectangle()
