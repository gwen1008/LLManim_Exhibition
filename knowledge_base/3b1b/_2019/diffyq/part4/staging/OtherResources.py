# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示兩個影片縮圖與標題從中心生長並淡入，然後重新排列並加入網址的過程。



from manim import *
class OtherResources(Scene):
    def construct(self):
        thumbnails = Group(
            ImageMobject("MathologerFourier"),
            ImageMobject("CodingTrainFourier"),
        )
        names = VGroup(
            Text("Mathologer"),
            Text("The Coding Train"),
        )

        for thumbnail, name in zip(thumbnails, names):
            thumbnail.set_height(3)

        thumbnails.arrange(RIGHT, buff=LARGE_BUFF)
        thumbnails.set_width(config.frame_width - 1)

        for thumbnail, name in zip(thumbnails, names):
            name.scale(1.5)
            name.next_to(thumbnail, UP)
            thumbnail.add(name)
            self.play(
                FadeIn(name, shift=DOWN),
                GrowFromCenter(thumbnail)
            )
            self.wait()

        url = Text("www.jezzamon.com")
        url.scale(1.5)
        url.move_to(config.frame_width * RIGHT / 5)
        url.to_edge(UP)
        self.play(
            thumbnails.animate.arrange(DOWN, buff=LARGE_BUFF),
            thumbnails.animate.set_height(config.frame_height - 2),
            thumbnails.animate.to_edge(LEFT)
        )
        self.play(FadeIn(url, shift=DOWN))
        self.wait()
