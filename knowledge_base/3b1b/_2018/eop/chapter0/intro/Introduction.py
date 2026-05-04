# Source: 3b1b/_2018/eop/chapter0/intro.py
# Description: [3b1b translated] 展示教師與學生場景，包含影片系列動畫和歡迎文字，並演示一系列動畫效果。



from manim import *
class Introduction(TeacherStudentsScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": MAROON_E,
            "flip_at_start": True,
        },
        **kwargs
    ):
        super().__init__(default_pi_creature_kwargs=default_pi_creature_kwargs, **kwargs)

    def construct(self):
        self.show_series()
        self.show_examples()

    def show_series(self):
        series = VideoSeries(num_videos=11)
        series.to_edge(UP)
        this_video = series[0]
        this_video.set_color(YELLOW)
        this_video.save_state()
        this_video.set_fill(opacity=0)
        this_video.center()
        this_video.set_height(FRAME_HEIGHT)
        self.this_video = this_video

        words = Text("Welcome to\n", "Essence of Probability")
        words.set_color_by_tex("Essence of Probability", YELLOW)

        self.teacher.change_mode("happy")
        self.play(
            FadeIn(
                series,
                lag_ratio=0.5,
                run_time=2
            ),
            Blink(self.teacher)
        )
        self.teacher_says(words, target_mode="hooray")
        self.play_student_changes(
            *["hooray"]*3,
            look_at=series[1].get_left(),
            added_anims=[
                ApplyMethod(this_video.restore, run_time=3),
            ]
        )
        self.play(*[
            ApplyMethod(
                video.shift, 0.5*video.get_height()*DOWN,
                run_time=3,
                rate_func=squish_rate_func(
                    there_and_back, alpha, alpha+0.3
                )
            )
            for video, alpha in zip(series, np.linspace(0, 0.7, len(series)))
        ]+[
            Animation(self.teacher.bubble),
            Animation(self.teacher.bubble.content),
        ])

        self.play(
            FadeOut(self.teacher.bubble),
            FadeOut(self.teacher.bubble.content),
            self.teacher.change_mode, "raise_right_hand",
            *[
                ApplyMethod(pi.change_mode, "pondering")
                for pi in self.students
            ]
        )
        self.wait()

        self.series = series

    def show_examples(self):
        self.wait(10)
