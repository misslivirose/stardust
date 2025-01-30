from fastapi import APIRouter, HTTPException, Request
import requests

url = "http://localhost:11434/api/generate"

router = APIRouter()

@router.post("/recommendation")
async def generate_recommendations(request: Request):
    try:
        # Extract the input message from the request payload
        payload = await request.json()
        ai_message = payload.get("message")
        print(f"Generating recommendations for:{ai_message}")

        if not ai_message:
            raise HTTPException(status_code=400, detail="Message field is required in the payload.")

        # Construct the prompt
        prompt = (
            f"You are a recommendation engine. Based on the following message, generate three short, concise, "
            f"and insightful questions that could be used as follow-up questions for the user to ask to the AI assistant"
            f"Return only three questions and nothing else. Message: {ai_message}"
        )

        # Set up the parameters for the external API request
        params = {"model": "qwen2.5", "prompt": prompt, "stream":False}

        # Make a POST request to the external API
        response = requests.post(url, json=params)

        # Check the response status and return accordingly
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error from external API: {response.text}")

        # Parse the response and return the result
        result = response.json()
        print(result)
        return {'questions' : [q.strip() for q in result["response"].split("\n") if q.strip()]}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting external API: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
