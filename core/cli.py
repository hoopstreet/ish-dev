import os
import sys

def main():
    print("🛰️  AI-CODER MECHANIC | Xenia Edition")
    print("-" * 30)
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    
    if cmd == "status":
        print("✅ Core Environment: Ready")
        print(f"📂 Active Path: {os.getcwd()}")
    elif cmd == "push":
        os.system("git add .")
        os.system('git commit -m "🧬 Evolution Update"')
        os.system("git push origin main")
    else:
        print("Commands: status, push")

if __name__ == "__main__":
    main()
