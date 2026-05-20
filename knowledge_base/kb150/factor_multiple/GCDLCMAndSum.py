from manim import *

class GCDLCMAndSum(Scene):
    """
    Factor multiple GCD LCM 因數與倍數: Visualizes the "prime-factorization-based GCD & LCM" technique.

    動畫手法範本：質因數分解求 GCD 與 LCM
    ----------
    適用場景：
    - 求多個正整數的最大公因數 (GCD) 與最小公倍數 (LCM)
    - 適合處理 3 個以上的數字（短除法相對麻煩時）
    - 也可作為 GCD+LCM、GCD×LCM 等綜合應用題的前置步驟

    視覺要點（四階段）：
    1. **質因數分解**：對每個數寫出 a^x × b^y × ... 形式
    2. **求 GCD**：用 YELLOW 框標記「共同因數的最低次方」→ 相乘
    3. **求 LCM**：用 RED 框標記「所有因數的最高次方」→ 相乘
    4. **後續運算**（GCD+LCM、GCD×LCM 等）：依題目要求加總或相乘

    注意：本範本用 24, 40, 90 三個數作為示意例（避開 Q109 的 36/60/126、Q116 的相關數字），
    使用者套用時須**自行**對真實題目做質因數分解，並抓出共同/全部質因數。
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

        title = Text("Technique: Prime Factorization → GCD & LCM", font_size=32).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: 質因數分解（示意例 24, 40, 90）
        s1_title = Text("Step 1: Prime Factorization", font_size=26, color="#3A86FF").next_to(title, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(s1_title))

        n1 = MathTex("24", "=", "2^3", "\\times", "3")
        n2 = MathTex("40", "=", "2^3", "\\times", "5")
        n3 = MathTex("90", "=", "2", "\\times", "3^2", "\\times", "5")
        facts = VGroup(n1, n2, n3).arrange(DOWN, buff=0.3).next_to(s1_title, DOWN, buff=0.3).align_to(s1_title, LEFT)
        self.play(Write(n1)); self.wait(0.3)
        self.play(Write(n2)); self.wait(0.3)
        self.play(Write(n3)); self.wait(0.8)

        # Step 2: GCD = 共同因數最低次方
        s2_title = Text("Step 2: GCD = lowest power of SHARED primes", font_size=26, color="#06D6A0").next_to(facts, DOWN, buff=0.6).to_edge(LEFT)
        self.play(Write(s2_title))

        # 標記 24 的 2^3, 40 的 2^3, 90 的 2（共同 prime 2，最低次方 = 2^1）
        h_2_1 = self.get_glow_rect(n1[2], color="#FFBE0B")
        h_2_2 = self.get_glow_rect(n2[2], color="#FFBE0B")
        h_2_3 = self.get_glow_rect(n3[2], color="#FFBE0B")
        self.play(Create(h_2_1), Create(h_2_2), Create(h_2_3))
        self.wait(0.5)

        gcd_calc = MathTex("\\text{GCD} = 2^1 = 2", color="#FFBE0B").next_to(s2_title, DOWN, buff=0.3).align_to(s2_title, LEFT)
        self.play(Write(gcd_calc))
        self.wait(0.8)
        self.play(FadeOut(h_2_1, h_2_2, h_2_3))

        # Step 3: LCM = 所有因數最高次方
        s3_title = Text("Step 3: LCM = highest power of ALL primes", font_size=26, color=ORANGE).next_to(gcd_calc, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(s3_title))

        # 標記每個 prime 的最高次方位置
        h_2_max = self.get_glow_rect(n1[2], color="#FF006E")  # 2^3
        h_3_max = self.get_glow_rect(n3[4], color="#FF006E")  # 3^2
        h_5_max = self.get_glow_rect(n2[4], color="#FF006E")  # 5
        self.play(Create(h_2_max), Create(h_3_max), Create(h_5_max))
        self.wait(0.5)

        lcm_calc = MathTex("\\text{LCM} = 2^3 \\times 3^2 \\times 5 = 360", color=ORANGE).next_to(s3_title, DOWN, buff=0.3).align_to(s3_title, LEFT)
        self.play(Write(lcm_calc))
        self.wait(0.8)
        self.play(FadeOut(h_2_max, h_3_max, h_5_max))

        # Step 4: 後續應用（依題目要求，這裡演示 GCD + LCM）
        s4_title = Text("Step 4: Apply result to question (sum / product / etc.)", font_size=24, color="#8338EC").next_to(lcm_calc, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(s4_title))

        apply_eq = MathTex("\\text{Example: } \\text{GCD} + \\text{LCM} = 2 + 360 = 362", color="#FFBE0B").next_to(s4_title, DOWN, buff=0.3).align_to(s4_title, LEFT)
        self.play(Write(apply_eq))
        self.wait(1.5)

        # 收尾：標記答案 + 通用提示
        self.play(
            FadeOut(VGroup(s1_title, facts, s2_title, gcd_calc, s3_title, lcm_calc, s4_title)),
            apply_eq.animate.move_to(ORIGIN),
        )
        ans_box = self.get_glow_rect(apply_eq, color="#06D6A0", buff=0.2)
        self.play(Create(ans_box))
        self.wait(1.5)

        hint = Text("To apply: factorize each number, then read off GCD/LCM by power rules.",
                    font_size=20, color=GRAY).to_edge(DOWN, buff=0.4)
        self.play(Write(hint))
        self.wait(2)

        self.play(FadeOut(VGroup(title, apply_eq, ans_box, hint)))
