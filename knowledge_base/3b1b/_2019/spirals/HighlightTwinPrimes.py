# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示數線上的質數點與孿生質數之間的紅色弧線標記，並讓數線向左平移以顯示更多數字。



from manim import *
class HighlightTwinPrimes(Scene):
    def construct(self):
        self.add_paper_titles()
        self.show_twin_primes()

    def add_paper_titles(self):
        gpy = Tex(
            "Goldston, Pintz, Yildirim\\\\",
            "2005",
        )
        zhang = Tex("Zhang\\\\2014")

        gpy.move_to(FRAME_WIDTH * LEFT / 4)
        gpy.to_edge(UP)
        zhang.move_to(FRAME_WIDTH * RIGHT / 4)
        zhang.to_edge(UP)

        self.play(LaggedStart(
            *[FadeIn(mob, shift=DOWN) for mob in [gpy, zhang]],
            lag_ratio=0.3,
        ))

    def show_twin_primes(self):
        max_x = 300
        line = NumberLine(
            x_range=[0, max_x, 10],
            length=0.5 * max_x,
            include_numbers=True,
            numbers_to_include=range(10, max_x, 10),
        )
        line.move_to(2.5 * DOWN + 7 * LEFT, LEFT)

        # 假設 read_in_primes 函數會回傳質數列表
        primes = self.read_in_primes(max_x)
        prime_mobs = VGroup(*[
            Integer(p).next_to(line.number_to_point(p), UP)
            for p in primes
        ])
        dots = VGroup(*[Dot(line.number_to_point(p)) for p in primes])

        arcs = VGroup()
        for pm, npm in zip(prime_mobs, prime_mobs[1:]):
            p = pm.get_value()
            np = npm.get_value()
            if np - p == 2:
                angle = 30 * DEGREES
                arc = Arc(
                    start_angle=angle,
                    angle=PI - 2 * angle,
                    color=RED,
                )
                arc.set_width(
                    np.linalg.norm(npm.get_center() - pm.get_center())
                )
                arc.next_to(VGroup(pm, npm), UP, buff=SMALL_BUFF)
                arcs.add(arc)

        dots.set_color(TEAL)
        prime_mobs.set_color(TEAL)

        line.add(dots)

        self.play(
            FadeIn(line, lag_ratio=0.9),
            LaggedStart(*[FadeIn(mob, shift=DOWN) for mob in prime_mobs]),
            run_time=2,
        )
        line.add(prime_mobs)
        self.wait()

        self.play(FadeIn(arcs))
        self.play(
            line.animate.shift(100 * LEFT),
            arcs.animate.shift(100 * LEFT),
            run_time=20,
            rate_func=lambda t: smooth(t, 5)
        )
        self.wait()

    # 由於原代碼未提供 read_in_primes 函數，這裡假設一個簡單的實現
    def read_in_primes(self, max_x):
        # 簡單的質數篩選，僅供示例
        primes = []
        for num in range(2, max_x + 1):
            if all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
                primes.append(num)
        return primes
