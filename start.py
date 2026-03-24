"""
Start both FastAPI backend and Vite frontend
"""
import subprocess
import sys
import time

def start_servers():
    print("🚀 Starting TB Prediction System...")
    print("=" * 50)
    
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
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
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
