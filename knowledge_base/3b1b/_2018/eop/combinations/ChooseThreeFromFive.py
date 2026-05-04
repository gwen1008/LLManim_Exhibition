# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示從五個人中選出三人的組合數，透過二進位字串與人物排列的對應關係，說明組合不考慮順序的特性。


from manim import *
import itertools as it
import random

class ChooseThreeFromFive(Scene):
    def __init__(self, n=5, k=3, pi_creature_scale_val=0.3, people_colors=[PURPLE, BLUE, GREEN, GOLD_E, GREY], **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.k = k
        self.pi_creature_scale_val = pi_creature_scale_val
        self.people_colors = people_colors
        
    def construct(self):
        self.create_pi_creatures()
        self.remove(self.people)
        self.show_binary_strings()
        self.add_people()
        self.choose_triplets()
        self.show_association_with_binary(3)
        self.show_association_with_binary(5)
        self.order_doesnt_matter()
        self.that_phrase_is_confusing()
        self.pattern_is_unambiguous()

    def show_binary_strings(self):
        n, k = self.n, self.k
        stack = self.get_stack(self.get_obj1(), self.get_obj2(), n, k, vertical_buff=SMALL_BUFF)
        stack.to_edge(DOWN, buff=LARGE_BUFF)
        equation = MathTex("{%d \\choose %d}"%(n, k), "=", str(self.choose(n, k)))
        equation[0].scale(0.75, about_point=equation[0].get_right())
        equation.next_to(stack, UP)

        for i, line in enumerate(stack):
            num = MathTex(str(i+1))
            num.next_to(stack, UP)
            self.add(line, num)
            self.wait(0.25)
            self.remove(num)
        self.play(
            Write(VGroup(*equation[:-1])),
            ReplacementTransform(num, equation[-1])
        )
        self.wait()

        self.stack = stack
        self.equation = equation

    def add_people(self):
        people = self.people

        names = self.get_names(people)
        braces = self.get_people_braces(people)

        self.play(
            Write(braces),
            LaggedStartMap(FadeIn, people),
            VGroup(self.stack, self.equation).animate.to_edge(RIGHT, LARGE_BUFF)
        )
        self.play(LaggedStartMap(FadeIn, names))

        self.names = names
        self.braces = braces

    def choose_triplets(self):
        movers = VGroup()
        movers.generate_target()
        max_name_width = max([n.get_width() for n in self.names])
        for name_triplet in it.combinations(self.names, 3):
            mover = VGroup(*name_triplet).copy()
            mover.generate_target()
            if hasattr(self, "stack"):
                mover.target.set_height(self.stack[0].get_height())
            for name in mover.target[:2]:
                name[-1].set_fill(opacity=1)
            mover.target.arrange(RIGHT, MED_SMALL_BUFF)
            movers.add(mover)
            movers.target.add(mover.target)
        movers.target.arrange(
            DOWN, buff=SMALL_BUFF,
            aligned_edge=LEFT,
        )
        movers.target.next_to(self.people, DOWN, MED_LARGE_BUFF)
        if hasattr(self, "stack"):
            movers.target.align_to(self.stack, UP)

        self.play(LaggedStartMap(
            MoveToTarget, movers,
            lag_ratio=0.2,
            run_time=4,
        ))
        self.wait()

        self.name_triplets = movers
        
    def show_association_with_binary(self, index):
        people = self.people
        names = self.names
        for mob in [people, names]:
            mob.save_state()
            mob.generate_target()

        line = self.stack[index].copy()
        triplet = self.name_triplets[index]
        triplet.save_state()
        line.generate_target()
        for bit, name in zip(line.target, self.names):
            bit.next_to(name, UP)

        line_rect = SurroundingRectangle(line)
        full_line_rect = SurroundingRectangle(VGroup(line, triplet))
        people_rects = VGroup()
        for pi, name, obj in zip(people.target, names.target, line):
            if "1" in obj.tex_string:
                rect = SurroundingRectangle(VGroup(pi, name))
                people_rects.add(rect)
                pi.change_mode("hooray")
            else:
                pi.set_opacity(0.5)
                name.set_opacity(0.5)

        self.play(Create(line_rect))
        self.play(MoveToTarget(line))
        self.play(
            LaggedStartMap(Create, people_rects),
            MoveToTarget(people),
            MoveToTarget(names),
        )
        self.wait()
        self.play(
            ReplacementTransform(line_rect, full_line_rect),
            triplet.animate.set_color(YELLOW)
        )
        self.wait(2)
        self.play(
            people.restore,
            names.restore,
            triplet.restore,
            FadeOut(line),
            FadeOut(full_line_rect),
            FadeOut(people_rects),
        )

    def order_doesnt_matter(self):
        triplet = self.name_triplets[0].copy()
        triplet.set_fill(opacity=1)
        triplet.next_to(
            self.name_triplets, RIGHT,
            buff=LARGE_BUFF,
            aligned_edge=UP,
        )
        updownarrow = MathTex("\\Updownarrow")
        updownarrow.set_color(YELLOW)
        updownarrow.next_to(triplet, DOWN, SMALL_BUFF)
        permutations = VGroup()
        for indices in it.permutations(list(range(len(triplet)))):
            perm = triplet.copy()
            resorter = VGroup(*[
                perm[i] for i in indices
            ])
            resorter.arrange(RIGHT, MED_SMALL_BUFF)
            resorter.next_to(updownarrow, DOWN)
            permutations.add(perm)

        words = Tex("``Order doesn't matter''")
        words.scale(0.75)
        words.set_color(BLUE)
        words.next_to(permutations, DOWN)

        self.play(ReplacementTransform(
            self.name_triplets[0].copy(), triplet
        ))
        curr_perm = permutations[0]
        self.play(
            ReplacementTransform(triplet.copy(), curr_perm),
            Write(updownarrow)
        )
        for i in range(8):
            new_perm = permutations[i%(len(permutations)-1)+1]
            anims = [
                Transform(
                    curr_perm, new_perm,
                    path_arc=PI,
                )
            ]
            if i == 1:
                self.wait()
            if i == 4:
                anims.append(Write(words, run_time=1))
            self.play(*anims)
        self.play(*[FadeOut(mob) for mob in [triplet, curr_perm, updownarrow]])

        self.order_doesnt_matter_words = words

    def that_phrase_is_confusing(self):
        odm_words = self.order_doesnt_matter_words
        odm_words_outline = VGroup()
        for letter in odm_words:
            mob = VMobject()
            mob.set_points(letter.get_points())
            odm_words_outline.add(mob)
        odm_words_outline.set_fill(opacity=0)
        odm_words_outline.set_stroke(YELLOW, 1)

        line = self.stack[0].copy()

        q_marks = Tex("???")
        q_marks.next_to(odm_words, DOWN)
        q_marks.set_color(YELLOW)

        self.play(
            LaggedStartMap(
                Create, odm_words_outline,
                lag_ratio=0.2,
                run_time=1,
            ),
            LaggedStartMap(
                lambda pi: pi.animate.change("confused", odm_words), self.people
            ),
            LaggedStartMap(FadeIn, q_marks),
        )
        self.play(line.animate.next_to(odm_words, UP))
        for x in range(6):
            line.generate_target()
            resorter = VGroup(*line.target)
            resorter.sort(lambda p: random.random())
            resorter.arrange(RIGHT, buff=SMALL_BUFF)
            resorter.move_to(line)
            self.play(MoveToTarget(line, path_arc=PI))
        self.play(FadeOut(q_marks))

        line.sort(lambda p: p[0])
        words = VGroup(*[Tex(word) for word in ["First", "Second", "Fifth"]])
        words.set_color(YELLOW)
        words.scale(0.75)
        word_arrow_groups = VGroup()
        for i, word in zip([0, 1, 4], words):
            arrow = Vector(0.5*DOWN)
            arrow.set_color(YELLOW)
            arrow.next_to(line[i], UP, SMALL_BUFF)
            word.next_to(arrow, UP, SMALL_BUFF)
            word_arrow_groups.add(VGroup(word, arrow))

        for x in range(2):
            for i in range(len(word_arrow_groups)+1):
                anims = []
                if i > 0:
                    anims.append(FadeOut(word_arrow_groups[i-1]))
                if i < len(word_arrow_groups):
                    anims.append(FadeIn(word_arrow_groups[i]))
                self.play(*anims)
            self.wait()
            word_arrow_groups.submobjects = [
                word_arrow_groups[j]
                for j in (1, 2, 0)
            ]
        self.play(*[FadeOut(mob) for mob in [line, odm_words]])

    def pattern_is_unambiguous(self):
        all_ones = VGroup()
        for line in self.stack:
            ones = VGroup(*[m for m in line if "1" in m.tex_string]).copy()
            ones.set_color(YELLOW)
            all_ones.add(ones)

        self.play(
            LaggedStartMap(
                FadeIn, all_ones,
                lag_ratio=0.2,
                run_time=3,
                rate_func=there_and_back
            ),
            LaggedStartMap(
                lambda pi: pi.animate.change("happy", all_ones), self.people
            )
        )
        self.wait()
        for trip in it.combinations(self.people, 3):
            rects = VGroup(*[SurroundingRectangle(person) for person in trip])
            self.add(rects)
            self.wait(0.3)
            self.remove(rects)
        self.wait()

    ###

    def create_pi_creatures(self):
        people = VGroup(*[
            PiCreature(color=color).scale(self.pi_creature_scale_val)
            for color in self.people_colors
        ])
        people.arrange(RIGHT)
        people.shift(3*LEFT)
        people.to_edge(UP, buff=1.25)
        self.people = people
        return people

    def get_names(self, people):
        names = VGroup(*[
            Tex(name + ",")
            for name in ("Ali", "Ben", "Cam", "Denis", "Evan")
        ])
        for name, pi in zip(names, people):
            name[-1].set_fill(opacity=0)
            name.scale(0.75)
            name.next_to(pi, UP, 2*SMALL_BUFF)
            pi.name = name
        return names

    def get_people_braces(self, people):
        group = VGroup(people, *[pi.name for pi in people])
        lb, rb = braces = MathTex("\\{ \\}")
        braces.scale(2)
        braces.stretch_to_fit_height(1.3*group.get_height())
        lb.next_to(group, LEFT, SMALL_BUFF)
        rb.next_to(group, RIGHT, SMALL_BUFF)
        return braces

    # Helper methods (需要自行實現或從原代碼中提取)
    def get_stack(self, obj1, obj2, n, k, vertical_buff):
        # 這裡需要實現生成二進位字串堆疊的邏輯
        # 由於原代碼中 get_stack 函數未提供，這裡創建一個簡單的替代
        stack = VGroup()
        for i in range(self.choose(n, k)):
            line = VGroup(*[MathTex("1") if j < k else MathTex("0") for j in range(n)])
            line.arrange(RIGHT, buff=SMALL_BUFF)
            stack.add(line)
        stack.arrange(DOWN, buff=vertical_buff)
        return stack
    
    def get_obj1(self):
        return MathTex("1")
    
    def get_obj2(self):
        return MathTex("0")
    
    def choose(self, n, k):
        import math
        return math.comb(n, k)
