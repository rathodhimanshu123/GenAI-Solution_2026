import { Link } from 'react-router-dom';
import { Sparkles, Network, BookOpen, Users, ArrowRight, Zap, Globe, Shield } from 'lucide-react';
import './Home.css';

const STATS = [
  { value: '10,000+', label: 'Ancient Texts' },
  { value: '8', label: 'Indian Languages' },
  { value: '500+', label: 'Knowledge Concepts' },
  { value: '6', label: 'IKS Domains' },
];

const FEATURES = [
  {
    icon: <Sparkles size={24} />, title: 'AI-Powered Q&A',
    desc: 'Ask questions in any Indian language and receive contextual answers drawn from authentic ancient texts using RAG technology.',
    to: '/ask', color: 'gold',
  },
  {
    icon: <Network size={24} />, title: 'Knowledge Graph',
    desc: 'Visually explore connections between concepts across Ayurveda, Yoga, Sanskrit, Philosophy, Arts and Mathematics.',
    to: '/graph', color: 'violet',
  },
  {
    icon: <BookOpen size={24} />, title: 'Text Library',
    desc: 'Browse and search a curated corpus of ancient Indian texts — from Charaka Samhita to Aryabhatiya.',
    to: '/texts', color: 'teal',
  },
  {
    icon: <Users size={24} />, title: 'Heritage Portal',
    desc: "Contribute regional and folk knowledge. Help preserve India's living traditions for future generations.",
    to: '/heritage', color: 'red',
  },
];

const DOMAINS = [
  { emoji: '🌿', name: 'Ayurveda', desc: 'Ancient medicine & healing' },
  { emoji: '🧘', name: 'Yoga', desc: 'Mind, body & spirit' },
  { emoji: '📜', name: 'Sanskrit', desc: "World's most precise language" },
  { emoji: '🔬', name: 'Philosophy', desc: 'Darshanas & metaphysics' },
  { emoji: '🎵', name: 'Arts & Music', desc: 'Classical performing arts' },
  { emoji: '🔢', name: 'Mathematics', desc: 'Aryabhata to zero' },
];

export default function Home() {
  return (
    <div className="home">
      {/* Hero */}
      <section className="hero">
        <div className="hero-glow" />
        <div className="container hero-content">
          <div className="hero-badge">
            <span className="badge badge-gold"><Zap size={10} /> Powered by Gemini AI</span>
          </div>
          <h1 className="hero-title">
            Ancient Wisdom,<br />
            <span className="gradient-text">Conversational Intelligence</span>
          </h1>
          <p className="hero-desc">
            VedaVerse digitizes and makes India's classical knowledge — spanning Ayurveda, Yoga,
            Sanskrit, Philosophy and the Arts — searchable and conversational in your language.
          </p>
          <div className="hero-actions">
            <Link to="/ask" className="btn btn-primary">
              <Sparkles size={16} /> Ask VedaVerse <ArrowRight size={14} />
            </Link>
            <Link to="/graph" className="btn btn-outline">
              <Network size={16} /> Explore Knowledge Graph
            </Link>
          </div>
          <div className="hero-langs">
            {['English', 'हिन्दी', 'தமிழ்', 'বাংলা', 'తెలుగు', 'ಕನ್ನಡ'].map(l => (
              <span key={l} className="lang-pill">{l}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="stats-section">
        <div className="container stats-grid">
          {STATS.map(s => (
            <div key={s.label} className="stat-card">
              <div className="stat-value gradient-text">{s.value}</div>
              <div className="stat-label">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Domains */}
      <section className="domains-section container">
        <div className="section-header">
          <span className="badge badge-gold"><Globe size={10} /> Knowledge Domains</span>
          <h2>Six Pillars of Indian Wisdom</h2>
          <p>Explore knowledge across India's rich intellectual traditions</p>
        </div>
        <div className="domains-grid">
          {DOMAINS.map(d => (
            <Link to="/texts" key={d.name} className="domain-card">
              <span className="domain-emoji">{d.emoji}</span>
              <strong>{d.name}</strong>
              <span>{d.desc}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="features-section container">
        <div className="section-header">
          <span className="badge badge-violet"><Shield size={10} /> Platform Features</span>
          <h2>Everything You Need</h2>
          <p>A complete platform for exploring and contributing to India's knowledge heritage</p>
        </div>
        <div className="features-grid">
          {FEATURES.map(f => (
            <Link to={f.to} key={f.title} className={`feature-card feature-${f.color}`}>
              <div className="feature-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
              <span className="feature-arrow">Explore <ArrowRight size={14} /></span>
            </Link>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="cta-section container">
        <div className="cta-card card card-glow">
          <h2>Ready to explore India's living heritage?</h2>
          <p>Ask your first question in any Indian language and discover the depth of ancient wisdom.</p>
          <Link to="/ask" className="btn btn-primary">
            Start Exploring <ArrowRight size={14} />
          </Link>
        </div>
      </section>
    </div>
  );
}
