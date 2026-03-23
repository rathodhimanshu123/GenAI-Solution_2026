"""
VedaVerse Backend — FastAPI main entry point
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)
logger.info(f"Loaded GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY', 'NOT SET')[:8]}...")

# Import RAG pipeline singleton
from rag_pipeline import rag_pipeline

# Import routers
from routes.ask import router as ask_router
from routes.ingest import router as ingest_router
from routes.graph import router as graph_router
from routes.heritage import router as heritage_router
from routes.texts import router as texts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup."""
    logger.info("VedaVerse backend starting...")
    rag_pipeline.initialize()
    if rag_pipeline._initialized:
        logger.info("RAG pipeline initialized with Gemini")
    else:
        logger.warning("RAG pipeline running in MOCK mode")
    yield
    logger.info("VedaVerse backend shutting down")


app = FastAPI(
    title="VedaVerse API",
    description="AI-powered Living Archive for Indian Knowledge Systems",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — wide open for local development to avoid any browser-specific issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_headers=["*"],
    allow_methods=["*"],
)
# Note: FastAPI/Starlette allows "*" with allow_credentials=True if you omit allow_credentials=True or set it,
# but actually it will raise error if you use allow_origins=["*"] and allow_credentials=True together.
# However, many versions of fastapi-cors-middleware allow it but then the browser rejects it.
# To be super safe, let's use a regex or just a wide list.

# Mount uploads directory for static file access
uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Register API routes
app.include_router(ask_router, prefix="/api", tags=["Q&A"])
app.include_router(ingest_router, prefix="/api", tags=["Ingestion"])
app.include_router(graph_router, prefix="/api", tags=["Knowledge Graph"])
app.include_router(heritage_router, prefix="/api", tags=["Heritage Portal"])
app.include_router(texts_router, prefix="/api", tags=["Text Library"])


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "VedaVerse API",
        "rag_initialized": rag_pipeline._initialized,
        "gemini_key_set": bool(os.getenv("GEMINI_API_KEY")),
    }


@app.get("/api/languages")
async def get_languages():
    return {
        "languages": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
            {"code": "bn", "name": "Bengali", "native": "বাংলা"},
            {"code": "te", "name": "Telugu", "native": "తెలుగు"},
            {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
            {"code": "mr", "name": "Marathi", "native": "মরাठी"},
            {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    # Important: host '127.0.0.1' is sometimes safer than '0.0.0.0' for localhost CORS
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
