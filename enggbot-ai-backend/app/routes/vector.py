from fastapi import APIRouter

from pydantic import BaseModel

from app.services.vector_store import (
    store_memory,
    search_memory
)

router = APIRouter()

class MemoryRequest(BaseModel):

    text: str

class SearchRequest(BaseModel):

    query: str

@router.post("/store")

def store(request: MemoryRequest):

    store_memory(request.text)

    return {
        "message": "Stored successfully"
    }

@router.post("/search")

def search(request: SearchRequest):

    results = search_memory(
        request.query
    )

    return {
        "results": results
    }