from manim import *
import numpy as np

# [VISUAL REASONING]
# 1. Goal: Show how a Galton board turns independent random left/right choices into a bell curve (CLT).
# 2. Layout: Title in header, triangular pin grid in upper content (y +0.2..+2.0),
#    histogram axes + normal curve in lower content (y -2.0..0), rotating caption in footer (y ~ -2.3).
# 3. Flow: Build board -> one demo ball random walk -> 50 balls lumpy histogram ->
#    500 balls smooth bars -> overlay normal pdf confirming convergence.

class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Non-blocking subtitle (instant add/remove) —
    runs in parallel with animations and never stalls the main timeline.
    Does NOT use add_updater opacity tweening (broken on manim CE 0.19: VGroup.set_opacity(0)
    on a Text cannot be reversed inside an updater → subtitle stays invisible)."""
    MAX_WIDTH = 12.5
    Y_POSITION = 3.2 * DOWN

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None

    def show(self, text_str, run_time=1.0):
        # 瞬間顯示，不呼叫 scene.play/scene.wait → 不消耗時間軸（非阻塞）。
        # opacity 維持預設=1（絕不 set_opacity(0)），確保字幕一定可見。
        s = str(text_str).strip()
        if not s:
            return
        text_mob = Text(s, font_size=self.font_size, color=WHITE, weight="BOLD")
        bg = BackgroundRectangle(text_mob, color=BLACK, fill_opacity=0.75, buff=0.15)
        new_mob = VGroup(bg, text_mob).move_to(self.Y_POSITION)
        if new_mob.width > self.MAX_WIDTH:
            new_mob.scale_to_fit_width(self.MAX_WIDTH)
        if self._current is not None:
            self.scene.remove(self._current)
        self.scene.add(new_mob)
        self._current = new_mob

    def clear(self, run_time=0.0):
        if self._current is not None:
            self.scene.remove(self._current)
            self._current = None


class SceneInstrumentor:
    """Auto-injected by RefiningLoop.pre_render_patch to quantitatively track object overlap."""
    def __init__(self, scene, log_path="scene_state_log.json"):
        import json
        self._scene = scene
        self._log_path = log_path
        self._log = []
        self._step = 0
        self._original_play = scene.play
        scene.play = self._instrumented_play

    def _instrumented_play(self, *anims, **kwargs):
        result = self._original_play(*anims, **kwargs)
        self._step += 1
        snapshot = {"step": self._step, "mobjects": []}

        for mob in getattr(self._scene, "mobjects", []):
            # Manim v0.20.0: __getattr__ wraps deprecated getters, making hasattr() unreliable.
            # get_fill_opacity() may raise AttributeError or return None on internal mobjects.
            # Use try/except + (val or 0) to handle both cases robustly.
            try:
                opacity = (mob.get_fill_opacity() or 0) + (mob.get_stroke_opacity() or 0)
            except Exception:
                opacity = 1.0  # assume visible if opacity cannot be determined
                 
            if opacity <= 0.01 or type(mob).__name__ == "BackgroundRectangle":
                continue
            try:
                w, h = mob.width, mob.height
                if w * h < 0.05: continue
                c = mob.get_center().tolist()
                snapshot["mobjects"].append({
                    "type": type(mob).__name__, "width": round(w, 3), "height": round(h, 3),
                    "center": [round(c[0], 3), round(c[1], 3), round(c[2], 3)], "area": round(w * h, 3)
                })
            except Exception: pass
            
        snapshot["n_mobjects_visible"] = len(snapshot["mobjects"])
        oc = 0
        mobs = snapshot["mobjects"]
        for i in range(len(mobs)):
            for j in range(i + 1, len(mobs)):
                m1, m2 = mobs[i], mobs[j]
                ho = (abs(m1["center"][0] - m2["center"][0]) * 2 < (m1["width"] + m2["width"]))
                vo = (abs(m1["center"][1] - m2["center"][1]) * 2 < (m1["height"] + m2["height"]))
                if ho and vo: oc += 1
                
        snapshot["overlap_pairs"] = oc
        snapshot["total_screen_coverage"] = sum(m["area"] for m in mobs)
        self._log.append(snapshot)
        
        try:
            import json
            with open(self._log_path, "w", encoding="utf-8") as f:
                json.dump({
                    "max_simultaneous_objects": max((s["n_mobjects_visible"] for s in self._log), default=0),
                    "max_overlap_pairs": max((s["overlap_pairs"] for s in self._log), default=0),
                    "steps_with_overlap": sum(1 for s in self._log if s["overlap_pairs"] > 0),
                    "peak_screen_coverage": max((s["total_screen_coverage"] for s in self._log), default=0),
                    "timeline": self._log
                }, f, indent=2)
        except Exception: pass
        return result


class GeneratedScene(Scene):
    def construct(self):
        self._instrumentor = SceneInstrumentor(self, log_path='/Users/liaozhenting/Desktop/LLManim_Agent/scene_state_log.json')
        self._sm = SubtitleManager(self)
        self.set_subtitle = self._sm.show
        registry = {}

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q18_galton_board_1781379742/media/audio/Simulate_a_normal_di_5bd79536dd/step_00_f7afa498.mp3")  # [auto-injected]
        _audio_dur_0 = 6.05  # [audio-sync]
        # Step 1
        _scale_1 = min(2.5, max(1.0, (_audio_dur_0 * 0.95) / 4.300))
        title = Text("Galton Board: From Randomness to the Bell Curve", color=WHITE, font_size=34)
        title.to_edge(UP)
        registry["title"] = title

        apex = np.array([0.0, 2.0 + 0.6, 0.0])
        h_spacing = 0.45
        v_spacing = 0.2
        pin_grid = VGroup()
        for i in range(10):
            row = VGroup()
            for j in range(i + 1):
                x = apex[0] + (j - i / 2.0) * h_spacing
                y = apex[1] - i * v_spacing
                row.add(Dot(point=[x, y, 0], color=GREY_B, radius=0.04))
            pin_grid.add(row)
        registry["pin_grid"] = pin_grid

        funnel = Polygon(
            [-0.4, 2.25 + 0.6, 0],
            [0.4, 2.25 + 0.6, 0],
            [0, 2.05 + 0.6, 0],
            color=GREY, fill_opacity=0.4
        )
        registry["funnel"] = funnel

        self.play(Write(title), run_time=(1.2)*_scale_1)
        self.play(Create(funnel), run_time=(0.6)*_scale_1)
        self.play(LaggedStart(*[Create(row) for row in pin_grid], lag_ratio=0.12, run_time=(2.5)*_scale_1))
        self.set_subtitle("這是一個高爾頓板：球從頂端進入，穿過十排釘子。", run_time=_audio_dur_0)
        anim_time_1 = 4.300 * _scale_1
        remaining_1 = min(1.5, max(0.1, _audio_dur_0 - anim_time_1 + 0.1))
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q18_galton_board_1781379742/media/audio/Simulate_a_normal_di_5bd79536dd/step_01_1b4e31cb.mp3")  # [auto-injected]
        _audio_dur_1 = 8.11  # [audio-sync]
        # Step 2
        _scale_2 = min(2.5, max(1.0, (_audio_dur_1 * 0.95) / 3.600))
        ball_start = funnel.get_center() + np.array([0, 0.1, 0])
        ball_demo = Dot(point=ball_start, color=YELLOW, radius=0.08)
        registry["ball_demo"] = ball_demo

        np.random.seed(7)
        path_points = [ball_start.copy()]
        cur = ball_start.copy()
        net = 0
        for i in range(10):
            step = 0.225 if np.random.random() < 0.5 else -0.225
            net += (1 if step > 0 else -1)
            cur = cur + np.array([step, -v_spacing, 0])
            path_points.append(cur.copy())
        # land slightly above histogram zone
        landing = np.array([net * 0.105, -0.2, 0])
        path_points.append(landing)

        demo_path = VMobject()
        demo_path.set_points_as_corners(path_points)

        self.add(ball_demo)
        self.play(Indicate(ball_demo, color=YELLOW), run_time=(0.6)*_scale_2)
        self.set_subtitle("每碰到一根釘子，球以相等機率向左或向右，所以最終落點是十次硬幣的總和。", run_time=_audio_dur_1)
        self.play(MoveAlongPath(ball_demo, demo_path), run_time=(3.0)*_scale_2, rate_func=linear)
        anim_time_2 = 3.600 * _scale_2
        remaining_2 = min(1.5, max(0.1, _audio_dur_1 - anim_time_2 + 0.1))
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q18_galton_board_1781379742/media/audio/Simulate_a_normal_di_5bd79536dd/step_02_0c00e170.mp3")  # [auto-injected]
        _audio_dur_2 = 6.62  # [audio-sync]
        # Step 3
        _scale_3 = min(2.5, max(1.0, (_audio_dur_2 * 0.95) / 5.400))
        self.play(FadeOut(ball_demo), run_time=(0.4)*_scale_3)

        hist_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 5, 1],
            x_length=5.0,
            y_length=1.8,
            axis_config={"color": GREY, "include_tip": False},
        )
        hist_axes.move_to(np.array([0, -1.0, 0]))
        registry["hist_axes"] = hist_axes

        bin_centers = np.arange(-5, 6, 1)
        bar_width = 0.42

        from math import comb
        probs = np.array([comb(10, k) * (0.5 ** 10) for k in range(11)])

        counts_50 = probs * 50.0
        max_y = 5.0

        def make_histogram(counts, color, opacity):
            bars = VGroup()
            for idx, c in enumerate(counts):
                height_val = min(c, max_y)
                base = hist_axes.c2p(bin_centers[idx], 0)
                top = hist_axes.c2p(bin_centers[idx], height_val)
                pixel_h = max(0.001, top[1] - base[1])
                bar = Rectangle(
                    width=bar_width,
                    height=pixel_h,
                    color=color,
                    fill_opacity=opacity,
                    stroke_width=1,
                )
                bar.move_to([base[0], base[1] + pixel_h / 2.0, 0])
                bars.add(bar)
            return bars

        zero_hist = VGroup()
        for idx in range(11):
            base = hist_axes.c2p(bin_centers[idx], 0)
            bar = Rectangle(width=bar_width, height=0.001, color=BLUE, fill_opacity=0.8, stroke_width=1)
            bar.move_to([base[0], base[1], 0])
            zero_hist.add(bar)

        histogram = make_histogram(counts_50, BLUE, 0.8)
        registry["histogram"] = histogram

        self.play(Create(hist_axes), run_time=(1.0)*_scale_3)
        self.add(zero_hist)
        self.set_subtitle("現在丟下五十顆球，落點計數堆成一個不平整、參差不齊的直方圖。", run_time=_audio_dur_2)
        self.play(
            LaggedStart(
                *[ReplacementTransform(zero_hist[i], histogram[i]) for i in range(11)],
                lag_ratio=0.08,
            ),
            run_time=(4.0)*_scale_3,
        )
        anim_time_3 = 5.400 * _scale_3
        remaining_3 = min(1.5, max(0.1, _audio_dur_2 - anim_time_3 + 0.1))
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q18_galton_board_1781379742/media/audio/Simulate_a_normal_di_5bd79536dd/step_03_20be5294.mp3")  # [auto-injected]
        _audio_dur_3 = 5.45  # [audio-sync]
        # Step 4
        _scale_4 = min(2.5, max(1.0, (_audio_dur_3 * 0.95) / 4.500))
        counts_500 = probs * 500.0
        histogram_500 = make_histogram(counts_500, BLUE, 0.8)
        registry["histogram_500"] = histogram_500

        self.set_subtitle("丟下五百顆球後，柱子變得平滑，緊貼出一條乾淨的鐘形曲線。", run_time=_audio_dur_3)
        self.play(
            ReplacementTransform(histogram, histogram_500),
            run_time=(3.5)*_scale_4,
        )
        self.play(Circumscribe(histogram_500, color=YELLOW), run_time=(1.0)*_scale_4)
        anim_time_4 = 4.500 * _scale_4
        remaining_4 = min(1.5, max(0.1, _audio_dur_3 - anim_time_4 + 0.1))
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q18_galton_board_1781379742/media/audio/Simulate_a_normal_di_5bd79536dd/step_04_ce7625c8.mp3")  # [auto-injected]
        _audio_dur_4 = 8.42  # [audio-sync]
        # Step 5
        _scale_5 = min(2.5, max(1.0, (_audio_dur_4 * 0.95) / 4.100))
        mu = 0.0
        sigma = 1.58
        peak = min(max(counts_500), max_y)
        normal_curve = hist_axes.plot(
            lambda x: peak * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)),
            x_range=[-5, 5],
            color=RED,
        )
        registry["bell_curve"] = normal_curve

        caption = Text("More balls -> closer to the normal curve.", color=WHITE, font_size=26)
        caption.move_to(np.array([0, -2.3, 0]))
        registry["caption"] = caption

        self.set_subtitle("疊上常態曲線後得到證實：隨著球數增加，直方圖收斂到鐘形分佈。", run_time=_audio_dur_4)
        self.play(Create(normal_curve), run_time=(3.0)*_scale_5)
        self.play(Indicate(normal_curve, color=RED), run_time=(0.6)*_scale_5)
        self.play(FadeIn(caption), run_time=(0.5)*_scale_5)
        anim_time_5 = 4.100 * _scale_5
        remaining_5 = min(1.5, max(0.1, _audio_dur_4 - anim_time_5 + 0.1))
        self.wait(remaining_5)