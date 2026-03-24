# Troubleshooting Guide

## Common Issues and Solutions

### 1. TensorFlow Model Loading Error

**Error**: `Error when deserializing class 'InputLayer'`

**Cause**: Version mismatch between the TensorFlow version used to train the model and the installed version.

**Solutions**:

#### Option A: Use Alternative Model Format (Recommended)
If your X-ray model was saved in a different format, try converting it:
```python
# If you have access to the original training code
model.save('tb_model.h5', save_format='h5')
```

#### Option B: Install Compatible TensorFlow Version
Check which version was used to train the model and install that specific version.

#### Option C: Continue Without X-ray Model
The system will still work with blood test and cough analysis even if X-ray model fails to load.

### 2. Port Already in Use

**Error**: `Address already in use` or `OSError: [WinError 10048]`

**Solution**: Change the port number
```bash
# In main.py, change line 368:
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use port 8001 instead

# Or specify when running:
uvicorn main:app --reload --port 8001
```

### 3. Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Ensure virtual environment is activated and dependencies are installed
```bash
pip install -r requirements.txt --force-reinstall
```

### 4. Frontend Can't Connect to Backend

**Error**: Network errors in browser console

**Solutions**:
1. Verify backend is running: http://localhost:8000/docs
2. Check CORS settings in `main.py`
3. Update API URL in `src/utils/apiService.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000'; // Ensure this matches backend port
   ```

### 5. Model Files Not Found

**Error**: `FileNotFoundError`

**Solution**: Verify all model files exist in project root:
- `tb_model (1).h5`
- `class_indices.json`
- `tb_lgbm_model.pkl`
- `tb_scaler.pkl`
- `tb_label_encoder.pkl`
- `cough_model.pkl`
- `scaler.pkl`
- `features.pkl`

### 6. npm Install Fails

**Error**: Various npm installation errors

**Solutions**:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### 7. Slow Prediction Times

**Issue**: Predictions taking too long

**Solutions**:
1. Models load on startup - wait for "Application startup complete" message
2. First prediction may be slower due to model warmup
3. Consider using GPU acceleration for TensorFlow

### 8. Tesseract OCR Not Found (for Blood Test OCR Feature)

**Error**: `TesseractNotFoundError`

**Solution**: Install Tesseract OCR
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Add to system PATH

## Verification Steps

### Test Backend Independently

1. Start backend:
   ```bash
   uvicorn main:app --reload
   ```

2. Check console output for:
   ```
   ✓ X-ray model loaded successfully
   ✓ Blood test model loaded successfully
   ✓ Cough model loaded successfully
   INFO:     Application startup complete.
   ```

3. Visit API docs: http://localhost:8000/docs
4. Test each endpoint using Swagger UI

### Test Frontend Independently

1. Ensure backend is running
2. Start frontend:
   ```bash
   npm run dev
   ```

3. Visit: http://localhost:5173
4. Open browser DevTools (F12)
5. Check for network errors

### Test Each Prediction Mode

#### X-ray Prediction
```bash
curl -X POST http://localhost:8000/predict/xray \
  -F "file=@path/to/test_image.jpg"
```

#### Blood Test Prediction
```bash
curl -X POST http://localhost:8000/predict/blood \
  -d "hemoglobin=12.5" \
  -d "wbc_count=7000" \
  -d "rbc_count=4.5" \
  -d "platelet_count=250000" \
  -d "esr=20" \
  -d "lymphocytes=30" \
  -d "monocytes=5" \
  -d "neutrophils=60"
```

#### Cough Prediction
```bash
curl -X POST http://localhost:8000/predict/cough \
  -d "cough_severity=7" \
  -d "cough_duration=14" \
  -d "chest_pain=1" \
  -d "breathlessness=1" \
  -d "fever=1"
```

## Performance Optimization

### For Production Deployment

1. **Use Gunicorn with Uvicorn workers**:
   ```bash
   pip install gunicorn
   gunicorn -k uvicorn.workers.UvicornWorker main:app --workers 4
   ```

2. **Enable model caching**: Models are already loaded at startup

3. **Add request timeout**:
   ```python
   @app.post("/predict/xray", response_model=PredictionResponse)
   async def predict_xray(file: UploadFile = File(...)):
       # Add timeout decorator if needed
   ```

4. **Use async database logging** for predictions

5. **Add Redis** for caching frequent predictions

## Getting Help

If issues persist:

1. Check logs in terminal/console
2. Enable debug mode in `main.py`:
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
   ```
3. Review API documentation at /docs
4. Check browser console for frontend errors
5. Verify all dependencies match versions in requirements.txt

## Known Limitations

1. **X-ray Model**: May require specific TensorFlow version used during training
2. **OCR Feature**: Blood test OCR is basic - consider implementing advanced OCR
3. **Batch Processing**: Current implementation handles one request at a time
4. **File Size Limits**: No upload size limits configured (add if needed)

## Security Considerations

For production use:

1. **Add Authentication**: Implement user login/JWT tokens
2. **Rate Limiting**: Add slowapi or similar for rate limiting
3. **Input Validation**: Enhance validation for all inputs
4. **HTTPS**: Always use HTTPS in production
5. **Environment Variables**: Store sensitive data in .env file
6. **Logging**: Implement comprehensive logging
7. **Monitoring**: Add health checks and monitoring
