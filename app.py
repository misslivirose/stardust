from fastapi import FastAPI
from utils.cors import configure_cors
from routers import chat, websockets, html, recommendations
from fastapi.staticfiles import StaticFiles
import logging

# Initialize FastAPI Application
app = FastAPI()

# Configure CORS
configure_cors(app)

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include Routers
app.include_router(chat.router, prefix="/chat")
app.include_router(websockets.router)
app.include_router(html.router)
app.include_router(recommendations.router)

# Enable logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
