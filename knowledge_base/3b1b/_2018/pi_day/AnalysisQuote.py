# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示分析頁面圖片與圓周率定義的文字和公式，並動態繪製圓形來視覺化半圓周與半徑的關係。



from manim import *
class AnalysisQuote(Scene):
    def construct(self):
        # 載入圖片並調整大小位置
        analysis = ImageMobject("Analysis_page_showing_pi")
        analysis.set_height(config.frame_height)
        analysis.to_edge(LEFT, buff=0)

        # 文字內容（使用 MathTex 處理 LaTeX）
        text = MathTex(
            "\\dots \\text{set the radius of}",
            "\\text{the circle}\\dots \\text{to be} = 1, \\dots \\\\",
            "\\text{through approximations the}",
            "\\text{semicircumference} \\\\", 
            "\\text{of said circle}",
            "\\text{has been found to be}", 
            "= 3.14159\\dots,\\\\",
            "\\text{for which number, for the sake of}",
            "\\text{brevity,} \\\\ \\text{I will write}", 
            "\\pi\\dots",
            alignment=""
        )
        
        # 圓周率公式
        pi_formula = MathTex(
            "\\pi", "=", "{ \\text{semicircumference}", "\\over", "\\text{radius}}"
        )
        
        # 設定文字寬度與位置
        text.set_width(config.frame_width / 2)
        text.next_to(analysis, RIGHT, buff=LARGE_BUFF)
        text.to_edge(UP)

        HIGHLIGHT_COLOR = GREEN
        # 設定關鍵詞顏色
        for mob in [text, pi_formula]:
            mob.set_color_by_tex_to_color_map({
                "semicircumference": HIGHLIGHT_COLOR,
                "3.14159": HIGHLIGHT_COLOR,
                "\\pi": HIGHLIGHT_COLOR
            })

        # 取得繪製圓形的元件（自定義函數需另外定義）
        terms, generate_anims1, generate_anims2 = get_circle_drawing_terms(
            radius=1,
            positioning_func=lambda circ: circ.next_to(text, DOWN, LARGE_BUFF)
        )
        terms[0].set_color(HIGHLIGHT_COLOR)
        terms[-1].set_color(HIGHLIGHT_COLOR)

        # 設定公式位置
        pi_formula.next_to(terms, DOWN, buff=0)
        pi_formula.align_to(text, RIGHT)
        pi_formula[0].scale(2, about_edge=RIGHT)

        # 動畫序列
        self.add(analysis)
        self.play(*generate_anims2(), rate_func=lambda t: 0.5 * smooth(t))
        self.play(LaggedStart(*[FadeIn(word) for word in text]), run_time=5)
        self.play(FadeIn(pi_formula))
        self.wait()
