# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示數學家 Germinal Pierre Dandelin 的介紹畫面，包含標題、肖像、Google搜尋結果和蒲公英圖片動畫。



from manim import *
class NameDandelin(Scene):
    def __init__(self, camera_config={"background_opacity": 1}, **kwargs):
        super().__init__(camera_config=camera_config, **kwargs)
    
    def construct(self):
        title = Text(
            "Proof by\nGerminal Pierre Dandelin (1822)",
            font_size=36
        )
        title.to_edge(UP)

        portrait = ImageMobject("GerminalDandelin")
        portrait.set_height(5)
        portrait.next_to(title, DOWN)

        google_result = ImageMobject("GoogleDandelin")
        google_result.set_height(4)
        google_result.center()
        google_result.to_corner(DR)

        cmon_google = Text("C'mon Google...", color=RED, font_size=24)
        cmon_google.next_to(google_result, RIGHT)
        cmon_google.next_to(google_result, UP, aligned_edge=RIGHT)

        dandelion = ImageMobject("DandelionSphere", height=1.5)
        dandelion.to_edge(LEFT, buff=LARGE_BUFF)
        dandelion.shift(UP)
        big_dandelion = dandelion.copy().scale(2)
        big_dandelion.next_to(dandelion, DOWN, buff=0)
        dandelions = Group(dandelion, big_dandelion)

        self.add(title[0])
        self.play(FadeIn(portrait, shift=DOWN))
        self.play(Write(title[1]))
        self.wait()
        self.play(FadeIn(google_result, shift=LEFT))
        self.play(Write(cmon_google, run_time=1))
        self.wait()

        self.play(LaggedStart(
            *[FadeIn(d, shift=DOWN) for d in dandelions],
            lag_ratio=0.7,
            run_time=1
        ))
        self.wait()
