from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: int
    text: str