from mem0 import MemoryClient
import os
import datetime
from uuid import uuid4
import load_env

client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))

# there is no way to query deeper lexically in mem0.ai ....
# def generate_categories(intent, loc_name = None, bedrooms = None, price= None):
#     categories = []
#     if intent:
#         categories.append(intent.lower())
#     if loc_name:
#         categories.append(f"loc:{loc_name.lower()}")
#     if bedrooms is not None:
#         categories.append(f"bhk:{bedrooms}")
#     if price is not None:
#         categories.append(f"price:{price}")
#     return categories

def upsert_memory(user_id, description, intent, metadata):
    messages = [{"role": "user", "content": description}]
    enriched_metadata = {
        **metadata,
        "intent": intent,
        "description": description,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    # categories = generate_categories(
    #     intent=intent,
    #     loc_name=metadata.get("loc_name"),
    #     bedrooms=metadata.get("bedrooms"),
    #     price=metadata.get("price")
    # )

    try:
        client.add(
            messages=messages,
            user_id=user_id,
            metadata=enriched_metadata,
            #categories=categories,
            chunk_size=None,
            #immutable=True
        )
        print("[Mem0] Memory upserted successfully.")
    except Exception as e:
        print(f"[Mem0 Upsert Error] {e}")

def search_similar_users(posted_description, loc_name, bhk, price, current_user_id):
    filters = {
        "user_id": {"ne": current_user_id}
    }

    try:
        results = client.search(
            query=posted_description,
            version="v2",
            filters=filters,
            top_k=10 
        )

        # i decided to do semantic search first, and manually filter the results in py
        matches = []
        for m in results:
            meta = m.get("metadata", {})
            if (
                meta.get("intent") == "search" and
                meta.get("loc_name", "").lower() == loc_name.lower()
            ):
                matches.append(m)

        print(f"[Mem0] Matching user memories after location filter: {len(matches)}")
        return matches

    except Exception as e:
        print(f"[Mem0 Search Error] {e}")
        return []


def get_memories(user_id, top_k = 3):
    try:
        response = client.get_all(user_id=user_id, page=1, page_size=top_k)
        print("Raw Mem0 get_all response:", response)

        return [
            {
                "memory_id": m.get("id"),
                "text": m.get("metadata", {}).get("description", ""),
                "user_id": user_id
            }
            for m in response.get("results", [])
        ]
    except Exception as e:
        print(f"[Mem0 Get Error] {e}")
        return []
