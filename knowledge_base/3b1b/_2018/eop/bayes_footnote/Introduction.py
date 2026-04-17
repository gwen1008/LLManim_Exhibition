# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 教師與學生場景，展示貝葉斯定理的疾病範例與直覺之間的對立關係，並引入其他直觀範例進行對比。



from manim import *
class Introduction(TeacherStudentsScene):
    def construct(self):
        self.hold_up_example()
        self.write_counter_intuitive()
        self.comment_on_crazy_results()
        self.put_it_first()
        self.swap_example_order()
        self.other_culprit()

    def hold_up_example(self):
        everyone = self.get_pi_creatures()
        self.teacher.change_mode("raise_right_hand")
        rect = ScreenRectangle()
        rect.set_stroke(YELLOW, 2)
        rect.to_edge(UP)
        randy = Randolph()
        randy.scale(0.7)
        name = Text(r"""
            Bayes' theorem \\
            disease example
        """)
        name.next_to(rect.get_top(), DOWN, SMALL_BUFF)
        randy.next_to(name, DOWN)
        example = VGroup(rect, name, randy)

        self.remove(everyone)
        self.add(name, randy)
        self.play(
            randy.change_mode, "sick",
            randy.set_color, SICKLY_GREEN
        )
        self.play(Create(rect))
        self.play(
            FadeIn(everyone),
            example.animate.scale(0.5),
            example.animate.next_to(self.teacher.get_corner(UP+LEFT), UP),
        )
        self.wait(2)

        self.example = example

    def write_counter_intuitive(self):
        bayes = Text("Bayes")
        arrow = MathTex("\\leftrightarrow")
        intuition = Text("Intuition")

        group = VGroup(bayes, arrow, intuition)
        group.arrange(RIGHT, buff=SMALL_BUFF)
        group.scale(0.8)
        group.next_to(self.example, UP, buff=SMALL_BUFF)
        group.shift_onto_screen()
        cross = VGroup(
            Line(UP+LEFT, DOWN+RIGHT),
            Line(UP+RIGHT, DOWN+LEFT),
        )
        cross.replace(arrow, stretch=True)
        cross.set_stroke(RED, 6)
        group.add(cross)

        self.play(*list(map(FadeIn, [bayes, intuition])))
        self.play(Write(arrow))
        self.play(Create(cross))
        self.play_student_changes(*["confused"]*3)
        self.wait(2)

        self.bayes_to_intuition = group

    def comment_on_crazy_results(self):
        disease_group = VGroup(self.example, self.bayes_to_intuition)
        disease_group.save_state()

        self.teacher_says(
            "Who doesn't love \\\\ crazy results?",
            target_mode="hooray",
            added_anims=[disease_group.animate.to_corner(UP+LEFT)]
        )
        self.wait(2)

        self.disease_group = disease_group

    def put_it_first(self):
        poker_example = self.get_poker_example()
        music_example = self.get_music_example()
        disease_group = self.disease_group

        self.play(
            disease_group.animate.restore(),
            disease_group.animate.to_edge(LEFT),
            RemovePiCreatureBubble(
                self.teacher,
                target_mode="hesitant"
            )
        )
        self.play_student_changes(
            *["pondering"]*3, 
            look_at=disease_group
        )

        poker_example.next_to(self.example, RIGHT)
        music_example.next_to(poker_example, RIGHT)
        examples = VGroup(poker_example, music_example)
        brace = Brace(examples, UP)
        bayes_to_intuition = VGroup(*list(map(Text, [
            "Bayes", "$\\leftrightarrow$", "Intuition"
        ])))
        bayes_to_intuition.arrange(RIGHT, buff=SMALL_BUFF)
        bayes_to_intuition.next_to(brace, UP, SMALL_BUFF)
        check = MathTex("\\checkmark")
        check.set_color(GREEN)
        check.next_to(bayes_to_intuition[1], UP, SMALL_BUFF)

        for example in examples:
            self.play(FadeIn(example))
            self.wait()
        self.play(GrowFromCenter(brace))
        self.play(FadeIn(bayes_to_intuition))
        self.play(Write(check))
        self.wait(2)

        self.intuitive_examples = VGroup(
            examples, brace, bayes_to_intuition, check
        )

    def swap_example_order(self):
        intuitive_examples = self.intuitive_examples
        disease_group = VGroup(
            self.example, self.bayes_to_intuition
        )

        self.play(
            disease_group.animate.next_to(
                self.teacher.get_corner(UP+LEFT), UP
            ),
            disease_group.animate.shift(LEFT),
            intuitive_examples.animate.scale(0.7),
            intuitive_examples.animate.to_corner(UP+LEFT),
            self.teacher.change_mode("sassy")
        )

    def other_culprit(self):
        bayes = self.bayes_to_intuition[0]
        something_else = Text("Something else")
        something_else.set_color(YELLOW)
        something_else.set_height(bayes.get_height())
        something_else.move_to(bayes, RIGHT)
        new_group = VGroup(
            something_else, 
            *self.bayes_to_intuition[1:]
        )

        self.play(bayes.animate.to_edge(UP))
        self.play(Write(something_else))
        self.play(new_group.animate.next_to(self.example, UP, SMALL_BUFF))
        self.play_student_changes(
            "erm", "confused", "hesitant",
            added_anims=[self.teacher.change_mode("happy")]
        )
        self.wait(3)

    #####

    def get_poker_example(self):
        rect = self.get_example_rect()
        values = IntroducePokerHand.CONFIG["community_card_values"]
        community_cards = VGroup(*list(map(PlayingCard, values)))
        community_cards.arrange(RIGHT)
        deck = VGroup(*[
            PlayingCard(turned_over=True)
            for x in range(5)
        ])
        for i, card in enumerate(deck):
            card.shift(i*(0.03*RIGHT + 0.015*DOWN))
        deck.next_to(community_cards, LEFT)
        cards = VGroup(deck, community_cards)
        cards.set_width(rect.get_width() - 2*SMALL_BUFF)
        cards.next_to(rect.get_bottom(), UP, MED_SMALL_BUFF)

        probability = MathTex(
            "P(", "\\text{Flush}", "|", "\\text{High bet}", ")"
        )
        probability.set_color_by_tex("Flush", RED)
        probability.set_color_by_tex("High bet", GREEN)
        probability.scale(0.5)
        probability.next_to(rect.get_top(), DOWN)

        return VGroup(rect, probability, cards)

    def get_music_example(self):
        rect = self.get_example_rect()

        musician = Randolph(mode="soulful_musician")
        musician.left_arm_range = [.36, .45]
        musician.arms = musician.get_arm_copies()
        guitar = musician.guitar = Guitar()
        guitar.move_to(musician)
        guitar.shift(0.31*RIGHT + 0.6*UP)
        musician.add(guitar, musician.arms)
        musician.set_height(0.7*rect.get_height())
        musician.next_to(rect.get_bottom(), UP, SMALL_BUFF)

        probability = MathTex(
            "P(", "\\text{Suck }", "|", "\\text{ Good review}", ")"
        )
        probability.set_color_by_tex("Suck", RED)
        probability.set_color_by_tex("Good", GREEN)
        probability.scale(0.5)
        probability.next_to(rect.get_top(), DOWN)

        return VGroup(rect, musician, probability)

    def get_example_rect(self):
        rect = self.example[0].copy()
        rect.set_color(WHITE)
        return rect
