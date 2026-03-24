import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle, BadgeCheck, ShieldPlus } from 'lucide-react';
import ResultHeatmapCard from '../components/ResultHeatmapCard';

function ResultPage() {
  const [result, setResult] = useState(null);

  useEffect(() => {
    // Get prediction result from localStorage
    const storedResult = localStorage.getItem('predictionResult');
    if (storedResult) {
      setResult(JSON.parse(storedResult));
    }
  }, []);

  // Show loading or error if no result
  if (!result) {
    return (
      <section className="container-pad py-10">
        <div className="text-center">
          <h1 className="text-3xl font-bold">No Results Found</h1>
          <p className="mt-2 text-slate-600 dark:text-slate-300">
            Please complete a prediction analysis first.
          </p>
        </div>
      </section>
    );
  }

  const riskClass =
    result.risk_level.toLowerCase().includes('low')
      ? 'text-care-700 bg-care-100 dark:text-care-200 dark:bg-care-900/40'
      : 'text-amber-700 bg-amber-100 dark:text-amber-200 dark:bg-amber-900/40';

  return (
    <section className="container-pad py-10">
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-3xl font-bold">Prediction Results</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          AI-powered TB detection analysis with confidence score and recommendations
        </p>
      </motion.div>

      {/* Model Type Info */}
      {result.details && (
        <div className="glass-card mb-5 p-4">
          <p className="text-sm text-slate-600 dark:text-slate-300">
            <span className="font-semibold">Analysis Method:</span> {result.details.model_type}
          </p>
        </div>
      )}

      <div className="grid gap-5 lg:grid-cols-3">
        <article className="glass-card p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Prediction</p>
          <p className="mt-2 flex items-center gap-2 text-2xl font-bold text-brand-700 dark:text-brand-300">
            <BadgeCheck size={22} /> {result.prediction}
          </p>
        </article>

        <article className="glass-card p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Confidence Score</p>
          <p className="mt-2 text-2xl font-bold text-slate-900 dark:text-slate-100">{result.confidence}%</p>
        </article>

        <article className="glass-card p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Risk Level</p>
          <p className={`mt-2 inline-flex rounded-lg px-3 py-1 text-sm font-semibold ${riskClass}`}>
            {result.risk_level}
          </p>
        </article>
      </div>

      <div className="mt-6 grid gap-5 lg:grid-cols-2">
        <div className="glass-card p-5">
          <h3 className="flex items-center gap-2 text-lg font-semibold">
            <ShieldPlus size={18} className="text-care-600" /> Precautions
          </h3>
          <ul className="mt-3 space-y-2 text-sm text-slate-600 dark:text-slate-300">
            {result.precautions.map((item, index) => (
              <li key={index} className="rounded-lg bg-slate-100 px-3 py-2 dark:bg-slate-800">
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
            {result.suggestions.map((item, index) => (
              <li key={index} className="rounded-lg bg-slate-100 px-3 py-2 dark:bg-slate-800">
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-6">
        <ResultHeatmapCard />
      </div>

      <div className="mt-6 glass-card p-5">
        <h3 className="text-lg font-semibold mb-3">Educational Resources</h3>
        <p className="text-sm text-slate-600 dark:text-slate-300">
          Watch these videos to learn more about TB prevention, diagnosis, and treatment.
        </p>
      </div>
    </section>
  );
}

export default ResultPage;
