from manim import *

class TestScene(Scene):
    def construct(self):
        c = Circle()
        # Test 1: keyword arg
        c.add_updater(updater=lambda m: m.become(Square()))
        
        # Test 2: named function
        def my_upd(m):
            m.become(Triangle())
            
        c.add_updater(my_upd)
