from manim import *

class FindExponentsGCDLCM(Scene):
    """
    Factor multiple GCD LCM 因數與倍數: Visualizes finding unknown exponents a, b, c in prime factorizations of A and B, given their GCD and LCM.
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

        # 1. Setup - Display the given information
        title = Text("Finding Unknown Exponents with GCD and LCM", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Given expressions
        A_expr = MathTex("A = 2^a \\times 3^2 \\times 5^c")
        B_expr = MathTex("B = 2^3 \\times 3^b \\times 5^2")
        gcd_expr = MathTex("\\text{GCD}(A,B) = 2^2 \\times 3^1 \\times 5^2")
        lcm_expr = MathTex("\\text{LCM}(A,B) = 2^3 \\times 3^2 \\times 5^3")

        expressions = VGroup(A_expr, B_expr, gcd_expr, lcm_expr).arrange(DOWN, buff=0.6).next_to(title, DOWN, buff=0.8)
        self.play(FadeIn(expressions, shift=UP))
        self.wait(1)

        # Rules for GCD and LCM exponents
        gcd_rule = Text("GCD: Takes the minimum exponent for each prime factor.", font_size=28, color="#FFBE0B").to_edge(LEFT).shift(UP*2)
        lcm_rule = Text("LCM: Takes the maximum exponent for each prime factor.", font_size=28, color="#FFBE0B").to_edge(RIGHT).shift(UP*2)
        rules_group = VGroup(gcd_rule, lcm_rule).arrange(RIGHT, buff=1.0).next_to(expressions, DOWN, buff=1.0)
        
        self.play(Write(gcd_rule))
        self.wait(0.5)
        self.play(Write(lcm_rule))
        self.wait(1)

        # 2. Find 'a' (for prime factor 2)
        self.play(
            Indicate(A_expr[0][2]), # a in 2^a
            Indicate(B_expr[0][2]), # 3 in 2^3
            Indicate(gcd_expr[0][2]), # 2 in 2^2
            FadeOut(lcm_rule) # Focus on GCD rule
        )
        self.play(gcd_rule.animate.to_edge(UP).shift(DOWN*0.5).scale(1.2).set_color(GREEN))

        find_a_text = Text("For prime factor 2:", font_size=32).next_to(expressions, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(find_a_text))

        a_logic = MathTex("\\min(a, 3) = 2").next_to(find_a_text, DOWN, buff=0.5).align_to(find_a_text, LEFT)
        self.play(Write(a_logic))
        self.wait(1)

        a_result = MathTex("\\Rightarrow a = 2", color="#3A86FF").next_to(a_logic, RIGHT, buff=0.5)
        self.play(Write(a_result))
        self.wait(1)

        # 3. Find 'b' (for prime factor 3)
        self.play(
            FadeOut(find_a_text, a_logic, a_result),
            Indicate(A_expr[0][5]), # 2 in 3^2
            Indicate(B_expr[0][5]), # b in 3^b
            Indicate(gcd_expr[0][5]), # 1 in 3^1
            gcd_rule.animate.set_color(YELLOW).scale(1/1.2).to_edge(LEFT).shift(UP*2) # Reset rule position
        )
        self.play(gcd_rule.animate.to_edge(UP).shift(DOWN*0.5).scale(1.2).set_color(GREEN))

        find_b_text = Text("For prime factor 3:", font_size=32).next_to(expressions, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(find_b_text))

        b_logic = MathTex("\\min(2, b) = 1").next_to(find_b_text, DOWN, buff=0.5).align_to(find_b_text, LEFT)
        self.play(Write(b_logic))
        self.wait(1)

        b_result = MathTex("\\Rightarrow b = 1", color="#3A86FF").next_to(b_logic, RIGHT, buff=0.5)
        self.play(Write(b_result))
        self.wait(1)

        # 4. Find 'c' (for prime factor 5)
        self.play(
            FadeOut(find_b_text, b_logic, b_result),
            FadeIn(lcm_rule), # Bring back LCM rule
            Indicate(A_expr[0][8]), # c in 5^c
            Indicate(B_expr[0][8]), # 2 in 5^2
            Indicate(lcm_expr[0][8]), # 3 in 5^3
            FadeOut(gcd_rule) # Focus on LCM rule
        )
        self.play(lcm_rule.animate.to_edge(UP).shift(DOWN*0.5).scale(1.2).set_color(GREEN))

        find_c_text = Text("For prime factor 5:", font_size=32).next_to(expressions, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(find_c_text))

        c_logic = MathTex("\\max(c, 2) = 3").next_to(find_c_text, DOWN, buff=0.5).align_to(find_c_text, LEFT)
        self.play(Write(c_logic))
        self.wait(1)

        c_result = MathTex("\\Rightarrow c = 3", color="#3A86FF").next_to(c_logic, RIGHT, buff=0.5)
        self.play(Write(c_result))
        self.wait(1)

        # 5. Calculate a+b+c
        self.play(
            FadeOut(find_c_text, c_logic, c_result, lcm_rule),
            FadeOut(expressions),
            FadeOut(title)
        )

        summary_a = MathTex("a = 2").to_edge(LEFT).shift(UP*1)
        summary_b = MathTex("b = 1").next_to(summary_a, DOWN, buff=0.5).align_to(summary_a, LEFT)
        summary_c = MathTex("c = 3").next_to(summary_b, DOWN, buff=0.5).align_to(summary_a, LEFT)
        
        self.play(Write(summary_a), Write(summary_b), Write(summary_c))
        self.wait(1)

        final_calc = MathTex("a + b + c = 2 + 1 + 3").next_to(summary_c, DOWN, buff=1.0).align_to(summary_a, LEFT)
        self.play(Write(final_calc))
        self.wait(1)

        final_answer = MathTex("= 6", color="#06D6A0").next_to(final_calc, RIGHT, buff=0.5)
        self.play(Write(final_answer))
        self.wait(1)

        final_box = self.get_glow_rect(final_answer, color="#06D6A0", buff=0.2)
        self.play(Create(final_box))
        self.wait(2)