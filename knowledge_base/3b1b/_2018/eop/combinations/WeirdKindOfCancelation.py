# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示教師與學生場景中，透過分數與名字排列解釋組合數學中的消去概念，並以動畫呈現分子分母的對應關係與消去過程。


from manim import *
import random
import itertools as it

class WeirdKindOfCancelation(TeacherStudentsScene):
    def construct(self):
        fraction = MathTex(
            "{5 \\cdot 4 \\cdot 3", 
            "\\text{ ordered}", "\\text{ triplets}",
            "\\over",
            "1 \\cdot 2 \\cdot 3", "\\text{ orderings \\;\\qquad}}"
        )
        top_numbers, ordered, triplets, frac_line, bottom_numbers, orderings = fraction
        for mob in top_numbers, bottom_numbers:
            mob.set_color_by_gradient(GREEN, YELLOW)
        fraction.next_to(self.teacher.get_corner(UP+LEFT), UP+LEFT)

        names = VGroup(*[TexText(name) for name in [
            "Ali", "Ben", "Cam", "Denis", "Evan"
        ]])
        names.arrange(RIGHT)
        names.to_edge(UP, buff=LARGE_BUFF)
        names.save_state()
        lb, rb = braces = MathTex("\\{\\}")
        braces.scale(2)
        lb.next_to(names, LEFT, SMALL_BUFF)
        rb.next_to(names, RIGHT, SMALL_BUFF)

        chosen_names = VGroup(*random.sample(names, 3))
        chosen_names.generate_target()
        chosen_names.target.arrange(RIGHT)
        chosen_names.target.next_to(top_numbers, UP, MED_LARGE_BUFF)
        for name, name_target in zip(chosen_names, chosen_names.target):
            name.target = name_target

        self.teacher_says("It's like unit cancellation.")
        self.play_student_changes(*["confused"]*3)
        self.play(
            FadeOut(self.teacher.bubble),
            self.teacher.animate.change("raise_right_hand"),
            LaggedStartMap(FadeIn, fraction, run_time=1),
            FadeIn(braces),
            LaggedStartMap(FadeIn, names)
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at=fraction
        )

        # Go through numerators
        for num, name in zip(top_numbers[::2], chosen_names):
            rect = SurroundingRectangle(num)
            name.target.set_color(num.get_color())
            self.play(
                Create(rect),
                Uncreate(rect),
                MoveToTarget(name),
            )
        self.wait(2)

        # Go through denominators
        permutations = list(it.permutations(list(range(3))))[1:]

        self.shuffle(chosen_names, permutations[:2])
        self.play(LaggedStartMap(
            lambda mob: Create(mob) and Uncreate(mob),
            VGroup(*[SurroundingRectangle(num) for num in bottom_numbers[::2]])
        ))
        self.shuffle(chosen_names, permutations[2:])
        self.wait()

        # Show cancelation
        top_cross = Cross(ordered)
        bottom_cross = Cross(orderings)

        self.play(
            Create(top_cross),
            self.teacher.animate.change("maybe"),
        )
        self.play(Create(bottom_cross))
        self.play_student_changes(*["happy"]*3)
        self.wait(3)

    def shuffle(self, mobject, permutations):
        for permutation in permutations:
            self.play(*[
                mobject[i].animate.move_to(mobject[j].get_center()).set(path_arc=PI)
                for i, j in enumerate(permutation)
            ])
