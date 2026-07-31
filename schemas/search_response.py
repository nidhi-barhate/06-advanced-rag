from pydantic import BaseModel

from schemas.search_result import SearchResult

class SearchResponse(BaseModel):
    results: list[SearchResult]