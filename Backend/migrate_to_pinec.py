import os
from pymongo import MongoClient
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.real_estate
listings = db.listings

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("description-dense-real-estate-chatbot")   

NAMESPACE = "real-estate"

batch = []
for doc in listings.find({}, {"_id": 1, "description": 1}):
    text = doc.get("description", "").strip()
    if not text:
        continue  

    batch.append({
        "_id": str(doc["_id"]),      
        "chunk_text":text
    })

for i in range(0, len(batch), 100):
    index.upsert_records(namespace=NAMESPACE, records=batch[i:i+100])

print(f"Upserted {len(batch)} documents to Pinecone.")
