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

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Decorator to verify JWT token for protected routes // not used currently
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db_users.find_one({'_id': data['user_id']})
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@socketio.on("message")
def handle_message(data):
    token = data.get("token", "")
    session_id = request.sid
    session = get_or_create_session(session_id)
    if not session.get("user_id"):
        if not token:
            emit("bot_response", {"message": "Authentication required"}, room=session_id)
            return
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = payload['user_id']
            set_user(session_id,user_id)
        except:
            emit("bot_response", {"message": "Invalid or expired token"}, room=session_id)
            return
    user_msg = data.get("msg", "")
    
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
        "post_preferences": [],
        "search_preferences": []
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
if __name__ == "__main__":
    socketio.run(app, port=5000, debug=False)
