"""
Quick script to verify Weaviate has data
"""
import weaviate

client = weaviate.connect_to_local()
collection = client.collections.get("ManimGoldenPair")

# Check total count
total = len(collection)
print(f"📊 Total objects in Weaviate: {total}")

if total > 0:
    # Fetch one object to inspect
    result = collection.query.fetch_objects(limit=1)
    if result.objects:
        obj = result.objects[0]
        print(f"\n✅ Sample object found:")
        print(f"   Code: {obj.properties.get('code_content', '')[:100]}...")
        print(f"   Imports: {obj.properties.get('imports', 'N/A')}")
        print(f"   Modules: {obj.properties.get('manim_modules', 'N/A')}")
else:
    print("⚠️  No objects found in Weaviate!")

client.close()
