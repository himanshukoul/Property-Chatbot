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
