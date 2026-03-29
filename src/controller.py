from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from . import embedding
from . import taggings
from . import qdrant
from . import bucket_minio
from . import kafka_producer
import json
import uuid
from kafka import KafkaConsumer
from . import product_processor
from . import postgres_dao as dao
from . import product as p 
import threading
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
OLLAMA_URL = "http://localhost:11434/api/chat"

# Serve the main HTML page
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.get("/search-products")
def home():
    return FileResponse("frontend/chat.html")


# API endpoint to add a new product with image upload and metadata
@app.post("/products")
async def add_product(
    file: UploadFile,
    name: str = Form(...),
    price: float = Form(...),
    brand: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    attributes: str = Form(...)
):
    # ✅ generate unique ID
    product_id = str(uuid.uuid4())
    print(f"Generated product ID: {product_id}")

    # convert attributes string → JSON
    attributes_dict = json.loads(attributes)
    product = p.Product(product_id, name, price, brand, description, category, attributes_dict, file.filename)

    # 1. Store product metadata in PostgreSQL
    print("Storing product metadata in PostgreSQL...")
    dao.insert_record(product)
    print("Product metadata stored successfully.")

    # 2. Upload image to MinIO
    print("Received product:", product_id)
    print("Uploading image to MinIO...")
    await bucket_minio.upload_product_image(file, category)
    print("Image uploaded to MinIO successfully.")


    # 3. Send message to Kafka
    kafka_payload = {
        "id": str(product_id)
    }

    kafka_producer.send_product_message(kafka_payload)
    print("Message sent to Kafka successfully.")
    return {"message": "Product added successfully", "product": product}


# Define the request structure
class ChatRequest(BaseModel):
    message: str

# Define the response structure
class ChatResponse(BaseModel):
    text: str
    image_url: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    user_text = request.message.lower()
    embeddings = embedding.get_embedding(user_text)
    print("Generated embeddings for query.")
    qdrant_res = qdrant.search_similar_products(embeddings, 1)
    print("Received search results from Qdrant.")

    prod = []
    for res in qdrant_res:
        print("Database", dao.get_product_by_id(res.id))
        prod.append(dao.get_product_by_id(res.id))
        # print(f"Fetched product details from PostgreSQL for ID: {prod[-1].id}")

    chat_response = ChatResponse(text="", image_url=None)
    chat_response.text = "Here are some products that match your query."
    chat_response.text += "\n\n" + "\n\n".join([f"- {p.name} (${p.price})" for p in prod])
    chat_response.image_url = "products/"+prod[0].filename
    print(f"Retrieved {len(prod)} products from PostgreSQL based on Qdrant results'")
    return chat_response

# Kafka consumer function to process messages from "products" topic 
def consume_messages():
    consumer = KafkaConsumer(
        'products',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Kafka consumer started...")
    for message in consumer:
        print("Received :", message.value)
        print("Processing product data...")
        product_processor.process_product_data(message.value["id"])
        print("Product data processed successfully.")


# Start consumer in background thread
@app.on_event("startup")
def start_kafka_consumer():
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()