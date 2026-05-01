import subprocess
import sys

def ask_gemini(err_msg):
    try:
        # Calls your /usr/local/bin/gemini shell script
        cmd = ["gemini", f"Analyze this error and provide a fix for iSH: {err_msg}"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(ask_gemini(sys.argv[1]))
    else:
        print("🤖 Usage: python3 ai_debugger.py 'your error message'")
