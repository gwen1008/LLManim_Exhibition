# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示一個直角三角形，從兩個頂點發出的光源照射到對邊的螢幕上，並隨著光源移動到直角頂點時螢幕旋轉縮放的動畫過程。



from manim import *
class IPTScene1(PiCreatureScene):
    def __init__(self, show_detail=True, **kwargs):
        super().__init__(**kwargs)
        self.show_detail = show_detail

    def construct(self):
        SCREEN_SCALE = 0.1
        SCREEN_THICKNESS = 0.2

        # 定義三角形頂點（假設 A, B, C, H 已在全局定義）
        # 注意：原始代碼中 A, B, C, H 未定義，這裡假設它們是預先定義的點
        # 例如：A = LEFT*3, B = RIGHT*3, C = UP*2, H = ORIGIN
        # 由於原始代碼未提供，這裡保留變量名但需要用戶自行定義
        
        # 使用以下代碼進行縮放插入
        if self.show_detail:
            self.camera.frame_width = 0.02 * config.frame_width
            self.camera.frame_height = 0.02 * config.frame_height
            self.camera.frame.move_to(C)
            SCREEN_SCALE = 0.01
            SCREEN_THICKNESS = 0.02

        morty = self.pi_creature
        self.remove(morty)
        morty.scale(0.3).flip()
        right_pupil = morty.pupils[1]
        morty.next_to(C, LEFT, buff=0, aligned_edge=right_pupil.get_center())
        
        if not self.show_detail:
            self.add(morty)

        stroke_width = 6
        line_a = Line(B, C, stroke_width=stroke_width)
        line_b = Line(A, C, stroke_width=stroke_width)
        line_c = Line(A, B, stroke_width=stroke_width)
        line_h = Line(C, H, stroke_width=stroke_width)

        length_a = line_a.get_length()
        length_b = line_b.get_length()
        length_c = line_c.get_length()
        length_h = line_h.get_length()

        label_a = MathTex("a")
        label_a.next_to(line_a, LEFT, buff=0.5)
        label_b = MathTex("b")
        label_b.next_to(line_b, DOWN, buff=0.5)
        label_h = MathTex("h")
        label_h.next_to(line_h.get_center(), RIGHT, buff=0.5)

        self.add(line_a, line_b, line_c, line_h)
        self.add(label_a, label_b, label_h)
        
        if not self.show_detail:
            self.add(morty)

        # 注意：ManimCE 沒有內建的 LightSource 類
        # 這裡用一個圓點和線條模擬光源
        ls1_dot = Dot(B, color=YELLOW, radius=0.1)
        ls1_line = Line(B, C, color=YELLOW, stroke_width=2)
        self.add(ls1_dot, ls1_line)

        if not self.show_detail:
            self.play(FadeIn(ls1_dot))

        self.wait()

        # 添加第一個螢幕
        screen_width_a = SCREEN_SCALE * length_a
        screen_width_b = SCREEN_SCALE * length_b
        screen_width_ap = screen_width_a * length_a / length_c
        screen_width_bp = screen_width_b * length_b / length_c
        screen_width_c = SCREEN_SCALE * length_c

        screen_thickness_a = SCREEN_THICKNESS
        screen_thickness_b = SCREEN_THICKNESS

        screen1 = Rectangle(
            width=screen_width_b,
            height=screen_thickness_b,
            stroke_width=0,
            fill_opacity=1.0,
            color=WHITE
        )
        screen1.move_to(C + screen_width_b/2 * RIGHT + screen_thickness_b/2 * DOWN)
        
        if not self.show_detail:
            self.add(morty)

        self.play(FadeIn(screen1))
        self.add(screen1)

        # 模擬光源追蹤螢幕（簡化實現）
        screen_tracker = Dot(color=RED).move_to(screen1.get_center())
        self.add(screen_tracker)

        if not self.show_detail:
            self.play(FadeIn(ls1_dot))

        # 模擬聚光燈效果
        spotlight1 = Line(B, screen1.get_center(), color=YELLOW, stroke_width=4)
        self.play(
            Create(spotlight1),
            FadeOut(ls1_line)
        )

        # 將光源移動到高度點 H，同時縮放螢幕
        screen1p = screen1.copy()
        screen1pp = screen1.copy()
        angle = np.arccos(length_b / length_c)
        
        screen1p.stretch_to_fit_width(screen_width_bp)
        screen1p.move_to(C + (screen_width_b - screen_width_bp/2) * RIGHT + SCREEN_THICKNESS/2 * DOWN)
        screen1p.rotate(-angle, about_point=C + screen_width_b * RIGHT)
        
        # 移動光源點和聚光燈
        new_spotlight1 = Line(H, screen1p.get_center(), color=YELLOW, stroke_width=4)
        self.play(
            ls1_dot.animate.move_to(H),
            Transform(screen1, screen1p),
            Transform(spotlight1, new_spotlight1)
        )

        # 添加第二個光源和螢幕
        ls2_dot = Dot(A, color=YELLOW, radius=0.1)
        ls2_line = Line(A, C, color=YELLOW, stroke_width=2)
        screen2 = Rectangle(
            width=screen_width_a,
            height=screen_thickness_a,
            stroke_width=0,
            fill_opacity=1.0,
            color=WHITE
        )
        screen2.rotate(-TAU/4)
        screen2.move_to(C + screen_width_a/2 * UP + screen_thickness_a/2 * LEFT)

        self.play(FadeIn(screen2))
        self.add(screen2)

        if not self.show_detail:
            self.add(morty)

        # 第二個光源的追蹤點
        screen_tracker2 = Dot(color=RED).move_to(screen2.get_center())
        self.add(screen_tracker2)

        if not self.show_detail:
            self.play(FadeIn(ls2_dot))

        self.wait()

        # 第二個聚光燈
        spotlight2 = Line(A, screen2.get_center(), color=YELLOW, stroke_width=4)
        self.play(
            Create(spotlight2),
            FadeOut(ls2_line)
        )

        # 移動第二個光源到高度點 H，同時縮放螢幕
        screen2p = screen2.copy()
        screen2pp = screen2.copy()
        angle = np.arccos(length_a / length_c)
        screen2p.stretch_to_fit_height(screen_width_ap)
        screen2p.move_to(C + (screen_width_a - screen_width_ap/2) * UP + screen_thickness_a/2 * LEFT)
        screen2p.rotate(angle, about_point=C + screen_width_a * UP)
        
        new_spotlight2 = Line(H, screen2p.get_center(), color=YELLOW, stroke_width=4)
        self.play(
            ls2_dot.animate.move_to(H),
            Transform(screen2, screen2p),
            Transform(spotlight2, new_spotlight2)
        )

        # 將兩個螢幕變回原始形狀
        self.play(
            Transform(screen1, screen1pp),
            Transform(screen2, screen2pp),
        )
