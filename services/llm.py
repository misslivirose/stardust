import requests
import json
from services.chat_history import chat_histories
from services.rag import augment_prompt, initialize_rag, return_filepath

# Initialize RAG
embeddings, index, all_chunks = initialize_rag()

url = "http://localhost:11434/api/generate"

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
    prompt += f"chat: {query}\nassistant:"
    return prompt


def generate_response(query: str, room_id: str):
    # prompt = build_prompt(room_id, query)
    augmented_prompt = augment_prompt(query, embeddings, index, all_chunks, k=10 )
    # Send the query to the LLM API and stream the response.
    params = {"model": "qwen2.5", "prompt": augmented_prompt}
    with requests.post(url, json=params, stream=True) as response:
        if response.status_code != 200:
            yield {"error": response.text}
        else:
            for line in response.iter_lines():
                if line:
                    try:
                        # Decode the line as raw text
                        decoded_line = line.decode("utf-8").strip()
                        # print(f"API Chunk: {decoded_line}")
                        # Ensure it's properly formatted
                        if decoded_line.startswith("{") and decoded_line.endswith("}"):
                            # Parse as JSON if valid
                            chunk = json.loads(decoded_line)
                            yield chunk
                        else:
                            # Treat as raw text and wrap in JSON
                            yield {"response": decoded_line}
                    except Exception as e:
                        yield {"error": f"Error parsing response: {str(e)}"}

def get_related_doc(query: str):
    return return_filepath(query, embeddings, index, all_chunks )
