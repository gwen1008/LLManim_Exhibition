# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示從5人中隨機選取女性人數的機率分佈，透過排列組合視覺化所有可能性並計算二項式係數。


from manim import *
import itertools as it
import random
from math import comb

class ProbabilityOfKWomenInGroupOfFive(Scene):
    def __init__(self, random_seed=0, n_people_per_lineup=5, n_examples=18, item_line_width=0.4, **kwargs):
        super().__init__(**kwargs)
        self.random_seed = random_seed
        self.n_people_per_lineup = n_people_per_lineup
        self.n_examples = n_examples
        self.item_line_width = item_line_width
        
    def construct(self):
        self.ask_question()
        self.show_all_possibilities()
        self.stack_all_choices_by_number_of_women()
        self.go_through_stacks()
        self.remember_this_sensation()
        self.show_answer_to_question()
        self.ask_about_pattern()

    def ask_question(self):
        title = Text("5 randomly chosen people")
        title.to_edge(UP)
        self.add(title)

        lineup_point = 1.5*UP
        prob_words = VGroup(*[
            Text(
                f"Probability of {n} women?"
            ).set_color_by_tex(str(n), YELLOW)
            for n in range(self.n_people_per_lineup+1)
        ])
        prob_words.arrange(DOWN)
        prob_words.next_to(lineup_point, DOWN, buff=MED_LARGE_BUFF)

        def get_lineup():
            lineup = self.get_random_lineup_of_men_and_women()
            lineup.scale(1.5)
            lineup.move_to(lineup_point, DOWN)
            return lineup

        last_lineup = get_lineup()
        self.play(LaggedStart(*[FadeIn(item) for item in last_lineup.items], run_time=1))

        for x in range(self.n_examples):
            lineup = get_lineup()
            anims = [last_lineup.items.animate.set_opacity(0.3)]
            anims += [GrowFromCenter(item) for item in lineup.items]
            if x >= 12 and x-12 < len(prob_words):
                anims.append(FadeIn(prob_words[x-12]))
            self.play(*anims, run_time=0.75)
            self.remove(last_lineup)
            self.add(lineup)
            self.wait(0.25)
            last_lineup = lineup

        self.title = title
        self.prob_words = prob_words
        self.lineup = last_lineup

    def show_all_possibilities(self):
        man, woman = Male(), Female()

        vects = [
            1.5*UP,
            0.65*UP,
            0.25*UP,
            3.5*RIGHT,
            1.5*RIGHT,
        ]
        lineup_groups = VGroup()
        for k in range(6):
            lineup_group = VGroup()
            for tup in it.product(*[[woman, man]]*k):
                lineup = self.get_lineup(*list(tup) + (5-k)*[None])
                lineup.scale(1.4*(0.9)**k)
                lineup.move_to(0.5*DOWN)
                for mob, vect in zip(tup, vects):
                    if mob is woman:
                        lineup.shift(vect)
                    else:
                        lineup.shift(-vect)
                lineup_group.add(lineup)
            lineup_groups.add(lineup_group)

        n_possibilities = MathTex(
            "2 \\cdot", "2 \\cdot", "2 \\cdot", "2 \\cdot", "2",
            "\\text{ Possibilities}"
        )
        n_possibilities.next_to(self.title, DOWN)
        twos = VGroup(*n_possibilities[-2::-1])
        twos.set_color(YELLOW)
        two_anims = [
            ReplacementTransform(
                Dot(twos[0].get_center(), radius=0), 
                twos[0]
            )
        ] + [
            ReplacementTransform(t1.copy(), t2)
            for t1, t2 in zip(twos, twos[1:])
        ]

        curr_lineup_group = lineup_groups[0]
        self.play(
            ReplacementTransform(self.lineup, curr_lineup_group[0]),
            FadeOut(self.prob_words)
        )
        for i, lineup_group in enumerate(lineup_groups[1:]):
            anims = [ReplacementTransform(curr_lineup_group, lineup_group)]
            anims += two_anims[:i+1]
            if i == 0:
                anims.append(FadeIn(n_possibilities[-1]))
            self.remove(twos)
            self.play(*anims)

            men, women = VGroup(), VGroup()
            for lineup in lineup_group:
                item = lineup.items[i]
                if "female" in item.get_tex():
                    women.add(item)
                else:
                    men.add(item)
            for group in men, women:
                self.play(LaggedStart(*[
                    item.animate.shift(MED_SMALL_BUFF*RIGHT)
                    for item in group
                ], lag_ratio=0.9**i, run_time=1))
            self.wait()
            curr_lineup_group = lineup_group
        self.lineups = curr_lineup_group

        eq_32 = MathTex("=", "32")
        eq_32.move_to(twos.get_right())
        eq_32.set_color_by_tex("32", YELLOW)
        self.play(
            n_possibilities[-1].animate.next_to(eq_32, RIGHT),
            twos.animate.next_to(eq_32, LEFT),
            FadeIn(eq_32),
        )
        self.wait()

        n_possibilities.add(*eq_32)
        self.n_possibilities = n_possibilities

    def stack_all_choices_by_number_of_women(self):
        lineups = self.lineups
        stacks = VGroup(*[VGroup() for x in range(6)])
        for lineup in lineups:
            lineup.women = VGroup(*[m for m in lineup.items if "female" in m.get_tex()])
            stacks[len(lineup.women)].add(lineup)
        stacks.generate_target()
        stacks.target.scale(0.75)
        for stack in stacks.target:
            stack.arrange(DOWN, buff=1.5*SMALL_BUFF)
        stacks.target.arrange(
            RIGHT, buff=MED_LARGE_BUFF, aligned_edge=DOWN
        )
        stacks.target.to_edge(DOWN)

        self.play(MoveToTarget(
            stacks, 
            run_time=2,
            path_arc=PI/2
        ))
        self.wait()

        self.stacks = stacks

    def go_through_stacks(self):
        stacks = self.stacks
        n = len(stacks) - 1
        equations = VGroup()
        for k, stack in enumerate(stacks):
            items = VGroup()
            lines = VGroup()
            women = VGroup()
            for lineup in stack:
                items.add(lineup.items)
                lines.add(lineup.lines)
                for item in lineup.items:
                    if "female" in item.get_tex():
                        women.add(item)
            equation = MathTex(
                f"{{{n} \\choose {k}}}",
                "=",
                str(len(stack))
            )
            equation[0].scale(0.6)
            equation.arrange(RIGHT, buff=SMALL_BUFF)
            equation.set_color(YELLOW)
            equation.set_color_by_tex("=", WHITE)
            equation.next_to(stack, UP)
            equations.add(equation)

            self.play(
                items.animate.set_fill(opacity=1),
                lines.animate.set_stroke(width=3, color=WHITE),
                Write(equation, run_time=1)
            )
            self.play(LaggedStart(*[
                Indicate(woman, color=YELLOW)
                for woman in women
            ]))
        self.wait()

        self.equations = equations
        self.numbers = VGroup(*[eq[-1] for eq in equations])

    def remember_this_sensation(self):
        n_possibilities = self.n_possibilities
        n_possibilities_rect = SurroundingRectangle(n_possibilities)
        twos = VGroup(*n_possibilities[:5])
        numbers = self.numbers

        self.play(Create(n_possibilities_rect))
        self.play(LaggedStart(*[
            Indicate(two, color=YELLOW)
            for two in twos
        ]))
        self.play(FadeOut(n_possibilities_rect))
        for number in numbers:
            self.play(Indicate(number, color=PINK, run_time=0.5))
        self.wait()

    def show_answer_to_question(self):
        stacks = self.stacks
        numbers = self.numbers
        n_possibilities = VGroup(
            self.n_possibilities[-1],
            self.n_possibilities[-3]
        )
        n_possibilities_part_to_fade = VGroup(
            self.n_possibilities[-2],
            *self.n_possibilities[:-3]
        )
        total = n_possibilities[-1]
        title = self.title
        n = self.n_people_per_lineup

        self.play(
            FadeOut(title),
            FadeOut(n_possibilities_part_to_fade),
            n_possibilities.animate.to_corner(UR)
        )
        for k, stack, num in zip(it.count(), stacks, numbers):
            rect = SurroundingRectangle(stack)
            num.save_state()
            prob_words = MathTex(
                "P(", "\\#", "\\female", "=", str(k), ")",
                "=", "{\\quad \\over", "32}",
                "\\approx", f"{comb(n, k)/32.0:.3f}"
            )
            prob_words.set_color_by_tex_to_color_map({
                "\\female" : MAROON_B,
                "32" : YELLOW,
            })
            prob_words.to_corner(UL)

            self.play(
                num.animate.next_to(prob_words[7], UP, SMALL_BUFF),
                FadeIn(prob_words)
            )
            self.play(Create(rect))
            self.wait(2)
            self.play(
                num.restore,
                FadeOut(rect),
                FadeOut(prob_words)
            )

    def ask_about_pattern(self):
        question = Text("Where do these \\\\ numbers come from?")
        question.to_edge(UP)
        numbers = self.numbers
        circles = VGroup(*[
            Circle().replace(num, stretch=True).scale(1.5)
            for num in numbers
        ])
        circles.set_color(WHITE)

        self.play(LaggedStart(*[FadeIn(word) for word in question]))
        self.play(LaggedStart(*[
            Create(circle, run_time=0.5) for circle in circles
        ]))
        self.wait(2)

    ######

    def get_random_lineup_of_men_and_women(self):
        man, woman = Male(), Female()
        lineup = self.get_lineup(*[
            woman if random.choice([True, False]) else man
            for y in range(self.n_people_per_lineup)
        ])
        return lineup

    def get_lineup(self, *mobjects, **kwargs):
        buff = kwargs.get("buff", MED_SMALL_BUFF)
        lines = VGroup(*[
            Line(ORIGIN, self.item_line_width*RIGHT)
            for mob in mobjects
        ])
        lines.arrange(RIGHT, buff=buff)
        items = VGroup()
        for line, mob in zip(lines, mobjects):
            item = Dot(radius=0) if mob is None else mob.copy()
            item.next_to(line, UP, buff=SMALL_BUFF)
            items.add(item)
        result = VGroup(lines, items)
        result.lines = lines
        result.items = items
        return result

class Male(MathTex):
    def __init__(self, **kwargs):
        super().__init__("\\male", **kwargs)

class Female(MathTex):
    def __init__(self, **kwargs):
        super().__init__("\\female", **kwargs)
