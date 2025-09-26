from pinecone_config import dense_index

NAMESPACE = "real-estate"

def upsert_listing(doc_id, text):
    dense_index.upsert_records(
        namespace=NAMESPACE,
        records=[{"_id": doc_id,"chunk_text":text}]
    )

def delete_listing(doc_id):
    dense_index.delete(ids=[doc_id], namespace=NAMESPACE)

def hybrid_search(query, top_k=10):

    results = dense_index.search(
        namespace=NAMESPACE,
        query={"inputs": {"text": query}, "top_k": top_k},
        fields=["chunk_text"]
    )
    return [
        {
            "_id": hit["_id"],
            "_score": hit["_score"],
            "chunk_text": hit["fields"].get("chunk_text", "")
        }
        for hit in results.result.hits
    ]
    
