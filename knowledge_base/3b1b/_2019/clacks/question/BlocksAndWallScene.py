# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示兩個滑動方塊在牆壁和地板之間碰撞的物理模擬，包含碰撞計數器、閃光效果和聲音。



from manim import *
class BlocksAndWallScene(Scene):
    def __init__(
        self,
        include_sound=True,
        collision_sound="clack.wav",
        count_clacks=True,
        counter_group_shift_vect=LEFT,
        sliding_blocks_config={},
        floor_y=-2,
        wall_x=-6,
        n_wall_ticks=15,
        counter_label="\\# Collisions: ",
        show_flash_animations=True,
        min_time_between_sounds=0.004,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.include_sound = include_sound
        self.collision_sound = collision_sound
        self.count_clacks = count_clacks
        self.counter_group_shift_vect = counter_group_shift_vect
        self.sliding_blocks_config = sliding_blocks_config
        self.floor_y = floor_y
        self.wall_x = wall_x
        self.n_wall_ticks = n_wall_ticks
        self.counter_label = counter_label
        self.show_flash_animations = show_flash_animations
        self.min_time_between_sounds = min_time_between_sounds

    def setup(self):
        self.track_time()
        self.add_floor_and_wall()
        self.add_blocks()
        if self.show_flash_animations:
            self.add_flash_animations()

        if self.count_clacks:
            self.add_counter()

    def add_floor_and_wall(self):
        self.floor = self.get_floor()
        self.wall = self.get_wall()
        self.add(self.floor, self.wall)

    def add_blocks(self):
        self.blocks = SlidingBlocks(self, **self.sliding_blocks_config)
        if hasattr(self.blocks, "clack_data"):
            self.clack_data = self.blocks.clack_data
        self.add(self.blocks)

    def add_flash_animations(self):
        self.clack_flashes = ClackFlashes(self.clack_data)
        self.add(self.clack_flashes)

    def track_time(self):
        time_tracker = ValueTracker()
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(time_tracker)
        self.get_time = time_tracker.get_value

    def add_counter(self):
        self.n_clacks = 0
        counter_label = MathTex(self.counter_label)
        counter_mob = Integer(self.n_clacks)
        counter_mob.next_to(
            counter_label[-1], RIGHT,
        )
        counter_mob.align_to(counter_label[-1][-1], DOWN)
        counter_group = VGroup(
            counter_label,
            counter_mob,
        )
        counter_group.to_corner(UR)
        counter_group.shift(self.counter_group_shift_vect)
        self.add(counter_group)

        self.counter_mob = counter_mob

    def get_wall(self):
        height = (config.frame_height / 2) - self.floor_y
        wall = Wall(height=height)
        wall.shift(self.wall_x * RIGHT)
        wall.to_edge(UP, buff=0)
        return wall

    def get_floor(self):
        floor = Line(self.wall_x * RIGHT, config.frame_width * RIGHT / 2)
        floor.shift(self.floor_y * UP)
        return floor

    def update_num_clacks(self, n_clacks):
        if hasattr(self, "n_clacks"):
            if n_clacks == self.n_clacks:
                return
            self.counter_mob.set_value(n_clacks)

    def add_clack_sounds(self, clack_data):
        clack_file = self.collision_sound
        total_time = self.get_time()
        times = [
            time
            for location, time in clack_data
            if time < total_time
        ]
        last_time = 0
        for time in times:
            d_time = time - last_time
            if d_time < self.min_time_between_sounds:
                continue
            last_time = time
            self.add_sound(
                clack_file,
                time_offset=(time - total_time),
                gain=-20,
            )
        return self

    def tear_down(self):
        super().tear_down()
        if self.include_sound:
            self.add_clack_sounds(self.clack_data)
