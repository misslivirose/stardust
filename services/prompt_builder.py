from services.chat_history import chat_histories

def build_prompt(room_id: str, query: str) -> str:
    # Retrieve history for the room
    history = chat_histories.get(room_id, {}).get("history", [])

    # Construct a conversational prompt
    prompt = ""
    for message in history:
        prompt += f"{message['user']}: {message['message']}\n"
        if message["ai"]:
            prompt += f"assistant: {message['ai']}\n"

    # Add the new user query
    prompt += f"user: {query}\nassistant:"
    return prompt
