import requests
import os


RAPID_API_KEY = os.getenv(
    "RAPID_API_KEY"
)


def fetch_jobs(
    role,
    location
):

    url = (
        "https://jsearch.p.rapidapi.com/"
        "search"
    )

    query = (
        f"{role} in {location}"
    )

    headers = {
        "X-RapidAPI-Key":
        RAPID_API_KEY,

        "X-RapidAPI-Host":
        "jsearch.p.rapidapi.com"
    }

    response = requests.get(
        url,
        headers=headers,
        params={
            "query": query,
            "page": 1,
            "num_pages": 1
        }
    )

    return response.json()