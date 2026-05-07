import { motion } from 'motion/react';
import { ReactNode } from 'react';

interface GlassPanelProps {
  children: ReactNode;
  className?: string;
  glow?: boolean;
}

export function GlassPanel({ children, className = '', glow = false }: GlassPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className={`
        relative backdrop-blur-xl bg-white/70
        border border-white/60 rounded-3xl
        shadow-[0_8px_32px_0_rgba(139,92,246,0.15)]
        ${glow ? 'shadow-[0_0_40px_rgba(139,92,246,0.25)]' : ''}
        ${className}
      `}
    >
      {/* Glass reflection effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/40 to-transparent rounded-3xl pointer-events-none" />
      {children}
    </motion.div>
  );
}
