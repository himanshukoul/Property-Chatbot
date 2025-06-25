import load_env
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from config import DevelopmentConfig
from extractors2 import extract_fields_from_query
from session2 import *
from geocode import geocode_location
from search_handler import handle_search
from post_handler import handle_post 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("message")
def handle_message(data):
    user_msg = data.get("msg", "")
    session_id = request.sid
    if user_msg.lower().strip() in ["yes", "confirm", "go ahead", "looks good", "post it"]:
        update_field(session_id, "confirm", True)
        handle_post(session_id, None)
        return
    mode = get_or_create_session(session_id)['mode']
    print(f"User said: {user_msg}")
    if(mode == 'common'):
        extracted = extract_fields_from_query(user_msg,get_fields(session_id),'common')
    elif (mode == 'search'):
        extracted = extract_fields_from_query(user_msg,get_fields(session_id),'search')
    else:
        extracted = extract_fields_from_query(user_msg,get_fields(session_id),'post')

    #update_description(session_id, user_msg)
    #extracted_items = extracted.items()
    if(extracted.get("user_message")): update_description(session_id,extracted.get("user_message"))
    intent = extracted.get("data", {}).get("intent")

    
    if(intent and mode != "common" and mode != intent):
        #can save this data somewhere across session  post<->search
        reset_session(session_id)
        get_or_create_session(session_id)
        
    for k, v in (extracted.get("data") or {}).items():
        if k == "intent":
            set_mode(session_id, v)
        else:
            update_field(session_id, k, v)
            
    fields = get_fields(session_id)
    loc = fields.get("location")
    loc_name = None
    if loc and loc.get("city") and loc.get("locality"):
        loc_name = f"{loc['locality']}, {loc['city']}"
        geo = geocode_location(loc_name)
        if geo:
            update_field(session_id, "loc_name", geo["loc_name"])
            update_field(session_id, "loc_lat", geo["loc_lat"])
            update_field(session_id, "loc_lon", geo["loc_lon"])

    cur_mode = get_mode(session_id)
    fields = get_fields(session_id)
    print(f"Mode: {cur_mode}, Fields: {fields}")

    bot_reply = extracted.get("bot_reply")
    if cur_mode == "search":
        handle_search(session_id,bot_reply)
    elif cur_mode == "post":
        #emit("bot_response", {"message": "Posting not done yet"}, room=session_id)
        handle_post(session_id,bot_reply)
    else:
        emit("bot_response", {"message": bot_reply, "properties": None}, room=session_id)
@app.route("/")
def home():
    return "Backend running"

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)
