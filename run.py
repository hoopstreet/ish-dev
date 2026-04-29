import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from system.agents.runtime import RuntimeAgent

agent = RuntimeAgent()

def run_agent(task):
    print("\nRUNNING AGENT...\n")
    return agent.execute(task)

def menu():
    while True:
        print("\n===== HOOPSTREET AGENT =====")
        print("1. Run AI Agent")
        print("0. Exit")

        c = input("> ")

        if c == "1":
            t = input("Task: ")
            print(run_agent(t))

        elif c == "0":
            break

menu()
