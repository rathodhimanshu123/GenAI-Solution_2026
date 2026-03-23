import { useState, useEffect } from 'react';
import { getTexts } from '../api';
import { Search, BookOpen, Filter, Loader2, Tag } from 'lucide-react';
import './Texts.css';

const CATEGORIES = ['All', 'Ayurveda', 'Yoga', 'Philosophy', 'Sanskrit', 'Arts', 'Mathematics'];

export default function Texts() {
  const [texts, setTexts] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    getTexts()
      .then(data => { setTexts(data.texts); setFiltered(data.texts); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    let result = texts;
    if (category !== 'All') result = result.filter(t => t.category === category);
    if (search) result = result.filter(t =>
      t.title.toLowerCase().includes(search.toLowerCase()) ||
      t.description.toLowerCase().includes(search.toLowerCase()) ||
      t.tags.some(tag => tag.includes(search.toLowerCase()))
    );
    setFiltered(result);
  }, [search, category, texts]);

  const BADGE_MAP = {
    Ayurveda: 'badge-gold', Yoga: 'badge-teal', Philosophy: 'badge-violet',
    Sanskrit: 'badge-red', Arts: 'badge-gold', Mathematics: 'badge-teal',
  };

  return (
    <div className="texts-page page-wrapper">
      <div className="container">
        <div className="texts-header">
          <div>
            <h2><BookOpen size={22} style={{display:'inline', marginRight:8}} />Text Library</h2>
            <p>Browse {texts.length} curated ancient Indian knowledge texts</p>
          </div>
        </div>

        {/* Filters */}
        <div className="texts-filters">
          <div className="search-wrap">
            <Search size={16} className="search-icon" />
            <input className="input search-input" placeholder="Search texts, topics, tags..."
              value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <div className="category-tabs">
            <Filter size={14} style={{color:'var(--text-muted)'}} />
            {CATEGORIES.map(c => (
              <button key={c}
                className={`cat-tab ${category === c ? 'active' : ''}`}
                onClick={() => setCategory(c)}>{c}</button>
            ))}
          </div>
        </div>

        {loading && <div className="loading-center"><Loader2 size={32} className="spin" /></div>}

        {/* Grid */}
        <div className="texts-grid">
          {filtered.map(text => (
            <div key={text.id} className={`text-card card ${selected?.id === text.id ? 'expanded' : ''}`}
              onClick={() => setSelected(selected?.id === text.id ? null : text)}>
              <div className="text-card-top">
                <span className={`badge ${BADGE_MAP[text.category] || 'badge-gold'}`}>{text.category}</span>
                <span className="text-era">{text.era}</span>
              </div>
              <h3 className="text-title">{text.title}</h3>
              <p className="text-original">{text.original_title}</p>
              <p className="text-desc">{text.description}</p>
              {selected?.id === text.id && (
                <div className="text-tags">
                  <Tag size={12} />
                  {text.tags.map(tag => (
                    <span key={tag} className="tag-chip">{tag}</span>
                  ))}
                </div>
              )}
              <div className="text-meta">
                <span>{text.language}</span>
              </div>
            </div>
          ))}
        </div>

        {!loading && filtered.length === 0 && (
          <div className="no-results">
            <BookOpen size={40} />
            <p>No texts found. Try a different search or category.</p>
          </div>
        )}
      </div>
    </div>
  );
}
