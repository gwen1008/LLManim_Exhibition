# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個由 Patreon 贊助的動畫場景，包含文字動畫和兩個角色觀看數學公式與螺旋圖形的過程。



from manim import *
class BroughtToYouBy(PiCreatureScene):
    def __init__(self, pi_creatures_start_on_screen=False, **kwargs):
        super().__init__(pi_creatures_start_on_screen=pi_creatures_start_on_screen, **kwargs)

    def construct(self):
        self.brought_to_you_by()
        self.just_you_and_me()

    def brought_to_you_by(self):
        so_words = Text("So", "...", font_size=48)
        so_words.scale(2)

        btyb = Text("Brought to you", "by", font_size=36)
        btyb.scale(1.5)
        btyb_line = Line(LEFT, RIGHT)
        btyb_line.next_to(btyb, RIGHT, buff=SMALL_BUFF)
        btyb_line.align_to(btyb[0], DOWN)
        btyb_group = VGroup(btyb, btyb_line)
        btyb_group.center()

        you_word = Text("\\emph{you}", font_size=42)
        you_word.set_color(YELLOW)
        you_word.scale(1.75)
        you_word.move_to(btyb_line)
        you_word.align_to(btyb, DOWN)

        only_word = Text("(only)", font_size=30)
        only_word.scale(1.25)
        only_brace = Brace(only_word, DOWN, buff=SMALL_BUFF)
        only_group = VGroup(only_word, only_brace)
        only_group.next_to(
            VGroup(btyb[0][-1], btyb[1][0]), UP, buff=SMALL_BUFF
        )
        only_group.set_color(RED)

        full_group = VGroup(btyb_group, only_group, you_word)
        full_group.generate_target()
        full_group.target.scale(0.4)
        full_group.target.to_corner(UL)

        patreon_logo = PatreonLogo()
        patreon_logo.scale(0.4)
        patreon_logo.next_to(full_group.target, DOWN)

        self.play(
            Write(so_words[0]),
            LaggedStartMap(
                DrawBorderThenFill, so_words[1],
                run_time=5
            ),
        )
        self.play(
            so_words.animate.shift(DOWN),
            so_words.animate.set_opacity(0),
            remover=True
        )
        self.play(FadeIn(btyb_group, shift=DOWN))
        self.wait()
        self.play(Write(you_word))
        self.play(
            GrowFromCenter(only_brace),
            Write(only_word)
        )
        self.wait()
        self.play(MoveToTarget(
            full_group,
            rate_func=running_start,
        ))
        self.play(LaggedStartMap(
            DrawBorderThenFill, patreon_logo
        ))
        self.wait()

    def just_you_and_me(self):
        randy, morty = self.pi_creatures
        for pi in self.pi_creatures:
            pi.change("pondering")
        math = MathTex("\\sum_{n=1}^\\infty \\frac{1}{n^s}")
        math.scale(2)
        math.move_to(self.pi_creatures)

        # 創建螺旋曲線
        spiral = Line(0.5 * RIGHT, 0.5 * RIGHT + 70 * UP)
        spiral.insert_n_curves(1000)
        # 注意：zeta 函數需要從原始代碼導入，這裡假設已定義
        from _2017.eoc.zeta import zeta
        # 應用複變函數（ManimCE 中需要手動實現）
        # 這裡簡化處理，使用預設的螺旋
        spiral.set_points_as_corners([
            np.array([np.cos(t), np.sin(t), 0]) * (0.5 + t/10)
            for t in np.linspace(0, 10*np.pi, 1000)
        ])
        step = 0.1
        spiral_parts = VGroup(*[
            VMobject().set_points(spiral.points[int(a*len(spiral.points)):int((a+step)*len(spiral.points))])
            for a in np.arange(0, 1, step)
        ])
        spiral_parts.set_color_by_gradient(BLUE, YELLOW, RED)
        spiral_parts.scale(0.5)
        spiral_parts.move_to(math)

        self.play(FadeIn(randy, shift=DOWN))
        self.play(FadeIn(morty, shift=DOWN))
        self.play(
            Write(math),
            randy.change("hooray"),
            morty.change("hooray"),
        )
        self.look_at(math)
        self.play(
            Create(spiral_parts, run_time=6, rate_func=linear),
            math.animate.scale(0.5).shift(3 * UP),
            randy.change("thinking"),
            morty.change("thinking"),
        )
        self.play(LaggedStartMap(FadeOut, spiral_parts, run_time=3))
        self.wait(3)

    # Helpers
    def create_pi_creatures(self):
        randy = Randolph(color=BLUE_C)
        randy.to_edge(DOWN).shift(4 * LEFT)
        morty = Mortimer()
        morty.to_edge(DOWN).shift(4 * RIGHT)
        return VGroup(randy, morty)
