## Working of Application

1. Developed search platform using vector embeddings to replace keyword matching with natural language queries.
2. Built a scalable pipeline that separates image storage from intensive AI tasks, automating product tagging and
metadata generation using the Gemma vision model.
3. Converted product descriptions into embeddings using Mistral (via Ollama) and indexed them in Qdrant,
allowing users to find items via descriptive prompts and PostgreSQL retrieval.
## Technologies Used
1. Programming Language: Python
2. Storage: Postgresql (RDBMS), QDrant (Vector Database), MinIO(Object Storage)
3. Messaging Service: Kafka
4. LLM: Mistal for NLP, Gemma for VLM


## System Design
<img src="https://raw.githubusercontent.com/Nikesh559/ecommerce-semantic-search/refs/heads/main/system-design.png" alt="Alt text" width="700">

## Page to add Product
<img src="https://raw.githubusercontent.com/Nikesh559/ecommerce-semantic-search/refs/heads/main/product-add.png" alt="Alt text" width="700">

## Chat Bot Page 

<img src="https://raw.githubusercontent.com/Nikesh559/ecommerce-semantic-search/refs/heads/main/chat-ss.png" alt="Alt text" width="700">

