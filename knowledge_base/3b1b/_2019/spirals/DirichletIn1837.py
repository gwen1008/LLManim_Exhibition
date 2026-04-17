# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示時間軸上三個重要數學事件（Dirichlet定理、黎曼猜想、質數定理）的標記，並聚焦於1837年Dirichlet定理的視覺呈現。



from manim import *
class DirichletIn1837(Scene):
    def construct(self):
        # Add timeline
        dates = list(range(1780, 2030, 10))
        timeline = NumberLine(
            x_range=[1700, 2020, 1],
            length=10,
            include_numbers=True,
            numbers_with_elongated_ticks=dates,
            stroke_color=GREY,
            stroke_width=2,
        )
        timeline.add_labels(
            dict(zip(dates, [str(date) for date in dates])),
            font_size=24
        )
        timeline.labels.shift(SMALL_BUFF * DOWN)
        timeline.to_edge(RIGHT)

        # Special dates
        arrows = VGroup()
        labels = VGroup()
        special_dates = [1837, 1859, 1896]
        label_texts = [
            "Dirichlet's\\\\theorem\\\\1837",
            "Riemann\\\\hypothesis\\\\1859",
            "Prime number\\\\theorem\\\\1896",
        ]
        
        for date, text in zip(special_dates, label_texts):
            arrow = Arrow(start=UP, end=DOWN, color=WHITE)
            arrow.next_to(timeline.number_to_point(date), UP)
            arrows.add(arrow)
            
            label = MathTex(text)
            label.next_to(arrow, UP)
            labels.add(label)

        d_arrow, rh_arrow, pnt_arrow = arrows
        d_label, rh_label, pnt_label = labels

        # Back in time
        frame = self.camera.frame
        self.add(timeline, arrows, labels)
        self.play(
            frame.animate.move_to(timeline.number_to_point(1837)),
            run_time=4,
        )
        self.wait()

        # Show picture
        image = ImageMobject("Dirichlet")
        image.set_height(3)
        image.next_to(d_label, LEFT)
        self.play(FadeIn(image, shift=RIGHT))
        self.wait()

        # Flash
        self.play(
            Flash(
                d_label.get_center(),
                num_lines=12,
                line_length=0.25,
                flash_radius=1.5,
                line_stroke_width=3,
                lag_ratio=0.05,
            )
        )
        self.wait()

        # Transition title
        title, underline = self.get_title_and_underline()
        n = len(title[0])
        self.play(
            ReplacementTransform(d_label[0][:n], title[0][:n]),
            FadeOut(d_label[0][n:]),
            LaggedStart(
                *[FadeOut(mob, shift=DOWN) for mob in [
                    image, d_arrow,
                    rh_label, rh_arrow,
                    pnt_label, pnt_arrow,
                    *timeline,
                ]]
            ),
        )
        self.play(Create(underline))
        self.wait()

    def get_title_and_underline(self):
        frame = self.camera.frame
        title = MathTex("Dirichlet's theorem")
        title.scale(1.5)
        title.next_to(frame.get_top(), DOWN, buff=MED_LARGE_BUFF)
        underline = Line()
        underline.match_width(title)
        underline.next_to(title, DOWN, SMALL_BUFF)
        return title, underline
