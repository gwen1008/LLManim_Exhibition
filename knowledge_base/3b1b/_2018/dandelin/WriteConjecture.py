# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個錐線與平面線段長度相等的猜想，包含標題、方程式和兩條線段的動畫繪製過程。



from manim import *
class WriteConjecture(Scene):
    def __init__(
        self,
        image_name="ConjectureLineEquivalenceBigSphere",
        q_coords=1.28 * UP + 0.15 * LEFT,
        circle_point_coords=0.84 * RIGHT + 0.05 * DOWN,
        tangent_point_coords=0.85 * UP + 1.75 * LEFT,
        plane_line_color=GOLD,
        text_scale_factor=0.75,
        shift_plane_word_down=False,
        include_image=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.image_name = image_name
        self.q_coords = q_coords
        self.circle_point_coords = circle_point_coords
        self.tangent_point_coords = tangent_point_coords
        self.plane_line_color = plane_line_color
        self.text_scale_factor = text_scale_factor
        self.shift_plane_word_down = shift_plane_word_down
        self.include_image = include_image

    def construct(self):
        if self.include_image:
            image = ImageMobject(self.image_name)
            image.set_height(config.frame_height)
            self.add(image)

        title = Text("Conjecture:")
        title.to_corner(UR)

        cone_line = Line(self.q_coords, self.circle_point_coords)
        plane_line = Line(self.q_coords, self.tangent_point_coords)
        plane_line.set_color(self.plane_line_color)
        lines = VGroup(cone_line, plane_line)

        cone_line_words = Text("Cone line")
        plane_line_words = Text("Plane line")
        plane_line_words.set_color(self.plane_line_color)
        words = VGroup(cone_line_words, plane_line_words)

        for word in words:
            word.add_to_back(word.copy().set_stroke(BLACK, 5))
            word.in_equation = word.copy()

        equation = VGroup(
            MathTex("||"),
            words[0].in_equation,
            MathTex("||"),
            MathTex("="),
            MathTex("||"),
            words[1].in_equation,
            MathTex("||"),
        )
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        equation.scale(0.75)
        equation.next_to(title, DOWN, MED_LARGE_BUFF)
        equation.shift_onto_screen()
        title.next_to(equation, UP)

        for word, line in zip(words, lines):
            word.scale(self.text_scale_factor)
            word.next_to(ORIGIN, UP, SMALL_BUFF)
            if self.shift_plane_word_down and (word is plane_line_words):
                word.next_to(ORIGIN, DOWN, SMALL_BUFF)
            angle = line.get_angle()
            if abs(angle) > 90 * DEGREES:
                angle += PI
            word.rotate(angle, about_point=ORIGIN)
            word.shift(line.get_center())

        self.play(LaggedStart(
            *[FadeIn(obj, shift=DOWN) for obj in [title, equation]],
            lag_ratio=0.7
        ))
        self.wait()
        for word, line in zip(words, lines):
            self.play(Create(line))
            self.play(Wiggle(line, scale_value=1.1, rotation_angle=0.1 * TAU))
            self.play(ReplacementTransform(
                word.in_equation.copy(), word
            ))
            self.wait()
