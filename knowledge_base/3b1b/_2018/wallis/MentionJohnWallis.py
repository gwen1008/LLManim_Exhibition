# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示沃利斯乘積公式、約翰·沃利斯畫像和無限符號的逐步出現動畫。



from manim import *
class MentionJohnWallis(Scene):
    def construct(self):
        product = get_wallis_product(10)
        product.to_edge(UP)

        name = Text("``Wallis product''", color=BLUE)
        name.scale(1.5)
        name.next_to(product, DOWN, buff=MED_LARGE_BUFF)

        # 注意：ImageMobject 在 ManimCE 中改為 Image
        # 需要確保圖片文件 "John_Wallis" 存在於正確路徑
        image = ImageMobject("John_Wallis")
        image.set_height(3)
        image.next_to(name, DOWN)
        image_name = Text("John Wallis")
        image_name.next_to(image, DOWN)

        infinity = MathTex("\\infty")
        infinity.set_height(1.5)
        infinity.next_to(image, RIGHT, buff=MED_LARGE_BUFF)

        self.add(product)
        self.wait()
        self.play(Write(name))
        # GrowFromEdge 在 ManimCE 中沒有直接對應
        # 使用 FadeIn 替代，從上方進入
        self.play(FadeIn(image, shift=UP))
        self.play(Write(image_name))
        self.wait(2)
        self.play(Write(infinity, run_time=3))
        self.wait(2)
