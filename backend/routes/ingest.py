"""
POST /api/ingest — Upload and index documents (PDF or text)
"""
import os
import uuid
import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import aiofiles
from models import IngestResponse
from text_processor import process_pdf, process_text, UPLOAD_DIR
from rag_pipeline import rag_pipeline

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    source_name: str = Form(...),
    category: str = Form(default="General"),
):
    """Upload a PDF or text file and add it to the knowledge base."""
    if not rag_pipeline._initialized:
        raise HTTPException(
            status_code=503,
            detail="RAG pipeline not initialized. Please set GEMINI_API_KEY and restart the server."
        )

    # Validate file type
    filename = file.filename or "upload"
    ext = Path(filename).suffix.lower()
    if ext not in [".pdf", ".txt", ".md"]:
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and MD files are supported")

    # Save uploaded file
    save_path = UPLOAD_DIR / f"{uuid.uuid4()}_{filename}"
    try:
        async with aiofiles.open(save_path, "wb") as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Process and ingest
    try:
        if ext == ".pdf":
            chunks = process_pdf(str(save_path), source_name)
        else:
            text_content = content.decode("utf-8", errors="replace")
            chunks = process_text(text_content, source_name, category)

        chunks_added = rag_pipeline.add_documents(chunks)
        return IngestResponse(
            success=True,
            message=f"Successfully ingested '{source_name}' — {chunks_added} chunks added to knowledge base",
            chunks_added=chunks_added,
            filename=filename,
        )
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
