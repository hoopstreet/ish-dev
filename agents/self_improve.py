from core import Orchestrator
from ai_debugger import debug_code

class SelfImprover:
    def __init__(self):
        self.orch = Orchestrator()

    def run(self, code):
        try:
            self.orch.run_cycle(code)
        except Exception as e:
            fix = debug_code(str(e))
            print("AUTO FIX:", fix)

        print("🔁 Cycle complete - system evolving")
