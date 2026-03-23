import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

function PipelinePreview({ steps }) {
  return (
    <div className="glass-card overflow-x-auto p-5">
      <div className="flex min-w-max items-center gap-2">
        {steps.map((step, index) => (
          <div key={step} className="flex items-center gap-2">
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.08 }}
              className="rounded-xl border border-brand-200 bg-white px-4 py-2 text-sm font-medium text-brand-700 dark:border-slate-700 dark:bg-slate-900 dark:text-brand-300"
            >
              {step}
            </motion.div>
            {index < steps.length - 1 && <ArrowRight size={16} className="text-slate-400" />}
          </div>
        ))}
      </div>
    </div>
  );
}

export default PipelinePreview;
