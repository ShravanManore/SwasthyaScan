# Manual Start Guide (If start.py fails)

## Problem: "The system cannot find the file specified"

This error means Node.js or npm is not properly installed or not in your system PATH.

---

## Solution 1: Install Node.js Properly

### Step 1: Download and Install Node.js
1. Go to https://nodejs.org/
2. Download **LTS version** (recommended)
3. Run installer
4. **IMPORTANT**: Make sure to check "Add to PATH" during installation
5. Complete installation

### Step 2: Verify Installation
Open a **NEW** terminal/PowerShell window and run:
```bash
node --version
npm --version
```

You should see version numbers like:
```
v20.x.x
10.x.x
```

If you see the versions, proceed to Step 3.

### Step 3: Install Frontend Dependencies
```bash
cd f:\spandan\projects\tb_predict
npm install
```

### Step 4: Start the Application

**Terminal 1 - Backend:**
```bash
python -m uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

---

## Solution 2: Use Alternative Start Method

If `start.py` still fails, use this manual method:

### Terminal 1: Start Backend
```bash
cd f:\spandan\projects\tb_predict
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Leave this terminal running!

### Terminal 2: Start Frontend
```bash
cd f:\spandan\projects\tb_predict
npm install
npm run dev
```

Leave this terminal running too!

### Access the App
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Solution 3: Fix PATH on Windows

If Node.js is installed but commands don't work:

### Method A: Add to PATH Manually
1. Find where Node.js is installed (usually `C:\Program Files\nodejs\`)
2. Press `Win + R`, type `sysdm.cpl`, press Enter
3. Click "Advanced" tab
4. Click "Environment Variables"
5. Under "System variables", find "Path", click "Edit"
6. Click "New", add: `C:\Program Files\nodejs\`
7. Click "OK" on all windows
8. **Restart your terminal/computer**

### Method B: Use Full Path
Instead of `npm`, use the full path:
```bash
"C:\Program Files\nodejs\npm.cmd" run dev
```

---

## Solution 4: Quick Fix Using start.bat

The `start.bat` file handles Windows paths better:

```bash
start.bat
```

Or if that fails, edit `start.bat` and change the npm line to use full path.

---

## Verification Checklist

✅ Node.js installed from https://nodejs.org/  
✅ npm command works in NEW terminal window  
✅ `npm install` completed successfully  
✅ `node_modules` folder exists in project  
✅ Can run `npm run dev` manually  

---

## Common Issues After Installation

### Issue: "npm is not recognized"
**Solution**: Close ALL terminals and open a new one, or restart computer.

### Issue: "EACCES permission denied"
**Solution**: Run terminal as Administrator (right-click → Run as Administrator)

### Issue: "Port 5173 already in use"
**Solution**: 
```bash
# Kill the process using port 5173
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F
```

### Issue: "Cannot find module 'vite'"
**Solution**: 
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## Easiest Method (Recommended for Beginners)

1. **Install Node.js** from https://nodejs.org/ (LTS version)
2. **Restart computer**
3. **Open NEW PowerShell**
4. Run these commands:

```bash
cd f:\spandan\projects\tb_predict
npm install
```

Wait for installation to complete...

Then open TWO terminals:

**Terminal 1:**
```bash
python -m uvicorn main:app --reload
```

**Terminal 2:**
```bash
npm run dev
```

Visit http://localhost:5173 🎉

---

## Still Having Issues?

### Check These:
1. Is Node.js version 16 or higher? (`node --version`)
2. Are you in the correct folder? (`pwd`)
3. Does `package.json` exist? (`ls`)
4. Any error messages when running `npm install`?

### Get Help:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Look at error messages carefully
- Make sure you're in `f:\spandan\projects\tb_predict` folder

---

## Quick Reference

### Commands You Need:
```bash
# One-time setup
npm install

# Start backend (Terminal 1)
python -m uvicorn main:app --reload

# Start frontend (Terminal 2)
npm run dev
```

### URLs to Remember:
- Frontend: http://localhost:5173
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

**Good luck! The system will work once Node.js is properly installed.** 🚀
