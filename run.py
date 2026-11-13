import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
processes = []

def shutdown(*_):
    for process in processes:
        if process.poll() is None:
            process.terminate()
    raise SystemExit(0)

if __name__ == "__main__":
    os.chdir(ROOT)
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app",
                                "--host", "127.0.0.1", "--port", "8000"])
    processes.append(backend)
    time.sleep(2)
    frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run",
                                 "frontend/dashboard.py", "--server.port", "8501"])
    processes.append(frontend)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    print("Dashboard: http://localhost:8501")
    print("API documentation: http://127.0.0.1:8000/docs")
    try:
        while any(process.poll() is None for process in processes):
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown()
