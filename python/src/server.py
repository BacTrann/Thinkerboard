import asyncio
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager


from db.db import connect_db_client, disconnect_db_client
from models.vectorstore import get_embedding
from models.model import get_retrieval_model
from utils.mongo_index import create_note_index, get_context_notes
from utils.mongo_embed import update_missing_embeddings, periodic_embedding_scheduler
from schemas.Note import Note
from schemas.AIQuery import AIQuery


# Lifespan event for FastApi app
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_note_index()
    asyncio.create_task(periodic_embedding_scheduler())
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
    res = await get_context_notes(user_query)
    return res


@app.post("/update")
async def update():
    try:
        await update_missing_embeddings()
        return {"message": "Updated successful"}
    except Exception as e:
        raise HTTPException(status_code="400", detail=e)


@app.post("/test")
async def test():
    res = await get_retrieval_model("Hello")
    return {"res": res}
