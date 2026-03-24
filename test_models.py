"""
Test script to verify all models load correctly
"""
import sys

print("=" * 60)
print("Testing Model Loading")
print("=" * 60)

# Test 1: TensorFlow model
print("\n1. Loading X-ray model (tb_model.h5)...")
try:
    import tensorflow as tf
    xray_model = tf.keras.models.load_model("tb_model (1).h5")
    print("   ✅ X-ray model loaded successfully!")
    print(f"   Model type: {type(xray_model)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Class indices
print("\n2. Loading class indices...")
try:
    import json
    with open("class_indices.json", "r") as f:
        class_indices = json.load(f)
    print("   ✅ Class indices loaded!")
    print(f"   Classes: {class_indices}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Blood test models
print("\n3. Loading blood test models...")
try:
    import joblib
    blood_model = joblib.load("tb_lgbm_model.pkl")
    blood_scaler = joblib.load("tb_scaler.pkl")
    blood_encoder = joblib.load("tb_label_encoder.pkl")
    print("   ✅ Blood test models loaded!")
    print(f"   Model type: {type(blood_model)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: Cough models
print("\n4. Loading cough models...")
try:
    cough_model = joblib.load("cough_model.pkl")
    cough_scaler = joblib.load("scaler.pkl")
    cough_features = joblib.load("features.pkl")
    print("   ✅ Cough models loaded!")
    print(f"   Model type: {type(cough_model)}")
    print(f"   Features: {cough_features}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL MODELS LOADED SUCCESSFULLY!")
print("=" * 60)
print("\nYou can now start the backend server:")
print("  python -m uvicorn main:app --reload")
