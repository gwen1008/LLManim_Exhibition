# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示漢米爾頓的肖像、引言與布魯姆橋紀念牌上的四元數方程式，逐步呈現歷史背景與數學發現。



from manim import *
class IntroduceHamilton(Scene):
    def construct(self):
        hamilton = ImageMobject("Hamilton").set_height(6)
        hamilton.to_corner(UL)
        shamrock = SVGMobject(file_name="shamrock")
        shamrock.set_height(1)
        shamrock.set_color("#009a49")
        shamrock.set_fill(opacity=0.25)
        shamrock.next_to(hamilton.get_corner(UL), DR)
        shamrock.align_to(hamilton, UP)
        hamilton_name = Text(
            "William Rowan Hamilton"
        )
        hamilton_name.match_width(hamilton)
        hamilton_name.next_to(hamilton, DOWN)

        quote = Text(
            """...Every morning in the early part of the above-cited
            month, on my coming down to breakfast, your (then)
            little brother William Edwin, and yourself, used to
            ask me,""",
            "``Well, Papa, can you multiply triplets''?",
            """Whereto I was always obliged to reply, with a sad
            shake of the head: ``No, I can only add and subtract
            them.''...""",
            font_size=36,
            line_spacing=1.2
        )
        # 手動設定顏色（ManimCE 沒有 set_color_by_tex）
        quote_parts = quote.submobjects
        quote_parts[0].set_color(WHITE)
        quote_parts[1].set_color(YELLOW)  # "Papa" 在第二部分
        quote_parts[2].set_color(WHITE)
        quote = VGroup(*quote_parts)
        quote.set_width(FRAME_WIDTH - hamilton.get_width() - 2)
        quote.to_edge(RIGHT)
        quote_rect = SurroundingRectangle(quote, buff=MED_SMALL_BUFF)
        quote_rect.set_stroke(WHITE, 2)
        quote_rect.stretch(1.1, 1)
        quote_label = Text(
            "August 5, 1865 Letter\nfrom Hamilton to his son",
            font_size=24
        )
        quote_label.next_to(quote_rect, UP)
        quote_label.set_color(BLUE)
        VGroup(quote, quote_rect, quote_label).to_edge(UP)

        plaque = ImageMobject("BroomBridgePlaque")
        plaque.set_width(FRAME_WIDTH / 2)
        plaque.to_edge(LEFT)
        plaque.shift(UP)
        equation = MathTex(
            "i^2 = j^2 = k^2 = ijk = -1",
            tex_to_color_map={"i": GREEN, "j": RED, "k": BLUE}
        )
        equation_rect = Rectangle(width=3.25, height=0.7)
        equation_rect.move_to(3.15 * LEFT + 0.25 * DOWN)
        equation_rect.set_color(WHITE)
        equation_arrow = Arrow(start=UP, end=DOWN, color=WHITE)
        equation_arrow.match_color(equation_rect)
        equation_arrow.next_to(equation_rect, DOWN)
        equation.next_to(equation_arrow, DOWN)

        self.play(
            FadeIn(hamilton, shift=DOWN),
            Write(hamilton_name),
        )
        self.play(DrawBorderThenFill(shamrock))
        self.wait()

        self.play(
            LaggedStartMap(
                FadeIn, quote,
                lag_ratio=0.2,
                run_time=4
            ),
            FadeIn(quote_label, shift=DOWN),
            Create(quote_rect)
        )
        self.wait(3)
        self.play(
            VGroup(hamilton, shamrock, hamilton_name).animate.to_edge(RIGHT),
            run_time=2,
            rate_func=lambda t: smooth(min(1, 0.5 + 0.5 * t))  # 近似 squish_rate_func(smooth, 0.5, 1)
        )
        self.play(
            LaggedStartMap(
                FadeOut, VGroup(quote, quote_rect, quote_label),
                shift=DOWN,
                lag_ratio=0.1
            )
        )
        self.wait()
        self.play(FadeIn(plaque))
        self.play(
            Create(equation_rect),
            GrowArrow(equation_arrow)
        )
        # 建立一個隱形的方程式副本用於轉換
        equation_faded = equation.copy()
        equation_faded.replace(equation_rect)
        equation_faded.set_opacity(0)
        self.play(ReplacementTransform(
            equation_faded,
            equation
        ))
        self.wait()
