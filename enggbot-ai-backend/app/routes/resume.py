from fastapi import APIRouter

from pydantic import BaseModel

from app.services.resume_analyzer import (
    analyze_resume
)

router = APIRouter()

class ResumeRequest(BaseModel):

    resume_text: str

@router.post("/analyze")

def analyze(request: ResumeRequest):

    result = analyze_resume(
        request.resume_text
    )

    return result