"""
RAG Pipeline for VedaVerse
Uses LangChain + FAISS + Google Gemini for retrieval-augmented generation
"""
import os
import pickle
import logging
from typing import List, Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import LangChain / Gemini deps
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("LangChain not available — using mock responses")
    # Stub so module-level Document(...) calls don't fail
    class Document:  # type: ignore
        def __init__(self, page_content: str, metadata: dict = None):
            self.page_content = page_content
            self.metadata = metadata or {}

FAISS_PATH = Path(__file__).parent / "data" / "faiss_index"

# ---------------------------------------------------------------------------
# Sample corpus embedded at startup (so app works without uploading PDFs)
# ---------------------------------------------------------------------------
SAMPLE_DOCUMENTS = [
    Document(
        page_content=(
            "The Charaka Samhita is one of the oldest and most important ancient authoritative writings "
            "on Ayurveda. It describes three doshas: Vata, Pitta, and Kapha. Vata governs movement and "
            "the nervous system. Pitta governs metabolism, energy production and digestion. Kapha governs "
            "growth and protection. An imbalance among these three doshas is considered the root cause of "
            "disease. Charaka emphasizes that Ayurveda aims not just to cure disease but to maintain "
            "health of the healthy and cure disease of the sick."
        ),
        metadata={"source": "Charaka Samhita", "category": "Ayurveda", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "Patanjali's Yoga Sutras define yoga as the cessation of mental fluctuations (Yogas chitta "
            "vritti nirodhah). The eight limbs of yoga (Ashtanga) are: Yama (ethical restraints), "
            "Niyama (personal observances), Asana (physical postures), Pranayama (breath control), "
            "Pratyahara (withdrawal of senses), Dharana (concentration), Dhyana (meditation), and "
            "Samadhi (enlightened absorption). The goal of yoga is self-realization (Kaivalya)."
        ),
        metadata={"source": "Yoga Sutras of Patanjali", "category": "Yoga", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "The Arthashastra by Kautilya (Chanakya) is an ancient Indian treatise on statecraft, "
            "economic policy, and military strategy. Written around 3rd century BCE, it covers topics "
            "including taxation, law, diplomacy, war, and the duties of a king. Kautilya describes the "
            "ideal state as one where the king's happiness lies in the happiness of his subjects "
            "(Praja-sukhe sukham rajnah). The text is divided into 15 books covering different aspects "
            "of governance and administration."
        ),
        metadata={"source": "Arthashastra", "category": "Philosophy", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "Panini's Ashtadhyayi is the foundational text of Sanskrit grammar, composed around 4th "
            "century BCE. It consists of 3,959 sutras (rules) organized in 8 chapters. The work is "
            "renowned for its extraordinary brevity and computational completeness. Panini's grammar "
            "describes the morphological structure of Sanskrit in a rule-based system that anticipated "
            "modern computational linguistics by over two millennia. The Ashtadhyayi remains a "
            "masterpiece of human intellectual achievement."
        ),
        metadata={"source": "Ashtadhyayi", "category": "Sanskrit", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "The Sushruta Samhita is a foundational text of Ayurvedic surgery (Shalya Tantra). "
            "Sushruta, often called the father of surgery, describes over 300 surgical procedures and "
            "120 surgical instruments. He pioneered techniques for rhinoplasty (nose reconstruction), "
            "cataract surgery, and various types of fracture management. The Sushruta Samhita also "
            "covers anatomy, pathology, pharmacology and obstetrics. It recognizes 8 branches of "
            "Ayurvedic medicine (Ashtanga)."
        ),
        metadata={"source": "Sushruta Samhita", "category": "Ayurveda", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "The Natya Shastra by Bharata Muni is the ancient Indian treatise on performing arts "
            "including theatre, dance, and music. Written between 200 BCE and 200 CE, it describes "
            "the Navarasa — nine fundamental emotions: Shringara (love/beauty), Hasya (humor), "
            "Karuna (sorrow), Raudra (fury), Vira (heroism), Bhayanaka (terror), Bibhatsa (disgust), "
            "Adbhuta (wonder), and Shanta (peace). The Navarasa theory profoundly influenced Indian "
            "classical dance forms like Bharatanatyam, Kathak, Odissi, and Kuchipudi."
        ),
        metadata={"source": "Natya Shastra", "category": "Arts", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "Pancha Mahabhuta (five great elements) is a fundamental concept in Indian classical "
            "thought. The five elements are Prithvi (earth), Jala (water), Agni (fire), Vayu (air), "
            "and Akasha (space/ether). In Ayurveda, the three doshas are combinations of these "
            "elements: Vata = Vayu + Akasha, Pitta = Agni + Jala, Kapha = Prithvi + Jala. In "
            "philosophy, all matter and consciousness emerge from these five elements. Traditional "
            "Indian architecture, music, and medicine are all guided by this elemental framework."
        ),
        metadata={"source": "Samkhya Karika", "category": "Philosophy", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "Ayurvedic herbs and their medicinal properties: Ashwagandha (Withania somnifera) is "
            "an adaptogen used for stress, fatigue and immune support. Turmeric (Curcuma longa) "
            "contains curcumin and has anti-inflammatory and antioxidant properties. Neem (Azadirachta "
            "indica) is used for skin diseases, diabetes and infections. Brahmi (Bacopa monnieri) "
            "enhances memory and cognitive function. Amla (Phyllanthus emblica) is rich in Vitamin C "
            "and acts as a rejuvenative. Triphala, a combination of Amalaki, Bibhitaki and Haritaki, "
            "is used for digestive health."
        ),
        metadata={"source": "Charaka Samhita", "category": "Ayurveda", "language": "Sanskrit", "page": 3},
    ),
    Document(
        page_content=(
            "Indian classical music is based on the system of Ragas and Talas. A Raga is a melodic "
            "framework comprising specific ascending (Aroha) and descending (Avaroha) patterns of "
            "notes (Swaras). The seven basic notes (Saptak) are: Sa, Re, Ga, Ma, Pa, Dha, Ni. "
            "There are 72 parent scales (Melakarta Ragas) in Carnatic music. Hindustani classical "
            "music has 10 parent scales (Thaats). Ragas are associated with specific times of day, "
            "seasons and emotional states. Raga Bhairav is performed at dawn; Raga Yaman at dusk."
        ),
        metadata={"source": "Sangita Ratnakara", "category": "Arts", "language": "Sanskrit", "page": 1},
    ),
    Document(
        page_content=(
            "Vastu Shastra is the ancient Indian science of architecture and spatial arrangement. "
            "It integrates principles of direction, geometry, and the five elements to create "
            "harmonious living spaces. The eight directions (Ashtadisha) each have a presiding deity "
            "and elemental association. The Brahmasthan (center of a building) must remain open and "
            "unobstructed. Northeast (Ishanya) is sacred for water and prayer spaces. The Southeast "
            "(Agneya) is associated with fire and ideal for kitchens. Vastu principles influence "
            "temple architecture, town planning, and domestic construction throughout India."
        ),
        metadata={"source": "Manasara", "category": "Arts", "language": "Sanskrit", "page": 1},
    ),
]

MOCK_RESPONSES = {
    "default": (
        "Based on the ancient Indian Knowledge Systems corpus, I can share that Indian classical "
        "knowledge encompasses a vast array of subjects including Ayurveda (medicine), Yoga "
        "(mind-body practice), Sanskrit linguistics, philosophy, mathematics, astronomy, and the "
        "performing arts. These traditions, developed over thousands of years, represent a holistic "
        "understanding of human existence and the natural world. Please ask a specific question "
        "about any of these domains for detailed information."
    ),
    "ayurveda": (
        "Ayurveda, the 'Science of Life', is one of the world's oldest holistic healing systems. "
        "According to the Charaka Samhita, health (Swasthya) is the balance of the three doshas "
        "(Vata, Pitta, Kapha), seven dhatus (body tissues), and proper agni (digestive fire). "
        "Treatment involves diet, lifestyle, herbal medicine, panchakarma (detoxification), and "
        "yoga. Key texts include Charaka Samhita, Sushruta Samhita, and Ashtanga Hridayam."
    ),
}


class RAGPipeline:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.vectorstore = None
        self.llm = None
        self.embeddings = None
        self._initialized = False

    def initialize(self):
        """Initialize vector store and LLM. Called on startup."""
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not installed. Running in mock mode.")
            return
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Running in mock mode.")
            return
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=self.api_key,
            )
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=self.api_key,
                temperature=0.3,
            )
            FAISS_PATH.mkdir(parents=True, exist_ok=True)
            index_file = FAISS_PATH / "index.faiss"
            # Load or create FAISS vector store
            if index_file.exists():
                self.vectorstore = FAISS.load_local(
                    str(FAISS_PATH),
                    embeddings=self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                logger.info(f"Loaded existing FAISS index from {FAISS_PATH}")
            else:
                self.vectorstore = FAISS.from_documents(
                    documents=SAMPLE_DOCUMENTS,
                    embedding=self.embeddings,
                )
                self.vectorstore.save_local(str(FAISS_PATH))
                logger.info("Created new FAISS index with sample corpus")
            self._initialized = True
            logger.info("RAG pipeline initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {e}")

    def add_documents(self, docs: List["Document"]) -> int:
        """Add documents to vector store. Returns number of chunks added."""
        if not self._initialized:
            raise RuntimeError("RAG pipeline not initialized (check GEMINI_API_KEY)")
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        self.vectorstore.add_documents(chunks)
        self.vectorstore.save_local(str(FAISS_PATH))
        return len(chunks)

    def query(self, question: str, k: int = 4) -> Tuple[str, List[dict]]:
        """Run RAG query. Returns (answer, sources)."""
        if not self._initialized:
            return self._mock_response(question), []

        try:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
            relevant_docs = retriever.invoke(question)

            context = "\n\n---\n\n".join(
                f"[Source: {d.metadata.get('source', 'Unknown')}]\n{d.page_content}"
                for d in relevant_docs
            )

            prompt = f"""You are VedaVerse, a knowledgeable assistant specializing in Indian Knowledge Systems (IKS).
Answer the question below using ONLY the provided context from ancient Indian texts.
Be informative, respectful, and cite your sources. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Answer:"""

            response = self.llm.invoke(prompt)
            answer = response.content

            sources = []
            for doc in relevant_docs:
                sources.append({
                    "title": doc.metadata.get("source", "Unknown"),
                    "category": doc.metadata.get("category", "General"),
                    "excerpt": doc.page_content[:200] + "...",
                    "page": doc.metadata.get("page"),
                })

            return answer, sources

        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return self._mock_response(question), []

    def _mock_response(self, question: str) -> str:
        q_lower = question.lower()
        if any(w in q_lower for w in ["ayurveda", "dosha", "vata", "pitta", "kapha", "herb"]):
            return MOCK_RESPONSES["ayurveda"]
        return MOCK_RESPONSES["default"]


# Singleton instance
rag_pipeline = RAGPipeline()
