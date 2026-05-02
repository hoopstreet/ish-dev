#!/usr/bin/env python3
import os

def display_menu():
    os.system('clear')
    print("════════════════════════════════════════════════")
    print("     🚀 ISH-DEV MASTER CONTROLLER v20.0.0")
    print("      📍 Location: Philippines | Time: PHT")
    print("════════════════════════════════════════════════")
    print("\n  [CORE SYSTEMS]")
    print("  1. 🧬 DNA Architect - Deep Scan & Auto-Adopt")
    print("  2. 🔄 Cloud Pulse   - Force Sync GitHub/Supabase")
    print("  3. 🔧 Self-Healing  - Fix Circular Imports")
    
    print("\n  [AFFILIATE NICHES]")
    print("  4. 👕 MK Online     - Apparel & Lifestyle")
    print("  5. 🏀 Hoopstreet    - Sports & Gear")
    print("  6. 🏎️ Daily Drive   - Moto & Car Acc")
    print("  7. 🎮 Budget Acc    - Tech & Gaming")
    
    print("\n  [SYSTEM]")
    print("  0. 🚪 Exit to Shell")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    display_menu()
    choice = input("👉 Select Module (0-7): ")
    if choice == '1': os.system('python3 /root/ish-dev/core/omni_architect.py')
    elif choice == '2': os.system('cd /root/ish-dev && git push origin main --force')
    # Additional logic for niches can be mapped here as the Architect builds them
