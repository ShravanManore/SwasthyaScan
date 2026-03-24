"""
TB Prediction API - FastAPI Backend
Three prediction modes:
1. X-ray Image Analysis (tb_model.h5 + class_indices.json)
2. Blood Test Report OCR (tb_lgbm_model, tb_scaler, tb_label_encoder)
3. Cough Sound Analysis (cough_model.pkl, features.pkl)
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import joblib
import json
import io
from PIL import Image
import cv2

app = FastAPI(title="TB Prediction API", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Load Models at Startup
# =========================
print("Loading models...")

# Load X-ray model
try:
    xray_model = tf.keras.models.load_model("tb_model (1).h5", compile=False)
    with open("class_indices.json", "r") as f:
        class_indices = json.load(f)
    print("✓ X-ray model loaded successfully")
except Exception as e:
    print(f"✗ Error loading X-ray model: {e}")
    print("  Note: This model may require a specific TensorFlow version")
    xray_model = None
    class_indices = {}

# Load Blood Test model
try:
    blood_model = joblib.load("tb_lgbm_model.pkl")
    blood_scaler = joblib.load("tb_scaler.pkl")
    blood_encoder = joblib.load("tb_label_encoder.pkl")
    print("✓ Blood test model loaded successfully")
except Exception as e:
    print(f"✗ Error loading blood test model: {e}")
    blood_model = None
    blood_scaler = None
    blood_encoder = None

# Load Cough model
try:
    cough_model = joblib.load("cough_model.pkl")
    cough_scaler = joblib.load("scaler.pkl")
    cough_features = joblib.load("features.pkl")
    print("✓ Cough model loaded successfully")
except Exception as e:
    print(f"✗ Error loading cough model: {e}")
    cough_model = None
    cough_scaler = None
    cough_features = None


# =========================
# Pydantic Models
# =========================
class PredictionResponse(BaseModel):
    success: bool
    prediction: str
    confidence: float
    risk_level: str
    precautions: list[str]
    suggestions: list[str]
    details: dict | None = None


class BloodTestData(BaseModel):
    # For manual blood test data entry
    Hemoglobin: float | None = None
    WBC_Count: float | None = None
    RBC_Count: float | None = None
    Platelet_Count: float | None = None
    ESR: float | None = None
    Lymphocytes: float | None = None
    Monocytes: float | None = None
    Neutrophils: float | None = None


# =========================
# Helper Functions
# =========================
def get_xray_prediction(image_bytes: bytes) -> dict:
    """Predict TB from X-ray image"""
    if xray_model is None:
        raise HTTPException(status_code=503, detail="X-ray model not available")
    
    # Load and preprocess image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))  # Adjust size based on your model
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0) / 255.0  # Normalize
    
    # Predict
    predictions = xray_model.predict(img_array, verbose=0)
    confidence = float(np.max(predictions)) * 100
    predicted_class = int(np.argmax(predictions))
    
    # Map to class name
    class_names = {v: k for k, v in class_indices.items()}
    prediction_name = class_names.get(predicted_class, "Unknown")
    
    # Determine risk level
    is_tb = predicted_class == 1 or "TB" in prediction_name.upper()
    risk_level = "High Risk" if is_tb else "Low Risk"
    
    return {
        "prediction": prediction_name,
        "confidence": round(confidence, 2),
        "risk_level": risk_level,
        "is_tb": is_tb
    }


def get_blood_test_prediction(data: dict) -> dict:
    """Predict TB from blood test parameters"""
    if blood_model is None:
        raise HTTPException(status_code=503, detail="Blood test model not available")
    
    # Prepare input data in correct order
    input_data = np.array([[
        data.get('Hemoglobin', 0),
        data.get('WBC_Count', 0),
        data.get('RBC_Count', 0),
        data.get('Platelet_Count', 0),
        data.get('ESR', 0),
        data.get('Lymphocytes', 0),
        data.get('Monocytes', 0),
        data.get('Neutrophils', 0)
    ]])
    
    # Scale
    input_scaled = blood_scaler.transform(input_data)
    
    # Predict
    prediction_encoded = blood_model.predict(input_scaled)[0]
    prediction = blood_encoder.inverse_transform([prediction_encoded])[0]
    confidence = float(np.max(blood_model.predict_proba(input_scaled))) * 100
    
    is_tb = prediction == 1 or (isinstance(prediction, str) and "TB" in prediction.upper())
    risk_level = "High Risk" if is_tb else "Low Risk"
    
    return {
        "prediction": "TB Positive" if is_tb else "TB Negative",
        "confidence": round(confidence, 2),
        "risk_level": risk_level,
        "is_tb": is_tb
    }


def get_cough_prediction(data: dict) -> dict:
    """Predict TB from cough sound features"""
    if cough_model is None:
        raise HTTPException(status_code=503, detail="Cough model not available")
    
    # Prepare input data in correct feature order
    input_values = []
    for feature in cough_features:
        value = data.get(feature, 0)
        input_values.append(value)
    
    input_data = np.array([input_values])
    
    # Scale
    input_scaled = cough_scaler.transform(input_data)
    
    # Predict
    prediction = int(cough_model.predict(input_scaled)[0])
    confidence = float(np.max(cough_model.predict_proba(input_scaled))) * 100
    
    is_tb = prediction == 1
    risk_level = "High Risk" if is_tb else "Low Risk"
    
    return {
        "prediction": "TB Detected" if is_tb else "No TB Detected",
        "confidence": round(confidence, 2),
        "risk_level": risk_level,
        "is_tb": is_tb
    }


def generate_recommendations(is_tb: bool, risk_level: str) -> tuple[list[str], list[str]]:
    """Generate precautions and suggestions based on prediction"""
    if is_tb or risk_level == "High Risk":
        precautions = [
            "Isolate from close contact with others",
            "Wear a mask in public spaces",
            "Cover mouth while coughing or sneezing",
            "Ensure proper ventilation in living spaces",
            "Avoid sharing personal items"
        ]
        suggestions = [
            "Consult a pulmonologist immediately",
            "Get a chest X-ray and sputum test done",
            "Start prescribed medication course",
            "Maintain a healthy diet rich in proteins",
            "Get adequate rest and sleep",
            "Follow up regularly with healthcare provider"
        ]
    else:
        precautions = [
            "Maintain good hygiene practices",
            "Boost immunity through balanced diet",
            "Regular health check-ups",
            "Avoid close contact with infected individuals"
        ]
        suggestions = [
            "Continue regular health monitoring",
            "Maintain a healthy lifestyle",
            "Exercise regularly",
            "Stay hydrated and eat nutritious food"
        ]
    
    return precautions, suggestions


# =========================
# API Routes
# =========================

@app.get("/")
def root():
    models_status = {
        "xray_model": "loaded" if xray_model is not None else "not_available",
        "blood_model": "loaded" if blood_model is not None else "not_available",
        "cough_model": "loaded" if cough_model is not None else "not_available"
    }
    
    return {
        "message": "TB Prediction API is running",
        "version": "1.0.0",
        "models": models_status,
        "endpoints": [
            "/predict/xray",
            "/predict/blood",
            "/predict/cough"
        ]
    }


@app.post("/predict/xray", response_model=PredictionResponse)
async def predict_xray(file: UploadFile = File(...)):
    """
    Predict TB from chest X-ray image upload
    """
    try:
        contents = await file.read()
        
        result = get_xray_prediction(contents)
        precautions, suggestions = generate_recommendations(result["is_tb"], result["risk_level"])
        
        return PredictionResponse(
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            precautions=precautions,
            suggestions=suggestions,
            details={"model_type": "X-ray CNN"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/blood", response_model=PredictionResponse)
async def predict_blood(
    hemoglobin: float | None = Form(None),
    wbc_count: float | None = Form(None),
    rbc_count: float | None = Form(None),
    platelet_count: float | None = Form(None),
    esr: float | None = Form(None),
    lymphocytes: float | None = Form(None),
    monocytes: float | None = Form(None),
    neutrophils: float | None = Form(None),
    file: UploadFile = File(None)
):
    """
    Predict TB from blood test report
    Accepts either form data or OCR from uploaded document
    """
    try:
        # If file is uploaded, perform OCR (simplified - you can enhance this)
        if file:
            # TODO: Implement full OCR processing here
            # For now, use provided form data
            pass
        
        data = {
            "Hemoglobin": hemoglobin,
            "WBC_Count": wbc_count,
            "RBC_Count": rbc_count,
            "Platelet_Count": platelet_count,
            "ESR": esr,
            "Lymphocytes": lymphocytes,
            "Monocytes": monocytes,
            "Neutrophils": neutrophils
        }
        
        result = get_blood_test_prediction(data)
        precautions, suggestions = generate_recommendations(result["is_tb"], result["risk_level"])
        
        return PredictionResponse(
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            precautions=precautions,
            suggestions=suggestions,
            details={"model_type": "LightGBM Classifier"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/cough", response_model=PredictionResponse)
async def predict_cough(
    cough_severity: float = Form(...),
    cough_duration: float = Form(...),
    chest_pain: float = Form(...),
    breathlessness: float = Form(...),
    fever: float = Form(...)
):
    """
    Predict TB from cough sound analysis and symptoms
    """
    try:
        data = {
            "Cough_Severity": cough_severity,
            "Cough_Duration": cough_duration,
            "Chest_Pain": chest_pain,
            "Breathlessness": breathlessness,
            "Fever": fever
        }
        
        result = get_cough_prediction(data)
        precautions, suggestions = generate_recommendations(result["is_tb"], result["risk_level"])
        
        return PredictionResponse(
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            precautions=precautions,
            suggestions=suggestions,
            details={
                "model_type": "Random Forest",
                "symptoms": data
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
