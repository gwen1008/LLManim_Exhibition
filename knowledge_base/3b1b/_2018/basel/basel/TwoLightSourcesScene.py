# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示兩個光源照射 Pi 生物，並用光強度指示器測量光照強度，最後引入逆畢氏定理的視覺化證明。


from manim import *
import numpy as np

class TwoLightSourcesScene(PiCreatureScene):
    def construct(self):
        MAX_OPACITY = 0.4
        INDICATOR_RADIUS = 0.6
        OPACITY_FOR_UNIT_INTENSITY = 0.5

        morty = self.get_primary_pi_creature()
        morty.scale(0.3).flip()
        right_pupil = morty.pupils[1]
        morty.next_to(ORIGIN, LEFT, buff=0)
        # ManimCE 沒有 submobject_to_align 參數，改用 align_to 手動對齊
        morty.align_to(ORIGIN, RIGHT)
        
        # 定義點 A, B, C, H (假設這些點已在全局定義)
        # 如果沒有定義，我們需要創建它們
        A = np.array([-3, 2, 0])
        B = np.array([3, 2, 0])
        C = np.array([0, -2, 0])
        H = np.array([0, 2, 0])
        
        horizontal = VMobject(stroke_width=1)
        horizontal.set_points_as_corners([C, A])
        vertical = VMobject(stroke_width=1)
        vertical.set_points_as_corners([C, B])
        
        self.play(
            Create(horizontal),
            Create(vertical)
        )
        
        # 創建自定義 LightIndicator 類的替代品
        # 由於 ManimCE 沒有內建的 LightIndicator，我們用一個簡單的圓和文本代替
        indicator_circle = Circle(
            radius=INDICATOR_RADIUS,
            color=LIGHT_COLOR,
            stroke_width=2
        )
        indicator_text = Text("0.00", font_size=24)
        indicator_text.move_to(indicator_circle.get_center())
        indicator = VGroup(indicator_circle, indicator_text)
        indicator.next_to(morty, LEFT)
        
        self.play(
            Write(indicator)
        )
        
        # 創建自定義 LightSource 類的替代品
        # 用簡單的圓形表示光源
        ls1_lighthouse = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        ls1_lighthouse.move_to(A)
        ls1_light = Circle(radius=2, color=YELLOW, fill_opacity=0.1)
        ls1_light.move_to(A)
        
        ls2_lighthouse = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        ls2_lighthouse.move_to(B)
        ls2_light = Circle(radius=2, color=YELLOW, fill_opacity=0.1)
        ls2_light.move_to(B)
        
        self.play(
            FadeIn(ls1_lighthouse),
            FadeIn(ls2_lighthouse),
            FadeIn(ls1_light),
            FadeIn(ls2_light)
        )
        
        # 計算光強度
        distance1 = np.linalg.norm(C - A)
        distance2 = np.linalg.norm(C - B)
        # 簡單的強度計算：與距離平方成反比
        intensity1 = 1 / (distance1 ** 2) if distance1 > 0 else 1
        intensity2 = 1 / (distance2 ** 2) if distance2 > 0 else 1
        total_intensity = intensity1 + intensity2
        
        # 更新指示器文本
        new_text = Text(f"{total_intensity:.2f}", font_size=24)
        new_text.move_to(indicator_circle.get_center())
        
        self.play(
            Transform(indicator_text, new_text)
        )
        
        self.wait()
        
        # 創建第三個光源
        ls3_lighthouse = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        ls3_lighthouse.move_to(np.array([6, 3.5, 0]))
        ls3_light = Circle(radius=2, color=YELLOW, fill_opacity=0.1)
        ls3_light.move_to(ls3_lighthouse.get_center())
        
        new_indicator = indicator.copy()
        self.add(new_indicator)
        self.play(
            indicator.animate.shift(2 * UP)
        )
        
        # 關閉前兩個光源
        self.play(
            FadeOut(ls1_light),
            FadeOut(ls2_light),
            Transform(new_indicator[1], Text("0.00", font_size=24).move_to(new_indicator[0].get_center()))
        )
        
        # 打開第三個光源
        self.play(
            FadeIn(ls3_light),
            FadeIn(ls3_lighthouse),
        )
        
        # 更新指示器函數
        def update_indicator(mobj, dt):
            distance = np.linalg.norm(C - ls3_lighthouse.get_center())
            intensity = 1 / (distance ** 2) if distance > 0 else 1
            new_text = Text(f"{intensity:.2f}", font_size=24)
            new_text.move_to(mobj[0].get_center())
            mobj[1].become(new_text)
        
        new_indicator.add_updater(update_indicator)
        
        self.wait()
        
        # 移動光源
        location = np.array([-3, -2., 0.])
        self.play(ls3_lighthouse.animate.move_to(location), ls3_light.animate.move_to(location))
        location = np.array([6., 1., 0.])
        self.play(ls3_lighthouse.animate.move_to(location), ls3_light.animate.move_to(location))
        location = np.array([5., 2., 0.])
        self.play(ls3_lighthouse.animate.move_to(location), ls3_light.animate.move_to(location))
        closer_location = interpolate(location, C, 0.5)
        self.play(ls3_lighthouse.animate.move_to(closer_location), ls3_light.animate.move_to(closer_location))
        self.play(ls3_lighthouse.animate.move_to(location), ls3_light.animate.move_to(location))
        
        self.play(ls3_lighthouse.animate.move_to(H), ls3_light.animate.move_to(H))
        
        # 繪製幾何圖形並標記
        line_a = VMobject()
        line_a.set_points_as_corners([B, C])
        line_b = VMobject()
        line_b.set_points_as_corners([A, C])
        line_c = VMobject()
        line_c.set_points_as_corners([A, B])
        line_h = VMobject()
        line_h.set_points_as_corners([H, C])
        
        label_a = MathTex("a")
        label_a.next_to(line_a, LEFT, buff=0.5)
        label_b = MathTex("b")
        label_b.next_to(line_b, DOWN, buff=0.5)
        label_h = MathTex("h")
        label_h.next_to(line_h.get_center(), RIGHT, buff=0.5)
        
        self.play(
            Create(line_a),
            Write(label_a)
        )
        
        self.play(
            Create(line_b),
            Write(label_b)
        )
        
        self.play(
            Create(line_c),
        )
        
        self.play(
            Create(line_h),
            Write(label_h)
        )
        
        # 顯示逆畢氏定理
        theorem_location = np.array([3., 2., 0.])
        theorem = MathTex("{1\\over a^2} + {1\\over b^2} = {1\\over h^2}")
        theorem_name = Text("Inverse Pythagorean Theorem")
        buffer = 1.2
        theorem_box = Rectangle(
            width=buffer * theorem.width,
            height=buffer * theorem.height
        )
        
        theorem.move_to(theorem_location)
        theorem_box.move_to(theorem_location)
        theorem_name.next_to(theorem_box, UP)
        
        self.play(
            Write(theorem),
        )
        
        self.play(
            Create(theorem_box),
            Write(theorem_name),
        )
        
        self.wait()
