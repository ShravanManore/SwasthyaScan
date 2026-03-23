import { motion } from 'framer-motion';
import { Cpu, HeartPulse, ScanLine } from 'lucide-react';

function MedicalHeroArt() {
  return (
    <div className="relative mx-auto flex h-80 w-full max-w-md items-center justify-center rounded-3xl bg-hero-gradient p-8">
      <motion.div
        initial={{ opacity: 0.4, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1.2, repeat: Infinity, repeatType: 'reverse' }}
        className="absolute h-60 w-60 rounded-full border-2 border-brand-300/70"
      />
      <motion.div
        initial={{ opacity: 0.2, scale: 1 }}
        animate={{ opacity: 0.8, scale: 1.08 }}
        transition={{ duration: 1.3, repeat: Infinity, repeatType: 'reverse' }}
        className="absolute h-44 w-44 rounded-full border border-care-300/70"
      />
      <div className="relative z-10 grid grid-cols-2 gap-3">
        <div className="glass-card flex h-24 w-24 items-center justify-center text-brand-600">
          <HeartPulse size={34} />
        </div>
        <div className="glass-card flex h-24 w-24 items-center justify-center text-care-600">
          <ScanLine size={34} />
        </div>
        <div className="glass-card col-span-2 flex h-24 items-center justify-center gap-3 text-slate-700 dark:text-slate-200">
          <Cpu className="text-brand-600" />
          <span className="font-semibold">AI Lung Scan Pipeline</span>
        </div>
      </div>
    </div>
  );
}

export default MedicalHeroArt;
