# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示老師和學生們觀看一個雷達盤發射脈衝波追蹤飛機的動畫，並帶有「都卜勒雷達」文字標題。



from manim import *
class MentionDopplerRadar(TeacherStudentsScene):
    def construct(self):
        words = Text("Doppler Radar")
        words.next_to(self.teacher, UP)
        words.save_state()
        words.shift(DOWN).set_opacity(0)
        
        dish = RadarDish()
        dish.next_to(self.students, UP, buff=2, aligned_edge=LEFT)
        
        plane = Plane()
        plane.to_edge(RIGHT)
        plane.align_to(dish)
        plane.add_updater(lambda m, dt: m.shift(LEFT * dt))
        plane.flip(axis=UP)
        
        pulse = RadarPulse(dish, plane)
        
        look_at_anims = [
            pi.add_updater(lambda pi: pi.look_at(pulse.mobject))
            for pi in self.get_pi_creatures()
        ]

        self.add(dish, plane, pulse, *look_at_anims)
        self.play(
            self.teacher.animate.change("hooray"),
            words.animate.restore()
        )
        self.play_student_changes("pondering", "erm", "sassy")
        self.wait(2)
        self.play(
            self.teacher.animate.change("happy"),
            self.change_students(*["thinking"]*3)
        )
        self.wait()
        
        dish.set_stroke(width=0)
        self.play(
            UpdateFromAlphaFunc(
                VGroup(plane, dish),
                lambda m, alpha: m.set_fill(opacity=1 - alpha)
            )
        )
