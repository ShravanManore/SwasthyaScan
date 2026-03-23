import { motion } from 'framer-motion';
import { AlertTriangle, BadgeCheck, ShieldPlus } from 'lucide-react';
import ResultHeatmapCard from '../components/ResultHeatmapCard';
import { resultMock } from '../utils/mockData';

function ResultPage() {
  const riskClass =
    resultMock.riskLevel.toLowerCase().includes('low')
      ? 'text-care-700 bg-care-100 dark:text-care-200 dark:bg-care-900/40'
      : 'text-amber-700 bg-amber-100 dark:text-amber-200 dark:bg-amber-900/40';

  return (
    <section className="container-pad py-10">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-3xl font-bold">SwasthyaScan Results</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          Simulated prediction summary with confidence score, risk profile, and clinical guidance references.
        </p>
      </motion.div>

      <div className="grid gap-5 lg:grid-cols-3">
        <article className="glass-card p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Prediction</p>
          <p className="mt-2 flex items-center gap-2 text-2xl font-bold text-brand-700 dark:text-brand-300">
            <BadgeCheck size={22} /> {resultMock.prediction}
          </p>
        </article>

        <article className="glass-card p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Confidence Score</p>
          <p className="mt-2 text-2xl font-bold text-slate-900 dark:text-slate-100">{resultMock.confidence}%</p>
        </article>

        <article className="glass-card p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Risk Level</p>
          <p className={`mt-2 inline-flex rounded-lg px-3 py-1 text-sm font-semibold ${riskClass}`}>
            {resultMock.riskLevel}
          </p>
        </article>
      </div>

      <div className="mt-6 grid gap-5 lg:grid-cols-2">
        <div className="glass-card p-5">
          <h3 className="flex items-center gap-2 text-lg font-semibold">
            <ShieldPlus size={18} className="text-care-600" /> Precautions
          </h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-600 dark:text-slate-300">
            {resultMock.precautions.map((item) => (
              <li key={item} className="rounded-lg bg-slate-100 px-3 py-2 dark:bg-slate-800">
                {item}
              </li>
            ))}
          </ul>
        </div>

        <div className="glass-card p-5">
          <h3 className="flex items-center gap-2 text-lg font-semibold">
            <AlertTriangle size={18} className="text-amber-500" /> Suggestions
          </h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-600 dark:text-slate-300">
            {resultMock.suggestions.map((item) => (
              <li key={item} className="rounded-lg bg-slate-100 px-3 py-2 dark:bg-slate-800">
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-6">
        <ResultHeatmapCard />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {resultMock.videos.map((videoUrl) => (
          <div key={videoUrl} className="glass-card overflow-hidden p-3">
            <div className="aspect-video overflow-hidden rounded-xl">
              <iframe
                className="h-full w-full"
                src={videoUrl}
                title="TB awareness and treatment guidance"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerPolicy="strict-origin-when-cross-origin"
                allowFullScreen
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default ResultPage;
