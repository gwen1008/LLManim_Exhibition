# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示三個亮度指示器從左到右依序出現，並顯示對應的亮度讀數（1、1/4、1/9）。



from manim import *
class IndicatorScalingScene(Scene):
    def construct(self):
        unit_intensity = 0.6

        # 假設 LightIndicator 是自定義的 Mobject，保留原邏輯
        indicator1 = LightIndicator(show_reading=False, color=LIGHT_COLOR)
        indicator1.set_intensity(unit_intensity)
        reading1 = MathTex("1")
        reading1.move_to(indicator1)

        indicator2 = LightIndicator(show_reading=False, color=LIGHT_COLOR)
        indicator2.shift(2 * RIGHT)
        indicator2.set_intensity(unit_intensity / 4)
        reading2 = MathTex("{1\\over 4}").scale(0.8)
        reading2.move_to(indicator2)

        indicator3 = LightIndicator(show_reading=False, color=LIGHT_COLOR)
        indicator3.shift(4 * RIGHT)
        indicator3.set_intensity(unit_intensity / 9)
        reading3 = MathTex("{1\\over 9}").scale(0.8)
        reading3.move_to(indicator3)

        self.play(FadeIn(indicator1))
        self.play(FadeIn(reading1))
        self.wait()
        self.play(FadeOut(reading1))
        self.play(Transform(indicator1, indicator2))
        self.play(FadeIn(reading2))
        self.wait()
        self.play(FadeOut(reading2))
        self.play(Transform(indicator1, indicator3))
        self.play(FadeIn(reading3))
        self.wait()
