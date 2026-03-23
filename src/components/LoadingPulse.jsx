import { motion } from 'framer-motion';

function LoadingPulse({ label = 'Processing AI model...' }) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-brand-200 bg-brand-50 px-4 py-3 text-sm text-brand-700 dark:border-brand-700 dark:bg-brand-950/40 dark:text-brand-200">
      <div className="flex gap-1">
        {[0, 1, 2].map((dot) => (
          <motion.span
            key={dot}
            animate={{ opacity: [0.3, 1, 0.3], y: [0, -3, 0] }}
            transition={{ duration: 0.9, delay: dot * 0.12, repeat: Infinity }}
            className="h-2.5 w-2.5 rounded-full bg-brand-600"
          />
        ))}
      </div>
      <span>{label}</span>
    </div>
  );
}

export default LoadingPulse;
