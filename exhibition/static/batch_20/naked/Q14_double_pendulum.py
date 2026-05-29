from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        title = Text("Double Pendulum Chaos", font_size=36).to_edge(UP)
        self.play(Write(title))

        pivot = np.array([0.0, 1.5, 0.0])
        L1, L2 = 1.6, 1.6
        m1, m2 = 1.0, 1.0
        g = 9.8

        state = [PI/2 + 0.3, PI/2 + 0.1, 0.0, 0.0]  # th1, th2, w1, w2

        def derivs(s):
            t1, t2, w1, w2 = s
            d = t2 - t1
            den1 = (m1 + m2)*L1 - m2*L1*np.cos(d)**2
            den2 = (L2/L1)*den1
            a1 = (m2*L1*w1**2*np.sin(d)*np.cos(d)
                  + m2*g*np.sin(t2)*np.cos(d)
                  + m2*L2*w2**2*np.sin(d)
                  - (m1+m2)*g*np.sin(t1)) / den1
            a2 = (-m2*L2*w2**2*np.sin(d)*np.cos(d)
                  + (m1+m2)*g*np.sin(t1)*np.cos(d)
                  - (m1+m2)*L1*w1**2*np.sin(d)
                  - (m1+m2)*g*np.sin(t2)) / den2
            return np.array([w1, w2, a1, a2])

        def positions():
            t1, t2 = state[0], state[1]
            p1 = pivot + np.array([L1*np.sin(t1), -L1*np.cos(t1), 0])
            p2 = p1 + np.array([L2*np.sin(t2), -L2*np.cos(t2), 0])
            return p1, p2

        p1, p2 = positions()
        rod1 = Line(pivot, p1, color=BLUE)
        rod2 = Line(p1, p2, color=GREEN)
        pivot_dot = Dot(pivot, color=WHITE)
        bob1 = Dot(p1, color=BLUE, radius=0.12)
        bob2 = Dot(p2, color=RED, radius=0.14)

        trail = VMobject(color=YELLOW, stroke_width=2)
        trail.set_points_as_corners([p2, p2 + 0.001*RIGHT])
        trail_pts = [p2.copy()]

        self.add(rod1, rod2, pivot_dot, bob1, bob2, trail)

        dt = 1/60
        max_pts = 400

        def update(mob, d_t):
            steps = 3
            h = d_t / steps if d_t > 0 else dt/steps
            for _ in range(steps):
                s = np.array(state)
                k1 = derivs(s)
                k2 = derivs(s + h/2*k1)
                k3 = derivs(s + h/2*k2)
                k4 = derivs(s + h*k3)
                new = s + h/6*(k1 + 2*k2 + 2*k3 + k4)
                for i in range(4):
                    state[i] = new[i]
            np1, np2 = positions()
            rod1.put_start_and_end_on(pivot, np1)
            rod2.put_start_and_end_on(np1, np2)
            bob1.move_to(np1)
            bob2.move_to(np2)
            trail_pts.append(np2.copy())
            if len(trail_pts) > max_pts:
                trail_pts.pop(0)
            if len(trail_pts) >= 2:
                trail.set_points_as_corners(trail_pts)

        rod1.add_updater(update)
        self.wait(12)
        rod1.clear_updaters()
        self.wait(1)