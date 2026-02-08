# Manim Community v0.19.2 API Strict Rules
# Added as part of Conservative LLM Upgrade (Feb 2026)
# Based on deep research identifying common failure modes

MANIM_API_STRICT_RULES = """
=== CRITICAL: Manim Community v0.19.2 API Compliance ===
The following rules are MANDATORY to prevent rendering failures:

1. ✅ Use Text() and MathTex(), NOT TextMobject or TexMobject (deprecated)
2. ✅ Use class attributes, NOT CONFIG dictionary (removed in v0.19+)
3. ✅ Use .animate syntax for transformations: obj.animate.shift(UP)
4. ⚠️ SVGMobject only supports basic paths - NO <text>, <image>, or CSS
5. ⚠️ Always self.add() or self.play(Create()) BEFORE self.play(...animate...)
6. 🎵 For audio: ALWAYS use add_sound() for EVERY narration step when audio files exist

=== Known Issues to Avoid ===
- Issue #4005: add_sound() skipped when caching enabled → System auto-disables caching
- SVG Parser: Limited to basic paths, complex SVGs will be silently ignored
- State Sequencing: Animating non-added objects causes AttributeError

"""
