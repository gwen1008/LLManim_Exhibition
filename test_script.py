from manim import *


class GeneratedScene(Scene):
    """
    Perfect Vertical Addition: 9 + 991 = 1000
    Generated with modular addition template.
    """

    def setup(self):
        """Initialize subtitle area"""
        self.subtitle_area = Text(
            "", 
            font_size=32, 
            font="PingFang TC",
            color=WHITE
        ).to_edge(DOWN, buff=0.4)
        self.add(self.subtitle_area)


    def create_wrapped_subtitle(self, text):
        """Create subtitle for a single sentence"""
        new_sub = Text(
            text, 
            font_size=32, 
            font="PingFang TC", 
            color=WHITE
        ).to_edge(DOWN, buff=0.4)
        
        if new_sub.get_width() > self.camera.frame_width * 0.9:
            new_sub.scale_to_fit_width(self.camera.frame_width * 0.9)
        
        return new_sub

    def update_subtitle(self, text, duration=1.0):
        """Update subtitle instantly"""
        new_sub = self.create_wrapped_subtitle(text)
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.wait(duration)

    def construct(self):
        # ==================== Scene Setup ====================
        self.camera.background_color = BLACK

        # Title
        title = Text("整數加法：9 + 991", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.add(title)
        
        # ==================== Number Construction ====================
        str1 = "9"
        str2 = "991"
        
        # Build number mobjects
        mob1 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str1])
        mob1.arrange(RIGHT, buff=0.2).move_to(UP * 1.0)
        
        mob2 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str2])
        mob2.arrange(RIGHT, buff=0.2)
        mob2.next_to(mob1, DOWN, buff=0.5).align_to(mob1, RIGHT)
        
        plus_sign = MathTex('+', font_size=60, color=BLUE)
        plus_sign.next_to(mob2, LEFT, buff=0.3)
        
        line = Line(
            start=plus_sign.get_left() + LEFT * 0.2,
            end=mob2.get_right() + RIGHT * 0.2,
            color=WHITE
        ).next_to(mob2, DOWN, buff=0.2)
        
        ans_mobs = []
        carry_mobs = []
        
        # ==================== Phase-Based Step Processing ====================
        # Step 0: [intro]
        self.add_sound("media/audio/9+991/step_00.mp3")
        new_sub = self.create_wrapped_subtitle("今天我們要學習整數的直式加法。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.play(
            FadeIn(mob1), FadeIn(mob2),
            Write(plus_sign), Create(line),
            run_time=4.088
        )
        
        # Step 1: [intro]
        self.add_sound("media/audio/9+991/step_01.mp3")
        self.update_subtitle("題目是 9 加 991。", 3.3200000000000003)
        
        # Step 2: [intro]
        self.add_sound("media/audio/9+991/step_02.mp3")
        self.update_subtitle("在開始計算之前，我們要記得兩個數字要靠右對齊，也就是個位對個位、十位對十位，這樣才能正確計算。", 10.664)
        
        # Step 3: [intro]
        self.add_sound("media/audio/9+991/step_03.mp3")
        self.update_subtitle("現在，讓我們從個位數開始，一步一步往左邊計算。", 6.008)
        
        # Step 4: [digit_0_identify]
        self.add_sound("media/audio/9+991/step_04.mp3")
        new_sub = self.create_wrapped_subtitle("首先，我們從個位開始計算。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.play(
            Circumscribe(mob1[0], color=YELLOW), Circumscribe(mob2[2], color=YELLOW),
            run_time=3.9200000000000004
        )
        
        # Step 5: [digit_0_state]
        self.add_sound("media/audio/9+991/step_05.mp3")
        self.update_subtitle("個位上面是 9，下面是 1。", 3.728)
        
        # Step 6: [digit_0_calculate]
        self.add_sound("media/audio/9+991/step_06.mp3")
        self.update_subtitle("我們把它們相加：9 加 1，等於 10。", 4.712)
        
        # Step 7: [digit_0_write_carry]
        self.add_sound("media/audio/9+991/step_07.mp3")
        new_sub = self.create_wrapped_subtitle("因為 10 大於等於 10，所以我們在個位寫下 0，然後把 1 進到十位。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        digit_0 = MathTex('0', font_size=60, color=GREEN)
        digit_0.move_to([mob2[2].get_center()[0], line.get_center()[1] - 0.6, 0])
        carry_0 = MathTex('1', font_size=36, color=RED)
        carry_0.move_to([mob2[1].get_center()[0], mob2.get_top()[1] + 0.3, 0])
        carry_mobs.append(carry_0)
        self.play(
            FadeIn(digit_0, shift=UP * 0.2), Write(carry_0),
            run_time=7.04
        )
        ans_mobs.append(digit_0)
        
        # Step 8: [digit_1_identify]
        self.add_sound("media/audio/9+991/step_08.mp3")
        new_sub = self.create_wrapped_subtitle("接下來計算十位。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.play(
            Circumscribe(mob2[1], color=YELLOW),
            run_time=2.7920000000000003
        )
        
        # Step 9: [digit_1_state]
        self.add_sound("media/audio/9+991/step_09.mp3")
        self.update_subtitle("十位上面是 0，下面是 9。", 3.8240000000000003)
        
        # Step 10: [digit_1_carry_reminder]
        self.add_sound("media/audio/9+991/step_10.mp3")
        self.update_subtitle("別忘了，我們還有從前一位進上來的 1。", 4.5920000000000005)
        
        # Step 11: [digit_1_calculate]
        self.add_sound("media/audio/9+991/step_11.mp3")
        self.update_subtitle("所以現在要算的是：0 加 9 再加 1，等於 10。", 5.6000000000000005)
        
        # Step 12: [digit_1_write_carry]
        self.add_sound("media/audio/9+991/step_12.mp3")
        new_sub = self.create_wrapped_subtitle("因為 10 大於等於 10，所以我們在十位寫下 0，然後把 1 進到百位。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        digit_1 = MathTex('0', font_size=60, color=GREEN)
        digit_1.move_to([mob2[1].get_center()[0], line.get_center()[1] - 0.6, 0])
        carry_1 = MathTex('1', font_size=36, color=RED)
        carry_1.move_to([mob2[0].get_center()[0], mob2.get_top()[1] + 0.3, 0])
        carry_mobs.append(carry_1)
        self.play(
            FadeIn(digit_1, shift=UP * 0.2), Write(carry_1),
            run_time=7.016
        )
        ans_mobs.append(digit_1)
        
        # Step 13: [digit_2_identify]
        self.add_sound("media/audio/9+991/step_13.mp3")
        new_sub = self.create_wrapped_subtitle("接下來計算百位。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.play(
            Circumscribe(mob2[0], color=YELLOW),
            run_time=2.7920000000000003
        )
        
        # Step 14: [digit_2_state]
        self.add_sound("media/audio/9+991/step_14.mp3")
        self.update_subtitle("百位上面是 0，下面是 9。", 3.728)
        
        # Step 15: [digit_2_carry_reminder]
        self.add_sound("media/audio/9+991/step_15.mp3")
        self.update_subtitle("別忘了，我們還有從前一位進上來的 1。", 4.5920000000000005)
        
        # Step 16: [digit_2_calculate]
        self.add_sound("media/audio/9+991/step_16.mp3")
        self.update_subtitle("所以現在要算的是：0 加 9 再加 1，等於 10。", 5.6000000000000005)
        
        # Step 17: [digit_2_write_carry]
        self.add_sound("media/audio/9+991/step_17.mp3")
        new_sub = self.create_wrapped_subtitle("因為 10 大於等於 10，所以我們在百位寫下 0，然後把 1 進到千位。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        digit_2 = MathTex('0', font_size=60, color=GREEN)
        digit_2.move_to([mob2[0].get_center()[0], line.get_center()[1] - 0.6, 0])
        carry_2 = MathTex('1', font_size=36, color=RED)
        carry_2.move_to([mob2[0].get_center()[0] - (3 - 2) * (mob2[0].width + 0.2), mob2.get_top()[1] + 0.3, 0])
        carry_mobs.append(carry_2)
        self.play(
            FadeIn(digit_2, shift=UP * 0.2), Write(carry_2),
            run_time=6.992
        )
        ans_mobs.append(digit_2)
        
        # Step 18: [digit_3_identify]
        self.add_sound("media/audio/9+991/step_18.mp3")
        new_sub = self.create_wrapped_subtitle("最後，我們還有從百位進上來的 1。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.wait(4.376)
        
        # Step 19: [digit_3_write_final_carry]
        self.add_sound("media/audio/9+991/step_19.mp3")
        new_sub = self.create_wrapped_subtitle("所以千位是 1。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        digit_3 = MathTex('1', font_size=60, color=GREEN)
        # Calculate X position: to the left of the leftmost digit
        left_x = mob2[0].get_center()[0] - mob2[0].get_width()/2 - 0.2 - digit_3.get_width()/2
        digit_3.move_to([left_x, line.get_center()[1] - 0.6, 0])
        self.play(
            FadeIn(digit_3, shift=UP * 0.2),
            run_time=2.528
        )
        ans_mobs.append(digit_3)
        
        # Step 20: [conclusion]
        self.add_sound("media/audio/9+991/step_20.mp3")
        ans_mobs.reverse()
        full_answer = VGroup(*ans_mobs)
        answer_box = SurroundingRectangle(full_answer, color=GREEN, buff=0.15)
        new_sub = self.create_wrapped_subtitle("太棒了！我們已經完成了所有位數的計算。")
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.play(
            Create(answer_box),
            run_time=5.456
        )
        
        # Step 21: [conclusion]
        self.add_sound("media/audio/9+991/step_21.mp3")
        self.update_subtitle("讓我們確認一下答案：9 加 991 等於 1000。", 5.336)
        
        # Step 22: [conclusion]
        self.add_sound("media/audio/9+991/step_22.mp3")
        self.update_subtitle("記住，在做直式加法時，一定要記得位數對齊、從右到左計算、還有注意進位，這樣就不會算錯了！", 10.495999999999999)
        
        # Final wait
        self.wait(2)