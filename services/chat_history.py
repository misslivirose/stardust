import requests

chat_histories = {}
url = "http://localhost:11434/api/generate" # TODO: Make this work in a single module

def initialize_room(room_id: str):
    if room_id not in chat_histories:
        chat_histories[room_id] = {"history": [], "context": ""}

def append_message(room_id: str, user: str, message: str):
    chat_histories[room_id]["history"].append({"user": user, "message": message, "ai": ""})
    manage_history(room_id, max_messages=50)

def update_ai_response(room_id: str, response: str):
    if chat_histories[room_id]["history"]:
        chat_histories[room_id]["history"][-1]["ai"] += response

def create_summary(text: str):
    prompt = "Create a short summary of the following conversation. Include the names of the users who participated and key topics: ".join(text)

    # Send the query to Ollama without streaming
    params = {"model": "llama3.2", "prompt" : prompt}
    with requests.post(url, json=params, stream=False) as response:
        if response.status_code != 200:
            yield {"error": response.text}
        else:
            return response

def summarize_history(history: list, keep_last_n: int = 5) -> str:
    messages_to_summarize = history[:-keep_last_n]
    if not messages_to_summarize:
        return ""
    text = "\n".join([f"{msg['user']}: {msg['message']}" for msg in messages_to_summarize])

    # Placeholder for summarization (replace with LLM or other methods)
    summary = create_summary(text)
    return summary

def manage_history(room_id: str, max_messages: int = 50, keep_last_n: int = 5):
    history = chat_histories.get(room_id, {}).get("history", [])
    # Check if summarization is needed
    if len(history) > max_messages:
        # Summarize older messages
        summary = summarize_history(history, keep_last_n=keep_last_n)

        # Retain only the last N messages
        recent_messages = history[-keep_last_n:]

        # Update history with the summary and recent messages
        chat_histories[room_id]["history"] = [{"user": "system", "message": summary, "ai": ""}] + recent_messages
        print(f"History summarized for room {room_id}.")
