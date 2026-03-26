import os
import sys
import json
import pytest
from manim import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.utils.scene_instrumentor import SceneInstrumentor

class MyTestScene(Scene):
    def construct(self):
        # We wrap Scene.play during initialization
        self.instrumentor = SceneInstrumentor(self, "test_log.json")
        
        c1 = Circle().move_to(LEFT)
        self.play(Create(c1))
        
        c2 = Circle().move_to(RIGHT)
        self.play(Create(c2))
        
        c3 = Circle().move_to(RIGHT) # Overlap with c2
        self.play(Create(c3))

def test_instrumentor_creates_log():
    scene = MyTestScene()
    scene.render()
    
    assert os.path.exists("test_log.json")
    with open("test_log.json", "r") as f:
        data = json.load(f)
        
    assert "max_simultaneous_objects" in data
    assert data["max_simultaneous_objects"] == 3
    assert data["steps_with_overlap"] > 0
    
    if os.path.exists("test_log.json"):
        os.remove("test_log.json")

test_instrumentor_creates_log()
print("Success!")
