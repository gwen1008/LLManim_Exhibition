# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示雷達操作員面對不確定性時，雷達波脈衝與機率分佈雲的動態變化。



from manim import *
class RadarOperatorUncertainty(Scene):
    def construct(self):
        dish = RadarDish()
        dish.scale(3)
        dish.move_to(4*RIGHT + 2*DOWN)
        dish_words = MathTex(r"\text{3b1b industrial} \\ \text{enterprises}")
        dish_words.scale(0.25)
        dish_words.set_stroke(BLACK, 0.5)
        dish_words.set_color(BLACK)
        dish_words.move_to(dish, DOWN)
        dish_words.shift(0.1*(UP+2*LEFT))  # SMALL_BUFF 約為 0.1
        dish.add(dish_words)
        
        randy = Randolph()
        randy.next_to(dish, LEFT, aligned_edge=DOWN)
        bubble = randy.get_bubble(
            width=7,
            height=4,
        )

        echo_object = Square()
        echo_object.move_to(dish)
        echo_object.shift(FRAME_WIDTH/2 * RIGHT)  # FRAME_X_RADIUS 替換為 FRAME_WIDTH/2
        pulse = RadarPulse(dish, echo_object, speed=6)

        plane = NumberPlane().scale(0.5)  # Plane() 改為 NumberPlane()
        plane.move_to(bubble.get_bubble_center() + LEFT)
        plane_cloud = ProbabalisticMobjectCloud(
            plane, 
            fill_opacity=0.3,
            n_copies=10,
        )
        plane_gdw = plane_cloud.gaussian_distribution_wrapper

        vector_cloud = ProbabalisticVectorCloud(
            center_func=plane_gdw.get_center,
        )
        vector_gdw = vector_cloud.gaussian_distribution_wrapper
        vector_gdw.scale(0.05)
        vector_gdw.move_to(plane_gdw)
        vector_gdw.shift(2*RIGHT)

        self.add(randy, dish, bubble, plane_cloud, pulse)
        self.play(randy.animate.change("confused"))
        self.wait(3)
        self.add(vector_cloud)
        for i in range(3):
            for plane_factor, vector_factor, freq in [(0.05, 10, 0.01), (20, 0.1, 0.1)]:
                pulse.internal_time = 0
                pulse.frequency = freq
                self.play(
                    randy.animate.change("pondering", plane),
                    plane_gdw.animate.scale(plane_factor),
                    vector_gdw.animate.scale(vector_factor),
                )
                self.wait(2)
