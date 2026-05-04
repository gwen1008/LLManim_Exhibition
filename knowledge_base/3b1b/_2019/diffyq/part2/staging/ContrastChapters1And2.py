# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 對比第一章和第二章的內容，展示常微分方程與偏微分方程在求解難度上的視覺化比較。



from manim import *
class ContrastChapters1And2(Scene):
    def construct(self):
        c1_frame, c2_frame = frames = VGroup(*[
            ScreenRectangle(height=3.5)
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)

        c1_title, c2_title = titles = VGroup(
            Text("Chapter 1"),
            Text("Chapter 2"),
        )
        titles.scale(1.5)

        ode, pde = des = VGroup(
            Text(
                "Ordinary\nDifferential Equations\nODEs",
                alignment="center"
            ),
            Text(
                "Partial\nDifferential Equations\nPDEs",
                alignment="center"
            ),
        )
        ode[0].set_color(BLUE)
        pde[0].set_color(YELLOW)
        for de in des:
            # 在CE中，Text對象沒有子部分索引，所以我們需要不同的方法
            # 我們將使用set_color_by_text來近似
            de.set_color_by_text("ODEs", BLUE)
            de.set_color_by_text("PDEs", YELLOW)
            # 放大最後一行
            lines = de.text.split('\n')
            if len(lines) > 2:
                de.text = '\n'.join(lines[:-1]) + '\n'  # 保留前兩行
                # 添加放大的最後一行
                last_line = Text(lines[-1], color=de[-1].get_color() if hasattr(de[-1], 'get_color') else WHITE)
                last_line.scale(1.5, about_point=de.get_top())
                last_line.next_to(de, DOWN, buff=0.1)
                de.add(last_line)

        for title, frame, de in zip(titles, frames, des):
            title.next_to(frame, UP)
            de.match_width(frame)
            de.next_to(frame, DOWN)

        lt = MathTex("<")
        lt.move_to(Line(ode.get_right(), pde.get_left()))
        lt.scale(2, about_edge=UP)

        c1_words = Text(
            "They're\nreally\nfreaking\nhard\nto\nsolve",
            alignment="center"
        )
        c1_words.set_height(0.5 * c1_frame.get_height())
        c1_words.move_to(c1_frame)

        c2_words = Text(
            "They're\nreally\nreally\nfreaking\nhard\nto\nsolve",
            alignment="center"
        )
        # 在CE中，我們需要手動設置顏色
        c2_words[0].set_color(WHITE)  # They're
        c2_words[1].set_color(WHITE)  # really
        c2_words[2].set_color(YELLOW)  # really (強調)
        c2_words[3].set_color(WHITE)  # freaking
        c2_words[4].set_color(WHITE)  # hard
        c2_words[5].set_color(WHITE)  # to
        c2_words[6].set_color(WHITE)  # solve
        c2_words.move_to(c2_frame)
        
        edit_shift = MED_LARGE_BUFF * RIGHT
        c2_edits = VGroup(
            Text("sometimes").next_to(
                c2_words[1:3], UP,
                aligned_edge=LEFT,
            ),
            Line(
                c2_words[1].get_left(),
                c2_words[2].get_right(),
                stroke_width=8,
            ),
            Text("not too").next_to(
                c2_words[3], LEFT,
            ),
            Line(
                c2_words[3].get_left(),
                c2_words[3].get_right(),
                stroke_width=8,
            ),
        )
        c2_edits.set_color(RED)
        c2_edits[2:].shift(edit_shift)

        self.add(titles)
        self.add(frames)
        self.add(des)

        self.wait()
        self.play(LaggedStart(
            *[FadeIn(word, shift=DOWN) for word in c1_words],
            lag_ratio=0.1,
        ))
        self.wait()
        self.play(
            TransformFromCopy(c1_words, c2_words),
            Write(lt)
        )
        self.wait()
        self.play(
            Write(c2_edits[:2], run_time=1),
        )
        self.play(
            c2_words[3:5].animate.shift(edit_shift),
            Write(c2_edits[2:]),
            run_time=1,
        )
        self.wait()
