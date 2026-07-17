from fastapi import APIRouter

from pydantic import BaseModel

from app.services.interview_engine import (
    get_questions,
    evaluate_answer
)

router = APIRouter()

class QuestionRequest(BaseModel):

    skill: str

class AnswerRequest(BaseModel):

    answer: str

@router.post("/questions")

def questions(request: QuestionRequest):

    return {
        "questions": get_questions(
            request.skill
        )
    }

@router.post("/evaluate")

def evaluate(request: AnswerRequest):

    return evaluate_answer(
        request.answer
    )