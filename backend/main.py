# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# CORS (for Streamlit frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    async with httpx.AsyncClient() as client:
        try:
            ollama_resp = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3",  # or mistral, phi, etc.
                    "messages": [
                        {"role": "user", "content": req.message}
                    ]
                }
            )
            result = ollama_resp.json()
            return ChatResponse(response=result["message"]["content"])
        except Exception as e:
            return ChatResponse(response=f"[Error]: {str(e)}")
