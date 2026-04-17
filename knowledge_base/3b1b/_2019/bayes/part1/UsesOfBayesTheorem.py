# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示貝葉斯定理公式及其在不同人物（科學家、程式設計師、卡通角色）之間的應用與思考過程，包含概率條的動態變化。



from manim import *
class UsesOfBayesTheorem(Scene):
    def construct(self):
        formula = get_bayes_formula()
        formula.to_corner(UL)
        rhs = formula[7:]

        bubble = ThoughtBubble(direction=RIGHT)
        bubble.set_fill(opacity=0)
        arrow = Vector(RIGHT)
        arrow.next_to(formula, RIGHT, MED_LARGE_BUFF)
        bubble.set_height(2)
        bubble.next_to(arrow, RIGHT, MED_LARGE_BUFF)
        bubble.align_to(formula, UP)
        bar = ProbabilityBar(
            0.1,
            percentage_background_stroke_width=1,
            include_braces=False,
        )
        bar.set_width(0.8 * bubble[-1].get_width())
        bar.move_to(bubble.get_bubble_center())

        scientist = SVGMobject(file_name="scientist")
        programmer = SVGMobject(file_name="programmer")
        randy = Randolph().flip()

        people = VGroup(scientist, programmer, randy)
        people.set_stroke(width=0)
        for person in people:
            person.set_height(2.5)
            if person is not randy:
                person.set_fill(GREY)
                person.set_sheen(0.5, UL)

        people.arrange(RIGHT, buff=2.5)
        # programmer.shift(0.5 * RIGHT)
        people.to_edge(DOWN, buff=LARGE_BUFF)

        self.add(formula)
        self.wait()
        self.play(GrowArrow(arrow))
        self.play(Create(bubble), FadeIn(bar))
        self.play(bar.p_tracker.set_value, 0.8)
        self.wait()

        # Add people
        for person in [scientist, programmer]:
            self.play(FadeIn(person, shift=DOWN))
            rhs_copy = rhs.copy()
            rhs_copy.add_to_back(
                SurroundingRectangle(
                    rhs_copy,
                    fill_color=BLACK,
                    fill_opacity=0.8,
                    stroke_color=WHITE,
                    stroke_width=2,
                )
            )
            rhs_copy.generate_target()
            rhs_copy[0].set_stroke(width=0)
            rhs_copy.target.scale(0.5)
            rhs_copy.target.move_to(person.get_corner(DR))
            self.add(rhs_copy, formula)
            self.play(MoveToTarget(rhs_copy))
            self.wait()
            person.add(rhs_copy)

        self.play(FadeIn(randy, shift=DOWN))
        self.play(randy.animate.change("pondering"))
        self.play(Blink(randy))
        bubble_group = VGroup(bubble, bar)
        self.play(
            bubble_group.animate.scale(1.4),
            bubble_group.animate.move_to(randy.get_corner(UL) + DR),
            randy.animate.look_at(bubble),
            FadeOut(arrow),
        )
        self.wait()
        self.play(Blink(randy))
        self.play(bar.p_tracker.set_value, 0.3, run_time=3)
        self.play(randy.animate.change("thinking"))
        self.play(Blink(randy))
        self.wait()

        self.play(LaggedStart(
            *[FadeOut(mob, shift=DOWN) for mob in [*people, bubble_group]],
            lag_ratio=0.15,
        ))
