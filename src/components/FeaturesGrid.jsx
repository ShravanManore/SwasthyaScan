import { motion } from 'framer-motion';
import { Activity, BrainCircuit, Sparkles, TabletSmartphone } from 'lucide-react';

const iconMap = [Activity, BrainCircuit, Sparkles, TabletSmartphone];

function FeaturesGrid({ features }) {
  return (
    <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
      {features.map((feature, index) => {
        const Icon = iconMap[index % iconMap.length];
        return (
          <motion.article
            key={feature.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.08 }}
            className="glass-card p-5"
          >
            <div className="mb-4 inline-flex rounded-lg bg-brand-100 p-2 text-brand-700 dark:bg-brand-950 dark:text-brand-300">
              <Icon size={20} />
            </div>
            <h3 className="text-lg font-semibold">{feature.title}</h3>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{feature.description}</p>
          </motion.article>
        );
      })}
    </div>
  );
}

export default FeaturesGrid;
