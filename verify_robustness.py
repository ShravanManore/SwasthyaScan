
import requests
import json

BASE_URL = "http://localhost:8000"

def test_combined_with_missing_models():
    print("\n--- Testing Combined Prediction with Missing Models (Simulated) ---")
    
    # Test 1: Only Blood Data
    payload = {
        "wbc_count": 7000,
        "hemoglobin": 13.5,
        "esr": 10,
        "crp": 3.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict/combined", data=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result['success']}")
            print(f"Prediction: {result['prediction']}")
            print(f"Methodology: {result['details']['methodology']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def test_individual_blood_safety():
    print("\n--- Testing Individual Blood Prediction Safety ---")
    payload = {
        "wbc_count": 7000,
        "hemoglobin": 13.5,
        "esr": 10,
        "crp": 3.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict/blood", data=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Blood prediction successful")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Ensure server is running before running this
    print("Please make sure the FastAPI server is running on http://localhost:8000")
    test_individual_blood_safety()
    test_combined_with_missing_models()
