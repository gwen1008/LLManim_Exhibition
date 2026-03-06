import ast
import sys
import os
import re

class ManimLinter(ast.NodeVisitor):
    # Manim Mobject classes that do NOT accept 'opacity' as constructor arg
    MOBJECT_CLASSES = {
        'Circle', 'Square', 'Rectangle', 'Line', 'Arrow', 'DoubleArrow',
        'Text', 'MathTex', 'Tex', 'Paragraph', 'Title',
        'Triangle', 'Polygon', 'RegularPolygon', 'Ellipse', 'Dot',
        'VGroup', 'VMobject', 'Brace', 'NumberLine',
    }
    # Python builtin types — used to detect `X | Y` union syntax (Python 3.10+ only)
    PYTHON_BUILTIN_TYPES = {
        'int', 'float', 'str', 'bool', 'bytes', 'list', 'dict',
        'tuple', 'set', 'None', 'Any', 'Optional',
    }

    # Mobjects that take positional coordinate arguments — checked for raw array usage
    COORD_CONSUMERS = {'Arrow', 'Dot', 'Line', 'Vector', 'DashedLine', 'DoubleArrow'}
    # Classes that define a logical coordinate system
    COORDINATE_PLANE_TYPES = {'NumberPlane', 'Axes', 'ThreeDAxes', 'ComplexPlane'}

    def __init__(self):
        self.errors = []
        self.advisories = []  # Non-blocking hints for TDR pre-render signal
        self.filename = ""
        self.has_coordinate_plane = False  # Set to True if scene uses NumberPlane/Axes
        self._become_func_names = set()

    def visit_FunctionDef(self, node):
        """Track named functions that call .become() to catch updater assignments."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) and child.func.attr == 'become':
                self._become_func_names.add(node.name)
                break
        self.generic_visit(node)

    def visit_Assign(self, node):
        """Track whether the scene instantiates a coordinate plane."""
        if isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Name) and func.id in self.COORDINATE_PLANE_TYPES:
                self.has_coordinate_plane = True
        self.generic_visit(node)

    def visit_Call(self, node):
        # 1. Check for deprecated 'get_lines()'
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'get_lines':
            self.errors.append({
                "line": node.lineno,
                "code": "DEPRECATED_API",
                "message": "The method 'get_lines()' is deprecated or does not exist on Mobjects. Use 'get_vertices()' or 'get_edges()' instead."
            })
        
        # 2. Check for deprecated 'ShowCreation'
        if isinstance(node.func, ast.Name) and node.func.id == 'ShowCreation':
            self.errors.append({
                "line": node.lineno,
                "code": "DEPRECATED_API",
                "message": "'ShowCreation' is deprecated. Use 'Create' or 'Write' instead."
            })
            
        # 10. [NEW / Animate Kwargs Safety] Check for invalid kwargs passed to .animate.set()
        if (isinstance(node.func, ast.Attribute) and node.func.attr == 'set'
                and isinstance(node.func.value, ast.Attribute) 
                and node.func.value.attr == 'animate'):
            for keyword in node.keywords:
                if keyword.arg in ['length', 'width', 'height', 'radius', 'outer_radius']:
                    self.errors.append({
                        "line": node.lineno,
                        "code": "INVALID_SET_KWARG",
                        "message": f".animate.set({keyword.arg}=...) is invalid. You cannot set geometric dimensions via kwargs. Use .scale() or specific scaling methods instead."
                    })

        # 3. Check for 'get_part_by_tex' with 'substrings' argument (Hallucination)
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'get_part_by_tex':
            for keyword in node.keywords:
                if keyword.arg == 'substrings':
                    self.errors.append({
                        "line": node.lineno,
                        "code": "HALLUCINATED_ARG",
                        "message": "'get_part_by_tex' does not accept 'substrings' argument. This is a known LLM hallucination."
                    })

        # 4. Check for 'get_parts_by_tex' with 'substrings' argument (Hallucination)
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'get_parts_by_tex':
            for keyword in node.keywords:
                if keyword.arg == 'substrings':
                    self.errors.append({
                        "line": node.lineno,
                        "code": "HALLUCINATED_ARG",
                        "message": "'get_parts_by_tex' does not accept 'substrings' argument. This is a known LLM hallucination."
                    })

        # 5. [NEW] Check for arrange_in_circle() — does not exist in Manim v0.19
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'arrange_in_circle':
            self.errors.append({
                "line": node.lineno,
                "code": "HALLUCINATED_METHOD",
                "message": "'arrange_in_circle()' does not exist in Manim v0.19. Use .arrange(RIGHT, buff=0.5) or position manually."
            })

        # 6. [NEW] Check for 'opacity=' as constructor kwarg on Mobject classes
        # This crashes at runtime: Circle(opacity=0.5) → use Circle().set_opacity(0.5)
        if isinstance(node.func, ast.Name) and node.func.id in self.MOBJECT_CLASSES:
            for keyword in node.keywords:
                if keyword.arg == 'opacity':
                    self.errors.append({
                        "line": node.lineno,
                        "code": "INVALID_CONSTRUCTOR_ARG",
                        "message": f"'{node.func.id}' does not accept 'opacity' as a constructor argument. Use {node.func.id}(...).set_opacity(value) instead."
                    })

        # 7. [NEW] Check for deprecated 'axes.get_graph()' — removed in Manim v0.18+
        # Confirmed cause of HIGH_03 first-iteration crash (TypeError: unexpected keyword 'x_range')
        # Correct replacement: axes.plot(lambda x: np.sin(x), x_range=[...])
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'get_graph':
            self.errors.append({
                "line": node.lineno,
                "code": "DEPRECATED_API",
                "message": (
                    "'get_graph()' is a deprecated Manim API removed in v0.18+. "
                    "Replace with 'axes.plot(func, x_range=[start, end, step], color=...)'. "
                    "Example: axes.get_graph(lambda x: np.sin(x)) → axes.plot(lambda x: np.sin(x))"
                )
            })

        # 8. [NEW] Raw coordinate array passed to geometry objects when a NumberPlane/Axes is present.
        # The object will render at screen-space coords ignoring the plane's scale/origin.
        # Correct fix: use plane.c2p(x, y) to map logical → screen coordinates.
        if self.has_coordinate_plane:
            if isinstance(node.func, ast.Name) and node.func.id in self.COORD_CONSUMERS:
                for arg in node.args:
                    if isinstance(arg, (ast.List, ast.Tuple)):
                        self.errors.append({
                            "line": node.lineno,
                            "code": "RAW_COORD_ON_PLANE",
                            "message": (
                                f"'{node.func.id}' receives a raw coordinate array, but a "
                                "NumberPlane/Axes is present in this scene. "
                                "Use plane.c2p(x, y) to map logical grid coordinates to screen space. "
                                f"Example: {node.func.id}(plane.c2p(0, 0), plane.c2p(3, 1), ...)"
                            ),
                        })
                        break  # One error per call is enough

        # 9. [NEW] Check for MathTex() with non-math content (plain English words)
        # MathTex is for LaTeX math mode ONLY. Plain text causes "latex error converting to dvi"
        if isinstance(node.func, ast.Name) and node.func.id == 'MathTex':
            for arg in node.args:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    s = arg.value
                    # Strip explicitly text-mode LaTeX commands entirely so their contents are ignored
                    cleaned = re.sub(r'\\(?:text|mathrm|mathbf)\{[^}]*\}', '', s)
                    # Strip other LaTeX commands
                    cleaned = re.sub(r'\\{1,2}[a-zA-Z]+', '', cleaned)  # remove \frac, \\frac, \sqrt, etc.
                    cleaned = re.sub(r'[_^{}\\$=+\-*/()0-9.,<>|!\[\]&:\']', ' ', cleaned)  # remove math chars
                    # len >= 5: short words (run, rise, area, side, base) are valid math variable names
                    words = [w for w in cleaned.split() if len(w) >= 5 and w.isalpha()]
                    if words:
                        latex_whitelist = {
                            # Standard LaTeX math operators & commands
                            'sin', 'cos', 'tan', 'log', 'exp', 'lim', 'inf',
                            'sup', 'max', 'min', 'det', 'dim', 'ker', 'mod',
                            'gcd', 'lcm', 'deg', 'arg', 'hom', 'sec', 'csc',
                            'cot', 'arcsin', 'arccos', 'arctan', 'sinh', 'cosh',
                            'tanh', 'text', 'mathrm', 'mathbf', 'mathbb', 'cdot',
                            'cdots', 'ldots', 'quad', 'qquad', 'left', 'right',
                            'begin', 'end', 'array', 'matrix', 'frac', 'sqrt',
                            'sum', 'prod', 'int', 'oint', 'over', 'times', 'div',
                            'approx', 'equiv', 'neq', 'leq', 'geq', 'infty',
                            'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta',
                            'lambda', 'sigma', 'omega', 'phi', 'psi', 'pi', 'tau',
                            'rho', 'eta', 'zeta', 'chi',
                            # Common math vocabulary that appears in formulas
                            'slope', 'angle', 'ratio', 'value', 'point',
                            'where', 'given', 'since', 'hence', 'there',
                        }
                        non_math = [w for w in words if w.lower() not in latex_whitelist]
                        # Require >= 2 non-math words to trigger — a single word is likely a variable name
                        if len(non_math) >= 2:
                            self.errors.append({
                                "line": node.lineno,
                                "code": "MATHTEX_PLAIN_TEXT",
                                "message": (
                                    f"MathTex() contains plain text words: {non_math}. "
                                    "MathTex is for LaTeX math mode ONLY. "
                                    "For plain text use Text(). For mixed text+math use Tex() with $...$ delimiters. "
                                    "Plain words in MathTex cause 'latex error converting to dvi'."
                                )
                            })
                    # [Fix 4] Directly detect \text{} in MathTex — causes LaTeX "latex error converting to dvi"
                    # The existing MATHTEX_PLAIN_TEXT rule strips \text{} before checking — so it never fires.
                    # DeepSeek-V3 frequently hallucinates \text{slope}, \text{rise}, \text{run} etc. in MathTex.
                    if r'\text{' in s:
                        self.errors.append({
                            "line": arg.lineno,
                            "code": "LATEX_TEXT_CMD",
                            "message": (
                                r"MathTex contains \text{} which requires the amsmath LaTeX package "
                                r"(not loaded by Manim's default template). "
                                r"DO NOT replace with \mathrm{} — that also crashes in Manim v0.19/v0.20. "
                                r"Instead: use plain math symbols (e.g. \Delta y / \Delta x), "
                                r"or switch to Tex(r'$formula$ plain text') for mixed content. "
                                r"This causes 'latex error converting to dvi'."
                            )
                        })
                    # [Fix 5] \mathrm{word} in MathTex also crashes in Manim v0.19/v0.20.
                    # Confirmed: "Missing } inserted" LaTeX error when multiple \mathrm{} appear.
                    # Root cause: Manim's internal MathTex string splitter mishandles \mathrm{} braces.
                    if r'\mathrm{' in s:
                        self.errors.append({
                            "line": arg.lineno,
                            "code": "MATHRM_IN_MATHTEX",
                            "message": (
                                r"MathTex contains \mathrm{} which crashes in Manim v0.19/v0.20 "
                                r"with 'Missing } inserted' LaTeX error. "
                                r"Manim's internal string splitter mishandles \mathrm{} braces. "
                                r"FIX: remove \mathrm{} and use plain math notation instead. "
                                r"e.g. MathTex(r'm = \frac{\Delta y}{\Delta x}') — no \mathrm needed. "
                                r"For mixed text+math use Tex(r'slope $= \frac{rise}{run}$') instead."
                            )
                        })
                    # Check unescaped special chars that crash LaTeX
                    for ch in ['%', '#']:
                        if ch in s and f'\\{ch}' not in s:
                            self.errors.append({
                                "line": node.lineno,
                                "code": "MATHTEX_SPECIAL_CHAR",
                                "message": (
                                    f"MathTex() contains unescaped '{ch}' which will crash LaTeX. "
                                    f"Escape it as '\\{ch}' or use Text() for non-math content."
                                )
                            })
                            break

        # 10. [NEW] Detect add_updater(lambda: become(...)) — causes 120s render timeout
        # Rebuilding complex objects (ParametricFunction, DashedLine) every frame is too expensive.
        # Pattern: obj.add_updater(lambda m: m.become(HeavyObject(...)))
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'add_updater':
            _lambda_candidates = list(node.args) + [kw.value for kw in node.keywords]
            for arg in _lambda_candidates:
                is_risky = False
                if isinstance(arg, ast.Lambda):
                    # Walk the lambda body looking for .become() calls
                    for child in ast.walk(arg.body):
                        if (
                            isinstance(child, ast.Call)
                            and isinstance(child.func, ast.Attribute)
                            and child.func.attr == 'become'
                        ):
                            is_risky = True
                            break
                elif isinstance(arg, ast.Name) and arg.id in self._become_func_names:
                    is_risky = True
                
                if is_risky:
                    self.errors.append({
                        "line": node.lineno,
                        "code": "UPDATER_BECOME_RISK",
                        "message": (
                            "add_updater(lambda m: m.become(...)) rebuilds the object every frame "
                            "and causes a 120s render timeout for complex objects (ParametricFunction, DashedLine). "
                            "REPLACE WITH: obj = always_redraw(lambda: NewObject(...)) "
                            "and drive with self.play(tracker.animate.set_value(TARGET), run_time=N, rate_func=linear). "
                            "See MANIM_API_RULES Rule 7: ValueTracker Pattern."
                        ),
                    })
                    break  # One error per add_updater call is enough

        # 11. [NEW] Detect TransformMatchingTex/TransformMatchingShapes called with Group/VGroup args.
        # These animations require both args to have a `.tex_string` attribute (MathTex/Tex only).
        # Passing a Group/VGroup triggers: AssertionError: assert hasattr(mobject, "tex_string")
        # This is the root cause of HIGH_01 5-iteration total failure.
        if (isinstance(node.func, ast.Name) and
                node.func.id in ('TransformMatchingTex', 'TransformMatchingShapes')):
            for arg in node.args[:2]:  # Only check the first two positional args (source, target)
                if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name):
                    if arg.func.id in ('Group', 'VGroup'):
                        self.errors.append({
                            "line": node.lineno,
                            "code": "TRANSFORM_MATCHING_GROUP",
                            "message": (
                                f"{node.func.id}() requires both arguments to be MathTex or Tex objects "
                                f"(they must have a .tex_string attribute). "
                                f"You passed a {arg.func.id}() which has no .tex_string — this causes "
                                f"AssertionError at runtime. "
                                f"FIX: Use ReplacementTransform(old_mathtex, new_mathtex) for Group/VGroup, "
                                f"or ensure both args are MathTex/Tex instances directly."
                            )
                        })
                        break

        # Advisory: always_redraw without a corresponding self.play() — likely causes infinite animation
        if isinstance(node.func, ast.Name) and node.func.id == 'always_redraw':
            self.advisories.append({
                "line": node.lineno,
                "code": "ALWAYS_REDRAW_RISK",
                "message": (
                    "always_redraw() creates a continuously updating mobject. "
                    "Ensure it is driven by a finite self.play(..., run_time=N) call "
                    "(e.g. via ValueTracker.animate), otherwise the scene will hang."
                ),
            })

        # Advisory: suspiciously small non-zero buff on next_to — may cause MISALIGNED
        # (0, 0.15) range: below the Vision Agent's "obvious gap" threshold but > 0
        # These are non-blocking; they surface as hints for the TDR classifier.
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'next_to':
            for kw in node.keywords:
                if (
                    kw.arg == 'buff'
                    and isinstance(kw.value, ast.Constant)
                    and isinstance(kw.value.value, (int, float))
                    and 0 < kw.value.value < 0.15
                ):
                    self.advisories.append({
                        "line": node.lineno,
                        "code": "BUFF_SUSPICIOUS",
                        "message": (
                            f"buff={kw.value.value} is between 0 and 0.15 in next_to(). "
                            "If these objects should touch, use buff=0. "
                            "If this is intentional aesthetic spacing, ignore this advisory."
                        ),
                    })

        self.generic_visit(node)

    def visit_Subscript(self, node):
        """
        Detect hardcoded array indexing like `eq[2]` or `equation[1:3]`.
        """
        def check_name(n):
            MATHTEX_VAR_NAMES = {'eq', 'tex', 'formula', 'math_tex', 'mathtex', 'equation', 'equations'}
            
            if isinstance(n, ast.Name):
                var_name = n.id.lower()
                if var_name in MATHTEX_VAR_NAMES or var_name.startswith('eq_') or var_name.endswith('_eq') or var_name.startswith('tex_') or var_name.endswith('_tex'):
                    self.errors.append({
                        "line": node.lineno,
                        "code": "HARDCODED_MOBJECT_INDEX",
                        "message": f"Hardcoded indexing (`{n.id}[...]`) on a suspected MathTex/Tex/Text object is strictly forbidden to prevent IndexError. Use `.get_part_by_tex('substring')` or `.set_color_by_tex()` instead."
                    })
            elif isinstance(n, ast.Attribute):
                 if isinstance(n.attr, str):
                     var_name = n.attr.lower()
                     if var_name in MATHTEX_VAR_NAMES or var_name.startswith('eq_') or var_name.endswith('_eq') or var_name.startswith('tex_') or var_name.endswith('_tex'):
                         self.errors.append({
                             "line": node.lineno,
                             "code": "HARDCODED_MOBJECT_INDEX",
                             "message": f"Hardcoded indexing (`{n.attr}[...]`) on a suspected MathTex/Tex/Text object is strictly forbidden to prevent IndexError. Use `.get_part_by_tex('substring')` or `.set_color_by_tex()` instead."
                         })
            elif isinstance(n, ast.Subscript):
                check_name(n.value)
                
        check_name(node.value)
        self.generic_visit(node)

    def visit_While(self, node):
        """Detect bare `while True:` loops inside construct() — these will cause render timeout."""
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            self.errors.append({
                "line": node.lineno,
                "code": "INFINITE_LOOP",
                "message": (
                    "'while True:' inside a Manim scene will cause a render timeout (120s). "
                    "Replace with a ValueTracker + self.play(..., run_time=N) pattern. "
                    "Example: theta = ValueTracker(0); self.play(theta.animate.set_value(2*PI), run_time=8)"
                ),
            })
        self.generic_visit(node)

    def visit_Name(self, node):
        """Detect usage of 'null' (JSON syntax) instead of 'None' (Python syntax)."""
        if node.id == 'null':
            self.errors.append({
                "line": node.lineno,
                "code": "JSON_SYNTAX_ERROR",
                "message": "'null' is not valid Python. Use 'None' instead. (Common LLM mistake when translating JSON to Python)"
            })
        self.generic_visit(node)

    def visit_BinOp(self, node):
        """Detect Python 3.10+ X | Y type union syntax that crashes on Python 3.9."""
        if not isinstance(node.op, ast.BitOr):
            self.generic_visit(node)
            return

        def is_builtin_type(n):
            if isinstance(n, ast.Name):
                return n.id in self.PYTHON_BUILTIN_TYPES
            if isinstance(n, ast.Constant) and n.value is None:
                return True
            # Allow chained unions (int | str | None)
            if isinstance(n, ast.BinOp) and isinstance(n.op, ast.BitOr):
                return is_builtin_type(n.left) or is_builtin_type(n.right)
            return False

        # Only flag when BOTH sides look like type names (avoids flagging legitimate bitwise OR)
        if is_builtin_type(node.left) and is_builtin_type(node.right):
            self.errors.append({
                "line": node.lineno,
                "code": "PYTHON310_SYNTAX",
                "message": (
                    "'X | Y' type union requires Python 3.10+. "
                    "The runtime may be Python 3.9, which will raise TypeError. "
                    "Remove type annotations or use Union[X, Y] from typing instead."
                )
            })

        self.generic_visit(node)

    def visit_Constant(self, node):
        r"""Detect LaTeX strings with Python variable names in \color{} commands."""
        if isinstance(node.value, str):
            # Check if this is likely a LaTeX string (contains backslash commands)
            if '\\' in node.value:
                # Pattern: \color{PYTHON_VAR} where PYTHON_VAR is uppercase (e.g., BRIGHT_RED, YELLOW)
                # This is a common mistake where LLMs use Python constants inside LaTeX strings
                latex_color_pattern = r'\\color\{([A-Z_]+)\}'
                matches = re.findall(latex_color_pattern, node.value)
                if matches:
                    # Check if any of these look like Python constants (all uppercase)
                    for match in matches:
                        if match.isupper() and '_' in match or match in ['RED', 'BLUE', 'GREEN', 'YELLOW', 'WHITE', 'BLACK', 'BRIGHT_RED', 'DARK_BLUE']:
                            self.errors.append({
                                "line": node.lineno,
                                "code": "LATEX_COLOR_ERROR",
                                "message": f"LaTeX string contains '\\color{{{match}}}' which appears to be a Python variable. LaTeX only understands color names like 'red', 'blue', etc. Use .set_color({match}) on the MathTex object instead."
                            })
                            break  # Report only once per string

                # [TRUNCATED_LATEX] Detect LLM-truncated LaTeX commands at end of string.
                # e.g. r"\mathrm{slope} = \frac{rise}{run} = \f"  ← truncated mid-token
                # These pass Python compile() but crash LaTeX renderer with "Emergency stop" or
                # "Undefined control sequence". Pattern: string ends with \<1-4 lowercase chars>
                # that form a known incomplete prefix of a LaTeX command.
                _TRUNCATED_PREFIXES = (
                    r'\fr', r'\sq', r'\su', r'\pr', r'\pa',  # \frac \sqrt \sum \prod \partial
                    r'\cd', r'\ld', r'\ri', r'\le', r'\ov',  # \cdot \ldots \right \left \over
                    r'\ma', r'\mb', r'\te', r'\be', r'\en',  # \mathrm \mathbf \text \begin \end
                )
                _s_stripped = node.value.rstrip()
                if re.search(r'\\[a-zA-Z]{1,4}$', _s_stripped):
                    _tail = re.search(r'(\\[a-zA-Z]{1,4})$', _s_stripped).group(1)
                    # Exclude known complete short commands
                    _COMPLETE_SHORT = {
                        r'\pi', r'\mu', r'\nu', r'\xi', r'\pm', r'\ge', r'\le',
                        r'\ne', r'\in', r'\to', r'\rm', r'\bf', r'\it', r'\em',
                        r'\ln', r'\Re', r'\Im', r'\wp',
                    }
                    if _tail not in _COMPLETE_SHORT and any(_s_stripped.endswith(p) for p in _TRUNCATED_PREFIXES):
                        self.errors.append({
                            "line": node.lineno,
                            "code": "TRUNCATED_LATEX",
                            "message": (
                                f"LaTeX string appears truncated: ends with '{_tail}' which is an "
                                "incomplete LaTeX command (e.g. \\fr instead of \\frac{{...}}{{...}}). "
                                "This will crash the LaTeX renderer with 'Undefined control sequence'. "
                                "Complete the command or remove it."
                            )
                        })
        self.generic_visit(node)

def lint_file(filepath):
    if not os.path.exists(filepath):
        print(f"Error: File not found - {filepath}")
        return False, [{"line": 0, "code": "FILE_NOT_FOUND", "message": f"File not found: {filepath}"}]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        
        tree = ast.parse(source)
        linter = ManimLinter()
        linter.filename = filepath
        linter.visit(tree)

        if linter.errors:
            # print(f"❌ Static Analysis Failed for {filepath}:")
            # for err in linter.errors:
            #     print(f"  - Line {err['line']} [{err['code']}]: {err['message']}")
            return False, linter.errors
        else:
            # print(f"✅ Static Analysis Passed for {filepath}")
            return True, []

    except SyntaxError as e:
        return False, [{"line": e.lineno, "code": "SYNTAX_ERROR", "message": str(e)}]
    except Exception as e:
        return False, [{"line": 0, "code": "LINTER_EXCEPTION", "message": str(e)}]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_manim.py <file_to_lint.py>")
        sys.exit(1)
    
    success, errors = lint_file(sys.argv[1])
    if not success:
        for err in errors:
            print(f"  - Line {err.get('line', '?')} [{err.get('code', 'ERROR')}]: {err.get('message', '')}")
        sys.exit(1)
