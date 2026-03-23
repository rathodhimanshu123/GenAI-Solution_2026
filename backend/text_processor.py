"""
Text processor for VedaVerse — handles PDF and plain text ingestion
"""
import os
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

try:
    from pypdf import PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    from langchain.schema import Document
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

CATEGORY_KEYWORDS = {
    "Ayurveda": ["ayurveda", "dosha", "vata", "pitta", "kapha", "charaka", "sushruta", "herb", "panchakarma"],
    "Yoga": ["yoga", "asana", "pranayama", "patanjali", "meditation", "dhyana", "sutra"],
    "Philosophy": ["vedanta", "upanishad", "brahman", "atman", "samkhya", "arthashastra", "kautilya"],
    "Sanskrit": ["sanskrit", "grammar", "panini", "ashtadhyayi", "vyakarana", "sutra"],
    "Arts": ["music", "dance", "raga", "tala", "natya", "bharatanatyam", "navarasa"],
    "Mathematics": ["mathematics", "aryabhata", "brahmagupta", "zero", "algebra", "geometry"],
}


def detect_category(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return category
    return "General"


def process_pdf(file_path: str, source_name: str) -> List:
    """Extract and chunk text from a PDF file."""
    if not PYPDF_AVAILABLE:
        raise RuntimeError("pypdf not installed")
    if not LANGCHAIN_AVAILABLE:
        raise RuntimeError("langchain not installed")

    reader = PdfReader(file_path)
    documents = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and len(text.strip()) > 50:
            category = detect_category(text)
            documents.append(Document(
                page_content=text,
                metadata={
                    "source": source_name,
                    "category": category,
                    "language": "Sanskrit/English",
                    "page": page_num,
                    "file_path": file_path,
                }
            ))

    if not documents:
        raise ValueError("No readable text found in PDF")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"Processed '{source_name}': {len(reader.pages)} pages → {len(chunks)} chunks")
    return chunks


def process_text(text: str, source_name: str, category: str = "General") -> List:
    """Process plain text content."""
    if not LANGCHAIN_AVAILABLE:
        raise RuntimeError("langchain not installed")

    doc = Document(
        page_content=text,
        metadata={"source": source_name, "category": category, "language": "English"},
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    return splitter.split_documents([doc])
