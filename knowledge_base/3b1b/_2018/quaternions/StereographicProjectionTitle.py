# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示「立體投影」標題從旋轉變形到最終位置的動畫過程。



from manim import *
class StereographicProjectionTitle(Scene):
    def construct(self):
        title = Text("Stereographic projection")
        final_title = title.copy()
        final_title.set_width(10)
        final_title.to_edge(UP)

        title.rotate(-90 * DEGREES)
        title.next_to(RIGHT, RIGHT, buff=SMALL_BUFF)
        # 在 ManimCE 中，apply_complex_function 需要手動實現或替換
        # 這裡假設原意是進行某種變換，我們用縮放和旋轉模擬類似效果
        title.scale(1.5)  # 替代 apply_complex_function(np.exp) 的視覺效果
        title.rotate(90 * DEGREES)
        title.set_height(6)
        title.to_edge(UP)

        self.play(Write(title))
        self.play(Transform(title, final_title), run_time=2)
        self.wait()
