from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from config.db import connect_db_client
from services.embed_and_save_note import embed_and_save_note
from schemas.Note import Note

app = FastAPI()


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


@app.post("/embedd")
async def embedd(note: Note):
    await embed_and_save_note(note)
