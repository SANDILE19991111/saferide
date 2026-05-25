"""
SafeRide — mobile launcher
Run: python run_mobile.py
Then open http://YOUR_IP:8501 on your phone (same WiFi)
"""
import subprocess, socket, sys

def get_local_ip():
    try:
        import socket as s
        sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except:
        return "localhost"

ip = get_local_ip()
print(f"\n{'='*50}")
print(f"  SafeRide starting...")
print(f"  Local:  http://localhost:8501")
print(f"  Phone:  http://{ip}:8501")
print(f"{'='*50}\n")

subprocess.run([
    sys.executable, "-m", "streamlit", "run", "app.py",
    "--server.port", "8501",
    "--server.address", "0.0.0.0",
    "--server.headless", "true",
    "--browser.gatherUsageStats", "false",
])
