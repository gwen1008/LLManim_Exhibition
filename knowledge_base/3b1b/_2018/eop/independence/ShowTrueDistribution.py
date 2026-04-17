# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示一個二項分佈圖表，並透過角色情緒變化表達對分佈結果的不滿。


from manim import *
import numpy as np
import itertools as it

class ShowTrueDistribution(PiCreatureScene):
    def construct(self):
        self.force_skipping()

        self.remove(self.randy)
        self.add_title()
        self.show_distributions()
        self.show_emotion()
        self.imagine_score_0()

        self.revert_to_original_skipping_status()
        self.get_angry()

    def add_title(self):
        title = MathTex("P(", "\\text{Correct}", ")", "=", "0.65")
        title.to_edge(UP)
        title.set_color_by_tex("Correct", GREEN)

        self.add(title)
        self.title = title

    def show_distributions(self):
        # 模擬二項分佈函數
        def get_binomial_distribution(n, p):
            from math import comb
            return lambda k: comb(n, k) * (p**k) * ((1-p)**(n-k))
        
        dist = get_binomial_distribution(3, 0.65)
        values = np.array(list(map(dist, list(range(4)))))
        alt_values = values + [0.2, 0, 0, 0.2]
        alt_values /= sum(alt_values)
        
        # 創建條形圖
        chart = BarChart(
            values,
            bar_names=[str(i) for i in range(4)],
            bar_colors=[BLUE, GREEN, YELLOW, RED]
        )
        bars = chart.bars
        old_bars = bars.copy()
        
        arrows = VGroup()
        for bar, old_bar in zip(bars, old_bars):
            for mob, vect in [(bar, RIGHT), (old_bar, LEFT)]:
                mob.generate_target()
                # 調整目標位置和縮放
                corner = mob.get_corner(DOWN + vect)
                mob.target.move_to(corner, aligned_edge=DOWN + vect)
                mob.target.stretch(0.5, 0)
            
            old_bar.target.set_color(average_color(RED_E, BLACK))
            old_bar.target.set_stroke(width=0)
            
            arrow = Arrow(ORIGIN, UP, buff=0, color=GREEN)
            arrow.move_to(bar.get_bottom())
            arrow.shift(3 * UP)
            arrows.add(arrow)
        
        for arrow in arrows[1:3]:
            arrow.rotate(np.pi)
            arrow.set_color(RED)
        
        # 設置漸變色
        arrows.set_color_by_gradient(BLUE, YELLOW)

        self.add(chart)
        self.play(*[MoveToTarget(mob) for mob in it.chain(bars, old_bars)])
        self.play(
            chart.animate.change_bar_values(alt_values),
            *[Create(arrow) for arrow in arrows]
        )
        self.wait(2)

        self.bar_chart = chart
        self.old_bars = old_bars

    def show_emotion(self):
        randy = self.randy

        self.play(FadeIn(randy))
        self.play(randy.animate.change("sad"))
        self.play(Blink(randy))

    def imagine_score_0(self):
        prob_rect = SurroundingRectangle(self.title[-1])
        bar_rect = SurroundingRectangle(VGroup(
            self.bar_chart.bars[0], self.old_bars[0],
            self.bar_chart.bar_labels[0],
        ))

        self.play(Create(prob_rect))
        self.wait()
        self.play(Transform(prob_rect, bar_rect))
        self.wait()
        self.play(FadeOut(bar_rect))

    def get_angry(self):
        randy = self.randy

        self.play(randy.animate.change("angry"))
        self.wait(2)
        self.play(PiCreatureSays(
            randy, "It's not representative!",
            target_mode="pleading",
            bubble_config={"fill_opacity": 1}
        ))
        self.wait(2)

    def create_pi_creature(self):
        self.randy = Randolph()
        self.randy.to_corner(DOWN + LEFT)
        return self.randy
