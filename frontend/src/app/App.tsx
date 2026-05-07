import { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Sparkles, Brain } from 'lucide-react';
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
    status: '',
    sentiment: 'neutral' as 'positive' | 'neutral' | 'negative',
    description: '',
    wellness: 0,
    stress: 0,
    clarity: 0,
    energy: 0
  });

  const [consultationLogs, setConsultationLogs] = useState<ConsultationLog[]>([]);

  // --- KOMUNIKASI RESMI STREAMLIT ---
  useEffect(() => {
    const Streamlit = (window as any).Streamlit;

    const onRender = (event: any) => {
      const data = event.detail.args.result;
      if (data && data.status) {
        setAnalysisResult(data);
        setIsAnalyzed(true);
        setIsAnalyzing(false);
        setConsultationText(data.originalText || '');
        
        const newLog: ConsultationLog = {
          id: Date.now().toString(),
          time: new Date().toLocaleTimeString('id-ID'),
          input: data.originalText || '',
          status: data.status,
          sentiment: data.sentiment,
          confidence: data.clarity
        };
        setConsultationLogs(prev => [newLog, ...prev]);
      }
      
      if (Streamlit) {
        Streamlit.setFrameHeight();
      }
    };

    window.addEventListener('message', (event) => {
      if (event.data.type === 'streamlit:render') {
        onRender({ detail: { args: event.data.args } });
      }
    });

    if (Streamlit) {
      Streamlit.setComponentReady();
      Streamlit.setFrameHeight();
    }
  }, []);

  const handleAnalyze = () => {
    if (consultationText.trim()) {
      setIsAnalyzing(true);
      const Streamlit = (window as any).Streamlit;
      if (Streamlit) {
        Streamlit.setComponentValue({
          action: 'analyze',
          text: consultationText
        });
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-br from-violet-200/40 to-cyan-200/40 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-pink-200/30 to-purple-200/30 rounded-full blur-3xl" />
      </div>

      <Sidebar />

      <div className="ml-80 p-8 relative z-10">
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <h2 className="text-4xl font-bold text-slate-800 mb-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>
            Analisis Kesehatan Mental AI
          </h2>
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
              className="w-full h-40 bg-white/60 border border-violet-200 rounded-2xl px-6 py-4 text-slate-800 focus:outline-none focus:border-violet-400 focus:ring-2 focus:ring-violet-300/30 resize-none backdrop-blur-sm transition-all"
            />
            
            <motion.button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="mt-6 relative group"
            >
              <div className="relative px-10 py-4 bg-gradient-to-r from-violet-600 to-cyan-600 rounded-2xl shadow-[0_0_40px_rgba(139,92,246,0.6)] text-white font-bold flex items-center gap-2">
                {isAnalyzing ? "Menganalisis..." : <><Sparkles className="w-5 h-5" /> Analisis Kondisi Emosi</>}
              </div>
            </motion.button>
          </div>
        </GlassPanel>

        {isAnalyzed && (
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="space-y-8">
            <GlassPanel>
              <div className="p-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                  <div className="lg:col-span-2 space-y-4">
                    <h3 className="text-3xl font-bold text-slate-800">{analysisResult.status}</h3>
                    <p className="text-slate-600 leading-relaxed">{analysisResult.description}</p>
                    <div className="flex items-center gap-4 mt-6 pt-6 border-t border-slate-200 text-sm text-slate-500">
                      <Brain className="w-4 h-4 text-violet-600" /> Keyakinan AI: {analysisResult.clarity}%
                    </div>
                  </div>
                  <div className="flex justify-center">
                    <MoodAvatar sentiment={analysisResult.sentiment} />
                  </div>
                </div>
              </div>
            </GlassPanel>
            
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <GlassPanel className="p-6 flex justify-center text-center">
                <CircularProgress value={analysisResult.wellness} color="#10b981" label="Kesejahteraan" />
              </GlassPanel>
              <GlassPanel className="p-6 flex justify-center text-center">
                <CircularProgress value={100 - analysisResult.stress} color="#8b5cf6" label="Ketenangan" />
              </GlassPanel>
              <GlassPanel className="p-6 flex justify-center text-center">
                <CircularProgress value={analysisResult.clarity} color="#06b6d4" label="Kejelasan" />
              </GlassPanel>
              <GlassPanel className="p-6 flex justify-center text-center">
                <CircularProgress value={analysisResult.energy} color="#f59e0b" label="Energi" />
              </GlassPanel>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}