from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_response
from build_knowledge_base import build_if_needed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    build_if_needed()


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
def root():
    return {"status": "T2B ON"}


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = get_response(request.message)
    return ChatResponse(response=response, session_id=request.session_id)