# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示數線上的燈塔光源及其亮度變化，並用思想泡泡中的指示器顯示亮度總和趨近於π²/6的過程。


from manim import *
import numpy as np

class FirstLighthouseScene(PiCreatureScene):
    def __init__(self, num_levels=100, opacity_function=None, **kwargs):
        super().__init__(**kwargs)
        self.num_levels = num_levels
        self.opacity_function = opacity_function if opacity_function else lambda x: 1/(1+x**2)
        
    def construct(self):
        self.remove(self.pi_creature)
        self.show_lighthouses_on_number_line()
        self.describe_brightness_of_each()
        self.ask_about_rearrangements()

    def show_lighthouses_on_number_line(self):
        number_line = self.number_line = NumberLine(
            x_range=[0, 6, 1],
            length=10,
            color=WHITE,
            stroke_width=1,
            include_numbers=True,
            numbers_to_include=list(range(1, 6)),
            label_direction=DOWN,
        )
        number_line.shift(DOWN*2)
        self.add(number_line)

        origin_point = number_line.number_to_point(0)

        morty = self.pi_creature
        morty.scale(0.75)
        morty.flip(RIGHT)
        right_pupil = morty.eyes[1]
        morty.next_to(origin_point, LEFT, buff=0)
        morty.align_to(right_pupil, RIGHT)

        NUM_CONES = 100  # 假設的常數
        NUM_VISIBLE_CONES = 5  # 假設的常數
        
        light_sources = VGroup()
        for i in range(1, NUM_CONES+1):
            # 創建簡化的光源表示
            light_source = Dot(
                point=number_line.number_to_point(i),
                color=YELLOW,
                radius=0.1
            )
            light_sources.add(light_source)

        lighthouses = self.lighthouses = VGroup(*[
            Triangle(
                color=WHITE,
                fill_opacity=0.8,
                stroke_width=2
            ).scale(0.3).move_to(ls.get_center())
            for ls in light_sources[:NUM_VISIBLE_CONES+1]
        ])

        morty.save_state()
        morty.scale(3)
        morty.set_opacity(0)
        morty.center()
        self.play(Restore(morty))
        self.play(
            morty.animate.change("pondering"),
            LaggedStart(*[
                FadeIn(lh, scale=0.5)
                for lh in lighthouses
            ], run_time=1)
        )
        
        # 簡化的光源動畫
        ambient_lights = VGroup(*[
            Circle(
                color=YELLOW,
                fill_opacity=0.1,
                stroke_width=0
            ).scale(0.5).move_to(ls.get_center())
            for ls in light_sources
        ])
        
        self.play(LaggedStart(
            *[Create(light) for light in ambient_lights],
            run_time=5,
            lag_ratio=0.1
        ))
        self.wait()

        self.light_sources = light_sources
        self.ambient_lights = ambient_lights

    def describe_brightness_of_each(self):
        number_line = self.number_line
        morty = self.pi_creature
        light_sources = self.light_sources
        lighthouses = self.lighthouses

        # 簡化的亮度指示器
        light_indicator = Circle(
            radius=0.5,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=2
        )
        reading = DecimalNumber(0, num_decimal_places=3)
        reading.scale(0.8)
        reading.move_to(light_indicator)
        light_indicator.add(reading)
        
        NUM_CONES = 100  # 假設的常數
        intensities = np.cumsum(np.array([1./n**2 for n in range(1, NUM_CONES+1)]))
        OPACITY_FOR_UNIT_INTENSITY = 0.3  # 假設的常數
        opacities = intensities * OPACITY_FOR_UNIT_INTENSITY

        bubble = ThoughtBubble()
        bubble.pin_to(morty)
        bubble.add_content(light_indicator)

        euler_sum_above = MathTex(
            "1", "+", 
            r"{1\over 4}", "+", 
            r"{1\over 9}", "+", 
            r"{1\over 16}", "+", 
            r"{1\over 25}", "+", 
            r"{1\over 36}"
        )
        euler_sum_terms = euler_sum_above[::2]
        plusses = euler_sum_above[1::2]

        for i, term in enumerate(euler_sum_above):
            term.next_to(number_line.number_to_point(0.5*i+1), UP, buff=2)
            term.shift(UP*2)

        # 顯示極限值
        limit_reading = MathTex(r"{\pi^2 \over 6}")
        limit_reading.move_to(light_indicator.reading)

        equals_sign = MathTex("=")
        equals_sign.next_to(morty, UP)
        equals_sign.shift(UP*2)

        # 簡化的三角形光線
        eye = morty.eyes[1]
        triangle = Polygon(
            number_line.number_to_point(1),
            eye.get_top(),
            eye.get_bottom(),
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=0.5,
        )

        # 第一個燈塔
        self.play(LaggedStart(*[
            FadeOut(ls) for ls in light_sources[1:]
        ]))
        self.wait()
        
        self.play(Create(triangle))
        for _ in range(4):
            self.play(
                FadeOut(triangle.copy()),
                Create(triangle.copy()),
            )
        self.play(
            FadeOut(triangle),
            Create(bubble),
            FadeIn(light_indicator),
        )
        
        # 更新亮度指示器
        def update_indicator(mob, value):
            mob.reading.set_value(value)
            mob.set_fill(opacity=min(value * OPACITY_FOR_UNIT_INTENSITY, 1))
            
        self.play(
            UpdateFromFunc(light_indicator, lambda m: update_indicator(m, 1)),
            FadeIn(euler_sum_terms[0])
        )
        self.wait(2)

        # 其他燈塔
        ls0 = light_sources[0]
        ls0.save_state()
        
        for i in range(1, 5):
            self.play(
                ls0.animate.move_to(light_sources[i]),
                UpdateFromFunc(light_indicator, lambda m: update_indicator(m, 1./(i+1)**2)),
                FadeIn(euler_sum_terms[i]),
                run_time=3
            )
            self.wait()
            
        self.play(
            Restore(ls0),
            UpdateFromFunc(light_indicator, lambda m: update_indicator(m, 1))
        )

        # 打開所有燈塔
        self.play(
            LaggedStart(*[
                FadeIn(lh, scale=0.5) for lh in lighthouses[1:]
            ]),
            morty.animate.change("hooray"),
        )
        
        self.play(
            LaggedStart(*[
                Create(light) for light in self.ambient_lights[1:]
            ], run_time=5),
            Write(plusses),
            UpdateFromFunc(light_indicator, lambda m: update_indicator(m, np.pi**2/6)),
            morty.animate.change("happy"),
            run_time=5
        )
        self.wait()
        
        self.play(
            FadeOut(light_indicator.reading),
            FadeIn(limit_reading),
            morty.animate.change("confused"),
        )
        self.play(Write(equals_sign))
        self.wait()

    def ask_about_rearrangements(self):
        light_sources = self.light_sources
        origin = self.number_line.number_to_point(0)
        morty = self.pi_creature

        self.play(
            LaggedStart(*[
                Rotate(
                    ls, 
                    angle=(2*np.random.random()-1)*90*DEGREES,
                    about_point=origin
                )
                for ls in light_sources
            ], lag_ratio=0.9, run_time=10),
            morty.animate.change("pondering"),
        )
