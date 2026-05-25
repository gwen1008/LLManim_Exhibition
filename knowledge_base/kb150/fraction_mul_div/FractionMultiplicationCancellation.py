from manim import *

class FractionMultiplicationCancellation(Scene):
    """
    Fraction multiplication division 分數乘除: Visualizes the "direct cancellation" technique when integer factor equals fraction's denominator.

    動畫手法範本：整數與分母直接約分
    ----------
    適用場景：
    - n × (k/n) 形式（整數因數 = 分數分母）→ 直接消去
    - 適用於先化簡分配律後出現大數字、但發現整數與某分母正好相同的情況
    - 強調「先觀察結構、再硬算」的思考路徑

    視覺要點：
    1. 用 self.get_glow_rect 標記「整數因數」與「分母」兩個相同的數
    2. 用 Cross 演出消去動作（兩個地方同時打叉）
    3. 直接寫出最終答案，省略中間運算

    注意：本範本用 12 × (-25/12) 作為示意例（避開 2023, 2024 等實驗題數字），
    使用者套用時須**自行判斷**整數是否真的等於分母，並選擇此手法。
    若整數不等於分母（如 12 × (-25/6) 須先約分），須改用其他手法。
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

        # 標題：描述手法
        title = Text("Technique: Direct Cancellation (integer = denominator)", font_size=32).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 示意題目：12 × (-25/12)，避開實驗題中的 2023, 2024
        # 把分數拆成獨立 MathTex（"25" 與 "12"）放在 Tex 包裝的分數線結構裡，
        # 這樣可以直接拿到分母 Mobject 來標記。
        frac_numer = MathTex("25", font_size=48)
        frac_denom = MathTex("12", font_size=48)
        frac_line = Line(LEFT * 0.3, RIGHT * 0.3, stroke_width=2)
        frac_group = VGroup(frac_numer, frac_line, frac_denom).arrange(DOWN, buff=0.05)

        eq_parts = VGroup(
            MathTex("12", font_size=48),
            MathTex("\\times", font_size=48),
            MathTex("\\left(", font_size=48),
            MathTex("-", font_size=48),
            frac_group,
            MathTex("\\right)", font_size=48),
        ).arrange(RIGHT, buff=0.15).next_to(title, DOWN, buff=1)
        self.play(Write(eq_parts))
        self.wait(1)

        # 標記要約分的兩個 12（整數因數 與 分母）
        integer_part = eq_parts[0]
        denom_part = frac_denom
        rect_int = self.get_glow_rect(integer_part, color="#FFBE0B", buff=0.1)
        rect_den = self.get_glow_rect(denom_part, color="#FFBE0B", buff=0.1)
        self.play(Create(rect_int), Create(rect_den))
        self.wait(1)

        hint = Text("Observation: integer factor equals the denominator → cancel directly",
                    font_size=24, color="#3A86FF").next_to(eq_parts, DOWN, buff=0.8)
        self.play(Write(hint))
        self.wait(1)

        # Cross 演出消去
        cross_int = Cross(integer_part, stroke_width=5, color="#FF006E")
        cross_den = Cross(denom_part, stroke_width=5, color="#FF006E")
        self.play(Create(cross_int), Create(cross_den), FadeOut(rect_int), FadeOut(rect_den))
        self.wait(1)

        # 簡化結果
        simplified = MathTex("=", "-25", font_size=48).next_to(hint, DOWN, buff=1)
        self.play(Write(simplified))
        self.wait(1)

        # 收尾：清理畫面，標記最終答案
        final_box = self.get_glow_rect(simplified, color="#06D6A0", buff=0.2)
        self.play(
            FadeOut(eq_parts, cross_int, cross_den, hint),
            simplified.animate.move_to(ORIGIN),
        )
        self.play(Create(final_box))
        self.wait(2)

        warning = Text("Only valid if integer = denominator exactly. Otherwise factor first.",
                       font_size=20, color=GRAY).to_edge(DOWN, buff=0.4)
        self.play(Write(warning))
        self.wait(2)
        self.play(FadeOut(VGroup(title, simplified, final_box, warning)))
