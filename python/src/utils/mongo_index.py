from pymongo.operations import SearchIndexModel
from config.db import connect_db_client

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

    await note_db.create_search_index(model=note_search_index_model)


async def query_note_index(embedded_query):
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
        result.append(note)

    return result
