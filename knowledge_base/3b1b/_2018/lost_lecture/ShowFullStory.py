# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一系列圖片以網格排列，並進行縮放和平移的動畫效果。


from manim import *
import os

class ShowFullStory(Scene):
    def construct(self):
        # 假設 MEDIA_DIR 已定義，若未定義請自行替換為實際路徑
        # 例如: MEDIA_DIR = "/path/to/media"
        directory = os.path.join(
            MEDIA_DIR,
            "animations/active_projects/lost_lecture/images"
        )
        scene_names = [
            "ShowEmergingEllipse",
            "ShowFullStory",
            "FeynmanFameStart",
            "TheMotionOfPlanets",
            "FeynmanElementaryQuote",
            "DrawingEllipse",
            "ShowEllipseDefiningProperty",
            "ProveEllipse",
            "KeplersSecondLaw",
            "AngularMomentumArgument",
            "HistoryOfAngularMomentum",
            "FeynmanRecountingNewton",
            "IntroduceShapeOfVelocities",
            "ShowEqualAngleSlices",
            "PonderOverOffCenterDiagram",
            "UseVelocityDiagramToDeduceCurve",
        ]
        images = Group(*[
            ImageMobject(os.path.join(directory, name + ".png"))
            for name in scene_names
        ])
        for image in images:
            image.add(
                SurroundingRectangle(image, buff=0, color=WHITE)
            )
        images.arrange_in_grid(rows=4, buff=0)  # 注意: ManimCE 參數名為 rows 而非 n_rows

        # 調整縮放比例以適應畫面寬度
        images.scale(
            1.01 * config.frame_width / images[0].width  # FRAME_WIDTH -> config.frame_width
        )
        images.shift(-images[0].get_center())

        # 第一個動畫: 縮放並置中
        self.play(
            images.animate.set_width(config.frame_width - 1).center(),  # 使用 .animate 語法
            run_time=3,
        )
        self.wait()
        # 第二個動畫: 平移並縮放
        self.play(
            images.animate.shift(-images[2].get_center()).scale(
                config.frame_width / images[2].width,
                about_point=ORIGIN  # 將 about_point 作為關鍵字參數傳入
            ),
            run_time=3,
        )
        self.wait()
