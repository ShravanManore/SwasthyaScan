# =====================================
# TB COUGH PREDICTION - SINGLE FILE APP (FIXED)
# =====================================

from flask import Flask, request, render_template_string
import joblib
import numpy as np

app = Flask(__name__)

# Load model, scaler, and features
model = joblib.load("cough_model.pkl")
scaler = joblib.load("scaler.pkl")

# Load feature names (VERY IMPORTANT)
features = joblib.load("features.pkl")  # must be saved during training

# =========================
# HTML TEMPLATE
# =========================
html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>TB Detection System</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-align: center;
            padding-top: 80px;
        }
        input, button {
            padding: 10px;
            margin: 8px;
            border-radius: 8px;
            border: none;
        }
        button {
            background-color: #ff7b54;
            color: white;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            font-size: 22px;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <h1>🫁 TB Detection (Cough Model)</h1>

    <form method="POST" action="/predict">

        <input type="number" step="any" name="Cough_Severity" placeholder="Cough Severity" required><br>
        <input type="number" step="any" name="Cough_Duration" placeholder="Cough Duration" required><br>
        <input type="number" step="any" name="Chest_Pain" placeholder="Chest Pain (0/1)" required><br>
        <input type="number" step="any" name="Breathlessness" placeholder="Breathlessness (0/1)" required><br>
        <input type="number" step="any" name="Fever" placeholder="Fever (0/1)" required><br>

        <button type="submit">Predict</button>
    </form>

    {% if prediction is not none %}
        <div class="result">
            {% if prediction == 1 %}
                ⚠️ TB Detected
            {% else %}
                ✅ No TB Detected
            {% endif %}
        </div>
    {% endif %}

</body>
</html>
"""

# =========================
# ROUTES
# =========================

@app.route('/')
def home():
    return render_template_string(html_page, prediction=None)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect inputs dynamically based on features list
        input_values = []
        for feature in features:
            value = float(request.form[feature])
            input_values.append(value)

        # Convert to array
        input_data = np.array([input_values])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_scaled)[0]

        return render_template_string(html_page, prediction=prediction)

    except Exception as e:
        return f"Error: {str(e)}"


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)