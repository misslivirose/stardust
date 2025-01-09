from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app: FastAPI):
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO Update in Production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)