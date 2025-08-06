import asyncio
from pymongo import errors
from bson.objectid import ObjectId

from db.db import connect_db_client
from models.vectorstore import get_embedding


# TODO: update to embed_and_update_note(str: ID of note)
async def embed_and_update_note(note_id: str):
    # insert_note = {
    #     "title": note["title"],
    #     "content": note["content"],
    #     "createdAt": note["createdAt"],
    #     "updatedAt": note["updatedAt"],
    #     "embedding": get_embedding(note["content"])
    # }

    try:
        _id = ObjectId(note_id)
        note_db = await connect_db_client()
        note = await note_db.find_one({"_id": _id})
        if not note:
            raise ValueError("Note not found")
        embedding = get_embedding(note["content"])
        await note_db.update_one({"_id": note_id}, {"$set": {"embedding": embedding}})

    except Exception as e:
        print(f"Error updating embedding of note: {e}")


async def update_missing_embeddings():
    note_db = await connect_db_client()

    try:
        # Find notes without an embedding field
        cursor = note_db.find({"embedding": {"$exists": False}})

        async for note in cursor:
            note_id = note["_id"]
            content = note.get("content")

            if content:
                try:
                    embedding = get_embedding(content)  # If sync
                    # embedding = await get_embedding(content)  # If async

                    await note_db.update_one(
                        {"_id": note_id},
                        {"$set": {"embedding": embedding}}
                    )
                    print(f"Updated embedding for note {note_id}")
                except Exception as embed_err:
                    print(f"Failed to embed note {note_id}: {embed_err}")

    except errors.PyMongoError as db_err:
        print(f"Database error during update: {db_err}")


# Periodic wrapper
async def periodic_embedding_scheduler(interval_seconds: int = 300):
    await asyncio.sleep(5)  # slight delay on startup
    while True:
        print("🔁 Checking for notes missing embeddings...")
        await update_missing_embeddings()
        print("✅ Finished checking for notes embeddings")
        await asyncio.sleep(interval_seconds)
