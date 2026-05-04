"""
3b1b Code Ingestion Pipeline
============================
Append-only ingestion of 3b1b translated Manim CE scripts into ManimGoldenPair.

Fixes applied (from plan review):
  #1 - Append-only: never deletes or recreates schema
  #2 - Explicit class_name / source_library fields
  #3 - Strips '[3b1b translated]' prefix from description embedding
  #4 - Dedup check: skips files already indexed (by source_file)
  #5 - Extracts description from file header '# Description:' comment
  #7 - Detects external function dependencies and tags them
"""

import ast
import re
from pathlib import Path
from typing import List, Dict
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import Filter

# 3b1b 專有 Scene 類別 (在 Manim CE 中不存在)
B3_ONLY_SCENES = {
    'TeacherStudentsScene', 'PiCreatureScene', 'AltTeacherStudentsScene',
    'SampleSpaceScene', 'PositionPhaseSpaceScene',
}

MANIM_CLASSES = {
    'Circle', 'Square', 'Rectangle', 'Triangle', 'Dot', 'Line', 'Arrow', 'Vector',
    'Polygon', 'RegularPolygon', 'Ellipse', 'Annulus', 'Arc', 'Sector', 'ArcBetweenPoints',
    'CurvedArrow', 'DoubleArrow', 'DashedLine', 'Brace', 'BraceLabel',
    'SurroundingRectangle', 'Cross', 'Underline',
    'Text', 'MathTex', 'Tex', 'MarkupText', 'DecimalNumber', 'Integer',
    'NumberLine', 'Axes', 'NumberPlane', 'ComplexPlane',
    'FunctionGraph', 'ParametricFunction', 'ImplicitFunction',
    'VGroup', 'Group', 'Mobject', 'VMobject',
    'Angle', 'RightAngle',
    'Create', 'Uncreate', 'Write', 'Unwrite', 'DrawBorderThenFill',
    'FadeIn', 'FadeOut', 'FadeTransform',
    'GrowFromCenter', 'GrowArrow', 'GrowFromPoint', 'GrowFromEdge',
    'Transform', 'ReplacementTransform', 'TransformMatchingTex', 'TransformMatchingShapes',
    'Rotate', 'ScaleInPlace', 'MoveToTarget',
    'Indicate', 'Flash', 'Circumscribe', 'Wiggle', 'ApplyWave',
    'ShowPassingFlash', 'ShowCreationThenDestruction',
    'AnimationGroup', 'LaggedStart', 'LaggedStartMap', 'Succession',
    'ValueTracker', 'ComplexValueTracker',
    'UpdateFromFunc', 'UpdateFromAlphaFunc', 'always_redraw',
    'Scene', 'MovingCameraScene', 'ZoomedScene', 'ThreeDScene',
    'LinearTransformationScene',
}


class Manim3b1bChunker:
    """Extracts Scene classes from 3b1b translated Manim CE files."""

    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)

    def _extract_header_description(self, source: str) -> str:
        """Extract description from '# Description: ...' header comment.
        Fix #3: strip '[3b1b translated]' prefix to avoid embedding pollution.
        """
        match = re.search(r'#\s*Description:\s*(.*)', source)
        if match:
            desc = match.group(1).strip()
            # Fix #3: remove translation prefix tag
            desc = re.sub(r'^\[3b1b translated\]\s*', '', desc)
            return desc
        return ""

    def _detect_external_deps(self, node: ast.ClassDef, source: str) -> bool:
        """Fix #7: detect if class calls functions not defined in the same file."""
        # Collect all function/class names defined at module level
        try:
            tree = ast.parse(source)
            top_level_names = {
                n.name for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            }
            # Check if class body calls anything that looks external
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.Call):
                    if isinstance(subnode.func, ast.Name):
                        name = subnode.func.id
                        if (name not in top_level_names
                                and name not in MANIM_CLASSES
                                and not name[0].isupper()  # skip class instantiation
                                and name not in dir(__builtins__)):
                            return True
        except Exception:
            pass
        return False

    def extract_scene_classes(self, filepath: Path) -> List[Dict]:
        """Parse file and extract Scene classes with 3b1b-specific metadata."""
        source = filepath.read_text(encoding='utf-8')

        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"⚠️  Syntax error in {filepath}: {e}")
            return []

        # Extract imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"from {module} import {alias.name}")

        description = self._extract_header_description(source)

        # Derive topic from directory structure: _2018/fourier/File.py → "fourier"
        rel = filepath.relative_to(self.source_dir)
        parts = rel.parts
        topic = parts[1] if len(parts) >= 3 else parts[0]

        chunks = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            base_names = [b.id for b in node.bases if isinstance(b, ast.Name)]
            if not any('Scene' in n for n in base_names):
                continue

            class_code = ast.get_source_segment(source, node)
            complexity = sum(1 for _ in ast.walk(node) if isinstance(_, ast.Call))
            used_modules = {
                sn.id for sn in ast.walk(node)
                if isinstance(sn, ast.Name) and sn.id in MANIM_CLASSES
            }
            is_3b1b_only = any(b in B3_ONLY_SCENES for b in base_names)
            has_external_deps = self._detect_external_deps(node, source)

            chunks.append({
                'class_name': node.name,
                'code_content': class_code,
                'imports': '\n'.join(imports),
                'complexity_score': complexity,
                'manim_modules': ', '.join(used_modules),
                'source_file': str(rel),
                'source_library': '3b1b',
                'topic': topic,
                'video_description': description or f"{node.name} scene about {topic}",
                # Extra tags (stored as text for BM25 filtering)
                # is_3b1b_only and has_external_deps surfaced via class_name tagging
            })

            if is_3b1b_only:
                chunks[-1]['manim_modules'] += ', [3b1b_only_base]'
            if has_external_deps:
                chunks[-1]['manim_modules'] += ', [has_external_deps]'

        return chunks

    def process_directory(self) -> List[Dict]:
        all_chunks = []
        files = list(self.source_dir.rglob('*.py'))
        for i, py_file in enumerate(files, 1):
            chunks = self.extract_scene_classes(py_file)
            all_chunks.extend(chunks)
            if i % 100 == 0:
                print(f"  🔄 Processed {i}/{len(files)} files, {len(all_chunks)} chunks so far...")
        print(f"✅ Extracted {len(all_chunks)} Scene classes from {len(files)} files")
        return all_chunks


class Weaviate3b1bIndexer:
    """Append-only indexer for 3b1b data."""

    def __init__(self):
        self.client = weaviate.connect_to_local()

    def _get_indexed_sources(self) -> set:
        """Fix #4: fetch all already-indexed 3b1b source_files to enable dedup."""
        collection = self.client.collections.get("ManimGoldenPair")
        indexed = set()
        response = collection.query.fetch_objects(
            filters=Filter.by_property("source_library").equal("3b1b"),
            limit=10000,
        )
        for obj in response.objects:
            src = obj.properties.get("source_file", "")
            if src:
                indexed.add(src)
        return indexed

    def upload_chunks(self, chunks: List[Dict]):
        """Append chunks, skipping already-indexed files."""
        print("🔍 Checking for already-indexed 3b1b files...")
        indexed_sources = self._get_indexed_sources()
        print(f"   Found {len(indexed_sources)} already-indexed 3b1b files, skipping them.")

        to_upload = [c for c in chunks if c['source_file'] not in indexed_sources]

        if not to_upload:
            print("✅ All files already indexed. Nothing to do.")
            return

        print(f"📤 Uploading {len(to_upload)} new chunks ({len(chunks) - len(to_upload)} skipped)...")

        collection = self.client.collections.get("ManimGoldenPair")
        with collection.batch.dynamic() as batch:
            for chunk in to_upload:
                batch.add_object(properties=chunk)

        print(f"✅ Uploaded {len(to_upload)} 3b1b chunks to Weaviate")

    def close(self):
        self.client.close()


if __name__ == "__main__":
    SOURCE_DIR = "./knowledge_base/3b1b"

    print("🚀 Starting 3b1b Ingestion Pipeline (append-only)...")

    # Step 1: Extract
    chunker = Manim3b1bChunker(SOURCE_DIR)
    chunks = chunker.process_directory()

    # Step 2: Upload (append, with dedup)
    indexer = Weaviate3b1bIndexer()
    indexer.upload_chunks(chunks)
    indexer.close()

    print("🎉 3b1b ingestion complete!")
