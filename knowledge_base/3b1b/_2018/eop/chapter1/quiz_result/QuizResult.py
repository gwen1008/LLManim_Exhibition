# Source: 3b1b/_2018/eop/chapter1/quiz_result.py
# Description: [3b1b translated] 展示一個班級學生在測驗中的成績分佈，從個別答題結果到成績直方圖，最後以隨機閃爍效果強調概率概念。


from manim import *
import numpy as np

class QuizResult(PiCreatureScene):
    def __init__(self, pi_creatures_start_on_screen=False, random_seed=0, **kwargs):
        super().__init__(pi_creatures_start_on_screen=pi_creatures_start_on_screen, **kwargs)
        self.random_seed = random_seed
    
    def construct(self):
        np.random.seed(self.random_seed)
        
        def get_example_quiz():
            quiz = get_quiz(
                "Define ``Brachistochrone'' ",
                "Define ``Tautochrone'' ",
                "Define ``Cycloid'' ",
            )
            rect = SurroundingRectangle(quiz, buff=0)
            rect.set_fill(color=BLACK, opacity=1)
            rect.set_stroke(width=0)
            quiz.add_to_back(rect)
            return quiz
        
        def get_slot_group(points, include_qs=False):
            # 簡化實現：創建表示答題結果的視覺元素
            group = VGroup()
            for i, point in enumerate(points):
                if point:
                    shape = Square(side_length=0.3, color=GREEN, fill_opacity=0.5)
                else:
                    shape = Square(side_length=0.3, color=RED, fill_opacity=0.5)
                if include_qs:
                    label = Text(f"Q{i+1}", font_size=12)
                    label.next_to(shape, UP, buff=0.1)
                    group.add(VGroup(shape, label))
                else:
                    group.add(shape)
            group.arrange(RIGHT, buff=0.1)
            return group
        
        highlight_color = WHITE
        
        nb_students_x = 5
        nb_students_y = 3
        spacing_students_x = 2.0
        spacing_students_y = 2.2
        
        # 創建學生群組
        all_students = VGroup()
        for i in range(nb_students_x * nb_students_y):
            pi = PiCreature(color=BLUE_E).scale(0.3)
            all_students.add(pi)
        
        student_points = []
        grades = []
        grades_count = []
        hist_y_values = np.zeros(4)
        
        # 佈置學生位置並生成成績
        for i in range(nb_students_x):
            for j in range(nb_students_y):
                idx = i * nb_students_y + j
                x = i * spacing_students_x
                y = j * spacing_students_y
                all_students[idx].move_to([x, y, 0])
                
                # 隨機生成答題結果
                q1 = np.random.choice([True, False])
                q2 = np.random.choice([True, False])
                q3 = np.random.choice([True, False])
                student_points.append([q1, q2, q3])
                
                # 計算成績
                grade = q1 * 1 + q2 * 1 + q3 * 1
                grades.append(grade)
                hist_y_values[grade] += 1
                
                # 計算該成績出現的次數
                grade_count = grades.count(grade)
                grades_count.append(grade_count)
        
        all_students.move_to(ORIGIN)
        self.pi_creatures = all_students
        self.play(FadeIn(all_students))
        
        # 創建測驗卷
        all_quizzes = VGroup()
        quiz = get_example_quiz().scale(0.2)
        for pi in all_students:
            quiz_copy = quiz.copy()
            quiz_copy.next_to(pi, UP)
            all_quizzes.add(quiz_copy)
        
        master_quiz = get_example_quiz()
        self.play(Write(master_quiz), run_time=2)
        self.wait()
        self.play(ReplacementTransform(
            VGroup(master_quiz), all_quizzes,
            run_time=2,
            lag_ratio=0.5
        ))
        self.wait(2)
        
        # 顯示成績
        grades_mob = VGroup()
        for (pi, quiz, grade) in zip(all_students, all_quizzes, grades):
            grade_mob = MathTex(str(grade) + "/3")
            grade_mob.move_to(quiz)
            grades_mob.add(grade_mob)
        
        self.remove(master_quiz)
        self.wait()
        self.play(
            FadeOut(all_quizzes),
            FadeIn(grades_mob)
        )
        
        # 顯示答題結果
        students_points_mob = VGroup()
        for (pi, quiz, points) in zip(all_students, all_quizzes, student_points):
            slot = get_slot_group(points, include_qs=False)
            slot.scale(0.5).move_to(quiz)
            students_points_mob.add(slot)
        
        self.wait()
        self.play(
            FadeOut(grades_mob),
            FadeIn(students_points_mob)
        )
        
        all_students.save_state()
        students_points_mob.save_state()
        self.wait()
        
        # 突出顯示兩個學生
        randy = all_students[0]
        morty = all_students[nb_students_y]
        all_other_students = VGroup(*all_students)
        all_other_students.remove(randy, morty)
        
        randy_points = students_points_mob[0]
        morty_points = students_points_mob[nb_students_y]
        all_other_points = VGroup(*students_points_mob)
        all_other_points.remove(randy_points, morty_points)
        
        self.play(
            all_other_students.animate.set_opacity(0.2),
            all_other_points.animate.set_opacity(0.2),
        )
        self.wait()
        
        scale = 1.5
        self.play(randy_points.animate.scale(scale))
        self.play(randy_points.animate.scale(1.0/scale), morty_points.animate.scale(scale))
        self.play(morty_points.animate.scale(1.0/scale))
        
        self.wait()
        self.play(
            Restore(all_students),
            Restore(students_points_mob),
        )
        
        # 放大所有答題結果
        self.wait()
        anims = []
        for points in students_points_mob:
            anims.append(points.animate.scale(scale))
        self.play(*anims)
        
        self.wait()
        anims = []
        for points in students_points_mob:
            anims.append(points.animate.scale(1.0/scale))
        self.play(*anims)
        
        # 根據成績重新排列學生
        anims = []
        anchor_point = 3 * DOWN + 1 * LEFT
        for (pi, grade, grade_count) in zip(all_students, grades, grades_count):
            anims.append(pi.animate.move_to(anchor_point + grade * RIGHT + grade_count * UP))
        anims.append(FadeOut(students_points_mob))
        
        self.wait()
        self.play(*anims)
        
        # 添加成績標籤
        grade_labels = VGroup()
        for i in range(4):
            grade_label = Integer(i, color=highlight_color)
            grade_label.move_to(i * RIGHT)
            grade_labels.add(grade_label)
        grade_labels.next_to(all_students, DOWN)
        out_of_label = Text("out of 3", color=highlight_color)
        out_of_label.next_to(grade_labels, RIGHT, buff=MED_LARGE_BUFF)
        grade_labels.add(out_of_label)
        self.wait()
        self.play(Write(grade_labels))
        
        # 創建直方圖
        class Histogram(VGroup):
            def __init__(self, x_values, y_values, **kwargs):
                super().__init__(**kwargs)
                self.bars = VGroup()
                max_y = max(y_values)
                for i, (x, y) in enumerate(zip(x_values, y_values)):
                    if y > 0:
                        bar = Rectangle(
                            width=0.8,
                            height=y/max_y * 3,
                            fill_color=BLUE,
                            fill_opacity=0.7,
                            stroke_color=WHITE,
                            stroke_width=2
                        )
                        bar.move_to([x, bar.height/2, 0])
                        self.bars.add(bar)
                self.add(self.bars)
        
        grade_hist = Histogram(
            np.ones(4),
            hist_y_values,
        )
        grade_hist.move_to(all_students)
        
        self.wait()
        self.play(
            FadeIn(grade_hist),
            FadeOut(all_students)
        )
        
        # 添加學生數量標籤
        nb_students_label = Text("\\# of students", color=highlight_color)
        nb_students_label.move_to(5 * RIGHT + 1 * UP)
        arrows = VGroup(*[
            Arrow(
                nb_students_label.get_left(),
                grade_hist.bars[i].get_center(),
                color=highlight_color
            )
            for i in range(len(grade_hist.bars))
        ])
        self.wait()
        self.play(Write(nb_students_label), LaggedStart(*[GrowArrow(arrow) for arrow in arrows]))
        
        # 轉換為百分比
        percentage_label = Text("\\% of students", color=highlight_color)
        percentage_label.move_to(nb_students_label)
        percentages = hist_y_values / (nb_students_x * nb_students_y) * 100
        
        # 創建百分比標籤
        y_labels_group = VGroup()
        for i, percentage in enumerate(percentages):
            label = DecimalNumber(
                percentage,
                num_decimal_places=1,
                unit="\\%",
                color=highlight_color
            )
            label.scale(0.7)
            if i < len(grade_hist.bars):
                label.next_to(grade_hist.bars[i], UP, buff=0.1)
            y_labels_group.add(label)
        
        self.wait()
        self.play(
            *[FadeIn(label) for label in y_labels_group],
            ReplacementTransform(nb_students_label, percentage_label)
        )
        
        # 在角落顯示縮小的學生群組
        self.remove(all_quizzes)
        for i, pi in enumerate(all_students):
            x = i % 5
            y = i // 5
            pi.move_to(x * RIGHT + y * UP)
        all_students.scale(0.8)
        all_students.to_corner(DL)
        self.wait()
        self.play(FadeIn(all_students))
        
        # 轉換為概率標籤
        prob_label = Text("probability", color=highlight_color)
        prob_label.move_to(percentage_label)
        self.wait()
        self.play(
            all_students[8].animate.set_color(MAROON_E),
            ReplacementTransform(percentage_label, prob_label)
        )
        
        self.wait()
        self.play(
            FadeOut(prob_label),
            FadeOut(arrows),
            FadeOut(y_labels_group)
        )
        
        # 簡化的閃爍效果
        class FlashThroughHistogram:
            def __init__(self, histogram, **kwargs):
                self.histogram = histogram
                
            def __call__(self):
                anims = []
                for bar in self.histogram.bars:
                    anims.append(bar.animate.set_fill(opacity=0.3))
                return AnimationGroup(*anims)
        
        class FlashThroughClass:
            def __init__(self, students, **kwargs):
                self.students = students
                
            def __call__(self):
                anims = []
                for student in self.students:
                    anims.append(student.animate.set_color(MAROON_E))
                return AnimationGroup(*anims)
        
        flash_hist = FlashThroughHistogram(grade_hist)
        flash_class = FlashThroughClass(all_students)
        
        self.wait()
        for i in range(3):
            self.play(flash_hist(), flash_class())
            self.play(
                *[bar.animate.set_fill(opacity=0.7) for bar in grade_hist.bars],
                *[student.animate.set_color(BLUE_E) for student in all_students]
            )
