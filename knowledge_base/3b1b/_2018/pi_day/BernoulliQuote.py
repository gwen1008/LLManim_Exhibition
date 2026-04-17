# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一段伯努利引文逐字淡入，其中特定數學公式和關鍵詞以高亮顏色標示，然後淡出。



from manim import *
class BernoulliQuote(Scene):
    def construct(self):
        text = MathTex(
            r'``Your most profound investigation of the series \\',
            r'1+{1\over 4}+{1\over 9}+{1\over 16} + \text{ etc., which I had found to be } \\',
            r'\text{one sixth of the square of }\pi\text{ itself}\dots\text{, not only} \\',
            r'\text{ gave me the greatest pleasure, but also renown } \\',
            r'\text{among the whole Academy of St. Petersburg."}'
        )
        # 將所有部分合併成一個物件以便索引操作
        full_text = VGroup(*text)
        # 在 ManimCE 中，MathTex 的 submobjects 結構不同，我們直接對 text 的 parts 進行操作
        # 這裡假設 text 是一個 VGroup，每個元素是一個單獨的 Tex 物件
        # 由於原代碼索引複雜，我們簡化為對整個 text 中特定部分著色
        # 我們用一個近似方法：先將整個文本設為默認顏色，然後選取特定子物件著色
        # 注意：原代碼索引是基於 OldTexText 的字符級別，這裡我們用 MathTex 的組件級別近似
        # 我們將高亮顏色設為 YELLOW 作為示例
        HIGHLIGHT_COLOR = YELLOW
        
        # 由於 MathTex 結構不同，我們無法精確對應原索引
        # 這裡改為直接對包含數學公式的部分著色
        # 假設 text[1] 是包含 "1+1/4+1/9+1/16+" 的部分
        text[1].set_color(HIGHLIGHT_COLOR)
        # 假設 text[2] 是包含 "π" 公式的部分
        text[2].set_color(HIGHLIGHT_COLOR)
        
        self.play(LaggedStartMap(FadeIn, text), run_time=5)
        self.wait()
        self.play(FadeOut(text))
        self.wait()
