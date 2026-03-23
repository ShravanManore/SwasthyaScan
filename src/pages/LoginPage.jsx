import { useNavigate } from 'react-router-dom';
import AuthCard from '../components/AuthCard';
import { useToast } from '../components/ToastProvider';

function LoginPage() {
  const navigate = useNavigate();
  const { showToast } = useToast();

  const handleSubmit = (event) => {
    event.preventDefault();
    showToast('Login successful. Welcome to SwasthyaScan.');
    setTimeout(() => navigate('/dashboard'), 700);
  };

  return (
    <section className="container-pad py-16">
      <AuthCard
        title="Login"
        subtitle="Secure access for healthcare professionals and diagnostic teams."
        ctaLabel="Login to SwasthyaScan"
        onSubmit={handleSubmit}
      />
    </section>
  );
}

export default LoginPage;
