# 🧠 Thinking Summary

```text
============================================================
🌳 **VISUAL TREE OF THOUGHTS (ToT)**
============================================================
```

```text
============================================================


============================================================
```

```text
============================================================
**Concept Extraction**: Function y = 0.5x², its graph (parabola), derivative y' = x, tangent line at a point (x, f(x)), slope m = x. Real-time updating of line and slope value.

**Visual Metaphor**: Clean, symbolic visualization. The derivative equation is the "engine" driving the animation.

**Spatial Plan & Calculations**:
- **Zones**: HEADER (title), CONTENT (graph & moving elements), FOOTER (explanatory text).
- **CONTENT Anchor (global_center)**: ORIGIN (0,0,0). This is the stage.
- **Graph**: Parabola y = 0.5x². Plot from x = -4 to x = 4. Vertex at (0,0). Points at extremes: (-4, 8), (4, 8). Fits well within y ∈ [-1, 9] if we shift view down slightly. We'll set the graph's center at ORIGIN.
- **Moving Point**: `dot = Dot(point=(x, 0.5*x**2, 0))`. Controlled by a ValueTracker for x.
- **Tangent Line**: Segment centered on the moving point. Slope m = x (from y'=x). Line equation at point (a, 0.5a²): y - 0.5a² = a(x - a). For visualization, we need two points. We'll create a line of length 3, symmetric around the point of tangency.
  - Direction vector: (1, m) = (1, a). Normalize? Simpler: From point `a`, go `dx=1.5` units left/right.
  - Start: `(a - 1.5, 0.5*a² - 1.5*a, 0)`
  - End: `(a + 1.5, 0.5*a² + 1.5*a, 0)`
- **Slope Label**: `MathTex(f"m = {x_val:.2f}")`. Position it above and to the right of the moving point.
- **Derivative Display**: A static `MathTex(r"y' = x")` placed in the upper-left of the CONTENT zone, acting as a legend/controller.
- **Explanation Anchor**: At `DOWN * 3.0`. For text explaining the relationship.

**Constraints**:
- All main action (graph, dot, line) stays within x ∈ [-5, 5], y ∈ [-2, 9] in scene coordinates. We'll adjust camera accordingly.
- The slope label must always be visible and not overlap severely with the line.
- The tangent line must be clearly a *line segment* (not infinite), emphasizing its local nature.

**Signal Strategy**:
1. Introduce the function and its graph.
2. Introduce the derivative as the slope function. Point to `y' = x`.
3. Animate the dot moving, with the tangent line and slope label updating in real-time. Use `Indicate` on the derivative equation and the slope label to reinforce the link: `y' = x` -> `m = [current x]`.
============================================================
```

