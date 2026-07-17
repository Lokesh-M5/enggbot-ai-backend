from fastapi import APIRouter

from pydantic import BaseModel

from app.services.roadmap_generator import (
    generate_roadmap
)

router = APIRouter()

class RoadmapRequest(BaseModel):

    role: str

@router.post("/generate")

def roadmap(data: RoadmapRequest):

    return generate_roadmap(
        data.role
    )