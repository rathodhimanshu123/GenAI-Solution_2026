import { Github, Globe, BookOpen, Cpu, Database, Layers } from 'lucide-react';
import './About.css';

const STACK = [
  { icon: <Cpu size={20} />, name: 'Google Gemini', desc: 'LLM for generation & translation', color: 'gold' },
  { icon: <Database size={20} />, name: 'ChromaDB', desc: 'Vector database for semantic search', color: 'violet' },
  { icon: <Layers size={20} />, name: 'LangChain', desc: 'RAG orchestration framework', color: 'teal' },
  { icon: <Globe size={20} />, name: 'FastAPI', desc: 'High-performance Python backend', color: 'red' },
  { icon: <BookOpen size={20} />, name: 'React + Vite', desc: 'Modern frontend framework', color: 'teal' },
  { icon: <Globe size={20} />, name: 'D3.js', desc: 'Interactive knowledge graph', color: 'gold' },
];

const DOMAINS_INFO = [
  { emoji: '🌿', name: 'Ayurveda', texts: ['Charaka Samhita', 'Sushruta Samhita', 'Ashtanga Hridayam'] },
  { emoji: '🧘', name: 'Yoga', texts: ['Yoga Sutras of Patanjali', 'Hatha Yoga Pradipika', 'Gherand Samhita'] },
  { emoji: '📜', name: 'Sanskrit', texts: ['Ashtadhyayi (Panini)', 'Nirukta (Yaska)', 'Vakyapadiya'] },
  { emoji: '🔬', name: 'Philosophy', texts: ['Principal Upanishads', 'Arthashastra', 'Samkhya Karika'] },
  { emoji: '🎵', name: 'Arts', texts: ['Natya Shastra', 'Sangita Ratnakara', 'Abhinaya Darpana'] },
  { emoji: '🔢', name: 'Math & Astronomy', texts: ['Aryabhatiya', 'Brahmasphutasiddhanta', 'Sulba Sutras'] },
];

export default function About() {
  return (
    <div className="about-page page-wrapper">
      <div className="container">
        {/* Mission */}
        <section className="about-mission">
          <div className="badge badge-gold">🙏 Our Mission</div>
          <h2>Bridging Ancient Wisdom &<br /><span className="gradient-text">Modern Accessibility</span></h2>
          <p>
            India possesses one of the world's oldest, deepest knowledge systems — Ayurveda, Yoga, Sanskrit,
            Philosophy, Mathematics, and the Arts. Yet much of this wisdom remains locked in ancient manuscripts,
            inaccessible to the billion+ people who could benefit from it.
          </p>
          <p>
            VedaVerse uses cutting-edge AI — specifically Retrieval-Augmented Generation with Google Gemini —
            to make this knowledge conversational, multilingual, and universally accessible. Ask a question in
            Hindi, Tamil, or Bengali and receive contextual, citation-backed answers from authentic ancient texts.
          </p>
        </section>

        {/* Corpus */}
        <section className="about-section">
          <h3>📚 Knowledge Corpus</h3>
          <div className="corpus-grid">
            {DOMAINS_INFO.map(d => (
              <div key={d.name} className="corpus-card card">
                <div className="corpus-emoji">{d.emoji}</div>
                <h4>{d.name}</h4>
                <ul>
                  {d.texts.map(t => <li key={t}>{t}</li>)}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* How it works */}
        <section className="about-section">
          <h3>⚙️ How VedaVerse Works</h3>
          <div className="pipeline-steps">
            {[
              { step: '01', title: 'Query', desc: 'User asks a question in any Indian language' },
              { step: '02', title: 'Translate', desc: 'Gemini translates the query to English for retrieval' },
              { step: '03', title: 'Retrieve', desc: 'ChromaDB finds the most relevant passages from ancient texts' },
              { step: '04', title: 'Generate', desc: 'Gemini generates a contextual answer with source citations' },
              { step: '05', title: 'Translate Back', desc: 'Answer is translated back to the user\'s preferred language' },
            ].map(s => (
              <div key={s.step} className="pipeline-step">
                <span className="step-num-lg">{s.step}</span>
                <div>
                  <strong>{s.title}</strong>
                  <p>{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Tech Stack */}
        <section className="about-section">
          <h3>🛠️ Technology Stack</h3>
          <div className="stack-grid">
            {STACK.map(s => (
              <div key={s.name} className={`stack-card card feature-${s.color}`}>
                <div className="feature-icon">{s.icon}</div>
                <div>
                  <strong>{s.name}</strong>
                  <p>{s.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Team */}
        <section className="about-section about-cta card card-glow">
          <h3>Built by Team VedaVerse</h3>
          <p>
            <em>Veda</em> — ancient knowledge. <em>Verse</em> — modern digital layer. Together,
            VedaVerse represents the union of India's timeless wisdom with 21st-century AI.
          </p>
          <div className="cta-badges">
            <span className="badge badge-gold">🏆 Hackathon Project</span>
            <span className="badge badge-violet">🤖 Gemini Powered</span>
            <span className="badge badge-teal">🇮🇳 Made in India</span>
          </div>
        </section>
      </div>
    </div>
  );
}
