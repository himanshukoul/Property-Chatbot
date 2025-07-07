from pinecone_client import upsert_listing
from db import post_listings, db_users
from flask_socketio import emit
from session2 import get_or_create_session, reset_session
import uuid
from bson import ObjectId
from email_sender import send_property_alert
from mem0_client import search_similar_users

REQUIRED_FIELDS = [
    "loc_name", "listing_type", "property_type", "ownership", "price", "area",
    "bedrooms", "bathrooms", "furnishing", "available_from", "amenities",
    "floor_number", "total_floors", "property_age"
]

def handle_post(session_id, bot_reply):
    session = get_or_create_session(session_id)
    fields = session["fields"]
    user_id = session.get("user_id")
    if not user_id:
        emit("bot_response", {"message": "Authentication required to post"}, room=session_id)
        return
    missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]
    if missing:
        message = bot_reply or f"To post your property, I still need: {', '.join(missing)}. Could you please share those?" #fallback manual
        emit("bot_response", {"message": message}, room=session_id)
        return
    
    
    description = session["description"]
    
    doc = {
        "_id": "temporary",
        "user_id": user_id,
        "city": fields["location"]["city"],
        "location": fields["loc_name"],
        "listing_type": fields["listing_type"],
        "property_type": fields["property_type"],
        "ownership": fields["ownership"],
        "price": fields["price"],
        "area": fields["area"],
        "bedrooms": fields["bedrooms"],
        "bathrooms": fields["bathrooms"],
        "furnishing": fields["furnishing"],
        "available_from": fields["available_from"],
        "amenities": fields["amenities"],
        "floor_number": fields["floor_number"],
        "total_floors": fields["total_floors"],
        "property_age": fields["property_age"],
        "description": description,
        "location_point": {
            "type": "Point",
            "coordinates": [fields["loc_lon"], fields["loc_lat"]]
        }
    }
    
    if not fields.get("confirm"):
        message = bot_reply or "You can still modify your property and confirm it later."
        emit("bot_response", {"message": message,"properties": [doc]}, room=session_id)
        return
    
    doc_id = str(uuid.uuid4())
    doc["_id"] = doc_id
    
    post_listings(doc)
    upsert_listing(doc_id, description)
    
    matches = search_similar_users(description, fields["loc_name"], fields["bedrooms"], fields["price"],session["user_id"])
    #checkout returned json
    print(matches)
    for m in matches:
        matched_user_id = m.get("user_id")
        if matched_user_id == user_id:
            continue  
        user = db_users.find_one({"_id": ObjectId(matched_user_id)})
        if user and user.get("email"):
            send_property_alert(user["email"], doc)  

    # user preferences
    # post_prefs = {
    #     "location": fields.get("location"),
    #     "listing_type": fields.get("listing_type"),
    #     "property_type": fields.get("property_type"),
    #     "price": fields.get("price"),
    #     "area": fields.get("area")
    # }
    # db_users.update_one(
    #     {"_id": ObjectId(user_id)},
    #     {"$push": {"post_preferences": post_prefs}}
    # )
    message = bot_reply or "Your property has been successfully posted! You can now upload some photos to make it more attractive to buyers or tenants."
    emit("bot_response", {"message": message, "properties": [doc]}, room=session_id)
    reset_session(session_id)
