import { motion } from 'motion/react';

interface MoodAvatarProps {
  sentiment: 'positive' | 'neutral' | 'negative';
}

export function MoodAvatar({ sentiment }: MoodAvatarProps) {
  const getExpression = () => {
    switch (sentiment) {
      case 'positive':
        return {
          eyes: '😊',
          color: 'from-emerald-400 to-cyan-400',
          glow: 'shadow-[0_0_50px_rgba(52,211,153,0.4)]'
        };
      case 'negative':
        return {
          eyes: '😔',
          color: 'from-rose-400 to-pink-400',
          glow: 'shadow-[0_0_50px_rgba(251,113,133,0.4)]'
        };
      default:
        return {
          eyes: '😌',
          color: 'from-violet-400 to-purple-400',
          glow: 'shadow-[0_0_50px_rgba(167,139,250,0.4)]'
        };
    }
  };

  const expression = getExpression();

  return (
    <motion.div
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={{ type: 'spring', duration: 1, bounce: 0.5 }}
      className="relative"
    >
      {/* Outer glow ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
        className={`absolute inset-0 rounded-full bg-gradient-to-r ${expression.color} opacity-30 blur-2xl ${expression.glow}`}
      />

      {/* Avatar */}
      <motion.div
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
        className={`relative w-40 h-40 rounded-full bg-gradient-to-br ${expression.color} flex items-center justify-center text-7xl ${expression.glow}`}
      >
        {expression.eyes}
      </motion.div>

      {/* Floating particles */}
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          animate={{
            y: [0, -40, 0],
            x: [0, Math.sin(i) * 20, 0],
            opacity: [0, 0.7, 0]
          }}
          transition={{
            duration: 2 + i,
            repeat: Infinity,
            delay: i * 0.5
          }}
          className={`absolute w-2 h-2 rounded-full bg-gradient-to-r ${expression.color} blur-sm`}
          style={{
            top: `${30 + i * 20}%`,
            left: `${20 + i * 30}%`
          }}
        />
      ))}
    </motion.div>
  );
}
