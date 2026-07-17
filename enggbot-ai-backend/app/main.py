from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import (
    resume,
    chatbot,
    interview,
    market,
    vector,
    pdf,
    ats,
    roadmap,
    skill_gap,
    career,
    jobs,
)

# ==========================================================
# FASTAPI APP
# ==========================================================

app = FastAPI(
    title="EnggBot AI Backend",
    description="AI-powered Career Guidance and Resume Analysis API",
    version="1.0.0",
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# STARTUP
# ==========================================================

@app.on_event("startup")
async def startup():

    print("=" * 60)
    print("🚀 EnggBot Backend Started Successfully")
    print("=" * 60)

# ==========================================================
# GLOBAL EXCEPTION HANDLER
# ==========================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    print("Unhandled Error:", exc)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        },
    )

# ==========================================================
# ROUTERS
# ==========================================================

app.include_router(chatbot.router)

app.include_router(
    resume.router,
    prefix="/resume",
    tags=["Resume"],
)

app.include_router(
    interview.router,
    prefix="/interview",
    tags=["Interview"],
)

app.include_router(
    market.router,
    prefix="/market",
    tags=["Market"],
)

app.include_router(
    vector.router,
    prefix="/vector",
    tags=["Vector Memory"],
)

app.include_router(
    pdf.router,
    prefix="/pdf",
    tags=["PDF Upload"],
)

app.include_router(
    ats.router,
    prefix="/ats",
    tags=["ATS Analyzer"],
)

app.include_router(
    roadmap.router,
    prefix="/roadmap",
    tags=["Roadmap"],
)

app.include_router(
    skill_gap.router,
    prefix="/skill-gap",
    tags=["Skill Gap"],
)

app.include_router(
    career.router,
    prefix="/career",
    tags=["Career Analyzer"],
)

app.include_router(
    jobs.router,
    prefix="/jobs",
    tags=["Jobs"],
)

# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def home():

    return {
        "success": True,
        "application": "EnggBot AI Backend",
        "version": "1.0.0",
        "status": "Running"
    }

# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }