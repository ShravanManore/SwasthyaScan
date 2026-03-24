# TB Prediction System - Full Stack Application

A comprehensive AI-powered Tuberculosis detection system using multiple machine learning models for accurate diagnosis through different methods.

## 🌟 Features

### Three Prediction Modes

1. **🫁 X-ray Analysis**
   - Upload chest X-ray images
   - Uses deep learning CNN model (`tb_model.h5`)
   - Detects TB from radiological patterns
   - Instant prediction with confidence score

2. **🩸 Blood Test Analysis**
   - Input blood test parameters
   - Uses LightGBM classifier (`tb_lgbm_model.pkl`)
   - Analyzes:
     - Hemoglobin, WBC Count, RBC Count
     - Platelet Count, ESR
     - Lymphocytes, Monocytes, Neutrophils
   - Preprocessing with `tb_scaler.pkl`

3. **🎤 Cough Sound Analysis**
   - Symptom-based prediction
   - Uses Random Forest classifier (`cough_model.pkl`)
   - Analyzes:
     - Cough severity and duration
     - Chest pain, breathlessness, fever
   - Pattern recognition from clinical features

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI (Python)
- **Models**: TensorFlow, scikit-learn, LightGBM
- **Features**:
  - RESTful API endpoints
  - CORS enabled for frontend communication
  - Real-time predictions
  - Comprehensive error handling

### Frontend (React + Vite)
- **Framework**: React 18 with Vite
- **Styling**: TailwindCSS
- **Features**:
  - Modern, responsive UI
  - Three-mode selection interface
  - File upload with preview
  - Form-based data entry
  - Real-time result display
  - Dark mode support

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd tb_predict
```

### 2. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues with TensorFlow on Windows, you may need to install it separately:
```bash
pip install tensorflow==2.15.0
```

### 3. Install Frontend Dependencies
```bash
npm install
```

## 🚀 Running the Application

### Option 1: Start Both Servers Together
```bash
python start.py
```

This will automatically start both the backend and frontend servers.

### Option 2: Start Separately

**Terminal 1 - Backend:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

### Access the Application
- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 API Endpoints

### 1. X-ray Prediction
```http
POST /predict/xray
Content-Type: multipart/form-data

Parameters:
- file: Image file (chest X-ray)

Response:
{
  "success": true,
  "prediction": "TB Chest X-rays",
  "confidence": 94.5,
  "risk_level": "High Risk",
  "precautions": [...],
  "suggestions": [...],
  "details": {"model_type": "X-ray CNN"}
}
```

### 2. Blood Test Prediction
```http
POST /predict/blood
Content-Type: application/x-www-form-urlencoded

Parameters:
- hemoglobin: float
- wbc_count: float
- rbc_count: float
- platelet_count: float
- esr: float
- lymphocytes: float
- monocytes: float
- neutrophils: float

Response: Same as above
```

### 3. Cough Analysis Prediction
```http
POST /predict/cough
Content-Type: application/x-www-form-urlencoded

Parameters:
- cough_severity: float (0-10)
- cough_duration: float (days)
- chest_pain: float (0 or 1)
- breathlessness: float (0 or 1)
- fever: float (0 or 1)

Response: Same as above
```

## 🎯 Usage Guide

### Using X-ray Analysis
1. Navigate to Prediction page
2. Select "X-ray Analysis" mode
3. Upload a chest X-ray image (JPG, PNG)
4. Click "Start Analysis"
5. View results with confidence score

### Using Blood Test Analysis
1. Navigate to Prediction page
2. Select "Blood Test" mode
3. Enter blood test parameters from lab report
4. Click "Start Analysis"
5. Review prediction and recommendations

### Using Cough Analysis
1. Navigate to Prediction page
2. Select "Cough Analysis" mode
3. Fill in symptom details:
   - Rate cough severity (0-10)
   - Duration in days
   - Yes/No for chest pain, breathlessness, fever
4. Click "Start Analysis"
5. Get instant prediction

## 📊 Model Information

### X-ray Model
- **Type**: Convolutional Neural Network (CNN)
- **Input**: 224x224 RGB images
- **Classes**: Normal vs TB
- **File**: `tb_model (1).h5`

### Blood Test Model
- **Type**: LightGBM Classifier
- **Features**: 8 blood parameters
- **Preprocessing**: StandardScaler
- **Files**: `tb_lgbm_model.pkl`, `tb_scaler.pkl`, `tb_label_encoder.pkl`

### Cough Model
- **Type**: Random Forest Classifier
- **Features**: 5 clinical symptoms
- **Preprocessing**: StandardScaler
- **Files**: `cough_model.pkl`, `scaler.pkl`, `features.pkl`

## 🔧 Configuration

### Backend Configuration
Edit `main.py` to modify:
- CORS origins (line 16)
- Model loading paths
- Prediction thresholds
- Recommendation text

### Frontend Configuration
Edit `src/utils/apiService.js` to change:
- API base URL (default: http://localhost:8000)

## ⚠️ Important Notes

1. **Medical Disclaimer**: This system is for educational/research purposes only. Always consult healthcare professionals for medical diagnosis.

2. **Model Accuracy**: Predictions are based on trained models but should not replace professional medical advice.

3. **Data Privacy**: Patient data should be handled according to HIPAA or local regulations.

4. **Production Deployment**: For production use:
   - Implement authentication
   - Add rate limiting
   - Use HTTPS
   - Store models securely
   - Log all predictions
   - Regular model updates
