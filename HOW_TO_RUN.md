# 🚀 How to Run Your TB Prediction System

## Quick Start (3 Easy Steps)

### Step 1: Open Terminal in Project Folder
```bash
cd f:\spandan\projects\tb_predict
```

### Step 2: Run the Startup Script

**Windows Users (Easiest):**
```bash
start.bat
```

**Alternative (Manual):**
```bash
python start.py
```

### Step 3: Open Your Browser
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

That's it! 🎉

---

## Detailed Setup Instructions

### First Time Setup

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- TensorFlow (X-ray model)
- scikit-learn (blood & cough models)
- uvicorn (server)
- And more...

#### 2. Install Node.js Dependencies
```bash
npm install
```

This installs:
- React (UI framework)
- Vite (build tool)
- Tailwind CSS (styling)
- React Router (navigation)
- And more...

#### 3. Start the Application

**Option A: Use the startup script**
```bash
python start.py
```

**Option B: Start manually**

Terminal 1 (Backend):
```bash
uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
npm run dev
```

---

## Using the Application

### Home Page
1. Visit http://localhost:5173
2. You'll see the beautiful home page with:
   - Hero section
   - Features overview
   - ML pipeline preview
   - Statistics

### Making a Prediction

#### Method 1: X-ray Analysis (Most Accurate)

1. **Navigate to Prediction Page**
   - Click "Prediction" in navbar OR
   - Go to http://localhost:5173/prediction

2. **Select X-ray Mode**
   - Click the "X-ray Analysis" card

3. **Upload Image**
   - Click "Upload Chest X-ray Image"
   - Select a chest X-ray image file
   - Preview will appear automatically

4. **Get Results**
   - Click "Start Analysis"
   - Wait 2-3 seconds
   - View detailed results including:
     - Prediction (Normal/TB)
     - Confidence score
     - Risk level
     - Precautions
     - Suggestions

#### Method 2: Blood Test Analysis

1. **Select Blood Test Mode**
   - Click "Blood Test" card on Prediction page

2. **Enter Lab Values**
   Enter values from blood test report:
   - Hemoglobin (g/dL): e.g., 12.5
   - WBC Count (/μL): e.g., 7500
   - RBC Count (million/μL): e.g., 4.5
   - Platelet Count (/μL): e.g., 250000
   - ESR (mm/hr): e.g., 20
   - Lymphocytes (%): e.g., 30
   - Monocytes (%): e.g., 5
   - Neutrophils (%): e.g., 60

3. **Analyze**
   - Click "Start Analysis"
   - Get instant results

#### Method 3: Cough Symptom Analysis

1. **Select Cough Analysis Mode**
   - Click "Cough Analysis" card

2. **Enter Symptoms**
   - Cough Severity: Rate 0-10
   - Cough Duration: Number of days
   - Chest Pain: Yes (1) or No (0)
   - Breathlessness: Yes (1) or No (0)
   - Fever: Yes (1) or No (0)

3. **Get Prediction**
   - Click "Start Analysis"
   - See results immediately

---

## Testing the System

### Quick Test Checklist

✅ **Backend Running:**
- Visit http://localhost:8000
- Should show API info with model status

✅ **Frontend Running:**
- Visit http://localhost:5173
- Should see homepage

✅ **API Documentation:**
- Visit http://localhost:8000/docs
- Should see interactive Swagger UI

✅ **Test Prediction:**
1. Go to prediction page
2. Select any mode
3. Enter test data
4. Click "Start Analysis"
5. Should see results

### Sample Test Data

#### Blood Test Example:
```
Hemoglobin: 11.5
WBC Count: 12000
RBC Count: 4.0
Platelet Count: 150000
ESR: 35
Lymphocytes: 40
Monocytes: 8
Neutrophils: 52
```

#### Cough Analysis Example:
```
Cough Severity: 8
Cough Duration: 21
Chest Pain: 1 (Yes)
Breathlessness: 1 (Yes)
Fever: 1 (Yes)
```

---

## Troubleshooting

### Problem: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Change port in main.py line 368:
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Problem: Can't Connect to Backend

**Error:** Network error in browser

**Solution:**
1. Check if backend is running: http://localhost:8000
2. If not, start it: `uvicorn main:app --reload`
3. Check console for errors

### Problem: Models Not Loading

**Error:** Model loading failed

**Solution:**
1. Verify all .pkl and .h5 files exist
2. Check file sizes (should not be 0 bytes)
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Problem: X-ray Model Error

**Error:** InputLayer deserialization error

**Solution:**
- System still works with blood test and cough analysis
- To fix X-ray model, check TensorFlow version compatibility
- See TROUBLESHOOTING.md for details

---

## Understanding the Results

### Prediction Output

After analysis, you'll see:

1. **Prediction**: The model's diagnosis
   - "TB Positive" / "TB Negative"
   - "TB Detected" / "No TB Detected"
   - "TB Chest X-rays" / "Normal Chest X-rays"

2. **Confidence Score**: How certain the model is (0-100%)
   - Higher = more confident
   - Typically 70-99%

3. **Risk Level**: Overall risk assessment
   - Low Risk: Likely no TB
   - High Risk: Possible TB, consult doctor

4. **Precautions**: Steps to prevent spread

5. **Suggestions**: Recommended actions

---

## Daily Usage Workflow

### For Healthcare Providers:

1. **Morning Setup**
   ```bash
   start.bat
   ```

2. **Patient Screening**
   - Open http://localhost:5173
   - Navigate to Prediction
   - Choose appropriate method
   - Enter patient data
   - Review results with patient

3. **End of Day**
   - Close browser tabs
   - Stop servers (Ctrl+C in terminals)
   - Or just close the terminal windows

### For Researchers:

1. **Access API Directly**
   - Visit http://localhost:8000/docs
   - Test endpoints with Swagger UI
   - Export predictions for analysis

2. **Batch Processing**
   - Use Python scripts to call API
   - Process multiple samples
   - Save results to database

---

## Performance Tips

### For Best Results:

1. **Wait for Full Startup**
   - See "Application startup complete" message
   - All models should load before first use

2. **Quality Inputs**
   - X-ray: Clear, high-resolution images
   - Blood test: Accurate lab values
   - Cough: Honest symptom reporting

3. **First Prediction Delay**
   - First prediction may be slower (model warmup)
   - Subsequent predictions are faster

---

## Advanced Features

### API Access

You can call the API directly:

```bash
# X-ray prediction
curl -X POST http://localhost:8000/predict/xray \
  -F "file=@chest_xray.jpg"

# Blood test prediction
curl -X POST http://localhost:8000/predict/blood \
  -d "hemoglobin=12.5" \
  -d "wbc_count=7000"

# Cough prediction
curl -X POST http://localhost:8000/predict/cough \
  -d "cough_severity=7" \
  -d "cough_duration=14"
```

### Programmatic Access

```python
import requests

# X-ray prediction
files = {'file': open('xray.jpg', 'rb')}
response = requests.post('http://localhost:8000/predict/xray', files=files)
result = response.json()

print(result['prediction'])
print(result['confidence'])
```

---

## Security & Privacy

### Important Notes:

⚠️ **For Research/Educational Use Only**
- Not a replacement for professional medical diagnosis
- Always consult healthcare professionals

⚠️ **Patient Data Privacy**
- Don't store real patient data without proper safeguards
- Comply with HIPAA or local regulations
- Use anonymized data for testing

⚠️ **Production Deployment**
Before deploying publicly:
- Add user authentication
- Enable HTTPS
- Implement rate limiting
- Add logging and monitoring
- Secure environment variables

---

## Support Resources

### Documentation Files:

- 📘 **README.md** - Complete project documentation
- ⚡ **QUICKSTART.md** - Quick setup guide
- 🔧 **TROUBLESHOOTING.md** - Common issues and solutions
- ✅ **SETUP_COMPLETE.md** - Detailed feature list
- 📖 **HOW_TO_RUN.md** - This file

### Getting Help:

1. Check TROUBLESHOOTING.md first
2. Review API docs at /docs endpoint
3. Inspect browser console (F12)
4. Check terminal logs for errors

---

## Success Indicators

### Your System is Working When:

✅ Both servers start without errors  
✅ Frontend loads at http://localhost:5173  
✅ API docs accessible at http://localhost:8000/docs  
✅ Predictions return results in < 5 seconds  
✅ All three modes (X-ray, Blood, Cough) work  
✅ Results display correctly  

---

## What's Next?

### After Confirming Everything Works:

1. **Test with Real Data**
   - Use actual X-ray images
   - Enter real blood test values
   - Document symptoms accurately

2. **Customize UI**
   - Change colors in tailwind.config.js
   - Modify text in components
   - Add your branding

3. **Extend Functionality**
   - Add user accounts
   - Store prediction history
   - Create admin dashboard
   - Implement advanced OCR

4. **Deploy to Production**
   - Choose cloud provider (AWS, GCP, Azure)
   - Set up domain name
   - Configure SSL certificates
   - Implement monitoring

---

## Quick Reference

### URLs:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Commands:
```bash
# Start everything
python start.py

# Backend only
uvicorn main:app --reload

# Frontend only
npm run dev

# Install dependencies
pip install -r requirements.txt
npm install
```

### Ports:
- 8000: Backend API
- 5173: Frontend UI

---

**🎉 You're all set! Start making AI-powered TB predictions now!**

For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
