import os
import json

from system.agents.engine import AgentSystem
from memory.store import save

system = AgentSystem()

def run_agent(task):
    result = system.run(task)
    save({"task": task, "result": result})
    return result


def git_sync():
    print("🔄 Git Sync...")
    os.system("cd ~/ish-dev && git add .")
    os.system('cd ~/ish-dev && git commit -m "auto sync iSH agent"')
    os.system("cd ~/ish-dev && git push origin main")


def view_memory():
    try:
        with open("memory/logs.json") as f:
            data = json.load(f)

        print("\n🧠 LAST TASKS:")
        for d in data[-5:]:
            print("•", d["task"])
    except:
        print("No memory found")


def menu():
    while True:
        print("\n===== HOOPSTREET AGENT =====")
        print("1. Run AI Agent")
        print("2. Git Sync")
        print("3. View Memory")
        print("0. Exit")

        c = input("> ")

        if c == "1":
            t = input("Task: ")
            print("\n", run_agent(t))

        elif c == "2":
            git_sync()

        elif c == "3":
            view_memory()

        elif c == "0":
            break


menu()


# 🔥 GLOBAL COMMAND ALIAS (IMPORTANT FIX)
