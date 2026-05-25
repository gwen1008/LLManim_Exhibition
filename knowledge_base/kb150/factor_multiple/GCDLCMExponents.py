from manim import *

class GCDLCMExponents(Scene):
    """
    Factor multiple GCD LCM 因數與倍數: Visualizes finding unknown exponents 'a' and 'b' in prime factorizations using given GCD and LCM values.
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

        # Problem Statement
        title = Text("Finding Unknown Exponents using GCD and LCM", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Given information
        prime_factor_a = MathTex(r"M = 2^a \times 3^2 \times 7")
        prime_factor_b = MathTex(r"N = 2^3 \times 3^b \times 5")
        given_gcd = MathTex(r"\text{GCD}(M, N) = 72")
        given_lcm = MathTex(r"\text{LCM}(M, N) = 2^4 \times 3^3 \times 5 \times 7")
        
        problem_group = VGroup(prime_factor_a, prime_factor_b, given_gcd, given_lcm).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        problem_group.next_to(title, DOWN, buff=0.8).to_edge(LEFT)
        
        self.play(Write(problem_group))
        self.wait(1)

        # Step 1: Factorize GCD
        step1_title = Text("Step 1: Factorize GCD", font_size=30).next_to(problem_group, RIGHT, buff=1).align_to(prime_factor_a, UP)
        self.play(Write(step1_title))

        gcd_val = given_gcd.copy().set_color(YELLOW)
        self.play(Transform(gcd_val, MathTex(r"72 = 2^3 \times 3^2").move_to(step1_title).shift(DOWN*0.8)))
        
        gcd_rule = Text("GCD: take min exponent of shared primes", font_size=22, color="#3A86FF").next_to(gcd_val, DOWN, buff=0.5)
        self.play(Write(gcd_rule))
        self.wait(1)

        # Step 2: Determine 'a' (for prime factor 2)
        step2_title = Text("Step 2: Determine 'a' (for prime factor 2)", font_size=30).next_to(gcd_rule, DOWN, buff=1).align_to(step1_title, LEFT)
        self.play(Write(step2_title))

        # Highlight relevant parts for 'a'
        a_parts = VGroup(
            prime_factor_a[0][3], # 2^a
            prime_factor_b[0][3], # 2^3
            gcd_val[0][3],        # 2^3 from 72
            given_lcm[0][3]       # 2^4 from LCM
        ).copy().set_color(YELLOW)
        
        self.play(
            Indicate(prime_factor_a[0][3:5]),
            Indicate(prime_factor_b[0][3:5]),
            Indicate(gcd_val[0][3:5]),
            Indicate(given_lcm[0][3:5]),
            FadeIn(a_parts)
        )
        
        # GCD condition for 'a'
        gcd_a_eq = MathTex(r"\min(a, 3) = 3").next_to(step2_title, DOWN, buff=0.5)
        gcd_a_implication = MathTex(r"\Rightarrow a \ge 3").next_to(gcd_a_eq, RIGHT, buff=0.5)
        self.play(Write(gcd_a_eq))
        self.play(Write(gcd_a_implication))
        self.wait(0.5)

        # LCM condition for 'a'
        lcm_rule = Text("LCM: take max exponent of all primes", font_size=22, color="#3A86FF").next_to(gcd_a_implication, DOWN, buff=0.5).align_to(gcd_rule, LEFT)
        self.play(Write(lcm_rule))
        
        lcm_a_eq = MathTex(r"\max(a, 3) = 4").next_to(lcm_rule, DOWN, buff=0.5)
        lcm_a_implication = MathTex(r"\Rightarrow a = 4").next_to(lcm_a_eq, RIGHT, buff=0.5)
        self.play(Write(lcm_a_eq))
        self.play(Write(lcm_a_implication))
        self.wait(1)

        # Conclude 'a'
        a_result = MathTex(r"\therefore a = 4", color="#06D6A0").next_to(lcm_a_implication, DOWN, buff=0.5).align_to(lcm_a_eq, LEFT)
        self.play(Write(a_result))
        self.wait(1)

        # Step 3: Determine 'b' (for prime factor 3)
        step3_title = Text("Step 3: Determine 'b' (for prime factor 3)", font_size=30).next_to(a_result, DOWN, buff=1).align_to(step2_title, LEFT)
        self.play(Write(step3_title))

        # Highlight relevant parts for 'b'
        b_parts = VGroup(
            prime_factor_a[0][7], # 3^2
            prime_factor_b[0][7], # 3^b
            gcd_val[0][7],        # 3^2 from 72
            given_lcm[0][7]       # 3^3 from LCM
        ).copy().set_color(YELLOW)

        self.play(
            Indicate(prime_factor_a[0][7:9]),
            Indicate(prime_factor_b[0][7:9]),
            Indicate(gcd_val[0][7:9]),
            Indicate(given_lcm[0][7:9]),
            FadeIn(b_parts)
        )

        # GCD condition for 'b'
        gcd_b_eq = MathTex(r"\min(2, b) = 2").next_to(step3_title, DOWN, buff=0.5)
        gcd_b_implication = MathTex(r"\Rightarrow b \ge 2").next_to(gcd_b_eq, RIGHT, buff=0.5)
        self.play(Write(gcd_b_eq))
        self.play(Write(gcd_b_implication))
        self.wait(0.5)

        # LCM condition for 'b'
        lcm_b_eq = MathTex(r"\max(2, b) = 3").next_to(gcd_b_implication, DOWN, buff=0.5).align_to(lcm_rule, LEFT)
        lcm_b_implication = MathTex(r"\Rightarrow b = 3").next_to(lcm_b_eq, RIGHT, buff=0.5)
        self.play(Write(lcm_b_eq))
        self.play(Write(lcm_b_implication))
        self.wait(1)

        # Conclude 'b'
        b_result = MathTex(r"\therefore b = 3", color="#06D6A0").next_to(lcm_b_implication, DOWN, buff=0.5).align_to(lcm_b_eq, LEFT)
        self.play(Write(b_result))
        self.wait(1)

        # Step 4: Calculate a + b
        step4_title = Text("Step 4: Calculate a + b", font_size=30).next_to(b_result, DOWN, buff=1).align_to(step3_title, LEFT)
        self.play(Write(step4_title))

        final_calc = MathTex(r"a + b = 4 + 3 = 7", color="#FFBE0B").next_to(step4_title, DOWN, buff=0.5)
        self.play(Write(final_calc))
        self.wait(1)

        # Highlight final answer
        final_answer_box = self.get_glow_rect(final_calc, color="#06D6A0", buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)