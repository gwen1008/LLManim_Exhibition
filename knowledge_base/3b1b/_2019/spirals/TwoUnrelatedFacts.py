# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示兩個不相關的數論事實：左側為分數近似圓周率，右側為模44的剩餘類表格，並用顏色標示偶數行和質數。



from manim import *
class TwoUnrelatedFacts(Scene):
    def construct(self):
        self.add_title()
        self.show_columns()

    def add_title(self):
        title = Text("Two (unrelated) bits of number theory")
        title.set_width(config.frame_width - 1)
        title.to_edge(UP)
        h_line = Line()
        h_line.match_width(title)
        h_line.next_to(title, DOWN, buff=SMALL_BUFF)
        h_line.set_stroke(GREY_B)

        self.play(
            FadeIn(title),
            Create(h_line),
        )

        self.h_line = h_line

    def show_columns(self):
        h_line = self.h_line
        v_line = Line(
            h_line.get_center() + MED_SMALL_BUFF * DOWN,
            config.frame_height * DOWN / 2,
        )
        v_line.match_style(h_line)

        approx = MathTex(
            "{44 \\over 7} \\approx 2\\pi"
        )
        approx.scale(1.5)
        approx.next_to(
            h_line.point_from_proportion(0.25),
            DOWN, buff=MED_LARGE_BUFF,
        )

        mod = 44
        n_terms = 9
        residue_classes = VGroup()
        prime_numbers = self.read_in_primes(1000)
        primes = VGroup()
        non_primes = VGroup()
        for r in range(mod):
            if r <= 11 or r == 43:
                row = VGroup()
                for n in range(r, r + n_terms * mod, mod):
                    elem = Integer(n)
                    comma = MathTex(",")
                    comma.next_to(
                        elem.get_corner(DR),
                        RIGHT, buff=SMALL_BUFF
                    )
                    elem.add(comma)
                    row.add(elem)
                    if n in prime_numbers:
                        primes.add(elem)
                    else:
                        non_primes.add(elem)
                row.arrange(RIGHT, buff=0.3)
                dots = MathTex("\\dots")
                dots.next_to(row.get_corner(DR), RIGHT, buff=SMALL_BUFF)
                dots.shift(SMALL_BUFF * UP)
                row.add(dots)
                row.r = r
            if r == 12:
                row = MathTex("\\vdots")
            residue_classes.add(row)

        residue_classes.arrange(DOWN)
        residue_classes[-2].align_to(residue_classes, LEFT)
        residue_classes[-2].shift(MED_SMALL_BUFF * RIGHT)
        residue_classes.set_height(6)
        residue_classes.next_to(ORIGIN, RIGHT)
        residue_classes.to_edge(DOWN, buff=MED_SMALL_BUFF)

        def get_line(row):
            return Line(
                row.get_left(), row.get_right(),
                stroke_color=RED,
                stroke_width=4,
            )

        even_lines = VGroup(*[
            get_line(row)
            for row in residue_classes[:12:2]
        ])
        eleven_line = get_line(residue_classes[11])
        eleven_line.set_color(PINK)
        for line in [even_lines[1], eleven_line]:
            line.scale(0.93, about_edge=RIGHT)

        self.play(Create(v_line))
        self.wait()
        self.play(FadeIn(approx, shift=DOWN))
        self.wait()
        self.play(FadeIn(residue_classes))
        self.wait()
        self.play(
            LaggedStartMap(Create, even_lines),
        )
        self.wait()
        self.play(Create(eleven_line))
        self.wait()
        self.play(
            primes.animate.set_color(TEAL),
            non_primes.animate.set_opacity(0.25),
            even_lines.animate.set_opacity(0.25),
            eleven_line.animate.set_opacity(0.25),
        )
        self.wait()

    def read_in_primes(self, n):
        # 簡單的質數生成函數（替代原來的讀檔功能）
        primes = []
        for num in range(2, n + 1):
            is_prime = True
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        return primes
