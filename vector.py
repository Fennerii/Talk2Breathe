from langchain_ollama import OllamaEmbeddings  # fixed import
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

DataFrame = pd.read_csv('SG_Warning.txt', sep='\t', header=None, names=["text"])
DataFrame["source"] = 'SG_Warning.txt'  # added source column to the DataFrame
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
Database_location = "./chroma_db"
add_documents = not os.path.exists(Database_location)

if add_documents:
    documents = []
    ids = []  # renamed from 'id' (id is a built-in Python function)
    for i, row in DataFrame.iterrows():
        doc = Document(
            page_content=row['text'],
            metadata={"source": row['source']},
            id=str(i)  # fixed: closed parenthesis was missing
        )
        ids.append(str(i))
        documents.append(doc)

vector_store = Chroma(
    collection_name="SG_Warning",
    embedding_function=embeddings,
    persist_directory=Database_location
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)  # fixed: 'ids' not 'id'

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)