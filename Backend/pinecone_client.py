"""from pinecone_config import dense_index, sparse_index
from sentence_transformers import SentenceTransformer
from pinecone_text.sparse import BM25Encoder

dense_model = SentenceTransformer("intfloat/multilingual-e5-large")
sparse_model = BM25Encoder()

NAMESPACE = "real-estate"

def embed_dense(text):
    return dense_model.encode(text).tolist()

def embed_sparse(text):
    return sparse_model.encode_documents([text])[0]

def upsert_listing(doc_id, text):
    dense_vec = embed_dense(text)
    sparse_vec = embed_sparse(text)
    metadata = {"chunk_text": text}

    dense_index.upsert(
        namespace=NAMESPACE,
        vectors=[{"id": doc_id, "values": dense_vec, "metadata": metadata}]
    )
    sparse_index.upsert(
        namespace=NAMESPACE,
        vectors=[{"id": doc_id, "values": sparse_vec, "metadata": metadata}]
    )

def delete_listing(doc_id):
    dense_index.delete(ids=[doc_id], namespace=NAMESPACE)
    sparse_index.delete(ids=[doc_id], namespace=NAMESPACE)

def hybrid_search(query, top_k=10):
    dense_vec = embed_dense(query)
    sparse_vec = embed_sparse(query)

    dres = dense_index.query(
        namespace=NAMESPACE,
        vector=dense_vec,
        top_k=top_k,
        include_metadata=True
    )
    sres = sparse_index.query(
        namespace=NAMESPACE,
        vector=sparse_vec,
        top_k=top_k,
        include_metadata=True
    )

    return merge_chunks(sres, dres)

def merge_chunks(h1, h2):
    all_hits = h1["matches"] + h2["matches"]
    deduped = {}
    for hit in all_hits:
        doc_id = hit["id"]
        score = hit["score"]
        text = hit["metadata"].get("chunk_text", "")
        if doc_id not in deduped or deduped[doc_id]["score"] < score:
            deduped[doc_id] = {"_id": doc_id, "_score": score, "chunk_text": text}
    return sorted(deduped.values(), key=lambda x: x["_score"], reverse=True)
"""

from pinecone_config import dense_index
from sentence_transformers import SentenceTransformer

dense_model = SentenceTransformer("intfloat/multilingual-e5-large")

NAMESPACE = "real-estate"

def embed_dense(text):
    return dense_model.encode(text).tolist()

def upsert_listing(doc_id, text):
    dense_vec = embed_dense(text)
    metadata = {"chunk_text": text}

    dense_index.upsert(
        namespace=NAMESPACE,
        vectors=[{"id": doc_id, "values": dense_vec, "metadata": metadata}]
    )

def delete_listing(doc_id):
    dense_index.delete(ids=[doc_id], namespace=NAMESPACE)

def hybrid_search(query, top_k=10):
    dense_vec = embed_dense(query)

    results = dense_index.query(
        namespace=NAMESPACE,
        vector=dense_vec,
        top_k=top_k,
        include_metadata=True
    )

    return merge_chunks(results)

def merge_chunks(results):
    all_hits = results["matches"]
    deduped = {}
    for hit in all_hits:
        doc_id = hit["id"]
        score = hit["score"]
        text = hit["metadata"].get("chunk_text", "")
        if doc_id not in deduped or deduped[doc_id]["score"] < score:
            deduped[doc_id] = {"_id": doc_id, "_score": score, "chunk_text": text}
    return sorted(deduped.values(), key=lambda x: x["_score"], reverse=True)
