# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 展示一個角色思考一本書，然後顯示書的動機和翻頁效果。



from manim import *
class StrogatzMention(PiCreatureScene):
    def construct(self):
        self.show_book()
        self.show_motives()
        self.show_pages()

    def show_book(self):
        morty = self.pi_creature
        book = ImageMobject("InfinitePowers")
        book.set_height(5)
        book.to_edge(LEFT)

        steve = ImageMobject("Strogatz_by_bricks")
        steve.set_height(5)
        steve.to_edge(LEFT)

        name = Tex("Steven Strogatz")
        name.match_width(steve)
        name.next_to(steve, DOWN)

        self.think(
            "Hmm...many good\\\\lessons here...",
            run_time=1
        )
        self.wait()
        self.play(FadeIn(steve, shift=DOWN))
        self.wait()
        self.play(
            FadeIn(book, shift=DOWN),
            steve.animate.shift(4 * RIGHT),
            RemovePiCreatureBubble(
                morty, target_mode="thinking"
            )
        )
        self.wait(3)
        self.play(
            FadeOut(steve),
            FadeOut(morty),
        )

        self.book = book

    def show_motives(self):
        motives = VGroup(
            Tex("1) Scratch and itch"),
            Tex("2) Make people love math"),
        )
        motives.scale(1.5)
        motives.arrange(
            DOWN, buff=LARGE_BUFF,
            aligned_edge=LEFT,
        )
        motives.move_to(
            Line(
                self.book.get_right(),
                FRAME_WIDTH * RIGHT / 2
            )
        )
        motives.to_edge(UP)

        for motive in motives:
            self.play(FadeIn(motive, shift=DOWN))
            self.wait(2)
        self.play(FadeOut(motives))

    def show_pages(self):
        book = self.book
        pages = Group(*[
            ImageMobject("IP_Sample_Page{}".format(i))
            for i in range(1, 4)
        ])
        for page in pages:
            page.match_height(book)
            page.next_to(book, RIGHT)

        last_page = VectorizedPoint()
        for page in pages:
            self.play(
                FadeOut(last_page),
                FadeIn(page)
            )
            self.wait()
            last_page = page

        self.play(FadeOut(last_page))

    def create_pi_creature(self):
        return Mortimer().to_corner(DR)
