import { motion } from 'framer-motion';
import { FlaskConical, PlayCircle, Upload, FileText, Mic } from 'lucide-react';
import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingPulse from '../components/LoadingPulse';
import MLPipeline from '../components/MLPipeline';
import { useToast } from '../components/ToastProvider';
import { predictFromXray, predictFromBlood, predictFromCough } from '../utils/apiService';

function PredictionPage() {
  const navigate = useNavigate();
  const { showToast } = useToast();
  
  // Mode selection: 'xray', 'blood', 'cough'
  const [selectedMode, setSelectedMode] = useState('xray');
  const [running, setRunning] = useState(false);
  
  // X-ray state
  const [xrayFile, setXrayFile] = useState(null);
  const [xrayPreview, setXrayPreview] = useState(null);
  
  // Blood test state
  const [bloodParams, setBloodParams] = useState({
    wbc_count: '',
    hemoglobin: '',
    esr: '',
    crp: ''
  });
  
  // Cough symptoms state
  const [coughSymptoms, setCoughSymptoms] = useState({
    coughSeverity: '',
    coughDuration: '',
    chestPain: '',
    breathlessness: '',
    fever: ''
  });

  const [predictionResult, setPredictionResult] = useState(null);

  const startPipeline = async () => {
    setRunning(true);
    setPredictionResult(null);

    try {
      let result;
      
      if (selectedMode === 'xray') {
        if (!xrayFile) {
          showToast('Please upload a chest X-ray image');
          setRunning(false);
          return;
        }
        showToast('Analyzing chest X-ray...');
        result = await predictFromXray(xrayFile);
        
      } else if (selectedMode === 'blood') {
        const params = {};
        Object.keys(bloodParams).forEach(key => {
          if (bloodParams[key] !== '') {
            params[key] = parseFloat(bloodParams[key]);
          }
        });
        
        if (Object.keys(params).length === 0) {
          showToast('Please enter blood test parameters');
          setRunning(false);
          return;
        }
        
        showToast('Processing blood test results...');
        result = await predictFromBlood(params);
        
      } else if (selectedMode === 'cough') {
        const symptoms = {};
        Object.keys(coughSymptoms).forEach(key => {
          if (coughSymptoms[key] !== '') {
            symptoms[key] = parseFloat(coughSymptoms[key]);
          }
        });
        
        if (Object.keys(symptoms).length === 0) {
          showToast('Please enter symptom details');
          setRunning(false);
          return;
        }
        
        showToast('Analyzing cough symptoms...');
        result = await predictFromCough(symptoms);
      }

      // Store result in localStorage for ResultPage
      localStorage.setItem('predictionResult', JSON.stringify(result));
      
      showToast('Analysis completed. Redirecting to results.');
      setTimeout(() => navigate('/result'), 800);
      
    } catch (error) {
      console.error('Prediction error:', error);
      showToast(`Error: ${error.message}`);
      setRunning(false);
    }
  };

  const handleXrayFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setXrayFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setXrayPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleBloodParamChange = (e) => {
    const { name, value } = e.target;
    setBloodParams(prev => ({ ...prev, [name]: value }));
  };

  const handleCoughSymptomChange = (e) => {
    const { name, value } = e.target;
    setCoughSymptoms(prev => ({ ...prev, [name]: value }));
  };

  return (
    <section className="container-pad py-10">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-3xl font-bold">TB Prediction Analysis</h1>
        <p className="mt-2 text-slate-600 dark:text-slate-300">
          Choose a prediction method and provide the required information
        </p>
      </motion.div>

      {/* Mode Selection */}
      <div className="grid gap-4 sm:grid-cols-3 mb-6">
        <button
          type="button"
          className={`glass-card p-4 text-center transition-all ${
            selectedMode === 'xray' ? 'ring-2 ring-brand-500 bg-brand-50 dark:bg-brand-900/20' : ''
          }`}
          onClick={() => setSelectedMode('xray')}
        >
          <Upload className="mx-auto mb-2 h-8 w-8" />
          <h3 className="font-semibold">X-ray Analysis</h3>
          <p className="text-xs text-slate-500 mt-1">Upload chest X-ray image</p>
        </button>
        
        <button
          type="button"
          className={`glass-card p-4 text-center transition-all ${
            selectedMode === 'blood' ? 'ring-2 ring-brand-500 bg-brand-50 dark:bg-brand-900/20' : ''
          }`}
          onClick={() => setSelectedMode('blood')}
        >
          <FileText className="mx-auto mb-2 h-8 w-8" />
          <h3 className="font-semibold">Blood Test</h3>
          <p className="text-xs text-slate-500 mt-1">Enter blood parameters</p>
        </button>
        
        <button
          type="button"
          className={`glass-card p-4 text-center transition-all ${
            selectedMode === 'cough' ? 'ring-2 ring-brand-500 bg-brand-50 dark:bg-brand-900/20' : ''
          }`}
          onClick={() => setSelectedMode('cough')}
        >
          <Mic className="mx-auto mb-2 h-8 w-8" />
          <h3 className="font-semibold">Cough Analysis</h3>
          <p className="text-xs text-slate-500 mt-1">Describe your symptoms</p>
        </button>
      </div>

      {/* Input Forms */}
      <div className="glass-card mb-5 p-5">
        {selectedMode === 'xray' && (
          <div>
            <label className="block text-sm font-medium mb-2">Upload Chest X-ray Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={handleXrayFileChange}
              className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100 dark:file:bg-brand-900/50 dark:file:text-brand-300"
            />
            {xrayPreview && (
              <div className="mt-4">
                <img src={xrayPreview} alt="X-ray preview" className="max-h-64 rounded-lg mx-auto" />
              </div>
            )}
          </div>
        )}

        {selectedMode === 'blood' && (
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium mb-1">WBC Count (cells/μL)</label>
              <input
                type="number"
                step="any"
                name="wbc_count"
                value={bloodParams.wbc_count}
                onChange={handleBloodParamChange}
                placeholder="e.g., 7000"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Hemoglobin (g/dL)</label>
              <input
                type="number"
                step="any"
                name="hemoglobin"
                value={bloodParams.hemoglobin}
                onChange={handleBloodParamChange}
                placeholder="e.g., 12.5"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">ESR (mm/hr)</label>
              <input
                type="number"
                step="any"
                name="esr"
                value={bloodParams.esr}
                onChange={handleBloodParamChange}
                placeholder="e.g., 20"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">CRP (mg/L)</label>
              <input
                type="number"
                step="any"
                name="crp"
                value={bloodParams.crp}
                onChange={handleBloodParamChange}
                placeholder="e.g., 5.0"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              />
            </div>
          </div>
        )}

        {selectedMode === 'cough' && (
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium mb-1">Cough Severity (0-10)</label>
              <input
                type="number"
                step="any"
                name="coughSeverity"
                value={coughSymptoms.coughSeverity}
                onChange={handleCoughSymptomChange}
                placeholder="Rate from 0-10"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Cough Duration (days)</label>
              <input
                type="number"
                step="any"
                name="coughDuration"
                value={coughSymptoms.coughDuration}
                onChange={handleCoughSymptomChange}
                placeholder="Number of days"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Chest Pain (0=no, 1=yes)</label>
              <select
                name="chestPain"
                value={coughSymptoms.chestPain}
                onChange={handleCoughSymptomChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              >
                <option value="">Select</option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Breathlessness (0=no, 1=yes)</label>
              <select
                name="breathlessness"
                value={coughSymptoms.breathlessness}
                onChange={handleCoughSymptomChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              >
                <option value="">Select</option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Fever (0=no, 1=yes)</label>
              <select
                name="fever"
                value={coughSymptoms.fever}
                onChange={handleCoughSymptomChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg dark:border-slate-600 dark:bg-slate-800"
              >
                <option value="">Select</option>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>
          </div>
        )}

        <div className="mt-6 flex justify-end">
          <button
            type="button"
            className="btn-primary gap-2"
            onClick={startPipeline}
            disabled={running}
          >
            <PlayCircle size={16} /> {running ? 'Analyzing...' : 'Start Analysis'}
          </button>
        </div>
      </div>

      {running && <LoadingPulse label="AI is processing your data..." />}

      <div className="mt-6 rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm text-brand-700 dark:border-brand-800 dark:bg-brand-950/30 dark:text-brand-200">
        <div className="flex items-center gap-2 font-semibold">
          <FlaskConical size={16} /> AI Analysis Note
        </div>
        <p className="mt-1">Results are generated using machine learning models. Please consult a healthcare professional for proper diagnosis.</p>
      </div>
    </section>
  );
}

export default PredictionPage;
