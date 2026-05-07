import { useState, useEffect } from 'react';

interface ConsultationLog {
  id: string;
  time: string;
  input: string;
  status: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  confidence: number;
}

export default function App() {
  const [consultationText, setConsultationText] = useState('');
  const [isAnalyzed, setIsAnalyzed] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState({
    status: 'Menunggu Analisis',
    sentiment: 'neutral',
    description: 'Silakan masukkan teks konsultasi Anda di atas untuk memulai analisis kesehatan emosional Anda.',
    wellness: 0,
    stress: 0,
    clarity: 0,
    energy: 0
  });

  const [consultationLogs, setConsultationLogs] = useState<ConsultationLog[]>([]);

  // Komunikasi Ringan ke Streamlit
  useEffect(() => {
    const onMessage = (event: any) => {
      const data = event.data;
      if (data.type === "streamlit:render") {
        const result = data.args.result;
        if (result && result.status !== 'Menunggu Analisis') {
          setAnalysisResult(result);
          setIsAnalyzed(true);
          setIsAnalyzing(false);
          setConsultationLogs(prev => {
            const isNew = !prev.some(log => log.id === result.id);
            if (isNew) return [{
              id: result.id,
              time: 'Baru saja',
              input: result.lastInput,
              status: result.status,
              sentiment: result.sentiment,
              confidence: result.clarity
            }, ...prev];
            return prev;
          });
        }
      }
    };
    window.addEventListener("message", onMessage);
    window.parent.postMessage({ isStreamlitMessage: true, type: "streamlit:setFrameHeight", height: document.body.scrollHeight }, "*");
    return () => window.removeEventListener("message", onMessage);
  }, [consultationLogs]);

  const handleAnalyze = () => {
    if (consultationText.trim()) {
      setIsAnalyzing(true);
      window.parent.postMessage({
        isStreamlitMessage: true,
        type: "streamlit:setComponentValue",
        value: { action: 'analyze', text: consultationText }
      }, "*");
    }
  };

  return (
    <div className="app-container">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
        :root { --glass: rgba(255, 255, 255, 0.7); }
        body { margin: 0; font-family: 'Plus Jakarta Sans', sans-serif; background: #f0f4ff; color: #1e293b; }
        .app-container { display: flex; min-height: 100vh; }
        
        /* Sidebar */
        .sidebar { width: 300px; background: white; border-right: 1px solid #e2e8f0; padding: 32px; position: fixed; height: 100vh; }
        .logo { font-size: 24px; font-weight: 800; color: #6366f1; margin-bottom: 40px; display: flex; align-items: center; gap: 10px; }
        .profile-card { background: linear-gradient(135deg, #6366f1, #a855f7); color: white; padding: 20px; rounded-2xl; border-radius: 20px; margin-bottom: 24px; }
        .stats { display: grid; grid-template-cols: 1fr 1fr 1fr; gap: 10px; text-align: center; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); pt: 10px; }
        
        /* Main */
        .main { margin-left: 300px; flex: 1; padding: 40px; }
        .glass-panel { background: var(--glass); backdrop-filter: blur(12px); border: 1px solid white; border-radius: 24px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
        textarea { width: 100%; height: 120px; border-radius: 16px; border: 1px solid #e2e8f0; padding: 15px; font-size: 16px; resize: none; outline: none; transition: 0.3s; }
        textarea:focus { border-color: #6366f1; box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1); }
        .btn { background: linear-gradient(90deg, #6366f1, #a855f7); color: white; border: none; padding: 15px 30px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.3s; margin-top: 20px; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3); }
        
        /* Results */
        .results-grid { display: grid; grid-template-cols: repeat(4, 1fr); gap: 20px; margin-top: 30px; }
        .stat-box { background: white; padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #e2e8f0; }
        .history-card { background: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
      `}</style>

      <div className="sidebar">
        <div className="logo">🧠 EmosiKu</div>
        <div className="profile-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ fontSize: '32px' }}>👤</div>
            <div style={{ fontWeight: 700 }}>Pengguna</div>
          </div>
          <div className="stats" style={{ paddingTop: '10px' }}>
            <div><div>{consultationLogs.length}</div><div style={{fontSize: '10px', opacity: 0.8}}>Sesi</div></div>
            <div><div>85%</div><div style={{fontSize: '10px', opacity: 0.8}}>Mental</div></div>
            <div><div>{Math.floor(consultationLogs.length/2)}</div><div style={{fontSize: '10px', opacity: 0.8}}>Medali</div></div>
          </div>
        </div>
        <h4 style={{ color: '#64748b' }}>Menu</h4>
        <div style={{ color: '#1e293b', fontWeight: 600 }}>🏠 Dashboard</div>
      </div>

      <div className="main">
        <h1 style={{ fontSize: '36px', marginBottom: '8px' }}>Analisis Kesehatan Mental AI</h1>
        <p style={{ color: '#64748b', marginBottom: '32px' }}>Bagikan apa yang Anda rasakan, biarkan AI kami memberikan wawasan.</p>

        <div className="glass-panel">
          <h3 style={{ marginBottom: '16px' }}>✨ Sesi Konsultasi</h3>
          <textarea 
            value={consultationText}
            onChange={(e) => setConsultationText(e.target.value)}
            placeholder="Bagaimana perasaan Anda hari ini? Ceritakan saja semuanya di sini..."
          />
          <button className="btn" onClick={handleAnalyze} disabled={isAnalyzing}>
            {isAnalyzing ? "⌛ Sedang Menganalisis..." : "🚀 Analisis Kondisi Emosi"}
          </button>
        </div>

        {isAnalyzed && (
          <div style={{ marginTop: '40px' }}>
            <div className="glass-panel" style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
              <div style={{ fontSize: '80px' }}>{analysisResult.sentiment === 'positive' ? '😊' : '😔'}</div>
              <div>
                <h2 style={{ margin: 0, color: '#1e293b' }}>{analysisResult.status}</h2>
                <p style={{ color: '#64748b', fontSize: '18px' }}>{analysisResult.description}</p>
              </div>
            </div>
            
            <div className="results-grid">
              <div className="stat-box"><div style={{fontSize: '24px', fontWeight: 700}}>{analysisResult.wellness}%</div><div>Wellness</div></div>
              <div className="stat-box"><div style={{fontSize: '24px', fontWeight: 700}}>{100-analysisResult.stress}%</div><div>Calmness</div></div>
              <div className="stat-box"><div style={{fontSize: '24px', fontWeight: 700}}>{analysisResult.clarity}%</div><div>Clarity</div></div>
              <div className="stat-box"><div style={{fontSize: '24px', fontWeight: 700}}>{analysisResult.energy}%</div><div>Energy</div></div>
            </div>
          </div>
        )}

        <div style={{ marginTop: '50px' }}>
          <h3 style={{ marginBottom: '20px' }}>Sesi Terakhir</h3>
          {consultationLogs.length === 0 ? (
            <p style={{ color: '#94a3b8' }}>Belum ada riwayat sesi.</p>
          ) : (
            consultationLogs.map(log => (
              <div key={log.id} className="history-card">
                <div>
                  <div style={{fontWeight: 700}}>{log.status}</div>
                  <div style={{fontSize: '14px', color: '#64748b'}}>"{log.input.substring(0, 50)}..."</div>
                </div>
                <div style={{fontWeight: 700, color: '#6366f1'}}>{log.confidence}%</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}