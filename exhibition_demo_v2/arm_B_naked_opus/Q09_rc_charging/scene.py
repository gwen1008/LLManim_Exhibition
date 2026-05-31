from manim import *
import numpy as np


class MainScene(Scene):
    def construct(self):
        # ---------- Title ----------
        title = Text("RC Circuit Charging Response", font_size=44, color=YELLOW)
        underline = Line(LEFT, RIGHT, color=YELLOW).set_width(title.width * 1.1)
        underline.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), GrowFromCenter(underline))
        self.wait(0.6)
        self.play(
            title.animate.scale(0.6).to_edge(UP),
            FadeOut(underline),
        )
        self.wait(0.3)

        # ---------- Step 1: Draw RC series circuit ----------
        circuit = self.build_circuit()
        circuit.scale(0.9).move_to(ORIGIN + UP * 0.2)
        self.play(Create(circuit), run_time=2.5)
        self.wait(0.8)

        # Move circuit to the left to make room
        self.play(circuit.animate.scale(0.7).to_corner(UL).shift(DOWN * 0.8))
        self.wait(0.3)

        # ---------- Step 2: KVL ----------
        eq1 = MathTex("V_0", "=", "R\\,i", "+", "V(t)", font_size=42)
        eq1.set_color_by_tex("V_0", BLUE)
        eq1.set_color_by_tex("R\\,i", RED)
        eq1.set_color_by_tex("V(t)", GREEN)
        eq1.to_edge(RIGHT).shift(UP * 2.0 + LEFT * 0.3)
        kvl_label = Text("Kirchhoff's Voltage Law", font_size=22, color=GRAY_A)
        kvl_label.next_to(eq1, UP, buff=0.2)
        self.play(FadeIn(kvl_label, shift=DOWN), Write(eq1))
        self.wait(1.0)

        # ---------- Step 3: substitute i = C dV/dt ----------
        sub = MathTex("i = C\\,\\frac{dV}{dt}", font_size=34, color=ORANGE)
        sub.next_to(eq1, DOWN, buff=0.45)
        self.play(Write(sub))
        self.wait(0.6)

        eq2 = MathTex("V_0", "=", "RC\\,\\frac{dV}{dt}", "+", "V(t)", font_size=42)
        eq2.set_color_by_tex("V_0", BLUE)
        eq2.set_color_by_tex("RC", RED)
        eq2.set_color_by_tex("V(t)", GREEN)
        eq2.next_to(sub, DOWN, buff=0.45)
        self.play(TransformFromCopy(eq1, eq2))
        self.wait(1.0)

        # ---------- Step 4: solve the ODE ----------
        solve_label = Text("Solve first-order linear ODE", font_size=22, color=GRAY_A)
        solve_label.next_to(eq2, DOWN, buff=0.45)
        eq3 = MathTex(
            "V(t) = V_0\\left(1 - e^{-t/RC}\\right)",
            font_size=40,
        )
        eq3[0][0:4].set_color(GREEN)
        eq3.next_to(solve_label, DOWN, buff=0.35)
        box = SurroundingRectangle(eq3, color=YELLOW, buff=0.18)
        self.play(FadeIn(solve_label, shift=DOWN))
        self.play(Write(eq3))
        self.play(Create(box))
        self.wait(1.2)

        # Clear equations except final solution; move solution up
        self.play(
            FadeOut(eq1), FadeOut(sub), FadeOut(eq2),
            FadeOut(kvl_label), FadeOut(solve_label),
            FadeOut(circuit),
            VGroup(eq3, box).animate.scale(0.85).to_corner(UR).shift(DOWN * 0.2),
        )
        self.wait(0.4)

        # ---------- Step 5: plot V(t) ----------
        V0 = 4.0
        RC = 1.0
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            x_length=7.5,
            y_length=4.5,
            axis_config={"include_tip": True, "color": GREY_B},
        ).to_corner(DL).shift(RIGHT * 0.4 + UP * 0.2)

        x_label = axes.get_x_axis_label(MathTex("t").scale(0.8))
        y_label = axes.get_y_axis_label(MathTex("V(t)").scale(0.8))

        # Asymptote line V0
        asym = DashedLine(
            axes.c2p(0, V0), axes.c2p(6, V0), color=BLUE, stroke_width=2
        )
        asym_lbl = MathTex("V_0", font_size=30, color=BLUE).next_to(
            axes.c2p(6, V0), RIGHT, buff=0.1
        )

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))
        self.play(Create(asym), Write(asym_lbl))

        graph = axes.plot(
            lambda t: V0 * (1 - np.exp(-t / RC)),
            x_range=[0, 6],
            color=GREEN,
        )
        graph_lbl = MathTex("V_0(1-e^{-t/RC})", font_size=26, color=GREEN)
        graph_lbl.next_to(axes.c2p(4.2, V0 * (1 - np.exp(-4.2))), UP, buff=0.3)
        self.play(Create(graph), run_time=2.5)
        self.play(FadeIn(graph_lbl))
        self.wait(0.8)

        # ---------- Step 6: mark tau (63%) ----------
        tau = RC
        v_tau = V0 * (1 - np.exp(-1))  # 63%
        dot_tau = Dot(axes.c2p(tau, v_tau), color=YELLOW, radius=0.08)
        v_tau_line = DashedLine(axes.c2p(tau, 0), axes.c2p(tau, v_tau), color=YELLOW)
        h_tau_line = DashedLine(axes.c2p(0, v_tau), axes.c2p(tau, v_tau), color=YELLOW)
        tau_lbl = MathTex("\\tau = RC", font_size=28, color=YELLOW).next_to(
            axes.c2p(tau, 0), DOWN, buff=0.15
        )
        pct63 = MathTex("63\\%\\,V_0", font_size=26, color=YELLOW).next_to(
            axes.c2p(0, v_tau), LEFT, buff=0.1
        )
        self.play(
            Create(v_tau_line), Create(h_tau_line),
            FadeIn(dot_tau, scale=0.5),
        )
        self.play(Write(tau_lbl), Write(pct63))
        self.wait(1.2)

        # ---------- Step 7: mark 5 tau (99%) ----------
        t5 = 5 * RC
        v_5 = V0 * (1 - np.exp(-5))  # ~99%
        dot_5 = Dot(axes.c2p(t5, v_5), color=ORANGE, radius=0.08)
        v_5_line = DashedLine(axes.c2p(t5, 0), axes.c2p(t5, v_5), color=ORANGE)
        t5_lbl = MathTex("5\\tau", font_size=28, color=ORANGE).next_to(
            axes.c2p(t5, 0), DOWN, buff=0.15
        )
        pct99 = MathTex("\\approx 99\\%", font_size=26, color=ORANGE).next_to(
            dot_5, UP, buff=0.15
        )
        self.play(Create(v_5_line), FadeIn(dot_5, scale=0.5))
        self.play(Write(t5_lbl), Write(pct99))
        self.wait(1.5)

        # Final emphasis
        self.play(Indicate(box, color=YELLOW, scale_factor=1.1))
        self.wait(2.0)

    # ---------------------------------------------------------------
    def build_circuit(self):
        """Build a simple RC series circuit as VGroup."""
        # Rectangle loop corners
        tl = np.array([-2.5, 1.5, 0])
        tr = np.array([2.5, 1.5, 0])
        br = np.array([2.5, -1.5, 0])
        bl = np.array([-2.5, -1.5, 0])

        wire_color = GREY_A
        # Top wire (with resistor in middle)
        top_left = Line(tl, np.array([-0.7, 1.5, 0]), color=wire_color)
        top_right = Line(np.array([0.7, 1.5, 0]), tr, color=wire_color)

        # Resistor (zigzag)
        zig_pts = [np.array([-0.7, 1.5, 0])]
        n = 6
        amp = 0.22
        for k in range(n):
            x = -0.7 + (1.4) * (k + 0.5) / n
            y = 1.5 + (amp if k % 2 == 0 else -amp)
            zig_pts.append(np.array([x, y, 0]))
        zig_pts.append(np.array([0.7, 1.5, 0]))
        resistor = VMobject(color=RED, stroke_width=4)
        resistor.set_points_as_corners(zig_pts)
        r_label = MathTex("R", color=RED, font_size=36).next_to(resistor, UP, buff=0.2)

        # Right wire
        right_wire = Line(tr, br, color=wire_color)

        # Capacitor on bottom (two plates)
        cap_gap = 0.18
        plate_h = 0.55
        cap_x = 0.0
        plate1 = Line(
            np.array([cap_x - cap_gap, -1.5 + plate_h, 0]),
            np.array([cap_x - cap_gap, -1.5 - plate_h, 0]),
            color=GREEN, stroke_width=5,
        )
        plate2 = Line(
            np.array([cap_x + cap_gap, -1.5 + plate_h, 0]),
            np.array([cap_x + cap_gap, -1.5 - plate_h, 0]),
            color=GREEN, stroke_width=5,
        )
        bottom_left = Line(br, np.array([cap_x + cap_gap, -1.5, 0]), color=wire_color)
        bottom_right = Line(np.array([cap_x - cap_gap, -1.5, 0]), bl, color=wire_color)
        c_label = MathTex("C", color=GREEN, font_size=36).next_to(
            VGroup(plate1, plate2), DOWN, buff=0.2
        )

        # Left wire (with battery)
        bat_y = 0.0
        long_plate = Line(
            np.array([-2.5, bat_y + 0.3, 0]),
            np.array([-2.5, bat_y + 0.3, 0]) + RIGHT * 0,
            color=BLUE,
        )
        # battery symbol: long line (+) and short line (-)
        lp = Line(np.array([-2.7, bat_y + 0.25, 0]), np.array([-2.3, bat_y + 0.25, 0]),
                  color=BLUE, stroke_width=5)
        sp = Line(np.array([-2.6, bat_y - 0.25, 0]), np.array([-2.4, bat_y - 0.25, 0]),
                  color=BLUE, stroke_width=8)
        left_top = Line(tl, np.array([-2.5, bat_y + 0.25, 0]), color=wire_color)
        left_bot = Line(np.array([-2.5, bat_y - 0.25, 0]), bl, color=wire_color)
        v_label = MathTex("V_0", color=BLUE, font_size=36).next_to(
            VGroup(lp, sp), LEFT, buff=0.25
        )

        # Current arrow
        i_arrow = Arrow(
            np.array([-1.5, 1.5, 0]), np.array([-1.0, 1.5, 0]),
            color=YELLOW, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.5,
        )
        i_label = MathTex("i", color=YELLOW, font_size=32).next_to(i_arrow, UP, buff=0.1)

        return VGroup(
            top_left, top_right, resistor, r_label,
            right_wire,
            plate1, plate2, bottom_left, bottom_right, c_label,
            lp, sp, left_top, left_bot, v_label,
            i_arrow, i_label,
        )