
"""
Common helper functions for generating Manim arithmetic scene code.
This module provides standard code blocks for setup, subtitles, and audio integration.
"""

def get_imports_code():
    """Returns the standard imports required for Manim scenes."""
    return "from manim import *\n\n"

def get_setup_code(font="PingFang TC"):
    """
    Returns the setup method code for the Scene class.
    Initializes the subtitle area.
    """
    return f"""
    def setup(self):
        \"\"\"Initialize subtitle area\"\"\"
        self.subtitle_area = Text(
            "", 
            font_size=32, 
            font="{font}",
            color=WHITE
        ).to_edge(DOWN, buff=0.4)
        self.add(self.subtitle_area)
"""

def get_subtitle_methods_code(font="PingFang TC"):
    """
    Returns the helper methods for creating and updating subtitles.
    Includes the 'instant update' logic to avoid rendering delays.
    """
    return f"""
    def create_wrapped_subtitle(self, text):
        \"\"\"Create subtitle for a single sentence\"\"\"
        new_sub = Text(
            text, 
            font_size=32, 
            font="{font}", 
            color=WHITE
        ).to_edge(DOWN, buff=0.4)
        
        if new_sub.get_width() > self.camera.frame_width * 0.9:
            new_sub.scale_to_fit_width(self.camera.frame_width * 0.9)
        
        return new_sub

    def update_subtitle(self, text, duration=1.0):
        \"\"\"Update subtitle instantly\"\"\"
        new_sub = self.create_wrapped_subtitle(text)
        self.remove(self.subtitle_area)
        self.subtitle_area = new_sub
        self.add(self.subtitle_area)
        self.wait(duration)
"""
