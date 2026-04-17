# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一個 Tau 生物角色從站立狀態旋轉倒下，並在過程中變為憤怒表情的動畫。



from manim import *
class TauFalls(Scene):
    def construct(self):
        tau = TauCreature()
        bottom = np.min(tau.body.get_points()[:, 1]) * UP
        angle = -0.15 * TAU
        tau.generate_target()
        tau.target.change("angry")
        tau.target.rotate(angle, about_point=bottom)
        self.play(Rotate(tau, angle, rate_func=rush_into, path_arc=angle, about_point=bottom))
        # self.play(MoveToTarget(tau, rate_func=rush_into, path_arc=angle))
        self.play(MoveToTarget(tau))
        self.wait()
