chat_histories = {}

def initialize_room(room_id: str):
    if room_id not in chat_histories:
        chat_histories[room_id] = []

def append_message(room_id: str, user: str, message: str):
    chat_histories[room_id].append({"user": user, "message": message, "ai": ""})

def update_ai_response(room_id: str, response: str):
    if chat_histories[room_id]:
        chat_histories[room_id][-1]["ai"] += response
