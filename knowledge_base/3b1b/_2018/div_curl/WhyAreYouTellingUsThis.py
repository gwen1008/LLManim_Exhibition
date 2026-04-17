# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 老師與學生場景中，一位學生以諷刺語氣提問，老師露出愧疚表情，其他學生則表現出生氣或諷刺的反應。



from manim import *
class WhyAreYouTellingUsThis(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Cool story bro...\\\\ how about the actual math?",
            target_mode="sassy",
            added_anims=[self.teacher.animate.change("guilty")]
        )
        self.play_student_changes("angry", "sassy", "angry")
        self.wait(2)
