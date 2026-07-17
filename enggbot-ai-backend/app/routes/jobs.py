from fastapi import APIRouter

from pydantic import BaseModel

from app.services.job_service import (
    fetch_jobs
)

router = APIRouter()


class JobSearchRequest(
    BaseModel
):
    role: str
    job_type: str
    location: str


@router.post("/search")
def search_jobs(
    data: JobSearchRequest
):

    jobs = fetch_jobs(
        data.role,
        data.location
    )

    return jobs