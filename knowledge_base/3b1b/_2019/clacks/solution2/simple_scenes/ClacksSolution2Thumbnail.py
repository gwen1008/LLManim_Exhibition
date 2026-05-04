# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示兩個物理場景的縮圖：左側是滑動方塊系統，右側是光線在鏡面反射的軌跡，中間用紅色箭頭連接。



from manim import *
class ClacksSolution2Thumbnail(Scene):
    def construct(self):
        self.add_scene1()
        self.add_scene2()

        arrow = Arrow(
            self.block_word.get_top(),
            self.light_dot.get_bottom(),
            tip_length=0.75,
            stroke_width=0.2,
            color=RED,
            buff=0.5,
        )
        arrow.add_to_back(arrow.copy().set_stroke(BLACK, 20))
        self.add(arrow)
        
        # 註解掉的代碼（原代碼中有 return 語句，後面的部分不會執行）
        # arrow = MathTex("\\Updownarrow")
        # arrow.set_height(2)
        # arrow.set_color(YELLOW)
        # arrow.set_stroke(Color("red"), 2, background=True)
        # self.add(arrow)

    def add_scene1(self):
        # 注意：Thumbnail 類別需要自行定義或替換
        scene1 = Thumbnail(
            sliding_blocks_config={
                "block1_config": {
                    "label_text": "$100^{d}$ kg",
                    "distance": 8,
                },
            }
        )
        group = Group(*scene1.mobjects)
        group.scale(0.75, about_point=ORIGIN)
        group.shift(1.5 * DOWN + 3 * LEFT)
        scene1.remove(scene1.question)
        self.add(*scene1.mobjects)

        black_rect = FullScreenFadeRectangle(fill_opacity=1)
        black_rect.shift(3.5 * UP)
        self.add(black_rect)

        word = Text("Blocks")
        word.set_color(YELLOW)
        word.scale(3)
        word.to_corner(DR, buff=LARGE_BUFF)
        word.shift(0.5 * LEFT)
        self.block_word = word
        self.add(word)

    def add_scene2(self):
        # 注意：ReflectWorldThroughMirrorNew 類別需要自行定義或替換
        scene2 = ReflectWorldThroughMirrorNew(
            skip_animations=True,
            file_writer_config={
                "write_to_movie": False,
            },
            end_at_animation_number=18,
            center=ORIGIN,
        )
        worlds = VGroup(scene2.world, *scene2.reflected_worlds)
        mirrors = VGroup(*[rw[1] for rw in worlds])
        mirrors.set_stroke(width=5)
        triangles = VGroup(*[rw[0] for rw in worlds])
        trajectories = VGroup(
            scene2.trajectory,
            *scene2.reflected_trajectories
        )
        trajectories.set_stroke(YELLOW, 1)

        beams1, beams2 = [
            scene2.get_shooting_beam_anims(
                path,
                max_stroke_width=20,
                max_time_width=1,
                num_flashes=50,
            )
            for path in [
                scene2.trajectory,
                scene2.ghost_trajectory,
            ]
        ]
        beams = beams1 + beams2
        beams = beams2
        flashes = VGroup()
        for beam in beams:
            beam.update(0.5)
            flashes.add(beam.mobject)

        dot = self.light_dot = Dot(color=YELLOW, radius=0.1)
        dot.move_to(flashes[0].get_left())
        flashes.add(dot)

        self.add(triangles, mirrors)
        self.add(trajectories[0].set_stroke(width=2))
        self.add(flashes)

        word = Text("Light beam")
        word.scale(3.5)
        word.set_color(YELLOW)
        word.add_to_back(word.copy().set_stroke(
            BLACK, 25,
        ))
        word.next_to(dot, UR)
        word.shift(-word.get_center()[0] * RIGHT)
        word.shift(SMALL_BUFF * RIGHT)
        self.light_word = word
        self.add(word)
