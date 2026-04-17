# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示三個影片縮圖與傅立葉肖像的動畫，並突顯其中一個影片縮圖。



from manim import *
class RelationToOtherVideos(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_D

    def construct(self):
        # Show three videos
        videos = self.get_video_thumbnails()
        brace = Brace(videos, UP)
        text = Text("Heat equation", font_size=96)  # OldTexText -> Text
        text.next_to(brace, UP)

        self.play(
            LaggedStartMap(
                lambda m: FadeIn(m, shift=LEFT),  # FadeInFrom -> FadeIn with shift
                videos,
                lag_ratio=0.4,
                run_time=2,
            ),
            GrowFromCenter(brace),
            FadeIn(text, shift=DOWN),  # FadeInFromDown -> FadeIn with shift
        )
        self.wait()
        group = Group(text, brace, videos)

        # Show Fourier thinking
        fourier = ImageMobject("Joseph Fourier")
        fourier.set_height(4)
        fourier.to_edge(RIGHT)
        group.generate_target()
        group.target.to_edge(DOWN)
        fourier.align_to(group.target[0], DOWN)
        bubble = ThoughtBubble(
            direction=RIGHT,
            width=3,
            height=2,
            fill_opacity=0.5,
            stroke_color=WHITE,
        )
        bubble[-1].shift(0.25 * DOWN + 0.5 * LEFT)
        bubble[:-1].rotate(20 * DEGREES)
        for mob in bubble[:-1]:
            mob.rotate(-20 * DEGREES)
        bubble.move_to(
            fourier.get_center(), RIGHT
        )
        bubble.shift(LEFT)
        bubble.to_edge(UP, buff=SMALL_BUFF)

        self.play(
            MoveToTarget(group),
            FadeIn(fourier, shift=LEFT)  # FadeIn with shift
        )
        self.play(Write(bubble, run_time=1))
        self.wait()

        # Discount first two
        first_two = videos[:2]
        first_two.generate_target()
        first_two.target.scale(0.5)
        first_two.target.to_corner(DL)
        new_brace = Brace(first_two.target, UP)

        self.play(
            # fourier.scale, 0.8,
            fourier.animate.match_x(new_brace),  # .match_x -> .animate.match_x
            fourier.animate.to_edge(UP),  # .to_edge -> .animate.to_edge
            MoveToTarget(first_two),
            Transform(brace, new_brace),
            text.animate.scale(0.7),  # .scale -> .animate.scale
            text.animate.next_to(new_brace, UP),  # .next_to -> .animate.next_to
            FadeOut(bubble, shift=LEFT),  # FadeOut with shift
        )
        self.play(
            videos[2].animate.scale(1.7),  # .scale -> .animate.scale
            videos[2].animate.to_corner(UR),  # .to_corner -> .animate.to_corner
        )
        self.wait()

    def get_video_thumbnails(self):
        thumbnails = Group(
            ImageMobject("diffyq_part2_thumbnail"),
            ImageMobject("diffyq_part3_thumbnail"),
            ImageMobject("diffyq_part4_thumbnail"),
        )
        for thumbnail in thumbnails:
            thumbnail.set_height(4)
            thumbnail.add(SurroundingRectangle(
                thumbnail,
                color=WHITE,
                stroke_width=2,
                buff=0
            ))
        thumbnails.arrange(RIGHT, buff=LARGE_BUFF)
        thumbnails.set_width(config.frame_width - 1)  # FRAME_WIDTH -> config.frame_width
        return thumbnails
