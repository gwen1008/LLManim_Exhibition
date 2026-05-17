from manim import *

class ScientificNotationBacterialLength(Scene):
    """
    Exponent scientific notation 指數與科學記號: Visualizes calculating total length of 5 million bacteria (3.2 micrometers each) in meters,
    converting units and expressing the final answer in scientific notation.
    """
    def construct(self):
        # Problem Statement
        problem_text = Text("問題：5百萬個細菌首尾相連，總長度是多少公尺？", font_size=36)
        problem_text.to_edge(UP)
        self.play(Write(problem_text))
        self.wait(1)

        # Step 1: Convert single bacterium length to meters
        step1_title = Text("步驟 1: 單一細菌長度換算為公尺", font_size=30).next_to(problem_text, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(step1_title))

        bacterium_length_um = MathTex(r"\text{單一細菌長度} = 3.2 \text{ 微米}")
        conversion_factor = MathTex(r"1 \text{ 微米} = 10^{-6} \text{ 公尺}")
        
        step1_grp = VGroup(bacterium_length_um, conversion_factor).arrange(DOWN, buff=0.5).next_to(step1_title, DOWN, buff=0.5).align_to(step1_title, LEFT)
        self.play(Write(step1_grp))
        self.wait(1)

        bacterium_length_m = MathTex(r"3.2 \text{ 微米} = 3.2 \times 10^{-6} \text{ 公尺}", color=YELLOW)
        bacterium_length_m.next_to(conversion_factor, DOWN, buff=0.5).align_to(step1_title, LEFT)
        self.play(TransformMatchingTex(bacterium_length_um, bacterium_length_m))
        self.play(FadeOut(conversion_factor))
        self.wait(1)

        # Step 2: Convert number of bacteria to scientific notation
        step2_title = Text("步驟 2: 細菌總數轉換為科學記號", font_size=30).next_to(bacterium_length_m, DOWN, buff=1).to_edge(LEFT)
        self.play(Write(step2_title))

        num_bacteria_text = MathTex(r"\text{細菌總數} = 5 \text{ 百萬個}")
        num_bacteria_sci = MathTex(r"5 \text{ 百萬個} = 5 \times 10^6 \text{ 個}", color=YELLOW)
        
        step2_grp = VGroup(num_bacteria_text, num_bacteria_sci).arrange(DOWN, buff=0.5).next_to(step2_title, DOWN, buff=0.5).align_to(step2_title, LEFT)
        self.play(Write(num_bacteria_text))
        self.wait(0.5)
        self.play(TransformMatchingTex(num_bacteria_text, num_bacteria_sci))
        self.wait(1)

        # Move relevant parts to center for calculation
        self.play(
            FadeOut(step1_title),
            FadeOut(step2_title),
            bacterium_length_m.animate.shift(UP * 2.5).to_edge(LEFT).set_color(WHITE),
            num_bacteria_sci.animate.shift(UP * 2.5).next_to(bacterium_length_m, RIGHT, buff=1).set_color(WHITE),
            problem_text.animate.set_opacity(0.3)
        )
        
        # Step 3: Set up the total length calculation
        calc_title = Text("計算總長度", font_size=36).to_edge(UP)
        self.play(Transform(problem_text, calc_title))

        total_length_eq = MathTex(
            r"\text{總長度} =",
            r"(3.2 \times 10^{-6})",
            r"\times",
            r"(5 \times 10^6)",
            font_size=48
        ).move_to(ORIGIN)
        self.play(Write(total_length_eq[0]))
        self.play(FadeIn(total_length_eq[1]), FadeIn(total_length_eq[3]), FadeIn(total_length_eq[2]))
        self.wait(1)

        # Step 4: Rearrange and multiply
        rearranged_eq = MathTex(
            r"\text{總長度} =",
            r"(3.2 \times 5)",
            r"\times",
            r"(10^{-6} \times 10^6)",
            font_size=48
        ).move_to(ORIGIN)
        self.play(TransformMatchingTex(total_length_eq, rearranged_eq))
        self.wait(1.5)

        # Calculate numerical part
        num_product = MathTex(r"3.2 \times 5 = 16", color=BLUE).next_to(rearranged_eq, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(num_product))
        self.wait(1)

        # Calculate powers of 10 part
        exp_product = MathTex(r"10^{-6} \times 10^6 = 10^{-6+6} = 10^0", color=GREEN).next_to(num_product, RIGHT, buff=1)
        self.play(Write(exp_product))
        self.wait(1.5)

        # Step 5: Simplify 10^0
        exp_simplify = MathTex(r"10^0 = 1", color=GREEN).next_to(exp_product, DOWN, buff=0.5).align_to(exp_product, LEFT)
        self.play(Write(exp_simplify))
        self.wait(1)

        # Step 6: Combine results
        combined_result = MathTex(
            r"\text{總長度} =",
            r"16",
            r"\times",
            r"1",
            font_size=48
        ).move_to(ORIGIN)
        self.play(
            TransformMatchingTex(rearranged_eq[0], combined_result[0]),
            TransformMatchingTex(rearranged_eq[1], combined_result[1]),
            TransformMatchingTex(rearranged_eq[3], combined_result[3]),
            TransformMatchingTex(rearranged_eq[2], combined_result[2]),
            FadeOut(num_product),
            FadeOut(exp_product),
            FadeOut(exp_simplify)
        )
        self.wait(1)

        final_intermediate = MathTex(r"\text{總長度} = 16 \text{ 公尺}", font_size=48, color=YELLOW).move_to(ORIGIN)
        self.play(TransformMatchingTex(combined_result, final_intermediate))
        self.wait(1.5)

        # Step 7: Convert to standard scientific notation
        sci_notation_rule = Text("科學記號要求數字部分介於 1 (含) 到 10 (不含) 之間", font_size=28, color=BLUE)
        sci_notation_rule.next_to(final_intermediate, DOWN, buff=1)
        self.play(Write(sci_notation_rule))
        self.wait(2)

        final_answer_sci = MathTex(r"16 = 1.6 \times 10^1", font_size=48, color=GREEN).next_to(final_intermediate, DOWN, buff=0.5)
        self.play(Write(final_answer_sci))
        self.wait(1.5)

        final_result_text = MathTex(r"\text{最終答案: } 1.6 \times 10^1 \text{ 公尺}", font_size=54, color=WHITE)
        final_result_text.move_to(ORIGIN)
        
        self.play(
            FadeOut(final_intermediate),
            FadeOut(sci_notation_rule),
            FadeOut(final_answer_sci),
            FadeOut(bacterium_length_m),
            FadeOut(num_bacteria_sci),
            Transform(problem_text, final_result_text)
        )
        final_box = SurroundingRectangle(problem_text, color=GREEN, buff=0.3)
        self.play(Create(final_box))
        self.wait(3)