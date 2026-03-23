"""
POST /api/ask — RAG-powered Q&A with multilingual support
"""
import uuid
from fastapi import APIRouter, HTTPException
from models import AskRequest, AskResponse, Source
from rag_pipeline import rag_pipeline
from translation import translation_service

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
async def ask_vedaverse(request: AskRequest):
    """Ask a question about Indian Knowledge Systems."""
    session_id = request.session_id or str(uuid.uuid4())
    language = request.language.value

    # Translate query to English for retrieval
    english_query = translation_service.translate_to_english(request.query, language)

    # Run RAG
    try:
        answer_en, sources_raw = rag_pipeline.query(english_query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")

    # Translate answer back to user's language
    translated = (language != "en")
    final_answer = translation_service.translate_from_english(answer_en, language) if translated else answer_en

    sources = [
        Source(
            title=s["title"],
            category=s["category"],
            excerpt=s["excerpt"],
            page=s.get("page"),
        )
        for s in sources_raw
    ]

    return AskResponse(
        answer=final_answer,
        sources=sources,
        language=language,
        translated=translated,
        session_id=session_id,
    )
