from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/market-trends")
def market_trends():
    return {
        "frontend": {
            "demand": "High",
            "placement_probability": 72
        },
        "backend": {
            "demand": "High",
            "placement_probability": 68
        },
        "aiml": {
            "demand": "Medium",
            "placement_probability": 52
        }
    }
