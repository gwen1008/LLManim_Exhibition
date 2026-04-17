# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一個包含三個不確定性主題（聲波、都卜勒雷達、量子粒子）的計畫，每個主題都有對應的動畫和勾選標記。



from manim import *
class ShowPlan(PiCreatureScene):
    def construct(self):
        self.add_title()
        words = self.get_words()
        self.play_sound_anims(words[0])
        self.play_doppler_anims(words[1])
        self.play_quantum_anims(words[2])

    def add_title(self):
        title = TexText("The plan")
        title.scale(1.5)
        title.to_edge(UP)
        h_line = Line(LEFT, RIGHT).scale(FRAME_WIDTH / 2)
        h_line.next_to(title, DOWN)
        self.add(title, h_line)

    def get_words(self):
        trips = [
            ("sound waves", "(time vs. frequency)", YELLOW),
            ("Doppler radar", "(distance vs. velocity)", GREEN),
            ("quantum particles", "(position vs. momentum)", BLUE),
        ]
        words = VGroup()
        for topic, tradeoff, color in trips:
            word = TexText("Uncertainty for", topic, tradeoff)
            word[1:].set_color(color)
            word[2].scale(0.75)
            word[2].next_to(word[1], DOWN, buff=1.5 * SMALL_BUFF)
            words.add(word)
        words.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        words.to_edge(LEFT)

        return words

    def play_sound_anims(self, word):
        morty = self.pi_creature
        wave = FunctionGraph(
            lambda x: 0.3 * np.sin(15 * x) * np.sin(0.5 * x),
            x_range=[0, 30],
        )
        wave.next_to(word, RIGHT)
        rect = BackgroundRectangle(wave, fill_opacity=1)
        rect.stretch(2, 1)
        rect.next_to(wave, LEFT, buff=0)
        
        # 替代 always_shift
        wave.add_updater(lambda m, dt: m.shift(LEFT * 5 * dt))
        
        checkmark = self.get_checkmark(word)

        self.add(wave)
        self.add(word)
        self.play(
            Animation(word),
            morty.change, "raise_right_hand", word
        )
        # 手動實現淡入效果
        wave.set_stroke(width=0)
        self.play(
            wave.animate.set_stroke(width=3),
            run_time=2
        )
        self.wait(2)
        
        # 淡出效果
        self.add(checkmark)
        self.play(
            Write(checkmark),
            morty.change, "happy",
            wave.animate.set_stroke(width=0),
        )
        self.wait()

    def play_doppler_anims(self, word):
        morty = self.pi_creature

        # 需要自定義 RadarDish 和 RadarPulse 類
        radar_dish = self.create_radar_dish()
        radar_dish.next_to(word, DOWN, aligned_edge=LEFT)
        target = Square()  # 簡化為正方形
        target.next_to(radar_dish, RIGHT, buff=LARGE_BUFF)
        
        # 替代 always_shift
        target.add_updater(lambda m, dt: m.shift(RIGHT * 1.25 * dt))

        checkmark = self.get_checkmark(word)

        self.add(target)
        self.play(
            Write(word),
            Create(radar_dish),
            FadeIn(target),
            morty.change, "pondering",
            run_time=1
        )
        
        # 簡化脈衝動畫
        pulse = self.create_pulse(radar_dish, target)
        self.add(pulse)
        
        # 簡化追蹤動畫
        for _ in range(5):
            self.play(
                morty.animate.look_at(pulse),
                run_time=0.5
            )
            
        self.play(
            Write(checkmark),
            FadeOut(target),
            FadeOut(radar_dish),
            morty.change, "happy"
        )
        self.wait()

    def play_quantum_anims(self, word):
        morty = self.pi_creature
        
        # 簡化為點雲表示
        dot_cloud = self.create_dot_cloud()
        dot_cloud.next_to(word, DOWN, MED_LARGE_BUFF)
        dot_cloud.rotate(5 * DEGREES)
        dot_cloud.save_state()
        dot_cloud.scale(0)

        checkmark = self.get_checkmark(word)
        ish = TexText("$\\dots$ish")
        ish.next_to(checkmark, RIGHT, -SMALL_BUFF, DOWN)

        self.add(dot_cloud)
        self.play(
            Write(word),
            FadeIn(dot_cloud),
            morty.change, "confused",
        )
        self.play(dot_cloud.animate.restore(), run_time=2)
        self.play(Write(checkmark))
        self.wait()
        self.play(
            Write(ish), 
            morty.change, 'maybe'
        )
        self.wait(6)

    def get_checkmark(self, word):
        checkmark = MathTex("\\checkmark")
        checkmark.set_color(GREEN)
        checkmark.scale(1.25)
        checkmark.next_to(word[1], UP + RIGHT, buff=0)
        return checkmark

    # 輔助方法（需要根據實際需求實現）
    def create_radar_dish(self):
        """創建簡化的雷達天線"""
        dish = Circle(radius=0.5, color=GREEN)
        stand = Rectangle(height=0.3, width=0.1, color=GREEN)
        stand.next_to(dish, DOWN, buff=0)
        return VGroup(dish, stand)

    def create_pulse(self, source, target):
        """創建簡化的脈衝"""
        pulse = Circle(radius=0.1, color=YELLOW, fill_opacity=0.5)
        pulse.move_to(source.get_center())
        return pulse

    def create_dot_cloud(self):
        """創建簡化的點雲"""
        dots = VGroup(*[
            Dot(radius=0.05, color=BLUE) for _ in range(50)
        ])
        dots.arrange_in_grid(rows=5, cols=10, buff=0.1)
        return dots
