# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個 Q&A 標題和一系列問題列表的淡入淡出動畫。



from manim import *
class MentionQAndA(Scene):
    def construct(self):
        title = Tex("Q\\&A with ", "Ben", "and", "Sridhar\\\\", "at", "Patreon")
        title.set_color_by_tex_to_color_map({
            "Ben": MAROON,
            "Sridhar": YELLOW,
        })
        # 在 ManimCE 中，PatreonLogo 不是內建類別，我們用替代方案
        # 建立一個簡單的文字或形狀來代表 Patreon 標誌
        patreon_logo = Text("Patreon", font_size=36, color=BLUE)
        # 取得 title 中 "Patreon" 文字部分的位置
        patreon_part = title.get_part_by_tex("Patreon")
        if patreon_part:
            patreon_logo.move_to(patreon_part)
        patreon_logo.scale(1.3, about_edge=LEFT)
        patreon_logo.shift(0.5 * SMALL_BUFF * DOWN)
        # 替換 title 中的最後一個元素
        title.submobjects[-1] = patreon_logo

        title.to_edge(UP)
        self.add(title)

        questions = VGroup(*[
            TexText("If you think of the current videos as short stories, \\\\ what is the novel that you want to write?"),
            TexText("How did you get into mathematics?"),
            TexText("What motivated you to join 3b1b?"),
            MathTex("\\vdots"),
        ])
        questions.arrange(DOWN, buff=0.75)
        questions.next_to(title, DOWN, buff=LARGE_BUFF)

        self.play(LaggedStartMap(FadeIn, questions, run_time=3))
        self.wait(2)
        self.play(FadeOut(questions))
        self.wait()
