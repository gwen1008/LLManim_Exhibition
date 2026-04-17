# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個 PiCreature 角色旁邊出現三行文字項目，分別標示不同媒體的價格，並伴隨角色手勢和表情變化。



from manim import *
class MentionFree(PiCreatureScene):
    def __init__(
        self,
        default_pi_creature_kwargs=None,
        default_pi_creature_start_corner=DOWN,
        **kwargs
    ):
        if default_pi_creature_kwargs is None:
            default_pi_creature_kwargs = {"flip_at_start": False}
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            default_pi_creature_start_corner=default_pi_creature_start_corner,
            **kwargs
        )

    def construct(self):
        morty = self.pi_creature
        morty.shift(RIGHT)

        items = VGroup(
            Text("Movie:", font_size=36).to_edge(LEFT),
            Text("College course:", font_size=36).to_edge(LEFT),
            Text("YouTube video:", font_size=36).to_edge(LEFT),
        )
        # 添加價格部分
        prices = VGroup(
            MathTex(">\\$10.00"),
            MathTex(">\\$1{,}000.00"),
            MathTex("=\\$0.00"),
        )
        
        # 將價格設置為綠色並對齊
        for i, price in enumerate(prices):
            price.set_color(GREEN)
            price.next_to(items[i], RIGHT)
        
        # 組合文字和價格
        for i in range(3):
            items[i] = VGroup(items[i], prices[i])
        
        items.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        items.next_to(morty, UP, LARGE_BUFF)
        
        # 對齊右邊緣
        right_x = morty.get_right()[0]
        for item in items:
            item.shift((right_x - item.get_right()[0]) * RIGHT)

        self.play(
            morty.animate.change("raise_right_hand"),
            FadeIn(items[0], shift=DOWN)
        )
        self.wait()
        self.play(
            FadeIn(items[1], shift=DOWN),
            items[0].animate.shift(UP),
        )
        self.wait()
        self.play(
            items[:2].animate.shift(UP),
            FadeIn(items[2], shift=DOWN),
            morty.animate.change("surprised")
        )
        self.wait(4)
        self.play(
            morty.animate.change("raise_left_hand"),
            Create(Dot(3*LEFT, radius=0))  # VectorizedPoint 替代方案
        )
        self.wait(4)
        self.play(morty.animate.change("gracious"))
        self.wait(4)
