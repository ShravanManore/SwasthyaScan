import { motion } from 'framer-motion';
import { Menu, X } from 'lucide-react';
import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import Logo from './Logo';
import ThemeToggle from './ThemeToggle';

const navItems = [
  { label: 'Home', to: '/' },
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Prediction', to: '/prediction' },
  { label: 'Results', to: '/result' },
];

function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-slate-200/80 bg-white/90 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90">
      <div className="container-pad flex h-20 items-center justify-between">
        <Logo />

        <nav className="hidden items-center gap-8 md:flex">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `text-sm font-medium transition ${
                  isActive
                    ? 'text-brand-700 dark:text-brand-300'
                    : 'text-slate-600 hover:text-brand-700 dark:text-slate-300 dark:hover:text-brand-300'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="hidden items-center gap-3 md:flex">
          <ThemeToggle />
          <Link to="/login" className="btn-secondary px-4 py-2 text-sm">
            Login
          </Link>
          <Link to="/register" className="btn-primary px-4 py-2 text-sm">
            Register
          </Link>
        </div>

        <button
          type="button"
          className="rounded-lg border border-slate-200 p-2 md:hidden dark:border-slate-700"
          onClick={() => setOpen((prev) => !prev)}
          aria-label="Toggle menu"
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {open && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="border-t border-slate-200 bg-white px-4 pb-4 pt-3 dark:border-slate-800 dark:bg-slate-950 md:hidden"
        >
          <div className="mb-3 flex items-center justify-between">
            <ThemeToggle />
            <div className="flex gap-2">
              <Link to="/login" className="btn-secondary px-3 py-1.5 text-sm" onClick={() => setOpen(false)}>
                Login
              </Link>
              <Link to="/register" className="btn-primary px-3 py-1.5 text-sm" onClick={() => setOpen(false)}>
                Register
              </Link>
            </div>
          </div>
          <div className="grid gap-2">
            {navItems.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 hover:bg-brand-50 dark:text-slate-200 dark:hover:bg-slate-800"
              >
                {item.label}
              </Link>
            ))}
          </div>
        </motion.div>
      )}
    </header>
  );
}

export default Navbar;
