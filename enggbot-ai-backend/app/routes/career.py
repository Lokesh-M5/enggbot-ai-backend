from fastapi import APIRouter

from pydantic import BaseModel

from app.services.career_analyzer import (
    analyze_career
)

router = APIRouter()


class CareerRequest(BaseModel):

    resume_text: str


@router.post("/analyze")

def analyze(data: CareerRequest):

    return analyze_career(
        data.resume_text
    )