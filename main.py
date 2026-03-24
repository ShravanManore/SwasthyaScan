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
    
    try:
        # Load and preprocess image
        image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        print(f"✓ Image loaded: {image_pil.size}, mode: {image_pil.mode}")
        
        # Convert to OpenCV format for CLAHE enhancement
        open_cv_image = np.array(image_pil) 
        # Convert RGB to BGR for OpenCV
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        
        # Apply CLAHE to enhance contrast (helpful for medical images)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced_gray = clahe.apply(gray)
        
        # Convert back to RGB for the model
        enhanced_rgb = cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2RGB)
        
        # Resize and normalize
        image_resized = cv2.resize(enhanced_rgb, (224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(image_resized)
        img_array = tf.expand_dims(img_array, 0) / 255.0  # Normalize
        
        # Predict
        predictions = xray_model.predict(img_array, verbose=0)
        
        if predictions is None or len(predictions) == 0:
            raise ValueError("X-ray model returned no predictions")
            
        confidence = float(np.max(predictions)) * 100
        predicted_class = int(np.argmax(predictions))
        
        print(f"📊 Prediction: class={predicted_class}, confidence={confidence:.2f}%")
        
        # Safe access to sub-elements
        raw_probs = predictions[0] if len(predictions) > 0 else [0.5, 0.5]
        print(f"   Raw predictions: {raw_probs}")
        
        # Map to class name
        class_names = {v: k for k, v in class_indices.items()}
        prediction_name = class_names.get(predicted_class, "Unknown")
        print(f"   Class name: {prediction_name}")
        
        # Determine risk level - class 1 is TB, class 0 is Normal
        is_tb = (predicted_class == 1)
        risk_level = "High Risk" if is_tb else "Low Risk"
        
        print(f"   Result: is_tb={is_tb}, risk_level={risk_level}")
        
        return {
            "prediction": prediction_name,
            "confidence": round(float(confidence), 2),
            "risk_level": risk_level,
            "is_tb": is_tb,
            "success": True,
            "probabilities": raw_probs.tolist() if hasattr(raw_probs, 'tolist') else list(raw_probs)
        }
    except Exception as e:
        print(f"✗ X-ray prediction error: {e}")
        import traceback
        traceback.print_exc()
        raise


def get_blood_test_prediction(data: dict) -> dict:
    """Predict TB from blood test parameters"""
    if blood_model is None or blood_scaler is None or blood_encoder is None:
        return {
            "success": False,
            "error": "Blood test model or components not available",
            "is_tb": False,
            "confidence": 0
        }
    
    # Prepare input data in correct order (WBC_Count, Hemoglobin, ESR, CRP)
    input_data = np.array([[
        float(data.get('WBC_Count', 0)),
        float(data.get('Hemoglobin', 0)),
        float(data.get('ESR', 0)),
        float(data.get('CRP', 0))
    ]])
    
    # Scale
    input_scaled = blood_scaler.transform(input_data)
    
    # Predict
    preds = blood_model.predict(input_scaled)
    if len(preds) == 0:
        raise ValueError("Blood model returned no predictions")
        
    prediction_encoded = preds[0]
    prediction = blood_encoder.inverse_transform([prediction_encoded])[0]
    
    # Get probabilities
    probs_list = blood_model.predict_proba(input_scaled)
    if len(probs_list) == 0:
        raise ValueError("Blood model returned no probabilities")
        
    probs = probs_list[0]
    confidence = float(np.max(probs)) * 100
    
    is_tb = prediction == 1 or (isinstance(prediction, str) and "TB" in prediction.upper())
    risk_level = "High Risk" if is_tb else "Low Risk"
    
    return {
        "prediction": "TB Positive" if is_tb else "TB Negative",
        "confidence": round(float(confidence), 2),
        "risk_level": risk_level,
        "is_tb": is_tb,
        "success": True,
        "probabilities": probs.tolist() if hasattr(probs, 'tolist') else list(probs)
    }


def get_cough_prediction(data: dict) -> dict:
    """Predict TB from cough sound features"""
    if cough_model is None or cough_scaler is None:
        return {
            "success": False,
            "error": "Cough model or components not available",
            "is_tb": False,
            "confidence": 0
        }
    
    # Prepare input data in correct feature order
    input_values = []
    for feature in cough_features:
        value = float(data.get(feature, 0))
        input_values.append(value)
    
    input_data = np.array([input_values])
    
    # Scale
    input_scaled = cough_scaler.transform(input_data)
    
    # Predict
    preds = cough_model.predict(input_scaled)
    if len(preds) == 0:
        raise ValueError("Cough model returned no predictions")
        
    prediction = int(preds[0])
    
    # Get probabilities
    probs_list = cough_model.predict_proba(input_scaled)
    if len(probs_list) == 0:
        raise ValueError("Cough model returned no probabilities")
        
    probs = probs_list[0]
    confidence = float(np.max(probs)) * 100
    
    is_tb = prediction == 1
    risk_level = "High Risk" if is_tb else "Low Risk"
    
    return {
        "prediction": "TB Detected" if is_tb else "No TB Detected",
        "confidence": round(float(confidence), 2),
        "risk_level": risk_level,
        "is_tb": is_tb,
        "success": True,
        "probabilities": probs.tolist() if hasattr(probs, 'tolist') else list(probs)
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
    # Adjusted: Equal weights for all models to test accuracy
    if xray_result and xray_result.get('success'):
        results.append(xray_result)
        weights.append(0.34)  # X-ray (34%) - Balanced weight
    
    if blood_result and blood_result.get('success'):
        results.append(blood_result)
        weights.append(0.33)  # Blood test (33%) - Balanced
    
    if cough_result and cough_result.get('success'):
        results.append(cough_result)
        weights.append(0.33)  # Cough symptoms (33%) - Balanced
    
    if not results:
        return {
            "success": False,
            "error": "No valid predictions to combine"
        }
    
    # Normalize weights so they sum to 1.0
    total_weight = sum(weights)
    if total_weight > 0:
        weights = [w / total_weight for w in weights]
    
    # SOFT VOTING ENSEMBLE
    # ---------------------
    # Calculate weighted mean probabilities
    # X-ray: [Normal (0), TB (1)]
    # Blood: [Negative (0), Positive (1)]
    # Cough: [Negative (0), Positive (1)]
    
    weighted_p0 = 0
    weighted_p1 = 0
    
    for result, weight in zip(results, weights):
        probs = result.get('probabilities', [0.5, 0.5])
        weighted_p0 += probs[0] * weight
        weighted_p1 += probs[1] * weight
        
        # SENSITIVITY BOOST: If any model is extremely confident (>90%) about TB, 
        # add a significant bonus to the TB probability
        if result.get('is_tb') and result.get('confidence', 0) > 90:
            weighted_p1 += 0.15 # Veto power/Bonus
            
    # Re-normalize
    total_p = weighted_p0 + weighted_p1
    final_p0 = weighted_p0 / total_p
    final_p1 = weighted_p1 / total_p
    
    # DECISION THRESHOLD TUNING (Sensitivity focus)
    # Default is 0.5, but we use a lower threshold to avoid False Negatives
    TB_THRESHOLD = 0.38 
    
    final_is_tb = final_p1 > TB_THRESHOLD
    final_confidence = (final_p1 if final_is_tb else final_p0) * 100
    
    # Calculate agreement level
    agreement_count = sum(1 for r in results if r.get('is_tb') == final_is_tb)
    agreement_percentage = (agreement_count / len(results)) * 100 if results else 0
    
    # Determine risk level with high sensitivity
    prediction_text = "No TB Detected"
    if final_is_tb:
        prediction_text = "TB Detected"
        if final_p1 > 0.7 or agreement_percentage >= 67:
            risk_level = "High Risk"
        else:
            risk_level = "Moderate Risk"
    else:
        if final_p1 > 0.25: # Borderline cases
            risk_level = "Low-Moderate Risk"
            prediction_text = "No TB Detected (Monitor Symptoms)"
        else:
            risk_level = "Low Risk"
            prediction_text = "No TB Detected"
    
    prediction_text = "TB Detected" if final_is_tb else "No TB Detected"
    
    # Determine methodology text based on available models
    method_parts = []
    model_names = []
    
    # Re-identify which models were actually used to label weights correctly
    if xray_result and xray_result.get('success'): model_names.append("X-ray")
    if blood_result and blood_result.get('success'): model_names.append("Blood")
    if cough_result and cough_result.get('success'): model_names.append("Cough")
    
    for name, weight in zip(model_names, weights):
        method_parts.append(f"{name}:{weight*100:.0f}%")
    
    methodology_text = f"Soft-voting ensemble ({', '.join(method_parts)}) with Sensitivity Boost"
    
    return {
        "success": True,
        "prediction": prediction_text,
        "confidence": round(float(final_confidence), 2),
        "risk_level": risk_level,
        "is_tb": final_is_tb,
        "models_used": len(results),
        "agreement_percentage": round(float(agreement_percentage), 2),
        "individual_results": results,
        "methodology": methodology_text
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
            "combined_prediction": "Uses weighted ensemble of all available models (34% X-ray + 33% Blood + 33% Cough)"
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
