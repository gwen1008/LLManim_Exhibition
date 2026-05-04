# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示兩個 PiCreature 角色對話，一個邀請學習四元數，另一個困惑並產生思考泡泡，最後顯示時間文字。



from manim import *
class ShareWithFriends(PiCreatureScene):
    def construct(self):
        pi1, pi2 = self.pi_creatures

        # 第一個 PiCreature 說話
        bubble1 = pi1.get_bubble(
            direction=LEFT,
            width=4,
            height=3,
        )
        bubble1.add_content(Text("Come learn about\nquaternions!", font_size=24))
        self.play(
            pi1.change("hooray"),
            pi2.change("confused", run_time=1.5, rate_func=lambda t: smooth(min(1, max(0, (t-0.3)/0.7)))),
            Create(bubble1),
            Write(bubble1.content),
        )
        pi1.look_at(pi2.eyes)
        self.wait()

        # 第二個 PiCreature 的思考泡泡
        bubble2 = ThoughtBubble(
            direction=RIGHT,
            width=4,
            height=4,
        )
        bubble2.pin_to(pi2)
        bubble2_content = Text("What's that, some\nkind of particle?", font_size=24)
        bubble2.add_content(bubble2_content)
        bubble2.resize_to_content()
        bubble2_group = VGroup(bubble2, bubble2_content)
        bubble2_group.shift_onto_screen(buff=SMALL_BUFF)
        
        self.play(
            pi2.look_at(pi1.eyes),
            pi1.look_at(pi2.eyes),
            Create(bubble2),
            Write(bubble2_content),
        )
        self.wait(1)
        
        # 移除第一個泡泡
        self.play(
            FadeOut(bubble1),
            FadeOut(bubble1.content),
            pi1.change("raise_right_hand")
        )
        self.wait()

        # 顯示時間文字
        time_words = Text("Oh man...\n30 minutes", font_size=24)
        time_words.move_to(bubble2_content)
        self.play(
            Animation(Dot().next_to(pi1, UL, LARGE_BUFF)),  # 替代 VectorizedPoint
            pi2.change("sad"),
            FadeOut(bubble2_content, shift=DOWN),
            FadeIn(time_words, shift=DOWN),
        )
        self.wait(7)

    def create_pi_creatures(self):
        pi1 = PiCreature(color=BLUE)
        pi1.to_edge(DOWN)
        pi1.flip()
        pi1.shift(2.5 * RIGHT)
        pi2 = PiCreature(color=RED)
        pi2.to_edge(DOWN)
        pi2.shift(2 * LEFT)
        return [pi1, pi2]
