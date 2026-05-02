#!/usr/bin/env python3
import sys, os

print("\n" + "━" * 60)
print("🤖 HOOPSTREET AI AGENT")
print("━" * 60)
print("📋 Commands: status, heal, sync, help, exit")
print("━" * 60)
print()

while True:
    try:
        cmd = input("🌟 Agent > ").strip().lower()
        
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
            print("\nCommands: status, heal, sync, help, exit\n")
        elif cmd == '':
            continue
        else:
            print(f"\n📌 Executing: {cmd}")
            os.system(cmd)
            print()
    except KeyboardInterrupt:
        print("\n🔙 Returning to menu...")
        break
    except EOFError:
        break

print()
