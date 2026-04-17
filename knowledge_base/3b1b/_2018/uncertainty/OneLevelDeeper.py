# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示海森堡不確定性原理與波函數詮釋之間的關聯，並用隨機性雲狀物體動態過渡。



from manim import *
class OneLevelDeeper(Scene):
    def construct(self):
        heisenberg = ImageMobject("Heisenberg")
        heisenberg.to_corner(UP + LEFT)
        self.add(heisenberg)

        hup_words = Text("Heisenberg's uncertainty principle")
        wave_words = Text("Interpretation of the wave function")
        arrow = Arrow(start=DOWN, end=UP)
        group = VGroup(hup_words, arrow, wave_words)
        group.arrange(DOWN)

        randomness = ProbabalisticMobjectCloud(
            Text("Randomness"),
            n_copies=5,
            time_per_change=0.05
        )
        gdw = randomness.gaussian_distribution_wrapper
        gdw.rotate(TAU / 4)
        gdw.set_height(1)
        # gdw.set_width(4)
        gdw.next_to(hup_words, UP, buff=MED_LARGE_BUFF)

        self.add(hup_words, randomness)
        self.wait(4)
        self.play(
            FadeIn(wave_words),
            Create(arrow),
            gdw.animate.next_to(wave_words, DOWN, buff=MED_LARGE_BUFF).rotate(
                TAU / 2
            )
        )
        self.wait(6)
