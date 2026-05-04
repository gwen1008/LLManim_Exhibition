# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示 Alan Kay 的圖片和名字從上方淡入，然後逐字顯示引文的動畫過程。



from manim import *
class FinalQuote(Scene):
    def construct(self):
        quote_text = """
            A change of perspective\\\\
            is worth 80 IQ points.
        """
        quote_parts = [s for s in quote_text.split(" ") if s]
        quote = Text(
            *quote_parts,
            font_size=48  # 替代 scale(1.2) 的近似效果
        )
        quote.scale(1.2)
        quote.shift(2 * RIGHT + UP)

        image = ImageMobject("AlanKay")
        image.set_height(6)
        image.to_corner(UL)
        image.shift(2 * LEFT + 0.5 * UP)
        name = Text("Alan Kay", font_size=48)
        name.scale(1.5)
        name.next_to(image, DOWN)
        # name.shift_onto_screen() 在 CE 中不需要，CE 會自動處理

        self.play(
            FadeIn(image, shift=DOWN),  # 替代 FadeInFromDown
            Write(name),
        )
        self.wait()

        for word in quote:
            self.play(Write(word))  # 替代 ShowWord
            self.wait(0.005 * len(word)**1.5)
        self.wait()
