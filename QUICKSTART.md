# Quick Start Guide

## Prerequisites Check
- ✅ Python 3.9+ installed
- ✅ Node.js 16+ installed
- ✅ All model files present in project root

## Step-by-Step Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Windows Users**: If you get an error with TensorFlow, try:
```bash
pip install tensorflow==2.15.0 --force-reinstall
```

### 2. Install Node.js Dependencies
```bash
npm install
```

### 3. Start the Application

**Option A - Automatic (Recommended):**
```bash
python start.py
```

This will start both backend and frontend servers automatically.

**Option B - Manual:**

Terminal 1 (Backend):
```bash
uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
npm run dev
```

### 4. Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## Testing Each Prediction Mode

### Test X-ray Prediction
1. Go to Prediction page
2. Click "X-ray Analysis" card
3. Upload any chest X-ray image
4. Click "Start Analysis"
5. Wait for prediction results

### Test Blood Test Prediction
1. Go to Prediction page
2. Click "Blood Test" card
3. Enter sample values:
   - Hemoglobin: 12.5
   - WBC Count: 7500
   - RBC Count: 4.5
   - Platelet Count: 250000
   - ESR: 20
   - Lymphocytes: 30
   - Monocytes: 5
   - Neutrophils: 60
4. Click "Start Analysis"

### Test Cough Prediction
1. Go to Prediction page
2. Click "Cough Analysis" card
3. Enter symptoms:
   - Cough Severity: 7
   - Cough Duration: 14 days
   - Chest Pain: Yes (1)
   - Breathlessness: Yes (1)
   - Fever: Yes (1)
4. Click "Start Analysis"

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify all .pkl and .h5 files exist
- Run: `python -c "import tensorflow; print(tensorflow.__version__)"`

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS is enabled in main.py

### Model loading errors
- Verify file paths in main.py
- Check file sizes (should not be 0 bytes)
- Re-download corrupted model files

## Success Indicators

✅ Backend starts with message: "Application startup complete"
✅ All models load successfully (check console output)
✅ Frontend loads at http://localhost:5173
✅ API docs accessible at http://localhost:8000/docs
✅ Predictions return results within 2-3 seconds

## Next Steps

After confirming everything works:
1. Test with real data
2. Customize UI colors in tailwind.config.js
3. Add authentication if needed
4. Deploy to production server

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review API docs at /docs endpoint
- Inspect browser console and terminal logs
