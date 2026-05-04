# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個三維場景，包含圓柱體、圓柱蓋以及將圓柱體展開的視覺效果，並提供投影功能將點映射到圓柱表面。



from manim import *
class SphereCylinderScene(ThreeDScene):
    def __init__(self, cap_config=None, **kwargs):
        super().__init__(**kwargs)
        if cap_config is None:
            cap_config = {
                "stroke_width": 1,
                "stroke_color": WHITE,
                "fill_color": BLUE_D,
                "fill_opacity": 1,
            }
        self.cap_config = cap_config
        # 假設 sphere_config 在子類中定義
        self.sphere_config = {}

    def get_cylinder(self, **kwargs):
        config = {**self.sphere_config, **kwargs}
        return Cylinder(**config)

    def get_cylinder_caps(self):
        R = self.sphere_config["radius"]
        caps = VGroup(*[
            Circle(
                radius=R,
                **self.cap_config,
            ).shift(R * vect)
            for vect in [IN, OUT]
        ])
        # ManimCE 中 3D 物體自動具有深度渲染，無需 set_shade_in_3d
        return caps

    def get_unwrapped_cylinder(self):
        # 假設 UnwrappedCylinder 是自定義類，需在代碼中定義
        return UnwrappedCylinder(**self.sphere_config)

    def get_xy_plane(self):
        pass

    def get_ghost_surface(self, surface):
        result = surface.copy()
        result.set_fill(BLUE_E, opacity=0.5)
        result.set_stroke(WHITE, width=0.5, opacity=0.5)
        return result

    def project_point(self, point):
        radius = self.sphere_config["radius"]
        result = np.array(point)
        norm = np.linalg.norm(result[:2])
        if norm > 0:
            result[:2] = result[:2] / norm * radius
        return result

    def project_mobject(self, mobject):
        return mobject.apply_function(self.project_point)
