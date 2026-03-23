import { motion } from 'framer-motion';

function StatsCards({ items }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {items.map((item, index) => (
        <motion.article
          key={item.label}
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: index * 0.07 }}
          className="glass-card p-5"
        >
          <p className="text-2xl font-bold text-brand-700 dark:text-brand-300">{item.value}</p>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-300">{item.label}</p>
        </motion.article>
      ))}
    </div>
  );
}

export default StatsCards;
