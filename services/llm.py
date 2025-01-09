import requests
import json

def generate_response(query: str):
    # Send the query to the LLM API and stream the response.
    url = "http://localhost:11434/api/generate"
    params = {"model": "llama3.2", "prompt": query}
    with requests.post(url, json=params, stream=True) as response:
        if response.status_code != 200:
            yield {"error": response.text}
        else:
            for line in response.iter_lines():
                if line:
                    try:
                        # Decode the line as raw text
                        decoded_line = line.decode("utf-8").strip()
                        
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
