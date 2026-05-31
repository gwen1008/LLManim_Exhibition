from manim import *

# [VISUAL REASONING]
# Two-phase design: Phase 1 derives eigenvalues/eigenvectors algebraically
# using in-place ReplacementTransform morphing at ORIGIN to avoid stacking/overflow.
# Phase 2 clears the algebra, introduces a NumberPlane, draws the eigenvector arrows,
# and applies the matrix [[3,1],[0,2]] to show eigenvectors only stretch, never rotate.

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
        title = Text("Eigenvalues & Eigenvectors", color=WHITE, font_size=38)
        title.to_edge(UP)
        self.add(title)

        matrix_A = MathTex(r"A = \left[\begin{array}{cc} 3 & 1 \\ 0 & 2 \end{array}\right]", color=WHITE)
        matrix_A.move_to(ORIGIN + np.array([0, 1.0, 0]))

        char_eq = MathTex(r"\det(A - \lambda I) = 0", color=YELLOW)
        char_eq.move_to(ORIGIN + np.array([0, -0.5, 0]))

        char_det = MathTex(r"\det\left[\begin{array}{cc} 3-\lambda & 1 \\ 0 & 2-\lambda \end{array}\right] = 0", color=WHITE)
        char_det.move_to(ORIGIN + np.array([0, -0.5, 0]))

        char_expand = MathTex(r"(3-\lambda)(2-\lambda) = 0", color=WHITE)
        char_expand.move_to(ORIGIN + np.array([0, -0.5, 0]))

        eigenvalues = MathTex(r"\lambda_1 = 3, \quad \lambda_2 = 2", color=GREEN)
        eigenvalues.move_to(ORIGIN + np.array([0, -0.5, 0]))

        eig3_setup = MathTex(r"(A - 3I)\,v = \left[\begin{array}{cc} 0 & 1 \\ 0 & -1 \end{array}\right] v = 0", color=WHITE)
        eig3_setup.move_to(ORIGIN + np.array([0, 0.3, 0]))

        eig3_vec = MathTex(r"v_1 = \left[\begin{array}{c} 1 \\ 0 \end{array}\right]", color=BLUE)
        eig3_vec.move_to(ORIGIN + np.array([0, -1.2, 0]))

        eig2_setup = MathTex(r"(A - 2I)\,v = \left[\begin{array}{cc} 1 & 1 \\ 0 & 0 \end{array}\right] v = 0", color=WHITE)
        eig2_setup.move_to(ORIGIN + np.array([0, 0.3, 0]))

        eig2_vec = MathTex(r"v_2 = \left[\begin{array}{c} 1 \\ -1 \end{array}\right]", color=RED)
        eig2_vec.move_to(ORIGIN + np.array([0, -1.2, 0]))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2.2, 2.2, 1],
            background_line_style={"stroke_color": GREY, "stroke_opacity": 0.4},
        )
        plane.move_to(ORIGIN)

        arrow_v1 = Arrow(start=[0, 0, 0], end=[1, 0, 0], color=BLUE, buff=0)
        arrow_v2 = Arrow(start=[0, 0, 0], end=[1, -1, 0], color=RED, buff=0)

        footer_label = Text("Eigenvectors only stretch, never rotate", color=YELLOW, font_size=26)
        footer_label.move_to(np.array([0, -2.3, 0]))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_00.mp3")  # [auto-injected] duration=4.90s
        _audio_dur_0 = 4.90  # [audio-sync] actual TTS duration
        # Step 1
        _scale_1 = max(1.0, (_audio_dur_0 * 0.7) / 1.800)
        self.set_subtitle("我們要求出這個二乘二矩陣 A 的特徵值與特徵向量。", run_time=_audio_dur_0)
        anim_time_1 = 1.800 * _scale_1
        self.play(Write(matrix_A), run_time=anim_time_1)
        remaining_1 = max(0.1, _audio_dur_0 - anim_time_1 + 0.1)
        self.wait(max(0.1, remaining_1))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_01.mp3")  # [auto-injected] duration=6.89s
        _audio_dur_1 = 6.89  # [audio-sync] actual TTS duration
        # Step 2
        _scale_2 = max(1.0, (_audio_dur_1 * 0.7) / 2.000)
        self.set_subtitle("特徵值來自特徵方程式：A 減去 lambda 乘以單位矩陣的行列式等於零。", run_time=_audio_dur_1)
        anim_time_2 = 2.000 * _scale_2
        self.play(Write(char_eq), run_time=anim_time_2)
        self.play(Circumscribe(char_eq, color=YELLOW))
        remaining_2 = max(0.1, _audio_dur_1 - anim_time_2 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_2))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_02.mp3")  # [auto-injected] duration=5.09s
        _audio_dur_2 = 5.09  # [audio-sync] actual TTS duration
        # Step 3
        _scale_3 = max(1.0, (_audio_dur_2 * 0.7) / 1.800)
        self.set_subtitle("將對角線各減去 lambda，就得到這個要計算的行列式。", run_time=_audio_dur_2)
        anim_time_3 = 1.800 * _scale_3
        self.play(ReplacementTransform(char_eq, char_det), run_time=anim_time_3)
        remaining_3 = max(0.1, _audio_dur_2 - anim_time_3 + 0.1)
        self.wait(max(0.1, remaining_3))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_03.mp3")  # [auto-injected] duration=6.12s
        _audio_dur_3 = 6.12  # [audio-sync] actual TTS duration
        # Step 4
        _scale_4 = max(1.0, (_audio_dur_3 * 0.7) / 1.800)
        self.set_subtitle("由於它是上三角矩陣，行列式就是對角線元素的乘積。", run_time=_audio_dur_3)
        anim_time_4 = 1.800 * _scale_4
        self.play(ReplacementTransform(char_det, char_expand), run_time=anim_time_4)
        remaining_4 = max(0.1, _audio_dur_3 - anim_time_4 + 0.1)
        self.wait(max(0.1, remaining_4))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_04.mp3")  # [auto-injected] duration=6.46s
        _audio_dur_4 = 6.46  # [audio-sync] actual TTS duration
        # Step 5
        _scale_5 = max(1.0, (_audio_dur_4 * 0.7) / 1.800)
        self.set_subtitle("令每個因式為零，得到特徵值 lambda 等於三與 lambda 等於二。", run_time=_audio_dur_4)
        anim_time_5 = 1.800 * _scale_5
        self.play(ReplacementTransform(char_expand, eigenvalues), run_time=anim_time_5)
        self.play(Indicate(eigenvalues, color=GREEN))
        remaining_5 = max(0.1, _audio_dur_4 - anim_time_5 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_5))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_05.mp3")  # [auto-injected] duration=5.50s
        _audio_dur_5 = 5.50  # [audio-sync] actual TTS duration
        # Step 6
        _scale_6 = max(1.0, (_audio_dur_5 * 0.7) / 2.000)
        self.set_subtitle("對於 lambda 等於三，我們解 A 減去三倍單位矩陣乘以 v 等於零。", run_time=_audio_dur_5)
        self.play(FadeOut(eigenvalues))
        anim_time_6 = 2.000 * _scale_6
        self.play(Write(eig3_setup), run_time=anim_time_6)
        remaining_6 = max(0.1, _audio_dur_5 - anim_time_6 + 0.1)
        self.wait(max(0.1, remaining_6))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_06.mp3")  # [auto-injected] duration=5.88s
        _audio_dur_6 = 5.88  # [audio-sync] actual TTS duration
        # Step 7
        _scale_7 = max(1.0, (_audio_dur_6 * 0.7) / 1.800)
        self.set_subtitle("這迫使第二個分量為零，得到特徵向量一、零。", run_time=_audio_dur_6)
        anim_time_7 = 1.800 * _scale_7
        self.play(Write(eig3_vec), run_time=anim_time_7)
        self.play(Circumscribe(eig3_vec, color=BLUE))
        remaining_7 = max(0.1, _audio_dur_6 - anim_time_7 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_7))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_07.mp3")  # [auto-injected] duration=5.88s
        _audio_dur_7 = 5.88  # [audio-sync] actual TTS duration
        # Step 8
        _scale_8 = max(1.0, (_audio_dur_7 * 0.7) / 1.800)
        self.set_subtitle("對於 lambda 等於二，同樣的過程得到特徵向量一、負一。", run_time=_audio_dur_7)
        self.play(FadeOut(eig3_setup), FadeOut(eig3_vec))
        anim_time_8 = 1.800 * _scale_8
        self.play(Write(eig2_setup), run_time=anim_time_8)
        self.play(Write(eig2_vec), run_time=1.0)
        self.play(Circumscribe(eig2_vec, color=RED))
        remaining_8 = max(0.1, _audio_dur_7 - anim_time_8 - 2.0 + 0.1)
        self.wait(max(0.1, remaining_8))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_08.mp3")  # [auto-injected] duration=4.68s
        _audio_dur_8 = 4.68  # [audio-sync] actual TTS duration
        # Step 9
        _scale_9 = max(1.0, (_audio_dur_8 * 0.7) / 2.000)
        self.set_subtitle("現在讓我們在座標平面上幾何地觀察這些特徵向量。", run_time=_audio_dur_8)
        self.play(FadeOut(matrix_A), FadeOut(eig2_setup), FadeOut(eig2_vec))
        anim_time_9 = 2.000 * _scale_9
        self.play(Create(plane), run_time=anim_time_9)
        remaining_9 = max(0.1, _audio_dur_8 - anim_time_9 + 0.1)
        self.wait(max(0.1, remaining_9))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_09.mp3")  # [auto-injected] duration=4.25s
        _audio_dur_9 = 4.25  # [audio-sync] actual TTS duration
        # Step 10
        _scale_10 = max(1.0, (_audio_dur_9 * 0.7) / 1.500)
        self.set_subtitle("這裡是從原點畫出的兩個特徵向量箭頭。", run_time=_audio_dur_9)
        anim_time_10 = 1.500 * _scale_10
        self.play(LaggedStart(Create(arrow_v1), Create(arrow_v2), lag_ratio=0.2), run_time=anim_time_10)
        remaining_10 = max(0.1, _audio_dur_9 - anim_time_10 + 0.1)
        self.wait(max(0.1, remaining_10))

        self.add_sound("/Users/liaozhenting/Desktop/LLManim_Agent/media/audio/Find_eigenvalues_and_0afa484a31/step_10.mp3")  # [auto-injected] duration=6.12s
        _audio_dur_10 = 6.12  # [audio-sync] actual TTS duration
        # Step 11
        _scale_11 = max(1.0, (_audio_dur_10 * 0.7) / 3.000)
        self.set_subtitle("看矩陣如何變換網格：特徵向量只會被拉伸，絕不旋轉。", run_time=_audio_dur_10)
        self.play(FadeIn(footer_label))
        matrix_transform = [[3, 1], [0, 2]]
        anim_time_11 = 3.000 * _scale_11
        self.play(
            ApplyMatrix(matrix_transform, plane),
            ApplyMatrix(matrix_transform, arrow_v1),
            ApplyMatrix(matrix_transform, arrow_v2),
            run_time=anim_time_11,
        )
        self.play(Indicate(footer_label, color=YELLOW))
        remaining_11 = max(0.1, _audio_dur_10 - anim_time_11 - 1.0 + 0.1)
        self.wait(max(0.1, remaining_11))