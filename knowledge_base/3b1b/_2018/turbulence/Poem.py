# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一首詩和作者照片的動畫，詩中特定單詞以藍色高亮顯示並逐字出現。



from manim import *
class Poem(Scene):
    def construct(self):
        picture = ImageMobject("Lewis_Richardson")
        picture.set_height(4)
        picture.center().to_edge(LEFT, buff=LARGE_BUFF)

        title = Text("Poem by Lewis F. Richardson")
        title.to_edge(UP)

        poem_text = """
            Big{\\,\\,}whirls have little{\\,\\,}whirls\\\\
            which feed on their velocity,\\\\
            And little{\\,\\,}whirls have lesser{\\,\\,}whirls\\\\
            And so on to viscosity.\\\\
        """
        poem_words = [s for s in poem_text.split(" ") if s]
        poem = Text(*poem_words, alignment="")
        poem.next_to(picture, RIGHT, LARGE_BUFF)

        self.add(picture)
        self.play(FadeIn(title, shift=DOWN))
        self.wait()
        for word in poem:
            if "whirl" in word.get_tex():
                word.set_color(BLUE)
            self.play(Write(word))
            self.wait(0.005 * len(word)**1.5)
