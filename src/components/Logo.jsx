import { Heart, Stethoscope } from 'lucide-react';
import { Link } from 'react-router-dom';

function Logo({ withLink = true }) {
  const content = (
    <div className="flex items-center gap-3">
      <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-care-500 text-white shadow-soft">
        <Heart size={20} />
        <span className="absolute -right-1 -top-1 rounded-full bg-white p-0.5 text-brand-600">
          <Stethoscope size={11} />
        </span>
      </div>
      <div>
        <p className="text-lg font-bold tracking-tight text-slate-900 dark:text-white">SwasthyaScan</p>
        <p className="text-xs text-slate-500 dark:text-slate-400">AI TB Screening</p>
      </div>
    </div>
  );

  if (!withLink) return content;

  return <Link to="/">{content}</Link>;
}

export default Logo;
