# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示不同寬度的高斯包絡正弦波圖形，並說明信號長度與頻率範圍的相關性。



from manim import *
class VariousMusicalNotes(Scene):
    def construct(self):
        freq = 20
        # x-coordinate of this point represents log(a)
        # where the bell curve component of the signal
        # is exp(-a*(x**2))
        graph_width_tracker = ValueTracker(1)
        
        def get_graph():
            a = graph_width_tracker.get_value()
            return FunctionGraph(
                lambda x: np.exp(-a * x**2) * np.sin(freq * x) - 0.5,
                x_range=[-config.frame_width / 2, config.frame_width / 2],
                color=BLUE
            )
        
        graph = get_graph()
        
        def graph_update(graph):
            new_graph = get_graph()
            graph.set_points(new_graph.get_points())
        
        graph_update_anim = UpdateFromFunc(graph, graph_update)
        
        def change_width_anim(width, **kwargs):
            a = 2.0 / (width**2)
            return AnimationGroup(
                graph_width_tracker.animate.set_value(a),
                graph_update_anim,
                **kwargs
            )
        
        # Initialize graph
        change_width_anim(config.frame_width / 2)
        graph_update_anim.update(0)

        phrases = [
            Tex(*words.split(" "), font_size=36)
            for words in [
                "Very clear frequency",
                "Less clear frequency",
                "Extremely unclear frequency",
            ]
        ]

        # Show graphs and phrases
        widths = [config.frame_width / 2, 1, 0.2]
        last_phrase = None
        last_brace = None
        
        for width, phrase in zip(widths, phrases):
            brace = Brace(Line(LEFT, RIGHT), UP)
            brace.stretch(width, 0)
            brace.next_to(graph.get_center(), UP, buff=1.2)
            phrase.next_to(brace, UP)

            if width is widths[0]:
                self.play(Create(graph, rate_func=linear))
                self.play(
                    GrowFromCenter(brace),
                    Write(phrase, run_time=1)
                )
            else:
                self.play(
                    change_width_anim(width),
                    ReplacementTransform(
                        VGroup(last_phrase, last_brace),
                        VGroup(phrase, brace),
                        rate_func=lambda t: squish_rate_func(smooth, 0.5, 1)(t),
                    ),
                    run_time=2
                )
            self.wait()
            last_phrase = phrase
            last_brace = brace

        # Talk about correlations
        short_signal_words = Tex(
            "Short", "signal", "correlates",
            "with", "wide range", "of frequencies",
            font_size=32
        )
        long_signal_words = Tex(
            "Only", "wide", "signals", "correlate",
            "with a", "short range", "of frequencies",
            font_size=32
        )
        phrases = VGroup(short_signal_words, long_signal_words)
        
        for phrase in phrases:
            phrase.scale(0.8)
            # Set colors based on text content
            for word in ["short", "long", "wide"]:
                for submob in phrase:
                    if isinstance(submob, Tex):
                        for part in submob:
                            if word in part.get_tex_string().lower():
                                if word == "short":
                                    part.set_color(RED)
                                else:
                                    part.set_color(GREEN)
        
        phrases.arrange(DOWN, buff=0.5)
        phrases.to_edge(UP)

        long_graph = FunctionGraph(
            lambda x: 0.5 * np.sin(freq * x),
            x_range=[-config.frame_width, config.frame_width],
            color=BLUE
        )
        long_graph.next_to(graph, UP, buff=MED_LARGE_BUFF)

        self.play(
            Create(long_graph),
            *[FadeOut(mob) for mob in [last_brace, last_phrase]]
        )
        self.play(
            Write(short_signal_words),
            change_width_anim(widths[2])
        )
        self.play(
            long_graph.animate.stretch(0.35, 0).set_color(GREEN),
            run_time=5,
            rate_func=wiggle
        )
        self.wait()
        self.play(
            Write(long_signal_words),
            change_width_anim(widths[0]),
        )
        self.play(
            long_graph.animate.stretch(0.95, 0).set_color(average_color(GREEN, BLUE)),
            run_time=4,
            rate_func=wiggle
        )
        self.wait()
