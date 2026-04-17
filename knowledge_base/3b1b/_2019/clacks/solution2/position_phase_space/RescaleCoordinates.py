# Source: 3b1b/_2019/clacks/solution2/position_phase_space.py
# Description: [3b1b translated] 展示在位置相空間中重新縮放坐標軸的過程，包括拉伸圖形元素、更新軸標籤，以及角色對視覺效果的評論。



from manim import *
class RescaleCoordinates(PositionPhaseSpaceScene, MovingCameraScene):
    def __init__(
        self,
        rescale_coordinates=False,
        ps_d2_label_vect=LEFT,
        axes_center=6 * LEFT + 0.65 * DOWN,
        block1_config={"distance": 7},
        wait_time=30,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.rescale_coordinates = rescale_coordinates
        self.ps_d2_label_vect = ps_d2_label_vect
        self.axes_center = axes_center
        self.block1_config = block1_config
        self.wait_time = wait_time

    def setup(self):
        PositionPhaseSpaceScene.setup(self)
        MovingCameraScene.setup(self)
        self.add(
            self.floor,
            self.wall,
            self.blocks,
            self.axes,
            self.d1_eq_d2_line,
            self.d1_eq_d2_label,
            self.d2_eq_w2_line,
            self.ps_dot,
            self.x_line,
            self.y_line,
            self.ps_d1_label,
            self.ps_d2_label,
            self.d1_brace,
            self.d2_brace,
            self.d1_label,
            self.d2_label,
        )

    def construct(self):
        self.show_rescaling()
        self.comment_on_ugliness()
        self.put_into_frame()

    def show_rescaling(self):
        axes = self.axes
        blocks = self.blocks
        to_stretch = VGroup(
            axes.added_lines,
            self.d1_eq_d2_line,
            self.ps_point,
        )
        m1 = self.block1.mass
        new_axes_labels = self.get_axes_labels(axes, with_sqrts=True)

        # Show label
        def show_label(index, block, vect):
            self.play(
                CreateThenFadeAround(axes.labels[index])
            )
            self.play(
                Transform(
                    axes.labels[index],
                    VGroup(
                        *new_axes_labels[index][:2],
                        new_axes_labels[index][3]
                    ),
                ),
                GrowFromCenter(new_axes_labels[index][2])
            )
            group = VGroup(
                new_axes_labels[index][2][-2:].copy(),
                MathTex("="),
                block.label.copy(),
            )
            group.generate_target()
            group.target.arrange(RIGHT, buff=SMALL_BUFF)
            group.target.next_to(block, vect)
            group[1].scale(0)
            group[1].move_to(group.target[1])
            group.target[2].set_fill(WHITE)
            group.target[2].set_stroke(width=0, background=True)
            self.play(MoveToTarget(
                group,
                rate_func=there_and_back_with_pause,
                run_time=3
            ))
            self.remove(group)
            self.wait()

        show_label(0, self.block1, RIGHT)

        # The stretch
        blocks.suspend_updating()
        self.play(
            ApplyMethod(
                to_stretch.stretch, np.sqrt(m1), 0,
                {"about_point": axes.coords_to_point(0, 0)},
            ),
            self.d1_eq_d2_label.animate.shift(6 * RIGHT),
            run_time=2,
        )
        self.rescale_coordinates = True
        blocks.resume_updating()
        self.wait()

        # Show wiggle
        d1, d2 = self.get_ds()
        for new_d1 in [d1 - 2, d1]:
            self.play(self.get_ps_point_change_anim(
                new_d1, d2,
                rate_func=smooth,
                run_time=2,
            ))
        self.wait()

        # Change y-coord
        show_label(1, self.block2, LEFT)

        axes.remove(axes.labels)
        self.remove(axes.labels)
        axes.labels = new_axes_labels
        axes.add(axes.labels)
        self.add(axes)

    def comment_on_ugliness(self):
        axes = self.axes

        randy = Randolph(height=1.7)
        randy.flip()
        randy.next_to(self.d2_eq_w2_line, UP, buff=0)
        randy.to_edge(RIGHT)
        randy.change("sassy")
        randy.save_state()
        randy.set_opacity(0)
        randy.change("plain")

        self.play(Restore(randy))
        self.play(
            PiCreatureSays(
                randy, "Hideous!",
                bubble_config={"height": 1.5, "width": 2},
                target_mode="angry",
                look_at=axes.labels[0]
            )
        )
        self.play(randy.animate.look_at(axes.labels[1]))
        self.play(Blink(randy))
        self.play(
            RemovePiCreatureBubble(
                randy, target_mode="confused"
            )
        )
        self.play(Blink(randy))
        self.play(randy.animate.look_at(axes.labels[0]))
        self.wait()
        self.play(FadeOut(randy))

    def put_into_frame(self):
        rect = ScreenRectangle(height=config.frame_height + 10)
        inner_rect = ScreenRectangle(height=config.frame_height)
        rect.add_subpath(inner_rect.get_points()[::-1])
        rect.set_fill("#333333", opacity=1)
        frame = self.camera.frame

        self.begin_sliding()
        self.add(rect)
        self.play(
            frame.animate.scale(1.5, about_point=frame.get_bottom() + UP),
            run_time=2,
        )
        self.wait(self.wait_time)
        self.end_sliding()

    def get_ds(self):
        if self.rescale_coordinates:
            return super().get_ds()
        return (
            self.block1_config["distance"],
            self.block2_config["distance"],
        )
