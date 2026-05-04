# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示兩個角色（藍色和紅色）分別被標註為「你」和「非數學愛好者」，並對一個螢幕矩形做出不同反應的動畫。



from manim import *
class AskWhyYouWouldChooseThisProof(PiCreatureScene):
    def construct(self):
        randy, other = self.pi_creatures
        screen = ScreenRectangle(height=4).to_edge(UP)

        for pi, vect, word in (randy, UP, "You"), (other, LEFT, "Non-math \\\\ enthusiast"):
            arrow = Vector(-vect, color=WHITE)
            arrow.next_to(pi, vect)
            label = Text(word)
            label.next_to(arrow, vect)
            pi.arrow = arrow
            pi.label = label

        for pi, mode in (randy, "hooray"), (other, "tired"):
            self.play(
                GrowArrow(pi.arrow),
                FadeIn(pi.label, shift=RIGHT),
                pi.animate.change(mode),
            )
        self.play(
            randy.animate.change("raise_right_hand", screen),
            other.animate.look_at(screen),
        )
        self.wait()
        self.play(other.animate.change("thinking", screen))
        self.wait(5)

    def create_pi_creatures(self):
        randy = Randolph(color=BLUE_C)
        other = PiCreature(color=RED_D)
        other.flip()
        group = VGroup(randy, other)
        group.arrange(RIGHT, buff=5)
        group.to_edge(DOWN)
        return group
