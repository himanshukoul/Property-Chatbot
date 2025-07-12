from pinecone_client import hybrid_search
from db import query_mongodb, db_users
from flask_socketio import emit
from session2 import get_or_create_session
from bson import ObjectId

def handle_search(session_id,bot_reply):
    session = get_or_create_session(session_id)
    fields = session["fields"]
    query_text = session["description"]

    top_vector_results = hybrid_search(query_text)
    print("vector result : " , top_vector_results)
    top_ids = [res["_id"] for res in top_vector_results]
    
    mongo_filters = {}
    if "price_min" in fields or "price_max" in fields:
            mongo_filters["price"] = {}
            if "price_min" in fields:
                mongo_filters["price"]["$gte"] = fields["price_min"]
            if "price_max" in fields:
                mongo_filters["price"]["$lte"] = fields["price_max"]
                
    if "area_min" in fields or "area_max" in fields:
        mongo_filters["area"] = {}
        if "area_min" in fields:
            mongo_filters["area"]["$gte"] = fields["area_min"]
        if "area_max" in fields:
            mongo_filters["area"]["$lte"] = fields["area_max"]
        
    if "property_age_min" in fields or "property_age_max" in fields:
        mongo_filters["property_age"] = {}
        if "property_age_min" in fields:
            mongo_filters["property_age"]["$gte"] = fields["property_age_min"]
        if "property_age_max" in fields:
            mongo_filters["property_age"]["$lte"] = fields["property_age_max"]
        
    if "preferred_floor_min" in fields or "preferred_floor_max" in fields:
        mongo_filters["floor_number"] = {}
        if "preferred_floor_min" in fields:
            mongo_filters["floor_number"]["$gte"] = fields["preferred_floor_min"]
        if "preferred_floor_max" in fields:
            mongo_filters["floor_number"]["$lte"] = fields["preferred_floor_max"]
    for k,v in fields.items():      
        if k not in ["location", "loc_name", "loc_lat", "loc_lon", "price_min", "price_max", "area_min", "area_max", "preferred_floor_min", "preferred_floor_max", "property_age_min", "property_age_max","amenities"]:
            mongo_filters[k] = v
            
    # if fields.get("search_type") is not None:
    #     stype = fields["search_type"]
    #     mongo_filters["post_type"] = "sell" if stype == "buy" else "rent_out" if stype == "rent" else "pg" if stype == "pg" else "commercial"
    lat = fields.get("loc_lat")
    lon = fields.get("loc_lon")
    print("MongoDB final query:", mongo_filters)

    matching_properties = query_mongodb(
        filters=mongo_filters,
        ids=top_ids,
        lat=lat,
        lon=lon
    )
    # Some cool logic is required to store it for future email sending
    # user_id = session.get("user_id")
    # if fields:
    #     db_users.update_one(
    #         {"_id": ObjectId(user_id)},
    #         {"$push": {"search_preferences": fields}}
    #     )
    print("mongo results :",matching_properties)
    emit("bot_response", {"message": bot_reply, "properties": matching_properties}, room=session_id)

