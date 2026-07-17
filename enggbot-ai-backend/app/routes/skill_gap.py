from fastapi import APIRouter
from pydantic import BaseModel

from app.services.skill_gap_engine import (
    analyze_skill_gap
)

router = APIRouter()


class SkillGapRequest(BaseModel):

    skills: list[str]
    target_role: str


@router.post("/analyze")

def analyze(data: SkillGapRequest):

    return analyze_skill_gap(
        data.skills,
        data.target_role
    )