from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv
import logging

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
mongo_client = None
note_db = None


async def connect_db_client():
    global mongo_client, note_db
    if note_db:
        return note_db
    try:
        # Create a new client and connect to the server
        client = AsyncMongoClient(MONGO_URI)
        await client.admin.command('ping')
        logging.info('Successfully connected to database')

        note_db = client['notes_db']
        return note_db['notes']
    except ConnectionFailure as e:
        logging.error(f"Failed to connect to database {e}")
