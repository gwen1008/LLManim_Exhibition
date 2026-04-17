# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示帶電粒子在隨時間變化的向量場中運動，向量場由粒子自身電荷產生並持續更新。



from manim import *
class ChangingElectricField(Scene):
    def __init__(self, vector_field_config={}, **kwargs):
        super().__init__(**kwargs)
        self.vector_field_config = vector_field_config

    def construct(self):
        particles = self.get_particles()
        vector_field = self.get_vector_field()

        def update_vector_field(vector_field):
            new_field = self.get_vector_field()
            # 在ManimCE中，Transform不能直接更新，需要創建新的動畫
            # 這裡改為直接替換vector_field的內容
            vector_field.become(new_field)
            vector_field.func = new_field.func

        def update_particles(particles, dt):
            func = vector_field.func
            for particle in particles:
                force = func(particle.get_center())
                particle.velocity += force * dt
                particle.shift(particle.velocity * dt)

        # ManimCE中的更新器語法不同
        vector_field.add_updater(lambda m, dt: update_vector_field(m))
        particles.add_updater(lambda m, dt: update_particles(m, dt))
        
        self.add(vector_field, particles)
        self.wait(20)

    def get_particles(self):
        particles = self.particles = VGroup()
        for n in range(9):
            if n % 2 == 0:
                # 假設get_proton和get_electron是自定義函數
                # 如果沒有定義，用簡單的圓形代替
                particle = Circle(radius=0.2, color=RED, fill_opacity=0.8)
                particle.charge = +1
            else:
                particle = Circle(radius=0.2, color=BLUE, fill_opacity=0.8)
                particle.charge = -1
            particle.velocity = np.random.normal(0, 0.1, 3)
            particles.add(particle)
            particle.shift(np.random.normal(0, 0.2, 3))

        particles.arrange_in_grid(buff=LARGE_BUFF)
        return particles

    def get_vector_field(self):
        # 假設get_force_field_func是自定義函數
        # 如果沒有定義，創建一個簡單的向量場函數
        def simple_force_field_func(point):
            total_force = np.zeros(3)
            for particle, charge in zip(self.particles, [p.charge for p in self.particles]):
                center = particle.get_center()
                diff = center - point
                dist = np.linalg.norm(diff)
                if dist > 0.1:  # 避免除以零
                    total_force += charge * diff / (dist**3)
            return total_force
        
        func = simple_force_field_func
        self.vector_field = VectorField(func, **self.vector_field_config)
        return self.vector_field
