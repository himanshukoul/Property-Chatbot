from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

dense_index_name = "description-dense-py"
if not pc.has_index(dense_index_name):
    pc.create_index(
        name=dense_index_name,
        vector_type="dense",
        dimension=1024,  
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

"""sparse_index_name = "description-sparse-py"
if not pc.has_index(sparse_index_name):
    pc.create_index(
        name=sparse_index_name,
        vector_type="sparse",
        metric="dotproduct",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
"""
dense_index = pc.Index(dense_index_name)
#sparse_index = pc.Index(sparse_index_name)
