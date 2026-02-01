# RAG System Setup Guide

## Prerequisites
- Docker installed and running
- OpenAI API key (for embeddings and GPT-4o)

## Step 1: Start Weaviate

```bash
docker-compose up -d
```

This will start Weaviate on `http://localhost:8080`.

## Step 2: Install Python Dependencies

```bash
pip install weaviate-client opencv-python openai python-dotenv
```

## Step 3: Prepare Your Knowledge Base

Create the following directory structure:

```
knowledge_base/
├── example1.py          # Manim Scene code
├── example2.py
└── videos/
    ├── example1.mp4     # Corresponding video output
    └── example2.mp4
```

**Important**: Video filenames must match the Python filenames (e.g., `example1.py` → `example1.mp4`).

## Step 4: Run Code Ingestion

```bash
python rag/ingest_code.py
```

This will:
- Parse all `.py` files in `knowledge_base/`
- Extract complete Scene classes using AST
- Upload them to Weaviate with metadata

## Step 5: Run Video Ingestion

```bash
python rag/ingest_video.py
```

This will:
- Extract keyframes from each MP4
- Use GPT-4o to generate visual descriptions
- Link descriptions to the corresponding code chunks

## Step 6: Verify the Index

```python
import weaviate

client = weaviate.connect_to_local()
collection = client.collections.get("ManimGoldenPair")

# Check total objects
print(f"Total indexed: {len(collection)}")

# Sample query
result = collection.query.near_text(
    query="rotating square",
    limit=1
)

print(result.objects[0].properties)
client.close()
```

## Troubleshooting

- **Weaviate not starting**: Check Docker logs with `docker-compose logs`
- **OpenAI errors**: Verify `OPENAI_API_KEY` is set in `.env`
- **No code chunks found**: Ensure your `.py` files contain classes inheriting from `Scene`
