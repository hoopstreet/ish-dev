#!/usr/bin/env python3
import sys, os

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🤖 HOOPSTREET AI AGENT")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📋 Commands: status, heal, sync, help, exit")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

while True:
    try:
        cmd = input("\n🌟 Agent > ").strip().lower()
        if cmd in ['exit', 'quit']:
            print("\n🔙 Returning to menu...")
            break
        elif cmd == 'status':
            os.system('/root/ish-dev/core/status.sh')
        elif cmd == 'heal':
            os.system('/root/ish-dev/core/heal.sh')
        elif cmd == 'sync':
            os.system('/root/ish-dev/core/sync.sh')
        elif cmd == 'help':
            print("\nCommands: status, heal, sync, help, exit")
        else:
            print(f"\n📌 Unknown: {cmd}")
    except KeyboardInterrupt:
        break
