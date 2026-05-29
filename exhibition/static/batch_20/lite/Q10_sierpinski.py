from manim import *
import numpy as np

# [VISUAL REASONING]
# Sierpinski triangle recursive construction with iteration counter.
# Each step uses LaggedStart wrapped in single self.play to fill audio duration.

def _midpoint(p, q):
    return [(p[0]+q[0])/2, (p[1]+q[1])/2, 0]

def _sierpinski(vertices_list, depth):
    """Recursively subdivide. Returns list of vertex-triples at given depth."""
    if depth == 0:
        return vertices_list
    new_list = []
    for (p1, p2, p3) in vertices_list:
        m12 = _midpoint(p1, p2)
        m23 = _midpoint(p2, p3)
        m31 = _midpoint(p3, p1)
        new_list.append((p1, m12, m31))
        new_list.append((m12, p2, m23))
        new_list.append((m31, m23, p3))
    return _sierpinski(new_list, depth - 1)


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
        SEED = [[-2.1, -1.3, 0], [2.1, -1.3, 0], [0, 2.0, 0]]

        title = Text("Sierpinski Triangle Construction", font_size=36).to_edge(UP)
        iter_label = MathTex("n = 0", font_size=40).to_corner(UR)

        tri_iter0 = Polygon(
            *SEED, color=BLUE_C, fill_color=BLUE_C,
            fill_opacity=0.7, stroke_width=2,
        )

        def build_group(depth, fill_opacity, stroke_width):
            tris = _sierpinski([tuple(map(tuple, SEED))], depth)
            return VGroup(*[
                Polygon(
                    list(p1), list(p2), list(p3),
                    color=BLUE_C, fill_color=BLUE_C,
                    fill_opacity=fill_opacity, stroke_width=stroke_width,
                )
                for (p1, p2, p3) in tris
            ])

        tri_group_iter1 = build_group(1, 0.65, 2)
        tri_group_iter2 = build_group(2, 0.6, 2)
        tri_group_iter3 = build_group(3, 0.55, 1.5)
        tri_group_iter4 = build_group(4, 0.5, 1.0)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q10_sierpinski_1779993257/media/audio/Construct_the_Sierpi_ddff600f9c/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 9.10  # [audio-sync]
        # Step 1
        self.set_subtitle("我們從一個大型等邊三角形開始，作為整個 Sierpinski 遞迴建構的起始畫布。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title),
                FadeIn(iter_label),
                Create(tri_iter0),
                tri_iter0.animate.set_fill(BLUE_C, opacity=0.7),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q10_sierpinski_1779993257/media/audio/Construct_the_Sierpi_ddff600f9c/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 9.58  # [audio-sync]
        # Step 2
        self.set_subtitle("第一輪:連接每邊的中點,將三角形分成四塊全等的小三角形,然後移除中央倒置的三角形。", run_time=_audio_dur_1)
        p1, p2, p3 = SEED
        m12 = _midpoint(p1, p2)
        m23 = _midpoint(p2, p3)
        m31 = _midpoint(p3, p1)
        connector = VGroup(
            DashedLine(m12, m23, color=YELLOW),
            DashedLine(m23, m31, color=YELLOW),
            DashedLine(m31, m12, color=YELLOW),
        )
        central = Polygon(m12, m23, m31, color=RED, fill_color=RED, fill_opacity=0.5, stroke_width=2)
        new_label1 = MathTex("n = 1", font_size=40).to_corner(UR)

        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                Create(connector),
                FadeIn(central),
                FadeOut(central),
                FadeOut(tri_iter0),
                FadeOut(connector),
                LaggedStart(*[FadeIn(t) for t in tri_group_iter1], lag_ratio=0.2),
                Transform(iter_label, new_label1),
                lag_ratio=0.25,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q10_sierpinski_1779993257/media/audio/Construct_the_Sierpi_ddff600f9c/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 8.90  # [audio-sync]
        # Step 3
        self.set_subtitle("第二輪:對每個剩下的三角形套用同樣的規則,產生九個更小的角落三角形,中央區域消失。", run_time=_audio_dur_2)
        new_label2 = MathTex("n = 2", font_size=40).to_corner(UR)
        highlight1 = tri_group_iter1.copy().set_stroke(YELLOW, width=3).set_fill(opacity=0)

        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                Create(highlight1),
                FadeOut(highlight1),
                FadeOut(tri_group_iter1),
                LaggedStart(*[FadeIn(t) for t in tri_group_iter2], lag_ratio=0.1),
                Transform(iter_label, new_label2),
                lag_ratio=0.25,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q10_sierpinski_1779993257/media/audio/Construct_the_Sierpi_ddff600f9c/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 8.95  # [audio-sync]
        # Step 4
        self.set_subtitle("第三輪再次重複此過程,產生二十七個微小三角形,展現出明顯的自相似 Sierpinski 圖樣。", run_time=_audio_dur_3)
        new_label3 = MathTex("n = 3", font_size=40).to_corner(UR)
        pulse_rect = SurroundingRectangle(tri_group_iter3, color=YELLOW, buff=0.1)

        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                FadeOut(tri_group_iter2),
                LaggedStart(*[FadeIn(t) for t in tri_group_iter3], lag_ratio=0.05),
                Transform(iter_label, new_label3),
                Create(pulse_rect),
                FadeOut(pulse_rect),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q10_sierpinski_1779993257/media/audio/Construct_the_Sierpi_ddff600f9c/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 9.12  # [audio-sync]
        # Step 5
        self.set_subtitle("第四輪後,剩下八十一個三角形,說明此簡單遞迴規則如何快速收斂至著名的碎形極限。", run_time=_audio_dur_4)
        new_label4 = MathTex("n = 4", font_size=40).to_corner(UR)
        final_rect = SurroundingRectangle(tri_group_iter4, color=YELLOW, buff=0.1)
        caption = MathTex(r"3^4 = 81  triangles", font_size=36).move_to([0, -2.6, 0])

        anim_time_5 = _audio_dur_4
        self.play(
            LaggedStart(
                FadeOut(tri_group_iter3),
                LaggedStart(*[FadeIn(t) for t in tri_group_iter4], lag_ratio=0.02),
                Transform(iter_label, new_label4),
                Create(final_rect),
                FadeIn(caption),
                lag_ratio=0.25,
                run_time=anim_time_5,
            )
        )
        self.wait(0.1)