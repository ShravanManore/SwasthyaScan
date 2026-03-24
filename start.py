"""
Start both FastAPI backend and Vite frontend
"""
import subprocess
import sys
import os
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        import tensorflow
        print("✅ Python dependencies found")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            raise Exception("Node.js not found")
    except Exception:
        print("❌ Node.js not found or not in PATH")
        print("   Please install Node.js from https://nodejs.org/")
        return False
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm found: {result.stdout.strip()}")
        else:
            raise Exception("npm not found")
    except Exception:
        print("❌ npm not found or not in PATH")
        print("   npm comes with Node.js. Make sure Node.js is properly installed.")
        return False
    
    # Check if node_modules exists
    if not os.path.exists("node_modules"):
        print("⚠️  node_modules not found. Installing...")
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✅ Frontend dependencies installed")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    else:
        print("✅ Frontend dependencies already installed")
    
    return True

def start_servers():
    print("🚀 Starting TB Prediction System...")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please fix the issues above and try again.")
        return
    
    print("\n" + "=" * 50)
    
    # Start FastAPI backend
    print("📡 Starting FastAPI backend on http://localhost:8000")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Wait for backend to start
    time.sleep(3)
    
    # Start Vite frontend
    print("🎨 Starting Vite frontend on http://localhost:5173")
    
    # Try different ways to run npm on Windows
    try:
        # Try using npm.cmd on Windows
        if os.name == 'nt':
            frontend_process = subprocess.Popen(
                ["npm.cmd", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
        else:
            frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
    except FileNotFoundError:
        # If npm.cmd fails, try full path or npx
        print("⚠️  Trying alternative npm command...")
        try:
            frontend_process = subprocess.Popen(
                ["npx", "vite"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
        except FileNotFoundError:
            print("❌ Could not find npm or npx. Please install Node.js properly.")
            print("\nManual start instructions:")
            print("1. Open a new terminal")
            print("2. Navigate to project folder")
            print("3. Run: npm run dev")
            backend_process.terminate()
            return
    
    print("=" * 50)
    print("✅ Both servers started successfully!")
    print("📊 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:5173")
    print("📖 API Docs: http://localhost:8000/docs")
    print("=" * 50)
    print("\nPress Ctrl+C to stop all servers\n")
    
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    start_servers()
