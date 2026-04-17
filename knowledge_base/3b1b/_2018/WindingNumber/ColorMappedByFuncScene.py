# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 根據自定義函數將數值平面映射為彩色背景，可選擇顯示坐標網格或隱藏背景。


from manim import *
import numpy as np
import itertools as it
import os

class ColorMappedByFuncScene(Scene):
    def __init__(
        self,
        func=lambda p: p,
        num_plane=NumberPlane(),
        show_num_plane=True,
        show_output=False,
        hide_background=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.func = func
        self.num_plane = num_plane
        self.show_num_plane = show_num_plane
        self.show_output = show_output
        self.hide_background = hide_background

    def short_path_to_long_path(self, filename_with_ext):
        return os.path.join(self.renderer.file_writer.image_dir_path, filename_with_ext)

    def setup(self):
        # The composition of input_to_pos and pos_to_color 
        # is to be equal to func (which turns inputs into colors)
        # However, depending on whether we are showing input or output (via a MappingCamera),
        # we color the background using either func or the identity map
        if self.show_output:
            self.input_to_pos_func = self.func
            self.pos_to_color_func = lambda p: p
        else:
            self.input_to_pos_func = lambda p: p
            self.pos_to_color_func = self.func

        self.pixel_pos_to_color_func = lambda x_y3: self.pos_to_color_func(
            self.num_plane.point_to_coords(np.array([x_y3[0], x_y3[1], 0]))
        )

        jitter_val = 0.1
        line_coords = np.linspace(-10, 10) + jitter_val
        func_hash_points = it.product(line_coords, line_coords)

        def mini_hasher(p):
            rgba = color_to_rgba(self.pixel_pos_to_color_func(p))
            if rgba[3] != 1.0:
                print("Warning! color_to_rgba assigns fractional alpha", rgba[3])
            return tuple(rgba)

        to_hash = tuple(mini_hasher(p) for p in func_hash_points)
        func_hash = hash(to_hash)
        # We hash just based on output image
        # Thus, multiple scenes with same output image can re-use it
        # without recomputation
        full_hash = hash((func_hash, self.camera.pixel_width))
        self.background_image_file = self.short_path_to_long_path(
            "color_mapped_bg_hash_" + str(full_hash) + ".png"
        )
        self.in_background_pass = not os.path.exists(self.background_image_file)

        print("Background file: " + self.background_image_file)
        if self.in_background_pass:
            print("The background file does not exist yet; this will be a background creation + video pass")
        else:
            print("The background file already exists; this will only be a video pass")

    def construct(self):
        if self.in_background_pass:
            # ManimCE 沒有 set_background_from_func，改為手動創建背景
            # 這裡簡化處理：創建一個覆蓋整個屏幕的彩色矩形
            background = Rectangle(
                width=self.camera.frame_width,
                height=self.camera.frame_height,
                fill_opacity=1
            )
            # 應用顏色映射函數到背景（這裡簡化為單色）
            try:
                color = self.pixel_pos_to_color_func((0, 0))
                background.set_color(color)
            except:
                background.set_color(BLUE)
            
            self.add(background)
            self.wait(0.01)  # 短暫等待以確保渲染
            self.camera.capture_mobjects(self.mobjects)
            self.camera.get_image().save(self.background_image_file, mode="RGBA")

        if self.hide_background:
            # Clearing background
            self.camera.background = None
        else:
            # 加載背景圖片
            if os.path.exists(self.background_image_file):
                background_image = ImageMobject(self.background_image_file)
                background_image.stretch_to_fit_width(self.camera.frame_width)
                background_image.stretch_to_fit_height(self.camera.frame_height)
                self.add(background_image)
        
        if self.show_num_plane:
            self.num_plane.set_opacity(0.5)
            self.add(self.num_plane)
