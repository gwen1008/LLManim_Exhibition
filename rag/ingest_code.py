"""
Code Ingestion Pipeline: AST-Based Chunking for Manim Scripts
==============================================================
This script parses Python files containing Manim Scene classes and extracts them
as complete, syntactically valid chunks for indexing in Weaviate.

Key Features:
- AST-based parsing (preserves class structure)
- Automatic import extraction
- Metadata enrichment (complexity, used modules)
"""

import ast
import os
from pathlib import Path
from typing import List, Dict
import weaviate
from weaviate.classes.config import Configure, Property, DataType


MANIM_CLASSES = {
    # Shapes / Mobjects
    'Circle', 'Square', 'Rectangle', 'Triangle', 'Dot', 'Line', 'Arrow', 'Vector',
    'Polygon', 'RegularPolygon', 'Ellipse', 'Annulus', 'Arc', 'Sector', 'ArcBetweenPoints',
    'CurvedArrow', 'DoubleArrow', 'DashedLine', 'Brace', 'BraceLabel',
    'SurroundingRectangle', 'Cross', 'Underline',
    # Text / Math
    'Text', 'MathTex', 'Tex', 'MarkupText', 'DecimalNumber', 'Integer',
    # Axes & Graphs
    'NumberLine', 'Axes', 'NumberPlane', 'ComplexPlane',
    'FunctionGraph', 'ParametricFunction', 'ImplicitFunction',
    # Groups
    'VGroup', 'Group', 'Mobject', 'VMobject',
    # Geometry helpers
    'Angle', 'RightAngle',
    # Animations
    'Create', 'Uncreate', 'Write', 'Unwrite', 'DrawBorderThenFill',
    'FadeIn', 'FadeOut', 'FadeTransform',
    'GrowFromCenter', 'GrowArrow', 'GrowFromPoint', 'GrowFromEdge',
    'Transform', 'ReplacementTransform', 'TransformMatchingTex', 'TransformMatchingShapes',
    'Rotate', 'ScaleInPlace', 'MoveToTarget',
    'Indicate', 'Flash', 'Circumscribe', 'Wiggle', 'ApplyWave',
    'ShowPassingFlash', 'ShowCreationThenDestruction',
    'AnimationGroup', 'LaggedStart', 'LaggedStartMap', 'Succession',
    # Updaters / Trackers
    'ValueTracker', 'ComplexValueTracker',
    'UpdateFromFunc', 'UpdateFromAlphaFunc', 'always_redraw',
    # Scene types
    'Scene', 'MovingCameraScene', 'ZoomedScene', 'ThreeDScene',
}


class ManimCodeChunker:
    """Extracts complete Scene classes from Manim Python files."""
    
    def __init__(self, source_dir: str):
        self.source_dir = Path(source_dir)
        
    def extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract all import statements from the module."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"from {module} import {alias.name}")
        return imports
    
    def extract_scene_classes(self, filepath: Path) -> List[Dict]:
        """Parse file and extract Scene classes with metadata."""
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"⚠️  Syntax error in {filepath}: {e}")
            return []
        
        imports = self.extract_imports(tree)
        chunks = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it inherits from Scene (or subclasses)
                base_names = [base.id for base in node.bases if isinstance(base, ast.Name)]
                if any('Scene' in name for name in base_names):
                    # Extract the complete class code
                    class_code = ast.get_source_segment(source, node)
                    
                    # Calculate complexity (number of method calls)
                    complexity = sum(1 for _ in ast.walk(node) if isinstance(_, ast.Call))
                    
                    # Extract docstring to use as video_description
                    docstring = ast.get_docstring(node)
                    topic_name = filepath.relative_to(self.source_dir).parts[0]
                    video_desc = docstring.strip() if docstring else f"{node.name} example about {topic_name}"

                    # Extract used Manim modules (uses module-level MANIM_CLASSES constant)
                    used_modules = set()

                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Name):
                            if subnode.id in MANIM_CLASSES:
                                used_modules.add(subnode.id)
                    
                    chunks.append({
                        'class_name': node.name,
                        'code_content': class_code,
                        'imports': '\n'.join(imports),
                        'complexity_score': complexity,
                        'manim_modules': ', '.join(used_modules),
                        'source_file': str(filepath.relative_to(self.source_dir)),
                        'source_library': 'examples',
                        'topic': topic_name,
                        'video_description': video_desc
                    })
        
        return chunks
    
    def process_directory(self) -> List[Dict]:
        """Process all .py files in the source directory."""
        all_chunks = []
        for py_file in self.source_dir.rglob('*.py'):
            print(f"📄 Processing: {py_file.name}")
            chunks = self.extract_scene_classes(py_file)
            all_chunks.extend(chunks)
        
        print(f"✅ Extracted {len(all_chunks)} Scene classes")
        return all_chunks


class WeaviateIndexer:
    """Handles Weaviate schema creation and data upload."""

    def __init__(self, url: str = "http://localhost:8080", collection_name: str = "ManimGoldenPair"):
        self.client = weaviate.connect_to_local()
        self.collection_name = collection_name

    def create_schema(self):
        """Create the collection schema.

        Always drops + recreates: switching vectorizer (or its dimensions)
        leaves old vectors with incompatible shape and breaks retrieval
        silently. Drop + re-ingest is cheap (<60 chunks per KB).

        Vectorizer: text2vec-google with gemini-embedding-001
        (Google's current production embedding model — replaces deprecated
        embedding-001 / text-embedding-004).
        """
        existing = [c.name for c in self.client.collections.list_all().values()]
        if self.collection_name in existing:
            print(f"⚠️  Existing collection {self.collection_name} found — dropping for clean re-ingest")
            self.client.collections.delete(self.collection_name)

        self.client.collections.create(
            name=self.collection_name,
            vectorizer_config=Configure.Vectorizer.text2vec_google_aistudio(
                model_id="gemini-embedding-001",
            ),
            properties=[
                # skip_vectorization=True: BM25 still indexes these for keyword search,
                # but they are NOT included in the OpenAI embedding vector.
                # Embedding only from video_description (natural language) + manim_modules.
                Property(name="class_name", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="code_content", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="imports", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="complexity_score", data_type=DataType.INT),
                Property(name="manim_modules", data_type=DataType.TEXT),  # vectorized: module names are useful signals
                Property(name="source_file", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="source_library", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="topic", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="video_description", data_type=DataType.TEXT),  # vectorized: primary semantic field
            ]
        )
        print(f"✅ Schema created: {self.collection_name}")

    def upload_chunks(self, chunks: List[Dict]):
        """Upload code chunks to Weaviate.

        rate_limit=60 RPM keeps us under Gemini free-tier's 100 RPM cap.
        Without throttling, dynamic() batches fire concurrent vectorize
        requests and hit Google 429 on ~half the inserts.
        """
        collection = self.client.collections.get(self.collection_name)

        with collection.batch.rate_limit(requests_per_minute=60) as batch:
            for chunk in chunks:
                batch.add_object(properties=chunk)

        failed = collection.batch.failed_objects
        if failed:
            print(f"❌ {len(failed)} chunks failed to upload (first 3):")
            for f in failed[:3]:
                print(f"   - {f.message}")
        print(f"✅ Uploaded {len(chunks) - len(failed)} / {len(chunks)} code chunks to {self.collection_name}")
    
    def close(self):
        self.client.close()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Ingest Manim Scene KB into Weaviate")
    ap.add_argument(
        "--kb-dir", default=os.environ.get("RAG_KB_DIR", "./knowledge_base/examples"),
        help="Directory holding Scene .py files (default: ./knowledge_base/examples, "
             "or env RAG_KB_DIR if set)",
    )
    ap.add_argument(
        "--collection", default=os.environ.get("RAG_COLLECTION", "ManimGoldenPair"),
        help="Weaviate collection name (default: ManimGoldenPair, or env RAG_COLLECTION if set)",
    )
    args = ap.parse_args()

    print(f"🚀 Starting Code Ingestion Pipeline...")
    print(f"   KB dir:     {args.kb_dir}")
    print(f"   Collection: {args.collection}")

    # Step 1: Extract code chunks
    chunker = ManimCodeChunker(args.kb_dir)
    chunks = chunker.process_directory()

    # Step 2: Upload to Weaviate
    indexer = WeaviateIndexer(collection_name=args.collection)
    indexer.create_schema()
    indexer.upload_chunks(chunks)
    indexer.close()

    print("🎉 Code ingestion complete!")
