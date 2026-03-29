import requests

url = "http://localhost:11434/api/embeddings"

def get_embedding(text):
    payload = {
        "model": "nomic-embed-text",
        "prompt": str([text])
    }
    print("Sending request to embedding API...", payload)
    response = requests.post(url, json=payload)
    print("Response status code:", response.status_code)
    result = response.json()
    return result["embedding"]