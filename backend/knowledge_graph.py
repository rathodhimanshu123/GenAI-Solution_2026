"""
Knowledge Graph data for VedaVerse
Returns D3-compatible node/edge data for IKS concept visualization
"""
from models import GraphData, GraphNode, GraphEdge


def get_knowledge_graph() -> GraphData:
    nodes = [
        # Root
        GraphNode(id="iks", label="Indian Knowledge\nSystems", category="root", description="The vast body of classical Indian knowledge spanning millennia", size=30),

        # Major domains
        GraphNode(id="ayurveda", label="Ayurveda", category="domain", description="Ancient Indian system of medicine and holistic healing", size=22),
        GraphNode(id="yoga", label="Yoga", category="domain", description="Physical, mental and spiritual practices for well-being", size=22),
        GraphNode(id="sanskrit", label="Sanskrit", category="domain", description="The classical language of Indian knowledge systems", size=22),
        GraphNode(id="philosophy", label="Philosophy", category="domain", description="Darshanas — Indian schools of thought and metaphysics", size=22),
        GraphNode(id="arts", label="Arts & Music", category="domain", description="Classical performing and visual arts traditions", size=20),
        GraphNode(id="math_astro", label="Math &\nAstronomy", category="domain", description="Ancient Indian contributions to mathematics and astronomy", size=20),

        # Ayurveda branches
        GraphNode(id="doshas", label="Three Doshas", category="ayurveda", description="Vata, Pitta and Kapha — the biological humors", size=14),
        GraphNode(id="vata", label="Vata", category="ayurveda", description="Governs movement — Air + Space elements", size=10),
        GraphNode(id="pitta", label="Pitta", category="ayurveda", description="Governs metabolism — Fire + Water elements", size=10),
        GraphNode(id="kapha", label="Kapha", category="ayurveda", description="Governs growth — Earth + Water elements", size=10),
        GraphNode(id="panchakarma", label="Panchakarma", category="ayurveda", description="Five cleansing therapies for detoxification", size=12),
        GraphNode(id="charaka", label="Charaka\nSamhita", category="text", description="Foundational Ayurvedic text on medicine", size=11),
        GraphNode(id="sushruta", label="Sushruta\nSamhita", category="text", description="Foundational text on Ayurvedic surgery", size=11),
        GraphNode(id="herbs", label="Medicinal\nHerbs", category="ayurveda", description="Ashwagandha, Turmeric, Neem, Brahmi, Amla...", size=12),

        # Yoga branches
        GraphNode(id="ashtanga", label="Ashtanga\n(8 Limbs)", category="yoga", description="Eight-fold path of yoga by Patanjali", size=14),
        GraphNode(id="yoga_sutras", label="Yoga Sutras", category="text", description="Patanjali's foundational text on yoga philosophy", size=11),
        GraphNode(id="pranayama", label="Pranayama", category="yoga", description="Breath control practices", size=10),
        GraphNode(id="meditation", label="Meditation\n(Dhyana)", category="yoga", description="Deep contemplative practice", size=10),

        # Philosophy
        GraphNode(id="vedanta", label="Vedanta", category="philosophy", description="Non-dualistic school of Indian philosophy (Advaita)", size=14),
        GraphNode(id="samkhya", label="Samkhya", category="philosophy", description="Enumeration philosophy — Purusha and Prakriti", size=12),
        GraphNode(id="panchamahabhuta", label="Pancha\nMahabhuta", category="philosophy", description="Five great elements: Earth, Water, Fire, Air, Space", size=13),
        GraphNode(id="upanishads", label="Upanishads", category="text", description="Philosophical texts exploring Brahman and Atman", size=12),
        GraphNode(id="arthashastra", label="Arthashastra", category="text", description="Kautilya's treatise on statecraft and economics", size=11),

        # Sanskrit
        GraphNode(id="ashtadhyayi", label="Ashtadhyayi", category="text", description="Panini's grammar — 3959 rules of Sanskrit", size=12),
        GraphNode(id="grammar", label="Sanskrit\nGrammar", category="sanskrit", description="Vyakarana — most precise grammar ever devised", size=12),

        # Arts
        GraphNode(id="natya_shastra", label="Natya Shastra", category="text", description="Bharata Muni's treatise on performing arts", size=12),
        GraphNode(id="navarasa", label="Navarasa", category="arts", description="Nine fundamental rasas (emotions) in Indian arts", size=13),
        GraphNode(id="carnatic", label="Carnatic\nMusic", category="arts", description="South Indian classical music tradition", size=10),
        GraphNode(id="hindustani", label="Hindustani\nMusic", category="arts", description="North Indian classical music tradition", size=10),

        # Math
        GraphNode(id="aryabhata", label="Aryabhatiya", category="text", description="Aryabhata's text — place value, pi, algebra", size=11),
        GraphNode(id="zero", label="Concept\nof Zero", category="math_astro", description="India's gift to the world — Shunya", size=12),
    ]

    edges = [
        # Root → domains
        GraphEdge(source="iks", target="ayurveda", label="encompasses", strength=0.9),
        GraphEdge(source="iks", target="yoga", label="encompasses", strength=0.9),
        GraphEdge(source="iks", target="sanskrit", label="encompasses", strength=0.9),
        GraphEdge(source="iks", target="philosophy", label="encompasses", strength=0.9),
        GraphEdge(source="iks", target="arts", label="encompasses", strength=0.9),
        GraphEdge(source="iks", target="math_astro", label="encompasses", strength=0.9),

        # Ayurveda
        GraphEdge(source="ayurveda", target="doshas", label="core concept", strength=0.9),
        GraphEdge(source="doshas", target="vata", label="includes", strength=0.8),
        GraphEdge(source="doshas", target="pitta", label="includes", strength=0.8),
        GraphEdge(source="doshas", target="kapha", label="includes", strength=0.8),
        GraphEdge(source="ayurveda", target="panchakarma", label="treatment", strength=0.7),
        GraphEdge(source="ayurveda", target="charaka", label="documented in", strength=0.8),
        GraphEdge(source="ayurveda", target="sushruta", label="documented in", strength=0.8),
        GraphEdge(source="ayurveda", target="herbs", label="uses", strength=0.7),

        # Yoga
        GraphEdge(source="yoga", target="ashtanga", label="core framework", strength=0.9),
        GraphEdge(source="yoga", target="yoga_sutras", label="documented in", strength=0.8),
        GraphEdge(source="ashtanga", target="pranayama", label="includes", strength=0.8),
        GraphEdge(source="ashtanga", target="meditation", label="includes", strength=0.8),

        # Philosophy
        GraphEdge(source="philosophy", target="vedanta", label="school", strength=0.8),
        GraphEdge(source="philosophy", target="samkhya", label="school", strength=0.8),
        GraphEdge(source="philosophy", target="panchamahabhuta", label="concept", strength=0.8),
        GraphEdge(source="philosophy", target="upanishads", label="documented in", strength=0.8),
        GraphEdge(source="philosophy", target="arthashastra", label="documented in", strength=0.6),

        # Sanskrit
        GraphEdge(source="sanskrit", target="grammar", label="core", strength=0.9),
        GraphEdge(source="grammar", target="ashtadhyayi", label="documented in", strength=0.9),

        # Arts
        GraphEdge(source="arts", target="natya_shastra", label="documented in", strength=0.8),
        GraphEdge(source="arts", target="navarasa", label="core concept", strength=0.9),
        GraphEdge(source="arts", target="carnatic", label="includes", strength=0.7),
        GraphEdge(source="arts", target="hindustani", label="includes", strength=0.7),

        # Math
        GraphEdge(source="math_astro", target="aryabhata", label="documented in", strength=0.8),
        GraphEdge(source="math_astro", target="zero", label="invented", strength=0.9),

        # Cross-domain
        GraphEdge(source="panchamahabhuta", target="doshas", label="forms basis of", strength=0.8),
        GraphEdge(source="yoga", target="ayurveda", label="complementary", strength=0.6),
        GraphEdge(source="yoga", target="vedanta", label="rooted in", strength=0.6),
        GraphEdge(source="natya_shastra", target="navarasa", label="defines", strength=0.9),
        GraphEdge(source="samkhya", target="ayurveda", label="philosophical basis", strength=0.6),
    ]

    return GraphData(nodes=nodes, edges=edges)
