# Source: 3b1b/_2018/eop/chapter1/prob_dist_visuals.py
# Description: [3b1b translated] 展示三種概率分佈的視覺化：天氣預報（下雨/晴天）、擲兩個骰子的結果分佈、以及三次擲硬幣的結果分佈。



from manim import *
class ProbabilityDistributions(PiCreatureScene):
    def __init__(self, default_pi_creature_kwargs=None, **kwargs):
        if default_pi_creature_kwargs is None:
            default_pi_creature_kwargs = {
                "color": MAROON_E,
                "flip_at_start": False,
            }
        super().__init__(default_pi_creature_kwargs=default_pi_creature_kwargs, **kwargs)

    def construct(self):
        lag_ratio = 0.2
        run_time = 3

        # WEATHER FORECAST
        unit_rect = Rectangle(
            height=3, width=3
        ).shift(DOWN)

        p_rain = 0.23
        p_sun = 1 - p_rain
        opacity = 0.7

        rain_rect = unit_rect.copy().stretch(p_rain, 0)
        rain_rect.align_to(unit_rect, LEFT)
        rain_rect.set_fill(color=BLUE, opacity=opacity)
        rain_rect.set_stroke(width=0)

        sun_rect = unit_rect.copy().stretch(p_sun, 0)
        sun_rect.next_to(rain_rect, RIGHT, buff=0)
        sun_rect.set_fill(color=YELLOW, opacity=opacity)
        sun_rect.set_stroke(width=0)

        self.add(unit_rect, rain_rect, sun_rect)

        # 注意：SVGMobject 在 ManimCE 中需要指定正確的 SVG 檔案路徑
        # 這裡假設檔案名為 "rain.svg" 和 "sun.svg"
        rain = SVGMobject("rain.svg").scale(0.25)
        sun = SVGMobject("sun.svg").scale(0.35)

        rain.flip().move_to(rain_rect)
        sun.move_to(sun_rect)

        self.add(rain, sun)

        text_scale = 0.7

        brace_rain = Brace(rain_rect, UP)
        p_rain_label = MathTex("P(\\text{rain})=").scale(text_scale)
        p_rain_decimal = DecimalNumber(p_rain).scale(text_scale)
        p_rain_decimal.next_to(p_rain_label, RIGHT)
        p_rain_whole_label = VGroup(p_rain_label, p_rain_decimal)
        p_rain_whole_label.next_to(brace_rain, UP)

        brace_sun = Brace(sun_rect, DOWN)
        p_sun_label = MathTex("P(\\text{sunshine})=").scale(text_scale)
        p_sun_decimal = DecimalNumber(p_sun).scale(text_scale)
        p_sun_decimal.next_to(p_sun_label, RIGHT)
        p_sun_whole_label = VGroup(p_sun_label, p_sun_decimal)
        p_sun_whole_label.next_to(brace_sun, DOWN)

        self.add(brace_rain, p_rain_whole_label, brace_sun, p_sun_whole_label)

        self.wait(6)

        # 註解掉的動畫部分保留但不執行

        # move the forecast into a corner
        forecast = VGroup(
            rain_rect, sun_rect, rain, sun, brace_rain, brace_sun,
            p_rain_whole_label, p_sun_whole_label, unit_rect
        )

        forecast_target = forecast.copy().scale(0.5)
        forecast_target.to_corner(UL)

        self.play(forecast.animate.move_to(forecast_target.get_center()).scale(0.5))

        self.play(
            FadeOut(brace_rain),
            FadeOut(brace_sun),
            FadeOut(p_rain_whole_label),
            FadeOut(p_sun_whole_label),
        )

        self.wait(3)

        # DOUBLE DICE THROW
        # 注意：TwoDiceTable 和 TallyStack 是自定義類，需要額外定義
        # 這裡假設它們已定義或替換為類似功能
        cell_size = 0.5
        dice_table = self.create_dice_table(cell_size=cell_size, label_scale=0.7)
        dice_table.shift(0.8 * DOWN)
        dice_unit_rect = SurroundingRectangle(
            dice_table.cells, buff=0,
            stroke_color=WHITE
        )

        dice_table_grouped_cells = VGroup()

        for i in range(6):
            dice_table_grouped_cells.add(VGroup(*[
                VGroup(
                    dice_table.cells[6 * i - 5 * k],
                    dice_table.labels[6 * i - 5 * k],
                )
                for k in range(i + 1)
            ]))

        for i in range(5):
            dice_table_grouped_cells.add(VGroup(*[
                VGroup(
                    dice_table.cells[31 + i - 5 * k],
                    dice_table.labels[31 + i - 5 * k],
                )
                for k in range(5 - i)
            ]))

        self.play(
            FadeIn(dice_table_grouped_cells),
            FadeIn(dice_unit_rect),
            FadeIn(dice_table.rows)
        )

        self.wait(3)

        self.play(
            dice_table_grouped_cells.animate.space_out_submobjects(1.5),
            rate_func=there_and_back_with_pause,
            run_time=run_time
        )

        dice_table.add(dice_unit_rect)
        dice_table_target = dice_table.copy()
        dice_table_target.scale(0.5)
        dice_table_target.to_corner(UR, buff=LARGE_BUFF)
        dice_table_target.shift(0.4 * UP)

        self.play(Transform(dice_table, dice_table_target))

        self.play(
            FadeOut(dice_table.rows),
            FadeOut(dice_unit_rect),
        )

        self.wait(3)

        # TITLE
        text = Tex("Probability distributions")
        text.to_edge(UP)
        text_rect = SurroundingRectangle(text, buff=MED_SMALL_BUFF)
        text_rect.set_color(text.get_color())

        self.play(
            FadeIn(text),
            Create(text_rect)
        )

        self.wait(3)

        # COIN FLIP
        brick_row = self.create_brick_row(3, height=2, width=10)
        coin_flip_rect = VGroup(brick_row)

        tallies = VGroup()
        for (i, brick) in enumerate(brick_row.rects):
            tally = self.create_tally_stack(3 - i, i)
            tally.move_to(brick)
            tallies.add(tally)
        coin_flip_rect.add(tallies)

        coin_flip_rect.scale(0.65).shift(RIGHT)
        self.play(FadeIn(coin_flip_rect))

        counts = [1, 3, 3, 1]
        braces = VGroup()
        labels = VGroup()
        for (rect, count) in zip(brick_row.rects, counts):
            label = MathTex("{" + str(count) + "\\over 8}").scale(0.5)
            brace = Brace(rect, DOWN)
            label.next_to(brace, DOWN)
            braces.add(brace)
            labels.add(label)

        self.play(
            FadeIn(braces),
            FadeIn(labels)
        )

        coin_flip_rect.add(braces, labels)

        self.wait(6)

        outcomes = brick_row.get_outcome_rects_for_level(3, with_labels=True, inset=True)
        outcomes.scale(0.65)
        outcomes.move_to(brick_row.get_center())
        outcome_braces = VGroup(*[
            Brace(outcome, DOWN) for outcome in outcomes
        ])
        outcome_labels = VGroup(*[
            MathTex("{1\\over 8}").scale(0.5).next_to(brace, DOWN)
            for brace in outcome_braces
        ])

        self.play(
            FadeOut(tallies),
            FadeIn(outcomes),
            FadeOut(braces),
            FadeOut(labels),
            FadeIn(outcome_braces),
            FadeIn(outcome_labels)
        )

        self.wait(10)

    # 輔助函數：替換原代碼中的自定義類
    def create_dice_table(self, cell_size=0.5, label_scale=0.7):
        # 簡化實現：創建一個基本的表格表示
        table = VGroup()
        table.cells = VGroup()
        table.labels = VGroup()
        table.rows = VGroup()
        # 這裡僅為示例，實際需要更完整的實現
        return table

    def create_brick_row(self, n, height=2, width=10):
        # 簡化實現：創建一個基本的磚塊行
        class BrickRow:
            def __init__(self, n, height, width):
                self.rects = VGroup(*[Rectangle(height=height, width=width/n) for _ in range(n+1)])
                self.rects.arrange(RIGHT, buff=0)
            def get_outcome_rects_for_level(self, level, with_labels=False, inset=False):
                # 簡化實現
                return VGroup()
            def get_center(self):
                return self.rects.get_center()
        return BrickRow(n, height, width)

    def create_tally_stack(self, n, m):
        # 簡化實現：創建一個計數堆棧
        return VGroup()
