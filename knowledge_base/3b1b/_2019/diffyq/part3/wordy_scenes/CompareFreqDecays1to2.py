# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示兩個並排的屏幕，分別顯示不同頻率的衰減餘弦函數公式，並用顏色標記變數和頻率。



from manim import *
class CompareFreqDecays1to2(Scene):
    def __init__(self, freqs=[1, 2], **kwargs):
        super().__init__(**kwargs)
        self.freqs = freqs

    def construct(self):
        background = FullScreenFadeRectangle(
            fill_color=GREY_E,
            fill_opacity=1,
        )

        screens = VGroup(*[
            ScreenRectangle(
                height=4,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=1,
                stroke_color=WHITE,
            )
            for x in range(2)
        ])
        screens.arrange(RIGHT)
        screens.set_width(FRAME_WIDTH - 1)

        formulas = VGroup(*[
            self.get_formula(freq)
            for freq in self.freqs
        ])
        for formula, screen in zip(formulas, screens):
            formula.next_to(screen, UP)

        self.add(background)
        self.add(screens)
        self.add(formulas)
        self.wait()

    def get_formula(self, freq):
        f_str = str(freq)
        return MathTex(
            "\\cos\\left(%s \\cdot {x}\\right)" % f_str,
            "e^{-\\alpha \\cdot %s^2 \\cdot {t}}" % f_str,
            tex_to_color_map={
                "{x}": GREEN,
                "{t}": YELLOW,
                f_str: MAROON_B,
            }
        )
