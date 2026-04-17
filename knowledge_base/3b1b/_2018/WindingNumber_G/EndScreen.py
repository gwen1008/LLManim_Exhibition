# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個結束畫面，包含 Patreon 贊助者名單和兩個角色輪流變換表情的動畫。



from manim import *
class EndScreen(Scene):
    def __init__(self, run_time=0, **kwargs):
        super().__init__(**kwargs)
        self.run_time = run_time
    
    def construct(self):
        # 注意：由於 PatreonEndScreen 和 PiCreatureScene 在 ManimCE 中沒有直接對應，
        # 這裡假設 pi_creatures 是兩個已經存在的 Mobject（例如 SVGMobject）
        # 實際使用時需要根據具體的 pi_creature 實現調整
        
        # 移除初始的 pi_creature（如果存在）
        if hasattr(self, 'pi_creature'):
            self.remove(self.pi_creature)
        
        # 這裡原本的 PatreonEndScreen.construct(self) 在 ManimCE 中沒有對應
        # 假設這部分只是顯示贊助者名單，用一個文字替代
        patreon_text = Text("Patreon Supporters", font_size=48)
        patreon_text.to_edge(UP)
        self.add(patreon_text)
        
        # 假設有兩個角色
        # 實際使用時需要替換為具體的 SVGMobject 或自定義 Mobject
        randy = Circle(color=BLUE, fill_opacity=0.5).scale(0.5)
        morty = Circle(color=RED, fill_opacity=0.5).scale(0.5)
        randy.to_edge(LEFT).shift(UP)
        morty.to_edge(RIGHT).shift(UP)
        
        self.add(randy, morty)
        
        # 表情變化序列
        for mode in ["thinking", "confused", "pondering", "hooray"]:
            # 改變 randy 的表情（這裡用顏色變化模擬）
            self.play(randy.animate.set_color(self.get_color_for_mode(mode)))
            self.wait()
            # 改變 morty 的表情
            self.play(morty.animate.set_color(self.get_color_for_mode(mode)))
            self.wait(2)
    
    def get_color_for_mode(self, mode):
        # 輔助函數：根據表情模式返回對應顏色
        color_map = {
            "thinking": BLUE,
            "confused": YELLOW,
            "pondering": PURPLE,
            "hooray": GREEN,
        }
        return color_map.get(mode, WHITE)
