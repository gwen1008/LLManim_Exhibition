# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示在數線上放置多個燈塔，隨著燈塔逐個開啟，光強度指示器顯示累加的光強度，最終趨近於 π²/6 的過程。



from manim import *
class FirstLighthouseScene(PiCreatureScene):
    def construct(self):
        self.remove(self.get_primary_pi_creature())
        self.show_lighthouses_on_number_line()

    def show_lighthouses_on_number_line(self):
        # 常數定義（假設這些常數已在外部定義）
        INDICATOR_RADIUS = 0.5
        OPACITY_FOR_UNIT_INTENSITY = 0.7
        LIGHT_COLOR = YELLOW
        NUM_CONES = 10
        AMBIENT_SCALE = 1.0
        NUM_LEVELS = 10
        AMBIENT_RADIUS = 2.0
        NUM_VISIBLE_CONES = 6
        SWITCH_ON_RUN_TIME = 2.0
        INDICATOR_UPDATE_TIME = 1.0
        FAST_SWITCH_ON_RUN_TIME = 0.5
        FAST_INDICATOR_UPDATE_TIME = 0.2
        
        self.number_line = NumberLine(
            x_range=[0, 5, 1],
            length=8,  # 根據 unit_size=2 和範圍 0-4 計算
            color=WHITE,
            stroke_width=1,
            include_numbers=True,
            numbers_to_include=list(range(1, 5)),
            label_direction=DOWN,
        )
        
        self.number_line_labels = self.number_line.get_number_mobjects()
        self.add(self.number_line, self.number_line_labels)
        self.wait()

        origin_point = self.number_line.number_to_point(0)

        self.default_pi_creature_class = Randolph
        randy = self.get_primary_pi_creature()

        randy.scale(0.5)
        randy.flip()
        right_pupil = randy.pupils[1]
        randy.next_to(origin_point, LEFT, buff=0)
        # 對齊右瞳孔
        randy.align_to(origin_point, RIGHT)

        # 自定義 LightIndicator 類（簡化實現）
        class LightIndicator(VGroup):
            def __init__(self, radius=0.5, opacity_for_unit_intensity=0.7, color=YELLOW, **kwargs):
                super().__init__(**kwargs)
                self.radius = radius
                self.opacity_for_unit_intensity = opacity_for_unit_intensity
                self.foreground = Circle(radius=radius, color=color, fill_opacity=0)
                self.reading = DecimalNumber(0, num_decimal_places=3)
                self.reading.scale(0.8)
                self.add(self.foreground, self.reading)
                
            def set_intensity(self, intensity):
                opacity = intensity * self.opacity_for_unit_intensity
                self.foreground.set_fill(opacity=opacity)
                self.reading.set_value(intensity)
        
        light_indicator = LightIndicator(
            radius=INDICATOR_RADIUS,
            opacity_for_unit_intensity=OPACITY_FOR_UNIT_INTENSITY,
            color=LIGHT_COLOR
        )
        light_indicator.reading.scale(0.8)

        bubble = ThoughtBubble(direction=RIGHT, width=2.5, height=3.5)
        bubble.next_to(randy, LEFT+UP)
        bubble.add_content(light_indicator)
        self.wait()
        self.play(
            randy.change, "wave_2",
            Create(bubble),
            FadeIn(light_indicator)
        )

        light_sources = []

        euler_sum_above = MathTex("1", "+", "{1\\over 4}", 
            "+", "{1\\over 9}", "+", "{1\\over 16}", "+", "{1\\over 25}", "+", "{1\\over 36}")

        for i, term in enumerate(euler_sum_above):
            # 水平對齊刻度
            term.next_to(self.number_line.number_to_point(0.5*i+1), UP, buff=2)
            # 垂直對齊光指示器
            old_y = term.get_center()[1]
            new_y = light_indicator.get_center()[1]
            term.shift([0, new_y - old_y, 0])

        # 自定義 LightSource 類（簡化實現）
        class LightSource(VGroup):
            def __init__(self, opacity_function=None, num_levels=10, radius=2.0, **kwargs):
                super().__init__(**kwargs)
                self.radius = radius
                self.lighthouse = Circle(radius=0.1, color=YELLOW, fill_opacity=1)
                self.ambient_light = Circle(radius=radius, color=YELLOW, fill_opacity=0)
                self.add(self.lighthouse, self.ambient_light)
                
            def move_source_to(self, point):
                self.move_to(point)
                
        def inverse_quadratic(a, b, c):
            # 簡化實現
            return lambda x: 1/(a*x**2 + b*x + c)

        for i in range(1, NUM_CONES+1):
            light_source = LightSource(
                opacity_function=inverse_quadratic(1, AMBIENT_SCALE, 1),
                num_levels=NUM_LEVELS,
                radius=AMBIENT_RADIUS,
            )
            point = self.number_line.number_to_point(i)
            light_source.move_source_to(point)
            light_sources.append(light_source)

        self.wait()
        for ls in light_sources:
            self.add(ls.lighthouse)

        light_indicator.set_intensity(0)

        intensities = np.cumsum(np.array([1./n**2 for n in range(1, NUM_CONES+1)]))
        opacities = intensities * light_indicator.opacity_for_unit_intensity

        # 緩慢開啟可見光錐並更新指示器
        for i, light_source in enumerate(light_sources[:NUM_VISIBLE_CONES]):
            indicator_start_time = 1.0 * (i+1) * SWITCH_ON_RUN_TIME/light_source.radius * 2  # unit_size=2
            indicator_stop_time = indicator_start_time + INDICATOR_UPDATE_TIME
            
            def indicator_rate_func(t):
                start = indicator_start_time / SWITCH_ON_RUN_TIME
                stop = indicator_stop_time / SWITCH_ON_RUN_TIME
                if t < start:
                    return 0
                elif t > stop:
                    return 1
                else:
                    return (t - start) / (stop - start)
            
            self.play(
                light_source.ambient_light.animate.set_fill(opacity=0.3),
                FadeIn(euler_sum_above[2*i], run_time=SWITCH_ON_RUN_TIME,
                    rate_func=indicator_rate_func),
                FadeIn(euler_sum_above[2*i - 1] if i > 0 else euler_sum_above[0], 
                    run_time=SWITCH_ON_RUN_TIME, rate_func=indicator_rate_func),
                light_indicator.reading.animate.set_value(intensities[i]),
                run_time=SWITCH_ON_RUN_TIME
            )
            
            # 更新前景填充
            light_indicator.foreground.set_fill(opacity=opacities[i])

            if i == 0:
                self.wait()
                # 複製指示器用於比較
                light_indicator_copy = light_indicator.copy()
                old_y = light_indicator_copy.get_center()[1]
                new_y = self.number_line.get_center()[1]
                self.play(
                    light_indicator_copy.animate.shift([0, new_y - old_y, 0])
                )

            self.wait()

        self.wait()

        # 快速開啟螢幕外的光錐並更新指示器
        for i, light_source in enumerate(light_sources[NUM_VISIBLE_CONES:NUM_CONES], start=NUM_VISIBLE_CONES):
            indicator_start_time = 0.5 * (i+1) * FAST_SWITCH_ON_RUN_TIME/light_source.radius * 2
            indicator_stop_time = indicator_start_time + FAST_INDICATOR_UPDATE_TIME
            
            def fast_rate_func(t):
                start = indicator_start_time / FAST_SWITCH_ON_RUN_TIME
                stop = indicator_stop_time / FAST_SWITCH_ON_RUN_TIME
                if t < start:
                    return 0
                elif t > stop:
                    return 1
                else:
                    return (t - start) / (stop - start)
            
            self.play(
                light_source.ambient_light.animate.set_fill(opacity=0.3),
                run_time=FAST_SWITCH_ON_RUN_TIME
            )
            
            # 更新指示器讀數
            light_indicator.reading.set_value(intensities[i])
            light_indicator.foreground.set_fill(opacity=opacities[i])

        # 在光指示器中顯示極限值並添加等號
        limit_reading = MathTex("{\\pi^2 \\over 6}")
        limit_reading.move_to(light_indicator.reading)

        equals_sign = MathTex("=")
        equals_sign.next_to(randy, UP)
        old_y = equals_sign.get_center()[1]
        new_y = euler_sum_above.get_center()[1]
        equals_sign.shift([0, new_y - old_y, 0])

        self.play(
            FadeOut(light_indicator.reading),
            FadeIn(limit_reading),
            FadeIn(equals_sign),
        )

        self.wait()
