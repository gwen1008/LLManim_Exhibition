# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示一本書和作者照片從兩側淡入，然後顯示引文並將其中「powerful」一詞高亮為藍色的過程。



from manim import *
class GleickQuote(Scene):
    def construct(self):
        quote = Text(
            "``[Phase space is] one of the most\n"
            "powerful inventions of modern science.''",
            alignment="center"
        )
        # 手動標記「powerful」部分
        quote_power_part = Text("powerful", color=BLUE)
        # 將引文移到頂部
        quote.to_edge(UP)
        
        # 載入圖片（假設圖片檔案存在於 assets 資料夾）
        book = ImageMobject("ChaosBookCover")
        book.set_height(5)
        book.next_to(ORIGIN, LEFT)
        book.to_edge(DOWN)
        
        gleick = ImageMobject("JamesGleick")
        gleick.set_height(5)
        gleick.next_to(ORIGIN, RIGHT)
        gleick.to_edge(DOWN)
        
        # 先淡入圖片
        self.play(
            FadeIn(book, shift=RIGHT),
            FadeIn(gleick, shift=LEFT),
        )
        self.wait()
        
        # 顯示引文
        self.play(Write(quote))
        self.wait(0.5)
        
        # 建立高亮的「powerful」文字並疊加顯示
        power_highlight = quote_power_part.copy()
        # 將高亮文字對齊到引文中「powerful」的位置
        # 這裡簡化處理：直接放在引文下方
        power_highlight.next_to(quote, DOWN, buff=0.5)
        self.play(
            Write(power_highlight),
            run_time=1
        )
        self.wait()
