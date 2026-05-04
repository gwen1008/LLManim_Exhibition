# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示一系列四元數旋轉如何作用於一個 3D 稜柱體，同時顯示四元數值和旋轉軸。


from manim import *
import numpy as np

class ShowSeveralQuaternionRotations(ThreeDScene):
    def __init__(
        self,
        quaternions=[
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 1, 0],
            [1, 1, 1, -1],
            [0, -1, 2, 1],
            [1, 0, 0, -1],
            [1, -1, 0, 0],
            [1, -1, 1, 0],
            [1, -1, 1, -1],
            [1, 0, 0, 0],
        ],
        start_phi=70 * DEGREES,
        start_theta=-140 * DEGREES,
        ambient_rotation_rate=0.01,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.quaternions = quaternions
        self.start_phi = start_phi
        self.start_theta = start_theta
        self.ambient_rotation_rate = ambient_rotation_rate

    def construct(self):
        self.add_q_tracker()
        self.setup_labels()
        self.setup_camera_position()
        self.add_prism()
        self.add_axes()
        self.apply_quaternions()

    def add_q_tracker(self):
        # 假設 QuaternionTracker 是一個自定義類，用於追蹤四元數值
        # 如果不存在，我們用一個簡單的 Mobject 替代
        self.q_tracker = Mobject()
        self.q_tracker.value = np.array([1, 0, 0, 0], dtype=float)
        
        def normalize_value(mob):
            norm = np.linalg.norm(mob.value)
            if norm > 0:
                mob.value = mob.value / norm
        self.q_tracker.add_updater(lambda m: normalize_value(m))
        self.add(self.q_tracker)

    def setup_labels(self):
        # 定義顏色常量
        I_COLOR = RED
        J_COLOR = GREEN
        K_COLOR = BLUE
        
        # 創建左側四元數標籤
        left_q_label = self.create_quaternion_label([1, 0, 0, 0])
        # 創建右側四元數標籤
        right_q_label = self.create_quaternion_label([1, 0, 0, 0])
        
        # 為標籤添加括號
        for label in [left_q_label, right_q_label]:
            lp = MathTex("(")
            rp = MathTex(")")
            lp.next_to(label, LEFT, SMALL_BUFF)
            rp.next_to(label, RIGHT, SMALL_BUFF)
            label.add(lp, rp)
        
        # 創建點標籤
        point_label = MathTex(
            "xi+yj+zk",
            tex_to_color_map={
                "i": I_COLOR,
                "j": J_COLOR,
                "k": K_COLOR,
            }
        )
        
        # 排列所有標籤
        left_q_label.next_to(point_label, LEFT)
        right_q_label.next_to(point_label, RIGHT)
        group = VGroup(left_q_label, point_label, right_q_label)
        group.arrange(RIGHT)
        group.set_width(config.frame_width - 1)
        group.to_edge(UP)
        
        # 添加背景矩形
        bg_rect = BackgroundRectangle(group)
        self.add_fixed_orientation_mobjects(bg_rect)
        
        # 為每個標籤添加括號和文字說明
        for label, text in zip(group, ["$q$", "Some 3d point", "$q^{-1}$"]):
            brace = Brace(label, DOWN)
            text_mob = Tex(text)
            if text_mob.width > brace.width:
                text_mob.match_width(brace)
            text_mob.next_to(brace, DOWN, buff=SMALL_BUFF)
            text_mob.add_background_rectangle()
            label.add(brace, text_mob)
        
        # 將標籤組添加到固定方向物件
        self.add_fixed_orientation_mobjects(*group)
        
        # 為左側標籤添加更新器
        def update_left_label(m):
            m.set_value(self.q_tracker.value)
            self.add_fixed_orientation_mobjects(m)
        left_q_label.add_updater(update_left_label)
        
        # 為右側標籤添加更新器
        def update_right_label(m):
            # 假設 quaternion_conjugate 函數存在
            conj = self.quaternion_conjugate(self.q_tracker.value)
            m.set_value(conj)
            self.add_fixed_orientation_mobjects(m)
        right_q_label.add_updater(update_right_label)

    def setup_camera_position(self):
        self.set_camera_orientation(
            phi=self.start_phi,
            theta=self.start_theta,
        )
        self.begin_ambient_camera_rotation(
            rate=self.ambient_rotation_rate
        )

    def add_prism(self):
        prism = self.prism = self.get_prism()
        
        def update_prism(p):
            p.become(self.get_prism(self.q_tracker.value))
        
        prism.add_updater(update_prism)
        self.add(prism)

    def add_axes(self):
        axes = self.axes = always_redraw(self.get_axes)
        self.add(axes)

    def apply_quaternions(self):
        for quat in self.quaternions:
            self.change_q(quat)
            self.wait(2)

    def get_unrotated_prism(self):
        # 假設 RandyPrism 是一個自定義 3D 物體
        # 這裡用一個立方體替代
        prism = Cube(side_length=2)
        prism.set_style(fill_opacity=0.5, stroke_width=2)
        return prism

    def get_prism(self, quaternion=None):
        if quaternion is None:
            quaternion = [1, 0, 0, 0]
        
        prism = self.get_unrotated_prism()
        angle, axis = self.angle_axis_from_quaternion(quaternion)
        prism.rotate(angle=angle, axis=axis, about_point=ORIGIN)
        return prism

    def get_axes(self):
        prism = self.prism
        # 獲取立方體六個面的中心點
        centers = []
        for face in prism:
            centers.append(face.get_center())
        
        axes = VGroup()
        for i in range(3):
            for u in [-1, 1]:
                vect = np.zeros(3)
                vect[i] = u
                
                # 計算每個中心點在向量方向上的投影
                dots = [np.dot(normalize(c), vect) for c in centers]
                max_i = np.argmax(dots)
                ec = centers[max_i]
                
                p1 = np.zeros(3)
                p1[i] = ec[i]
                p1 *= dots[max_i]
                p2 = 10 * vect
                
                line = Line(p1, p2)
                axes.add(line)
        
        axes.set_stroke(GREY_B, 1)
        return axes

    def change_q(self, value, run_time=3, added_anims=None, **kwargs):
        if added_anims is None:
            added_anims = []
        
        # 創建動畫來改變四元數值
        def update_q_tracker(mob, alpha):
            start = self.q_tracker.value.copy()
            end = np.array(value, dtype=float)
            # 線性插值
            self.q_tracker.value = start + alpha * (end - start)
        
        self.play(
            UpdateFromAlphaFunc(self.q_tracker, update_q_tracker),
            *added_anims,
            run_time=run_time,
            **kwargs
        )

    # 輔助函數
    def create_quaternion_label(self, value):
        # 創建一個簡單的文字標籤來顯示四元數
        label = Text(f"{value[0]:.2f} + {value[1]:.2f}i + {value[2]:.2f}j + {value[3]:.2f}k")
        label.set_value = lambda v: label.become(
            Text(f"{v[0]:.2f} + {v[1]:.2f}i + {v[2]:.2f}j + {v[3]:.2f}k")
        )
        return label

    def quaternion_conjugate(self, q):
        # 計算四元數的共軛
        return np.array([q[0], -q[1], -q[2], -q[3]])

    def angle_axis_from_quaternion(self, q):
        # 從四元數提取旋轉角度和軸
        q = np.array(q, dtype=float)
        norm = np.linalg.norm(q)
        if norm > 0:
            q = q / norm
        
        angle = 2 * np.arccos(q[0])
        if np.abs(q[0]) < 1 - 1e-6:
            axis = q[1:] / np.sqrt(1 - q[0]**2)
        else:
            axis = np.array([1, 0, 0])
        
        return angle, axis
