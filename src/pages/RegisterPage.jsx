import { useNavigate } from 'react-router-dom';
import AuthCard from '../components/AuthCard';
import { useToast } from '../components/ToastProvider';

function RegisterPage() {
  const navigate = useNavigate();
  const { showToast } = useToast();

  const handleSubmit = (event) => {
    event.preventDefault();
    showToast('Registration completed. Welcome to SwasthyaScan.');
    setTimeout(() => navigate('/dashboard'), 700);
  };

  return (
    <section className="container-pad py-16">
      <AuthCard
        title="Register"
        subtitle="Create your SwasthyaScan access to begin AI-powered TB screening."
        ctaLabel="Register with SwasthyaScan"
        onSubmit={handleSubmit}
      />
    </section>
  );
}

export default RegisterPage;
