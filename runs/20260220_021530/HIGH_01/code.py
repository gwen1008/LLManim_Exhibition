'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the graphing of a linear function y = 2x - 1, emphasizing the y-intercept and the slope as rise/run.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and function label
#    - Main Content: [Center y=0] for coordinate plane, line, dot, and slope triangle
#    - Footer Region: [Bottom y=-3.5] for final slope explanation
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine zones to keep title, main content, and footer separated.
#    - The plane and axes are centered. The slope triangle and labels are positioned relative to the axes.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show grid and highlight function.
#    - Step 2: Draw axes.
#    - Step 3: Show red dot at y-intercept.
#    - Step 4: Animate dot moving along slope (right 1, up 2).
#    - Step 5: Simultaneously grow line from dot's path.
#    - Step 6-7: Draw slope triangle (horizontal then vertical legs).
#    - Step 8-9: Label triangle sides (run=1, rise=2).
#    - Step 10: Show final slope formula at bottom.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Initialize Layout Engine
        layout = LayoutEngine()

        # Create objects from layout_plan
        # title
        title = Text("Graphing y = 2x - 1", color=WHITE, font_size=40)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        # plane (NumberPlane)
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-8, 6, 1],
            x_length=10,
            y_length=10,
            stroke_opacity=0.5
        )
        self.objects["plane"] = plane
        obj_plane = LayoutObject(plane, "plane")
        layout.add(obj_plane)
        layout.add_to_zone(obj_plane, "CONTENT")
        layout.add_constraint(obj_plane.center_x == 0)
        layout.add_constraint(obj_plane.center_y == 0)

        # axes (Axes)
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-8, 6, 1],
            x_length=10,
            y_length=10
        )
        self.objects["axes"] = axes
        obj_axes = LayoutObject(axes, "axes")
        layout.add(obj_axes)
        layout.add_to_zone(obj_axes, "CONTENT")
        layout.add_constraint(obj_axes.center_x == 0)
        layout.add_constraint(obj_axes.center_y == 0)

        # func_label
        func_label = MathTex("y = 2x - 1", color=YELLOW)
        self.objects["func_label"] = func_label
        obj_func = LayoutObject(func_label, "func_label")
        layout.add(obj_func)
        layout.add_to_zone(obj_func, "HEADER")
        layout.align_to(obj_func, obj_title, "BOTTOM", buff=0.5)
        layout.add_constraint(obj_func.center_x == 0)

        # line_full
        line_full = Line(
            start=np.array([-3, -7, 0]),
            end=np.array([3, 5, 0]),
            color=BLUE,
            stroke_width=4
        )
        self.objects["line_full"] = line_full
        # Position will be handled by layout, but we also need to keep it at axes center
        obj_line_full = LayoutObject(line_full, "line_full")
        layout.add(obj_line_full)
        layout.add_to_zone(obj_line_full, "CONTENT")
        layout.add_constraint(obj_line_full.center_x == 0)
        layout.add_constraint(obj_line_full.center_y == 0)

        # dot_start
        dot_start = Dot(radius=0.08, color=RED)
        dot_start.move_to(np.array([0, -1, 0]))
        self.objects["dot_start"] = dot_start
        obj_dot = LayoutObject(dot_start, "dot_start")
        layout.add(obj_dot)
        layout.add_to_zone(obj_dot, "CONTENT")
        # dot position is absolute (0,-1) relative to axes center, handled after solve

        # line_growing (initially a point at (0,-1))
        line_growing = Line(
            start=np.array([0, -1, 0]),
            end=np.array([0, -1, 0]),
            color=BLUE,
            stroke_width=4
        )
        self.objects["line_growing"] = line_growing
        obj_line_grow = LayoutObject(line_growing, "line_growing")
        layout.add(obj_line_grow)
        layout.add_to_zone(obj_line_grow, "CONTENT")
        layout.add_constraint(obj_line_grow.center_x == 0)
        layout.add_constraint(obj_line_grow.center_y == 0)

        # triangle_horizontal
        triangle_horizontal = Line(
            start=np.array([0, -1, 0]),
            end=np.array([1, -1, 0]),
            color=GREEN,
            stroke_width=3
        )
        self.objects["triangle_horizontal"] = triangle_horizontal
        obj_tri_h = LayoutObject(triangle_horizontal, "triangle_horizontal")
        layout.add(obj_tri_h)
        layout.add_to_zone(obj_tri_h, "CONTENT")
        # position is absolute, handled after solve

        # triangle_vertical
        triangle_vertical = Line(
            start=np.array([1, -1, 0]),
            end=np.array([1, 1, 0]),
            color=GREEN,
            stroke_width=3
        )
        self.objects["triangle_vertical"] = triangle_vertical
        obj_tri_v = LayoutObject(triangle_vertical, "triangle_vertical")
        layout.add(obj_tri_v)
        layout.add_to_zone(obj_tri_v, "CONTENT")

        # label_rise
        label_rise = MathTex("2", color=GREEN, font_size=30)
        self.objects["label_rise"] = label_rise
        obj_lrise = LayoutObject(label_rise, "label_rise")
        layout.add(obj_lrise)
        layout.add_to_zone(obj_lrise, "CONTENT")
        # position relative to triangle_vertical will be set after solve

        # label_run
        label_run = MathTex("1", color=GREEN, font_size=30)
        self.objects["label_run"] = label_run
        obj_lrun = LayoutObject(label_run, "label_run")
        layout.add(obj_lrun)
        layout.add_to_zone(obj_lrun, "CONTENT")

        # label_slope
        label_slope = MathTex(
            r"\text{slope} = \frac{\text{rise}}{\text{run}} = \frac{2}{1} = 2",
            color=YELLOW,
            font_size=30
        )
        self.objects["label_slope"] = label_slope
        obj_lslope = LayoutObject(label_slope, "label_slope")
        layout.add(obj_lslope)
        layout.add_to_zone(obj_lslope, "FOOTER")
        layout.add_constraint(obj_lslope.center_x == 0)

        # Solve layout constraints
        layout.solve()

        # Now adjust positions that are absolute relative to axes center
        # The axes center is at ORIGIN after layout solve.
        # We need to shift the dot, triangle legs, and their labels accordingly.
        # Since axes_center is ORIGIN, we can keep the absolute coordinates as defined.
        # But we must ensure they are children of the axes group? Not necessary.
        # The layout engine has already placed the axes at center.
        # The dot and triangle vertices are defined in scene coordinates, which are correct.

        # However, labels need to be positioned relative to their lines.
        # Do this after layout.solve() because we need the lines' final positions.
        label_rise.next_to(triangle_vertical, RIGHT, buff=0.1)
        label_run.next_to(triangle_horizontal, DOWN, buff=0.1)

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We want to graph the linear function y equals 2x minus 1. First, note that when x is zero, y is negative one. This is the y-intercept.",
                "signal_action": {"type": "Circumscribe", "target": "func_label", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "plane", "details": "Fade in the coordinate grid"},
                "duration": 11.184,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Let's place a point at the y-intercept, (0, -1).",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw the x and y axes"},
                "duration": 4.128,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, the slope is 2. This means for every 1 unit we move to the right (the run), we must move 2 units up (the rise). Let's animate this.",
                "signal_action": {"type": "Indicate", "target": "dot_start", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "dot_start", "details": "Show the red dot at the intercept"},
                "duration": 11.04,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Watch the dot move: one unit right, then two units up. This path defines the direction of our line.",
                "signal_action": {"type": "Indicate", "target": "dot_start", "color": "RED"},
                "visual_action": {"type": "Transform", "target_id": "dot_start", "details": "Animate the dot moving from (0,-1) to (1,1) along the path defined by the slope. Use a smooth animation lasting 3 seconds."},
                "duration": 7.536,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "As the dot moves, it traces out the line. The line is the set of all points following this same rise-over-run rule.",
                "signal_action": None,
                "visual_action": {"type": "Transform", "target_id": "line_growing", "details": "Simultaneously transform the 'line_growing' from a point at (0,-1) into the full 'line_full' from (-3,-7) to (3,5). This visually draws the line as the dot moves."},
                "duration": 7.896,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Let's isolate one cycle of rise-over-run. From our starting point, moving 1 unit right and 2 units up forms a right triangle.",
                "signal_action": {"type": "Circumscribe", "target": "triangle_horizontal", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "triangle_horizontal", "details": "Draw the horizontal green segment from (0,-1) to (1,-1)"},
                "duration": 9.12,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "The vertical side of this triangle represents the rise of 2 units.",
                "signal_action": {"type": "Circumscribe", "target": "triangle_vertical", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "triangle_vertical", "details": "Draw the vertical green segment from (1,-1) to (1,1)"},
                "duration": 4.704,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "Labeling these sides, we see the run is 1 and the rise is 2. The slope is their ratio.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_run", "details": "Write the label '1' below the horizontal leg"},
                "duration": 6.6,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_07.mp3"
            },
            {
                "step": 9,
                "narrative": "Therefore, the slope is 2 divided by 1, which equals 2. This matches the coefficient of x in our equation.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_rise", "details": "Write the label '2' to the right of the vertical leg"},
                "duration": 8.136,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_08.mp3"
            },
            {
                "step": 10,
                "narrative": "In summary, the graph of y = 2x - 1 is a line with y-intercept -1 and slope 2, meaning it rises 2 units for every 1 unit it runs.",
                "signal_action": {"type": "Indicate", "target": "label_slope", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "label_slope", "details": "Display the final slope formula and calculation at the bottom"},
                "duration": 9.792,
                "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_09.mp3"
            }
        ]

        for step in sequence:
            # === AUDIO (MANDATORY) ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects[signal["target"]]
                color = eval(signal["color"])  # YELLOW, RED, etc.
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))

            # Visual action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            obj = self.objects[target_id]

            if visual["type"] == "Create":
                self.play(Create(obj))
            elif visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Transform":
                if target_id == "dot_start":
                    # Animate dot moving from (0,-1) to (1,1)
                    # We'll create a path: right then up
                    path = VMobject()
                    path.set_points_smoothly([
                        np.array([0, -1, 0]),
                        np.array([1, -1, 0]),
                        np.array([1, 1, 0])
                    ])
                    self.play(MoveAlongPath(obj, path), run_time=3)
                elif target_id == "line_growing":
                    # Transform line_growing (point) into line_full
                    self.play(Transform(obj, self.objects["line_full"]), run_time=3)
                else:
                    # Fallback
                    self.play(Transform(obj, obj))

            # Wait for remaining duration
            # Estimate animation run_time
            if visual["type"] == "Create":
                anim_time = 1.0
            elif visual["type"] == "Write":
                anim_time = 1.0
            elif visual["type"] == "Transform":
                if target_id == "dot_start":
                    anim_time = 3.0
                elif target_id == "line_growing":
                    anim_time = 3.0
                else:
                    anim_time = 1.0
            else:
                anim_time = 1.0

            if signal is not None:
                anim_time += 1.0  # signal run_time

            remaining = step["duration"] - anim_time + 0.5
            if remaining > 0:
                self.wait(remaining)