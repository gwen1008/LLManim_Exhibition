"""測試 SubtitleManagerV2 跟動畫並行。

預期：
- 字幕「測試字幕跑 6 秒」從 t=0 顯示到 t=6
- 動畫 Write(eq) 從 t=0 跑到 t=2
- self.wait(4) 從 t=2 到 t=6
- 場景總長 6 秒（不是 6+2=8 秒）

用 `manim -ql evaluation/benchmark_set/test_subtitle_v2.py TestScene` 跑。
"""
from manim import *
import sys
sys.path.insert(0, "evaluation/benchmark_set")
from subtitle_manager_v2 import SubtitleManagerV2


class TestScene(Scene):
    def construct(self):
        self._sm = SubtitleManagerV2(self)
        self.set_subtitle = self._sm.show

        # 場景一：字幕跑 6 秒，動畫只 2 秒，靠 wait(4) 補齊
        eq = MathTex(r"2 + 3 = 5", color=YELLOW).scale(1.5)

        self.set_subtitle("這是測試字幕，應該跟動畫並行顯示六秒。", run_time=6.0)
        self.play(Write(eq), run_time=2.0)
        self.wait(4.0)

        # 場景二：第二段字幕、動畫並行
        eq2 = MathTex(r"= 5", color=GREEN).scale(2.0).next_to(eq, DOWN)

        self.set_subtitle("第二段字幕測試多句切換，看看是否流暢。", run_time=5.0)
        self.play(Write(eq2), run_time=1.5)
        self.wait(3.5)
