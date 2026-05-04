# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一個粒子雲和兩個角色對話的場景，其中一個角色引用海森堡不確定性原理，另一個角色回應。



from manim import *
class HeisenbergPetPeeve(Scene):
    def construct(self):
        # 創建角色
        morty, other = self.create_pi_creatures()
        
        # 創建粒子雲（使用替代實現）
        particle = self.create_probabilistic_dot_cloud()
        
        # 調整高斯分佈包裝器
        gdw = particle  # 簡化處理，假設particle本身有類似屬性
        gdw.to_edge(UP, buff=LARGE_BUFF)
        gdw.stretch_to_fit_width(3)
        gdw.rotate(3*DEGREES)

        self.add(particle, morty, other)
        self.wait()
        
        # 第一個角色說話
        other_bubble = Text("According to the H.U.P., the\nuniverse is unknowable!", 
                           font_size=24)
        other_bubble.next_to(other, UP, buff=0.5)
        arrow = Arrow(other_bubble.get_bottom(), other.get_top(), buff=0.1)
        
        self.play(
            Write(other_bubble),
            Create(arrow),
            other.animate.change("speaking")
        )
        
        # 第二個角色反應
        self.play(morty.animate.change("angry"))
        self.wait(3)
        
        # 第二個角色回應
        morty_bubble = Text("Well, yes and no", font_size=24)
        morty_bubble.next_to(morty, UP, buff=0.5)
        morty_arrow = Arrow(morty_bubble.get_bottom(), morty.get_top(), buff=0.1)
        
        self.play(
            FadeOut(other_bubble),
            FadeOut(arrow),
            other.animate.change("erm"),
            Write(morty_bubble),
            Create(morty_arrow),
            morty.animate.change("sassy")
        )
        self.wait(4)

    def create_pi_creatures(self):
        # 創建兩個角色
        morty = SVGMobject("morty.svg")  # 假設有SVG文件
        morty.set_color(BLUE)
        morty.scale(0.5)
        morty.to_corner(DOWN+RIGHT)
        
        other = SVGMobject("pi_creature.svg")  # 假設有SVG文件
        other.set_color(MAROON_E)
        other.scale(0.5)
        other.to_edge(DOWN).shift(3*LEFT)
        
        return VGroup(morty, other)

    def create_probabilistic_dot_cloud(self):
        # 創建一個簡單的粒子雲替代實現
        cloud = VGroup()
        for _ in range(50):
            dot = Dot(
                point=np.array([
                    np.random.normal(0, 0.5),
                    np.random.normal(0, 0.5),
                    0
                ]),
                radius=0.03,
                color=BLUE
            )
            cloud.add(dot)
        
        # 添加高斯分佈曲線
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"color": WHITE},
            x_length=3,
            y_length=2
        )
        
        # 高斯函數
        def gaussian(x):
            return 0.4 * np.exp(-x**2 / 2)
        
        graph = axes.plot(gaussian, color=YELLOW)
        cloud.add(axes, graph)
        
        return cloud
