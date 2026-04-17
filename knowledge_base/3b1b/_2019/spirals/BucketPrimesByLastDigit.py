# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示將質數按最後一位數字分組，並以動態長條圖顯示各組比例的過程。



from manim import *
class BucketPrimesByLastDigit(Scene):
    def __init__(
        self,
        bar_colors=[YELLOW, BLUE],
        mod=10,
        max_n=10000,
        n_to_animate=20,
        n_to_show=1000,
        x_label_scale_factor=1,
        x_axis_label="Last digit",
        bar_width=0.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.bar_colors = bar_colors
        self.mod = mod
        self.max_n = max_n
        self.n_to_animate = n_to_animate
        self.n_to_show = n_to_show
        self.x_label_scale_factor = x_label_scale_factor
        self.x_axis_label = x_axis_label
        self.bar_width = bar_width

    def construct(self):
        self.add_axes()
        self.add_bars()
        self.bucket_primes()

    def add_axes(self):
        mod = self.mod

        axes = Axes(
            x_range=[0, mod + 0.5, 1],
            y_range=[0, 100, 25],
            x_length=10,
            y_length=5.5,
            axis_config={
                "include_tip": False,
            },
            x_axis_config={
                "unit_size": 10 / mod,
            },
            y_axis_config={
                "unit_size": 0.055,
                "tick_frequency": 12.5,
            },
        )

        x_labels = VGroup()
        for x in range(mod):
            digit = Integer(x)
            digit.scale(self.x_label_scale_factor)
            digit.next_to(axes.c2p(x + 1, 0), DOWN, buff=MED_SMALL_BUFF)
            x_labels.add(digit)
        self.modify_x_labels(x_labels)
        x_labels.set_color_by_gradient(*self.bar_colors)
        axes.add(x_labels)
        axes.x_labels = x_labels

        y_labels = VGroup()
        for y in range(25, 125, 25):
            label = Integer(y)
            label.add(Text("%").scale(0.7).next_to(label, RIGHT, buff=0.1))
            label.next_to(axes.c2p(0, y), LEFT, buff=MED_SMALL_BUFF)
            y_labels.add(label)
        axes.add(y_labels)

        x_axis_label = Text(self.x_axis_label)
        x_axis_label.next_to(axes.x_axis.get_end(), RIGHT, buff=MED_LARGE_BUFF)
        axes.add(x_axis_label)

        y_axis_label = Text("Proportion")
        y_axis_label.next_to(axes.y_axis.get_end(), UP, buff=MED_LARGE_BUFF)
        axes.add(y_axis_label)

        axes.center()
        axes.set_width(FRAME_WIDTH - 1)
        axes.to_edge(DOWN)

        self.axes = axes
        self.add(axes)

    def add_bars(self):
        axes = self.axes
        mod = self.mod

        count_trackers = Group(*[
            ValueTracker(0)
            for x in range(mod)
        ])

        bars = VGroup()
        for x in range(mod):
            bar = Rectangle(
                height=1,
                width=self.bar_width,
                fill_opacity=1,
            )
            bar.bottom = axes.c2p(x + 1, 0)
            bars.add(bar)
        bars.set_color_by_gradient(*self.bar_colors)
        bars.set_stroke(WHITE, 1)

        def update_bars(bars):
            values = [ct.get_value() for ct in count_trackers]
            total = sum(values)
            if total == 0:
                props = [0 for x in range(mod)]
            elif total < 1:
                props = values
            else:
                props = [value / total for value in values]

            for bar, prop in zip(bars, props):
                bar.set_height(
                    max(
                        1e-5,
                        100 * prop * axes.y_axis.unit_size,
                    ),
                    stretch=True
                )
                bar.move_to(bar.bottom, DOWN)

        bars.add_updater(update_bars)

        self.add(count_trackers)
        self.add(bars)

        self.bars = bars
        self.count_trackers = count_trackers

    def bucket_primes(self):
        bars = self.bars
        count_trackers = self.count_trackers

        max_n = self.max_n
        n_to_animate = self.n_to_animate
        n_to_show = self.n_to_show
        mod = self.mod

        # 假設 read_in_primes 函數存在，返回質數列表
        # 這裡用一個簡單的質數生成器替代
        def generate_primes(limit):
            primes = []
            for num in range(2, limit + 1):
                is_prime = True
                for p in primes:
                    if p * p > num:
                        break
                    if num % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(num)
            return primes

        primes_list = generate_primes(max_n)
        
        primes = VGroup(*[
            Integer(prime).scale(2).to_edge(UP, buff=LARGE_BUFF)
            for prime in primes_list[:n_to_show + 1]
        ])

        arrow = Arrow(ORIGIN, DOWN)
        x_labels = self.axes.x_labels
        rects = VGroup(*[SurroundingRectangle(label) for label in x_labels])
        rects.set_color(RED)

        self.play(FadeIn(primes[0]))
        for i in range(min(n_to_show, len(primes) - 1)):
            p = primes[i]
            np = primes[i + 1]
            d = int(p.get_value()) % mod
            self.add(rects[d])
            if i < n_to_animate:
                self.play(
                    p.animate.scale(0.5).move_to(bars[d].get_top()).set_opacity(0),
                    FadeIn(np),
                    count_trackers[d].animate.set_value(count_trackers[d].get_value() + 1),
                )
                self.remove(p)
            else:
                arrow.next_to(bars[d], UP)
                self.add(arrow)
                self.add(p)
                count_trackers[d].set_value(count_trackers[d].get_value() + 1)
                self.wait(0.1)
                self.remove(p)
            self.remove(rects[d])

    def modify_x_labels(self, labels):
        pass
