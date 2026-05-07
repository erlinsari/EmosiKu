import { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Sparkles, Clock, Zap, Brain } from 'lucide-react';
import { Sidebar } from './components/Sidebar';
import { GlassPanel } from './components/GlassPanel';
import { MoodAvatar } from './components/MoodAvatar';
import { CircularProgress } from './components/CircularProgress';

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
    sentiment: 'neutral' as 'positive' | 'neutral' | 'negative',
    description: 'Silakan masukkan teks konsultasi Anda di atas untuk memulai analisis kesehatan emosional Anda.',
    wellness: 0,
    stress: 0,
    clarity: 0,
    energy: 0
  });

  const [consultationLogs, setConsultationLogs] = useState<ConsultationLog[]>([]);

  // Fungsi kirim data ke Streamlit
  const sendToStreamlit = (data: any) => {
    window.parent.postMessage({
      isStreamlitMessage: true,
      type: "streamlit:setComponentValue",
      value: data
    }, "*");
  };

  useEffect(() => {
    // Beritahu Streamlit tinggi frame
    window.parent.postMessage({
      isStreamlitMessage: true,
      type: "streamlit:setFrameHeight",
      height: document.body.scrollHeight
    }, "*");

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
            if (isNew && result.id) {
              return [{
                id: result.id,
                time: 'Baru saja',
                input: result.lastInput,
                status: result.status,
                sentiment: result.sentiment,
                confidence: result.clarity
              }, ...prev];
            }
            return prev;
          });
        }
      }
    };
    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, []);

  const handleAnalyze = () => {
    if (consultationText.trim()) {
      setIsAnalyzing(true);
      sendToStreamlit({
        action: 'analyze',
        text: consultationText
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden">
      {/* Sidebar */}
      <Sidebar name="Pengguna" sessionCount={consultationLogs.length} />

      {/* Main Content */}
      <div className="ml-80 p-8 relative z-10">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <h2 className="text-4xl font-bold text-slate-800 mb-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>
            Analisis Kesehatan Mental AI
          </h2>
          <p className="text-slate-600">Bagikan pikiran Anda dan biarkan AI kami memberikan wawasan</p>
        </motion.div>

        <GlassPanel glow className="mb-8">
          <div className="p-8">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-violet-600" />
              <label className="text-slate-800 font-semibold">Konsultasi</label>
            </div>
            <textarea
              value={consultationText}
              onChange={(e) => setConsultationText(e.target.value)}
              placeholder="Ekspresikan diri Anda secara bebas..."
              className="w-full h-40 bg-white/60 border border-violet-200 rounded-2xl px-6 py-4 text-slate-800 focus:outline-none focus:border-violet-400 resize-none transition-all"
            />
            <motion.button onClick={handleAnalyze} disabled={isAnalyzing} whileHover={{ scale: 1.02 }} className="mt-6 relative group">
              <div className="px-10 py-4 bg-gradient-to-r from-violet-600 via-purple-600 to-cyan-600 rounded-2xl shadow-lg">
                <span className="text-white font-bold flex items-center gap-2">
                  {isAnalyzing ? "Menganalisis..." : "Analisis Kondisi Emosi"}
                </span>
              </div>
            </motion.button>
          </div>
        </GlassPanel>

        {isAnalyzed && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
            <GlassPanel className="p-8">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                <div className="lg:col-span-2 space-y-4">
                  <h3 className="text-3xl font-bold text-slate-800">{analysisResult.status}</h3>
                  <p className="text-slate-600 leading-relaxed">{analysisResult.description}</p>
                </div>
                <div className="flex justify-center">
                  <MoodAvatar sentiment={analysisResult.sentiment} />
                </div>
              </div>
            </GlassPanel>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <GlassPanel className="p-6 text-center">
                <CircularProgress value={analysisResult.wellness} label="Wellness" />
              </GlassPanel>
              <GlassPanel className="p-6 text-center">
                <CircularProgress value={100 - analysisResult.stress} label="Ketenangan" />
              </GlassPanel>
              <GlassPanel className="p-6 text-center">
                <CircularProgress value={analysisResult.clarity} label="Kejelasan" />
              </GlassPanel>
              <GlassPanel className="p-6 text-center">
                <CircularProgress value={analysisResult.energy} label="Energi" />
              </GlassPanel>
            </div>
          </motion.div>
        )}

        <div className="mt-8">
          <h3 className="text-2xl font-bold text-slate-800 mb-6">Sesi Terakhir</h3>
          <div className="space-y-4">
            {consultationLogs.length === 0 ? (
              <div className="text-center py-10 text-slate-400">Belum ada riwayat sesi.</div>
            ) : (
              consultationLogs.map((log) => (
                <GlassPanel key={log.id} className="p-6">
                  <div className="flex justify-between items-center">
                    <div>
                      <h4 className="font-bold text-slate-800">{log.status}</h4>
                      <p className="text-sm text-slate-500 italic">"{log.input}"</p>
                    </div>
                    <div className="text-xl font-bold text-slate-800">{log.confidence}%</div>
                  </div>
                </GlassPanel>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}