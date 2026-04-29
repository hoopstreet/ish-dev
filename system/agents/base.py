class Agent:
    def __init__(self, name, role, ai):
        self.name = name
        self.role = role
        self.ai = ai

    def run(self, task):
        prompt = f"You are {self.name}\nRole: {self.role}\nTask:\n{task}\nReturn final answer only."
        return self.ai.ask(prompt)
