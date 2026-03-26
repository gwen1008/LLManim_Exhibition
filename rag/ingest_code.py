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
                    
                    # Extract used Manim modules
                    used_modules = set()
                    for subnode in ast.walk(node):
                        if isinstance(subnode, ast.Name):
                            # Common Manim classes
                            if subnode.id in ['Circle', 'Square', 'Text', 'MathTex', 'Create', 'FadeIn', 'Write']:
                                used_modules.add(subnode.id)
                    
                    chunks.append({
                        'class_name': node.name,
                        'code_content': class_code,
                        'imports': '\n'.join(imports),
                        'complexity_score': complexity,
                        'manim_modules': ', '.join(used_modules),
                        'source_file': str(filepath.relative_to(self.source_dir)),
                        'topic': filepath.relative_to(self.source_dir).parts[0]  # Extract topic from folder name
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
    
    def __init__(self, url: str = "http://localhost:8080"):
        self.client = weaviate.connect_to_local()
        
    def create_schema(self):
        """Create the ManimGoldenPair collection schema."""
        try:
            self.client.collections.delete("ManimGoldenPair")
        except:
            pass
        
        self.client.collections.create(
            name="ManimGoldenPair",
            vectorizer_config=Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(name="code_content", data_type=DataType.TEXT),
                Property(name="imports", data_type=DataType.TEXT),
                Property(name="complexity_score", data_type=DataType.INT),
                Property(name="manim_modules", data_type=DataType.TEXT),
                Property(name="source_file", data_type=DataType.TEXT),
                Property(name="topic", data_type=DataType.TEXT),  # Added topic field
                Property(name="video_description", data_type=DataType.TEXT),  # Will be filled by ingest_video.py
            ]
        )
        print("✅ Schema created: ManimGoldenPair")
    
    def upload_chunks(self, chunks: List[Dict]):
        """Upload code chunks to Weaviate."""
        collection = self.client.collections.get("ManimGoldenPair")
        
        with collection.batch.dynamic() as batch:
            for chunk in chunks:
                batch.add_object(properties=chunk)
        
        print(f"✅ Uploaded {len(chunks)} code chunks to Weaviate")
    
    def close(self):
        self.client.close()


if __name__ == "__main__":
    # Configuration
    KNOWLEDGE_BASE_DIR = "./knowledge_base"  # Where Team Member C stores examples
    
    print("🚀 Starting Code Ingestion Pipeline...")
    
    # Step 1: Extract code chunks
    chunker = ManimCodeChunker(KNOWLEDGE_BASE_DIR)
    chunks = chunker.process_directory()
    
    # Step 2: Upload to Weaviate
    indexer = WeaviateIndexer()
    indexer.create_schema()
    indexer.upload_chunks(chunks)
    indexer.close()
    
    print("🎉 Code ingestion complete!")
