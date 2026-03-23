import { motion } from 'framer-motion';
import { Activity, ArrowRight, Bell, ClipboardCheck, Users } from 'lucide-react';
import { Link } from 'react-router-dom';
import StatsCards from '../components/StatsCards';
import { stats } from '../utils/mockData';

const quickCards = [
  { label: 'Pending Reviews', value: '14', icon: ClipboardCheck },
  { label: 'Active Specialists', value: '9', icon: Users },
  { label: 'Alerts Today', value: '3', icon: Bell },
  { label: 'Pipeline Health', value: 'Optimal', icon: Activity },
];

function DashboardPage() {
  return (
    <section className="container-pad py-10">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-3xl font-bold">Welcome to SwasthyaScan Dashboard</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          Track screening flow, monitor mock analytics, and initiate new AI-assisted evaluations.
        </p>
      </motion.div>

      <StatsCards items={stats} />

      <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {quickCards.map((card) => (
          <article key={card.label} className="glass-card p-5">
            <card.icon className="mb-2 text-brand-600" size={20} />
            <p className="text-xl font-bold">{card.value}</p>
            <p className="text-sm text-slate-500 dark:text-slate-300">{card.label}</p>
          </article>
        ))}
      </div>

      <div className="mt-6">
        <Link to="/prediction" className="btn-primary gap-2">
          Go to AI Analysis <ArrowRight size={16} />
        </Link>
      </div>
    </section>
  );
}

export default DashboardPage;
