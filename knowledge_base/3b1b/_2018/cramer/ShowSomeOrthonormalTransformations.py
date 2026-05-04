# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示一系列隨機的正交變換，包括旋轉和可能的鏡射，應用於平面上的向量網格。


from manim import *
import numpy as np

class ShowSomeOrthonormalTransformations(LinearTransformationScene):
    def __init__(self, random_seed=1, n_angles=7, **kwargs):
        super().__init__(**kwargs)
        self.random_seed = random_seed
        self.n_angles = n_angles

    def construct(self):
        np.random.seed(self.random_seed)
        for x in range(self.n_angles):
            angle = TAU * np.random.random() - TAU / 2
            # 建立 2D 旋轉矩陣
            matrix = np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]
            ])
            if x in [2, 4]:
                matrix[:, 1] *= -1
            self.apply_matrix(matrix, run_time=1)
            self.wait()
