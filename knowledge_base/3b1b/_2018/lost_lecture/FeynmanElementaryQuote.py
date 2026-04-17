# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示費曼引言逐字出現，並用紅色「nothing」替換「very」，最後展示兩個被劃叉的縮圖圖像。



from manim import *
class FeynmanElementaryQuote(Scene):
    def construct(self):
        quote_text = """
            \\large
            I am going to give what I will call an
            \\emph{elementary} demonstration.  But elementary
            does not mean easy to understand.  Elementary
            means that very little is required
            to know ahead of time in order to understand it,
            except to have an infinite amount of intelligence.
        """
        quote_parts = [s for s in quote_text.split(" ") if s]
        quote = Text(
            *quote_parts,
            color=WHITE,
            t2c={
                "\\emph{elementary}": BLUE,
                "elementary": BLUE,
                "Elementary": BLUE,
                "infinite": YELLOW,
                "amount": YELLOW,
                "of": YELLOW,
                "intelligence": YELLOW,
                "very": RED,
                "little": RED,
            },
            alignment="left"
        )
        quote[-1].shift(2 * 0.1 * LEFT)  # SMALL_BUFF 約為 0.1
        quote.set_width(config.frame_width - 1)
        quote.to_edge(UP)
        # 找到 "of" 部分並設為白色
        for part in quote:
            if part.get_tex_string() == "of":
                part.set_color(WHITE)

        nothing = Text("nothing", color=RED)
        nothing.scale(0.9)
        very = None
        for part in quote:
            if part.get_tex_string() == "very":
                very = part
                break
        if very:
            nothing.shift(very.get_left() - nothing.get_left())

        for word in quote:
            if word is very:
                self.add(nothing)
                # 自定義 ShowWord 動畫，用 Write 替代
                self.play(Write(nothing))
                self.wait(0.2)
                # 排序點以實現特定消失效果，用 FadeOut 替代
                self.play(FadeOut(nothing, run_time=1))
            # 創建背景文字輪廓
            back_word = word.copy().set_stroke(BLACK, 5)
            self.add(back_word, word)
            # 用 Write 動畫顯示文字
            self.play(
                Write(back_word),
                Write(word),
            )
            self.wait(0.005 * len(word)**1.5)
        self.wait()

        # 顯示縮圖
        # 注意：ImageMobject 在 CE 中為 Image，但需要指定檔案路徑
        # 這裡假設圖片檔案存在於 assets 目錄中
        images = Group(
            ImageMobject("Calculus_Thumbnail"),
            ImageMobject("Fourier_Thumbnail"),
        )
        for image in images:
            image.set_height(3)
        images.arrange(RIGHT, buff=LARGE_BUFF)
        images.to_edge(DOWN, buff=LARGE_BUFF)
        images[1].move_to(images[0])
        crosses = VGroup(*[Cross(image) for image in images])
        crosses.set_stroke(RED, 10)

        for image, cross in zip(images, crosses):
            image.rect = SurroundingRectangle(
                image,
                stroke_width=3,
                stroke_color=WHITE,
                buff=0
            )
            cross.scale(1.1)
        self.play(
            FadeIn(images[0], shift=DOWN),
            FadeIn(images[0].rect, shift=DOWN)
        )
        self.play(Create(crosses[0]))
        self.wait()
        self.play(
            FadeOut(images[0], shift=DOWN),
            FadeOut(images[0].rect, shift=DOWN),
            FadeOut(crosses[0], shift=DOWN),
            FadeIn(images[1], shift=DOWN),
            FadeIn(images[1].rect, shift=DOWN),
        )
        self.play(Create(crosses[1]))
        self.wait()
