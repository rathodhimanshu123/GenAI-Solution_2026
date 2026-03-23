from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from models import AskRequest, AskResponse
from rag_pipeline import rag_pipeline

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
async def ask_vedaverse(request: AskRequest):
    """
    Multilingual Question Answering via RAG.
    """
    language = request.language.value  # e.g., "en", "hi", "bn"

    # Get answer directly from RAG (the prompt handles the multilingual translation)
    try:
        answer, sources_raw = rag_pipeline.query(request.query, target_language=language)
    except Exception as e:
        # Fallback to English mock if everything fails
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")

    # Format sources for response
    sources = []
    for src in sources_raw:
        sources.append({
            "title": src.get("title", "Document"),
            "category": src.get("category", "General"),
            "excerpt": src.get("excerpt", ""),
            "page": src.get("page", 1)
        })

    return AskResponse(
        answer=answer,
        sources=sources,
        language=language
    )
