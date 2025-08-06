import asyncio
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from contextlib import asynccontextmanager


from db.db import connect_db_client, disconnect_db_client
from models.model import query_model
from utils.mongo_index import create_note_index
from utils.mongo_embed import embed_and_update_note, periodic_embedding_scheduler
from schemas.Note import UpdateNoteQuery
from schemas.AIQuery import AIQuery


# Lifespan event for FastApi app
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_note_index()  # Create required index in MongoDB if not created
    # Periodicially check and update missing embedding
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
    res = await query_model(request.query)
    return {'message': res}


@app.put("/embed/{note_id}")
async def embed(note_id: str):
    try:
        await embed_and_update_note(note_id)
        return {"message": "Updated successful"}
    except Exception as e:
        raise HTTPException(status_code="400", detail=e)


@app.post("/test")
async def test():
    res = await query_model("Hello")
    return {"res": res}
