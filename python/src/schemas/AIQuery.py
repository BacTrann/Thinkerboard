from pydantic import BaseModel, Field


class AIQuery(BaseModel):
    query: str = Field(..., description="Query to the LLM")
