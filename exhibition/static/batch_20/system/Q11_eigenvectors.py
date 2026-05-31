# [VISUAL REASONING]
# 將矩陣 A 視為平面上的幾何作用：先變形基底網格，再凸顯兩個只被縮放、不改變方向的特徵向量。
# 佈局：HEADER 放標題，右上角顯示矩陣 A，中央為座標平面舞台，FOOTER 放步驟說明字幕。
# 節奏：先建立座標系與基底 → 套用矩陣造成剪切 → 依序揭露兩個特徵向量及其特徵方程式。

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
        registry = {}

        title = Text("Linear Transformation & Eigenvectors", color=WHITE, font_size=36).to_edge(UP, buff=0.4)
        registry["title"] = title

        matrix_label = Tex(r"$A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}$", color=YELLOW).to_corner(UR, buff=0.5)
        registry["matrix_label"] = matrix_label

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        ).move_to(ORIGIN)
        registry["plane"] = plane

        i_hat = Arrow(start=[0, 0, 0], end=[1, 0, 0], color=GREEN, buff=0)
        j_hat = Arrow(start=[0, 0, 0], end=[0, 1, 0], color=RED, buff=0)
        registry["i_hat"] = i_hat
        registry["j_hat"] = j_hat

        i_hat_transformed = Arrow(start=[0, 0, 0], end=[3, 0, 0], color=GREEN, buff=0)
        j_hat_transformed = Arrow(start=[0, 0, 0], end=[1, 2, 0], color=RED, buff=0)
        registry["i_hat_transformed"] = i_hat_transformed
        registry["j_hat_transformed"] = j_hat_transformed

        eigvec1 = Arrow(start=[0, 0, 0], end=[2, 0, 0], color=YELLOW, buff=0)
        eigvec2 = Arrow(start=[0, 0, 0], end=[1.4, -1.4, 0], color=ORANGE, buff=0)
        registry["eigvec1"] = eigvec1
        registry["eigvec2"] = eigvec2

        eig_eq1 = MathTex(r"A v_1 = 3 v_1", color=YELLOW).to_corner(DR, buff=0.5)
        eig_eq2 = MathTex(r"A v_2 = 2 v_2", color=ORANGE).next_to(eig_eq1, UP, buff=0.3)
        registry["eig_eq1"] = eig_eq1
        registry["eig_eq2"] = eig_eq2

        caption = Text("Watch how the basis vectors move.", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        registry["caption"] = caption

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q11_eigenvectors_1779987817/media/audio/Visualizing_the_line_2e8fd99b6f/step_00.mp3")  # [auto-injected]
        _audio_dur_0 = 5.47  # [audio-sync]
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 3.000)
        self.set_subtitle("矩陣 A 對平面作用，將每個基底向量送往新的位置。", run_time=_audio_dur_0)
        anim_time_1 = 3.000 * _scale_1
        self.play(Create(plane), run_time=2.0)
        self.play(Write(title), Write(matrix_label), run_time=1.0)
        self.play(Circumscribe(matrix_label, color=YELLOW), run_time=1.2)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 - 1.2 + 0.1)
        self.wait(remaining_1)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q11_eigenvectors_1779987817/media/audio/Visualizing_the_line_2e8fd99b6f/step_01.mp3")  # [auto-injected]
        _audio_dur_1 = 5.57  # [audio-sync]
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 1.500)
        self.set_subtitle("先看綠色的 i-hat 與紅色的 j-hat，它們是沿著座標軸的單位向量。", run_time=_audio_dur_1)
        anim_time_2 = 1.500 * _scale_2
        self.play(Create(i_hat), Create(j_hat), FadeIn(caption), run_time=1.5)
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 + 0.1)
        self.wait(remaining_2)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q11_eigenvectors_1779987817/media/audio/Visualizing_the_line_2e8fd99b6f/step_02.mp3")  # [auto-injected]
        _audio_dur_2 = 7.70  # [audio-sync]
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 4.000)
        self.set_subtitle("套用 A：i-hat 被拉伸到 (3,0)，j-hat 傾斜到 (1,2)，整個網格被剪切。", run_time=_audio_dur_2)
        anim_time_3 = 4.000 * _scale_3
        self.play(FadeOut(caption), run_time=0.4)
        self.play(
            plane.animate.apply_matrix([[3, 1], [0, 2]]),
            Transform(i_hat, i_hat_transformed),
            Transform(j_hat, j_hat_transformed),
            run_time=3.0,
        )
        self.play(Indicate(j_hat, color=RED), run_time=1.0)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 - 0.4 + 0.1)
        self.wait(remaining_3)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q11_eigenvectors_1779987817/media/audio/Visualizing_the_line_2e8fd99b6f/step_03.mp3")  # [auto-injected]
        _audio_dur_3 = 5.95  # [audio-sync]
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 3.000)
        self.set_subtitle("x 軸方向很特別：每個沿著它的向量，只被單純地放大三倍。", run_time=_audio_dur_3)
        anim_time_4 = 3.000 * _scale_4
        self.play(Create(eigvec1), Write(eig_eq1), run_time=2.0)
        self.play(Indicate(eigvec1, color=YELLOW), run_time=1.0)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(remaining_4)

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/exhibition/static/runs/batch_sys_Q11_eigenvectors_1779987817/media/audio/Visualizing_the_line_2e8fd99b6f/step_04.mp3")  # [auto-injected]
        _audio_dur_4 = 7.90  # [audio-sync]
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 3.500)
        self.set_subtitle("沿著 (1,-1) 的方向同樣不變，只被放大兩倍，這就揭示了兩個特徵向量。", run_time=_audio_dur_4)
        anim_time_5 = 3.500 * _scale_5
        self.play(Create(eigvec2), Write(eig_eq2), run_time=2.5)
        self.play(Indicate(eigvec2, color=ORANGE), run_time=1.0)
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 + 0.1)
        self.wait(remaining_5)