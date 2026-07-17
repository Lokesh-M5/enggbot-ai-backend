from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ats_analyzer import (
    ats_check
)

router = APIRouter()

class ATSRequest(BaseModel):

    resume_text: str


@router.post("/check")

def check_resume(
    request: ATSRequest
):

    return ats_check(
        request.resume_text
    )