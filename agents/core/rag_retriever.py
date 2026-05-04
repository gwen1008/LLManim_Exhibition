"""
RAG Retriever Module
====================
Handles retrieval of 'Golden Manim Examples' from Weaviate to ground the Coder agent.
"""

import weaviate
from weaviate.classes.query import MetadataQuery, Filter
from typing import List, Dict

class RAGRetriever:
    """Interface for retrieving semantic code examples from vector database."""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        # Connect to local Weaviate instance
        # Note: In docker-compose we set OPENAI_APIKEY env var for the container.
        # Here we rely on the python client using the local env var if needed for client-side operations,
        # but mostly we rely on the server-side text2vec-openai module.
        try:
            self.client = weaviate.connect_to_local(host=host, port=port)
            self._check_connection()
        except Exception as e:
            print(f"⚠️  RAG Warning: Could not connect to Weaviate at {host}:{port}. Error: {e}")
            self.client = None

    def _check_connection(self):
        """Verify connection to Weaviate."""
        if self.client and self.client.is_live():
            print("✅ RAG System: Connected to Weaviate.")
        else:
            print("⚠️  RAG System: Weaviate is not live.")
            self.client = None

    def retrieve_examples(self, query: str, limit: int = 2) -> List[Dict]:
        """Retrieve code examples with source-balanced results.

        Fix #4: To prevent 3b1b (918 items) from dominating over curated examples (90 items),
        we split the limit evenly: half from examples, half from 3b1b.
        """
        if not self.client:
            return []
        try:
            collection = self.client.collections.get("ManimGoldenPair")
            SCORE_THRESHOLD = 0.4
            results = []

            # Fetch from each source separately to avoid volume bias
            per_source_limit = max(1, limit // 2)
            sources = [
                ("examples", Filter.by_property("source_library").equal("examples")),
                ("3b1b",     Filter.by_property("source_library").equal("3b1b")),
                # Legacy entries without source_library tag
                ("legacy",   None),
            ]

            for source_name, f in sources:
                if len(results) >= limit:
                    break

                # Skip legacy if we already have enough results
                if source_name == "legacy" and len(results) >= limit:
                    continue

                kwargs = dict(
                    query=query,
                    limit=per_source_limit,
                    alpha=0.5,
                    return_metadata=__import__(
                        'weaviate.classes.query', fromlist=['MetadataQuery']
                    ).MetadataQuery(score=True)
                )
                if f is not None:
                    kwargs['filters'] = f
                elif source_name == "legacy":
                    # Only pick up objects that have no source_library set
                    kwargs['filters'] = Filter.by_property("source_file").not_equal("3b1b")

                response = collection.query.hybrid(**kwargs)
                for obj in response.objects:
                    src = obj.properties.get("source_file", "")
                    if src.startswith("manim_ce_rules"):
                        continue
                    score = obj.metadata.score
                    desc = obj.properties.get("video_description", "No description")
                    print(f"  📋 [{source_name}|score={score:.3f}] {desc[:60]}")
                    if score < SCORE_THRESHOLD:
                        continue
                    results.append({
                        "description": desc,
                        "code": obj.properties.get("code_content", ""),
                        "imports": obj.properties.get("imports", ""),
                        "modules": obj.properties.get("manim_modules", ""),
                        "score": score,
                        "kind": "example",
                        "source": source_name,
                    })

            print(f"🔍 RAG Examples: {len(results)} relevant (threshold={SCORE_THRESHOLD}) for '{query[:40]}'")
            return results[:limit]
        except Exception as e:
            print(f"⚠️  RAG Retrieval Failed: {e}")
            return []

    def retrieve_rules(self, query: str, limit: int = 2) -> List[Dict]:
        """Retrieve Manim CE API rules/best-practices (manim_ce_rules only)."""
        if not self.client:
            return []
        try:
            collection = self.client.collections.get("ManimGoldenPair")
            response = collection.query.hybrid(
                query=query,
                limit=limit,
                alpha=0.5,
                filters=Filter.by_property("source_file").like("manim_ce_rules*"),
                return_metadata=MetadataQuery(score=True)
            )
            SCORE_THRESHOLD = 0.35
            results = []
            for obj in response.objects:
                score = obj.metadata.score
                desc = obj.properties.get("video_description", "")
                print(f"  📖 [score={score:.3f}] {desc[:60]}")
                if score < SCORE_THRESHOLD:
                    continue
                results.append({
                    "description": desc,
                    "code": obj.properties.get("code_content", ""),
                    "modules": obj.properties.get("manim_modules", ""),
                    "score": score,
                    "kind": "rule",
                })
            print(f"📖 RAG Rules: {len(results)} relevant (threshold={SCORE_THRESHOLD}) for '{query[:40]}'")
            return results
        except Exception as e:
            print(f"⚠️  RAG Rules Retrieval Failed: {e}")
            return []

    def _prune_code(self, code: str) -> str:
        """Return the class code as stored, hard-limited to 100 lines.
        
        This prevents massive files from bloating the LLM context window.
        """
        lines = code.split("\n")
        if len(lines) > 100:
            return "\n".join(lines[:100]) + "\n\n        # ... (code truncated to 100 lines to save context)"
        return code

    def format_for_prompt(self, examples: List[Dict]) -> str:
        """Format retrieved examples+rules into a string for the LLM prompt.

        Accepts mixed list from retrieve_examples() and/or retrieve_rules().
        Items are separated by kind: code examples first, then API rules.
        """
        if not examples:
            return ""

        code_items = [e for e in examples if e.get("kind") != "rule"]
        rule_items = [e for e in examples if e.get("kind") == "rule"]

        formatted = ""

        if code_items:
            formatted += "\n\n=== 📚 REFERENCE EXAMPLES (RAG - Verified Code) ===\n"
            formatted += "Use these verified patterns. Full imports/class structure are in your system prompt.\n"
            for i, ex in enumerate(code_items, 1):
                formatted += f"\n--- Example {i} ---\n"
                formatted += f"Visual: {ex['description']}\n"
                if ex.get("imports"):
                    formatted += f"Imports: {ex['imports']}\n"
                pruned_code = self._prune_code(ex['code'])
                formatted += f"Core Logic:\n```python\n{pruned_code}\n```\n"

        if rule_items:
            formatted += "\n\n=== 📖 MANIM CE API RULES (RAG - Best Practices) ===\n"
            formatted += "Follow these API rules strictly. Do NOT call methods not listed here.\n"
            for ex in rule_items:
                formatted += f"\n{ex['code']}\n"

        return formatted

    def close(self):
        """Close the client connection."""
        if self.client:
            self.client.close()
