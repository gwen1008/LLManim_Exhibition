# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示教師與學生場景中，從英文術語「不確定性原理」到德文翻譯「Unschärferelation」，再到字面翻譯「Unsharpness relation」的動態轉換過程。



from manim import *
class BetterTranslation(TeacherStudentsScene):
    def construct(self):
        english_term = Text("Uncertainty principle")
        german_word = Text("Unschärferelation")
        translation = Text("Unsharpness relation")

        to_german_words = Text("In German")
        to_german_words.scale(0.5)
        to_german_arrow = Arrow(
            start=UP, end=DOWN, 
            color=WHITE, buff=SMALL_BUFF
        )
        to_german_words.next_to(to_german_arrow, RIGHT, SMALL_BUFF)
        to_german_words.set_color(YELLOW)
        to_german_group = VGroup(to_german_arrow, to_german_words)

        translation_words = Text("Literal translation")
        translation_words.scale(0.5)
        translation_arrow = Arrow(
            start=UP, end=DOWN, 
            color=WHITE, buff=SMALL_BUFF
        )
        translation_words.next_to(translation_arrow, LEFT, SMALL_BUFF)
        translation_words.set_color(YELLOW)
        translation_group = VGroup(translation_arrow, translation_words)

        english_term.next_to(self.teacher, UP+LEFT)
        english_term.save_state()
        english_term.shift(DOWN)
        english_term.set_opacity(0)
        self.play(
            Restore(english_term),
            self.change_students(*["pondering"]*3)
        )
        self.wait()

        german_word.move_to(english_term)
        to_german_group.next_to(
            german_word, UP,
            aligned_edge=to_german_arrow.get_center()
        )
        self.play(
            self.teacher.animate.change("raise_right_hand"),
            english_term.animate.next_to(to_german_arrow, UP)
        )
        self.play(
            GrowArrow(to_german_arrow),
            FadeIn(to_german_words),
            ReplacementTransform(
                english_term.copy().set_opacity(0),
                german_word
            )
        )
        self.wait(2)

        group = VGroup(english_term, to_german_group, german_word)
        translation.move_to(german_word)
        translation_group.next_to(
            german_word, UP,
            aligned_edge=translation_arrow.get_center()
        )
        self.play(
            group.animate.next_to(translation_arrow, UP),
        )
        self.play(
            GrowArrow(translation_arrow),
            FadeIn(translation_words),
            ReplacementTransform(
                german_word.copy().set_opacity(0),
                translation
            )
        )
        self.play_student_changes(*["happy"]*3)
        self.wait(2)
