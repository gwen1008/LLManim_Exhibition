from manim import *

class TelescopingProductFractions(Scene):
    """
    Fraction multiplication division 分數乘除: Visualizes the "telescoping cancellation" animation technique for chained fraction multiplication.

    動畫手法範本：相鄰約分（telescoping cancellation）
    ----------
    適用場景：
    - 分子分母相互抵消的連乘式，例如 a/b × b/c × c/d × ...
    - 通用展開規律（如 (1 - 1/k) 形式可化簡為 (k-1)/k 後做相鄰約分）
    - 任何「上下相鄰項可消去」的乘法鏈

    視覺要點：
    1. 顏色標記要約分的分子分母（成對配色）
    2. 用 FadeOut + Indicate 演出「消去」效果
    3. 保留鏈條兩端的項，化成最終答案
    4. 用 "..." 表達中段重複性，避免畫面擁擠

    注意：此範本僅展示動畫手法，使用者需自行計算具體題目的數值化簡。
    """
    def get_glow_rect(self, mobject, color="#3A86FF", buff=0.15):

        return RoundedRectangle(

            corner_radius=0.15,

            color=color,

            stroke_width=3,

            fill_color=color,

            fill_opacity=0.15

        ).surround(mobject, buff=buff)


    def construct(self):

        # 🌌 Set sleek deep-dark slate background

        self.camera.background_color = "#0B0F19"


        # 📐 Add modern thin background coordinate grid

        grid = NumberPlane(

            x_range=[-7, 7, 1], y_range=[-4, 4, 1],

            background_line_style={"stroke_color": "#1E293B", "stroke_opacity": 0.4, "stroke_width": 1}

        )

        self.add(grid)

        # Title - 標題只描述「手法」，不洩漏任何具體題目
        title = Text("Telescoping Cancellation Pattern", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Step 1: 展示一般化的鏈式乘積形式（用抽象變數 a, b, c, d, e）
        step1_label = Text("Step 1: Recognize the chain pattern", font_size=28).next_to(title, DOWN, buff=0.4)
        self.play(Write(step1_label))

        # 用抽象變數展示「相鄰項共享一個值」的模式
        frac_ab = MathTex("\\frac{a}{b}")
        times1 = MathTex("\\times")
        frac_bc = MathTex("\\frac{b}{c}")
        times2 = MathTex("\\times")
        frac_cd = MathTex("\\frac{c}{d}")
        times3 = MathTex("\\times")
        frac_de = MathTex("\\frac{d}{e}")

        chain = VGroup(frac_ab, times1, frac_bc, times2, frac_cd, times3, frac_de).arrange(RIGHT, buff=0.25).scale(0.9).move_to(ORIGIN)
        self.play(Write(chain))
        self.wait(1)

        # Step 2: 顏色標記要約分的相鄰項
        step2_label = Text("Step 2: Mark adjacent cancellable pairs", font_size=28).next_to(title, DOWN, buff=0.4)
        self.play(Transform(step1_label, step2_label))

        # 用 MathTex 的索引存取分子分母（注意：\\frac{x}{y} 解析為單一字元時 [0] 是分子，[1] 是分母）
        # 為了示範起見，這裡用 set_color 標記整個分子或分母位置
        b_top = frac_ab[0][1]  # 分母 b
        b_bot = frac_bc[0][0]  # 分子 b
        c_top = frac_bc[0][1]  # 分母 c
        c_bot = frac_cd[0][0]  # 分子 c
        d_top = frac_cd[0][1]  # 分母 d
        d_bot = frac_de[0][0]  # 分子 d

        self.play(
            b_top.animate.set_color(YELLOW), b_bot.animate.set_color(YELLOW),
        )
        self.wait(0.5)
        self.play(
            c_top.animate.set_color(GREEN), c_bot.animate.set_color(GREEN),
        )
        self.wait(0.5)
        self.play(
            d_top.animate.set_color(BLUE), d_bot.animate.set_color(BLUE),
        )
        self.wait(1)

        # Step 3: 消去動畫（用 FadeOut 演出相鄰約分）
        step3_label = Text("Step 3: Cancel each color-matched pair", font_size=28).next_to(title, DOWN, buff=0.4)
        self.play(Transform(step1_label, step3_label))

        self.play(FadeOut(b_top), FadeOut(b_bot), run_time=0.7)
        self.wait(0.3)
        self.play(FadeOut(c_top), FadeOut(c_bot), run_time=0.7)
        self.wait(0.3)
        self.play(FadeOut(d_top), FadeOut(d_bot), run_time=0.7)
        self.wait(1)

        # Step 4: 只剩鏈條兩端 → 寫出結果
        step4_label = Text("Step 4: Only chain endpoints remain", font_size=28).next_to(title, DOWN, buff=0.4)
        self.play(Transform(step1_label, step4_label))

        # 淡出中間殘骸（fraction bars、× 符號）
        self.play(
            FadeOut(frac_ab[0][2:]),  # 殘餘 fraction bar
            FadeOut(frac_bc[0]),
            FadeOut(frac_cd[0]),
            FadeOut(frac_de[0][1:]),  # 殘餘 fraction bar 與分母
            FadeOut(times1), FadeOut(times2), FadeOut(times3),
            run_time=1.2,
        )
        self.wait(0.5)

        # 最終結果：a / e
        result = MathTex("=", "\\frac{a}{e}").scale(1.1).move_to(ORIGIN)
        self.play(Write(result))
        self.wait(0.5)

        result_box = self.get_glow_rect(result, color="#FFBE0B", buff=0.2)
        self.play(Create(result_box))
        self.wait(1.5)

        # 提示：將此手法套用至具體題目時，使用者需先把每個括號化簡為單一分數，再套用此動畫
        hint = Text("To apply: simplify each factor to a single fraction first, then cancel adjacent pairs.",
                    font_size=22, color=GRAY).to_edge(DOWN, buff=0.5)
        self.play(Write(hint))
        self.wait(2)

        # 清理畫面
        self.play(FadeOut(VGroup(title, step1_label, result, result_box, hint,
                                 frac_ab[0][0], frac_de[0][0])))
        self.wait(0.5)
