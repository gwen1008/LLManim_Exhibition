from manim import *

class RotatingSquare(Scene):
    """A simple example: red square rotating 90 degrees."""
    def construct(self):
        # Create a red square
        square = Square(color=RED, fill_opacity=0.5)
        
        # Add to scene
        self.play(Create(square))
        self.wait(0.5)
        
        # Rotate 90 degrees
        self.play(Rotate(square, angle=PI/2))
        self.wait(1)
        
        # Fade out
        self.play(FadeOut(square))
