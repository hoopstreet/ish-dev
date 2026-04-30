import json
from ai.router import ai

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def run(self, task):
        prompt = f"You are {self.name} ({self.role}). Task: {task}. Return only final result."
        return ai.ask(prompt)


class AgentSystem:
    def __init__(self):
        self.planner = Agent("Planner", "break tasks")
        self.coder = Agent("Coder", "write code")
        self.debugger = Agent("Debugger", "fix errors")

    def run(self, task):
        try:
            plan = self.planner.run(task)
            code = self.coder.run(plan)
            return self.debugger.run(code)
        except Exception as e:
            return f"ERROR: {str(e)}"
