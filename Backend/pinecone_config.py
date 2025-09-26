import load_env
from pinecone import Pinecone
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

dense_index = "description-dense-real-estate-chatbot"

if not pc.has_index(dense_index):
    pc.create_index_for_model(
        name=dense_index,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"multilingual-e5-large",
            "field_map":{"text": "chunk_text"}
        }
    )

"""dense_index_name = "description-dense-py"
if not pc.has_index(dense_index_name):
    pc.create_index(
        name=dense_index_name,
        vector_type="dense",
        dimension=1024,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
"""

dense_index = pc.Index(dense_index)
