# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示海森堡不確定性原理，透過點雲和向量雲的寬度變化，以及位置/動量和時間/頻率之間的對偶關係。



from manim import *
class ThinkOfHeisenbergUncertainty(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        morty.center().to_edge(DOWN).shift(LEFT)

        # 注意：ProbabalisticDotCloud 和 ProbabalisticVectorCloud 不是 ManimCE 內建類別
        # 這裡保留原類別名稱，假設它們是自定義的 Mobject
        dot_cloud = ProbabalisticDotCloud()
        dot_gdw = dot_cloud.gaussian_distribution_wrapper
        dot_gdw.set_width(1)
        dot_gdw.rotate(TAU/8)
        dot_gdw.move_to(FRAME_X_RADIUS*RIGHT/2)

        vector_cloud = ProbabalisticVectorCloud(
            center_func = dot_gdw.get_center
        )
        vector_gdw = vector_cloud.gaussian_distribution_wrapper
        vector_gdw.set_width(0.1)
        vector_gdw.rotate(TAU/8)
        vector_gdw.next_to(dot_gdw, UP+LEFT, buff=LARGE_BUFF)

        time_tracker = ValueTracker(0)
        self.add()
        freq = 1
        continual_anims = [
            always(time_tracker.increment_value, 1/60),  # 替代 always_shift
            dot_gdw.add_updater(
                lambda d: d.set_width(
                    (np.cos(freq*time_tracker.get_value()) + 1.1)/2
                )
            ),
            vector_gdw.add_updater(
                lambda d: d.set_width(
                    (-np.cos(freq*time_tracker.get_value()) + 1.1)/2
                )
            ),
            dot_cloud, vector_cloud
        ]
        self.add(*continual_anims)

        position, momentum, time, frequency = list(map(Text, [
            "Position", "Momentum", "Time", "Frequency"
        ]))
        VGroup(position, time).set_color(BLUE)
        VGroup(momentum, frequency).set_color(YELLOW)
        groups = VGroup()
        for m1, m2 in (position, momentum), (time, frequency):
            arrow = MathTex("\\updownarrow").scale(1.5)
            group = VGroup(m1, arrow, m2)
            group.arrange(DOWN)
            lp, rp = parens = MathTex("\\big(\\big)")
            parens.stretch(1.5, 1)
            parens.match_height(group)
            lp.next_to(group, LEFT, buff=SMALL_BUFF)
            rp.next_to(group, RIGHT, buff=SMALL_BUFF)
            group.add(parens)
            groups.add(group)
        arrow = MathTex("\\Leftrightarrow").scale(2)
        groups.submobjects.insert(1, arrow)
        groups.arrange(RIGHT)
        groups.next_to(morty, UP+RIGHT, buff=LARGE_BUFF)
        groups.shift_onto_screen()

        # 注意：PiCreatureBubbleIntroduction 不是 ManimCE 內建動畫
        # 這裡用替代方式實現
        bubble = ThoughtBubble(
            height=4, width=4, direction=RIGHT
        )
        bubble.pin_to(morty)
        text = Text("Heisenberg\nuncertainty\nprinciple", font_size=24)
        bubble.add_content(text)
        
        self.play(
            morty.change("pondering"),
            Create(bubble),
            Write(text)
        )
        self.wait()
        self.play(morty.change("confused"), dot_gdw.animate)
        self.wait(10)
        self.play(
            VGroup(dot_gdw, vector_gdw).animate.shift(FRAME_X_RADIUS*RIGHT),
            rate_func=rate_functions.rush_into  # 替代 running_start
        )
        self.remove(*continual_anims)
        self.play(
            morty.change("raise_left_hand"),
            FadeIn(groups, lag_ratio=0.5, run_time=3)
        )
        self.wait(2)
