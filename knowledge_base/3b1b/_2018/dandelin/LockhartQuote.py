# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一段引言逐字出現，並在特定詞彙出現時淡入對應的圖片，最後所有元素淡出。



from manim import *
class LockhartQuote(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_opacity = 1

    def construct(self):
        mb_string = "Madame\\,\\,Bovary"
        ml_string = "Mona\\,\\,Lisa."
        strings = (mb_string, ml_string)
        quote_text = """
            \\large
            How do people come up with such ingenious arguments?
            It's the same way people come up with %s or %s
            I have no idea how it happens.  I only know that
            when it happens to me, I feel very fortunate.
        """ % strings
        quote_parts = [s for s in quote_text.split(" ") if s]
        quote = Text(
            *quote_parts,
            color=WHITE,
            tex_to_color_map={
                mb_string: BLUE,
                ml_string: YELLOW,
            },
            alignment=""
        )
        quote.set_width(config.frame_width - 2)
        quote.to_edge(UP)

        measurement = ImageMobject("MeasurementCover")
        madame_bovary = ImageMobject("MadameBovary")
        mona_lisa = ImageMobject("MonaLisa")
        pictures = Group(measurement, madame_bovary, mona_lisa)
        for picture in pictures:
            picture.set_height(4)
        pictures.arrange(RIGHT, buff=LARGE_BUFF)
        pictures.to_edge(DOWN)

        measurement.save_state()
        measurement.set_width(config.frame_width)
        measurement.center()
        measurement.set_opacity(0)
        self.play(Restore(measurement))
        self.wait()
        for word in quote:
            anims = [Write(word)]
            for text, picture in zip(strings, pictures[1:]):
                if word is quote.get_part_by_tex(text):
                    anims.append(FadeIn(picture, shift=DOWN, run_time=1))
            self.play(*anims)
            self.wait(0.005 * len(word)**1.5)
        self.wait(2)
        self.play(
            LaggedStart(
                *[FadeOut(word, shift=DOWN) for word in quote],
                lag_ratio=0.2,
                run_time=5,
            ),
            LaggedStart(
                *[FadeOut(pic, shift=DOWN) for pic in pictures],
                run_time=3,
            ),
        )
