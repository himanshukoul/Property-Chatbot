session_data = {}

def update_session(session_id, key, value):
    session = session_data.setdefault(session_id, {})
    session[key] = value
    return session

def get_session(session_id):
    return session_data.get(session_id, None)

def reset_session(session_id):
    session_data.pop(session_id, None)
