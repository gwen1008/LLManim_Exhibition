# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示動量公式 p = hξ 的視覺化推導，包含動量和空間頻率的標籤說明，以及一個向右傳播的波函數動畫，最後有學生對公式提出疑問的互動場景。



from manim import *
class ShowMomentumFormula(Scene):
    def __init__(
        self,
        default_wave_frequency=2,
        dispersion_factor=0.25,
        p_color=BLUE,
        xi_color=YELLOW,
        amplitude=0.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.default_wave_frequency = default_wave_frequency
        self.dispersion_factor = dispersion_factor
        self.p_color = p_color
        self.xi_color = xi_color
        self.amplitude = amplitude

    def construct(self):
        self.introduce_formula()
        self.react_to_claim()

    def introduce_formula(self):
        formula = MathTex("p", "=", "h", "\\xi")
        p, eq, h, xi = formula
        formula.move_to(ORIGIN)
        formula.scale(1.5)

        word_shift_val = 1.75
        p_words = Text("Momentum")
        p_words.next_to(p, UP, buff=LARGE_BUFF).shift(word_shift_val*LEFT)
        p_arrow = Arrow(
            p_words.get_bottom(), p.get_corner(UP+LEFT),
            buff=SMALL_BUFF
        )
        added_p_words = Text("(Classically $m \\times v$)")
        added_p_words.move_to(p_words, DOWN)
        VGroup(p, p_words, added_p_words, p_arrow).set_color(self.p_color)

        xi_words = Text("Spatial frequency")
        added_xi_words = Text("(cycles per unit distance)")
        xi_words.next_to(xi, UP, buff=LARGE_BUFF).shift(word_shift_val*RIGHT)
        xi_words.align_to(p_words, UP)
        xi_arrow = Arrow(
            xi_words.get_bottom(), xi.get_corner(UP+RIGHT), 
            buff=SMALL_BUFF
        )
        added_xi_words.move_to(xi_words, DOWN)
        added_xi_words.align_to(added_p_words, DOWN)
        VGroup(xi, xi_words, added_xi_words, xi_arrow).set_color(self.xi_color)

        axes = Axes(
            x_range=[0, FRAME_WIDTH],
            y_range=[-1, 1],
        )
        axes.center().to_edge(UP, buff=-0.5)
        
        # 創建波函數動畫
        particle = Dot(radius=0.05)
        wave = self.get_wave(axes, particle)
        particle.next_to(wave, LEFT, buff=2)
        
        # 波傳播動畫
        wave_propagation = AnimationGroup(
            particle.animate.move_to(axes.c2p(30, 0)),
            self.get_wave_update_animation(wave, particle),
            run_time=4,
            rate_func=linear,
        )
        
        # 停止的波傳播動畫
        stopped_wave_propagation = AnimationGroup(
            particle.animate.move_to(xi_words.get_bottom()),
            self.get_wave_update_animation(wave, particle),
            run_time=3,
            rate_func=linear,
        )
        
        n_v_lines = 10
        v_lines = VGroup(*[
            DashedLine(UP, DOWN)
            for x in range(n_v_lines)
        ])
        v_lines.set_color(self.xi_color)
        v_lines.arrange(
            RIGHT,
            buff=float(axes.x_axis.unit_size)/self.default_wave_frequency
        )
        v_lines.move_to(particle.get_center())
        v_lines.align_to(wave, UP)
        v_lines.shift(0.125*RIGHT)
        
        self.add(formula, wave)
        
        # 播放動畫序列
        self.play(
            GrowArrow(p_arrow),
            Write(p_words),
            FadeIn(
                added_p_words,
                rate_func=squish_rate_func(smooth, 0.5, 1),
                run_time=2,
            ),
            wave_propagation
        )
        
        self.play(
            Write(xi_words),
            GrowArrow(xi_arrow),
            stopped_wave_propagation
        )
        
        self.play(
            FadeIn(added_xi_words),
            xi_words.animate.next_to(added_xi_words, UP),
        )
        
        self.play(
            LaggedStartMap(Create, v_lines),
        )
        self.play(LaggedStartMap(FadeOut, v_lines))
        self.wait()

        self.formula_labels = VGroup(
            p_words, p_arrow, added_p_words,
            xi_words, xi_arrow, added_xi_words, 
        )
        self.formula = formula
        self.wave = wave
        self.wave_propagation = wave_propagation

    def get_wave(self, axes, particle):
        """創建波函數"""
        def wave_func(x):
            return self.amplitude * np.sin(
                2 * PI * self.default_wave_frequency * x
            )
        
        wave = axes.plot(wave_func, x_range=[0, 10])
        wave.set_color(self.xi_color)
        return wave

    def get_wave_update_animation(self, wave, particle):
        """更新波函數的動畫"""
        def update_wave(w):
            new_wave = self.get_wave(wave.axes, particle)
            w.become(new_wave)
        
        return UpdateFromFunc(wave, update_wave)

    def react_to_claim(self):
        formula_labels = self.formula_labels
        full_formula = VGroup(self.formula, formula_labels)
        full_formula.save_state()
        wave_propagation = self.wave_propagation

        # 創建學生對話泡泡
        student_bubble = Bubble(
            direction=LEFT,
            height=2,
            width=2
        )
        student_text = Text("Hang on...")
        student_bubble.add_content(student_text)
        
        self.play(
            FadeIn(student_bubble),
            Write(student_text),
        )
        self.wait()
        
        kwargs = {
            "path_arc": TAU/4,
            "lag_ratio": 0.7,
            "run_time": 1.5,
        }
        
        self.play(
            full_formula.animate.scale(0).move_to(ORIGIN + DOWN),
            **kwargs
        )
        self.play(full_formula.animate.restore(), **kwargs)
        
        self.play(
            wave_propagation,
            FadeOut(student_bubble),
            FadeOut(student_text),
        )
        
        # 另一個學生對話
        student2_bubble = Bubble(
            height=2.5,
            width=3
        )
        student2_text = Text("Physics is just weird")
        student2_bubble.add_content(student2_text)
        
        self.play(
            FadeIn(student2_bubble),
            Write(student2_text),
            full_formula.animate.shift(UP)
        )
        self.wait()
        
        self.play(
            wave_propagation,
            full_formula.animate.shift(DOWN),
            FadeOut(student2_bubble),
            FadeOut(student2_text),
        )
        self.play(wave_propagation)
