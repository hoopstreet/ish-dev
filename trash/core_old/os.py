from core.engine import main as run_engine
from core.self_writer import generate_module
from core.evolver import evolve_codebase

def menu():
    print("""
💎 HOOPSTREET V15 OS

1. Run AI Engine
2. Generate Module
3. Evolve System
0. Exit
""")

    while True:
        c=input("> ")

        if c=="1":
            run_engine()

        if c=="2":
            t=input("Task: ")
            print(generate_module(t))

        if c=="3":
            print(evolve_codebase("full system analysis"))

        if c=="0":
            break

if __name__=="__main__":
    menu()
