/**
 * API Service for TB Prediction Backend
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Upload X-ray image and get prediction
 */
export async function predictFromXray(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(`${API_BASE_URL}/predict/xray`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'X-ray prediction failed');
  }

  return await response.json();
}

/**
 * Get prediction from blood test parameters
 */
export async function predictFromBlood(params) {
  const formData = new FormData();
  
  // Append all provided parameters
  Object.keys(params).forEach((key) => {
    if (params[key] !== null && params[key] !== undefined) {
      formData.append(key.toLowerCase(), params[key]);
    }
  });

  const response = await fetch(`${API_BASE_URL}/predict/blood`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Blood test prediction failed');
  }

  return await response.json();
}

/**
 * Get prediction from cough analysis
 */
export async function predictFromCough(symptoms) {
  const formData = new FormData();
  
  formData.append('cough_severity', symptoms.coughSeverity || 0);
  formData.append('cough_duration', symptoms.coughDuration || 0);
  formData.append('chest_pain', symptoms.chestPain || 0);
  formData.append('breathlessness', symptoms.breathlessness || 0);
  formData.append('fever', symptoms.fever || 0);

  const response = await fetch(`${API_BASE_URL}/predict/cough`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Cough prediction failed');
  }

  return await response.json();
}

/**
 * Check API health
 */
export async function checkApiHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    return await response.json();
  } catch (error) {
    return null;
  }
}
