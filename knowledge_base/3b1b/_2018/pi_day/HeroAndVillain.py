# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示兩張歐拉畫像對比，左邊使用 tau (6.2831...)，右邊使用 pi (3.1415...)，右邊畫像從像素化逐漸清晰顯示。



from manim import *
class HeroAndVillain(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_opacity = 1
    
    def construct(self):
        # 載入圖片（假設 get_image 函數已定義或圖片已預先載入）
        # 這裡使用替代方案：用 Rectangle 模擬圖片
        good_euler = Rectangle(height=5, width=3.5, color=BLUE, fill_opacity=0.8)
        bad_euler_pixelated = Rectangle(height=5, width=3.5, color=RED, fill_opacity=0.5)
        bad_euler = Rectangle(height=5, width=3.5, color=RED, fill_opacity=0.8)
        
        # 設定位置
        good_euler.move_to(LEFT * 3.5)
        bad_euler.move_to(RIGHT * 3.5)
        bad_euler_pixelated.move_to(bad_euler)
        
        # 標籤文字
        good_euler_label = Text("Leonhard Euler")
        good_euler_label.next_to(good_euler, DOWN)
        tau_words = Text("Used 6.2831...")
        tau_words.next_to(good_euler, UP)
        tau_words.set_color(GREEN)
        
        bad_euler_label = Text("Also Euler...")
        bad_euler_label.next_to(bad_euler, DOWN)
        pi_words = Text("Used 3.1415...")
        pi_words.set_color(RED)
        pi_words.next_to(bad_euler, UP)
        
        # 動畫序列
        self.play(
            FadeIn(good_euler, shift=DOWN),
            Write(good_euler_label)
        )
        self.play(LaggedStart(*[FadeIn(word) for word in tau_words]))
        self.wait()
        self.play(FadeIn(bad_euler_pixelated, shift=DOWN))
        self.play(LaggedStart(*[FadeIn(word) for word in pi_words]))
        self.wait(2)
        self.play(
            FadeIn(bad_euler),
            Write(bad_euler_label),
        )
        self.remove(bad_euler_pixelated)
        self.wait(2)
