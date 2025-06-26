session_data = {}

def get_or_create_session(session_id):
    return session_data.setdefault(session_id, {
        "description": "",
        "mode": "common",  # 'common' | 'search' | 'post'
       # "fields_acquired": [],
        "fields": {},
        "user_id": None
    })

def set_user(session_id,user_id):
    session = get_or_create_session(session_id)
    session["user_id"] = user_id
    
def update_field(session_id, key, value):
    session = get_or_create_session(session_id)
    if value is not None:
        session["fields"][key] = value
        #session["fields_acquired"].append(key)

def update_description(session_id, message):
    session = get_or_create_session(session_id)
    session["description"] = f" {message.strip()}"

# def get_fields_acquired(session_id):
#     return get_or_create_session(session_id)["fields_acquired"]
def get_fields(session_id):
    return get_or_create_session(session_id)["fields"]

def get_mode(session_id):
    return get_or_create_session(session_id)["mode"]

def set_mode(session_id, mode):
    session = get_or_create_session(session_id)
    session["mode"] = mode

def reset_session(session_id):
    session_data.pop(session_id, None)