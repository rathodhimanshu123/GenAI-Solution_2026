import { useState, useRef, useEffect } from 'react';
import { useLanguage, LANGUAGES } from '../LanguageContext';
import { askQuestion } from '../api';
import { Send, Bot, User, BookOpen, Globe, Loader2, AlertCircle } from 'lucide-react';
import './Ask.css';

const SUGGESTED = [
  "What are the three doshas in Ayurveda?",
  "Explain the eight limbs of yoga (Ashtanga)",
  "Who was Kautilya and what is the Arthashastra?",
  "What is Panini's contribution to Sanskrit grammar?",
  "Tell me about the Navarasa theory in Indian arts",
  "What is the Pancha Mahabhuta concept?",
];

function MessageBubble({ msg }) {
  const isUser = msg.role === 'user';
  return (
    <div className={`message ${isUser ? 'message-user' : 'message-bot'}`}>
      <div className="msg-avatar">
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>
      <div className="msg-content">
        <div className="msg-text">{msg.content}</div>
        {msg.sources && msg.sources.length > 0 && (
          <div className="msg-sources">
            <div className="sources-label"><BookOpen size={11} /> Sources</div>
            {msg.sources.map((s, i) => (
              <div key={i} className="source-chip">
                <span className="badge badge-gold">{s.category}</span>
                <strong>{s.title}</strong>
                {s.page && <span className="source-page">p.{s.page}</span>}
              </div>
            ))}
          </div>
        )}
        {msg.translated && (
          <div className="translated-note">
            <Globe size={10} /> Auto-translated
          </div>
        )}
      </div>
    </div>
  );
}

export default function Ask() {
  const { language, setLanguage } = useLanguage();
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: "Namaste! 🙏 I am VedaVerse — your guide to India's ancient knowledge systems. Ask me anything about Ayurveda, Yoga, Sanskrit, Philosophy, or the Arts. You can ask in any Indian language!",
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (query = input) => {
    if (!query.trim() || loading) return;
    setError(null);
    const userMsg = { role: 'user', content: query };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await askQuestion(query, language, sessionId);
      if (!sessionId) setSessionId(res.session_id);
      setMessages(prev => [...prev, {
        role: 'bot',
        content: res.answer,
        sources: res.sources,
        translated: res.translated,
      }]);
    } catch (e) {
      setError('Could not reach the backend. Make sure the API server is running on port 8000.');
      setMessages(prev => [...prev, {
        role: 'bot',
        content: '⚠️ I could not connect to the backend. Please ensure the FastAPI server is running.',
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  const currentLang = LANGUAGES.find(l => l.code === language);

  return (
    <div className="ask-page page-wrapper">
      <div className="ask-layout container">
        {/* Sidebar */}
        <aside className="ask-sidebar">
          <div className="card">
            <h3>🌐 Response Language</h3>
            <select
              className="input"
              value={language}
              onChange={e => setLanguage(e.target.value)}
            >
              {LANGUAGES.map(l => (
                <option key={l.code} value={l.code}>{l.flag} {l.native} ({l.name})</option>
              ))}
            </select>
          </div>

          <div className="card">
            <h3>💡 Try asking...</h3>
            <div className="suggestions">
              {SUGGESTED.map(s => (
                <button key={s} className="suggestion-btn" onClick={() => handleSend(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div className="card sidebar-info">
            <div className="badge badge-teal">ℹ️ About RAG</div>
            <p>VedaVerse uses Retrieval-Augmented Generation to find relevant passages in ancient texts before generating your answer.</p>
          </div>
        </aside>

        {/* Chat */}
        <div className="chat-panel">
          <div className="chat-header">
            <Bot size={20} />
            <span>VedaVerse AI</span>
            <span className="badge badge-gold">Powered by Gemini</span>
            <span className="chat-lang-indicator">
              <Globe size={12} /> {currentLang?.native}
            </span>
          </div>

          {error && (
            <div className="error-bar">
              <AlertCircle size={14} /> {error}
            </div>
          )}

          <div className="chat-messages">
            {messages.map((msg, i) => <MessageBubble key={i} msg={msg} />)}
            {loading && (
              <div className="message message-bot">
                <div className="msg-avatar"><Bot size={16} /></div>
                <div className="msg-content">
                  <div className="typing-indicator">
                    <span /><span /><span />
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="chat-input-area">
            <textarea
              className="input chat-textarea"
              rows={3}
              placeholder="Ask about Ayurveda, Yoga, Sanskrit, Philosophy..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKey}
            />
            <button
              className="btn btn-primary send-btn"
              onClick={() => handleSend()}
              disabled={!input.trim() || loading}
            >
              {loading ? <Loader2 size={16} className="spin" /> : <Send size={16} />}
              {loading ? 'Thinking...' : 'Ask'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
