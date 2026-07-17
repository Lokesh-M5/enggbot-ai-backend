from fastapi import APIRouter

from pydantic import BaseModel

from app.services.market_analyzer import (
    analyze_market
)

router = APIRouter()

class MarketRequest(BaseModel):

    role: str

@router.post("/analyze")

def market_analysis(request: MarketRequest):

    return analyze_market(
        request.role
    )