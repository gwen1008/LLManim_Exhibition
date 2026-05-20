from manim import *

class IntegerSubtractionWithBrackets(Scene):
    """
    Integer addition subtraction 整數加減: Visualizes the step-by-step calculation of 543 - [219 + (-543)] - 381 using bracket removal and term rearrangement.
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

        # [VISUAL REASONING]
        # 1. Pedagogical Goal: Demonstrate correct bracket removal with a leading minus sign and efficient term rearrangement.
        # 2. Layout Strategy: Display the problem at the top, then show each step of the calculation vertically.
        # 3. Anti-Overlap Check: Use VGroup and .next_to for relative positioning.
        # 4. Animation Flow: Introduce problem -> Remove brackets (emphasize sign change) -> Rearrange terms -> Perform grouped additions -> Final subtraction.

        # --- Initial Setup ---
        title = Text("Calculate: 543 - [219 + (-543)] - 381", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Original expression
        expr1 = MathTex("543", "-", "[", "219", "+", "(-543)", "]", "-", "381")
        expr1.move_to(ORIGIN)
        self.play(Write(expr1))
        self.wait(1)

        # --- Step 1: Remove Brackets (Distribute the negative sign) ---
        # Highlight the minus sign before the bracket
        minus_sign_before_bracket = expr1[1] # The '-' before '['
        bracket_open = expr1[2]
        bracket_close = expr1[6]
        
        self.play(
            minus_sign_before_bracket.animate.set_color(RED),
            bracket_open.animate.set_color(RED),
            bracket_close.animate.set_color(RED),
            run_time=1
        )
        self.wait(0.5)

        # Explain the rule
        rule_text = Text("When removing brackets preceded by a minus sign, change the sign of each term inside.", font_size=28)
        rule_text.next_to(expr1, DOWN, buff=1).to_edge(LEFT)
        self.play(Write(rule_text))
        self.wait(2)
        self.play(FadeOut(rule_text))

        # Transform the expression
        # 543 - [219 + (-543)] - 381  =>  543 - 219 - (-543) - 381
        expr2_intermediate = MathTex("543", "-", "219", "-", "(-543)", "-", "381")
        expr2_intermediate.next_to(expr1, DOWN, buff=0.8).align_to(expr1, LEFT)
        
        # Animate the transformation of the bracketed part
        self.play(
            TransformMatchingTex(
                expr1, expr2_intermediate,
                transform_mismatches=True,
                key_map={
                    "219": "219",
                    "(-543)": "(-543)",
                    "-": "-", # The minus sign before bracket becomes part of the new expression
                }
            ),
            bracket_open.animate.set_opacity(0),
            bracket_close.animate.set_opacity(0),
            run_time=2
        )
        self.wait(1)

        # 543 - 219 - (-543) - 381  =>  543 - 219 + 543 - 381
        expr3 = MathTex("543", "-", "219", "+", "543", "-", "381")
        expr3.next_to(expr2_intermediate, DOWN, buff=0.8).align_to(expr2_intermediate, LEFT)

        # Highlight -(-543) becoming +543
        minus_minus_543 = VGroup(expr2_intermediate[3], expr2_intermediate[4])
        self.play(minus_minus_543.animate.set_color(YELLOW))
        self.wait(0.5)

        self.play(
            *[ReplacementTransform(expr2_intermediate[i], expr3[i]) for i in range(7)],
            run_time=1.5
        )
        self.wait(1)

        # --- Step 2: Rearrange Terms ---
        # Group positive and negative terms
        # (543 + 543) - (219 + 381)
        expr4 = MathTex("(", "543", "+", "543", ")", "-", "(", "219", "+", "381", ")")
        expr4.next_to(expr3, DOWN, buff=0.8).align_to(expr3, LEFT)

        # Highlight terms being grouped
        pos_543_1 = expr3[0]
        pos_543_2 = expr3[4]
        neg_219 = expr3[2]
        neg_381 = expr3[6]

        self.play(
            pos_543_1.animate.set_color(GREEN),
            pos_543_2.animate.set_color(GREEN),
            neg_219.animate.set_color(BLUE),
            neg_381.animate.set_color(BLUE)
        )
        self.wait(1)

        # expr3: 0:"543", 1:"-", 2:"219", 3:"+", 4:"543", 5:"-", 6:"381"
        # expr4: 0:"(", 1:"543", 2:"+", 3:"543", 4:")", 5:"-", 6:"(", 7:"219", 8:"+", 9:"381", 10:")"
        self.play(
            ReplacementTransform(expr3[0], expr4[1]), # 543
            ReplacementTransform(expr3[4], expr4[3]), # 543
            ReplacementTransform(expr3[3], expr4[2]), # +
            ReplacementTransform(expr3[1], expr4[5]), # -
            ReplacementTransform(expr3[2], expr4[7]), # 219
            ReplacementTransform(expr3[5], expr4[8]), # - becomes + inside bracket
            ReplacementTransform(expr3[6], expr4[9]), # 381
            FadeIn(expr4[0], expr4[4], expr4[6], expr4[10]), # Brackets
            run_time=2
        )
        self.wait(1)

        # --- Step 3: Perform Additions ---
        # Calculate (543 + 543) and (219 + 381)
        expr5 = MathTex("1086", "-", "600")
        expr5.next_to(expr4, DOWN, buff=0.8).align_to(expr4, LEFT)

        # Highlight (543 + 543)
        group_543 = VGroup(expr4[1], expr4[2], expr4[3])
        self.play(group_543.animate.set_color(GREEN))
        self.wait(0.5)
        self.play(
            TransformFromCopy(group_543, expr5[0])
        )
        self.wait(0.5)

        # Highlight (219 + 381)
        group_219_381 = VGroup(expr4[7], expr4[8], expr4[9])
        self.play(group_219_381.animate.set_color(BLUE))
        self.wait(0.5)
        self.play(
            TransformFromCopy(group_219_381, expr5[2])
        )
        self.wait(0.5)

        # expr4: 0:"(", 1:"543", 2:"+", 3:"543", 4:")", 5:"-", 6:"(", 7:"219", 8:"+", 9:"381", 10:")"
        # expr5: 0:"1086", 1:"-", 2:"600"
        self.play(
            ReplacementTransform(VGroup(expr4[0], expr4[1], expr4[2], expr4[3], expr4[4]), expr5[0]),
            ReplacementTransform(expr4[5], expr5[1]),
            ReplacementTransform(VGroup(expr4[6], expr4[7], expr4[8], expr4[9], expr4[10]), expr5[2]),
            run_time=1.5
        )
        self.wait(1)

        # --- Step 4: Final Subtraction ---
        expr6 = MathTex("486")
        expr6.next_to(expr5, DOWN, buff=0.8).align_to(expr5, LEFT)

        self.play(
            TransformMatchingTex(expr5, expr6),
            run_time=1.5
        )
        self.wait(1)

        # --- Final Answer ---
        final_answer_box = self.get_glow_rect(expr6, color="#06D6A0", buff=0.2)
        self.play(Create(final_answer_box))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))
        self.wait(1)