# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示歐拉寫下圓周率定義的過程，包含圖片、文字、圓形圖示和圓周展開的動畫。



from manim import *
class EulerWrites628(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_opacity = 1

    def construct(self):
        # 載入圖片
        image = ImageMobject("dalembert_zoom")
        image.set_width(config.frame_width - 1)
        image.to_edge(UP, buff=MED_SMALL_BUFF)
        image.set_opacity(0.85)  # 原 fade(0.15) 的反向
        
        # 綠色矩形裝飾
        rect = Rectangle(
            width=12,
            height=0.5,
            stroke_width=0,
            fill_opacity=0.3,
            fill_color=GREEN,
        )
        rect.insert_n_curves(20)
        rect.apply_function(lambda p: np.array([p[0], p[1] - 0.005*p[0]**2, p[2]]))
        rect.rotate(0.012*TAU)
        rect.move_to(image)
        rect.shift(0.15*DOWN)

        # 文字定義
        words = Tex(
            "``Let", "\\pi", "be the", "circumference", 
            "of a circle whose", "radius = 1''",
            tex_to_color_map={
                "circumference": YELLOW,
                "radius": GREEN,
            }
        )
        words.next_to(image, DOWN)
        pi = words.get_part_by_tex("\\pi").copy()

        # 建立圓形相關物件（簡化版本）
        circle = Circle(radius=1, color=BLUE)
        circle.next_to(words, DOWN, buff=1.25)
        
        radius_line = Line(circle.get_center(), circle.get_right(), color=GREEN)
        one_label = MathTex("1").next_to(radius_line, UP, buff=SMALL_BUFF)
        decimal = MathTex("\\approx 6.283185").next_to(circle, DOWN)
        
        terms = VGroup(circle, radius_line, one_label, decimal)
        
        # 展開的周長
        unwrapped_perimeter = Line(ORIGIN, TAU*RIGHT, color=BLUE)
        unwrapped_perimeter.next_to(circle, DOWN)
        brace = Brace(unwrapped_perimeter, UP, buff=SMALL_BUFF)

        # 周長文字
        perimeter = Tex(
            "\\pi\\epsilon\\rho\\iota\\mu\\epsilon\\tau\\rho\\text{o}\\varsigma",
            "\\text{ (perimeter)}",
            "="
        )
        perimeter.next_to(brace, UP, buff=SMALL_BUFF)
        perimeter[0][0].set_color(GREEN)

        # 動畫序列
        self.play(FadeIn(image, shift=DOWN))
        self.play(
            Write(words),
            GrowFromPoint(rect, rect.point_from_proportion(0.9))
        )
        self.wait()
        
        # 繪製圓形
        self.play(Create(circle))
        self.play(
            Create(radius_line),
            Write(one_label),
            Write(decimal)
        )
        self.wait()
        
        self.play(terms.animate.shift(UP))
        self.play(
            pi.animate.scale(2).shift(DOWN).set_color(GREEN)
        )
        self.wait()
        
        self.play(
            GrowFromCenter(brace),
            circle.animate.set_stroke(YELLOW, 1),
            ReplacementTransform(circle.copy(), unwrapped_perimeter),
            decimal.animate.scale(1.25).next_to(perimeter[-1].get_right(), RIGHT),
            ReplacementTransform(pi, perimeter[0][0]),
            Write(perimeter),
        )
        self.wait()
