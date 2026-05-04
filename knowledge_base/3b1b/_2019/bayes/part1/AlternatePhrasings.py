# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示一個 PiCreature 角色思考不同概率表述方式（分數、百分比、小數）的過程，並伴隨視覺元素（人群、概率條、刻板印象人物）的動態變化。



from manim import *
class AlternatePhrasings(PiCreatureScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        randy = self.pi_creature

        phrases = VGroup(
            Text("40 out of 100"),
            MathTex("40\\%"),
            MathTex("0.4"),
            Text("What's more likely$\\dots$"),
        )
        for phrase in phrases:
            phrase.scale(1.5)
            phrase.next_to(randy, RIGHT, buff=LARGE_BUFF)
            phrase.align_to(randy, UP)

        def push_down(phrase):
            phrase.scale(0.8, about_edge=LEFT)
            phrase.shift(1 * DOWN)
            phrase.set_opacity(0.5)
            return phrase

        bubble = randy.get_bubble()
        content_width = 4.5

        # 注意：Person、Steve、Linda 類別需要自行定義或替換
        # 這裡保持原樣，假設這些類別已存在
        people = VGroup(*[Person() for x in range(100)])
        people.arrange_in_grid(n_cols=20)
        people.set_width(content_width)
        people.move_to(bubble.get_bubble_center())
        people.shift(SMALL_BUFF * UP)
        people[:40].set_color(YELLOW)

        # 注意：ProbabilityBar 類別需要自行定義或替換
        bar = ProbabilityBar(0.9999)
        bar.set_width(content_width)
        bar.move_to(people)

        steve = Steve()
        steve.set_height(1)
        steve_words = Text("seems bookish...")
        steve_words.next_to(steve, RIGHT, MED_LARGE_BUFF)
        steve.add(steve_words)

        linda = Linda()
        linda.set_height(1)
        linda_words = Text("seems activist...")
        linda_words.next_to(linda, RIGHT, MED_LARGE_BUFF)
        linda.add(linda_words)

        stereotypes = VGroup(steve, linda)
        stereotypes.arrange(DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
        stereotypes.move_to(people)

        self.play(
            FadeIn(phrases[0], shift=UP),
            randy.animate.change("pondering"),
        )
        self.play(
            DrawBorderThenFill(bubble, lag_ratio=0.1),
            FadeIn(people, lag_ratio=0.1),
            randy.animate.change("thinking", people),
        )
        self.wait()
        self.play(
            FadeIn(phrases[1], shift=UP),
            randy.animate.change("confused", phrases[1]),
            FadeOut(people),
            ApplyFunction(push_down, phrases[0]),
            FadeIn(bar),
        )
        self.play(bar.p_tracker.animate.set_value(0.4))
        bar.clear_updaters()
        self.play(
            FadeIn(phrases[2], shift=UP),
            ApplyFunction(push_down, phrases[:2]),
            FadeOut(bar.percentages),
            randy.animate.change("guilty"),
        )
        self.wait()
        bar.remove(bar.percentages)
        self.play(
            FadeIn(phrases[3], shift=UP),
            ApplyFunction(push_down, phrases[:3]),
            FadeOut(bar),
            FadeIn(stereotypes),
            randy.animate.change("shruggie", stereotypes),
        )
        self.wait(6)
