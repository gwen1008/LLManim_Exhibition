# Source: 3b1b/_2018/fc1.py
# Description: [3b1b translated] 展示一個教師與學生場景，其中數字從0遞增到一百萬，伴隨彩帶動畫，然後討論真實里程碑（2^20），最後教師陷入思考。



from manim import *
class CrossingOneMillion(TeacherStudentsScene):
    def construct(self):
        self.increment_count()
        self.comment_on_real_milestone()
        self.reflect()

    def increment_count(self):
        number = self.number = Integer(0)
        number.move_to(UP + LEFT)
        number.scale(3)
        self.look_at(number, run_time=0)

        # 彩帶動畫 - 使用替代方案
        # 由於 get_confetti_animations 和 turn_animation_into_updater 在 CE 中不存在
        # 我們創建一個簡單的替代效果
        confetti_spirils = self.confetti_spirils = VGroup()
        for _ in range(50):
            dot = Dot(
                point=number.get_center(),
                radius=0.05,
                color=random_color()
            )
            confetti_spirils.add(dot)
        
        # 為每個點添加隨機移動動畫
        for dot in confetti_spirils:
            dot.velocity = np.array([
                np.random.uniform(-2, 2),
                np.random.uniform(-2, 2),
                0
            ])
            dot.add_updater(lambda d, dt: d.shift(d.velocity * dt))
        
        self.add(confetti_spirils)
        
        self.play(
            ChangeDecimalToValue(
                number, 10**6,
                position_update_func=lambda m: m.move_to(UP + LEFT),
                rate_func=bezier([0, 0, 0, 1, 1, 1]),
                run_time=5,
            ),
            LaggedStart(
                *[
                    ApplyMethod(
                        pi_creature.change, "hooray", number
                    )
                    for pi_creature in self.get_pi_creatures()
                ],
                rate_func=lambda t: squish_rate_func(smooth, 0, 0.5)(t),
                run_time=4,
            ),
        )
        self.wait()

    def comment_on_real_milestone(self):
        number = self.number
        remainder = Integer(2**20 - 10**6)
        words = Tex(
            "Just",
            f"{remainder.get_value():,}",
            "to go \\\\ before the real milestone",
        )
        
        self.student_says(
            words,
            added_anims=[
                ApplyMethod(self.teacher.change, "hesitant"),
                self.change_students("sassy", "speaking", "happy"),
                number.animate.scale(0.5).center().to_edge(UP),
            ]
        )
        self.wait()
        
        # 移除彩帶
        self.remove(*self.confetti_spirils)
        
        # 更新 remainder 的位置
        remainder.move_to(words[1].get_center())
        words.submobjects[1] = remainder
        
        self.play(
            ChangeDecimalToValue(number, 2**20, run_time=3),
            ChangeDecimalToValue(remainder, 0.1, run_time=3),
            self.teacher.animate.change("pondering", number),
            self.change_students(
                *["pondering"] * 3,
                look_at=number
            ),
        )
        
        self.play(
            FadeOut(self.students[1].bubble),
            FadeOut(self.students[1].bubble.content),
        )
        self.wait(2)

    def reflect(self):
        bubble = ThoughtBubble(
            direction=RIGHT,
            height=4,
            width=7,
        )
        bubble.pin_to(self.teacher)
        
        q_marks = Tex("???")
        q_marks.scale(2)
        q_marks.set_color_by_gradient(BLUE_D, BLUE_B)
        q_marks.next_to(bubble[-1].get_top(), DOWN)
        
        arrow = Arrow(
            start=ORIGIN,
            end=0.5 * DOWN,
            color=WHITE,
            buff=0
        )
        arrow.next_to(q_marks, DOWN)
        
        number = self.number
        number.generate_target()
        number.target.next_to(arrow, DOWN)

        self.play(
            Create(
                bubble,
                rate_func=lambda t: squish_rate_func(smooth, 0, 0.3)(t)
            ),
            Write(q_marks),
            GrowArrow(arrow),
            MoveToTarget(number),
            run_time=3
        )
        self.wait()
