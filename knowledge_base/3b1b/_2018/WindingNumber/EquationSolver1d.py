# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一維方程求解的二分法過程，在坐標軸上動態顯示區間收斂和函數值的變化。



from manim import *
class EquationSolver1d(Scene):
    def __init__(self, 
                 func=lambda x: x,
                 targetX=0,
                 targetY=0,
                 initial_lower_x=0,
                 initial_upper_x=10,
                 num_iterations=10,
                 iteration_at_which_to_start_zoom=None,
                 graph_label=None,
                 show_target_line=True,
                 base_line_y=0,
                 show_y_as_deviation=False,
                 **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.targetX = targetX
        self.targetY = targetY
        self.initial_lower_x = initial_lower_x
        self.initial_upper_x = initial_upper_x
        self.num_iterations = num_iterations
        self.iteration_at_which_to_start_zoom = iteration_at_which_to_start_zoom
        self.graph_label = graph_label
        self.show_target_line = show_target_line
        self.base_line_y = base_line_y
        self.show_y_as_deviation = show_y_as_deviation
        
        # 顏色定義
        self.positive_color = GREEN
        self.negative_color = RED
        self.neutral_color = WHITE

    def drawGraph(self):
        # 創建坐標軸
        self.ax = Axes(
            x_range=[self.initial_lower_x - 1, self.initial_upper_x + 1],
            y_range=[min(self.func(self.initial_lower_x), self.func(self.initial_upper_x), self.targetY) - 1,
                     max(self.func(self.initial_lower_x), self.func(self.initial_upper_x), self.targetY) + 1],
            axis_config={"include_numbers": True}
        )
        self.add(self.ax)
        
        # 繪製函數圖形
        self.graph = self.ax.plot(self.func, color=BLUE)
        self.add(self.graph)

        if self.graph_label is not None:
            curve_label = MathTex(self.graph_label)
            curve_label.next_to(self.graph.point_from_proportion(0.5), LEFT)
            self.add(curve_label)
        
        if self.show_target_line:
            target_line_object = DashedLine(
                self.ax.c2p(self.initial_lower_x - 1, self.targetY),
                self.ax.c2p(self.initial_upper_x + 1, self.targetY),
                dash_length=0.1
            )
            self.add(target_line_object)

            target_label_num = 0 if self.show_y_as_deviation else self.targetY
            target_line_label = MathTex(f"y = {target_label_num}")
            target_line_label.next_to(target_line_object.get_start(), UP + RIGHT)
            self.add(target_line_label)

        self.wait()

        if self.show_target_line:
            self.play(FadeOut(target_line_label))

    def solveEquation(self):
        def color_by_comparison(val, ref):
            if val > ref:
                return self.positive_color
            elif val < ref:
                return self.negative_color
            else:
                return self.neutral_color

        lower_color = color_by_comparison(self.func(self.initial_lower_x), self.targetY)
        upper_color = color_by_comparison(self.func(self.initial_upper_x), self.targetY)

        if self.show_y_as_deviation:
            y_bias = -self.targetY
        else:
            y_bias = 0

        startBrace = MathTex("|", stroke_width=10)
        startBrace.set_color(lower_color)
        endBrace = startBrace.copy()
        endBrace.set_color(upper_color)

        leftBrace = startBrace.copy()
        rightBrace = endBrace.copy()

        downBrace = startBrace.copy()
        upBrace = endBrace.copy()
        yBraces = VGroup(downBrace, upBrace)
        yBraces.rotate(PI/2)

        lowerX = self.initial_lower_x
        lowerY = self.func(lowerX)
        upperX = self.initial_upper_x
        upperY = self.func(upperX)

        leftBrace.move_to(self.ax.c2p(lowerX, self.base_line_y))
        leftBraceLabel = DecimalNumber(lowerX)
        leftBraceLabel.next_to(leftBrace, DOWN + LEFT, buff=SMALL_BUFF)
        
        rightBrace.move_to(self.ax.c2p(upperX, self.base_line_y))
        rightBraceLabel = DecimalNumber(upperX)
        rightBraceLabel.next_to(rightBrace, DOWN + RIGHT, buff=SMALL_BUFF)

        downBrace.move_to(self.ax.c2p(0, lowerY))
        downBraceLabel = DecimalNumber(lowerY)
        downBraceLabel.next_to(downBrace, LEFT + DOWN, buff=SMALL_BUFF)
        
        upBrace.move_to(self.ax.c2p(0, upperY))
        upBraceLabel = DecimalNumber(upperY)
        upBraceLabel.next_to(upBrace, LEFT + UP, buff=SMALL_BUFF)

        lowerDotPoint = self.ax.c2p(lowerX, lowerY)
        lowerDotXPoint = self.ax.c2p(lowerX, self.base_line_y)
        lowerDotYPoint = self.ax.c2p(0, lowerY)
        lowerDot = Dot(lowerDotPoint, color=lower_color)
        upperDotPoint = self.ax.c2p(upperX, upperY)
        upperDot = Dot(upperDotPoint, color=upper_color)
        upperDotXPoint = self.ax.c2p(upperX, self.base_line_y)
        upperDotYPoint = self.ax.c2p(0, upperY)

        lowerXLine = Line(lowerDotXPoint, lowerDotPoint, color=lower_color)
        upperXLine = Line(upperDotXPoint, upperDotPoint, color=upper_color)
        lowerYLine = Line(lowerDotPoint, lowerDotYPoint, color=lower_color)
        upperYLine = Line(upperDotPoint, upperDotYPoint, color=upper_color)

        x_guess_line = Line(lowerDotXPoint, upperDotXPoint, color=WHITE, stroke_width=10)

        lowerGroup = VGroup(
            lowerDot, 
            leftBrace, downBrace,
            lowerXLine, lowerYLine,
            x_guess_line
        )
        
        upperGroup = VGroup(
            upperDot, 
            rightBrace, upBrace,
            upperXLine, upperYLine,
            x_guess_line
        )

        initialLowerXDot = Dot(lowerDotXPoint, color=lower_color)
        initialUpperXDot = Dot(upperDotXPoint, color=upper_color)
        initialLowerYDot = Dot(lowerDotYPoint, color=lower_color)
        initialUpperYDot = Dot(upperDotYPoint, color=upper_color)

        # 初始動畫
        self.play(FadeIn(initialLowerXDot), FadeIn(leftBrace), FadeIn(leftBraceLabel))
        self.add(initialLowerXDot, leftBrace)
        self.play(Create(lowerXLine))
        self.add(lowerDot)
        self.play(Create(lowerYLine))
        self.play(FadeIn(initialLowerYDot), FadeIn(downBrace), FadeIn(downBraceLabel))
        self.add(initialLowerYDot, downBrace)

        self.wait()

        self.play(FadeIn(initialUpperXDot), FadeIn(rightBrace), FadeIn(rightBraceLabel))
        self.add(initialUpperXDot, rightBrace)
        self.play(Create(upperXLine))
        self.add(upperDot)
        self.play(Create(upperYLine))
        self.play(FadeIn(initialUpperYDot), FadeIn(upBrace), FadeIn(upBraceLabel))
        self.add(initialUpperYDot, upBrace)

        self.wait()

        self.play(FadeIn(x_guess_line))

        self.wait()

        for i in range(self.num_iterations):
            if i == self.iteration_at_which_to_start_zoom:
                # 縮放功能在ManimCE中需要不同的實現
                pass

            def makeUpdater(xAtStart, fixed_guess_x):
                def updater(group, alpha):
                    dot, xBrace, yBrace, xLine, yLine, guess_line = group
                    newX = interpolate(xAtStart, midX, alpha)
                    newY = self.func(newX)
                    graphPoint = self.ax.c2p(newX, newY)
                    dot.move_to(graphPoint)
                    xAxisPoint = self.ax.c2p(newX, self.base_line_y)
                    xBrace.move_to(xAxisPoint)
                    yAxisPoint = self.ax.c2p(0, newY)
                    yBrace.move_to(yAxisPoint)
                    xLine.put_start_and_end_on(xAxisPoint, graphPoint)
                    yLine.put_start_and_end_on(yAxisPoint, graphPoint)
                    fixed_guess_point = self.ax.c2p(fixed_guess_x, self.base_line_y)
                    guess_line.put_start_and_end_on(xAxisPoint, fixed_guess_point)
                    return group
                return updater

            midX = (lowerX + upperX) / 2.0
            midY = self.func(midX)

            in_negative_branch = midY < self.targetY
            sign_color = self.negative_color if in_negative_branch else self.positive_color

            midCoords = self.ax.c2p(midX, midY)
            midColor = self.neutral_color

            midXBrace = startBrace.copy()
            midXBrace.set_color(midColor)
            midXBrace.move_to(self.ax.c2p(midX, self.base_line_y))

            midXPoint = Dot(self.ax.c2p(midX, self.base_line_y), color=sign_color)

            x_guess_label_caption = Text("New guess: x = ", color=midColor)
            x_guess_label_num = DecimalNumber(midX, color=midColor)
            x_guess_label_num.move_to(0.9 * config.frame_height/2 * DOWN)
            x_guess_label_caption.next_to(x_guess_label_num, LEFT)
            x_guess_label = VGroup(x_guess_label_caption, x_guess_label_num)
            y_guess_label_caption = Text(", y = ", color=midColor)
            y_guess_label_num = DecimalNumber(midY, color=sign_color)
            y_guess_label_caption.next_to(x_guess_label_num, RIGHT)
            y_guess_label_num.next_to(y_guess_label_caption, RIGHT)
            y_guess_label = VGroup(y_guess_label_caption, y_guess_label_num)
            guess_labels = VGroup(x_guess_label, y_guess_label)

            self.play(
                ReplacementTransform(leftBrace.copy(), midXBrace),
                ReplacementTransform(rightBrace.copy(), midXBrace),
                FadeIn(x_guess_label)
            )

            self.add(midXBrace)

            midXLine = DashedLine(
                self.ax.c2p(midX, self.base_line_y),
                midCoords,
                color=midColor
            )
            self.play(Create(midXLine))
            midDot = Dot(midCoords, color=sign_color)
            self.add(midDot)
            midYLine = DashedLine(midCoords, self.ax.c2p(0, midY), color=sign_color)
            self.play(
                Create(midYLine),
                FadeIn(y_guess_label),
                midXBrace.animate.set_color(sign_color),
                midXLine.animate.set_color(sign_color),
                run_time=0.25
            )
            midYPoint = Dot(self.ax.c2p(0, midY), color=sign_color)
            self.add(midXPoint, midYPoint)

            if in_negative_branch:
                self.play(
                    UpdateFromAlphaFunc(lowerGroup, makeUpdater(lowerX, fixed_guess_x=upperX)),
                    FadeOut(guess_labels),
                )
                lowerX = midX
                lowerY = midY
            else:
                self.play(
                    UpdateFromAlphaFunc(upperGroup, makeUpdater(upperX, fixed_guess_x=lowerX)),
                    FadeOut(guess_labels),
                )
                upperX = midX
                upperY = midY
            
            self.remove(midXLine, midDot, midYLine, midXBrace)

        self.wait()

    def construct(self):
        self.drawGraph()
        self.solveEquation()
