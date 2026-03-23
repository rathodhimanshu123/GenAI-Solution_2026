"""
GET /api/texts — Browse the IKS text corpus
"""
from typing import Optional
from fastapi import APIRouter, Query
from models import TextEntry

router = APIRouter()

TEXTS = [
    TextEntry(id="charaka", title="Charaka Samhita", original_title="चरक संहिता",
              category="Ayurveda", language="Sanskrit", era="~300 BCE",
              description="The primary ancient text of Ayurvedic medicine by Charaka. Covers physiology, etiology, diagnosis, and treatment using herbs and lifestyle.",
              tags=["ayurveda", "medicine", "doshas", "herbs", "diet"]),
    TextEntry(id="sushruta", title="Sushruta Samhita", original_title="सुश्रुत संहिता",
              category="Ayurveda", language="Sanskrit", era="~600 BCE",
              description="Foundational text on Ayurvedic surgery. Describes surgical instruments, procedures including rhinoplasty, and anatomy in remarkable detail.",
              tags=["ayurveda", "surgery", "anatomy", "instruments"]),
    TextEntry(id="yoga_sutras", title="Yoga Sutras of Patanjali", original_title="पतञ्जलि योगसूत्र",
              category="Yoga", language="Sanskrit", era="~400 CE",
              description="196 aphorisms defining the philosophy and practice of yoga. Introduces the eight-limbed path (Ashtanga) to self-realization.",
              tags=["yoga", "meditation", "philosophy", "ashtanga", "samadhi"]),
    TextEntry(id="arthashastra", title="Arthashastra", original_title="अर्थशास्त्र",
              category="Philosophy", language="Sanskrit", era="~300 BCE",
              description="Kautilya's treatise on statecraft, economic policy, military strategy, and governance. A masterpiece of political science.",
              tags=["politics", "economics", "governance", "kautilya", "chanakya"]),
    TextEntry(id="ashtadhyayi", title="Ashtadhyayi", original_title="अष्टाध्यायी",
              category="Sanskrit", language="Sanskrit", era="~400 BCE",
              description="Panini's grammar of Sanskrit in 3,959 sutras. The most complete and precise grammar ever composed for any language.",
              tags=["grammar", "linguistics", "panini", "vyakarana"]),
    TextEntry(id="natya_shastra", title="Natya Shastra", original_title="नाट्यशास्त्र",
              category="Arts", language="Sanskrit", era="~200 BCE–200 CE",
              description="Bharata Muni's encyclopedic treatise on performing arts. Defines the Navarasa theory and guides classical Indian theatre, dance, and music.",
              tags=["dance", "music", "theatre", "navarasa", "rasa"]),
    TextEntry(id="aryabhatiya", title="Aryabhatiya", original_title="आर्यभटीय",
              category="Mathematics", language="Sanskrit", era="499 CE",
              description="Aryabhata's seminal work on mathematics and astronomy. Introduced the concept of zero, approximated pi, and described a heliocentric model.",
              tags=["mathematics", "astronomy", "zero", "pi", "aryabhata"]),
    TextEntry(id="upanishads", title="Principal Upanishads", original_title="उपनिषद्",
              category="Philosophy", language="Sanskrit", era="~800–200 BCE",
              description="108 philosophical texts forming the theoretical basis of Hinduism. Explore the nature of Brahman (ultimate reality) and Atman (individual soul).",
              tags=["vedanta", "philosophy", "brahman", "atman", "consciousness"]),
    TextEntry(id="hatha_pradipika", title="Hatha Yoga Pradipika", original_title="हठयोगप्रदीपिका",
              category="Yoga", language="Sanskrit", era="15th century CE",
              description="A classic manual of Hatha Yoga, describing asanas, pranayama, mudras, and bandhas for physical and spiritual development.",
              tags=["yoga", "asana", "pranayama", "mudra", "hatha"]),
    TextEntry(id="sangita_ratnakara", title="Sangita Ratnakara", original_title="संगीतरत्नाकर",
              category="Arts", language="Sanskrit", era="13th century CE",
              description="Sharngadeva's treatise on Indian classical music. Defines the system of ragas, talas, and gitas used in both Carnatic and Hindustani traditions.",
              tags=["music", "raga", "tala", "carnatic", "hindustani"]),
]


@router.get("/texts")
async def list_texts(
    category: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    limit: int = Query(default=20, le=100),
):
    """Browse and search the IKS text corpus."""
    results = TEXTS
    if category:
        results = [t for t in results if t.category.lower() == category.lower()]
    if search:
        s = search.lower()
        results = [
            t for t in results
            if s in t.title.lower() or s in t.description.lower()
            or any(s in tag for tag in t.tags)
        ]
    return {
        "total": len(results),
        "texts": [t.model_dump() for t in results[:limit]],
        "categories": list({t.category for t in TEXTS}),
    }
