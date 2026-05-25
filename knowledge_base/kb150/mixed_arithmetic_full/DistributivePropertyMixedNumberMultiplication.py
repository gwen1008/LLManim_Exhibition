from manim import *

class DistributivePropertyMixedNumberMultiplication(Scene):
    """
    Complete mixed arithmetic 完整的四則混合運算: Visualizes applying the distributive property to calculate 39 and 7/8 multiplied by -4, showing 39 * (-4) + 7/8 * (-4).
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

        # 1. Title and Initial Problem
        title = Text("Distributive Property with Mixed Numbers", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        problem_expr = MathTex("39", r"\frac{7}{8}", r" \times ", "(-4)", font_size=60)
        self.play(Write(problem_expr))
        self.wait(1)

        # 2. Deconstruct Mixed Number into sum and apply parentheses
        # Target expression: (39 + 7/8) * (-4)
        decomposed_expr = MathTex("(", "39", " + ", r"\frac{7}{8}", ")", r" \times ", "(-4)", font_size=60)
        
        # Move the problem expression up to make space for the next step
        self.play(problem_expr.animate.shift(UP * 1.5))
        
        # Transform the mixed number part into (integer + fraction) using TransformMatchingTex
        # This will match '39', '7/8', 'x (-4)' and add parentheses and '+'
        self.play(TransformMatchingTex(problem_expr, decomposed_expr))
        self.wait(1.5)

        # 3. Apply Distributive Property
        # Target expression for distribution: 39 * (-4) + 7/8 * (-4)
        distributed_expr = MathTex("39", r" \times ", "(-4)", " + ", r"\frac{7}{8}", r" \times ", "(-4)", font_size=60)
        distributed_expr.next_to(decomposed_expr, DOWN, buff=1)

        # Identify the terms for distribution from decomposed_expr
        term1_obj = decomposed_expr[1] # 39
        term2_obj = decomposed_expr[3] # 7/8
        multiplier_obj = decomposed_expr[6] # (-4)

        # Show the distribution arrows
        arrow1 = Arrow(multiplier_obj.get_left(), term1_obj.get_right(), buff=0.1, color="#FFBE0B")
        arrow2 = Arrow(multiplier_obj.get_left(), term2_obj.get_right(), buff=0.1, color="#FFBE0B")

        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        # Animate the distribution using TransformMatchingTex
        # TransformMatchingTex will handle the duplication of '(-4)' and insertion of 'x' and '+'
        self.play(
            TransformMatchingTex(decomposed_expr, distributed_expr),
            FadeOut(arrow1, arrow2)
        )
        self.wait(2)

        # Move the distributed expression to the center for clarity
        self.play(distributed_expr.animate.move_to(ORIGIN))
        self.wait(1)

        # 4. Compare with Option A
        option_A_label = Text("This matches Option A:", font_size=35).next_to(distributed_expr, DOWN, buff=1)
        option_A_expr = MathTex("39", r" \times ", "(-4)", " + ", r"\frac{7}{8}", r" \times ", "(-4)", font_size=60, color="#06D6A0")
        option_A_expr.next_to(option_A_label, DOWN, buff=0.5)

        self.play(Write(option_A_label))
        # Use TransformMatchingTex to show it's the same expression, but with a color change
        self.play(TransformMatchingTex(distributed_expr.copy(), option_A_expr))
        self.wait(2)

        # Final highlight of the correct option
        final_box = self.get_glow_rect(option_A_expr, color="#06D6A0", buff=0.2)
        self.play(Create(final_box))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
        self.wait(1)