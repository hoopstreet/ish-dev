import sys
sys.path.insert(0, '/root')
from fast_visual import FastVisualAgent

agent = FastVisualAgent()
print("🔧 Starting quick heal...\n")
agent.heal("/root/broken.py")

print("\n📄 Fixed code:")
with open('/root/broken.py', 'r') as f:
    print(f.read())
