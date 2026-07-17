from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunker import chunk_text
from app.services.vector_store import store_memory
from app.services.skill_extractor import extract_information
from app.services.role_predictor import predict_role
from app.services.skill_gap_engine import analyze_skill_gap
from app.services.roadmap_generator import generate_roadmap
from app.services.resume_review_service import review_resume

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    try:

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # -------------------------
        # Extract Resume Text
        # -------------------------

        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from PDF."
            )

        # -------------------------
        # AI Resume Review
        # -------------------------

        review = review_resume(extracted_text)

        # -------------------------
        # Store Resume Chunks
        # -------------------------

        chunks = chunk_text(extracted_text)

        for chunk in chunks:
            store_memory(chunk)

        # -------------------------
        # Extract Skills
        # -------------------------

        info = extract_information(extracted_text)

        skills = info.get("skills", [])

        # -------------------------
        # Predict Career Role
        # -------------------------

        predicted_role = predict_role(skills)

        # -------------------------
        # Skill Gap
        # -------------------------

        gap_result = analyze_skill_gap(
            skills,
            predicted_role
        )

        # -------------------------
        # Convert to analysis format
        # -------------------------

        analysis = {
            "target_role": predicted_role,
            "missing_skills": gap_result.get(
                "missing_skills",
                []
            )
        }

        roadmap = generate_roadmap(
            analysis
        )

        return {

            "message": "Resume analyzed successfully",

            "resume_text": extracted_text,

            "predicted_role": predicted_role,

            "skills_found": skills,

            "readiness_score": gap_result.get(
                "readiness_score",
                0
            ),

            "missing_skills": gap_result.get(
                "missing_skills",
                []
            ),

            "roadmap": roadmap,

            "chunks_stored": len(chunks),

            "ai_review": review

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)