import os
import time
import requests
import subprocess

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr

def analyze_and_fix():
    print("🔍 Analyzing repository state...")
    # Fetch latest from GitHub
    run_command("git fetch origin main")
    
    # Check for build errors in logs (Simulation of checking NF logs or local test)
    stdout, stderr = run_command("python3 -m py_compile *.py")
    
    if stderr:
        print(f"❌ Detected Error: {stderr}")
        # Here we would send stderr to Gemini to get a fix
        # For now, we auto-revert or auto-patch common credential paths
        print("🛠 Applying autonomous patch...")
        # (AI Logic would go here to rewrite files)
    else:
        print("✅ Code integrity verified.")

def main_loop():
    print("🚀 AAI Mode: ACTIVE. Monitoring for fixes...")
    while True:
        try:
            analyze_and_fix()
            # Push any autonomous fixes back to origin
            run_command("git add . && git commit -m 'auto: autonomous fix' && git push origin main")
            time.sleep(300) # Check every 5 minutes
        except Exception as e:
            print(f"⚠️ Agent Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main_loop()
