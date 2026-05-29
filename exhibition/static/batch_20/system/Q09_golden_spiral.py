# [VISUAL REASONING]
# Build the golden spiral incrementally from Fibonacci squares (1,1,2,3,5,8),
# then overlay quarter-arcs inside each square to trace the spiral.
# Title at HEADER, construction in CONTENT, Fibonacci label at bottom.

from manim import *

class SubtitleManager:
    """Auto-injected by RefiningLoop.pre_render_patch. Prevents subtitle overlap and implements YT-style chunking."""
    MAX_WIDTH = 12.5

    def __init__(self, scene, font_size=28):
        self.scene = scene
        self.font_size = font_size
        self._current = None
        self._y = 3.5 * DOWN

    def show(self, text_str, run_time=1.0):
        import re
        FADE_IN = 0.10
        FADE_BETWEEN = 0.08

        # Break text into chunks by punctuation (keeping the punctuation)
        parts = re.split(r'([，。！？,\.!?]+)', str(text_str))
        sentences = []
        for i in range(0, len(parts)-1, 2):
            sentences.append((parts[i] + parts[i+1]).strip())
        if len(parts) % 2 == 1 and parts[-1].strip():
            sentences.append(parts[-1].strip())

        # 過濾空字串，確保 is_last 判斷正確
        sentences = [s for s in sentences if s]
        if not sentences:
            return

        total_len = sum(len(s) for s in sentences)
        n = len(sentences)

        # run_time = 字幕總存活時間（= TTS 時長），字幕要撐滿這段時間
        time_cursor = 0.0

        for idx, s in enumerate(sentences):

            text_mob = Text(s, font_size=self.font_size, color=WHITE, weight="BOLD")
            bg = BackgroundRectangle(text_mob, color=BLACK, fill_opacity=0.75, buff=0.15)
            new_mob = VGroup(bg, text_mob).move_to(self._y)
            if new_mob.width > self.MAX_WIDTH:
                new_mob.scale_to_fit_width(self.MAX_WIDTH)

            is_last = (idx == n - 1)

            if self._current is None:
                self.scene.play(FadeIn(new_mob), run_time=FADE_IN)
                time_cursor += FADE_IN
            else:
                self.scene.play(
                    FadeOut(self._current, run_time=FADE_BETWEEN / 2),
                    FadeIn(new_mob, run_time=FADE_BETWEEN / 2),
                )
                time_cursor += FADE_BETWEEN

            self._current = new_mob

            if not is_last:
                # 按字數比例分配時間給非最後一句
                chunk_ratio = len(s) / max(1, total_len)
                hold = run_time * chunk_ratio - (FADE_IN if idx == 0 else FADE_BETWEEN)
                if hold > 0:
                    self.scene.wait(hold)
                    time_cursor += hold
            else:
                # 最後一句：把剩餘時間全用掉，確保字幕撐到 TTS 結束
                remaining = run_time - time_cursor
                if remaining > 0:
                    self.scene.wait(remaining)

    def clear(self, run_time=0.5):
        if self._current is not None:
            anim_time = min(0.2, run_time)
            self.scene.play(FadeOut(self._current), run_time=anim_time)
            if run_time > anim_time:
                self.scene.wait(run_time - anim_time)
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
        # Build objects from blueprint
        title = Text("Golden Spiral from Fibonacci Squares", color=GOLD, font_size=36).to_edge(UP, buff=0.4)

        sq1 = Square(side_length=0.35, color=WHITE, stroke_width=2).move_to(np.array([-0.525, -0.7, 0]))
        sq2 = Square(side_length=0.35, color=WHITE, stroke_width=2).move_to(np.array([-0.175, -0.7, 0]))
        sq3 = Square(side_length=0.7, color=WHITE, stroke_width=2).move_to(np.array([-0.35, -0.175, 0]))
        sq4 = Square(side_length=1.05, color=WHITE, stroke_width=2).move_to(np.array([-1.225, -0.35, 0]))
        sq5 = Square(side_length=1.75, color=WHITE, stroke_width=2).move_to(np.array([-0.525, -1.75, 0]))
        sq6 = Square(side_length=2.8, color=WHITE, stroke_width=2).move_to(np.array([2.1, -0.525, 0]))

        arc1 = Arc(radius=0.35, start_angle=PI, angle=PI/2, arc_center=np.array([-0.35, -0.525, 0]), color=GOLD, stroke_width=3)
        arc2 = Arc(radius=0.35, start_angle=-PI/2, angle=PI/2, arc_center=np.array([-0.35, -0.525, 0]), color=GOLD, stroke_width=3)
        arc3 = Arc(radius=0.7, start_angle=0, angle=PI/2, arc_center=np.array([0, -0.525, 0]), color=GOLD, stroke_width=3)
        arc4 = Arc(radius=1.05, start_angle=PI/2, angle=PI/2, arc_center=np.array([0, 0.175, 0]), color=GOLD, stroke_width=3)
        arc5 = Arc(radius=1.75, start_angle=PI, angle=PI/2, arc_center=np.array([-1.75, 0.175, 0]), color=GOLD, stroke_width=3)
        arc6 = Arc(radius=2.8, start_angle=-PI/2, angle=PI/2, arc_center=np.array([-1.75, -1.05, 0]), color=GOLD, stroke_width=3)

        lbl_seq = MathTex(r"1,\ 1,\ 2,\ 3,\ 5,\ 8", color=YELLOW).to_edge(DOWN, buff=0.4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1779987515/media/audio/Draw_a_golden_spiral_6870d67e9f/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 6.72  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 2.500)
        self.set_subtitle("我們從費氏數列開始：1, 1, 2, 3, 5, 8。", run_time=_audio_dur_0)
        anim_time_1 = 2.500 * _scale_1
        self.play(Write(title), run_time=1.5)
        self.play(Write(lbl_seq), run_time=1.0)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1779987515/media/audio/Draw_a_golden_spiral_6870d67e9f/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 6.31  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 3.000)
        self.set_subtitle("先放兩個單位正方形並排，再於上方擺一個 2×2 正方形，形成 L 形。", run_time=_audio_dur_1)
        anim_time_2 = 3.000 * _scale_2
        self.play(LaggedStart(Create(sq1), Create(sq2), Create(sq3), lag_ratio=0.4), run_time=3.0)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1779987515/media/audio/Draw_a_golden_spiral_6870d67e9f/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 7.82  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 3.600)
        self.set_subtitle("再在左側貼上 3×3，下方擺 5×5，最後右側加上 8×8。", run_time=_audio_dur_2)
        anim_time_3 = 3.600 * _scale_3
        self.play(LaggedStart(Create(sq4), Create(sq5), Create(sq6), lag_ratio=0.4), run_time=3.6)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1779987515/media/audio/Draw_a_golden_spiral_6870d67e9f/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 5.50  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 4.200)
        self.set_subtitle("在每個正方形內畫一條四分之一圓弧，連接相對的兩個角。", run_time=_audio_dur_3)
        anim_time_4 = 4.200 * _scale_4
        self.play(LaggedStart(
            Create(arc1), Create(arc2), Create(arc3),
            Create(arc4), Create(arc5), Create(arc6),
            lag_ratio=0.35
        ), run_time=4.2)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q09_golden_spiral_1779987515/media/audio/Draw_a_golden_spiral_6870d67e9f/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 6.24  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 2.000)
        self.set_subtitle("這些弧線連在一起，就形成了藏在費氏數列中的黃金螺旋。", run_time=_audio_dur_4)
        anim_time_5 = 2.000 * _scale_5
        self.play(Indicate(lbl_seq), Indicate(arc6, color=GOLD), run_time=2.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)