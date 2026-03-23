import { motion } from 'framer-motion';
import { FlaskConical, PlayCircle } from 'lucide-react';
import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingPulse from '../components/LoadingPulse';
import MLPipeline from '../components/MLPipeline';
import { useToast } from '../components/ToastProvider';
import { runMLSimulation } from '../utils/mlSimulation';
import { predictionSteps } from '../utils/mockData';

function PredictionPage() {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [running, setRunning] = useState(false);

  const [steps, setSteps] = useState(
    predictionSteps.map((name) => ({
      name,
      status: 'pending',
    }))
  );

  const completedCount = useMemo(
    () => steps.filter((step) => step.status === 'completed').length,
    [steps]
  );

  const startPipeline = async () => {
    setRunning(true);
    setSteps((prev) => prev.map((step) => ({ ...step, status: 'pending' })));

    await runMLSimulation((index, status) => {
      setSteps((prev) => prev.map((step, stepIndex) => (stepIndex === index ? { ...step, status } : step)));
    }, 900);

    showToast('SwasthyaScan analysis completed. Redirecting to results.');
    setRunning(false);
    setTimeout(() => navigate('/result'), 800);
  };

  return (
    <section className="container-pad py-10">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-3xl font-bold">SwasthyaScan AI Analysis</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          Interactive ML pipeline with simulated processing stages and live step status indicators.
        </p>
      </motion.div>

      <div className="glass-card mb-5 p-5">
        <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm font-medium text-slate-600 dark:text-slate-300">
            Completed Steps: <span className="text-brand-700 dark:text-brand-300">{completedCount}/6</span>
          </p>
          <button type="button" className="btn-primary gap-2" onClick={startPipeline} disabled={running}>
            <PlayCircle size={16} /> {running ? 'Running Analysis...' : 'Start AI Pipeline'}
          </button>
        </div>

        {running && <LoadingPulse label="SwasthyaScan is processing screening data..." />}
      </div>

      <MLPipeline steps={steps} />

      <div className="mt-6 rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700 dark:border-brand-800 dark:bg-brand-950/30 dark:text-brand-200">
        <div className="flex items-center gap-2 font-semibold">
          <FlaskConical size={16} /> Simulation Note
        </div>
        <p className="mt-1">All results are mock-generated for frontend demonstration and UI/UX validation only.</p>
      </div>
    </section>
  );
}

export default PredictionPage;
