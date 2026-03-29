from minio import Minio
from . import embedding
from . import taggings
from . import qdrant
from . import postgres_dao as dao
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="password",
    secure=False
)

bucket_name = "products"

def process_product_data(productId: str):
    # Placeholder for processing logic
    print("Processing product data..." + productId)
    filePath = dao.get_product_by_id(productId)
    print(f"Retrieved file path from database: {filePath.filename}")
    print(f"Fetching file {filePath.filename} from MinIO...")
    file = client.get_object(bucket_name, filePath.filename)
    image_bytes = file.read()

    # Extract tags using the taggings module
    tags = taggings.describe_product_image(image_bytes)
    tags["id"] = productId
    print("Extracted tags:", tags)

    # Generate embeddings using the embedding module
    embeddings = embedding.get_embedding(tags)
    print("Generated embeddings:", embeddings)

    # Store the embeddings and tags in Qdrant
    print("Storing in Qdrant...")
    qdrant.store_product_embedding(embeddings, tags)
    print("Product stored successfully.")

    # Clean up
    file.close()
    file.release_conn()