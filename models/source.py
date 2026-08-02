from pydantic import BaseModel

class Source(BaseModel):
    document_name: str
    score: float