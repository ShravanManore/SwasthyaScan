import { motion } from 'framer-motion';
import { ArrowRight, BookOpenCheck, PlayCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import ChatbotWidget from '../components/ChatbotWidget';
import FeaturesGrid from '../components/FeaturesGrid';
import MedicalHeroArt from '../components/MedicalHeroArt';
import PipelinePreview from '../components/PipelinePreview';
import StatsCards from '../components/StatsCards';
import { featureList, homePipeline, stats } from '../utils/mockData';

function HomePage() {
  return (
    <>
      <section className="container-pad grid gap-10 py-12 lg:grid-cols-2 lg:items-center lg:py-16">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <span className="inline-block rounded-full bg-brand-100 px-3 py-1 text-xs font-semibold text-brand-700 dark:bg-brand-950 dark:text-brand-200">
            AI-Enabled Healthcare Frontend
          </span>
          <h1 className="mt-4 text-4xl font-extrabold tracking-tight sm:text-5xl">SwasthyaScan</h1>
          <p className="mt-3 text-xl font-semibold text-slate-700 dark:text-slate-200">AI-Powered Tuberculosis Detection System</p>
          <p className="mt-3 max-w-xl text-slate-600 dark:text-slate-300">
            Smart AI-Powered Tuberculosis Detection for Early and Reliable Diagnosis
          </p>

          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/prediction" className="btn-primary gap-2">
              Start Screening <ArrowRight size={16} />
            </Link>
            <a href="#about" className="btn-secondary gap-2">
              Learn More <BookOpenCheck size={16} />
            </a>
          </div>
        </motion.div>

        <MedicalHeroArt />
      </section>

      <section id="about" className="container-pad py-10">
        <div className="glass-card p-8">
          <h2 className="text-2xl font-bold">About SwasthyaScan</h2>
          <p className="mt-3 text-slate-600 dark:text-slate-300">
            SwasthyaScan enables early TB detection with a clear ML-assisted screening flow. The platform is designed
            to support faster preliminary diagnosis, improve triage efficiency, and help doctors and patients make
            informed next-step decisions.
          </p>
        </div>
      </section>

      <section className="container-pad py-10">
        <h2 className="mb-4 text-2xl font-bold">How It Works (ML Pipeline Preview)</h2>
        <PipelinePreview steps={homePipeline} />
      </section>

      <section className="container-pad py-10">
        <h2 className="mb-4 text-2xl font-bold">Features</h2>
        <FeaturesGrid features={featureList} />
      </section>

      <section className="container-pad py-10">
        <h2 className="mb-4 text-2xl font-bold">SwasthyaScan Statistics</h2>
        <StatsCards items={stats} />
      </section>

      <section className="container-pad pb-16">
        <div className="glass-card flex flex-col items-start justify-between gap-4 p-6 md:flex-row md:items-center">
          <div>
            <h3 className="text-xl font-semibold">Ready for AI-assisted TB screening?</h3>
            <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
              Start the guided ML flow with simulated analysis and recommendation output.
            </p>
          </div>
          <Link to="/prediction" className="btn-primary gap-2">
            Run Analysis <PlayCircle size={16} />
          </Link>
        </div>
      </section>

      <ChatbotWidget />
    </>
  );
}

export default HomePage;
