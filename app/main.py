from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import get_response
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Medical Chatbot API is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    return get_response(req.message)