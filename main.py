from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")
template = """
You are Breathe, a friendly health educator talking to children aged 7-13.
Your only job is to help kids understand why smoking is harmful and how to make healthy choices.
Rules you must always follow:
- Use simple, clear language a 7-year-old can understand
- Be encouraging and positive, never scary or preachy
- Never explain how to smoke, buy, or obtain tobacco or nicotine products
- If asked something off-topic, gently redirect back to health and wellness
- Keep responses short — 3 to 5 sentences maximum
If you do not know something, say so honestly and suggest they talk to a trusted adult.
Here are some documents that you can use to help answer questions: {docs}
Here is the conversation {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    question = input("What can I help you with today?\n Type Exit to leave the conversation: ")
    print("\n")

    if question.strip().lower() == "exit":
        print("Goodbye! Remember to make healthy choices and stay active!")
        break

    docs = retriever.invoke(question)  # store retrieved docs

    # debug: confirm it's using your document
    print("--- Retrieved Docs ---")
    for doc in docs:
        print(doc.page_content)
    print("----------------------\n")

    result = chain.invoke({
        "docs": docs,   # pass the actual retrieved docs, not a hardcoded string
        "question": question
    })
    print(result)
    # removed the stray break so the loop continues