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
    status: '',
    sentiment: 'neutral' as 'positive' | 'neutral' | 'negative',
    description: '',
    wellness: 0,
    stress: 0,
    clarity: 0,
    energy: 0
  });

  const [consultationLogs, setConsultationLogs] = useState<ConsultationLog[]>([]);

  // Sistem Penerima Data dari Streamlit
  useEffect(() => {
    // Cek apakah ada hasil yang disuntikkan langsung oleh Streamlit
    const initialResult = (window as any).initialResult;
    if (initialResult) {
      setAnalysisResult(initialResult);
      setIsAnalyzed(true);
      setIsAnalyzing(false);
      
      const newLog: ConsultationLog = {
        id: Date.now().toString(),
        time: new Date().toLocaleTimeString('id-ID'),
        input: initialResult.originalText || '',
        status: initialResult.status,
        sentiment: initialResult.sentiment,
        confidence: initialResult.clarity
      };
      setConsultationLogs(prev => [newLog, ...prev]);
      // Bersihkan agar tidak muncul terus saat refresh
      delete (window as any).initialResult;
    }

    const onRender = (event: any) => {
      // ... existing listener code if needed ...
    };
    // ...
  }, []);

  const handleAnalyze = async () => {
    if (consultationText.trim()) {
      setIsAnalyzing(true);
      // Kirim data langsung ke Streamlit (bukan ke localhost)
      const Streamlit = (window as any).Streamlit;
      if (Streamlit) {
        Streamlit.setComponentValue({
          action: 'analyze',
          text: consultationText
        });
      } else {
        // Fallback jika dijalankan di luar Streamlit
        console.warn("Streamlit tidak terdeteksi.");
        setIsAnalyzing(false);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.4, 0.6, 0.4]
          }}
          transition={{ duration: 8, repeat: Infinity }}
          className="absolute top-0 right-0 w-[800px] h-[800px] bg-gradient-to-br from-violet-200/40 to-cyan-200/40 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.3, 0.5, 0.3]
          }}
          transition={{ duration: 10, repeat: Infinity }}
          className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-gradient-to-tr from-pink-200/30 to-purple-200/30 rounded-full blur-3xl"
        />
      </div>

      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="ml-80 p-8 relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h2 className="text-4xl font-bold text-slate-800 mb-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>
            Analisis Kesehatan Mental AI
          </h2>
          <p className="text-slate-600">Bagikan pikiran Anda dan biarkan AI kami memberikan wawasan</p>
        </motion.div>

        {/* Input Konsultasi */}
        <GlassPanel glow className="mb-8">
          <div className="p-8">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-violet-600" />
              <label className="text-slate-800 font-semibold">Konsultasi</label>
            </div>

            <textarea
              value={consultationText}
              onChange={(e) => setConsultationText(e.target.value)}
              placeholder="Ekspresikan diri Anda secara bebas... Bagikan pikiran, perasaan, kekhawatiran, atau apa pun yang ada di pikiran Anda. AI kami akan menganalisis kondisi emosional Anda."
              className="w-full h-40 bg-white/60 border border-violet-200 rounded-2xl px-6 py-4 text-slate-800 placeholder:text-slate-400 focus:outline-none focus:border-violet-400 focus:ring-2 focus:ring-violet-300/30 resize-none backdrop-blur-sm transition-all"
            />

            {/* Tombol Analisis 3D */}
            <motion.button
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="mt-6 relative group"
            >
              <motion.div
                animate={isAnalyzing ? { scale: [1, 1.05, 1] } : {}}
                transition={{ duration: 1, repeat: Infinity }}
                className="relative px-10 py-4 bg-gradient-to-r from-violet-600 via-purple-600 to-cyan-600 rounded-2xl overflow-hidden shadow-[0_0_40px_rgba(139,92,246,0.6)]"
              >
                {/* Shimmer effect */}
                <motion.div
                  animate={{ x: [-200, 200] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12"
                />

                <span className="relative z-10 text-white font-bold flex items-center gap-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                  {isAnalyzing ? (
                    <>
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      >
                        <Zap className="w-5 h-5" />
                      </motion.div>
                      Menganalisis...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      Analisis Kondisi Emosi
                    </>
                  )}
                </span>
              </motion.div>

              {/* Glow effect */}
              <div className="absolute -inset-1 bg-gradient-to-r from-violet-600 to-cyan-600 rounded-2xl blur-xl opacity-50 group-hover:opacity-75 transition-opacity -z-10" />
            </motion.button>
          </div>
        </GlassPanel>

        {/* Analysis Results */}
        {isAnalyzed && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="space-y-8"
          >
            {/* Main Result Card */}
            <GlassPanel>
              <div className="p-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                  {/* Status Info */}
                  <div className="lg:col-span-2 space-y-4">
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.2 }}
                    >
                      <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-100 border border-emerald-300 rounded-full mb-4">
                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                        <span className="text-emerald-700 text-sm font-semibold">Analisis AI Selesai</span>
                      </div>

                      <h3 className="text-3xl font-bold text-slate-800 mb-4" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                        {analysisResult.status}
                      </h3>

                      <p className="text-slate-600 leading-relaxed">
                        {analysisResult.description}
                      </p>

                      <div className="flex items-center gap-4 mt-6 pt-6 border-t border-slate-200">
                        <div className="flex items-center gap-2">
                          <Brain className="w-4 h-4 text-violet-600" />
                          <span className="text-sm text-slate-500">Keyakinan AI:</span>
                          <span className="text-slate-800 font-semibold">{analysisResult.clarity}%</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Clock className="w-4 h-4 text-cyan-600" />
                          <span className="text-sm text-slate-500">Dianalisis dalam 1.2 detik</span>
                        </div>
                      </div>
                    </motion.div>
                  </div>

                  {/* 3D Avatar */}
                  <div className="flex justify-center">
                    <MoodAvatar sentiment={analysisResult.sentiment} />
                  </div>
                </div>
              </div>
            </GlassPanel>

            {/* Holographic Mood Rings */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress
                  value={analysisResult.wellness}
                  color="url(#wellness-gradient)"
                  label="Kesejahteraan"
                  icon={<Sparkles className="w-6 h-6 text-emerald-400" />}
                />
                <svg width="0" height="0">
                  <defs>
                    <linearGradient id="wellness-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#10b981" />
                      <stop offset="100%" stopColor="#06b6d4" />
                    </linearGradient>
                  </defs>
                </svg>
              </GlassPanel>

              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress
                  value={100 - analysisResult.stress}
                  color="url(#calm-gradient)"
                  label="Ketenangan"
                  icon={<span className="text-2xl">🧘</span>}
                />
                <svg width="0" height="0">
                  <defs>
                    <linearGradient id="calm-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#8b5cf6" />
                      <stop offset="100%" stopColor="#ec4899" />
                    </linearGradient>
                  </defs>
                </svg>
              </GlassPanel>

              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress
                  value={analysisResult.clarity}
                  color="url(#clarity-gradient)"
                  label="Kejelasan"
                  icon={<span className="text-2xl">💎</span>}
                />
                <svg width="0" height="0">
                  <defs>
                    <linearGradient id="clarity-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#06b6d4" />
                      <stop offset="100%" stopColor="#3b82f6" />
                    </linearGradient>
                  </defs>
                </svg>
              </GlassPanel>

              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress
                  value={analysisResult.energy}
                  color="url(#energy-gradient)"
                  label="Energi"
                  icon={<Zap className="w-6 h-6 text-yellow-400" />}
                />
                <svg width="0" height="0">
                  <defs>
                    <linearGradient id="energy-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#f59e0b" />
                      <stop offset="100%" stopColor="#ef4444" />
                    </linearGradient>
                  </defs>
                </svg>
              </GlassPanel>
            </div>
          </motion.div>
        )}

        {/* Consultation History - Premium Cards */}
        <div className="mt-8">
          <h3 className="text-2xl font-bold text-slate-800 mb-6" style={{ fontFamily: 'Clash Display, sans-serif' }}>
            Sesi Terakhir
          </h3>

          <div className="space-y-4">
            {consultationLogs.map((log, index) => (
              <motion.div
                key={log.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <GlassPanel>
                  <div className="p-6">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-3">
                          <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                            log.sentiment === 'positive'
                              ? 'bg-emerald-100 text-emerald-600'
                              : log.sentiment === 'negative'
                              ? 'bg-rose-100 text-rose-600'
                              : 'bg-violet-100 text-violet-600'
                          }`}>
                            {log.sentiment === 'positive' ? '😊' : log.sentiment === 'negative' ? '😔' : '😌'}
                          </div>
                          <div>
                            <h4 className="text-slate-800 font-semibold">{log.status}</h4>
                            <p className="text-slate-500 text-sm flex items-center gap-2">
                              <Clock className="w-3 h-3" />
                              {log.time}
                            </p>
                          </div>
                        </div>
                        <p className="text-slate-600 text-sm leading-relaxed">{log.input}</p>
                      </div>

                      <div className="text-right">
                        <div className="text-2xl font-bold text-slate-800" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                          {log.confidence}%
                        </div>
                        <div className="text-xs text-slate-500">Keyakinan</div>
                      </div>
                    </div>
                  </div>
                </GlassPanel>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}