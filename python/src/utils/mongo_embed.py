import asyncio
from pymongo import errors

from schemas.Note import Note
from db.db import connect_db_client
from models.vectorstore import get_embedding


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
