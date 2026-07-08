import os
import sys
import subprocess
import time

def start_services():
    print("Starting Adaptive Hybrid Recommender Platform...")
    
    # Start FastAPI Backend in background
    api_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.server:app", "--port", "8000"])
    print("FastAPI Backend started on port 8000")
    
    time.sleep(2) # Wait for backend
    
    # Start Streamlit Frontend
    print("Starting Streamlit UI...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/app_main.py", "--server.port", "8501"])
    
    # On exit, terminate backend
    api_process.terminate()

if __name__ == "__main__":
    start_services()
