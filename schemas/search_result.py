from pydantic import BaseModel

class SearchResult(BaseModel):
    document_name: str
    text: str
    score: float