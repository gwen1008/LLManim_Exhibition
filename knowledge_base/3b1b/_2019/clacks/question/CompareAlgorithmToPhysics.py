# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一個 PiCreature 角色左右手分別指向兩個圖像元素，然後轉為思考泡泡並顯示圓周率數字序列的過程。



from manim import *
class CompareAlgorithmToPhysics(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        # 載入右側圖片
        right_pic = ImageMobject(
            self.get_image_file_path().replace(
                str(self), "PiComputingAlgorithmsAxes"
            )
        )
        right_rect = SurroundingRectangle(right_pic, buff=0, color=WHITE)
        right_pic.add(right_rect)
        right_pic.set_height(3)
        right_pic.next_to(morty, UR)
        right_pic.shift_onto_screen()

        # 左側矩形框
        left_rect = right_rect.copy()
        left_rect.next_to(morty, UL)
        left_rect.shift_onto_screen()

        # 動畫：顯示右側圖片並舉右手
        self.play(
            FadeIn(right_pic, shift=DOWN),
            morty.animate.change("raise_right_hand"),
        )
        self.wait()
        # 動畫：顯示左側矩形並舉左手
        self.play(
            FadeIn(left_rect, shift=DOWN),
            morty.animate.change("raise_left_hand"),
        )
        self.wait()

        # 圓周率數字序列
        digits = MathTex("3.141592653589793238462643383279502884197...")
        digits.set_width(FRAME_WIDTH - 1)
        digits.to_edge(UP)
        
        # 動畫：移除圖片和矩形，顯示思考泡泡和數字序列
        self.play(
            FadeOut(right_pic, shift=5 * RIGHT),
            FadeOut(left_rect),
            PiCreatureBubbleIntroduction(
                morty, "This doesn't seem \\\\ like me...",
                bubble_type=ThoughtBubble,
                bubble_config={"direction": LEFT},
                target_mode="pondering",
                look_at=left_rect,
            ),
            LaggedStart(
                *[FadeIn(d, shift=LEFT) for d in digits],
                run_time=5,
                lag_ratio=0.2,
            )
        )
        self.blink()
        self.wait()
        self.play(morty.animate.change("confused", left_rect))
        self.wait(5)

    def create_pi_creature(self):
        return Mortimer().flip().to_edge(DOWN)
