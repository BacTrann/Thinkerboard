import os
from langchain_ollama import OllamaLLM
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate

from models.vectorstore import get_embedding
from utils.mongo_index import get_context_notes


MODEL_NAME = os.getenv("MODEL_NAME")

retrieval_qa_chat_prompt = PromptTemplate(input_variables=["context", "input"], template="""
1. Use the following pieces of context to answer the question at the end.
2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.\n
3. Keep the answer crisp and limited to 3,4 sentences, do not show your reasoning steps.

Context: {context}

Question: {input}

Helpful Answer:""")


async def get_retrieval_model(query):
    llm = OllamaLLM(model=MODEL_NAME, temperature=0, verbose=False)
    embedded_query = get_embedding(query)
    context = await get_context_notes(embedded_query)

    combine_docs_chain = create_stuff_documents_chain(
        llm, retrieval_qa_chat_prompt)

    return combine_docs_chain.invoke({"input": query, "context": context})
