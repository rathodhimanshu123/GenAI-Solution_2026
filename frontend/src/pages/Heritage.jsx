import { useState } from 'react';
import { submitHeritage, ingestDocument } from '../api';
import { Upload, CheckCircle, AlertCircle, Loader2, User, FileText, MapPin, ChevronRight } from 'lucide-react';
import './Heritage.css';

const CATEGORIES = ['Ayurveda & Herbs', 'Yoga & Meditation', 'Folk Medicine', 'Traditional Arts', 'Indigenous Language', 'Agricultural Wisdom', 'Architecture', 'Other'];
const LANGUAGES_LIST = ['Sanskrit', 'Hindi', 'Tamil', 'Bengali', 'Telugu', 'Kannada', 'Marathi', 'Gujarati', 'Odia', 'Malayalam', 'Assamese', 'Other'];
const REGIONS = ['North India', 'South India', 'East India', 'West India', 'Northeast India', 'Central India'];

const STEPS = ['Your Info', 'Knowledge Details', 'Text & Submit'];

export default function Heritage() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    contributor_name: '', contributor_email: '',
    title: '', category: '', language: '', region: '',
    description: '', knowledge_text: '',
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const update = (field, value) => setForm(prev => ({ ...prev, [field]: value }));

  const handleSubmit = async () => {
    setLoading(true); setError(null);
    try {
      const res = await submitHeritage(form);
      setResult(res);

      // Also ingest into RAG if the form has enough text
      if (form.knowledge_text.length > 100) {
        try {
          const blob = new Blob([form.knowledge_text], { type: 'text/plain' });
          const fd = new FormData();
          fd.append('file', blob, `${form.title}.txt`);
          fd.append('source_name', form.title);
          fd.append('category', form.category);
          await ingestDocument(fd);
        } catch (_) { /* silently skip if RAG not ready */ }
      }
    } catch (e) {
      setError('Submission failed. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileDrop = (e) => {
    e.preventDefault(); setDragOver(false);
    const f = e.dataTransfer?.files[0] || e.target.files?.[0];
    if (f) setFile(f);
  };

  if (result) {
    return (
      <div className="heritage-page page-wrapper">
        <div className="container heritage-success">
          <CheckCircle size={56} className="success-icon" />
          <h2>Submission Received!</h2>
          <p>{result.message}</p>
          <div className="submission-id">Submission ID: <strong>{result.submission_id}</strong></div>
          <button className="btn btn-outline" onClick={() => { setResult(null); setForm({ contributor_name:'',contributor_email:'',title:'',category:'',language:'',region:'',description:'',knowledge_text:'' }); setStep(0); }}>
            Submit Another
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="heritage-page page-wrapper">
      <div className="container">
        <div className="heritage-header">
          <h2>Heritage Submission Portal</h2>
          <p>Help preserve India's living knowledge traditions. Submit regional, folk, or undocumented knowledge for inclusion in the VedaVerse archive.</p>
        </div>

        {/* Steps */}
        <div className="step-track">
          {STEPS.map((s, i) => (
            <div key={s} className={`step-item ${i <= step ? 'done' : ''} ${i === step ? 'active' : ''}`}>
              <span className="step-num">{i + 1}</span>
              <span className="step-label">{s}</span>
              {i < STEPS.length - 1 && <ChevronRight size={14} className="step-arrow" />}
            </div>
          ))}
        </div>

        <div className="heritage-form card">
          {/* Step 0 */}
          {step === 0 && (
            <div className="form-step">
              <h3><User size={18} /> Contributor Information</h3>
              <div className="form-row">
                <div className="form-group">
                  <label>Full Name *</label>
                  <input className="input" placeholder="Your name" value={form.contributor_name}
                    onChange={e => update('contributor_name', e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Email Address *</label>
                  <input className="input" type="email" placeholder="your@email.com" value={form.contributor_email}
                    onChange={e => update('contributor_email', e.target.value)} />
                </div>
              </div>
              <p className="form-note">Your details will not be shared publicly. We may contact you to verify or expand the submission.</p>
              <button className="btn btn-primary" disabled={!form.contributor_name || !form.contributor_email}
                onClick={() => setStep(1)}>Continue <ChevronRight size={14} /></button>
            </div>
          )}

          {/* Step 1 */}
          {step === 1 && (
            <div className="form-step">
              <h3><FileText size={18} /> Knowledge Details</h3>
              <div className="form-group">
                <label>Title *</label>
                <input className="input" placeholder="e.g. Traditional Marma Therapy of Kerala" value={form.title}
                  onChange={e => update('title', e.target.value)} />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Category *</label>
                  <select className="input" value={form.category} onChange={e => update('category', e.target.value)}>
                    <option value="">Select category</option>
                    {CATEGORIES.map(c => <option key={c}>{c}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Language *</label>
                  <select className="input" value={form.language} onChange={e => update('language', e.target.value)}>
                    <option value="">Select language</option>
                    {LANGUAGES_LIST.map(l => <option key={l}>{l}</option>)}
                  </select>
                </div>
                <div className="form-group">
                  <label>Region <MapPin size={12} /></label>
                  <select className="input" value={form.region} onChange={e => update('region', e.target.value)}>
                    <option value="">Select region</option>
                    {REGIONS.map(r => <option key={r}>{r}</option>)}
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label>Brief Description * <small>(min. 50 chars)</small></label>
                <textarea className="input" rows={3} placeholder="Describe this knowledge tradition — its origin, significance, and current state."
                  value={form.description} onChange={e => update('description', e.target.value)} />
              </div>
              <div className="step-actions">
                <button className="btn btn-ghost" onClick={() => setStep(0)}>Back</button>
                <button className="btn btn-primary"
                  disabled={!form.title || !form.category || !form.language || form.description.length < 50}
                  onClick={() => setStep(2)}>Continue <ChevronRight size={14} /></button>
              </div>
            </div>
          )}

          {/* Step 2 */}
          {step === 2 && (
            <div className="form-step">
              <h3><Upload size={18} /> Knowledge Text & Documents</h3>

              <div className="form-group">
                <label>Detailed Knowledge Text * <small>(min. 100 chars — this will be indexed in VedaVerse)</small></label>
                <textarea className="input" rows={8}
                  placeholder="Share the detailed knowledge, practices, recipes, techniques, mantras, or stories. Be as specific as possible — this is what future researchers will read."
                  value={form.knowledge_text} onChange={e => update('knowledge_text', e.target.value)} />
                <small className="char-count">{form.knowledge_text.length} characters</small>
              </div>

              <div className="form-group">
                <label>Upload Supporting Document (PDF/TXT — optional)</label>
                <div
                  className={`dropzone ${dragOver ? 'dragover' : ''} ${file ? 'has-file' : ''}`}
                  onDragOver={e => { e.preventDefault(); setDragOver(true); }}
                  onDragLeave={() => setDragOver(false)}
                  onDrop={handleFileDrop}
                  onClick={() => document.getElementById('file-input').click()}
                >
                  <input id="file-input" type="file" accept=".pdf,.txt,.md" style={{ display: 'none' }} onChange={handleFileDrop} />
                  {file ? (
                    <div className="file-chosen"><CheckCircle size={20} /><span>{file.name}</span></div>
                  ) : (
                    <>
                      <Upload size={24} />
                      <span>Drag & drop PDF or TXT, or click to browse</span>
                      <small>Max 10MB</small>
                    </>
                  )}
                </div>
              </div>

              {error && <div className="error-msg"><AlertCircle size={14} /> {error}</div>}

              <div className="step-actions">
                <button className="btn btn-ghost" onClick={() => setStep(1)}>Back</button>
                <button className="btn btn-primary"
                  disabled={form.knowledge_text.length < 100 || loading}
                  onClick={handleSubmit}>
                  {loading ? <><Loader2 size={14} className="spin" /> Submitting...</> : '🙏 Submit to Archive'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
