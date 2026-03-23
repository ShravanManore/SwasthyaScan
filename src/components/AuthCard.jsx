import { motion } from 'framer-motion';
import Logo from './Logo';

function AuthCard({ title, subtitle, ctaLabel, onSubmit }) {
  return (
    <motion.form
      onSubmit={onSubmit}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card mx-auto w-full max-w-md space-y-4 p-8"
    >
      <div className="space-y-3 text-center">
        <div className="flex justify-center">
          <Logo withLink={false} />
        </div>
        <h1 className="text-2xl font-bold">Welcome to SwasthyaScan</h1>
        <p className="text-sm text-slate-500 dark:text-slate-300">{subtitle}</p>
      </div>

      <div className="space-y-3">
        <input
          required
          type="email"
          placeholder="Email address"
          className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-brand-500 dark:border-slate-700 dark:bg-slate-800"
        />
        <input
          required
          type="password"
          placeholder="Password"
          className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-brand-500 dark:border-slate-700 dark:bg-slate-800"
        />
        {title === 'Register' && (
          <input
            required
            type="text"
            placeholder="Healthcare facility"
            className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none focus:border-brand-500 dark:border-slate-700 dark:bg-slate-800"
          />
        )}
      </div>

      <button type="submit" className="btn-primary w-full">
        {ctaLabel}
      </button>
    </motion.form>
  );
}

export default AuthCard;
