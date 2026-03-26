'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the slope of a linear function y=2x-1 as constant rise/run ratio.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title (equation)
#    - Main Content: [Center y=0] for axes and line graph
#    - Footer Region: [Bottom y=-3.5] for explanations (slope formula and value)
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for triangles to keep components together. Position axes at center, title at top, explanations at bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Plot line, indicate y-intercept point.
#    - Step 3: Create y-intercept dot and label.
#    - Step 4: Construct first rise/run triangle at (0,-1).
#    - Step 5: Write slope formula in footer.
#    - Step 6: Transform first triangle to a second identical triangle at (2,3).
#    - Step 7: Write numerical slope value, circumscribe equation.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        layout = LayoutEngine()

        # Define anchors based on layout_plan description (High-Low Split)
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = MathTex(r"y = 2x - 1", color=BLUE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_constraint(layout.get("title").center_x == 0)

        # axes
        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes
        layout.add(LayoutObject(axes, "axes"))
        layout.add_to_zone(layout.get("axes"), "CONTENT")
        layout.add_constraint(layout.get("axes").center_x == 0)
        layout.add_constraint(layout.get("axes").center_y == 0)

        # line_graph (will be created via axes.plot)
        line_graph = axes.plot(lambda x: 2*x - 1, color=GREEN, x_range=[-6, 6])
        line_graph.move_to(graph_anchor)
        self.objects["line_graph"] = line_graph

        # point_y_intercept
        point_y_intercept = Dot(axes.c2p(0, -1), color=YELLOW, radius=0.08)
        self.objects["point_y_intercept"] = point_y_intercept

        # label_y_intercept
        label_y_intercept = MathTex(r"(0, -1)", color=YELLOW, font_size=30)
        label_y_intercept.next_to(point_y_intercept, DOWN, buff=0.1)
        self.objects["label_y_intercept"] = label_y_intercept

        # triangle_1 VGroup (components defined in sequence step 4)
        # We'll create it later, just initialize as empty VGroup for now.
        triangle_1 = VGroup()
        self.objects["triangle_1"] = triangle_1

        # triangle_2 VGroup (components defined in sequence step 6)
        triangle_2 = VGroup()
        self.objects["triangle_2"] = triangle_2

        # explanation_text_slope
        explanation_text_slope = Text("Slope (m) = Rise / Run", color=WHITE, font_size=32)
        explanation_text_slope.move_to(explanation_anchor + UP*0.5)
        self.objects["explanation_text_slope"] = explanation_text_slope
        layout.add(LayoutObject(explanation_text_slope, "explanation_text_slope"))
        layout.add_to_zone(layout.get("explanation_text_slope"), "FOOTER")
        layout.add_constraint(layout.get("explanation_text_slope").center_x == 0)

        # explanation_text_value
        explanation_text_value = MathTex(r"m = \frac{2}{1} = 2", color=ORANGE, font_size=40)
        explanation_text_value.next_to(explanation_text_slope, DOWN, buff=0.3)
        self.objects["explanation_text_value"] = explanation_text_value
        layout.add(LayoutObject(explanation_text_value, "explanation_text_value"))
        layout.add_to_zone(layout.get("explanation_text_value"), "FOOTER")
        layout.add_constraint(layout.get("explanation_text_value").center_x == 0)

        # Solve layout constraints
        layout.solve()

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # [missing audio] self.add_sound("media/audio/Create_an_animation__ddb0c0b519/step_00.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_0 = 2.00  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(self.objects["axes"]), run_time=2.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # [missing audio] self.add_sound("media/audio/Create_an_animation__ddb0c0b519/step_01.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2
        # signal_action: Indicate point_y_intercept (but point_y_intercept not created yet, so skip? Actually, we should create it first? Wait, step 3 creates it. Let's follow JSON: signal_action targets point_y_intercept, but visual_action creates line_graph. We'll create point_y_intercept now for indication, but not show it yet? Better to create it now but set opacity 0, then indicate? However, rule says NO PRE-HIDING. Let's create it now and keep it in objects, but not add to scene. Indicate will fail if object not in scene. So we must add point_y_intercept before indicating. But step 3 visual_action creates it. Conflict. We'll interpret: step 2 signal_action is a pre-cue, so we need the dot to exist. Let's create and add it now, but keep it invisible? That's pre-hiding. Instead, we can create and add it now, but not animate its creation until step 3. That's okay: we can add it silently before step 2? Rule says objects should only enter via self.play. So we cannot self.add it. Let's re-examine JSON: step 2 signal_action targets "point_y_intercept". That means the dot must be present. But step 3 visual_action creates it. This is a design inconsistency. We'll assume the Director intends the dot to be created in step 3, so step 2 signal_action should be ignored because target doesn't exist yet. We'll skip the signal_action for step 2.
        # According to rule: Signal action MUST execute BEFORE visual_action in the same step. But here signal_action targets an object not yet created. We'll skip it.
        # We'll just create the line.
        self.play(Create(self.objects["line_graph"]), run_time=3.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        # [missing audio] self.add_sound("media/audio/Create_an_animation__ddb0c0b519/step_02.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        # signal_action: Circumscribe label_y_intercept (label not yet created, same issue). We'll skip signal_action.
        self.play(FadeIn(self.objects["point_y_intercept"]), Write(self.objects["label_y_intercept"]), run_time=2.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        # [missing audio] self.add_sound("media/audio/Create_an_animation__ddb0c0b519/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4: Construct triangle_1 VGroup at (0,-1)
        # Define components: horizontal leg (run=1), vertical leg (rise=2), hypotenuse, labels.
        start_point = axes.c2p(0, -1)
        end_point_h = axes.c2p(1, -1)  # 1 unit right
        end_point_v = axes.c2p(0, 1)   # 2 units up from -1? Wait, rise=2 means from y=-1 to y=1. Yes.
        # Actually, the triangle should go from (0,-1) to (1,-1) to (1,1). Let's compute.
        # Horizontal leg from (0,-1) to (1,-1)
        h_leg = Line(start_point, axes.c2p(1, -1), color=BLUE)
        # Vertical leg from (1,-1) to (1,1)
        v_leg = Line(axes.c2p(1, -1), axes.c2p(1, 1), color=RED)
        # Hypotenuse along line from (0,-1) to (1,1)
        hypo = Line(start_point, axes.c2p(1, 1), color=YELLOW)
        # Labels
        run_label = MathTex(r"1", color=BLUE, font_size=24).next_to(h_leg, DOWN, buff=0.1)
        rise_label = MathTex(r"2", color=RED, font_size=24).next_to(v_leg, RIGHT, buff=0.1)
        # Group
        triangle_1_components = VGroup(h_leg, v_leg, hypo, run_label, rise_label)
        self.objects["triangle_1"] = triangle_1_components
        # Create triangle
        self.play(Create(h_leg), Create(v_leg), Create(hypo), Write(run_label), Write(rise_label), run_time=4.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        # [missing audio] self.add_sound("media/audio/Create_an_animation__ddb0c0b519/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        # signal_action: Indicate explanation_text_value (not yet written). We'll skip.
        self.play(Write(self.objects["explanation_text_slope"]), run_time=3.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        # [missing audio] self.add_sound("media/audio/Create_an_animation__ddb0c0b519/step_05.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_5 = 2.00  # [audio-sync] actual TTS duration
        # Step 6
        # signal_action: Indicate triangle_1
        self.play(Indicate(self.objects["triangle_1"], color=RED, run_time=1))
        # visual_action: Transform triangle_1 into triangle_2 (identical triangle at (2,3))
        # Create triangle_2 VGroup at (2,3) with same structure.
        start2 = axes.c2p(2, 3)
        h_leg2 = Line(start2, axes.c2p(3, 3), color=BLUE)
        v_leg2 = Line(axes.c2p(3, 3), axes.c2p(3, 5), color=RED)
        hypo2 = Line(start2, axes.c2p(3, 5), color=YELLOW)
        run_label2 = MathTex(r"1", color=BLUE, font_size=24).next_to(h_leg2, DOWN, buff=0.1)
        rise_label2 = MathTex(r"2", color=RED, font_size=24).next_to(v_leg2, RIGHT, buff=0.1)
        triangle_2_components = VGroup(h_leg2, v_leg2, hypo2, run_label2, rise_label2)
        self.objects["triangle_2"] = triangle_2_components
        # Transform triangle_1 into triangle_2
        self.play(Transform(self.objects["triangle_1"], self.objects["triangle_2"]), run_time=3.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        # [missing audio] self.add_sound("media/audio/Create_an_animation__ddb0c0b519/step_06.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_6 = 2.00  # [audio-sync] actual TTS duration
        # Step 7
        # signal_action: Circumscribe title
        self.play(Circumscribe(self.objects["title"], color=BLUE, run_time=1))
        # visual_action: Write explanation_text_value
        self.play(Write(self.objects["explanation_text_value"]), run_time=4.0)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))