import weaviate
import json

client = weaviate.connect_to_local()

try:
    collection = client.collections.get("ManimGoldenPair")
    
    # 查詢包含 "3b1b" 的 source_file 數量
    response = collection.query.fetch_objects(
        filters=weaviate.classes.query.Filter.by_property("source_file").like("*3b1b*"),
        limit=5
    )
    
    print(f"🔍 找到 {len(response.objects)} 個來自 3b1b 的對象 (前 5 個):")
    for obj in response.objects:
        print(f"- {obj.properties.get('source_file')}")
        
    # 同時統計總量
    total_response = collection.aggregate.over_all(
        filters=weaviate.classes.query.Filter.by_property("source_file").like("*3b1b*"),
        total_count=True
    )
    print(f"📊 3b1b 在資料庫中的總數: {total_response.total_count}")

except Exception as e:
    print(f"❌ 發生錯誤: {e}")
finally:
    client.close()
