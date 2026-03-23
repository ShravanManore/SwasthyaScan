import { motion } from 'framer-motion';
import { BrainCog, CheckCircle2, CircleEllipsis, CloudUpload, Microscope, ShieldCheck, Sparkles, WandSparkles } from 'lucide-react';

const icons = [CloudUpload, ShieldCheck, Microscope, BrainCog, Sparkles, WandSparkles];

const statusStyles = {
  pending: 'border-slate-200 bg-white text-slate-500 dark:border-slate-700 dark:bg-slate-900 dark:text-slate-400',
  running: 'border-brand-300 bg-brand-50 text-brand-700 dark:border-brand-700 dark:bg-brand-950/40 dark:text-brand-300',
  completed: 'border-care-300 bg-care-50 text-care-700 dark:border-care-700 dark:bg-care-950/40 dark:text-care-300',
};

function MLPipeline({ steps }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {steps.map((step, index) => {
        const Icon = icons[index % icons.length];
        return (
          <motion.div
            key={step.name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-xl border p-4 transition ${statusStyles[step.status]}`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-3">
                <span className="rounded-lg bg-white/80 p-2 dark:bg-slate-800/70">
                  <Icon size={18} />
                </span>
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wide opacity-70">Step {index + 1}</p>
                  <p className="font-semibold">{step.name}</p>
                </div>
              </div>
              {step.status === 'completed' ? <CheckCircle2 size={18} /> : <CircleEllipsis size={18} />}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}

export default MLPipeline;
