memory_store = {}

def remember(session_id, data):
    memory_store[session_id] = data

def recall(session_id):
    return memory_store.get(session_id, {})