import { motion } from 'framer-motion';

function ResultHeatmapCard() {
  return (
    <div className="glass-card p-5">
      <h3 className="mb-4 text-lg font-semibold">AI Heatmap Overlay (Simulated)</h3>
      <div className="relative h-64 overflow-hidden rounded-xl border border-slate-200 bg-slate-100 dark:border-slate-700 dark:bg-slate-800">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_40%_42%,rgba(34,197,94,0.22),transparent_30%),radial-gradient(circle_at_62%_38%,rgba(6,182,212,0.24),transparent_28%),radial-gradient(circle_at_52%_56%,rgba(239,68,68,0.38),transparent_20%)]" />
        <motion.div
          animate={{ opacity: [0.3, 0.85, 0.3] }}
          transition={{ duration: 2.5, repeat: Infinity }}
          className="absolute inset-0 bg-gradient-to-b from-transparent via-white/20 to-transparent"
        />
        <div className="absolute inset-x-0 bottom-0 flex justify-between bg-white/70 px-3 py-2 text-xs dark:bg-slate-900/70">
          <span>Green/Blue: low concern</span>
          <span>Red: focus region</span>
        </div>
      </div>
    </div>
  );
}

export default ResultHeatmapCard;
