# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示傅立葉系列與傅立葉轉換的標題動畫，過渡到傅立葉肖像與論文介紹，並標註關鍵年份與熱力學相關內容。



from manim import *
class FourierNameIntro(Scene):
    def construct(self):
        self.show_two_titles()
        self.transition_to_image()
        self.show_paper()

    def show_two_titles(self):
        lt = MathTex("\\text{Fourier}", "\\text{Series}")
        rt = MathTex("\\text{Fourier}", "\\text{Transform}")
        lt_variants = VGroup(
            MathTex("\\text{Complex}", "\\text{Fourier Series}"),
            MathTex("\\text{Discrete}", "\\text{Fourier Series}"),
        )
        rt_variants = VGroup(
            MathTex("\\text{Discrete}", "\\text{Fourier Transform}"),
            MathTex("\\text{Fast}", "\\text{Fourier Transform}"),
            MathTex("\\text{Quantum}", "\\text{Fourier Transform}"),
        )

        titles = VGroup(lt, rt)
        titles.scale(1.5)
        for title, vect in (lt, LEFT), (rt, RIGHT):
            title.move_to(vect * config.frame_width / 4)
            title.to_edge(UP)

        for title, variants in (lt, lt_variants), (rt, rt_variants):
            title.save_state()
            title.target = title.copy()
            title.target.scale(1 / 1.5, about_edge=RIGHT)
            for variant in variants:
                variant.move_to(title.target, UR)
                variant[0].set_color(YELLOW)

        v_line = Line(UP, DOWN)
        v_line.set_height(config.frame_height)
        v_line.set_stroke(WHITE, 2)

        self.play(
            FadeIn(lt, shift=RIGHT),
            Create(v_line)
        )
        self.play(
            FadeIn(rt, shift=LEFT),
        )

        for title, variants in [(rt, rt_variants)]:
            self.play(
                title.animate.move_to(title.target.get_center()).scale(title.target.get_height() / title.get_height()),
                FadeIn(variants[0][0], shift=LEFT)
            )
            for v1, v2 in zip(variants, variants[1:]):
                self.play(
                    FadeOut(v1[0], shift=UP),
                    FadeIn(v2[0], shift=DOWN),
                    run_time=0.5,
                )
                self.wait(0.5)
            self.play(
                Restore(title),
                FadeOut(variants[-1][0])
            )
        self.wait()

        self.titles = titles
        self.v_line = v_line

    def transition_to_image(self):
        titles = self.titles
        v_line = self.v_line

        image = ImageMobject("Joseph Fourier")
        image.set_height(5)
        image.to_edge(LEFT)

        frame = Rectangle()
        frame.replace(image, stretch=True)

        name = MathTex("\\text{Joseph}", "\\text{Fourier}")
        fourier_part = name.get_part_by_tex("Fourier")
        fourier_part.set_color(YELLOW)
        F_sym = fourier_part[0]
        name.match_width(image)
        name.next_to(image, DOWN)

        self.play(
            ReplacementTransform(v_line, frame),
            FadeIn(image),
            FadeIn(name[0]),
            *[
                ReplacementTransform(
                    title[0].copy(),
                    name[1]
                )
                for title in titles
            ],
            titles.animate.scale(0.65).arrange(DOWN, buff=0.5).next_to(image, UP),
        )
        self.wait()

        big_F = F_sym.copy()
        big_F.set_fill(opacity=0)
        big_F.set_stroke(WHITE, 2)
        big_F.set_height(3)
        big_F.move_to(midpoint(
            image.get_right(),
            config.frame_right * RIGHT,
        ))
        big_F.shift(DOWN)
        equivalence = VGroup(
            fourier_part.copy().scale(1.25),
            MathTex("\\Leftrightarrow").scale(1.5),
            MathTex("\\text{Break down into}\\\\ \\text{pure frequencies}"),
        )
        equivalence.arrange(RIGHT)
        equivalence.move_to(big_F)
        equivalence.to_edge(UP)

        self.play(
            FadeIn(big_F),
            TransformFromCopy(fourier_part, equivalence[0]),
            Write(equivalence[1:]),
        )
        self.wait(3)
        self.play(FadeOut(VGroup(big_F, equivalence)))

        self.image = image
        self.name = name

    def show_paper(self):
        image = self.image
        paper = ImageMobject("Fourier paper")
        paper.match_height(image)
        paper.next_to(image, RIGHT, buff=MED_LARGE_BUFF)

        date = MathTex("1822")
        date.next_to(paper, DOWN)
        date_rect = SurroundingRectangle(date)
        date_rect.scale(0.3)
        date_rect.set_color(RED)
        date_rect.shift(1.37 * UP + 0.08 * LEFT)
        date_arrow = Arrow(
            date_rect.get_bottom(),
            date.get_top(),
            buff=SMALL_BUFF,
            color=date_rect.get_color(),
        )

        heat_rect = SurroundingRectangle(
            MathTex("\\text{CHALEUR}")
        )
        heat_rect.set_color(RED)
        heat_rect.scale(0.6)
        heat_rect.move_to(
            paper.get_top() +
            1.22 * DOWN + 0.37 * RIGHT
        )
        heat_word = MathTex("\\text{Heat}")
        heat_word.scale(1.5)
        heat_word.next_to(paper, UP)
        heat_word.shift(paper.get_width() * RIGHT)
        heat_arrow = Arrow(
            heat_rect.get_top(),
            heat_word.get_left(),
            buff=0.1,
            arc_center=heat_rect.get_top() + 0.5 * LEFT,
            color=heat_rect.get_color(),
        )

        self.play(FadeIn(paper, shift=LEFT))
        self.play(
            Create(date_rect),
        )
        self.play(
            GrowFromPoint(date, date_arrow.get_start()),
            Create(date_arrow),
        )
        self.wait(3)

        self.play(
            Create(heat_rect),
        )
        self.play(
            GrowFromPoint(heat_word, heat_arrow.get_start()),
            Create(heat_arrow),
        )
        self.wait(3)
