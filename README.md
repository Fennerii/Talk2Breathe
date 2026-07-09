# Talk2Breathe-AI

A child-centered AI chatbot for smoking prevention education. Built with FastAPI, LangChain, Ollama, and Vue 3.

---

## Prerequisites

Before starting, make sure you have the following installed:

- Python 3.10+
- Node.js 18+
- Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/Fennerii/Talk2Breathe.git
cd Talk2Breathe
```

---

## 2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the required models:

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

---

## 3. Backend Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add your knowledge base documents (PDF, HTML, or DOCX) to the `docs/` folder:

```bash
ls docs/
```

---

## 4. Frontend Setup

```bash
cd client
npm install
cd ..
```

---

## 5. Running the App

You need three terminals.

**Terminal 1 — Ollama:**
```bash
ollama serve
```

**Terminal 2 — Backend:**
```bash
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

On first run, the backend will automatically build the knowledge base from your `docs/` folder. This may take a few minutes.

**Terminal 3 — Frontend:**
```bash
cd client
npm run dev
```

Open your browser at `http://localhost:5173`

---

## 6. Updating the Knowledge Base

If you add or change documents in `docs/`, rebuild the knowledge base:

```bash
source venv/bin/activate
python build_knowledge_base.py
```

Then restart the backend.

## .gitignore

Make sure your `.gitignore` includes:

```
venv/
chroma_db/
client/node_modules/
```
