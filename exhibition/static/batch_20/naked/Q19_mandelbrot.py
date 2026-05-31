from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        title = Text("Mandelbrot 集合", font_size=42).to_edge(UP)
        formula = MathTex(r"z_{n+1} = z_n^2 + c").next_to(title, DOWN)
        self.play(Write(title), Write(formula))
        self.wait(0.5)

        width, height = 400, 400
        x_min, x_max = -2.0, 1.0
        y_min, y_max = -1.5, 1.5
        max_iter = 60

        x = np.linspace(x_min, x_max, width)
        y = np.linspace(y_min, y_max, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        div_time = np.full(C.shape, max_iter, dtype=float)
        mask = np.ones(C.shape, dtype=bool)

        for i in range(max_iter):
            Z[mask] = Z[mask] ** 2 + C[mask]
            diverged = mask & (np.abs(Z) > 2)
            div_time[diverged] = i
            mask &= ~diverged

        norm = div_time / max_iter
        smooth = np.sqrt(norm)

        img = np.zeros((height, width, 3), dtype=np.uint8)
        r = (9 * (1 - smooth) * smooth**3 * 255)
        g = (15 * (1 - smooth) ** 2 * smooth**2 * 255)
        b = (8.5 * (1 - smooth) ** 3 * smooth * 255)
        img[..., 0] = np.clip(r, 0, 255).astype(np.uint8)
        img[..., 1] = np.clip(g, 0, 255).astype(np.uint8)
        img[..., 2] = np.clip(b, 0, 255).astype(np.uint8)
        img[div_time >= max_iter] = [0, 0, 0]
        img = np.flipud(img)

        mandel = ImageMobject(img)
        mandel.set_height(5.5)
        mandel.next_to(formula, DOWN, buff=0.2)

        self.play(FadeIn(mandel))
        self.wait(1)

        caption = Text("顏色表示發散速度，黑色代表收斂區", font_size=24)
        caption.next_to(mandel, DOWN, buff=0.15)
        self.play(Write(caption))
        self.wait(2)

        self.play(mandel.animate.scale(1.15))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, formula, caption)), FadeOut(mandel))
        self.wait(0.3)