from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager

from config.db import connect_db_client, disconnect_db_client
from RAG_llm.embeddings_model import get_embedding
from utils.mongo_index import create_note_index, query_note_index
from schemas.Note import Note
from schemas.AIQuery import AIQuery


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_note_index()
    yield
    await disconnect_db_client()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    note_db = await connect_db_client()
    if note_db == None:
        raise HTTPException(
            status_code=500, detail='Failed to connect to database')

    notes = []
    async for note in note_db.find():
        # Pymongo returns BSON which needs to be converted to string
        note['_id'] = str(note['_id'])
        notes.append(note)
    return {"notes": notes}


@app.post("/query")
async def query(request: AIQuery):
    user_query = get_embedding(request.query)
    data = await query_note_index(user_query)
    return {"data": data}
