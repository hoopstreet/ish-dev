import sys
from core.agent import ai

def loop():
    print("\033[94m🤖 HOOPSTREET OS v3 - CLI MODE\033[0m")
    print("Type 'exit' to stop.")
    
    while True:
        try:
            task = input("\n\033[92mOS > \033[0m")
            if task.lower() in ["exit", "quit"]:
                break
            if not task.strip():
                continue
                
            result = ai.ask(task)
            print(f"\n\033[93mAI:\033[0m\n{result}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    loop()
