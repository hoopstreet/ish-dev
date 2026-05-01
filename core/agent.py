import sys
from core.orchestrator import AgentCLI
if __name__ == "__main__":
    agent = AgentCLI()
    task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Initialize System"
    agent.execute(task)
