# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 教師向學生介紹歐拉函數的術語，展示與44互質的數字，並解釋「相對質數」、「互質」和「totatives」等概念。


from manim import *
import itertools as it

class IntroduceTotientJargon(TeacherStudentsScene):
    def construct(self):
        self.add_title()
        self.eliminate_non_coprimes()

    def add_title(self):
        self.teacher_says(
            "More jargon!",
            target_mode="hooray",
        )
        self.play_all_student_changes("erm")
        words = self.teacher.bubble.content

        words.generate_target()
        words.target.scale(1.5)
        words.target.center().to_edge(UP, buff=MED_SMALL_BUFF)
        words.target.set_color(BLUE)
        underline = Line(LEFT, RIGHT)
        underline.match_width(words.target)
        underline.next_to(words.target, DOWN, buff=SMALL_BUFF)
        underline.scale(1.2)

        self.play(
            MoveToTarget(words),
            FadeOut(self.teacher.bubble),
            LaggedStart(*[
                FadeOut(pi, shift=4 * DOWN)
                for pi in self.pi_creatures
            ]),
            Create(underline)
        )

    def eliminate_non_coprimes(self):
        number_grid = VGroup(*[
            VGroup(*[
                Integer(n) for n in range(11 * k, 11 * (k + 1))
            ]).arrange(DOWN)
            for k in range(4)
        ]).arrange(RIGHT, buff=1)
        numbers = VGroup(*it.chain(*number_grid))
        numbers.set_height(6)
        numbers.move_to(4 * LEFT)
        numbers.to_edge(DOWN)

        evens = VGroup(*filter(
            lambda nm: nm.get_value() % 2 == 0,
            numbers
        ))
        div11 = VGroup(*filter(
            lambda nm: nm.get_value() % 11 == 0,
            numbers
        ))
        coprimes = VGroup(*filter(
            lambda nm: nm not in evens and nm not in div11,
            numbers
        ))

        words = Text(
            "Which ones don't\nshare any factors\nwith 44",
            alignment=""
        )
        words.scale(1.5)
        words.next_to(ORIGIN, RIGHT)

        # 手動標記 "44" 部分
        ff = words[3][-2:]  # 假設 "44" 是最後兩個字符
        ff.set_color(YELLOW)
        ff.generate_target()

        # Show coprimes
        self.play(
            ShowIncreasingSubsets(numbers, run_time=3),
            FadeIn(words, shift=LEFT)
        )
        self.wait()
        for group in evens, div11:
            rects = VGroup(*[
                SurroundingRectangle(number, color=RED)
                for number in group
            ])
            self.play(LaggedStartMap(Create, rects, run_time=1))
            self.play(
                LaggedStart(*[
                    number.animate.set_opacity(0.2)
                    for number in group
                ]),
                LaggedStartMap(FadeOut, rects),
                run_time=1
            )
            self.wait()

        # Rearrange words
        # 手動分割文字部分
        dsf = VGroup(words[1], words[2])  # "don't\nshare any factors"
        dsf.generate_target()
        dsf.target.arrange(RIGHT)
        # 對齊處理
        dsf.target[0].align_to(dsf.target[1][0], DOWN)

        example = numbers[35].copy()
        example.generate_target()
        example.target.match_height(ff)
        num_pair = VGroup(
            ff.target,
            Text("and").scale(1.5),
            example.target,
        )
        num_pair.arrange(RIGHT)
        num_pair.move_to(words.get_top(), DOWN)
        dsf.target.next_to(num_pair, DOWN, buff=MED_LARGE_BUFF)

        phrase1 = Text("are ``relatively prime''")
        phrase2 = Text("are ``coprime''")
        for phrase in [phrase1, phrase2]:
            phrase.scale(1.5)
            phrase.move_to(dsf.target)
            phrase[0][-13:].set_color(BLUE)  # 設置引號內文字為藍色
            phrase.arrow = MathTex("\\Updownarrow")
            phrase.arrow.scale(1.5)
            phrase.arrow.next_to(phrase, DOWN, buff=2 * SMALL_BUFF)
            phrase.rect = SurroundingRectangle(phrase[0][-13:])
            phrase.rect.set_stroke(BLUE)

        self.play(
            FadeOut(words[0]),  # "Which ones "
            FadeOut(words[3][:-2]),  # "with " 部分
            MoveToTarget(dsf),
            MoveToTarget(ff),
            GrowFromCenter(num_pair[1]),
        )
        self.play(
            MoveToTarget(example, path_arc=30 * DEGREES),
        )
        self.wait()
        self.play(
            dsf.animate.next_to(phrase1.arrow, DOWN, buff=SMALL_BUFF),
            GrowFromEdge(phrase1.arrow, UP),
            GrowFromCenter(phrase1),
            Create(phrase1.rect)
        )
        self.play(FadeOut(phrase1.rect))
        self.wait()
        self.play(
            VGroup(dsf, phrase1, phrase1.arrow).animate.next_to(
                phrase2.arrow, DOWN, buff=SMALL_BUFF
            ),
            GrowFromEdge(phrase2.arrow, UP),
            GrowFromCenter(phrase2),
            Create(phrase2.rect)
        )
        self.play(FadeOut(phrase2.rect))
        self.wait()

        # Count through coprimes
        coprime_rects = VGroup(*map(SurroundingRectangle, coprimes))
        coprime_rects.set_stroke(BLUE, 2)
        
        # 創建更新函數
        def update_example(mob):
            if len(coprime_rects) > 0:
                mob.set_value(coprimes[len(coprime_rects) - 1].get_value())
        
        example_anim = UpdateFromFunc(example, update_example)
        self.play(
            ShowIncreasingSubsets(coprime_rects, int_func=np.ceil),
            example_anim,
            run_time=3,
            rate_func=linear,
        )
        self.wait()

        # Show totient function
        words_to_keep = VGroup(ff, num_pair[1], example, phrase2)
        to_fade = VGroup(phrase2.arrow, phrase1, phrase1.arrow, dsf)

        totient = MathTex("\\phi", "(", "44", ")", "=", "20")
        totient.set_color_by_tex("44", YELLOW)
        totient.scale(1.5)
        totient.move_to(num_pair, UP)
        phi = totient[0]  # phi符號
        rhs = Integer(20)
        rhs.replace(totient[-1], dim_to_match=1)
        totient.submobjects[-1] = rhs

        self.play(
            words_to_keep.animate.to_edge(DOWN),
            MaintainPositionRelativeTo(to_fade, words_to_keep),
            VFadeOut(to_fade),
        )
        self.play(FadeIn(totient))
        self.wait()

        # Label totient
        brace = Brace(phi, DOWN)
        etf = Text("Euler's totient function")
        etf.next_to(brace, DOWN)
        etf.shift(RIGHT)

        self.play(
            GrowFromCenter(brace),
            FadeIn(etf, shift=UP)
        )
        self.wait()
        
        # 創建更新函數
        def update_rhs(mob):
            mob.set_value(len(coprime_rects))
        
        self.play(
            ShowIncreasingSubsets(coprime_rects),
            UpdateFromFunc(rhs, update_rhs),
            example_anim,
            rate_func=linear,
            run_time=3,
        )
        self.wait()

        # Show totatives
        totient_group = VGroup(totient, brace, etf)
        for cp, rect in zip(coprimes, coprime_rects):
            cp.add(rect)

        self.play(
            coprimes.animate.arrange(RIGHT, buff=SMALL_BUFF),
            coprimes.animate.set_width(FRAME_WIDTH - 1),
            coprimes.animate.move_to(2 * UP),
            FadeOut(evens),
            FadeOut(div11[1::2]),
            FadeOutAndShiftDown(words_to_keep),
            totient_group.animate.center(),
            totient_group.animate.to_edge(DOWN),
        )

        totatives = Text("``Totatives''")
        totatives.scale(2)
        totatives.set_color(BLUE)
        totatives.move_to(ORIGIN)
        arrows = VGroup(*[
            Arrow(totatives.get_top(), coprime.get_bottom())
            for coprime in coprimes
        ])
        arrows.set_color(WHITE)

        self.play(
            FadeIn(totatives),
            LaggedStartMap(VFadeInThenOut, arrows, run_time=4, lag_ratio=0.05)
        )
        self.wait(2)
