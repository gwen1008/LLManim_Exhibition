# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一系列影片圖標和角色對話泡泡，呈現從單一影片擴展到多個影片並加入思考與提問的動畫過程。



from manim import *
class NextVideo(Scene):
    def construct(self):
        videos = VGroup(*[VideoIcon() for x in range(2)])
        videos.set_height(2)
        for video in videos:
            video.set_color(BLUE)
            video.set_sheen(0.5, UL)
        videos.arrange(RIGHT, buff=2)

        titles = VGroup(
            Text("Here and now"),
            Text("Solution"),
        )
        for title, video in zip(titles, videos):
            title.next_to(video, UP)
            video.add(title)

        dots = Text(".....")
        dots.scale(2)
        dots.move_to(videos)

        mid_words = Text(
            "Patient\nproblem\nsolving"
        )
        mid_words.next_to(dots, DOWN)
        randy = Randolph(height=1)
        randy.next_to(dots, UP, SMALL_BUFF)
        thought_bubble = ThoughtBubble(height=2, width=2, direction=LEFT)
        thought_bubble.set_stroke(width=2)
        thought_bubble.move_to(randy.get_corner(UR), DL)
        speech_bubble = SpeechBubble(height=2, width=2)
        speech_bubble.pin_to(randy)
        speech_bubble.write("What do \n you think?")
        friends = VGroup(
            PiCreature(color=BLUE_E),
            PiCreature(color=BLUE_C),
            Mortimer()
        )
        friends.set_height(1)
        friends.arrange(RIGHT, buff=MED_SMALL_BUFF)
        friends[:2].next_to(randy, LEFT)
        friends[2].next_to(randy, RIGHT)

        self.add(videos[0])
        self.wait()
        self.play(
            TransformFromCopy(videos[0], videos[1]),
        )
        self.play(Write(dots))
        self.wait()
        self.play(
            LaggedStart(
                *[FadeIn(word, shift=UP) for word in mid_words],
                lag_ratio=0.8,
            ),
            randy.animate.change("pondering"),
            FadeIn(randy),
            videos.animate.space_out_submobjects(1.3),
        )
        self.play(Create(thought_bubble))
        self.play(Blink(randy))
        self.play(
            Uncreate(thought_bubble),
            Create(speech_bubble),
            Write(speech_bubble.content),
            randy.animate.change("maybe", friends[0].eyes),
            LaggedStart(*[FadeIn(friend, shift=DOWN) for friend in friends]),
            videos.animate.space_out_submobjects(1.6),
        )
        self.play(
            LaggedStart(
                *[friend.animate.change("pondering") for friend in friends],
                run_time=1,
                lag_ratio=0.7,
            )
        )
        self.play(Blink(friends[2]))
        self.play(friends[0].animate.change("confused"))
        self.wait()
