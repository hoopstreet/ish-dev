#!/usr/bin/python3
import sys, os

# Target project paths
sys.path.append("/root/Ai-Coder")
from core.ai_brain import GeminiBrain

def main():
    if len(sys.argv) < 2:
        print("Usage: gemini [prompt]")
        return
    
    # 🌀 Processing Visual for iSH
    print("🧠 Agent CLI: Processing task... 🌀")
    
    brain = GeminiBrain()
    prompt = " ".join(sys.argv[1:])
    response = brain.generate_code(prompt)
    
    print(f"\n✅ SUCCESS: Execution Done.")
    print(f"📝 Result: {response[:100]}...")
    print("\n🚀 Successfully synced. What is next? localhost:~#")

if __name__ == "__main__":
    main()
