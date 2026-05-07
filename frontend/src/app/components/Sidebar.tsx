import { motion } from 'motion/react';
import { LineChart, Line, ResponsiveContainer, YAxis } from 'recharts';
import { Brain, TrendingUp, Calendar, Award } from 'lucide-react';
import { GlassPanel } from './GlassPanel';

const moodData = [
  { value: 45 },
  { value: 55 },
  { value: 48 },
  { value: 72 },
  { value: 68 },
  { value: 78 },
  { value: 75 }
];

export function Sidebar() {
  return (
    <div className="w-80 h-screen fixed left-0 top-0 p-6 space-y-6 overflow-y-auto">
      {/* Logo */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex items-center gap-3 mb-8"
      >
        <motion.div
          animate={{ rotate: [0, 360] }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-500 to-cyan-500 flex items-center justify-center shadow-[0_0_30px_rgba(139,92,246,0.4)]"
        >
          <Brain className="w-7 h-7 text-white" />
        </motion.div>
        <h1 className="text-3xl font-bold text-slate-800" style={{ fontFamily: 'Clash Display, sans-serif' }}>
          EmosiKu
        </h1>
      </motion.div>

      {/* App Branding */}
      <GlassPanel glow>
        <div className="p-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-600 flex items-center justify-center shadow-lg shadow-violet-200">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-800 tracking-tight" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                EmosiKu
              </h2>
              <p className="text-slate-500 text-xs font-medium uppercase tracking-widest">AI Mental Health</p>
            </div>
          </div>
        </div>
      </GlassPanel>

      <GlassPanel glow>
        <div className="p-6">
          <div className="grid grid-cols-3 gap-3">
            <div className="text-center">
              <div className="text-xl font-bold text-slate-800" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                0
              </div>
              <div className="text-xs text-slate-500">Sesi</div>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-slate-800" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                0%
              </div>
              <div className="text-xs text-slate-500">Kesehatan</div>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-slate-800" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                0
              </div>
              <div className="text-xs text-slate-500">Pencapaian</div>
            </div>
          </div>
        </div>
      </GlassPanel>

      {/* Mood Journey */}
      <GlassPanel>
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-slate-800 font-semibold flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-cyan-600" />
              Jejak Emosi
            </h3>
            <span className="text-xs text-slate-500">7 Hari</span>
          </div>

          <div className="h-32 relative">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={moodData}>
                <defs>
                  <linearGradient id="lineGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#8b5cf6" />
                    <stop offset="100%" stopColor="#06b6d4" />
                  </linearGradient>
                </defs>
                <YAxis hide domain={[0, 100]} />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="url(#lineGradient)"
                  strokeWidth={3}
                  dot={false}
                  filter="drop-shadow(0 0 6px rgba(139, 92, 246, 0.4))"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-200">
            <span className="text-sm text-slate-500">Tren Saat Ini</span>
            <span className="text-emerald-600 text-sm font-semibold flex items-center gap-1">
              <TrendingUp className="w-4 h-4" />
              +12%
            </span>
          </div>
        </div>
      </GlassPanel>

      {/* Quick Stats */}
      <GlassPanel>
        <div className="p-6 space-y-3">
          <h3 className="text-slate-800 font-semibold mb-4">Statistik Cepat</h3>

          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-violet-100 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-violet-600" />
            </div>
            <div className="flex-1">
              <div className="text-sm text-slate-500">Sesi Terakhir</div>
              <div className="text-slate-800 font-semibold">-</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-cyan-100 flex items-center justify-center">
              <Award className="w-5 h-5 text-cyan-600" />
            </div>
            <div className="flex-1">
              <div className="text-sm text-slate-500">Pencapaian</div>
              <div className="text-slate-800 font-semibold">0 Terbuka</div>
            </div>
          </div>
        </div>
      </GlassPanel>
    </div>
  );
}
