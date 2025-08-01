import os
from langchain_ollama import OllamaLLM
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate

from models.vectorstore import get_embedding
from utils.mongo_index import get_context_notes


MODEL_NAME = os.getenv("MODEL_NAME")
retrieval_model = None

retrieval_qa_chat_prompt = PromptTemplate(input_variables=["context", "input"], template="""
1. Use the following pieces of context to answer the question at the end.
2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.\n
3. Keep the answer crisp and limited to 3,4 sentences, do not show your reasoning steps.

Context: {context}

Question: {input}

Helpful Answer:""")


# Helper Function to get document model
def get_document_model():
    llm = OllamaLLM(model=MODEL_NAME, temperature=0, verbose=False)

    document_model = create_stuff_documents_chain(
        llm, retrieval_qa_chat_prompt)

    return document_model


async def query_model(query):
    global retrieval_model
    if retrieval_model == None:
        retrieval_model = get_document_model()

    embedded_query = get_embedding(query)
    context = await get_context_notes(embedded_query)

    return retrieval_model.invoke({"input": query, "context": context})
