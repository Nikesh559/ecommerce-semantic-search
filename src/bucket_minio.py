from minio import Minio
import json
import io
from fastapi import UploadFile

# MinIO client
client = Minio(
    "localhost:9000",  # change if needed
    access_key="admin",
    secret_key="password",
    secure=False
)

BUCKET_NAME = "products"

# Define a Public Read-Only policy
public_read_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
            "Resource": [f"arn:aws:s3:::{BUCKET_NAME}"]
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{BUCKET_NAME}/*"]
        }
    ]
}

# Apply the policy
client.set_bucket_policy(BUCKET_NAME, json.dumps(public_read_policy))
print(f"Bucket '{BUCKET_NAME}' is now Public (Read-Only).")

async def upload_product_image(file:UploadFile, category):
    object_name = f"{category}/{file.filename}"
    file_bytes = await file.read()
    data_stream = io.BytesIO(file_bytes)
    # 4. Upload to MinIO
    client.put_object(
        BUCKET_NAME,
        object_name,
        data_stream,  # file stream
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=file.content_type
    )
    print(f"Uploaded {file.filename} to MinIO bucket '{BUCKET_NAME}' successfully.")
    # 5. Return metadata
    return {
        "id": file.filename,  # or generate a unique ID
        "filepath": category + "/" + file.filename,
        "url": f"http://localhost:9000/{BUCKET_NAME}/{file.filename}"
    }