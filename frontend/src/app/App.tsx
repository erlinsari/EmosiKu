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
  const [isAnalyzed, setIsAnalyzed] = useState(false);
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

  useEffect(() => {
    // Terima data hasil analisis langsung dari Python
    const result = (window as any).initialResult;
    if (result && result.status) {
      setAnalysisResult(result);
      setIsAnalyzed(true);
      
      const newLog: ConsultationLog = {
        id: Date.now().toString(),
        time: new Date().toLocaleTimeString('id-ID'),
        input: result.originalText || '',
        status: result.status,
        sentiment: result.sentiment,
        confidence: result.clarity
      };
      setConsultationLogs(prev => [newLog, ...prev]);
    }
  }, []);

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
          <p className="text-slate-600">Gunakan kotak input di bawah untuk memulai analisis emosi Anda</p>
        </motion.div>

        {!isAnalyzed ? (
          <GlassPanel glow className="p-12 text-center">
            <div className="max-w-md mx-auto space-y-4">
              <div className="w-20 h-20 bg-violet-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
                <Sparkles className="w-10 h-10 text-violet-600" />
              </div>
              <h3 className="text-2xl font-bold text-slate-800">Siap Mendengarkan</h3>
              <p className="text-slate-500">Silakan masukkan curhatan Anda pada kotak input di bawah halaman ini untuk melihat wawasan AI.</p>
            </div>
          </GlassPanel>
        ) : (
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="space-y-8">
            <GlassPanel>
              <div className="p-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
                  <div className="lg:col-span-2 space-y-4">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-100 border border-emerald-300 rounded-full mb-4">
                      <div className="w-2 h-2 bg-emerald-500 rounded-full" />
                      <span className="text-emerald-700 text-sm font-semibold">Hasil Analisis Terbaru</span>
                    </div>
                    <h3 className="text-3xl font-bold text-slate-800" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                      {analysisResult.status}
                    </h3>
                    <p className="text-slate-600 leading-relaxed">{analysisResult.description}</p>
                    <div className="flex items-center gap-4 mt-6 pt-6 border-t border-slate-200">
                      <div className="flex items-center gap-2">
                        <Brain className="w-4 h-4 text-violet-600" />
                        <span className="text-sm text-slate-500">Keyakinan AI: {analysisResult.clarity}%</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex justify-center">
                    <MoodAvatar sentiment={analysisResult.sentiment} />
                  </div>
                </div>
              </div>
            </GlassPanel>

            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress value={analysisResult.wellness} color="#10b981" label="Kesejahteraan" />
              </GlassPanel>
              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress value={100 - analysisResult.stress} color="#8b5cf6" label="Ketenangan" />
              </GlassPanel>
              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress value={analysisResult.clarity} color="#06b6d4" label="Kejelasan" />
              </GlassPanel>
              <GlassPanel className="p-6 flex justify-center">
                <CircularProgress value={analysisResult.energy} color="#f59e0b" label="Energi" />
              </GlassPanel>
            </div>
          </motion.div>
        )}

        <div className="mt-12">
          <h3 className="text-2xl font-bold text-slate-800 mb-6" style={{ fontFamily: 'Clash Display, sans-serif' }}>Riwayat Sesi</h3>
          <div className="space-y-4">
            {consultationLogs.map((log) => (
              <GlassPanel key={log.id} className="p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-2xl">{log.sentiment === 'positive' ? '😊' : '😔'}</span>
                      <h4 className="text-slate-800 font-semibold">{log.status}</h4>
                    </div>
                    <p className="text-slate-600 text-sm">{log.input}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-slate-800">{log.confidence}%</div>
                    <div className="text-xs text-slate-500">{log.time}</div>
                  </div>
                </div>
              </GlassPanel>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}