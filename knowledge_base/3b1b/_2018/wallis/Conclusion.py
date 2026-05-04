# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 教師與學生場景，展示從沃利斯乘積推導到正弦公式，再連接到巴塞爾問題的數學推導過程。



from manim import *
class Conclusion(TeacherStudentsScene):
    def __init__(self, camera_config={"background_opacity": 1}, **kwargs):
        super().__init__(camera_config=camera_config, **kwargs)

    def construct(self):
        wallis_product = get_wallis_product(6)
        wallis_product.move_to(self.hold_up_spot, DOWN)
        wallis_product.shift_onto_screen()
        for i in range(0, len(wallis_product) - 5, 4):
            color = GREEN if (i / 4) % 2 == 0 else BLUE
            wallis_product[i:i + 3].set_color(color)

        sine_formula = MathTex(
            "\\sin(", "f", "\\pi", ")", "=", "f", "\\pi",
            "\\prod_{k \\ne 0}", "\\left(", "1", "-",
            "{f", "\\over", "k}", "\\right)"
        )
        sine_formula.set_color_by_tex("f", GREEN)
        sine_formula.set_color_by_tex("left", WHITE)
        sine_formula.move_to(self.hold_up_spot, DOWN)
        sine_formula.shift_onto_screen()

        euler = ImageMobject("Euler")
        euler.set_height(2.5)
        basel_problem = MathTex(
            "\\frac{1}{1^2} + ",
            "\\frac{1}{2^2} + ",
            "\\frac{1}{3^2} + ",
            "\\cdots",
            "\\frac{\\pi^2}{6}"
        )
        basel_problem.move_to(self.hold_up_spot, DOWN)
        implication = MathTex("\\Rightarrow")
        implication.next_to(basel_problem[0][1], LEFT)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(wallis_product, shift=DOWN),
            self.change_students("thinking", "hooray", "surprised")
        )
        self.wait()
        self.play(
            self.teacher.animate.change("hooray"),
            FadeIn(sine_formula, shift=DOWN),
            wallis_product.animate.to_edge(UP),
            self.change_students("pondering", "thinking", "erm")
        )
        self.wait(3)
        self.play(
            sine_formula.animate.next_to(implication, LEFT, 
                submobject_to_align=sine_formula[-1]),
            FadeIn(implication),
        )
        euler.next_to(sine_formula, UP)
        self.play(
            FadeIn(euler),
            LaggedStartMap(FadeIn, basel_problem),
            self.teacher.animate.change("happy"),
            self.change_students("sassy", "confused", "hesitant")
        )
        self.wait(2)

        wallis_rect = SurroundingRectangle(wallis_product)
        wallis_rect.set_color(BLUE)
        basel_rect = SurroundingRectangle(basel_problem)
        basel_rect.set_color(YELLOW)

        self.play(
            Create(wallis_rect),
            FadeOut(implication),
            FadeOut(euler),
            FadeOut(sine_formula),
        )
        self.play(
            Create(basel_rect),
            self.teacher.animate.change("surprised"),
            self.change_students(*["happy"] * 3)
        )
        self.wait(5)
