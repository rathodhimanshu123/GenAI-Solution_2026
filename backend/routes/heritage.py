"""
POST /api/submit — Heritage submission portal
GET  /api/submissions — List submissions (admin)
"""
import uuid
import json
import logging
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, HTTPException
from models import HeritageSubmission, HeritageResponse

router = APIRouter()
logger = logging.getLogger(__name__)

SUBMISSIONS_FILE = Path(__file__).parent.parent / "data" / "submissions.json"
SUBMISSIONS_FILE.parent.mkdir(exist_ok=True)


def _load_submissions():
    if SUBMISSIONS_FILE.exists():
        with open(SUBMISSIONS_FILE) as f:
            return json.load(f)
    return []


def _save_submissions(submissions):
    with open(SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2, ensure_ascii=False)


@router.post("/submit", response_model=HeritageResponse)
async def submit_heritage(submission: HeritageSubmission):
    """Submit regional heritage knowledge to the archive."""
    try:
        submissions = _load_submissions()
        submission_id = str(uuid.uuid4())[:8].upper()
        record = {
            "id": submission_id,
            "submitted_at": datetime.utcnow().isoformat(),
            "status": "pending_review",
            **submission.model_dump(),
        }
        submissions.append(record)
        _save_submissions(submissions)
        return HeritageResponse(
            success=True,
            message=f"Thank you, {submission.contributor_name}! Your submission '{submission.title}' has been received and is pending review by our heritage experts.",
            submission_id=submission_id,
        )
    except Exception as e:
        logger.error(f"Heritage submission failed: {e}")
        raise HTTPException(status_code=500, detail="Submission failed. Please try again.")


@router.get("/submissions")
async def list_submissions():
    """List all heritage submissions."""
    return {"submissions": _load_submissions()}
