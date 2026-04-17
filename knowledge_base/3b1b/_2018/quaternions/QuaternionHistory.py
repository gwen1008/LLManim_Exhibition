# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數的歷史，包括點積與叉積的數學表示、哈密頓教學場景、反對四元數的名人引言，以及《愛麗絲夢遊仙境》的瘋狂茶會隱喻。


from manim import *
import random

class QuaternionHistory(Scene):
    def __init__(self, names_and_quotes=None, **kwargs):
        super().__init__(**kwargs)
        if names_and_quotes is None:
            self.names_and_quotes = [
                (
                    "Oliver Heaviside",
                    """\\huge ``As far as the vector analysis I required was
                    concerned, the quaternion was not only not
                    required, but was a positive evil of no
                    inconsiderable magnitude.''"""
                ),
                (
                    "Lord Kelvin",
                    """\\huge ``Quaternions... though beautifully \\\\ ingenious,
                    have been an unmixed evil to those who have
                    touched them in any way, including Clerk Maxwell.''"""
                ),
            ]
        else:
            self.names_and_quotes = names_and_quotes

    def construct(self):
        self.show_dot_product_and_cross_product()
        self.teaching_students_quaternions()
        self.show_anti_quaternion_quote()
        self.mad_hatter()

    def show_dot_product_and_cross_product(self):
        date = MathTex("1843")
        date.scale(2)
        date.to_edge(UP)

        t2c = self.t2c = {
            "x_1": GREEN,
            "x_2": GREEN,
            "y_1": RED,
            "y_2": RED,
            "z_1": BLUE,
            "z_2": BLUE,
        }

        def get_colored_tex_mobject(tex):
            return MathTex(tex, tex_to_color_map=t2c)

        v1, v2 = [
            Matrix([
                ["{}_{}".format(c, i)]
                for c in "xyz"
            ], element_to_mobject=get_colored_tex_mobject)
            for i in (1, 2)
        ]
        dot_rhs = get_colored_tex_mobject(
            "x_1 x_2 + y_1 y_2 + z_1 z_2",
        )
        cross_rhs = Matrix([
            ["y_1 z_2 - z_1 y_2"],
            ["z_1 x_2 - x_1 z_2"],
            ["x_1 y_2 - y_1 x_2"],
        ], element_to_mobject=get_colored_tex_mobject)

        dot_product = VGroup(
            v1.copy(), MathTex("\\cdot").scale(2),
            v2.copy(), MathTex("="),
            dot_rhs
        )
        cross_product = VGroup(
            v1.copy(), MathTex("\\times"),
            v2.copy(), MathTex("="),
            cross_rhs
        )
        for product in dot_product, cross_product:
            product.arrange(RIGHT, buff=2 * SMALL_BUFF)
            product.set_height(1.5)
        dot_product.next_to(date, DOWN, buff=MED_LARGE_BUFF)
        dot_product.to_edge(LEFT, buff=LARGE_BUFF)
        cross_product.next_to(
            dot_product, DOWN,
            buff=MED_LARGE_BUFF,
            aligned_edge=LEFT,
        )

        self.play(FadeIn(dot_product, shift=2 * RIGHT))
        self.play(FadeIn(cross_product, shift=2 * LEFT))
        self.wait()
        self.play(FadeIn(date, shift=DOWN))
        self.play(dot_product.animate.set_opacity(0.3))
        self.play(cross_product.animate.set_opacity(0.3))
        self.wait()
        self.play(
            FadeOut(dot_product, shift=2 * LEFT),
            FadeOut(cross_product, shift=2 * RIGHT),
        )

        self.date = date

    def teaching_students_quaternions(self):
        # Note: ImageMobject is replaced by Image in ManimCE
        # Since we don't have the actual image files, we'll use a placeholder
        hamilton = Square(side_length=4, color=BLUE, fill_opacity=0.5)
        hamilton.set_height(4)
        hamilton.to_corner(UR)
        hamilton.shift(MED_SMALL_BUFF * DOWN)

        colors = color_gradient([BLUE_E, GREY_BROWN, BLUE_B], 7)
        random.shuffle(colors)
        # PiCreature is not available in ManimCE, using circles as placeholders
        students = VGroup(*[
            Circle(radius=0.5, color=color, fill_opacity=0.8)
            for color in colors
        ])
        students.set_height(2)
        students.arrange(RIGHT)
        students.set_width(config.frame_width - hamilton.get_width() - 1)
        students.to_corner(DL)

        equation = MathTex("""
            (x_1 i + y_1 j + z_1 k)
            (x_2 i + y_2 j + z_2 k)
            =
            (-x_1 x_2 - y_1 y_2 - z_1 z_2) +
            (y_1 z_2 - z_1 y_2)i +
            (z_1 x_2 - x_1 z_2)j +
            (x_1 y_2 - y_1 x_2)k
        """, tex_to_color_map=self.t2c)
        equation.set_width(config.frame_width - 1)
        equation.to_edge(UP, buff=MED_SMALL_BUFF)

        images = Group()
        image_labels = VGroup()
        images_with_labels = Group()
        names = ["Peter Tait", "Robert Ball", "Macfarlane Alexander"]
        for name in names:
            # Using squares as placeholder images
            image = Square(side_length=3, color=random.choice([RED, GREEN, BLUE]), fill_opacity=0.5)
            image.set_height(3)
            label = Text(name, font_size=24)
            label.next_to(image, DOWN)
            image.label = label
            image_labels.add(label)
            images.add(image)
            images_with_labels.add(Group(image, label))
        images_with_labels.arrange(RIGHT)
        images_with_labels.next_to(hamilton, LEFT, LARGE_BUFF)
        images_with_labels.shift(MED_LARGE_BUFF * DOWN)
        society_title = Text("Quaternion society", font_size=36)
        society_title.next_to(images, UP, MED_LARGE_BUFF, UP)

        def blink_wait(n_loops):
            for x in range(n_loops):
                # Simplified blink animation
                student = random.choice(students)
                self.play(student.animate.set_opacity(0.3), run_time=0.2)
                self.play(student.animate.set_opacity(0.8), run_time=0.2)
                self.wait(random.random())

        self.play(
            FadeIn(hamilton, shift=DOWN),
            self.date.animate.set_opacity(0),
            run_time=1.5
        )
        self.play(LaggedStart(*[
            FadeIn(student, shift=LEFT) for student in students
        ]))
        self.play(
            LaggedStart(*[
                student.animate.shift(3 * LEFT + 2 * UP)
                for student in students
            ]),
            Write(equation),
        )
        blink_wait(3)
        self.play(
            LaggedStart(*[FadeIn(image, shift=DOWN) for image in images]),
            LaggedStart(*[FadeIn(label, scale=2) for label in image_labels]),
            Write(society_title)
        )
        blink_wait(3)
        self.play(
            FadeOut(hamilton, shift=RIGHT),
            LaggedStart(*[FadeOut(mob, shift=UP) for mob in images_with_labels]),
            FadeOut(students, shift=DOWN),
            FadeOut(society_title),
            run_time=1
        )

        self.equation = equation

    def show_anti_quaternion_quote(self):
        group = self.get_dissenter_images_quotes_and_names()
        images, quotes, names = group
        self.play(
            LaggedStart(*[FadeIn(image, shift=DOWN) for image in images]),
            LaggedStart(*[FadeIn(name, scale=2) for name in names]),
            lag_ratio=0.75,
            run_time=2,
        )
        for quote in quotes:
            self.play(LaggedStart(
                *[FadeIn(part) for part in quote],
                lag_ratio=0.3
            ))
            self.wait()
        self.play(FadeOut(Group(images, quotes, names)))

    def mad_hatter(self):
        title = Text("Lewis Carroll's \"Alice in wonderland\"", font_size=36)
        title.to_edge(UP, buff=LARGE_BUFF)
        author_brace = Brace(title[:len("Lewis Carroll's")], DOWN)
        aka = Text("a.k.a. Mathematician Charles Dodgson", font_size=24)
        aka.set_color(BLUE)
        aka.next_to(author_brace, DOWN)

        quote = Text(
            """``Why, you might just as well say that
            ‘I see what I eat’ is the same thing as
            ‘I eat what I see’!''""",
            font_size=30,
            t2c={
                "I see what I eat": BLUE,
                "I eat what I see": YELLOW,
            }
        )
        quote.to_edge(UP, buff=LARGE_BUFF)

        # Using simple shapes as character placeholders
        hatter = Circle(radius=1, color=RED, fill_opacity=0.8)
        hat = Triangle(color=GREY_D, fill_opacity=0.8)
        hat.set_height(1.25)
        hat.next_to(hatter, UP, buff=-MED_SMALL_BUFF)
        hatter.add(hat)
        hatter.set_height(2)

        hare = Circle(radius=0.75, color=GREY_B, fill_opacity=0.8)
        mouse = Circle(radius=0.5, color=GREY_B, fill_opacity=0.8)

        characters = VGroup(hatter, hare, mouse)
        for mob, p in zip(characters, [UP, DL, DR]):
            mob.move_to(p)
        hare.shift(MED_SMALL_BUFF * LEFT)

        characters.arrange(buff=1.5)
        characters.to_edge(DOWN)

        def change_single_place(char, **kwargs):
            i = characters.submobjects.index(char)
            target = characters[(i + 1) % 3]
            return ApplyMethod(
                char.move_to, target,
                path_arc=-90 * DEGREES,
                **kwargs
            )

        def get_change_places():
            return LaggedStart(*[
                change_single_place(char) for char in characters
            ], lag_ratio=0.6)

        self.play(
            Write(title),
            LaggedStart(*[FadeIn(char, shift=DOWN) for char in characters])
        )
        self.play(
            get_change_places(),
            GrowFromCenter(author_brace),
            FadeIn(aka)
        )
        for x in range(4):
            self.play(get_change_places())
        self.play(
            FadeOut(VGroup(title, author_brace, aka)),
            FadeIn(quote, shift=DOWN),
        )
        self.play(get_change_places())
        self.play(
            get_change_places(),
            FadeOut(characters, run_time=2)
        )
        self.remove(characters)
        self.wait()

    def get_dissenter_images_quotes_and_names(self):
        names_and_quotes = self.names_and_quotes
        images = Group()
        quotes = VGroup()
        names = VGroup()
        images_with_quotes = Group()
        for name, quote_text in names_and_quotes:
            # Using squares as placeholder images
            image = Square(side_length=4, color=random.choice([RED, BLUE]), fill_opacity=0.5)
            image.set_height(4)
            label = Text(name, font_size=24)
            label.next_to(image, DOWN)
            names.add(label)
            quote = Text(
                quote_text,
                font_size=18,
                t2c={
                    "positive evil": RED,
                    "unmixed evil": RED,
                }
            )
            quote.scale(0.3)
            quote.next_to(image, UP)
            images.add(image)
            quotes.add(quote)
            images_with_quotes.add(Group(image, label, quote))

        images_with_quotes.arrange(RIGHT, buff=LARGE_BUFF)
        images_with_quotes.to_edge(DOWN, buff=MED_LARGE_BUFF)
        return Group(images, quotes, names)
