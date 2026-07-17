from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.gemini_service import generate_response

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"]
)


class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


@router.post("/chat")
def chat(data: ChatRequest):

    user_id = data.user_id.strip()
    message = data.message.strip()

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="User ID cannot be empty."
        )

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:

        response = generate_response(
            user_id,
            message
        )

        return {
            "success": True,
            "response": response
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chatbot Error: {str(e)}"
        )