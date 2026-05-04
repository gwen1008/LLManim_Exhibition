# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示重複應用函數 f(x) = 1 + 1/x 的迭代過程，從任意初始值收斂到黃金比例 φ。



from manim import *
class ShowRepeatedApplication(Scene):
    def __init__(self, title_color=YELLOW, **kwargs):
        super().__init__(**kwargs)
        self.title_color = title_color

    def construct(self):
        self.add_func_title()
        self.show_repeated_iteration()

    def add_func_title(self):
        title = self.title = VGroup(
            MathTex("f(", "x", ")"),
            MathTex("="),
            self.get_nested_one_plus_one_over_x(1)
        )
        title.arrange(RIGHT)
        title.to_corner(UL)
        title.set_color(self.title_color)

        self.add(title)

    def get_nested_one_plus_one_over_x(self, n):
        # 創建嵌套的 1 + 1/x 表達式
        if n == 1:
            return MathTex("1 + \\frac{1}{x}")
        else:
            inner = self.get_nested_one_plus_one_over_x(n-1)
            return MathTex("1 + \\frac{1}{", inner.tex_string, "}")

    def show_repeated_iteration(self):
        line = VGroup()
        decimal_kwargs = {
            "num_decimal_places": 3,
            "show_ellipsis": True,
        }
        phi = (1 + np.sqrt(5)) / 2

        def func(x):
            return 1.0 + 1.0 / x

        initial_term = DecimalNumber(2.71828, **decimal_kwargs)
        line.add(initial_term)
        last_term = initial_term

        def get_arrow():
            arrow = MathTex("\\rightarrow")
            arrow.stretch(1.5, 0)
            arrow.next_to(line[-1], RIGHT)
            tex = MathTex("f(x)")
            tex.set_color(YELLOW)
            tex.match_width(arrow)
            tex.next_to(arrow, UP, buff=SMALL_BUFF)
            return VGroup(arrow, tex)

        for x in range(2):
            arrow = get_arrow()
            line.add(arrow)

            new_term = DecimalNumber(
                func(last_term.number),
                **decimal_kwargs
            )
            new_term.next_to(arrow[0], RIGHT)
            last_term = new_term
            line.add(new_term)

        line.add(get_arrow())
        line.add(MathTex("\\dots\\dots").next_to(line[-1][0], RIGHT))
        num_phi_mob = DecimalNumber(phi, **decimal_kwargs)
        line.add(num_phi_mob.next_to(line[-1], RIGHT))
        line.move_to(DOWN)

        rects = VGroup(*[
            SurroundingRectangle(mob)
            for mob in (line[0], line[1:-1], line[-1])
        ])
        rects.set_stroke(BLUE, 2)

        braces = VGroup(*[
            Brace(rect, DOWN, buff=SMALL_BUFF)
            for rect in rects
        ])
        # 使用漸變色
        colors = [GREEN, interpolate_color(GREEN, YELLOW, 0.5), YELLOW]
        for brace, color in zip(braces, colors):
            brace.set_color(color)
        
        brace_texts = VGroup(*[
            brace.get_text(text).scale(0.75, about_edge=UP)
            for brace, text in zip(braces, [
                "Arbitrary \\\\ starting \\\\ value",
                "Repeatedly apply $f(x)$",
                "$\\varphi$ \\\\ ``Golden ratio''"
            ])
        ])
        var_phi_mob = brace_texts[2][0]
        var_phi_mob.scale(2, about_edge=UP).set_color(YELLOW)
        brace_texts[2][1:].next_to(var_phi_mob, DOWN, buff=MED_SMALL_BUFF)

        # Animations
        self.add(line[0])
        self.play(
            GrowFromCenter(braces[0]),
            Write(brace_texts[0])
        )
        self.wait()
        self.play(
            GrowFromEdge(line[1], LEFT),
            FadeIn(braces[1]),
            FadeIn(brace_texts[1]),
        )
        self.play(TransformFromCopy(line[0], line[2]))
        self.wait()

        self.play(GrowFromEdge(line[3], LEFT))
        self.play(TransformFromCopy(line[2], line[4]))
        self.wait()

        self.play(GrowFromEdge(line[5], LEFT))
        self.play(LaggedStart(*[GrowFromCenter(mob) for mob in line[6]]))
        self.wait()

        self.play(FadeIn(line[7]))
        self.play(
            GrowFromCenter(braces[2]),
            FadeIn(brace_texts[2]),
        )
        self.wait()
