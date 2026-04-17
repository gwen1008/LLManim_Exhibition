# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示海森堡不確定性原理，透過點雲和向量雲的機率分佈變化，說明位置與動量的不確定性關係。



from manim import *
class MentionUncertaintyPrinciple(TeacherStudentsScene):
    def construct(self):
        title = Tex("Heisenberg Uncertainty Principle")
        title.to_edge(UP)

        # 注意：ProbabalisticDotCloud 和 ProbabalisticVectorCloud 是自訂類別
        # 在 ManimCE 中需要自行定義或使用替代方案
        dot_cloud = ProbabalisticDotCloud()
        vector_cloud = ProbabalisticVectorCloud(
            gaussian_distribution_wrapper_config={"sigma_x": 0.2},
            center_func=lambda: dot_cloud.gaussian_distribution_wrapper.get_parameters()[0],
        )
        
        for cloud in [dot_cloud, vector_cloud]:
            cloud.gaussian_distribution_wrapper.next_to(
                title, DOWN, buff=2*LARGE_BUFF
            )
        vector_cloud.gaussian_distribution_wrapper.shift(3*RIGHT)

        def get_brace_text_group_update(gdw, vect, text, color):
            brace = Brace(gdw, vect)
            tex_text = brace.get_tex(f"2\\sigma_{{\\text{{{text}}}}}", buff=SMALL_BUFF)
            group = VGroup(brace, tex_text)
            
            def update_group(group):
                brace, tex_text = group
                brace.match_width(gdw, stretch=True)
                brace.next_to(gdw, vect)
                tex_text.next_to(brace, vect, buff=SMALL_BUFF)
            
            group.set_color(color)
            return group.add_updater(update_group)

        dot_brace_anim = get_brace_text_group_update(
            dot_cloud.gaussian_distribution_wrapper,
            DOWN, "position", dot_cloud.color
        )
        vector_brace_anim = get_brace_text_group_update(
            vector_cloud.gaussian_distribution_wrapper,
            UP, "momentum", vector_cloud.color
        )

        self.add(title)
        self.add(dot_cloud)
        self.play(
            Write(title),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(*["pondering"]*3)
        )
        self.play(
            Write(dot_brace_anim.mobject, run_time=1)
        )
        self.add(dot_brace_anim)
        self.wait()
        
        self.play(
            dot_cloud.gaussian_distribution_wrapper.animate.change_parameters(
                {"sigma": 0.1*RIGHT}
            ),
            run_time=2,
        )
        self.wait()
        
        self.add(vector_cloud)
        self.play(
            FadeIn(vector_brace_anim.mobject)
        )
        self.add(vector_brace_anim)
        self.play(
            vector_cloud.gaussian_distribution_wrapper.animate.change_parameters(
                {"sigma": RIGHT}
            ),
            self.change_students(*["confused"]*3),
            run_time=3,
        )
        
        # 來回變化
        for x in range(2):
            self.play(
                dot_cloud.gaussian_distribution_wrapper.animate.change_parameters(
                    {"sigma": 2*RIGHT}
                ),
                vector_cloud.gaussian_distribution_wrapper.animate.change_parameters(
                    {"sigma": 0.1*RIGHT}
                ),
                run_time=3,
            )
            self.play_student_changes("thinking", "erm", "sassy")
            self.play(
                dot_cloud.gaussian_distribution_wrapper.animate.change_parameters(
                    {"sigma": 0.1*RIGHT}
                ),
                vector_cloud.gaussian_distribution_wrapper.animate.change_parameters(
                    {"sigma": 1*RIGHT}
                ),
                run_time=3,
            )
            self.wait()
