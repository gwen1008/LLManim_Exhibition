# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示兩個並排的矩形框，左側介紹 tau (τ) 和 Michael Hartl 的 "Tau manifesto"，右側介紹 Robert Palais 的 "Pi is Wrong!" 並有一個三腳 Pi 生物動畫。



from manim import *
class HartlAndPalais(Scene):
    def construct(self):
        hartl_rect = Rectangle(
            color=WHITE,
            stroke_width=1,
        )
        hartl_rect.set_width(config.frame_width / 2 - 1)
        hartl_rect.to_edge(LEFT)
        palais_rect = hartl_rect.copy()
        palais_rect.to_edge(RIGHT)

        tau_words = MathTex("\\tau", "\\text{``tau''}")
        tau_words.next_to(hartl_rect, UP)

        hartl_words = Tex("Michael Hartl's \\\\ ``Tau manifesto''")
        hartl_words.next_to(hartl_rect, DOWN)

        palais_words = Tex("Robert Palais' \\\\ ``Pi is Wrong!''")
        palais_words.next_to(palais_rect, DOWN)

        for words in [hartl_words, palais_words]:
            words.scale(0.7, about_edge=UP)

        # 注意：ManimCE 沒有內建的 ThreeLeggedPiCreature
        # 這裡用一個簡單的圓形替代，保持動畫結構
        three_legged_creature = Circle(
            radius=0.75,
            color=BLUE,
            fill_opacity=0.5
        )
        three_legged_creature.next_to(palais_rect, UP)

        self.add(hartl_words)
        self.play(Write(tau_words))
        self.wait()
        self.play(FadeIn(palais_words))
        self.play(FadeIn(three_legged_creature))
        # 模擬 change_mode 動畫
        self.play(three_legged_creature.animate.scale(1.2))
        self.play(three_legged_creature.animate.scale(1/1.2))
        # 模擬眨眼動畫
        self.play(three_legged_creature.animate.set_opacity(0.3))
        self.play(three_legged_creature.animate.set_opacity(0.5))
        # Homotopy 動畫
        def homotopy_func(x, y, z, t):
            new_x = x + 0.1 * np.sin(2 * TAU * t) * np.exp(-10 * (t - 0.5 - 0.5 * (y - 1.85))**2)
            return np.array([new_x, y, z])
        
        self.play(Homotopy(homotopy_func, three_legged_creature, run_time=2))
        self.wait()
