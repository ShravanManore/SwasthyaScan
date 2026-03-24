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
    # Try loading with compile=False first (handles version mismatches)
    xray_model = tf.keras.models.load_model("tb_model (1).h5", compile=False)
    with open("class_indices.json", "r") as f:
        class_indices = json.load(f)
    print("✓ X-ray model loaded successfully")
except Exception as e:
    print(f"✗ Error loading X-ray model: {e}")
    print("  Attempting alternative loading method...")
    try:
        # Alternative: Load without custom objects
        xray_model = tf.keras.models.load_model(
            "tb_model (1).h5",
            compile=False,
            custom_objects=None
        )
        with open("class_indices.json", "r") as f:
            class_indices = json.load(f)
        print("✓ X-ray model loaded with alternative method")
    except Exception as e2:
        print(f"✗ Failed to load X-ray model: {e2}")
        print("  Note: This model may require a specific TensorFlow version")
        print("  Blood test and cough models will still work")
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


class CombinedPredictionRequest(BaseModel):
    """Request for combined prediction using all three models"""
    # X-ray (optional)
    xray_image: str | None = None  # base64 encoded image
    
    # Blood test parameters
    wbc_count: float | None = None
    hemoglobin: float | None = None
    esr: float | None = None
    crp: float | None = None
    
    # Cough symptoms
    cough_severity: float | None = None
    cough_duration: float | None = None
    chest_pain: float | None = None
    breathlessness: float | None = None
    fever: float | None = None


# =========================
# Helper Functions
# =========================
def get_xray_prediction(image_bytes: bytes) -> dict:
    """Predict TB from X-ray image"""
    if xray_model is None:
        return {
            "success": False,
            "error": "X-ray model not available due to TensorFlow version incompatibility",
            "message": "Please use blood test or cough analysis instead",
            "is_tb": None,
            "confidence": 0
        }
    
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
        "is_tb": is_tb,
        "success": True
    }


def get_blood_test_prediction(data: dict) -> dict:
    """Predict TB from blood test parameters"""
    if blood_model is None:
        raise HTTPException(status_code=503, detail="Blood test model not available")
    
    # Prepare input data in correct order (WBC_Count, Hemoglobin, ESR, CRP)
    input_data = np.array([[
        data.get('WBC_Count', 0),
        data.get('Hemoglobin', 0),
        data.get('ESR', 0),
        data.get('CRP', 0)
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


def get_combined_prediction(xray_result: dict | None, blood_result: dict | None, cough_result: dict | None) -> dict:
    """
    Combine predictions from multiple models using weighted voting
    to improve overall accuracy
    """
    results = []
    weights = []
    
    # Assign weights based on model reliability
    # Adjusted: Blood test most reliable, X-ray reduced due to accuracy issues
    if xray_result and xray_result.get('success'):
        results.append(xray_result)
        weights.append(0.25)  # X-ray (25%) - Reduced from 40%
    
    if blood_result and blood_result.get('success'):
        results.append(blood_result)
        weights.append(0.45)  # Blood test (45%) - Increased for better accuracy
    
    if cough_result and cough_result.get('success'):
        results.append(cough_result)
        weights.append(0.30)  # Cough symptoms (30%) - Slightly increased
    
    if not results:
        return {
            "success": False,
            "error": "No valid predictions to combine"
        }
    
    # Normalize weights
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]
    
    # Calculate weighted confidence for TB vs No TB
    tb_confidence = 0
    no_tb_confidence = 0
    
    for result, weight in zip(results, weights):
        is_tb = result.get('is_tb', False)
        confidence = result.get('confidence', 0) / 100.0  # Convert to 0-1 scale
        
        if is_tb:
            tb_confidence += confidence * weight
        else:
            no_tb_confidence += confidence * weight
    
    # Determine final prediction
    final_is_tb = tb_confidence > no_tb_confidence
    final_confidence = max(tb_confidence, no_tb_confidence) * 100
    
    # Calculate agreement level
    agreement_count = sum(1 for r in results if r.get('is_tb') == final_is_tb)
    agreement_percentage = (agreement_count / len(results)) * 100 if results else 0
    
    # Determine risk level
    risk_level = "High Risk" if final_is_tb else "Low Risk"
    
    # Adjust risk level based on confidence and agreement
    if final_confidence < 60 or agreement_percentage < 67:
        risk_level = "Moderate Risk" if final_is_tb else "Low-Moderate Risk"
    
    prediction_text = "TB Detected" if final_is_tb else "No TB Detected"
    
    return {
        "success": True,
        "prediction": prediction_text,
        "confidence": round(final_confidence, 2),
        "risk_level": risk_level,
        "is_tb": final_is_tb,
        "models_used": len(results),
        "agreement_percentage": round(agreement_percentage, 2),
        "individual_results": results,
        "methodology": "Weighted ensemble voting (X-ray: 25%, Blood: 45%, Cough: 30%)"
    }


# =========================
# API Routes
# =========================

@app.get("/")
def root():
    models_status = {
        "xray_model": "loaded" if xray_model is not None else "not_available (TensorFlow version issue)",
        "blood_model": "loaded" if blood_model is not None else "not_available",
        "cough_model": "loaded" if cough_model is not None else "not_available"
    }
    
    return {
        "message": "TB Prediction API is running with ENSEMBLE learning!",
        "version": "2.0.0 - Combined Prediction System",
        "models": models_status,
        "endpoints": [
            "/predict/xray",
            "/predict/blood",
            "/predict/cough",
            "/predict/combined (NEW! - Uses all models for better accuracy)"
        ],
        "features": {
            "individual_predictions": "Use single model",
            "combined_prediction": "Uses weighted ensemble of all available models (25% X-ray + 45% Blood + 30% Cough)"
        }
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
    wbc_count: float = Form(...),
    hemoglobin: float = Form(...),
    esr: float = Form(...),
    crp: float = Form(...),
    file: UploadFile = File(None)
):
    """
    Predict TB from blood test report
    Requires 4 parameters: WBC_Count, Hemoglobin, ESR, CRP
    """
    try:
        # If file is uploaded, perform OCR (simplified - you can enhance this)
        if file:
            # TODO: Implement full OCR processing here
            # For now, use provided form data
            pass
        
        data = {
            "WBC_Count": wbc_count,
            "Hemoglobin": hemoglobin,
            "ESR": esr,
            "CRP": crp
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


@app.post("/predict/combined", response_model=PredictionResponse)
async def predict_combined(
    xray_image: UploadFile = File(None),
    wbc_count: float = Form(None),
    hemoglobin: float = Form(None),
    esr: float = Form(None),
    crp: float = Form(None),
    cough_severity: float = Form(None),
    cough_duration: float = Form(None),
    chest_pain: float = Form(None),
    breathlessness: float = Form(None),
    fever: float = Form(None),
):
    """
    Combined prediction using all three models for improved accuracy
    Uses weighted ensemble voting to combine predictions
    Accepts multipart/form-data for mixed file + data upload
    """
    try:
        xray_result = None
        blood_result = None
        cough_result = None
        
        # Get X-ray prediction if image provided
        if xray_image and xray_model is not None:
            try:
                contents = await xray_image.read()
                xray_result = get_xray_prediction(contents)
            except Exception as e:
                print(f"X-ray prediction failed: {e}")
        
        # Get blood test prediction if parameters provided
        if all([wbc_count is not None, hemoglobin is not None, 
                esr is not None, crp is not None]):
            try:
                blood_data = {
                    "WBC_Count": wbc_count,
                    "Hemoglobin": hemoglobin,
                    "ESR": esr,
                    "CRP": crp
                }
                blood_result = get_blood_test_prediction(blood_data)
            except Exception as e:
                print(f"Blood test prediction failed: {e}")
        
        # Get cough prediction if symptoms provided
        if all([cough_severity is not None, cough_duration is not None]):
            try:
                cough_data = {
                    "Cough_Severity": cough_severity,
                    "Cough_Duration": cough_duration,
                    "Chest_Pain": chest_pain or 0,
                    "Breathlessness": breathlessness or 0,
                    "Fever": fever or 0
                }
                cough_result = get_cough_prediction(cough_data)
            except Exception as e:
                print(f"Cough prediction failed: {e}")
        
        # Combine predictions
        combined = get_combined_prediction(xray_result, blood_result, cough_result)
        
        if not combined.get('success'):
            raise HTTPException(status_code=400, detail="At least one prediction method must be provided")
        
        precautions, suggestions = generate_recommendations(combined["is_tb"], combined["risk_level"])
        
        return PredictionResponse(
            success=True,
            prediction=combined["prediction"],
            confidence=combined["confidence"],
            risk_level=combined["risk_level"],
            precautions=precautions,
            suggestions=suggestions,
            details={
                "methodology": combined["methodology"],
                "models_used": combined["models_used"],
                "agreement_percentage": combined["agreement_percentage"]
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
