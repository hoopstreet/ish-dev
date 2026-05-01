#!/usr/bin/env python3
#!/usr/bin/env python3
import json, re
from collections import Counter

class CodePredictor:
    def __init__(self):
        self.common_patterns = {
            'echo': 'echo "text"',
            'python': 'python3 script.py',
            'pip': 'pip install package',
            'git': 'git add . && git commit -m "msg"',
            '# Phase': '# Phase N\necho "command"'
        }
    
    def predict_next(self, current_line):
        for cmd, template in self.common_patterns.items():
            if current_line.startswith(cmd):
                return template
        return None
    
    def complete_phase(self, phase_num):
        return f"# Phase {phase_num + 1}\necho \"Phase {phase_num + 1}\""

predictor = CodePredictor()
print("🔮 Code predictor ready")
