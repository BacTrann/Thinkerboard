from pymongo import errors

from schemas.Note import Note
from config.db import connect_db_client
from RAG_llm.embeddings_model import get_embedding


async def embed_and_save_note(note: Note):
    note_db = await connect_db_client()
    insert_note = {
        "title": note["title"],
        "content": note["content"],
        "createdAt": note["createdAt"],
        "updatedAt": note["updatedAt"],
        "embedding": get_embedding(note["content"])
    }

    try:
        result = await note_db.insert_one(insert_note)
        return str(result.inserted_id)
    except errors.PyMongoError as e:
        print(f"Error inserting note: {e}")
        return None
