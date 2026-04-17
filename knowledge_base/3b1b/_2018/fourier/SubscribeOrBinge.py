# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個 PiCreature 角色在「訂閱」和「追劇」兩個選項之間的動畫，包含影片圖標從追劇選項向下移動的視覺效果。



from manim import *
class SubscribeOrBinge(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        morty.center().to_edge(DOWN, buff=LARGE_BUFF)
        
        subscribe = Text("Subscribe")
        subscribe.set_color(RED)
        subscribe.next_to(morty, UP+RIGHT)
        
        binge = Text("Binge")
        binge.set_color(BLUE)
        binge.next_to(morty, UP+LEFT)

        videos = VGroup(*[VideoIcon() for x in range(30)])
        colors = it.cycle([BLUE_D, BLUE_E, BLUE_C, GREY_BROWN])
        for video, color in zip(videos, colors):
            video.set_color(color)
        videos.move_to(binge.get_bottom(), UP)
        
        video_anim = LaggedStartMap(
            Succession, videos, 
            lambda v : (
                FadeIn, v,
                ApplyMethod, v.shift, 5*DOWN, {"run_time" : 6},
            ),
            run_time = 10
        )
        
        sub_arrow = Arrow(
            subscribe.get_bottom(),
            Dot().to_corner(DOWN+RIGHT, buff=LARGE_BUFF),
            color = RED
        )

        for word in subscribe, binge:
            word.save_state()
            word.shift(DOWN)
            word.set_opacity(0)

        self.play(
            subscribe.animate.restore(),
            morty.animate.change("raise_left_hand")
        )
        self.play(GrowArrow(sub_arrow))
        self.wait()
        self.play(
            video_anim,
            Succession(
                AnimationGroup(
                    binge.animate.restore(),
                    morty.animate.change("raise_right_hand", binge),
                ),
                Blink(morty),
                morty.animate.change("shruggie", videos),
                Animation(Mobject(), run_time=2),
                Blink(morty),
                Animation(Mobject(), run_time=4)
            )
        )
