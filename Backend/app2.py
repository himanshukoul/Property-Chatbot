import load_env
from flask import Flask, request,jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from config import DevelopmentConfig
from extractors2 import extract_fields_from_query
from session2 import *
from geocode import geocode_location
from search_handler import handle_search
from post_handler import handle_post 
import jwt
import bcrypt
import datetime
from functools import wraps
from db import db_users
from threading import Thread
from mem0_client import upsert_memory, get_memories
import atexit

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def handle_connect(auth):
    session_id = request.sid
    print(f"Socket connected: {session_id}")
    token = auth.get("token", "") if auth else ""
    if not token:
        print("No token provided in socket.auth")
        emit("bot_response", {"message": "Authentication required"}, room=session_id)
        raise ConnectionRefusedError("Authentication required")
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        print(f"Decoded payload: {payload}")
        user_id = payload['user_id']
        session = get_or_create_session(session_id)
        set_user(session_id, user_id)
        update_last_active(session_id)
    except Exception as e:
        print(f"Socket connection error: {str(e)}")
        emit("bot_response", {"message": "Invalid or expired token"}, room=session_id)
    
@socketio.on("message")
def handle_message(data):
    session_id = request.sid
    session = get_or_create_session(session_id)
    update_last_active(session_id)
    if not session.get("user_id"):
        print("No user_id in session, emitting auth required")
        emit("bot_response", {"message": "Authentication required"}, room=session_id)
        return
    user_msg = data.get("msg", "")
    print(f"User said: {user_msg}")
    
    if get_mode(session_id) == "post" and user_msg.lower().strip() in ["yes", "confirm", "go ahead", "looks good", "post it"]:
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
    new_intent = extracted.get("data", {}).get("intent")
    
    if new_intent and mode != "common" and mode != new_intent:
        prev = get_or_create_session(session_id)
        if should_upsert(prev) and not prev.get("mem_sent"):
            upsert_memory(
                user_id=prev["user_id"],
                description=prev["description"],
                intent=prev["mode"],
                metadata=prev["fields"]
            )
            prev["mem_sent"] = True

        user_id = prev.get("user_id")
        reset_session(session_id)
        new_session = get_or_create_session(session_id)
        if user_id:
            set_user(session_id, user_id)
            update_last_active(session_id)


    if(extracted.get("user_message")): update_description(session_id,extracted.get("user_message"))

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

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
    if db_users.find_one({"email": email}):
        return jsonify({"message": "Email already exists"}), 400
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = db_users.insert_one({
        "email": email,
        "password": hashed,
    }).inserted_id
    token = jwt.encode({
        'user_id': str(user_id),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=app.config['JWT_EXPIRATION_DELTA'])

    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token, "email": email}), 200

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = db_users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=app.config['JWT_EXPIRATION_DELTA'])
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token, "email": email})

@app.route("/api/memories", methods=["GET"])
def fetch_memories():
    token = request.headers.get("Authorization", "")
    if not token.startswith("Bearer "):
        return jsonify({"message": "Invalid Authorization header"}), 401
    token = token.replace("Bearer ", "")
    print("Authorization header:", token)
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = payload["user_id"]
        memories = get_memories(user_id, top_k=3)
        return jsonify({"memories": memories}), 200
    except:
        return jsonify({"memories": []}), 401


def background_memory_pusher():
    while True:
        time.sleep(30)
        now = time.time()
        for session_id, session in get_all_sessions().items():
            if now - session["last_active"] > 600:  # 10 mins
                if should_upsert(session) and not session.get("mem_sent"):
                    upsert_memory(
                        user_id=session["user_id"],
                        description=session["description"],
                        intent=session["mode"],
                        metadata=session["fields"]
                    )
                    session["mem_sent"] = True
                    print(f"Idle session saved to Mem0: {session_id}")
                    socketio.emit("memory_popped", room=session_id)
                user_id = session.get("user_id")
                reset_session(session_id)
                new_session = get_or_create_session(session_id)
                if user_id:
                    set_user(session_id, user_id)
                    update_last_active(session_id)


def flush_all_sessions():
    print("Shutting down. Saving sessions...")
    for session_id, session in get_all_sessions().items():
        if should_upsert(session):
            upsert_memory(
                user_id=session["user_id"],
                description=session["description"],
                intent=session["mode"],
                metadata=session["fields"]
            )
            print(f"[MemoryUpsert] user={session['user_id']}, mode={session['mode']}")

atexit.register(flush_all_sessions)                    
if __name__ == "__main__":
    Thread(target=background_memory_pusher, daemon=True).start()
    socketio.run(app, port=5000, debug=False)
