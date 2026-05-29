from manim import *
import random

class GeneratedScene(Scene):
    def construct(self):
        random.seed(42)
        
        title = Text("Galton 板：常態分佈模擬", font_size=32).to_edge(UP)
        self.play(Write(title))
        
        n_rows = 8
        peg_spacing = 0.45
        top_y = 2.2
        
        # Build pegs
        pegs = VGroup()
        peg_positions = []
        for row in range(n_rows):
            row_pegs = []
            for col in range(row + 1):
                x = (col - row / 2) * peg_spacing
                y = top_y - row * peg_spacing
                p = Dot(point=[x, y, 0], radius=0.05, color=GRAY_B)
                pegs.add(p)
                row_pegs.append((x, y))
            peg_positions.append(row_pegs)
        
        # Bins
        n_bins = n_rows + 1
        bin_y = top_y - n_rows * peg_spacing - 0.2
        bin_xs = [(i - n_rows / 2) * peg_spacing for i in range(n_bins)]
        
        bin_lines = VGroup()
        for i in range(n_bins + 1):
            x = (i - n_bins / 2) * peg_spacing
            line = Line([x, bin_y, 0], [x, bin_y - 1.8, 0], color=GRAY_D, stroke_width=2)
            bin_lines.add(line)
        floor = Line([-n_bins / 2 * peg_spacing, bin_y - 1.8, 0],
                     [n_bins / 2 * peg_spacing, bin_y - 1.8, 0], color=GRAY_D)
        
        self.play(FadeIn(pegs), Create(bin_lines), Create(floor))
        
        bin_counts = [0] * n_bins
        ball_radius = 0.08
        
        n_balls = 60
        batch_size = 6
        
        all_balls = []
        for batch_start in range(0, n_balls, batch_size):
            anims = []
            new_balls = []
            for b in range(batch_size):
                if batch_start + b >= n_balls:
                    break
                # Random path
                path_points = [[0, top_y + 0.6, 0]]
                col = 0
                for row in range(n_rows):
                    x, y = peg_positions[row][col]
                    path_points.append([x, y + 0.05, 0])
                    go_right = random.random() < 0.5
                    if go_right:
                        col += 1
                    nx = (col - (row + 1) / 2 + (row + 1) / 2 - row / 2 - (0 if go_right else 1)) 
                
                # Recompute simply
                path_points = [[0, top_y + 0.6, 0]]
                col = 0
                rights = 0
                for row in range(n_rows):
                    x, y = peg_positions[row][col]
                    path_points.append([x, y + 0.08, 0])
                    if random.random() < 0.5:
                        col += 1
                        rights += 1
                
                bin_idx = rights
                bx = bin_xs[bin_idx]
                stack_y = bin_y - 1.8 + ball_radius + bin_counts[bin_idx] * (2 * ball_radius)
                path_points.append([bx, bin_y - 0.1, 0])
                path_points.append([bx, stack_y, 0])
                bin_counts[bin_idx] += 1
                
                ball = Dot(point=path_points[0], radius=ball_radius, color=BLUE)
                new_balls.append((ball, path_points))
            
            for ball, _ in new_balls:
                self.add(ball)
            
            anims = []
            for ball, path in new_balls:
                segs = [ball.animate.move_to(p) for p in path[1:]]
                anims.append(Succession(*segs, run_time=2.5))
            
            self.play(*anims, run_time=2.5)
            all_balls.extend([b for b, _ in new_balls])
        
        # Draw bell curve overlay
        max_count = max(bin_counts)
        curve_points = []
        for i, c in enumerate(bin_counts):
            x = bin_xs[i]
            h = c * 2 * ball_radius
            curve_points.append([x, bin_y - 1.8 + h + 0.05, 0])
        
        curve = VMobject(color=YELLOW, stroke_width=4)
        curve.set_points_smoothly(curve_points)
        
        label = Text("近似常態分佈", font_size=24, color=YELLOW).next_to(curve, UP, buff=0.2)
        self.play(Create(curve), Write(label))
        self.wait(2)