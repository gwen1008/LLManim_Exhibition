from manim import *
import numpy as np

# [VISUAL REASONING]
# Centered complex plane with unit circle; 8 roots placed at exact angles kπ/4
# with vectors from origin, plus angle arc to reveal rotational symmetry.
# Header equation at top, footer general formula at bottom (above subtitle zone).

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
        title_eq = MathTex("z^8 = 1").move_to([0, 3.0, 0])

        plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5.0,
            y_length=5.0,
        ).move_to(ORIGIN)

        unit_circle = Circle(radius=1.25, color=BLUE).move_to(ORIGIN)

        root_coords = [
            (1.25, 0.0),
            (0.8838, 0.8838),
            (0.0, 1.25),
            (-0.8838, 0.8838),
            (-1.25, 0.0),
            (-0.8838, -0.8838),
            (0.0, -1.25),
            (0.8838, -0.8838),
        ]
        roots = [Dot(point=[x, y, 0], color=YELLOW, radius=0.08) for x, y in root_coords]
        vecs = [
            Arrow(start=[0, 0, 0], end=[x, y, 0], buff=0, stroke_width=4, color=GREEN)
            for x, y in root_coords
        ]

        angle_arc = Arc(
            radius=0.5, start_angle=0, angle=PI / 4, color=RED
        ).move_to(ORIGIN)
        angle_label = MathTex(r"\frac{\pi}{4}").move_to([0.95, 0.25, 0])
        formula = MathTex(r"z_k = e^{i\,2\pi k/8}, \ k=0,1,\dots,7").move_to([0, -2.4, 0])

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q07_unit_roots_1779993146/media/audio/Visualize_all_soluti_70492d6055/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 9.70  # [audio-sync]
        # Step 1
        self.set_subtitle("我們要找所有八次方等於一的複數，這些解稱為單位的八次方根，皆位於單位圓上。", run_time=_audio_dur_0)
        anim_time_1 = _audio_dur_0
        self.play(
            LaggedStart(
                Write(title_eq),
                Create(plane),
                Create(unit_circle),
                Indicate(unit_circle),
                lag_ratio=0.25,
                run_time=anim_time_1,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q07_unit_roots_1779993146/media/audio/Visualize_all_soluti_70492d6055/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 11.74  # [audio-sync]
        # Step 2
        self.set_subtitle("由歐拉公式，每個根的模為一，幅角為二πk除以八。先從一出發，逆時針標出前四個根。", run_time=_audio_dur_1)
        anim_time_2 = _audio_dur_1
        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(vecs[0]), FadeIn(roots[0])),
                AnimationGroup(GrowArrow(vecs[1]), FadeIn(roots[1])),
                AnimationGroup(GrowArrow(vecs[2]), FadeIn(roots[2])),
                AnimationGroup(GrowArrow(vecs[3]), FadeIn(roots[3])),
                lag_ratio=0.3,
                run_time=anim_time_2,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q07_unit_roots_1779993146/media/audio/Visualize_all_soluti_70492d6055/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 8.11  # [audio-sync]
        # Step 3
        self.set_subtitle("沿著圓繼續，剩餘的四個根構成一個完美對稱的正八邊形，內接於單位圓。", run_time=_audio_dur_2)
        anim_time_3 = _audio_dur_2
        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(vecs[4]), FadeIn(roots[4])),
                AnimationGroup(GrowArrow(vecs[5]), FadeIn(roots[5])),
                AnimationGroup(GrowArrow(vecs[6]), FadeIn(roots[6])),
                AnimationGroup(GrowArrow(vecs[7]), FadeIn(roots[7])),
                lag_ratio=0.3,
                run_time=anim_time_3,
            )
        )
        self.wait(0.1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/lite_Q07_unit_roots_1779993146/media/audio/Visualize_all_soluti_70492d6055/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 10.08  # [audio-sync]
        # Step 4
        self.set_subtitle("相鄰根之間恰好相差π除以四弧度，給出通式：z_k 等於 e 的 i 二πk 除以八次方。", run_time=_audio_dur_3)
        anim_time_4 = _audio_dur_3
        self.play(
            LaggedStart(
                Create(angle_arc),
                Write(angle_label),
                AnimationGroup(Indicate(vecs[0]), Indicate(vecs[1])),
                Write(formula),
                lag_ratio=0.25,
                run_time=anim_time_4,
            )
        )
        self.wait(0.1)