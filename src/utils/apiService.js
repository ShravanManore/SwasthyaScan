/**
 * API Service for TB Prediction Backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
    const errorMessage = typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail);
    throw new Error(errorMessage || 'X-ray prediction failed');
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
    const errorMessage = typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail);
    throw new Error(errorMessage || 'Blood test prediction failed');
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
    const errorMessage = typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail);
    throw new Error(errorMessage || 'Cough prediction failed');
  }

  return await response.json();
}

/**
 * Get combined prediction from all three models
 */
export async function predictCombined(params) {
  const formData = new FormData();
  
  // Append X-ray image if provided (as File object)
  if (params.xrayImage instanceof File || params.xrayImage instanceof Blob) {
    formData.append('xray_image', params.xrayImage);
  }
  
  // Append blood test parameters if provided
  if (params.wbc_count !== undefined) formData.append('wbc_count', params.wbc_count);
  if (params.hemoglobin !== undefined) formData.append('hemoglobin', params.hemoglobin);
  if (params.esr !== undefined) formData.append('esr', params.esr);
  if (params.crp !== undefined) formData.append('crp', params.crp);
  
  // Append cough symptoms if provided
  if (params.cough_severity !== undefined) formData.append('cough_severity', params.cough_severity);
  if (params.cough_duration !== undefined) formData.append('cough_duration', params.cough_duration);
  if (params.chest_pain !== undefined) formData.append('chest_pain', params.chest_pain);
  if (params.breathlessness !== undefined) formData.append('breathlessness', params.breathlessness);
  if (params.fever !== undefined) formData.append('fever', params.fever);

  const response = await fetch(`${API_BASE_URL}/predict/combined`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    const errorMessage = typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail);
    throw new Error(errorMessage || 'Combined prediction failed');
  }

  return await response.json();
}
