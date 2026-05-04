# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示一個 PiCreature 角色旁邊出現測試箭頭和結果文字（患病或健康）的動畫場景。



from manim import *
class TestScene(PiCreatureScene):
    def get_result(self, creature, word, color):
        arrow = self.get_test_arrow()
        test_result = Text(word)  # OldTexText 改為 Text
        test_result.set_color(color)
        test_result.next_to(arrow.get_end(), RIGHT)
        group = VGroup(arrow, test_result)
        group.next_to(creature, RIGHT, aligned_edge=UP)
        return group

    def get_positive_result(self, creature):
        return self.get_result(creature, "Diseased", SICKLY_GREEN)

    def get_negative_result(self, creature):
        return self.get_result(creature, "Healthy", GREEN)

    def get_test_arrow(self):
        arrow = Arrow(
            LEFT, RIGHT,
            color=WHITE,
        )
        word = Text("Test")  # OldTexText 改為 Text
        word.scale(0.8)
        word.next_to(arrow, UP, buff=0)
        arrow.add(word)
        return arrow

    def create_pi_creature(self):
        randy = Randolph()
        randy.next_to(ORIGIN, LEFT)
        return randy
