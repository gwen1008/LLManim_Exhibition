# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示老師舉手制止學生們各自散開的動畫場景，老師說「等等！」後學生們恢復原位。



from manim import *
class Introduction(TeacherStudentsScene):
    def __init__(self, random_seed=2, **kwargs):
        super().__init__(**kwargs)
        self.random_seed = random_seed

    def construct(self):
        random.seed(self.random_seed)
        
        self.play(
            Animation(Dot(self.hold_up_spot)),  # VectorizedPoint 替代
            self.teacher.animate.change("raise_right_hand"),
        )
        self.play_student_changes(
            "angry", "sassy", "pleading"
        )
        self.wait()

        movements = []
        for student in self.students:
            student.center_tracker = Dot()  # VectorizedPoint 替代
            student.center_tracker.move_to(student)
            student.center_tracker.save_state()
            student.add_updater(
                lambda m: m.move_to(m.center_tracker)
            )
            # always_shift 手動實現
            student.center_tracker.add_updater(
                lambda m, dt: m.shift((DOWN + 3 * LEFT) * 1.5 * random.random() * dt)
            )
            movements.append(student.center_tracker)
        self.add(*movements)
        self.play_student_changes(
            "pondering", "sad", "concerned_musician",
            look_at=10 * LEFT + 2 * DOWN
        )
        self.teacher_says(
            "Wait, wait, wait!",
            target_mode="surprised"
        )
        self.remove(*movements)
        for student in self.students:
            student.center_tracker.clear_updaters()
        self.play(
            self.change_students(*3 * ["hesitant"]),
            *[
                Restore(student.center_tracker)
                for student in self.students
            ]
        )
        # 清理 updater
        for student in self.students:
            student.clear_updaters()
