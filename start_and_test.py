import subprocess
import time
import sys

def main():
    print("Starting FastAPI server...")
    server = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", "8005"])
    
    # Wait for server to bind
    print("Waiting 6 seconds for server to start...")
    time.sleep(6)
    
    print("Running tests...")
    test_proc = subprocess.run([sys.executable, "test_system.py"])
    
    print("Shutting down server...")
    server.terminate()
    server.wait()

if __name__ == "__main__":
    main()
