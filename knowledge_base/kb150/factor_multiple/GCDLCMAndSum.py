from manim import *

class GCDLCMAndSum(Scene):
    """
    Factor multiple GCD LCM 因數與倍數: Visualizes finding the Greatest Common Divisor and Least Common Multiple of 36, 60, and 126 using prime factorization, then sums them.
    """
    def construct(self):
        # Title
        title = Text("Finding GCD and LCM of 36, 60, 126", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 1. Prime Factorization
        prime_factor_title = Text("1. Prime Factorization", font_size=32, color=BLUE).next_to(title, DOWN, buff=0.7).to_edge(LEFT)
        self.play(Write(prime_factor_title))
        self.wait(0.5)

        num1_eq = MathTex("36", "=", "2^2", "\\times", "3^2")
        num2_eq = MathTex("60", "=", "2^2", "\\times", "3", "\\times", "5")
        num3_eq = MathTex("126", "=", "2", "\\times", "3^2", "\\times", "7")

        factorizations = VGroup(num1_eq, num2_eq, num3_eq).arrange(DOWN, buff=0.5).next_to(prime_factor_title, DOWN, buff=0.5).align_to(prime_factor_title, LEFT)
        
        self.play(Write(num1_eq))
        self.wait(1)
        self.play(Write(num2_eq))
        self.wait(1)
        self.play(Write(num3_eq))
        self.wait(1.5)

        # 2. Greatest Common Divisor (GCD)
        gcd_title = Text("2. Greatest Common Divisor (GCD)", font_size=32, color=GREEN).next_to(factorizations, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(gcd_title))
        self.wait(0.5)

        gcd_rule = Text("Rule: Take common prime factors with the lowest power.", font_size=28).next_to(gcd_title, DOWN, buff=0.3).align_to(gcd_title, LEFT)
        self.play(Write(gcd_rule))
        self.wait(1)

        common_factors_text = MathTex("\\text{Common factors: } 2, 3").next_to(gcd_rule, DOWN, buff=0.3).align_to(gcd_rule, LEFT)
        self.play(Write(common_factors_text))
        self.wait(1)

        # Highlight common factors and their lowest powers in the original factorizations
        highlight_2_1 = SurroundingRectangle(num1_eq[2], color=YELLOW) # 2^2
        highlight_2_2 = SurroundingRectangle(num2_eq[2], color=YELLOW) # 2^2
        highlight_2_3 = SurroundingRectangle(num3_eq[2], color=YELLOW) # 2
        highlight_3_1 = SurroundingRectangle(num1_eq[4], color=YELLOW) # 3^2
        highlight_3_2 = SurroundingRectangle(num2_eq[4], color=YELLOW) # 3
        highlight_3_3 = SurroundingRectangle(num3_eq[4], color=YELLOW) # 3^2

        self.play(Create(highlight_2_1), Create(highlight_2_2), Create(highlight_2_3))
        self.wait(0.5)
        self.play(Create(highlight_3_1), Create(highlight_3_2), Create(highlight_3_3))
        self.wait(1)

        lowest_powers_text = MathTex("\\text{Lowest powers: } 2^1, 3^1").next_to(common_factors_text, DOWN, buff=0.3).align_to(common_factors_text, LEFT)
        self.play(Write(lowest_powers_text))
        self.wait(1)

        gcd_calc = MathTex("\\text{GCD} = 2^1 \\times 3^1").next_to(lowest_powers_text, DOWN, buff=0.3).align_to(lowest_powers_text, LEFT)
        self.play(Write(gcd_calc))
        self.wait(0.5)
        gcd_result = MathTex("= 6", color=YELLOW).next_to(gcd_calc, RIGHT, buff=0.2)
        self.play(Write(gcd_result))
        self.wait(1)

        self.play(FadeOut(highlight_2_1, highlight_2_2, highlight_2_3, highlight_3_1, highlight_3_2, highlight_3_3))
        gcd_final = VGroup(gcd_calc, gcd_result)
        gcd_box = SurroundingRectangle(gcd_final, color=YELLOW, buff=0.1)
        self.play(Create(gcd_box))
        self.wait(1)

        # 3. Least Common Multiple (LCM)
        lcm_title = Text("3. Least Common Multiple (LCM)", font_size=32, color=ORANGE).next_to(gcd_final, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(lcm_title))
        self.wait(0.5)

        lcm_rule = Text("Rule: Take all prime factors with the highest power.", font_size=28).next_to(lcm_title, DOWN, buff=0.3).align_to(lcm_title, LEFT)
        self.play(Write(lcm_rule))
        self.wait(1)

        all_factors_text = MathTex("\\text{All factors: } 2, 3, 5, 7").next_to(lcm_rule, DOWN, buff=0.3).align_to(lcm_rule, LEFT)
        self.play(Write(all_factors_text))
        self.wait(1)

        # Highlight all factors and their highest powers
        highlight_2_highest = SurroundingRectangle(num1_eq[2], color=RED) # 2^2
        highlight_3_highest = SurroundingRectangle(num1_eq[4], color=RED) # 3^2
        highlight_5_highest = SurroundingRectangle(num2_eq[6], color=RED) # 5
        highlight_7_highest = SurroundingRectangle(num3_eq[6], color=RED) # 7

        self.play(Create(highlight_2_highest))
        self.wait(0.3)
        self.play(Create(highlight_3_highest))
        self.wait(0.3)
        self.play(Create(highlight_5_highest))
        self.wait(0.3)
        self.play(Create(highlight_7_highest))
        self.wait(1)

        highest_powers_text = MathTex("\\text{Highest powers: } 2^2, 3^2, 5^1, 7^1").next_to(all_factors_text, DOWN, buff=0.3).align_to(all_factors_text, LEFT)
        self.play(Write(highest_powers_text))
        self.wait(1)

        lcm_calc_part1 = MathTex("\\text{LCM} = 2^2 \\times 3^2 \\times 5 \\times 7").next_to(highest_powers_text, DOWN, buff=0.3).align_to(highest_powers_text, LEFT)
        self.play(Write(lcm_calc_part1))
        self.wait(0.5)
        lcm_calc_part2 = MathTex("= 4 \\times 9 \\times 5 \\times 7").next_to(lcm_calc_part1, RIGHT, buff=0.2)
        self.play(Write(lcm_calc_part2))
        self.wait(0.5)
        lcm_result = MathTex("= 1260", color=YELLOW).next_to(lcm_calc_part2, RIGHT, buff=0.2)
        self.play(Write(lcm_result))
        self.wait(1)

        self.play(FadeOut(highlight_2_highest, highlight_3_highest, highlight_5_highest, highlight_7_highest))
        lcm_final = VGroup(lcm_calc_part1, lcm_calc_part2, lcm_result)
        lcm_box = SurroundingRectangle(lcm_final, color=YELLOW, buff=0.1)
        self.play(Create(lcm_box))
        self.wait(1)

        # 4. Sum of GCD and LCM
        sum_title = Text("4. Sum of GCD and LCM", font_size=32, color=PURPLE).next_to(lcm_final, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(sum_title))
        self.wait(0.5)

        sum_eq = MathTex("\\text{Sum} = \\text{GCD} + \\text{LCM}").next_to(sum_title, DOWN, buff=0.3).align_to(sum_title, LEFT)
        self.play(Write(sum_eq))
        self.wait(0.5)

        sum_values = MathTex("= 6 + 1260").next_to(sum_eq, RIGHT, buff=0.2)
        self.play(Write(sum_values))
        self.wait(0.5)

        final_answer = MathTex("= 1266", color=YELLOW).next_to(sum_values, RIGHT, buff=0.2)
        self.play(Write(final_answer))
        self.wait(1)

        final_box = SurroundingRectangle(final_answer, color=GREEN, buff=0.2)
        self.play(Create(final_box))
        self.wait(2)

        # Fade out everything
        self.play(
            FadeOut(title, prime_factor_title, factorizations, gcd_title, gcd_rule, common_factors_text, lowest_powers_text, gcd_final, gcd_box,
                    lcm_title, lcm_rule, all_factors_text, highest_powers_text, lcm_final, lcm_box,
                    sum_title, sum_eq, sum_values, final_answer, final_box)
        )
        self.wait(0.5)