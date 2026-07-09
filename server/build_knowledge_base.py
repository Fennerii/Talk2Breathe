from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil

DATABASE_LOCATION = "./chroma_db"
DOCS_FOLDER = "./docs"

embeddings = OllamaEmbeddings(model="mxbai-embed-large")


def build_if_needed():
    """Builds the vector database from docs/ only if it doesn't already exist."""
    if os.path.exists(DATABASE_LOCATION):
        print("Knowledge base already exists")
        return

    print("Building knowledge base from docs")

    documents = []

    for filename in os.listdir(DOCS_FOLDER):
        filepath = os.path.join(DOCS_FOLDER, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
        elif filename.endswith(".html"):
            loader = BSHTMLLoader(filepath)
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(filepath)
        else:
            continue

        loaded = loader.load()
        documents.extend(loaded)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    ids = [str(i) for i in range(len(chunks))]

    vector_store = Chroma(
        collection_name="Talk2Breathe",
        embedding_function=embeddings,
        persist_directory=DATABASE_LOCATION,
    )
    vector_store.add_documents(documents=chunks, ids=ids)

    print(f"✅ Knowledge base built — {len(chunks)} chunks ingested.")


def rebuild():
    """Force a full rebuild even if chroma_db already exists. 
    Call this manually when you update documents in docs/."""
    if os.path.exists(DATABASE_LOCATION):
        shutil.rmtree(DATABASE_LOCATION)
        print("Cleared existing knowledge base.")
    build_if_needed()


if __name__ == "__main__":
    rebuild()