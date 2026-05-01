#!/bin/sh
clear
echo "🚀 ONE-CLICK SETUP FOR iSH AUTO AGENT"
echo "====================================="
echo ""

# Run all phases in sequence
python3 /root/smart_phase.py << 'SETUP'
# Phase 1: Imports
import subprocess, json, time, sys, os, threading, urllib.request
from pathlib import Path
from datetime import datetime

# Phase 2: Class definition
class CompleteAgent:
    def __init__(self):
        self.gemini_keys = ["AIzaSyDBHr3FRFAXexCYVYvolHWozEzsy5nZIas","AIzaSyBRmO1HL4NZ5k_8mOKFvO6QwIs83KtkTxA","AIzaSyCvqCQu0TCWnmEDFZmV1_P_fKxcw4kOBTY","AIzaSyC2RY14NPQYVN5NQZJciivyQuWME9Hc9Yg","AIzaSyBTyzstJWpdKAjGHMfBAINfd8c7kpL0XAY"]
        self.gemini_failed = [False]*5
        self.or_key = "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"
        self.current = "gemini-0"
        self.dna = Path("/root/DNA.md")
        self.spin = False

# Phase 3: Spinner methods
    def _spin(self, msg):
        chars = ['⣾','⣽','⣻','⢿','⡿','⣟','⣯','⣷']
        i = 0
        while self.spin:
            sys.stdout.write(f'\r{chars[i%8]} {msg}... ')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    def _start(self, msg):
        self.spin = True
        threading.Thread(target=self._spin, args=(msg,), daemon=True).start()
    
    def _stop(self, ok=True, msg=""):
        self.spin = False
        time.sleep(0.2)
        sys.stdout.write('\r' + ' '*50 + '\r')
        print(f"{'✅' if ok else '❌'} {msg}")

print("✅ Agent ready!")
SETUP

echo ""
echo "🎉 Setup complete!"
echo "Run: /root/run_safe_agent.sh"
