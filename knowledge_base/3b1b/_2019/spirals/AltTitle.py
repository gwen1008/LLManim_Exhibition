# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 在背景圖片上逐字淡入帶有顏色強調的標題文字，展示質數螺旋圖案與詩句的視覺效果。



from manim import *
class AltTitle(Scene):
    def construct(self):
        title_text = """
            How pretty but pointless patterns\\\\
            in polar plots of primes\\\\
            prompt pretty important ponderings\\\\
            on properties of those primes.
        """
        words = [w + " " for w in title_text.split(" ") if w]
        title = Text("".join(words), font_size=36)
        title.set_width(config.frame_width - 1)

        # 設定特定文字區塊的顏色
        # 注意：ManimCE 的 Text 物件索引方式與 OldTexText 不同
        # 這裡我們需要根據文字內容來設定顏色
        # 由於 Text 物件不是由單獨的單詞組成，我們需要手動處理
        # 簡化處理：建立一個新的 Text 物件並手動設定顏色
        full_text = "".join(words)
        title = Text(full_text, font_size=36)
        title.set_width(config.frame_width - 1)
        
        # 設定文字顏色
        # "pretty but pointless" 部分
        pretty_start = full_text.find("pretty")
        pretty_end = full_text.find("patterns") + len("patterns")
        for i in range(pretty_start, pretty_end):
            if i < len(title):
                title[i].set_color(TEAL)
        
        # "polar plots of primes" 部分
        polar_start = full_text.find("polar")
        polar_end = full_text.find("primes", polar_start) + len("primes")
        for i in range(polar_start, polar_end):
            if i < len(title):
                title[i].set_color(YELLOW)
        
        # 設定文字邊框
        title.set_stroke(BLACK, 5, background=True)

        # 載入圖片
        image = ImageMobject("PrimeSpiral")
        image.set_height(config.frame_height)
        
        # 建立半透明矩形
        rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=0.25,
            stroke_width=0
        )

        self.add(image, rect)

        # 逐字淡入
        for char in title:
            self.play(
                FadeIn(
                    char, 
                    run_time=0.05 * len(char.text) if char.text else 0.05,
                    lag_ratio=0.4,
                )
            )
        self.wait()
