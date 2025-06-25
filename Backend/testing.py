from sentence_transformers import SentenceTransformer
from pinecone_text.sparse import BM25Encoder

dense_model = SentenceTransformer("intfloat/multilingual-e5-large")
sparse_model = BM25Encoder()
