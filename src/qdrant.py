import requests
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)
print("Connected to Qdrant successfully.", client.get_collections())
collection_name = "product-embeddings "

def store_product_embedding(embedding, product):
    print("Storing product embedding in Qdrant..." + product["id"])
    point = PointStruct(
        id=product["id"],
        vector=embedding,
        payload=product
    )
    client.upsert(
        collection_name=collection_name,
        points=[point]
    )

def search_similar_products(query_embedding, top_k=1):
    results = client.query_points(
        collection_name=collection_name,
        query=query_embedding,   # ✅ correct
        limit=3
    )

    for r in results.points:
        print(f"ID: {r.id}, Score: {r.score}, Payload: {r.payload}")
    filtered = [
        r for r in results.points
        if r.score > 0.42   # tune this (0.6–0.8)
    ]

    if not filtered:
        print("No relevant results found")
    print(f"Found {len(filtered)} similar products")
    return filtered