from flask import Flask,request
from config import DevelopmentConfig
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from extractors import extract_action,extract_price,extract_bhk,extract_location
from session import update_session, get_session
import requests
app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

CORS(app)
socketio = SocketIO(app,cors_allowed_origins='*')

def geocode_location(place_name):
    try:
        print(place_name)
        url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json"
        headers = {'User-Agent': 'real-estate-chatbot'}
        response = requests.get(url, headers=headers)
        data = response.json()
        if data:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"]),
                "name": data[0]["name"]
            }
    except Exception as e:
        print("Geocoding error:", e)
    return None

def handle_buy(session_id):
    session = get_session(session_id)
    emit("bot_response",{"message":f'{session.get("action") , {session.get("loc_name",None)}, {session.get("loc_lat",None)}, {session.get("loc_lon",None)},{session.get("price",None)},{session.get("bhk",None)}}' \
        , "properties":None},room = session_id)


def handle_sell():
    pass

@app.route("/")
def index():
    return 'Backend is Running'

@socketio.on("message")
def handle_message(data):
    user_msg = data.get("msg","")
    session_id = request.sid
    print(f"User sent to backend: {user_msg}")
    user_action = extract_action(user_msg)
    user_price = extract_price(user_msg)
    user_bhk = extract_bhk(user_msg)
    user_location = extract_location(user_msg)
    print(user_location)
    loc_lat = loc_lon= loc_name = None
    if(user_location):
        geocoded_location_data = geocode_location(user_location)
        if(geocoded_location_data):
            print(geocoded_location_data)
            loc_lat = geocoded_location_data['lat']
            loc_lon = geocoded_location_data['lon']
            loc_name = geocoded_location_data['name']
    
    if(user_action): update_session(session_id,'action',user_action)
    if(user_price): update_session(session_id,'price',user_price)
    if(user_bhk) : update_session(session_id,'bhk',user_bhk)
    if(loc_name):
        update_session(session_id,'loc_name',loc_name)
        update_session(session_id,'loc_lat',loc_lat) 
        update_session(session_id,'loc_lon',loc_lon)

    session_data = get_session(session_id)
    intent = session_data.get('action',None)
    description = session_data.get('description','') + " " + user_msg
    update_session(session_id,'description',description)
    if (not intent):
        emit("bot_response",{"message":"please clarify you want to buy / sell / rent" , "properties":None},room = session_id)
    elif (intent in ("buy",'rent')):
        handle_buy(session_id)
    elif (intent in ("sell", 'rent_out')):
        handle_sell(session_id)
if __name__ == "__main__":
    socketio.run(app,debug=True,port=5000)