from pymongo.operations import SearchIndexModel
from langchain_core.documents import Document

from db.db import connect_db_client

EMBEDDING_DIM = 768


async def create_note_index():
    note_db = await connect_db_client()

    note_search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "similarity": "dotProduct",
                    "numDimensions": EMBEDDING_DIM
                }
            ]
        },
        name="note_vector_index",
        type="vectorSearch"
    )

    # create_search_index will skip if index is already created
    await note_db.create_search_index(model=note_search_index_model)


async def get_context_notes(embedded_query):
    note_db = await connect_db_client()
    pipeline = [
        {
            "$vectorSearch": {
                "index": "note_vector_index",
                "queryVector": embedded_query,
                "path": "embedding",
                "exact": True,
                "limit": 5
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": 1,
                "content": 1,
            }
        }
    ]

    result = []
    cursor = await note_db.aggregate(pipeline=pipeline)
    async for note in cursor:
        content = note["title"] + " : " + note["content"]
        result.append(Document(page_content=content))

    return result
