from fastapi import FastAPI
from chatbot import get_response
import json
import os
from datetime import datetime

app = FastAPI()

LOG_FILE = "./logs/chat_logs.json"
os.makedirs("./logs", exist_ok=True)

def log_interaction(question: str, response: str):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "response": response
    }
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@app.get("/")
def root():
    return {"message": "T2B ON"}

@app.post("/chat")
def chat(question: str):
    response = get_response(question)
    log_interaction(question, response)
    return {"response": response}