# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示捕食者與獵物兩個族群數量隨時間變化的動態模擬，狐狸和兔子圖示數量會根據微分方程模型增減，並顯示即時數量標籤。


from manim import *
import random
import numpy as np

class ShowTwoPopulations(Scene):
    def __init__(
        self,
        total_num_animals=80,
        start_num_foxes=40,
        start_num_rabbits=20,
        animal_height=0.5,
        final_wait_time=30,
        count_word_scale_val=1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.total_num_animals = total_num_animals
        self.start_num_foxes = start_num_foxes
        self.start_num_rabbits = start_num_rabbits
        self.animal_height = animal_height
        self.final_wait_time = final_wait_time
        self.count_word_scale_val = count_word_scale_val

    def construct(self):
        self.introduce_animals()
        self.evolve_system()

    def introduce_animals(self):
        foxes = self.foxes = VGroup(*[
            self.get_fox()
            for n in range(self.total_num_animals)
        ])
        rabbits = self.rabbits = VGroup(*[
            self.get_rabbit()
            for n in range(self.total_num_animals)
        ])
        foxes[self.start_num_foxes:].set_opacity(0)
        rabbits[self.start_num_rabbits:].set_opacity(0)

        fox, rabbit = examples = VGroup(foxes[0], rabbits[0])
        for mob in examples:
            mob.save_state()
            mob.set_height(3)
        examples.arrange(LEFT, buff=2)

        preditor, prey = words = VGroup(
            Text("Predator"),
            Text("Prey")
        )
        for mob, word in zip(examples, words):
            word.scale(1.5)
            word.next_to(mob, UP)
            self.play(
                FadeIn(mob, shift=DOWN),
                Write(word, run_time=1),
            )
        self.play(
            LaggedStart(*[
                mob.animate.restore() for mob in examples
            ]),
            LaggedStart(*[FadeOut(word) for word in words]),
            *[
                LaggedStart(*[
                    FadeIn(animal)
                    for animal in group[1:]
                ], run_time=4, lag_ratio=0.1)
                for group in [foxes, rabbits]
            ]
        )

    def evolve_system(self):
        foxes = self.foxes
        rabbits = self.rabbits
        phase_point = Dot(
            point=self.start_num_rabbits * RIGHT +
            self.start_num_foxes * UP,
            radius=0.01,
            color=WHITE
        )
        # 注意：move_along_vector_field 函數需要自行定義或從原代碼移植
        # 這裡假設它存在並能更新 phase_point 的位置
        self.add(move_along_vector_field(
            phase_point,
            preditor_prey_vector_field,
        ))

        def get_num_rabbits():
            return phase_point.get_center()[0]

        def get_num_foxes():
            return phase_point.get_center()[1]

        def get_updater(pop_size_getter):
            def update(animals):
                target_num = pop_size_getter()
                for n, animal in enumerate(animals):
                    animal.set_opacity(np.clip(target_num - n, 0, 1))
                target_int = int(np.ceil(target_num))
                tail = animals.submobjects[target_int:]
                random.shuffle(tail)
                animals.submobjects[target_int:] = tail

            return update

        foxes.add_updater(get_updater(get_num_foxes))
        rabbits.add_updater(get_updater(get_num_rabbits))

        # Add counts for foxes and rabbits
        labels = self.get_pop_labels()
        num_foxes = Integer(10)
        num_foxes.scale(self.count_word_scale_val)
        num_foxes.next_to(labels[0], RIGHT)
        num_foxes.align_to(labels[0][0][1], DOWN)
        num_rabbits = Integer(10)
        num_rabbits.scale(self.count_word_scale_val)
        num_rabbits.next_to(labels[1], RIGHT)
        num_rabbits.align_to(labels[1][0][1], DOWN)

        num_foxes.add_updater(lambda d: d.set_value(get_num_foxes()))
        num_rabbits.add_updater(lambda d: d.set_value(get_num_rabbits()))

        self.add(num_foxes, num_rabbits)

        for count in [num_foxes, num_rabbits]:
            count.add_updater(self.update_count_color)

        self.play(
            FadeIn(labels),
            *[
                UpdateFromAlphaFunc(count, lambda m, a: m.set_opacity(a))
                for count in (num_foxes, num_rabbits)
            ]
        )

        self.wait(self.final_wait_time)

    # Helpers

    def get_animal(self, name, color):
        result = SVGMobject(
            file_name=name,
            height=self.animal_height,
            fill_color=color,
        )
        # 註釋掉的代碼是原版處理子路徑的邏輯，在CE中可能不需要
        x_shift, y_shift = [
            (2 * random.random() - 1) * max_val
            for max_val in [
                config.frame_width / 2 - 2,
                config.frame_height / 2 - 2
            ]
        ]
        result.shift(x_shift * RIGHT + y_shift * UP)
        return result

    def get_fox(self):
        return self.get_animal("fox", FOX_COLOR)

    def get_rabbit(self):
        return self.get_animal("bunny", RABBIT_COLOR)

    def get_pop_labels(self):
        labels = VGroup(
            Text("# Foxes: "),
            Text("# Rabbits: "),
        )
        for label in labels:
            label.scale(self.count_word_scale_val)
        labels.arrange(RIGHT, buff=2)
        labels.to_edge(UP)
        return labels

    def update_count_color(self, count):
        count.set_color(interpolate_color(
            BLUE, RED, (count.get_value() - 20) / 30.0
        ))
        return count
