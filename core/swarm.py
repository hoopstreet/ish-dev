import subprocess
class AgentSwarm:
    def __init__(self, project_name):
        self.project = project_name
    def plan(self, task):
        return subprocess.getoutput(f"agent 'PLAN: {task} for {self.project}'")
    def code(self, step):
        return subprocess.getoutput(f"agent 'EXECUTE: {step}'")
    def test(self):
        return subprocess.getoutput("pytest || echo 'FAIL'")
    def fix(self, error):
        return subprocess.getoutput(f"agent 'FIX: {error}'")
