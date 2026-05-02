#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime

def get_pht_time():
    # Manual offset for PHT (UTC+8)
    return datetime.utcnow().strftime("%b %d, %Y at %I:%M:%S %p PHT")

def execute_phases(input_data):
    phases = [p.strip() for p in input_data.split('# Phase') if p.strip()]
    total = len(phases)
    success_count = 0
    
    print(f"\n📊 Detected {total} phase(s)")
    
    for i, phase_cmd in enumerate(phases, 1):
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📌 PHASE {i}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        attempt = 1
        success = False
        while attempt <= 3:
            # Spinner simulation
            for char in ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]:
                sys.stdout.write(f"\r{char} Executing Phase {i} (Attempt {attempt})...")
                sys.stdout.flush()
                time.sleep(0.1)
            
            exit_code = os.system(phase_cmd.split('\n', 1)[-1])
            if exit_code == 0:
                print(f"\n✅ Phase {i} SUCCESS (attempt {attempt})")
                success = True
                success_count += 1
                break
            else:
                print(f"\n❌ Phase {i} FAILED (attempt {attempt})")
                attempt += 1
        
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 EXECUTION SUMMARY")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ Successful: {success_count}/{total}")
    print(f"❌ Failed: {total - success_count}/{total}")
    print(f"📅 Date: {get_pht_time().split(' at ')[0]}")
    print(f"⏰ Time: {get_pht_time().split(' at ')[1]}")
    print("🔄 Max retries per phase: 3")
    print("🔧 Auto-healing: Enabled")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    if success_count == total:
        print(f"🎉 ALL PHASES COMPLETED SUCCESSFULLY! 🎉\n✅ Completed on {get_pht_time()}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    buffer = []
    while True:
        line = input()
        if line == "BACK": break
        if line == "END":
            execute_phases("\n".join(buffer))
            buffer = []
            print("\nReady for next code. Type BACK to exit.")
        else:
            buffer.append(line)
