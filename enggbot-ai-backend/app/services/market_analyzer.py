from app.services.market_data import (
    MARKET_DATA
)

def analyze_market(role):

    return MARKET_DATA.get(

        role,

        {
            "message":
            "Role data not found."
        }

    )