export const stats = [
  { label: 'Screenings Processed', value: '12,480+' },
  { label: 'Average Analysis Time', value: '18 sec' },
  { label: 'Clinical Guidance Accuracy', value: '94.2%' },
  { label: 'Partner Clinics', value: '86' },
];

export const featureList = [
  {
    title: 'Real-time prediction',
    description: 'Get a simulated TB risk prediction in seconds through the SwasthyaScan AI pipeline.',
  },
  {
    title: 'AI-powered analysis',
    description: 'Visual pipeline communicates each stage from data input to clinical decision support.',
  },
  {
    title: 'Smart recommendations',
    description: 'Receive evidence-based mock precautions and next-step suggestions for better outcomes.',
  },
  {
    title: 'Easy-to-use interface',
    description: 'Designed for healthcare staff with clear visuals, guided actions, and responsive UX.',
  },
];

export const homePipeline = ['Upload', 'Preprocess', 'AI Analysis', 'Prediction', 'Guidance'];

export const predictionSteps = [
  'User Input',
  'Data Validation',
  'Image Preprocessing',
  'AI Analysis',
  'Prediction',
  'Decision Support',
];

export const chatbotResponses = {
  symptoms:
    'Common TB symptoms include persistent cough (2+ weeks), chest pain, fever, night sweats, weight loss, and fatigue. Please consult a doctor for proper diagnosis.',
  precautions:
    'Key precautions: cover mouth while coughing, maintain ventilation, wear masks in high-risk settings, and complete prescribed medication without interruption.',
  doctor:
    'Consult a doctor if cough persists for more than two weeks, if you have blood in sputum, or if symptoms worsen. Early medical consultation is important.',
  default:
    'I can help with TB symptoms, TB precautions, and when to consult a doctor. Try typing: symptoms, precautions, or doctor.',
};

export const resultMock = {
  prediction: 'TB Negative',
  confidence: 91.4,
  riskLevel: 'Low Risk',
  precautions: [
    'Continue healthy respiratory hygiene and good ventilation at home/work.',
    'If symptoms persist for more than 2 weeks, seek clinical evaluation.',
    'Maintain nutrition and regular health checkups in high-risk populations.',
  ],
  suggestions: [
    'Schedule a repeat screening in 3-6 months if clinically advised.',
    'Track cough duration, fever, and fatigue in a symptom diary.',
    'Consult a pulmonologist for persistent recurrent respiratory concerns.',
  ],
  videos: [
    'https://www.youtube.com/embed/5k0f2xGf9fQ',
    'https://www.youtube.com/embed/G6w_MfQ4fGQ',
  ],
};
