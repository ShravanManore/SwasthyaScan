import Logo from './Logo';

function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
      <div className="container-pad flex flex-col gap-4 py-8 md:flex-row md:items-center md:justify-between">
        <Logo withLink={false} />
        <div className="text-sm text-slate-500 dark:text-slate-400">
          <p>Smart AI-Powered Tuberculosis Detection for Early and Reliable Diagnosis</p>
          <p className="mt-1">© {new Date().getFullYear()} SwasthyaScan. Frontend Prototype.</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
